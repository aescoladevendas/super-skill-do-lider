# -*- coding: utf-8 -*-
"""Cubo da rede a partir dos exports de KPIs por SKU do painel de varejo.

O que faz: lê os exports em tabela cruzada do portal do painel de varejo (um da rede
inteira e, se houver, um por estado), tira as linhas "Total", separa o que é da empresa
(marcas de produtos.marcas_foco da config) do resto do mercado e grava cubo_rede.json
com, por unidade (rede e estados), mês a mês: mercado da rede, empresa, categorias,
marcas, marca por categoria, concorrência, lojas com venda e SKUs da empresa.

Entradas (na --pasta):
  kpi_REDE.csv        export da rede inteira (obrigatório)
  kpi_UF_<UF>.csv     um por estado exportado (opcional; ex.: kpi_UF_PA.csv)
  Formato: CSV UTF-16 separado por tabulação, milhar brasileiro (1.234,56). Linha 1 =
  cabeçalho com 5 colunas de dimensão (marca, categoria, EAN, SKU, métrica) e depois um
  mês por coluna no formato MM/AA. Cada linha seguinte = um SKU x uma métrica. Os nomes
  das métricas vêm de diagnostico_rede.metricas_export na config.
Saída: <pasta>/cubo_rede.json
Regra: se só UM estado foi exportado, o cubo deriva "Demais estados" = rede menos esse
estado (aritmética exata, sem estimativa).

Como rodar:
  python3 painel_varejo_cubo.py --rede "REDE EXEMPLO NORTE" --pasta ./dados_rede
  (opcional: --config empresa.yaml)
"""
import argparse, glob, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from configuracao import carregar, obter

UFS = {'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia',
       'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás',
       'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
       'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí',
       'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul',
       'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo',
       'SE': 'Sergipe', 'TO': 'Tocantins'}

METRICAS_PADRAO = {'valor': 'Vendas em valor R$', 'quantidade': 'Quantidade de venda',
                   'lojas': 'Qtd Lojas'}


def sem_acento(texto):
    return unicodedata.normalize('NFKD', texto or '').encode('ascii', 'ignore').decode().upper().strip()


def num(s):
    """Número em formato brasileiro (1.234,56; R$; %) → float. Vazio → None."""
    s = (s or '').strip().replace('R$', '').replace('%', '').strip()
    if not s:
        return None
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def ler_export(arquivo):
    """Lê um export de KPIs por SKU. Devolve (meses, {(marca, categoria, ean): dados})."""
    with open(arquivo, encoding='utf-16') as fh:
        linhas = [r.split('\t') for r in fh.read().splitlines()]
    meses = [m.strip() for m in linhas[0][5:]]
    skus = {}
    for r in linhas[1:]:
        if len(r) < 6:
            continue
        # linhas "Total" do export (marca, categoria ou SKU = Total) DOBRAM a soma: fora
        if any(r[i].strip() == 'Total' for i in range(4)):
            continue
        chave = (r[0].strip(), r[1].strip(), r[2].strip())
        d = skus.setdefault(chave, dict(marca=r[0].strip(), cat=r[1].strip(),
                                        ean=r[2].strip(), nome=r[3].strip()))
        d[r[4].strip()] = [num(x) for x in r[5:5 + len(meses)]]
    return meses, skus


def conferir_meses(meses, arquivo):
    """Os meses precisam ser contínuos (MM/AA), senão as fórmulas de 'mesmo mês do ano
    anterior' (12 colunas para trás) quebram."""
    seq = []
    for m in meses:
        if not re.fullmatch(r'\d{2}/\d{2}', m):
            sys.exit(f'{arquivo}: coluna de mês fora do formato MM/AA: {m!r}')
        mm, aa = int(m[:2]), int(m[3:])
        seq.append(aa * 12 + mm)
    if any(b - a != 1 for a, b in zip(seq, seq[1:])):
        sys.exit(f'{arquivo}: os meses do export não são contínuos')


def montar_unidade(nome, meses, skus, eh_empresa, met):
    nm = len(meses)

    def agregar(chave, filtro=None):
        d = {}
        for s in skus.values():
            if filtro and not filtro(s):
                continue
            a = d.setdefault(chave(s), {'v': [0.0] * nm, 'q': [0.0] * nm})
            v = s.get(met['valor']) or [None] * nm
            q = s.get(met['quantidade']) or [None] * nm
            for i in range(nm):
                a['v'][i] += v[i] or 0
                a['q'][i] += q[i] or 0
        return d

    # lojas com venda no mês = maior número de lojas entre os SKUs (base comparável)
    lojas = []
    for i in range(nm):
        vals = [int(s[met['lojas']][i]) for s in skus.values()
                if s.get(met['lojas']) and s[met['lojas']][i]]
        lojas.append(max(vals or [0]))
    skus_emp = []
    for s in skus.values():
        if not eh_empresa(s):
            continue
        skus_emp.append(dict(marca=s['marca'], cat=s['cat'], ean=s['ean'], nome=s['nome'],
                             v=[x or 0 for x in (s.get(met['valor']) or [0] * nm)],
                             q=[x or 0 for x in (s.get(met['quantidade']) or [0] * nm)],
                             lojas=[x or 0 for x in (s.get(met['lojas']) or [0] * nm)]))
    vazio = {'v': [0.0] * nm, 'q': [0.0] * nm}
    return dict(name=nome, months=meses, lojas=lojas,
                mkt=agregar(lambda s: 'T').get('T', vazio),
                emp=agregar(lambda s: 'T', eh_empresa).get('T', vazio),
                cat_mkt=agregar(lambda s: s['cat']),
                cat_emp=agregar(lambda s: s['cat'], eh_empresa),
                marca=agregar(lambda s: s['marca'], eh_empresa),
                cat_marca=agregar(lambda s: s['cat'] + '|' + s['marca'], eh_empresa),
                conc=agregar(lambda s: s['cat'] + '|' + s['marca'], lambda s: not eh_empresa(s)),
                skus=skus_emp)


def derivar_demais(rede, uf, sigla):
    """Demais estados = rede menos o estado exportado (subtração exata, item a item)."""
    nm = len(rede['months'])

    def sub(a, b):
        return {'v': [a['v'][i] - b['v'][i] for i in range(nm)],
                'q': [a['q'][i] - b['q'][i] for i in range(nm)]}

    def subd(da, db):
        zero = {'v': [0] * nm, 'q': [0] * nm}
        return {k: sub(da.get(k, zero), db.get(k, zero)) for k in set(da) | set(db)}

    por_ean = {s['ean']: s for s in uf['skus']}
    skus = []
    for s in rede['skus']:
        d = por_ean.get(s['ean'], {'v': [0] * nm, 'q': [0] * nm, 'lojas': [0] * nm})
        skus.append(dict(marca=s['marca'], cat=s['cat'], ean=s['ean'], nome=s['nome'],
                         v=[s['v'][i] - d['v'][i] for i in range(nm)],
                         q=[s['q'][i] - d['q'][i] for i in range(nm)],
                         lojas=[s['lojas'][i] - d['lojas'][i] for i in range(nm)]))
    return dict(name=f'Demais estados (rede menos {sigla})', months=rede['months'],
                lojas=[rede['lojas'][i] - uf['lojas'][i] for i in range(nm)],
                mkt=sub(rede['mkt'], uf['mkt']), emp=sub(rede['emp'], uf['emp']),
                cat_mkt=subd(rede['cat_mkt'], uf['cat_mkt']),
                cat_emp=subd(rede['cat_emp'], uf['cat_emp']),
                marca=subd(rede['marca'], uf['marca']),
                cat_marca=subd(rede['cat_marca'], uf['cat_marca']),
                conc=subd(rede['conc'], uf['conc']), skus=skus, derivada_de=f'UF_{sigla}')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--rede', required=True, help='nome da rede como aparece no material')
    ap.add_argument('--pasta', default='.', help='pasta com os kpi_*.csv')
    ap.add_argument('--config', default=None)
    a = ap.parse_args()
    cfg = carregar(a.config)

    marcas_emp = {sem_acento(m) for m in obter(cfg, 'produtos.marcas_foco', []) or []}
    fora = {sem_acento(m) for m in obter(cfg, 'diagnostico_rede.marcas_fora_da_empresa', []) or []}
    if marcas_emp & fora:
        sys.exit('Config incoerente: marca listada como da empresa e como fora da empresa: '
                 + ', '.join(sorted(marcas_emp & fora)))
    met = dict(METRICAS_PADRAO)
    met.update(obter(cfg, 'diagnostico_rede.metricas_export', {}) or {})

    def eh_empresa(s):
        return sem_acento(s['marca']) in marcas_emp

    arq_rede = os.path.join(a.pasta, 'kpi_REDE.csv')
    if not os.path.isfile(arq_rede):
        sys.exit(f'Falta {arq_rede} (export da rede inteira)')
    cubo = {}
    arquivos = [arq_rede] + sorted(glob.glob(os.path.join(a.pasta, 'kpi_UF_*.csv')))
    for arq in arquivos:
        tag = os.path.basename(arq)[4:-4]          # REDE ou UF_PA
        meses, skus = ler_export(arq)
        conferir_meses(meses, arq)
        if tag == 'REDE':
            nome = f'{a.rede} (rede)'
        else:
            sigla = tag[3:]
            if sigla not in UFS:
                sys.exit(f'{arq}: sigla de estado desconhecida ({sigla})')
            nome = UFS[sigla]
        cubo[tag] = montar_unidade(nome, meses, skus, eh_empresa, met)
        u = cubo[tag]
        print(f"{tag}: {len(u['skus'])} SKUs da empresa · lojas no último mês {u['lojas'][-1]} · "
              f"marcas da empresa encontradas: {', '.join(sorted(u['marca'])) or 'NENHUMA'}")
        if not u['skus']:
            print('  ATENÇÃO: nenhuma marca da empresa no export. Confira produtos.marcas_foco '
                  'e os filtros de unidade/categoria no portal.')
    ufs = [t for t in cubo if t.startswith('UF_')]
    if len(ufs) == 1:
        sigla = ufs[0][3:]
        cubo['UF_DEMAIS'] = derivar_demais(cubo['REDE'], cubo[ufs[0]], sigla)
        print(f'derivada: Demais estados = rede menos {sigla}')
    saida = os.path.join(a.pasta, 'cubo_rede.json')
    with open(saida, 'w', encoding='utf-8') as fh:
        json.dump(cubo, fh, ensure_ascii=False)
    print('gravado', saida)


if __name__ == '__main__':
    main()
