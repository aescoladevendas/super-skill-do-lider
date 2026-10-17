# -*- coding: utf-8 -*-
"""Cubo loja a loja a partir do export de abertura por loja do painel de varejo.

O que faz: lê o export semanal loja x categoria x fabricante x marca x SKU (tabela cruzada,
CSV UTF-16 com tabulação), mantém só as lojas cujo nome começa com o PREFIXO da rede (o
filtro de rede do portal pode vir com outras redes marcadas que não aparecem na busca),
mantém só as marcas da empresa (produtos.marcas_foco), tira as linhas "Total" e grava
cubo_lojas.json com R$ e quantidade por loja x SKU x semana. Imprime o ranking das lojas
com a comparação P2 x P1 (dois blocos iguais de semanas fechadas).

Entradas (na --pasta):
  abertura_lojas.csv   (ou o nome passado em --arquivo)
  Formato: linha 1 = cabeçalho com 7 colunas de dimensão (loja, endereço, categoria,
  fabricante, marca, EAN, SKU) e, a partir da 8ª coluna, um bloco de métricas por semana
  (o rótulo da semana na 1ª coluna do bloco); linha 2 = nome das métricas; demais linhas =
  dados (dimensão em branco repete a de cima). A posição do valor e da quantidade dentro
  do bloco vem de diagnostico_rede.abertura_lojas na config.
Saída: <pasta>/cubo_lojas.json
Regra: loja a loja só existe a partir da primeira semana que o portal abre; é leitura de
TENDÊNCIA dentro do ano (P2 x P1), nunca contra o ano anterior.

Como rodar:
  python3 painel_varejo_lojas.py --prefixo "REDE EXEMPLO NORTE" --pasta ./dados_rede
  (opcionais: --arquivo abertura_lojas.csv --semanas-periodo 12 --incluir-ultima-semana
   --todas-as-marcas --config empresa.yaml)
"""
import argparse, json, os, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from configuracao import carregar, obter

LAYOUT_PADRAO = {'colunas_dimensao': 7, 'metricas_por_semana': 5,
                 'posicao_valor': 1, 'posicao_quantidade': 3}


def sem_acento(texto):
    return unicodedata.normalize('NFKD', texto or '').encode('ascii', 'ignore').decode().upper().strip()


def num(s):
    s = (s or '').strip().replace('R$', '').replace('%', '').strip()
    if not s:
        return None
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def periodos(n_semanas, por_periodo, incluir_ultima):
    """Semanas fechadas (a última do export é parcial, salvo pedido) e os blocos P1 e P2
    de mesmo tamanho, P2 = as mais recentes."""
    fechadas = list(range(n_semanas if incluir_ultima else n_semanas - 1))
    n = min(por_periodo, len(fechadas) // 2)
    p2 = fechadas[len(fechadas) - n:]
    p1 = fechadas[len(fechadas) - 2 * n:len(fechadas) - n]
    return fechadas, p1, p2


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--prefixo', required=True,
                    help='início do nome das lojas da rede (só essas lojas entram)')
    ap.add_argument('--pasta', default='.')
    ap.add_argument('--arquivo', default='abertura_lojas.csv')
    ap.add_argument('--semanas-periodo', type=int, default=12)
    ap.add_argument('--incluir-ultima-semana', action='store_true',
                    help='use só se a última semana do export já estiver fechada')
    ap.add_argument('--todas-as-marcas', action='store_true',
                    help='não filtrar pelas marcas da empresa (o export já vem só com elas)')
    ap.add_argument('--config', default=None)
    a = ap.parse_args()
    cfg = carregar(a.config)
    lay = dict(LAYOUT_PADRAO)
    lay.update(obter(cfg, 'diagnostico_rede.abertura_lojas', {}) or {})
    marcas_emp = {sem_acento(m) for m in obter(cfg, 'produtos.marcas_foco', []) or []}
    pfx = sem_acento(a.prefixo)

    arq = os.path.join(a.pasta, a.arquivo)
    with open(arq, encoding='utf-16') as fh:
        linhas = [r.split('\t') for r in fh.read().splitlines()]
    cab, metricas = linhas[0], linhas[1]
    nd, bloco = lay['colunas_dimensao'], lay['metricas_por_semana']
    semanas = []
    for i in range(nd, len(cab)):
        if cab[i].strip() and (not semanas or semanas[-1][0] != cab[i].strip()):
            semanas.append((cab[i].strip(), i))
    rotulos = [w for w, _ in semanas]
    print('semanas', len(rotulos), rotulos[0], 'a', rotulos[-1])
    print('métricas do 1º bloco:', [m.strip() for m in metricas[semanas[0][1]:semanas[0][1] + bloco]],
          f"→ valor na posição {lay['posicao_valor']}, quantidade na {lay['posicao_quantidade']}")

    campos = [('loja', 0), ('end', 1), ('cat', 2), ('fab', 3), ('marca', 4), ('ean', 5), ('nome', 6)]
    lojas, atual, fora_rede, fora_marca = {}, {}, set(), {}
    for r in linhas[2:]:
        if len(r) < nd + 1:
            continue
        # linha "Total" (de loja, categoria, marca ou SKU) não entra e não contamina o
        # "repete a de cima" das próximas linhas. Nas outras colunas a comparação é exata
        # para não descartar um produto cujo nome comece com a palavra Total.
        if r[0].strip().startswith('Total') or any(r[i].strip() in ('Total', 'Total geral')
                                                   for i in range(1, nd)):
            continue
        for k, idx in campos:
            if r[idx].strip():
                atual[k] = r[idx].strip()
        loja = atual.get('loja', '')
        if pfx and not sem_acento(loja).startswith(pfx):
            fora_rede.add(loja)
            continue
        if not a.todas_as_marcas and sem_acento(atual.get('marca')) not in marcas_emp:
            fora_marca[atual.get('marca')] = fora_marca.get(atual.get('marca'), 0) + 1
            continue
        d = lojas.setdefault(loja, dict(end=atual.get('end', ''), skus={}))
        s = d['skus'].setdefault(atual['ean'], dict(cat=atual['cat'], marca=atual['marca'],
                                                    nome=atual['nome'],
                                                    v=[0.0] * len(rotulos), q=[0.0] * len(rotulos)))
        for wi, (_, i) in enumerate(semanas):
            s['v'][wi] += num(r[i + lay['posicao_valor']]) or 0
            s['q'][wi] += num(r[i + lay['posicao_quantidade']]) or 0
    if fora_rede:
        print(f'{len(fora_rede)} loja(s) de outras redes descartadas pelo prefixo: '
              + ', '.join(sorted(fora_rede)[:6]))
    if fora_marca:
        print('linhas de marcas fora da empresa descartadas:', fora_marca)
    if not lojas:
        sys.exit('Nenhuma loja ficou depois dos filtros: confira o --prefixo e as marcas da config.')
    saida = os.path.join(a.pasta, 'cubo_lojas.json')
    with open(saida, 'w', encoding='utf-8') as fh:
        json.dump(dict(weeks=rotulos, lojas=lojas), fh, ensure_ascii=False)

    fechadas, p1, p2 = periodos(len(rotulos), a.semanas_periodo, a.incluir_ultima_semana)

    def tot(d, idx):
        return sum(s['v'][i] for s in d['skus'].values() for i in idx)

    print(f'{len(lojas)} lojas · P1 = {rotulos[p1[0]]} a {rotulos[p1[-1]]} · '
          f'P2 = {rotulos[p2[0]]} a {rotulos[p2[-1]]}')
    br = lambda v: f'{v:,.0f}'.replace(',', '.')
    for loja, d in sorted(lojas.items(), key=lambda x: -tot(x[1], fechadas)):
        x1, x2 = tot(d, p1), tot(d, p2)
        var = ((x2 / x1 - 1) * 100) if x1 else 0
        print(f"{loja[:38]:38s} {d['end'][:30]:30s} total {br(tot(d, fechadas)):>11s}  "
              f"P1 {br(x1):>10s} P2 {br(x2):>10s} var {f'{var:+6.1f}'.replace('.', ',')}%")
    print('gravado', saida)


if __name__ == '__main__':
    main()
