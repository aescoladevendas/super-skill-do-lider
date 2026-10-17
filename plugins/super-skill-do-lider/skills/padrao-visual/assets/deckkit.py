# -*- coding: utf-8 -*-
"""deckkit: biblioteca do padrão visual (skill padrao-visual).

O que faz: monta decks 16:9 (página de 1600 x 900 px) em HTML e converte em PDF com o
Chrome sem janela (headless). Traz os componentes do padrão: capa com prateleira de fotos,
capítulos, números-manchete, tabelas, gráficos, investimento, régua, linha do tempo, listas
numeradas e fechamento.

Entradas: o conteúdo de cada página, passado pelos métodos de Deck (cover, chapter, slide).
Cores, fonte e cores das marcas vêm do arquivo de configuração da empresa
(saidas.identidade_visual e produtos.cores_marcas), com padrão no código quando a chave falta.
O logo é opcional e entra por parâmetro: Deck(..., logos=[logo('caminho/logo.svg')]).

Saídas: arquivo .html e .pdf com o mesmo nome e, para a conferência visual, PNGs com as
páginas em montagem 2x2 (lista devolvida por save()).

Como rodar:
    import sys; sys.path.insert(0, '<pasta da skill padrao-visual>/assets')
    from deckkit import *
    d = Deck('Empresa × Cliente · Tema · Período', logos=[logo('logo_empresa.svg')])
    d.cover(['Título', 'linha 2'], 'Frase de apoio.', ['Nome · Cargo'], 'Mês de AAAA.', 'Continuação em cinza.')
    d.slide('ETIQUETA', 'Afirmação. Continuação.', tab(cab, linhas, total), read='leitura curta')
    d.save('saida.pdf')

Para trocar uma cor só neste deck: import deckkit; deckkit.DESTAQUE = '#0071E3' antes de salvar.

Regras visuais (não negociáveis): fundo cinza em toda página; um card branco (raio 18px, sem
sombra, sem borda) por bloco; nunca card dentro de card; cor de destaque só no que é
mandatório; verde, amarelo e vermelho só em números com significado; títulos em dois tons;
zero travessão.
"""
import base64, os, re, shutil, subprocess, sys
from string import Template

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------- configuração da empresa (opcional: sem ela valem os padrões abaixo)
def _carregar_config():
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'scripts')))
        from configuracao import carregar
        return carregar()
    except (Exception, SystemExit):
        return {}


def _obter(cfg, chave, padrao=None):
    atual = cfg
    for parte in chave.split('.'):
        if isinstance(atual, dict) and parte in atual:
            atual = atual[parte]
        else:
            return padrao
    return atual


CFG = _carregar_config()
_ID = _obter(CFG, 'saidas.identidade_visual', {}) or {}


def _cor(chave, padrao):
    v = _ID.get(chave)
    return v if isinstance(v, str) and re.fullmatch(r'#[0-9A-Fa-f]{6}', v) else padrao


# ---------------- tokens (nome do token = chave em saidas.identidade_visual)
FUNDO = _cor('fundo', '#F5F5F7')              # fundo de todas as páginas
CARD = _cor('card', '#FFFFFF')                # cards: raio 18px, sem sombra, sem borda
GRAFITE = _cor('grafite', '#1D1D1F')          # texto principal, títulos, totais
CINZA = _cor('cinza_texto', '#6E6E73')        # continuação do título, subtítulo, leitura
APOIO = _cor('apoio', '#86868B')              # apoio fraco
LINHA = _cor('linha', '#D2D2D7')              # linha sob o cabeçalho da tabela, trilho da linha do tempo
LINHA_TABELA = _cor('linha_tabela', '#ECECEF')  # linhas entre registros
DESTAQUE = _cor('destaque', '#FF007F')        # só o mandatório
ETIQUETA = _cor('etiqueta', '#B64400')        # etiqueta acima do título, rótulos de card
LINK = _cor('link', '#0066CC')                # participantes na capa
VERDE = _cor('verde', '#248A3D')              # crescimento
AMARELO = _cor('amarelo', '#B88400')          # atenção
VERMELHO = _cor('vermelho', '#D70015')        # perda e falta
BARRA_ANTERIOR = _cor('barra_anterior', LINHA)
BARRA_REFERENCIA = _cor('barra_referencia', CINZA)
MARCAS = dict(_obter(CFG, 'produtos.cores_marcas', {}) or {})   # nome da marca: cor (só em tabelas)
FONTE_NOME = _ID.get('fonte_web') or 'Inter'
FONT = '"%s", "Helvetica Neue", Helvetica, Arial, sans-serif' % FONTE_NOME
CARREGAR_FONTE_WEB = bool(_ID.get('carregar_fonte_web', True))   # busca a fonte na Google Fonts ao gerar


def _chrome():
    cands = [_obter(CFG, 'ambiente.binarios.chrome'),
             '/Applications/Utilities/Google Chrome.app/Contents/MacOS/Google Chrome',
             '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
    cands += [shutil.which(n) for n in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome')]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


CHROME = _chrome()


# ---------------- imagens
def img(path):
    """arquivo de imagem → data URI (a imagem vai embutida no HTML)."""
    ext = os.path.splitext(path)[1].lower().strip('.')
    mime = {'svg': 'image/svg+xml', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'webp': 'image/webp'}.get(ext, 'image/png')
    with open(path, 'rb') as fh:
        return f'data:{mime};base64,' + base64.b64encode(fh.read()).decode()


def logo(path, cor_svg=None):
    """logo da empresa ou do cliente (caminho passado pelo usuário). cor_svg troca o
    branco de um SVG (fill:#FFFFFF) por outra cor, útil para logo branco sobre fundo cinza."""
    if cor_svg and path.lower().endswith('.svg'):
        with open(path, encoding='utf-8') as fh:
            s = fh.read().replace('fill:#FFFFFF', 'fill:' + cor_svg).replace('fill="#FFFFFF"', f'fill="{cor_svg}"')
        return 'data:image/svg+xml;base64,' + base64.b64encode(s.encode()).decode()
    return img(path)


def placeholder(texto='Foto do cliente (site oficial)'):
    """marcador desenhado em traço fino para o lugar da foto. Sem bloco cinza dentro do card."""
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid meet">'
         f'<g fill="none" stroke="{LINHA}" stroke-width="3" stroke-linejoin="round">'
         f'<rect x="200" y="110" width="200" height="140" rx="16"/>'
         f'<circle cx="352" cy="148" r="14"/>'
         f'<polyline points="212,236 262,178 300,214 330,190 388,236"/></g>'
         f'<text x="300" y="300" text-anchor="middle" font-size="22" fill="{APOIO}" '
         f'font-family=\'{FONT}\'>{texto}</text></svg>')
    return 'data:image/svg+xml;base64,' + base64.b64encode(s.encode('utf-8')).decode()


# ---------------- números no padrão BR
def n0(x): return f'{x:,.0f}'.replace(',', '.')
def d1(x): return f'{x:.1f}'.replace('.', ',')
def mil(x): return f'{x/1e3:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + ' mil'
def mi(x, casas=1): return 'R$ ' + f'{x/1e6:,.{casas}f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + ' Mi'
def rsk(x): return 'R$ ' + n0(round(x / 1e3)) + ' mil'
def pc(x, d=0): return f'{x*100:+.{d}f}%'.replace('.', ',')
def p0(x, d=0): return f'{x*100:.{d}f}%'.replace('.', ',')


def var(x, d=1, atencao=None):
    """variação colorida: verde cresce, vermelho cai, amarelo quando abs(x) < atencao."""
    c = VERDE if x >= 0 else VERMELHO
    if atencao is not None and abs(x) < atencao:
        c = AMARELO
    return f'<b style="color:{c}">{pc(x, d)}</b>'


def marca(nome):
    """nome da marca na cor própria (produtos.cores_marcas); demais em grafite. Só em tabelas de marca."""
    return f'<b style="color:{MARCAS[nome]}">{nome}</b>' if nome in MARCAS else f'<b>{nome}</b>'


def destaque(txt): return f'<span style="color:{DESTAQUE};font-weight:700">{txt}</span>'


# ---------------- componentes de conteúdo
def tab(head, rows, total=None, cls=''):
    """cls: '' padrão · 'big' poucas linhas · 'mid' · 'tight' muitas linhas · 'nw' sem quebra."""
    t = f'<table class="{cls}"><tr>' + ''.join(f'<th>{x}</th>' for x in head) + '</tr>'
    for r in rows:
        t += '<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>'
    if total:
        t += '<tr class="tot">' + ''.join(f'<td>{x}</td>' for x in total) + '</tr>'
    return t + '</table>'


def kpi(label, value, sub='', cor=None):
    cor = cor or GRAFITE
    return f'<div class="card"><div class="cl">{label}</div><div class="cv" style="color:{cor}">{value}</div><div class="cs">{sub}</div></div>'


def kpis(*cards): return '<div class="cards4">' + ''.join(cards) + '</div>'
def stack(*cards): return '<div class="cards1">' + ''.join(cards) + '</div>'


def statement(*items):
    """até 3 números gigantes: items = (label, valor, sub, cor)."""
    return '<div class="stmt">' + ''.join(f'<div class="st"><div class="stl">{a}</div><div class="stv" style="color:{c}">{v}</div><div class="sts">{s}</div></div>' for a, v, s, c in items) + '</div>'


def hero(label, value, sub=''):
    """número-manchete na cor de destaque (ex.: valor da proposta)."""
    return f'<div class="hero"><div class="stl">{label}</div><div class="hv">{value}</div><div class="hs">{sub}</div></div>'


def two(a, b, wide_left=False):
    """duas colunas, cada uma vira um card branco. wide_left=True: 1,55 x 1."""
    return f'<div class="{"two7" if wide_left else "two"}"><div>{a}</div><div>{b}</div></div>'


def invest(pct, valor, sub, parts, rotulo='Investimento'):
    """bloco de investimento: pct e valor em manchete + composição. parts = [(label, pct, detalhe)]."""
    li = ''.join(f'<div class="ic"><div class="stl">{a}</div><div class="icv">{p}</div><div class="ics">{s}</div></div>' for a, p, s in parts)
    return f'<div class="inv"><div class="ih"><div class="stl">{rotulo}</div><div class="ihv">{pct}</div><div class="ihm">{valor}</div><div class="hs">{sub}</div></div><div class="i3">{li}</div></div>'


def timeline(items):
    """items = [(data, texto)] · pontos na cor de destaque."""
    return '<div class="tl">' + ''.join(f'<div class="tli"><div class="tld">{a}</div><div class="tlt">{b}</div></div>' for a, b in items) + '</div>'


def numbered(items, cols=2):
    """items = [(titulo, texto)] · numeração 01, 02 na cor de destaque."""
    return f'<div class="acts" style="grid-template-columns:repeat({cols},1fr)">' + ''.join(f'<div class="act"><div class="an">{i+1:02d}</div><div class="acth">{t}</div><div>{x}</div></div>' for i, (t, x) in enumerate(items)) + '</div>'


def checklist(items):
    """lista do fechamento: valores em <b> grafite."""
    return '<div class="chk">' + ''.join(f'<div class="ck"><span class="cn">{i+1:02d}</span><span>{t}</span></div>' for i, t in enumerate(items)) + '</div>'


def pillars(items, regua=None):
    """items = [(n, nome, pts, desc, [(cod, item, pts)])] · regua = [(ating, pct, valor)]."""
    h = '<div class="pcards">'
    for n, nome, pts, desc, its in items:
        li = ''.join(f'<div class="pit"><span class="pin">{a}</span><span class="pil">{b}</span><span class="pip">{c} pts</span></div>' for a, b, c in its)
        h += f'<div class="pcard"><div class="ph1"><div class="pnum">{n}</div><div><div class="pk">Pilar {n}</div><div class="pn">{nome}</div></div><div class="ppt">{pts} pts</div></div><div class="pdesc">{desc}</div>{li}</div>'
    h += '</div>'
    if regua:
        h += '<div class="rgs">' + ''.join(f'<div class="rg"><div class="rgl">ATINGIMENTO</div><div class="rgv">{a}</div><div class="rga">➜</div><div class="rgp">{p}</div><div class="rgr">{v}</div></div>' for a, p, v in regua) + '</div>'
    return h


def note(t): return f'<div class="note">{t}</div>'


# ---------------- gráficos SVG
def bars(labels, old, new, n_old, n_new, unit='', fmt=None, H=430, W=1400):
    """barras agrupadas: período anterior cinza, atual na cor de destaque. Sem eixo, sem grade."""
    fmt = fmt or (lambda v: n0(v))
    l, b, t = 70, 60, 30
    mx = max([v for v in old + new if v] + [1]) * 1.15
    gw = (W - l - 10) / len(labels)
    bw = gw * 0.34
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family=\'{FONT}\'>']
    for i, lab in enumerate(labels):
        x = l + i * gw + gw * 0.14
        for j, (v, c) in enumerate(((old[i], BARRA_ANTERIOR), (new[i], DESTAQUE))):
            if v is None:
                continue
            h = (H - b - t) * v / mx
            y = H - b - h
            s.append(f'<rect x="{x + j*(bw+4):.0f}" y="{y:.0f}" width="{bw:.0f}" height="{h:.0f}" fill="{c}" rx="7"/>')
            if j == 1:
                s.append(f'<text x="{x + j*(bw+4) + bw/2:.0f}" y="{y-8:.0f}" font-size="15" fill="{GRAFITE}" text-anchor="middle" font-weight="bold">{fmt(v)}</text>')
        s.append(f'<text x="{x + bw:.0f}" y="{H-b+26}" font-size="18" fill="{GRAFITE}" text-anchor="middle" font-weight="bold">{lab}</text>')
    s.append(f'<text x="{l}" y="18" font-size="16" fill="{CINZA}"><tspan fill="{BARRA_ANTERIOR}">●</tspan> {n_old}    <tspan fill="{DESTAQUE}">●</tspan> {n_new}    {("(" + unit + ")") if unit else ""}</text></svg>')
    return ''.join(s)


def hbars(items, fmt=None, W=760):
    """barras horizontais de variação: verde positivo, vermelho negativo."""
    fmt = fmt or (lambda v: pc(v))
    rh = 54
    H = 30 + rh * len(items)
    mid = W * 0.52
    mx = max(abs(v) for _, v in items) * 1.2 or 1
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family=\'{FONT}\'><line x1="{mid}" x2="{mid}" y1="10" y2="{H-10}" stroke="{APOIO}"/>']
    for i, (lab, v) in enumerate(items):
        y = 20 + i * rh
        w = (W - mid - 90) * abs(v) / mx
        c = VERDE if v >= 0 else VERMELHO
        x = mid if v >= 0 else mid - w
        s.append(f'<text x="{mid-12 if v>=0 else mid+12}" y="{y+24}" font-size="19" fill="{GRAFITE}" text-anchor="{"end" if v>=0 else "start"}" font-weight="bold">{lab}</text>')
        s.append(f'<rect x="{x:.0f}" y="{y+4}" width="{max(3,w):.0f}" height="30" fill="{c}" rx="5"/>')
        s.append(f'<text x="{(x+w+10) if v>=0 else (x-10):.0f}" y="{y+26}" font-size="19" fill="{c}" text-anchor="{"start" if v>=0 else "end"}" font-weight="bold">{fmt(v)}</text>')
    return ''.join(s) + '</svg>'


def columns(items, fmt=None, W=900, H=440):
    """colunas largas (ex.: ano anterior, ano atual, meta). items = [(rotulo 'linha1|linha2', valor, cor)]."""
    fmt = fmt or n0
    l, b, t = 40, 70, 40
    mx = max(v for _, v, _ in items) * 1.15
    gw = (W - l) / len(items)
    bw = gw * 0.55
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family=\'{FONT}\'>']
    for i, (lab, v, c) in enumerate(items):
        x = l + i * gw + gw * 0.22
        h = (H - b - t) * v / mx
        y = H - b - h
        s.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{h:.0f}" fill="{c}" rx="14"/>')
        s.append(f'<text x="{x+bw/2:.0f}" y="{y-12:.0f}" font-size="24" fill="{GRAFITE}" text-anchor="middle" font-weight="bold">{fmt(v)}</text>')
        for k, part in enumerate(lab.split('|')):
            s.append(f'<text x="{x+bw/2:.0f}" y="{H-b+30+k*22}" font-size="18" fill="{GRAFITE}" text-anchor="middle" font-weight="{"bold" if k==0 else "normal"}">{part}</text>')
    return ''.join(s) + '</svg>'


# ---------------- título em dois tons
def two_tone(t):
    """'Afirmação. Continuação' → afirmação em grafite e continuação em cinza (separa em '; ', ': ' ou '. ')."""
    for sep in ('; ', ': ', '. '):
        if sep in t:
            p, q = t.split(sep, 1)
            q = q.rstrip('.')
            return f'{p}. <span class="g">{q[0].upper() + q[1:]}.</span>'
    return t


CSS = Template('''@page { size: 1600px 900px; margin: 0; }
* { box-sizing: border-box; box-shadow: none !important; }
body { margin: 0; background: $FUNDO; font-family: $FONT; color: $GRAFITE; -webkit-font-smoothing: antialiased; font-feature-settings: "tnum" 1; }
.s { width: 1600px; height: 900px; padding: 56px 80px 64px; display: flex; flex-direction: column; position: relative; page-break-after: always; overflow: hidden; background: $FUNDO; }
.eb { color: $ETIQUETA; font-weight: 600; font-size: 17px; letter-spacing: .01em; text-transform: uppercase; }
h1 { font-size: 48px; font-weight: 600; margin: 10px 0 0; line-height: 1.1; letter-spacing: -0.015em; max-width: 1400px; } .g { color: $CINZA; }
.subh { font-size: 21px; line-height: 1.4; color: $CINZA; margin-top: 14px; max-width: 1300px; }
.body { margin-top: 28px; flex: 1; min-height: 0; display: flex; flex-direction: column; }
.foot { position: absolute; bottom: 22px; left: 80px; right: 80px; display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: $CINZA; }
.foot .fl { display: flex; gap: 16px; align-items: center; } .foot img { height: 26px; border-radius: 6px; } .foot img:first-child { height: 20px; border-radius: 0; }
/* cards: branco, raio 18, sem sombra, sem borda; nunca aninhados */
.panel, .card, .st, .pcard, .rg, .tl, .two > div, .two7 > div, .ih, .i3, .pc, .chi { background: $CARD; border-radius: 18px; }
.panel { padding: 34px 40px 30px; flex: 1; min-height: 0; display: flex; flex-direction: column; justify-content: center; }
.cdesc { font-size: 19px; color: $CINZA; line-height: 1.45; margin-bottom: 22px; max-width: 1250px; }
.two, .two7 { display: grid; gap: 20px; flex: 1; } .two { grid-template-columns: 1fr 1fr; } .two7 { grid-template-columns: 1.55fr 1fr; }
.two > div, .two7 > div { padding: 32px 36px; }
.two7 > div:has(.cards1) { background: none; padding: 0; }
table { width: 100%; border-collapse: collapse; }
th { font-size: 14px; font-weight: 600; color: $CINZA; text-align: left; padding: 0 12px 12px; border-bottom: 1px solid $LINHA; vertical-align: bottom; }
td { font-size: 22px; padding: 14px 12px; border-bottom: 1px solid $LINHA_TABELA; } td:first-child, th:first-child { padding-left: 0; }
table.big td { font-size: 26px; padding: 15px 12px; } table.mid td { font-size: 18px; padding: 9px 12px; } table.mid th { font-size: 14px; }
table.tight td { font-size: 16px; padding: 7px 12px; } table.tight th { font-size: 13px; padding-bottom: 8px; } table.nw td { white-space: nowrap; }
td b { font-weight: 600; } td small { color: $CINZA; font-size: 15px; } tr.tot td { font-weight: 600; border-bottom: none; border-top: 1px solid $GRAFITE; }
.cards4 { display: grid; grid-template-columns: repeat(4,1fr); gap: 20px; } .cards1 { display: grid; gap: 20px; height: 100%; }
.card { padding: 28px 30px 26px; } .cl { font-size: 15px; color: $ETIQUETA; font-weight: 600; text-transform: uppercase; } .cv { font-size: 52px; font-weight: 600; margin: 10px 0 8px; letter-spacing: -0.02em; line-height: 1.05; } .cs { font-size: 17px; color: $CINZA; line-height: 1.4; }
.stmt { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; flex: 1; } .st { padding: 40px; display: flex; flex-direction: column; justify-content: center; }
.stl { font-size: 15px; font-weight: 600; color: $ETIQUETA; text-transform: uppercase; } .stv { font-size: 112px; font-weight: 600; letter-spacing: -0.035em; line-height: 1; margin-top: 14px; } .sts { font-size: 19px; color: $CINZA; margin-top: 14px; line-height: 1.4; }
.hero { margin: 0 0 18px; } .hv { font-size: 104px; font-weight: 700; color: $DESTAQUE; letter-spacing: -0.03em; line-height: 1; margin-top: 8px; } .hs { font-size: 22px; color: $CINZA; margin-top: 12px; } .hs b { color: $GRAFITE; }
.inv { display: grid; grid-template-columns: 1.15fr 1fr; gap: 20px; align-items: start; } .ih { padding: 30px 40px; } .i3 { padding: 14px 36px; }
.ihv { font-size: 128px; font-weight: 700; color: $DESTAQUE; letter-spacing: -0.035em; line-height: 1; margin-top: 10px; white-space: nowrap; } .ihm { font-size: 64px; font-weight: 700; letter-spacing: -0.03em; line-height: 1; margin-top: 6px; }
.ic { display: grid; grid-template-columns: 1fr 150px; padding: 16px 0; border-top: 1px solid $LINHA; align-items: center; } .ic:first-child { border-top: none; }
.icv { grid-column: 2; grid-row: 1 / span 2; font-size: 64px; font-weight: 700; color: $DESTAQUE; text-align: right; letter-spacing: -0.03em; } .ics { grid-column: 1; font-size: 17px; color: $CINZA; margin-top: 4px; } .ics b { color: $GRAFITE; }
.tl { display: grid; grid-template-columns: repeat(4,1fr); margin-top: 20px; position: relative; padding: 26px 36px 22px; } .tl:before { content: ''; position: absolute; top: 34px; left: 36px; right: 36px; height: 2px; background: $LINHA; }
.tli { position: relative; padding-top: 30px; padding-right: 20px; } .tli:before { content: ''; position: absolute; top: 0; left: 0; width: 18px; height: 18px; border-radius: 50%; background: $DESTAQUE; }
.tld { font-size: 24px; font-weight: 600; } .tlt { font-size: 17px; margin-top: 4px; color: $CINZA; }
.acts { display: grid; gap: 0 56px; } .act { display: grid; grid-template-columns: 56px 1fr; gap: 0 14px; padding: 22px 0; border-top: 1px solid $LINHA_TABELA; font-size: 18px; line-height: 1.4; color: $CINZA; }
.act .an { font-size: 30px; font-weight: 600; color: $DESTAQUE; line-height: 1; grid-row: span 2; } .acth { font-weight: 600; color: $GRAFITE; font-size: 22px; margin-bottom: 4px; }
.chk { display: grid; } .ck { display: grid; grid-template-columns: 64px 1fr; align-items: baseline; font-size: 25px; padding: 20px 0; border-top: 1px solid $LINHA_TABELA; } .ck:first-child { border-top: none; } .ck .cn { font-size: 24px; font-weight: 600; color: $DESTAQUE; } .ck b { font-weight: 700; }
.pcards { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; } .pcard { padding: 26px 30px 18px; }
.ph1 { display: flex; align-items: center; gap: 14px; } .pnum { font-size: 48px; font-weight: 600; line-height: 1; color: $DESTAQUE; } .pk { font-size: 12px; font-weight: 600; color: $ETIQUETA; text-transform: uppercase; } .pn { font-size: 28px; font-weight: 600; } .ppt { margin-left: auto; font-size: 26px; font-weight: 600; } .pdesc { font-size: 16px; color: $CINZA; margin: 12px 0 6px; min-height: 44px; }
.pit { display: flex; align-items: center; padding: 11px 0; border-top: 1px solid $LINHA_TABELA; font-size: 19px; } .pin { color: $CINZA; width: 42px; font-size: 15px; } .pil { font-weight: 600; } .pip { margin-left: auto; font-weight: 600; }
.rgs { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; margin-top: 20px; } .rg { display: flex; align-items: baseline; flex-wrap: wrap; gap: 12px; padding: 18px 26px; }
.rgl { font-size: 12px; color: $ETIQUETA; font-weight: 600; } .rgv { font-size: 44px; font-weight: 600; } .rga { color: $DESTAQUE; font-size: 30px; } .rgp { font-size: 64px; font-weight: 700; color: $DESTAQUE; letter-spacing: -0.03em; } .rgr { flex-basis: 100%; font-size: 17px; color: $CINZA; }
.note { font-size: 14px; color: $CINZA; margin-top: 12px; }
/* capa: cabeçalho em duas colunas + prateleira de 3 cards */
.cover { padding: 70px 80px; } .chdr { display: flex; justify-content: space-between; align-items: flex-start; }
.ctit { font-size: 104px; font-weight: 600; letter-spacing: -0.015em; line-height: 1.02; }
.cside { text-align: right; max-width: 560px; } .cside .cq { font-size: 32px; font-weight: 600; line-height: 1.18; } .cside a { display: block; color: $LINK; font-size: 18px; margin-top: 12px; text-decoration: none; }
.cvl { display: flex; align-items: center; gap: 18px; margin-top: 18px; } .cvl img { height: 52px; border-radius: 10px; } .cvl img:first-child { height: 40px; border-radius: 0; } .x { font-size: 24px; color: $CINZA; }
.shelfh { font-size: 28px; font-weight: 600; margin-top: 40px; } .shelf { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; margin-top: 18px; }
.pc { overflow: hidden; height: 440px; display: flex; flex-direction: column; } .pc .pt { padding: 20px 26px 10px; } .pc .ey { font-size: 12px; font-weight: 600; color: $ETIQUETA; text-transform: uppercase; } .pc .nm { font-size: 24px; font-weight: 600; margin-top: 4px; } .pc .ds { font-size: 15px; color: $CINZA; margin-top: 4px; } .pc img { width: 100%; flex: 1; object-fit: cover; min-height: 0; }
/* capítulo */
.chap { justify-content: center; } .chg { display: grid; grid-template-columns: 1fr 1.05fr; gap: 56px; align-items: center; flex: 1; }
.chn { font-size: 20px; font-weight: 600; color: $ETIQUETA; text-transform: uppercase; } .cht { font-size: 78px; font-weight: 600; letter-spacing: -0.015em; margin-top: 14px; line-height: 1.04; }
.chi { overflow: hidden; height: 600px; } .chi img { width: 100%; height: 100%; object-fit: cover; }
img.ph { object-fit: contain !important; }
''')


def _css():
    return CSS.substitute(FUNDO=FUNDO, CARD=CARD, GRAFITE=GRAFITE, CINZA=CINZA, LINHA=LINHA,
                          LINHA_TABELA=LINHA_TABELA, DESTAQUE=DESTAQUE, ETIQUETA=ETIQUETA, LINK=LINK, FONT=FONT)


def _foto(im):
    """devolve (src, classe): foto passada pelo usuário ou o marcador desenhado."""
    return (im, '') if im else (placeholder(), ' class="ph"')


class Deck:
    """deck 16:9 no padrão. footer = texto do rodapé; logos = [logo('empresa.svg'), logo('cliente.png')] (opcional)."""

    def __init__(self, footer, logos=None, title='Apresentação'):
        self.footer, self.logos, self.title, self.pages = footer, list(logos or []), title, []

    def _foot(self):
        lg = ''.join(f'<img src="{x}">' for x in self.logos)
        return f'<div class="foot"><span>{self.footer} · {len(self.pages) + 1}</span><span class="fl">{lg}</span></div>'

    def cover(self, title_lines, quote, people, shelf_head, shelf_sub, shelf=None):
        """shelf = [(eyebrow, nome, descricao, img_datauri ou None, object_position)] · até 3 cards.
        Sem foto (None), o card recebe o marcador desenhado."""
        lg = '<div class="x">×</div>'.join(f'<img src="{x}">' for x in self.logos)
        lg = f'<div class="cvl">{lg}</div>' if lg else ''
        ppl = ''.join(f'<a>{p} ›</a>' for p in people)
        sh = ''
        if shelf:
            cards = []
            for e, n, d, im, pos in shelf:
                src, cls = _foto(im)
                cards.append(f'<div class="pc"><div class="pt"><div class="ey">{e}</div><div class="nm">{n}</div><div class="ds">{d}</div></div><img src="{src}"{cls} style="object-position:{pos}"></div>')
            sh = '<div class="shelf">' + ''.join(cards) + '</div>'
        self.pages.append(f'<section class="s cover"><div class="chdr"><div><div class="ctit">{"<br>".join(title_lines)}</div>{lg}</div><div class="cside"><div class="cq">{quote}</div>{ppl}</div></div><div class="shelfh">{shelf_head} <span class="g">{shelf_sub}</span></div>{sh}</section>')

    def chapter(self, n, title, sub, image=None):
        """capítulo: título em dois tons à esquerda e foto em card à direita (sem foto: marcador)."""
        src, cls = _foto(image)
        self.pages.append(f'<section class="s chap"><div class="chg"><div><div class="chn">Capítulo {n}</div><div class="cht">{title}. <span class="g">{sub}</span></div></div><div class="chi"><img src="{src}"{cls}></div></div>{self._foot()}</section>')

    def slide(self, eyebrow, title, body, read=None):
        """body livre (kpis, statement, two, invest, pillars) fica direto no cinza; qualquer outro vira 1 card."""
        free = any(k in body for k in ('class="cards4', 'class="stmt', 'class="pcards', 'class="two', 'class="inv'))
        sub = f'<div class="subh">{read}</div>' if (read and free) else ''
        if not free:
            body = '<div class="panel">' + (f'<div class="cdesc">{read}</div>' if read else '') + body + '</div>'
        self.pages.append(f'<section class="s"><div class="top"><div class="eb">{eyebrow}</div><h1>{two_tone(title)}</h1>{sub}</div><div class="body">{body}</div>{self._foot()}</section>')

    def html(self):
        fonte = ''
        if CARREGAR_FONTE_WEB:
            fam = FONTE_NOME.replace(' ', '+')
            fonte = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fam}:wght@400;600;700&display=block">'
        h = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{self.title}</title>{fonte}<style>{_css()}</style></head><body>{"".join(self.pages)}</body></html>'
        if chr(0x2014) in h or chr(0x2013) in h:   # travessão e meia-risca
            raise ValueError('travessão ou meia-risca encontrado no texto: o padrão proíbe')
        return h

    def save(self, pdf_path, qa=True):
        """grava HTML e PDF (1600x900 por página). qa=True devolve os PNGs de conferência 2x2."""
        if not CHROME:
            raise RuntimeError('Chrome não encontrado: informe ambiente.binarios.chrome na configuração')
        pdf_path = os.path.abspath(pdf_path)
        html_path = os.path.splitext(pdf_path)[0] + '.html'
        with open(html_path, 'w', encoding='utf-8') as fh:
            fh.write(self.html())
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=10000',
                        f'--print-to-pdf={pdf_path}', 'file://' + html_path], capture_output=True)
        if not os.path.exists(pdf_path):
            raise RuntimeError('o Chrome não gerou o PDF: confira o caminho e rode de novo')
        if qa:
            return qa_montage(pdf_path)
        return pdf_path


def qa_montage(pdf_path, per=4):
    """gera PNGs 2x2 para a conferência visual obrigatória antes de entregar."""
    import fitz
    d = fitz.open(pdf_path)
    W, H = 1600 * 0.45, 900 * 0.45
    out = []
    for i in range(0, len(d), per):
        o = fitz.open()
        pg = o.new_page(width=W * 2, height=H * 2)
        for k in range(per):
            if i + k < len(d):
                pg.show_pdf_page(fitz.Rect((k % 2) * W, (k // 2) * H, (k % 2 + 1) * W, (k // 2 + 1) * H), d, i + k)
        f = os.path.splitext(pdf_path)[0] + f'_qa{i//per}.png'
        pg.get_pixmap(dpi=110).save(f)
        out.append(f)
    return out
