# -*- coding: utf-8 -*-
"""Identidade de clientes: código, grupo e operação por UF.

Aplica as regras da seção `clientes` do arquivo de configuração:
  - resolver_codigo: segue as migrações de código (de → para), em cadeia
  - chave_grupo: devolve a chave do grupo econômico (merges_grupo) ou o próprio código
  - nome_exibicao: nome único para todos os materiais (exibicao), sem prefixos técnicos
  - caixa: camada 1, classifica uma linha de um grupo com várias operações por UF
  - caixa_por_uf_pdv: camada 2, PDV de UF fora das contratadas vira atacado
  - suspeitas_troca_de_codigo: código que zera enquanto outro nasce com volume parecido

Uso:
  python3 identidade_clientes.py --teste
  python3 identidade_clientes.py --classificar base.csv --grupo distribuidora_horizonte \
          --fonte sistema_do_distribuidor [--coluna-uf uf_pdv] [--saida saida.csv]
  python3 identidade_clientes.py --suspeitas serie.csv
      (serie.csv com colunas: codigo, mes (AAAA-MM), valor)
Todas as opções aceitam --config arquivo.yaml.
"""
import argparse, csv, os, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from configuracao import carregar, obter  # noqa: E402

VAZIOS = ('', '(em branco)', 'none', 'nan', 'null')


def _txt(v):
    return str(v if v is not None else '').strip()


def resolver_codigo(cfg, codigo):
    """Segue as migrações de código em cadeia (100300 → 100302 → ...)."""
    mapa = {_txt(m['de']): _txt(m['para']) for m in obter(cfg, 'clientes.migracoes', []) or []}
    atual, vistos = _txt(codigo), set()
    while atual in mapa and atual not in vistos:
        vistos.add(atual)
        atual = mapa[atual]
    return atual


def chave_grupo(cfg, codigo):
    cod = resolver_codigo(cfg, codigo)
    for chave, g in (obter(cfg, 'clientes.merges_grupo', {}) or {}).items():
        if cod in [_txt(c) for c in g.get('codigos', [])]:
            return chave
    return cod


def nome_exibicao(cfg, codigo, nome=''):
    cod = resolver_codigo(cfg, codigo)
    exib = obter(cfg, 'clientes.exibicao', {}) or {}
    if cod in exib:
        return exib[cod]
    for chave, g in (obter(cfg, 'clientes.merges_grupo', {}) or {}).items():
        if cod in [_txt(c) for c in g.get('codigos', [])]:
            return g.get('exibicao', chave)
    n = _txt(nome)
    for p in obter(cfg, 'clientes.prefixos_remover', []) or []:
        if n.upper().startswith(p.upper()):
            n = n[len(p):]
    return n.strip() or cod


def _grupo(cfg, grupo):
    g = (obter(cfg, 'clientes.grupos_por_uf', {}) or {}).get(grupo)
    if not g:
        raise KeyError(f'grupo {grupo!r} não está em clientes.grupos_por_uf')
    return g


def caixa(cfg, grupo, fonte, texto):
    """Camada 1: a primeira regra cujo trecho aparece no texto define a caixa; senão, 'resto'."""
    f = _grupo(cfg, grupo)['fontes'][fonte]
    s = _txt(texto).upper()
    for r in f['regras']:
        if r['contem'].upper() in s:
            return r['caixa']
    return f['resto']


def caixa_por_uf_pdv(cfg, grupo, caixa_entidade, uf_pdv):
    """Camada 2: dentro de uma caixa de distribuição, PDV de UF fora das contratadas é atacado.
    Só usar quando a UF do PDV for confiável; sem UF, fica a camada 1."""
    g = _grupo(cfg, grupo)
    uf = _txt(uf_pdv).upper()
    if uf.lower() in VAZIOS:
        return caixa_entidade
    if caixa_entidade == g['caixa_atacado']:
        return caixa_entidade
    return caixa_entidade if uf in [u.upper() for u in g['ufs_distribuicao']] else g['caixa_atacado']


def fatia_uf_em_branco(linhas, coluna_uf, coluna_valor):
    """Parte do valor com UF do PDV em branco (meça antes de usar a camada 2)."""
    total = branco = 0.0
    for l in linhas:
        try:
            v = float(str(l.get(coluna_valor, 0)).replace('.', '').replace(',', '.') or 0)
        except ValueError:
            v = 0.0
        total += abs(v)
        if _txt(l.get(coluna_uf)).lower() in VAZIOS:
            branco += abs(v)
    return branco / total if total else 0.0


def suspeitas_troca_de_codigo(serie, tolerancia=0.5, janela=3):
    """serie: {codigo: {'AAAA-MM': valor}}. Devolve pares (antigo, novo, mes, razao) em que o
    antigo para de faturar no mês em que o novo começa (ou no seguinte) com volume parecido."""
    def meses_com_venda(d):
        return sorted(m for m, v in d.items() if v)

    def prox(m):
        a, b = int(m[:4]), int(m[5:7])
        return f'{a + (b == 12):04d}-{(b % 12) + 1:02d}'

    fim, ini = {}, {}
    for cod, d in serie.items():
        ms = meses_com_venda(d)
        if ms:
            ini[cod], fim[cod] = ms[0], ms[-1]
    ultimo_mes = max(fim.values()) if fim else None
    pares = []
    for a, fa in fim.items():
        if fa == ultimo_mes:
            continue  # ainda ativo
        for b, ib in ini.items():
            if a == b or ib not in (fa, prox(fa)):
                continue
            va = [serie[a][m] for m in meses_com_venda(serie[a])[-janela:]]
            vb = [serie[b][m] for m in meses_com_venda(serie[b])[:janela]]
            ma, mb = sum(va) / len(va), sum(vb) / len(vb)
            if ma and mb and (1 - tolerancia) <= mb / ma <= 1 / (1 - tolerancia):
                pares.append((a, b, ib, round(mb / ma, 2)))
    return pares


def _teste(cfg):
    ok = True

    def conf(rotulo, obtido, esperado):
        nonlocal ok
        bate = obtido == esperado
        ok = ok and bate
        print(f"  {'ok ' if bate else 'ERRO'} {rotulo}: {obtido!r}" + ('' if bate else f' (esperado {esperado!r})'))

    print('Configuração:', cfg['_arquivo'])
    migs = obter(cfg, 'clientes.migracoes', []) or []
    if migs:
        conf('migração', resolver_codigo(cfg, migs[0]['de']), _txt(migs[0]['para']))
    for chave, g in (obter(cfg, 'clientes.merges_grupo', {}) or {}).items():
        conf(f'grupo {chave}', {chave_grupo(cfg, c) for c in g['codigos']}, {chave})
    for grupo, g in (obter(cfg, 'clientes.grupos_por_uf', {}) or {}).items():
        for fonte, f in g['fontes'].items():
            for r in f['regras']:
                conf(f'{grupo}/{fonte} "{r["contem"]}"', caixa(cfg, grupo, fonte, 'X ' + r['contem'] + ' Y'), r['caixa'])
            conf(f'{grupo}/{fonte} sem regra', caixa(cfg, grupo, fonte, 'outra filial qualquer'), f['resto'])
        dist = [c for c in g['caixas'] if c != g['caixa_atacado']][0]
        conf('camada 2, UF fora', caixa_por_uf_pdv(cfg, grupo, dist, 'BA'), g['caixa_atacado'])
        conf('camada 2, UF em branco', caixa_por_uf_pdv(cfg, grupo, dist, ''), dist)
    serie = {'A': {'2025-06': 100, '2025-07': 110, '2025-08': 90},
             'B': {'2025-09': 95, '2025-10': 105},
             'C': {'2025-06': 50, '2025-10': 60}}
    conf('suspeita de troca de código', [(a, b) for a, b, _, _ in suspeitas_troca_de_codigo(serie)], [('A', 'B')])
    print('Resultado:', 'todas as regras conferem' if ok else 'HÁ REGRA QUE NÃO CONFERE')
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--config')
    ap.add_argument('--teste', action='store_true')
    ap.add_argument('--classificar')
    ap.add_argument('--grupo')
    ap.add_argument('--fonte')
    ap.add_argument('--coluna-uf')
    ap.add_argument('--coluna-valor', default='valor')
    ap.add_argument('--suspeitas')
    ap.add_argument('--saida')
    a = ap.parse_args()
    cfg = carregar(a.config)
    if a.teste:
        sys.exit(0 if _teste(cfg) else 1)
    if a.classificar:
        coluna = _grupo(cfg, a.grupo)['fontes'][a.fonte]['coluna']
        with open(a.classificar, encoding='utf-8-sig', newline='') as fh:
            linhas = list(csv.DictReader(fh))
        if a.coluna_uf:
            fatia = fatia_uf_em_branco(linhas, a.coluna_uf, a.coluna_valor)
            print(f'UF do PDV em branco: {fatia:.0%} do valor' +
                  (' · ATENÇÃO: alto demais para a camada 2, fique na camada 1' if fatia > 0.2 else ''))
        for l in linhas:
            cx = caixa(cfg, a.grupo, a.fonte, l.get(coluna))
            l['caixa'] = caixa_por_uf_pdv(cfg, a.grupo, cx, l.get(a.coluna_uf)) if a.coluna_uf else cx
        saida = a.saida or os.path.splitext(a.classificar)[0] + '_classificada.csv'
        with open(saida, 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()) if linhas else ['caixa'])
            w.writeheader()
            w.writerows(linhas)
        print(f'{len(linhas)} linhas classificadas → {saida}')
    if a.suspeitas:
        serie = defaultdict(dict)
        with open(a.suspeitas, encoding='utf-8-sig', newline='') as fh:
            for l in csv.DictReader(fh):
                serie[_txt(l['codigo'])][_txt(l['mes'])[:7]] = float(l['valor'] or 0)
        pares = suspeitas_troca_de_codigo(serie)
        for antigo, novo, mes, razao in pares:
            print(f'  suspeita: {antigo} parou e {novo} começou em {mes} (volume novo/antigo = {razao})')
        print(f'{len(pares)} par(es) para investigar antes de reportar perda ou ganho de carteira')


if __name__ == '__main__':
    main()
