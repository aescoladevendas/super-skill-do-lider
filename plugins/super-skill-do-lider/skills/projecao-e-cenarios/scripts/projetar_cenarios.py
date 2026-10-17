# -*- coding: utf-8 -*-
"""Projeção por cliente e cenários (queda, estabilização, crescimento) para a melhor estimativa (BE).

Motor (parâmetros em `projecao` do arquivo de configuração):
  1. ritmo curto = média(mês fechado, mês em curso projetado). O mês em curso se projeta pelo dia
     útil, LIMITADO ao maior mês do ano do cliente; se já chegou a 90% do mês fechado, é "mês feito".
  2. ritmo longo = média dos seis meses até o mês fechado (só positivos).
  3. BASE = 50% curto + 50% longo.
  4. ESTABILIZAÇÃO = BASE × sazonalidade do próprio cliente no ano anterior
     (mês alvo ÷ média dos dois meses anteriores), limitada entre 0,6 e 1,4.
  5. QUEDA = ESTABILIZAÇÃO × 0,90. CRESCIMENTO = maior entre ×1,075 e o necessário para o
     acumulado do ano fechar +7,5%, com teto de 1,5× ou a meta.
  6. PROJEÇÃO (vai para o BE) = ESTABILIZAÇÃO + regras de evidência:
     (a) mês em curso zerado e mês fechado > 0 → base = mês fechado
     (b) sem venda nos dois meses → média do ano
     (c) piso de 60% da carteira aberta
     (d) contas com régua de verba no trimestre (no último mês do trimestre): puxar até o gap da
         régua (85% da meta do trimestre), com teto de 1,3× a estabilização
  7. Mix por marca = mix dos três últimos meses do cliente (senão, o mix padrão da regional).
  8. Data de subida = sexta-feira da 2ª semana do mês alvo, nunca depois do limite de pedido.

Entradas (uma das duas):
  --dados dados_painel.json        contrato do painel (skill painel-de-indicadores)
  --historico historico.csv        colunas: codigo, cliente, executivo, mes (AAAA-MM), marca, caixas
     + --carteira carteira.csv     colunas: codigo, caixas      (opcional)
Opcionais:
  --metas metas.csv                colunas: codigo, meta (meta do mês alvo, em caixas)
  --be arquivo_oficial.xlsx        escreve data de subida e caixas por marca numa CÓPIA do BE oficial
  --mes-alvo AAAA-MM  --dias-decorridos N  [--dias-totais N]  --saida pasta  --falar

Saída: planilha com a aba PROJECAO_<mês> (memória de cálculo cliente a cliente + resumo dos
cenários) e, com --be, a cópia do arquivo oficial com sufixo. Fórmulas do arquivo oficial nunca
são alteradas: só as colunas de data de subida e de caixas por marca.
"""
import argparse, collections, csv, datetime, json, os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from configuracao import carregar, obter, caminho, nomes_executivos  # noqa: E402

PADROES = {  # usados se a chave não estiver no arquivo de configuração
    'peso_ritmo_curto': 0.5, 'mes_feito_se_atingiu': 0.90, 'sazonalidade_min': 0.6,
    'sazonalidade_max': 1.4, 'fator_queda': 0.90, 'fator_crescimento': 1.075, 'ambicao_ytd': 0.075,
    'teto_crescimento': 1.5, 'piso_carteira': 0.60, 'teto_puxada_meta': 1.3, 'regua_meta': 0.85,
    'base_minima_sazonalidade': 300, 'carteira_relevante': 500, 'micro_conta': 200,
}


def p(cfg, chave):
    return obter(cfg, 'projecao.' + chave, PADROES.get(chave))


def mes_soma(m, n):
    a, b = int(m[:4]), int(m[5:7]) - 1 + n
    return f'{a + b // 12:04d}-{b % 12 + 1:02d}'


def br(v, casas=0):
    """Número no padrão brasileiro: 146.338 ou 1,5."""
    t = f'{v:,.{casas}f}'
    return t.replace(',', 'X').replace('.', ',').replace('X', '.')


def segunda_sexta(mes):
    d = datetime.date(int(mes[:4]), int(mes[5:7]), 1)
    while d.weekday() != 4:
        d += datetime.timedelta(days=1)
    return d + datetime.timedelta(days=7)


# ------------------------------------------------------------------ leitura das bases
class Historico:
    """Por cliente: caixas por mês (dois anos), carteira aberta, caixas por marca e executivo."""

    def __init__(self):
        self.cx = collections.defaultdict(lambda: collections.defaultdict(float))
        self.marca = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(float)))
        self.cart = collections.defaultdict(float)
        self.nome, self.execu = {}, {}

    @property
    def meses_com_dado(self):
        return {m for d in self.cx.values() for m, v in d.items() if v}

    def soma(self, cod, mes, cx, marca=None):
        self.cx[cod][mes] += cx
        if marca:
            self.marca[cod][mes][marca] += cx


def ler_csv(arq_hist, arq_cart):
    h = Historico()
    with open(arq_hist, encoding='utf-8-sig', newline='') as fh:
        for l in csv.DictReader(fh):
            cod = l['codigo'].strip()
            h.nome[cod] = l.get('cliente') or cod
            h.execu[cod] = l.get('executivo') or ''
            h.soma(cod, l['mes'][:7], float(l['caixas'] or 0), l.get('marca'))
    if arq_cart:
        with open(arq_cart, encoding='utf-8-sig', newline='') as fh:
            for l in csv.DictReader(fh):
                h.cart[l['codigo'].strip()] += float(l['caixas'] or 0)
    return h


def ler_json(arq, ano_corrente):
    """Lê o contrato do painel (references/contrato_dados.md da skill painel-de-indicadores):
    dims.cli = clientes; fat = [mes, exec, canal, cat, marca, seg, cli, uf, cx, valor];
    cart = [status, exec, canal, cat, marca, seg, cli, uf, cx, valor]; a referência do ano anterior
    por cliente vem em 'ref_ano_anterior' ou 'ref25' = [exec, canal, cli, mes1_corrente, [12 meses]]."""
    d = json.load(open(arq, encoding='utf-8'))
    dims = d['dims']
    lista = lambda k: dims[k] if isinstance(dims[k], list) else sorted(dims[k], key=dims[k].get)
    cli, exe, mar = lista('cli'), lista('exec'), lista('marca')
    h = Historico()
    codigos = d.get('cli_codigos') or cli  # o painel pode trazer o código ao lado do nome
    for r in d['fat']:
        cod = str(codigos[r[6]])
        h.nome[cod], h.execu[cod] = cli[r[6]], exe[r[1]]
        h.soma(cod, r[0], r[8], mar[r[4]])
    for r in d.get('cart', []):
        h.cart[str(codigos[r[6]])] += r[8]
    anterior = ano_corrente - 1
    for r in d.get('ref_ano_anterior', d.get('ref25', [])):
        cod = str(codigos[r[2]])
        h.nome.setdefault(cod, cli[r[2]])
        h.execu.setdefault(cod, exe[r[0]] if isinstance(r[0], int) else str(r[0]))
        for i, v in enumerate(r[-1]):
            h.cx[cod][f'{anterior}-{i + 1:02d}'] += v or 0
    return h


# ------------------------------------------------------------------ o motor por cliente
def projetar(cfg, h, cod, mes_alvo, dias_dec, dias_tot, meta, meta_tri=None):
    fechado, em_curso = mes_soma(mes_alvo, -2), mes_soma(mes_alvo, -1)
    y = h.cx[cod]
    m_fech, m_curso = y.get(fechado, 0.0), y.get(em_curso, 0.0)
    longos = [max(0.0, y.get(mes_soma(fechado, -i), 0.0)) for i in range(5, -1, -1)]
    longo = sum(longos) / len(longos)
    maior = max(longos + [m_fech])
    if m_curso <= 0:
        curso_proj = 0.0
    elif m_fech > 0 and m_curso >= p(cfg, 'mes_feito_se_atingiu') * m_fech:
        curso_proj = m_curso  # mês feito: conta de pedido grande já colocou o pedido do mês
    else:
        curso_proj = min(m_curso * dias_tot / max(dias_dec, 1), max(maior, m_curso))
    curto = (m_fech + curso_proj) / 2 if (m_fech or curso_proj) else longo
    w = p(cfg, 'peso_ritmo_curto')
    base = w * curto + (1 - w) * longo
    # sazonalidade do próprio cliente no ano anterior
    ant = lambda m: y.get(mes_soma(m, -12), 0.0)
    ref = (ant(fechado) + ant(em_curso)) / 2
    alvo_ant = ant(mes_alvo)
    if ref < p(cfg, 'base_minima_sazonalidade') or alvo_ant <= 0:
        saz = 1.0
    else:
        saz = max(p(cfg, 'sazonalidade_min'), min(p(cfg, 'sazonalidade_max'), alvo_ant / ref))
    estab = base * saz
    queda = estab * p(cfg, 'fator_queda')
    # crescimento: o necessário para o acumulado do ano fechar +7,5% até o mês alvo
    ano = mes_alvo[:4]
    meses_ytd = [f'{ano}-{i:02d}' for i in range(1, int(mes_alvo[5:7]) + 1)]
    ytd_ant = sum(ant(m) for m in meses_ytd)
    obs = []
    ytd_atual = 0.0
    for m in meses_ytd[:-1]:
        if m in h.meses_com_dado:
            ytd_atual += y.get(m, 0.0)
        else:
            ytd_atual += ant(m)  # mês ausente da base inteira: assume o do ano anterior
            if ant(m):
                obs.append(f'{m} fora da base: assumido o ano anterior')
    necessario = max(0.0, (1 + p(cfg, 'ambicao_ytd')) * ytd_ant - ytd_atual)
    cresc = max(estab * p(cfg, 'fator_crescimento'), necessario)
    cresc = min(cresc, max(estab * p(cfg, 'teto_crescimento'), meta or 0))
    # projeção = estabilização + regras de evidência
    cart = h.cart.get(cod, 0.0)
    rec = estab
    if m_curso == 0 and m_fech > 0:
        rec = min(estab, m_fech)
        obs.append('mês em curso zerado → base = mês fechado')
    if m_curso == 0 and m_fech == 0:
        rec = min(rec, longo)
        obs.append('sem venda no trimestre → média do ano')
    if cart > 0.5 * rec and cart > p(cfg, 'carteira_relevante'):
        obs.append(f'carteira aberta relevante ({br(cart)} cx): parte fatura ainda no mês em curso')
    fim_tri = obter(cfg, 'calendario.meses_fim_trimestre', [3, 6, 9, 12])
    if meta_tri and int(mes_alvo[5:7]) in fim_tri:  # régua só no último mês do trimestre
        gap = p(cfg, 'regua_meta') * meta_tri - (m_fech + m_curso + cart)
        if gap > rec:
            rec = min(gap, estab * p(cfg, 'teto_puxada_meta'))
        obs.append(f'régua do trimestre: faltam {br(max(0, gap))} cx além de fechado + em curso + carteira')
    if cart > 0 and rec < p(cfg, 'piso_carteira') * cart:
        rec = p(cfg, 'piso_carteira') * cart
        obs.append('elevado ao piso da carteira aberta')
    rec = max(rec, 0.0)
    if rec < p(cfg, 'micro_conta') and estab < p(cfg, 'micro_conta') and cart == 0:
        rec = round(rec)
    # mix por marca: três últimos meses do cliente, senão o padrão da regional
    marcas = obter(cfg, 'produtos.marcas_foco', [])
    mix = collections.defaultdict(float)
    for m in (mes_soma(fechado, -1), fechado, em_curso):
        for k, v in h.marca[cod].get(m, {}).items():
            mix[k] += v
    tot = sum(mix.get(k, 0) for k in marcas)
    if tot < 100:
        mix = dict(obter(cfg, 'produtos.mix_padrao_regional', {}) or {})
        tot = sum(mix.get(k, 0) for k in marcas) or 1.0
    por_marca = {k: round(rec * mix.get(k, 0) / tot) for k in marcas}
    return dict(codigo=cod, cliente=h.nome.get(cod, cod), executivo=h.execu.get(cod, ''), meta=meta or 0,
                fechado=m_fech, em_curso=m_curso, em_curso_proj=curso_proj, longo=longo, saz=saz,
                alvo_ant=alvo_ant, carteira=cart, queda=queda, estab=estab, cresc=cresc, projecao=rec,
                por_marca=por_marca, obs='; '.join(obs))


# ------------------------------------------------------------------ saídas
def escrever_memoria(wb, cfg, linhas, mes_alvo, data_base):
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    vis = obter(cfg, 'saidas.identidade_visual', {}) or {}
    destaque = vis.get('destaque', '#FF007F').lstrip('#')
    grafite = vis.get('grafite', '#1D1D1F').lstrip('#')
    marcas = obter(cfg, 'produtos.marcas_foco', [])
    nome = f'PROJECAO_{mes_alvo}'
    if nome in wb.sheetnames:
        del wb[nome]
    ws = wb.create_sheet(nome)
    ws.append([f'Projeção por cliente · mês alvo {mes_alvo} · base de {data_base} · gerente {obter(cfg, "organizacao.gerente")}'])
    ws['A1'].font = Font(bold=True, size=13, color=destaque)
    ws.append([f'Regra: BASE = {p(cfg, "peso_ritmo_curto"):.0%} ritmo curto + {1 - p(cfg, "peso_ritmo_curto"):.0%} ritmo longo; '
               f'ESTABILIZAÇÃO = BASE × sazonalidade do ano anterior ({p(cfg, "sazonalidade_min")} a {p(cfg, "sazonalidade_max")}); '
               f'QUEDA = ×{p(cfg, "fator_queda")}; CRESCIMENTO = maior entre ×{p(cfg, "fator_crescimento")} e o necessário para o '
               f'acumulado +{p(cfg, "ambicao_ytd"):.1%} (teto {p(cfg, "teto_crescimento")}× ou a meta). A PROJEÇÃO vai para o BE, '
               'distribuída pelo mix por marca do cliente.'])
    ws.append([])
    cab = ['Executivo', 'Cliente', 'Código', 'Meta', 'Mês fechado', 'Mês em curso (parcial)', 'Mês em curso proj.',
           'Média 6 meses', 'Sazonalidade', 'Mês alvo ano anterior', 'Carteira aberta', 'QUEDA', 'ESTABILIZAÇÃO',
           'CRESCIMENTO', 'PROJEÇÃO (BE)', 'Δ contra meta', '% meta'] + marcas + ['Observações']
    ws.append(cab)
    for c in ws[4]:
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor=grafite)
        c.alignment = Alignment(wrap_text=True, vertical='center')
    linhas.sort(key=lambda x: -x['projecao'])
    for l in linhas:
        ws.append([l['executivo'], l['cliente'], l['codigo'], l['meta'], l['fechado'], l['em_curso'], l['em_curso_proj'],
                   l['longo'], l['saz'], l['alvo_ant'], l['carteira'], l['queda'], l['estab'], l['cresc'], l['projecao'],
                   l['projecao'] - l['meta'], (l['projecao'] / l['meta']) if l['meta'] else None]
                  + [l['por_marca'][k] for k in marcas] + [l['obs']])
    fim = ws.max_row
    tr = fim + 1
    ws.cell(tr, 2).value = 'TOTAL'
    ws.cell(tr, 2).font = Font(bold=True)
    col_num = list(range(4, 17)) + list(range(18, 18 + len(marcas)))
    for j in col_num:
        if j == 9:
            continue
        L = get_column_letter(j)
        ws.cell(tr, j).value = f'=SUM({L}5:{L}{fim})'
        ws.cell(tr, j).font = Font(bold=True)
    ws.cell(tr, 17).value = f'=IF(D{tr}=0,"",O{tr}/D{tr})'
    for r in range(5, tr + 1):
        for j in col_num:
            ws.cell(r, j).number_format = '#,##0'
        ws.cell(r, 9).number_format = '0.00'
        ws.cell(r, 17).number_format = '0%'
        ws.cell(r, 15).font = Font(bold=True, color=destaque)
    for j, w in enumerate([18, 30, 10, 10, 11, 12, 12, 12, 11, 12, 11, 11, 13, 13, 13, 11, 8] + [9] * len(marcas) + [60], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'C5'
    tot = collections.Counter()
    for l in linhas:
        for k in ('meta', 'queda', 'estab', 'cresc', 'projecao', 'carteira', 'alvo_ant', 'fechado', 'em_curso'):
            tot[k] += l[k]
    tr += 2
    ws.cell(tr, 2).value = f'RESUMO DOS CENÁRIOS · {mes_alvo} (caixas)'
    ws.cell(tr, 2).font = Font(bold=True, size=12, color=destaque)
    resumo = [('Meta do mês', 'meta'), ('Cenário QUEDA', 'queda'), ('Cenário ESTABILIZAÇÃO', 'estab'),
              ('Cenário CRESCIMENTO', 'cresc'), ('PROJEÇÃO (BE)', 'projecao'), ('Carteira aberta hoje', 'carteira'),
              ('Mês alvo no ano anterior', 'alvo_ant'), ('Mês fechado', 'fechado'), ('Mês em curso (parcial)', 'em_curso')]
    for i, (rot, k) in enumerate(resumo, 1):
        ws.cell(tr + i, 2).value = rot
        ws.cell(tr + i, 3).value = round(tot[k])
        ws.cell(tr + i, 3).number_format = '#,##0'
        ws.cell(tr + i, 4).value = (tot[k] / tot['meta']) if tot['meta'] else None
        ws.cell(tr + i, 4).number_format = '0%'
    return tot


def preencher_be(cfg, arq_be, saida, linhas, mes_alvo):
    """Escreve SÓ a data de subida e as caixas por marca na cópia do arquivo oficial."""
    import openpyxl
    from openpyxl.utils import column_index_from_string as ci
    be = obter(cfg, 'projecao.arquivo_be', {}) or {}
    col = be.get('colunas', {})
    shutil.copy2(arq_be, saida)
    wb = openpyxl.load_workbook(saida)
    ws = wb[be.get('aba', wb.sheetnames[0])]
    por_cod = {l['codigo']: l for l in linhas}
    gerente = obter(cfg, 'organizacao.gerente')
    c_ger = ci(col.get('gerente', 'I'))
    c_cod = ci(col.get('codigo', 'C'))
    subida = segunda_sexta(mes_alvo)
    n = 0
    for r in range(int(be.get('linha_inicial', 5)), ws.max_row + 1):
        if str(ws.cell(r, c_ger).value or '').strip() != gerente:
            continue
        l = por_cod.get(str(ws.cell(r, c_cod).value or '').strip())
        if not l:
            continue
        limite = ws.cell(r, ci(col.get('data_limite_pedido', 'N'))).value
        data = subida
        if isinstance(limite, datetime.datetime) and limite.date() < data:
            data = limite.date()
        celula = ws.cell(r, ci(col.get('data_subida', 'O')))
        celula.value = datetime.datetime(data.year, data.month, data.day) if l['projecao'] > 0 else 0
        celula.number_format = 'DD/MM/YYYY'
        for letra, marca in zip(col.get('marcas', []), obter(cfg, 'produtos.marcas_foco', [])):
            ws.cell(r, ci(letra)).value = l['por_marca'].get(marca, 0)
        n += 1
    return wb, n


def main():
    ap = argparse.ArgumentParser(description='Projeção por cliente e cenários para o BE')
    ap.add_argument('--config')
    ap.add_argument('--dados')
    ap.add_argument('--historico')
    ap.add_argument('--carteira')
    ap.add_argument('--metas')
    ap.add_argument('--be')
    ap.add_argument('--mes-alvo', required=True)
    ap.add_argument('--dias-decorridos', type=int, required=True)
    ap.add_argument('--dias-totais', type=int)
    ap.add_argument('--saida')
    ap.add_argument('--falar', action='store_true')
    a = ap.parse_args()
    cfg = carregar(a.config)
    em_curso = mes_soma(a.mes_alvo, -1)
    dias_tot = a.dias_totais or (obter(cfg, 'calendario.dias_uteis', {}) or {}).get(em_curso) or 21
    ano = int(a.mes_alvo[:4])
    if a.dados:
        h = ler_json(a.dados, ano)
    elif a.historico:
        h = ler_csv(a.historico, a.carteira)
    else:
        sys.exit('Informe --dados (JSON do painel) ou --historico (CSV).')
    metas = {}
    if a.metas:
        with open(a.metas, encoding='utf-8-sig', newline='') as fh:
            metas = {l['codigo'].strip(): float(l['meta'] or 0) for l in csv.DictReader(fh)}
    regua = {str(k): v for k, v in (obter(cfg, 'projecao.contas_regua_trimestre', {}) or {}).items()}
    execs = set(nomes_executivos(cfg))
    linhas = [projetar(cfg, h, cod, a.mes_alvo, a.dias_decorridos, dias_tot, metas.get(cod), regua.get(cod))
              for cod in sorted(h.cx) if not execs or h.execu.get(cod, '') in execs or not h.execu.get(cod)]
    pasta = a.saida or caminho(cfg, 'caminhos.comunicacao')
    os.makedirs(pasta, exist_ok=True)
    import openpyxl
    if a.be:
        base, ext = os.path.splitext(os.path.basename(a.be))
        arq = os.path.join(pasta, base + obter(cfg, 'projecao.arquivo_be.sufixo_saida', '_Projecao') + ext)
        wb, n = preencher_be(cfg, a.be, arq, linhas, a.mes_alvo)
        print(f'{n} linhas do arquivo oficial preenchidas (data de subida e caixas por marca)')
    else:
        arq = os.path.join(pasta, f'PROJECAO_{a.mes_alvo}.xlsx')
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
    tot = escrever_memoria(wb, cfg, linhas, a.mes_alvo, datetime.date.today().strftime('%d/%m/%Y'))
    wb.save(arq)
    haircut = obter(cfg, 'projecao.arquivo_be.ajuste_colaborativo_pct', -0.10)
    final = tot['projecao'] * (1 + haircut)
    pct = lambda v: f'{br(100 * v / tot["meta"])}%' if tot['meta'] else 'meta n/d'
    resumo = (f'Projeção de {a.mes_alvo}: {br(tot["projecao"])} caixas nas subidas ({pct(tot["projecao"])} da meta); '
              f'BE final depois do ajuste colaborativo de {br(100 * haircut)}%: cerca de {br(final)} ({pct(final)}). '
              f'Cenários: queda {br(tot["queda"])} · estabilização {br(tot["estab"])} · crescimento {br(tot["cresc"])}.')
    print('salvo:', arq)
    print(resumo)
    print('\nMaiores projeções:')
    for l in sorted(linhas, key=lambda x: -x['projecao'])[:10]:
        print(f"  {l['cliente'][:28]:28s} meta={br(l['meta']):>7s} fechado={br(l['fechado']):>7s} "
              f"em curso={br(l['em_curso']):>7s} cart={br(l['carteira']):>6s} | queda={br(l['queda']):>7s} "
              f"estab={br(l['estab']):>7s} cresc={br(l['cresc']):>7s} | PROJ={br(l['projecao']):>7s} {l['obs']}")
    voz = obter(cfg, 'projecao.voz_resumo', {}) or {}
    if a.falar and shutil.which(voz.get('comando', 'say')):
        subprocess.run([voz.get('comando', 'say'), '-v', voz.get('voz', 'Felipe (Enhanced)'), '-r',
                        str(voz.get('velocidade', 185)), resumo])


if __name__ == '__main__':
    main()
