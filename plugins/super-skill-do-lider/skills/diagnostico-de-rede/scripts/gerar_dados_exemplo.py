# -*- coding: utf-8 -*-
"""Dados FICTÍCIOS no formato do painel de varejo, para testar a skill de ponta a ponta.

O que faz: cria, numa pasta de teste, os mesmos arquivos que o portal do painel de varejo
exporta (CSV UTF-16 com tabulação, milhar brasileiro, linhas "Total" embutidas) para uma
rede inventada: kpi_REDE.csv, kpi_UF_<UF>.csv, abertura_lojas.csv (com lojas de outra
rede e uma marca concorrente no meio, para testar os filtros) e uf_map.json. As marcas da
empresa vêm de produtos.marcas_foco da config; as categorias e os números são inventados.
Serve como teste de regressão: sempre que mexer nos scripts, rode os quatro em sequência
e confira que o Excel sai com 10 abas (11 com --liberada) e zero erro de fórmula.

Entradas: só a config (marcas, rede de exemplo do cadastro, mês corrente do calendário).
Saída: arquivos na --pasta (use uma pasta de rascunho, nunca a pasta do plugin).

Como rodar:
  python3 gerar_dados_exemplo.py --pasta /tmp/teste_rede
  opcionais: --rede "REDE EXEMPLO NORTE" --mes-corrente 09/26 --liberada
             --todos-os-estados --semente 7 --config empresa.yaml
"""
import argparse, datetime, json, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from configuracao import carregar, obter

# categoria do mercado → (índice da marca da empresa em marcas_foco ou None, linhas de SKU,
# mercado mensal base em R$, share da empresa no ano anterior, share no ano corrente,
# crescimento do mercado no ano)
CATEGORIAS = [
    ('Limpador Multiuso', 0, ['MULTIUSO ORIGINAL 500ML', 'MULTIUSO LAVANDA 500ML', 'MULTIUSO 750ML',
                              'MULTIUSO REFIL 2L'], 120000, 0.46, 0.49, 0.06),
    ('Limpador Perfumado', 0, ['PERFUMADO FLORAL 2L', 'PERFUMADO CITRUS 2L', 'PERFUMADO 500ML'],
     60000, 0.18, 0.27, 0.11),
    ('Desengordurante', 0, ['COZINHA SQUEEZE 500ML', 'COZINHA REFIL 400ML'], 38000, 0.40, 0.33, 0.09),
    ('Alvejantes', 1, ['PO 450G', 'PO 900G', 'GEL 1,2L', 'LIQUIDO 500ML'], 95000, 0.55, 0.49, 0.04),
    ('Limpador Sanitário', 2, ['GEL 500ML', 'LIMPADOR 750ML', 'CLORO GEL 750ML'], 42000, 0.30, 0.34, 0.05),
    ('Desodorizador Sanitário', 2, ['PEDRA 25G', 'BLOCO ADESIVO'], 21000, 0.22, 0.21, 0.02),
    ('Detergente Lava Louça em Po', 3, ['PO 450G', 'PO 1KG'], 16000, 0.62, 0.66, 0.15),
    ('Detergente Lava Louça Tabletes', 3, ['TABLETES 30UN', 'TABLETES 60UN'], 12000, 0.58, 0.60, 0.22),
    ('Desinfetante Clorado', None, [], 52000, 0.0, 0.0, 0.07),
]
SAZONALIDADE = [0.92, 0.88, 0.97, 0.95, 1.00, 0.98, 1.03, 1.02, 0.99, 1.04, 1.06, 1.16]
CONCORRENTES = ['MARCA CONCORRENTE A', 'MARCA CONCORRENTE B', 'MARCA PROPRIA DA REDE']


def br(v, casas=2):
    """1234.5 → '1.234,50' (formato do export)."""
    s = f'{v:,.{casas}f}'
    return s.replace(',', '#').replace('.', ',').replace('#', '.')


def gravar(caminho, linhas):
    with open(caminho, 'w', encoding='utf-16') as fh:
        fh.write('\n'.join('\t'.join(str(x) for x in r) for r in linhas))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--pasta', required=True)
    ap.add_argument('--rede', default=None)
    ap.add_argument('--mes-corrente', default=None, help='MM/AA do mês parcial (padrão: último período da config)')
    ap.add_argument('--liberada', action='store_true', help='a rede libera as marcas concorrentes em detalhe')
    ap.add_argument('--todos-os-estados', action='store_true', help='exporta todos os estados (sem derivada)')
    ap.add_argument('--semente', type=int, default=7)
    ap.add_argument('--config', default=None)
    a = ap.parse_args()
    cfg = carregar(a.config)
    rnd = random.Random(a.semente)
    os.makedirs(a.pasta, exist_ok=True)

    marcas = [m.upper() for m in obter(cfg, 'produtos.marcas_foco', [])][:4]
    if len(marcas) < 4:
        sys.exit('O exemplo precisa de 4 marcas em produtos.marcas_foco')
    fora = [m.upper() for m in obter(cfg, 'diagnostico_rede.marcas_fora_da_empresa', ['Marca V']) or ['MARCA V']]
    empresa = (obter(cfg, 'meta.empresa', 'Empresa') or 'Empresa').upper()
    rede = a.rede
    if not rede:
        diretos = [c['nome'] for c in obter(cfg, 'clientes.cadastro', []) or [] if c.get('canal') == 'Direto']
        rede = diretos[0] if diretos else 'REDE EXEMPLO'
    rede = rede.upper()
    if a.mes_corrente:
        mm, aa = int(a.mes_corrente[:2]), int(a.mes_corrente[3:])
    else:
        ult = sorted((obter(cfg, 'calendario.periodos', {}) or {'P09': '2026-09'}).values())[-1]
        mm, aa = int(ult[5:7]), int(ult[2:4])

    # meses: setembro de dois anos atrás até o mês corrente (parcial)
    meses, t = [], (2000 + aa - 2) * 12 + 8
    while t <= (2000 + aa) * 12 + mm - 1:
        meses.append(f'{t % 12 + 1:02d}/{(t // 12) % 100:02d}')
        t += 1
    nm = len(meses)
    ufs = [('PA', 14, 13, 0.80), ('TO', 4, 3, 0.20)]          # UF, lojas no ano, lojas no ano anterior, peso
    lojas_tot = sum(u[1] for u in ufs)
    lojas_ant = sum(u[2] for u in ufs)

    # ---------- série mensal por SKU (e concorrência) na rede
    itens = []   # (marca, categoria, ean, nome, [valor por mês], preço, cobertura)
    ean = 7890000000001
    for cat, im, linhas, base, sh_ant, sh_atu, g in CATEGORIAS:
        mercado = []
        for i, m in enumerate(meses):
            mes, ano = int(m[:2]), int(m[3:])
            fator = (1 + g) ** (ano - (aa - 1)) * SAZONALIDADE[mes - 1] * rnd.uniform(0.96, 1.04)
            mercado.append(base * fator * (0.45 if i == nm - 1 else 1.0))
        emp = []
        for i, m in enumerate(meses):
            ano = int(m[3:])
            emp.append(mercado[i] * (sh_atu if ano == aa else sh_ant))
        if im is not None:
            pesos = [rnd.uniform(0.6, 1.4) for _ in linhas]
            ativo = [[1.0] * nm for _ in linhas]
            for i, m in enumerate(meses):
                if cat == 'Limpador Perfumado' and int(m[3:]) < aa:
                    ativo[-1][i] = 0.0                            # SKU novo no ano corrente
                if cat == 'Alvejantes' and int(m[3:]) == aa:
                    ativo[0][i] = 0.0                             # SKU que saiu do mix
            for j, ln in enumerate(linhas):
                vals = []
                for i in range(nm):
                    soma = sum(pesos[k] * ativo[k][i] for k in range(len(linhas)))
                    vals.append(emp[i] * pesos[j] * ativo[j][i] / soma)
                cobertura = 1.0 if j < 2 else rnd.choice([0.65, 0.8, 0.9])
                itens.append((marcas[im], cat, str(ean), f'{marcas[im]} {ln}', vals, rnd.uniform(8, 45), cobertura))
                ean += 7
        resto = [mercado[i] - emp[i] for i in range(nm)]
        if a.liberada:
            nomes = list(CONCORRENTES) + (fora[:1] if cat == 'Desinfetante Clorado' else [])
            pesos = [rnd.uniform(0.5, 1.5) for _ in nomes]
            for j, nmc in enumerate(nomes):
                vals = [resto[i] * pesos[j] / sum(pesos) for i in range(nm)]
                itens.append((nmc, cat, str(ean), f'{nmc} {cat.upper()}', vals, rnd.uniform(6, 30), 0.9))
                ean += 7
        else:
            itens.append(('OUTRA MARCA', cat, '', 'OUTROS PRODUTOS', resto, 12.0, 1.0))

    def lojas_mes(i, cobertura, total_ano, total_ant):
        ano = int(meses[i][3:])
        return round((total_ano if ano == aa else total_ant) * cobertura)

    def export_kpi(nome_arq, peso_uf, lojas_ano, lojas_ano_ant):
        linhas = [['Marca', 'Categoria', 'EAN', 'Produto', 'Medida'] + meses]
        for cat in [c[0] for c in CATEGORIAS]:
            sub_v = [0.0] * nm
            for marca, c_, e, nome, vals, preco, cob in itens:
                if c_ != cat:
                    continue
                v = [x * peso_uf * rnd.uniform(0.97, 1.03) for x in vals]
                sub_v = [sub_v[i] + v[i] for i in range(nm)]
                linhas.append([marca, cat, e, nome, 'Vendas em valor R$'] + [br(x) for x in v])
                linhas.append([marca, cat, e, nome, 'Quantidade de venda'] + [br(x / preco, 0) for x in v])
                linhas.append([marca, cat, e, nome, 'Qtd Lojas'] +
                              [str(lojas_mes(i, cob, lojas_ano, lojas_ano_ant)) if v[i] > 0 else '' for i in range(nm)])
            linhas.append(['', cat, '', 'Total', 'Vendas em valor R$'] + [br(x) for x in sub_v])
        linhas.append(['Total', 'Total', '', '', 'Vendas em valor R$'] + ['1.000.000,00'] * nm)
        gravar(os.path.join(a.pasta, nome_arq), linhas)

    export_kpi('kpi_REDE.csv', 1.0, lojas_tot, lojas_ant)
    for k, (uf, n_ano, n_ant, peso) in enumerate(ufs):
        if k == 0 or a.todos_os_estados:
            export_kpi(f'kpi_UF_{uf}.csv', peso, n_ano, n_ant)

    # ---------- abertura por loja: semanas de 30/03 do ano corrente até o meio do mês corrente
    ini = datetime.date(2000 + aa, 3, 30)
    ini -= datetime.timedelta(days=ini.weekday())
    fim = datetime.date(2000 + aa, mm, 14)
    semanas = []
    d = ini
    while d <= fim:
        semanas.append(d)
        d += datetime.timedelta(days=7)
    nw = len(semanas)
    cab = ['Loja', 'Endereço', 'Categoria', 'Fabricante', 'Marca', 'EAN', 'Produto']
    met = ['', '', '', '', '', '', '']
    for s in semanas:
        cab += [s.strftime('%d/%m/%Y'), '', '', '', '']
        met += ['Preço médio', 'Vendas em valor R$', 'Vendas em kg', 'Quantidade de venda', '% participação']
    linhas = [cab, met]
    itens_emp = [x for x in itens if x[0] in marcas]
    lojas_def = []
    n = 0
    for uf, n_ano, n_ant, peso in ufs:
        for j in range(n_ano):
            n += 1
            nome = f'{rede} LJ{n:02d}'
            end = f'Avenida Exemplo, {100 + n} - Centro - {uf}'
            if n == 11:
                end = 'Rodovia Exemplo, km 4'                     # sem UF: vai para o uf_map.json
            tend = rnd.choice([0.80, 0.86, 0.95, 1.0, 1.04, 1.10, 1.18])
            lojas_def.append((nome, end, uf, peso / n_ano * rnd.uniform(0.6, 1.5), tend))
    uf_map = {}
    for nome, end, uf, peso, tend in lojas_def:
        if '- ' + uf not in end:
            uf_map[nome] = uf
        primeira_loja = True
        for cat in [c[0] for c in CATEGORIAS]:
            primeira_cat = True
            for marca, c_, e, nomesku, vals, preco, cob in itens_emp:
                if c_ != cat or rnd.random() > cob:
                    continue                                       # SKU sem venda na loja: gap de sortimento
                linha = [nome if primeira_loja else '', end if primeira_loja else '',
                         cat if primeira_cat else '', empresa, marca, e, nomesku]
                primeira_loja = primeira_cat = False
                mensal = sum(vals[-4:-1]) / 3                      # ordem de grandeza da semana
                for w in range(nw):
                    fator = (1 + (tend - 1) * (w / max(1, nw - 1))) * (0.5 if w == nw - 1 else 1.0)
                    v = mensal * peso * fator / 4.3 * rnd.uniform(0.85, 1.15)
                    linha += [br(preco), br(v), br(v / preco * 0.5), br(v / preco, 0), br(rnd.uniform(1, 9))]
                linhas.append(linha)
        linhas.append(['', '', 'Total', '', '', '', ''] + ['0,00'] * (5 * nw))
    # ruído que os filtros precisam tirar: uma loja de outra rede e uma marca concorrente
    linhas.append(['OUTRA REDE LOJA 01', 'Rua Exemplo, 9 - PA', 'Limpador Multiuso', 'CONCORRENTE',
                   'MARCA CONCORRENTE A', '7899999999999', 'MARCA CONCORRENTE A 500ML'] + ['1.000,00'] * (5 * nw))
    linhas.append([f'{rede} LJ01', '', 'Limpador Multiuso', 'CONCORRENTE', 'MARCA CONCORRENTE A',
                   '7899999999998', 'MARCA CONCORRENTE A 750ML'] + ['500,00'] * (5 * nw))
    linhas.append(['Total', '', '', '', '', '', ''] + ['9.999.999,00'] * (5 * nw))
    gravar(os.path.join(a.pasta, 'abertura_lojas.csv'), linhas)
    with open(os.path.join(a.pasta, 'uf_map.json'), 'w', encoding='utf-8') as fh:
        json.dump(uf_map, fh, ensure_ascii=False, indent=1)
    print(f'rede {rede}: {len(meses)} meses ({meses[0]} a {meses[-1]}), {len(itens)} itens, '
          f'{len(lojas_def)} lojas, {nw} semanas · arquivos em {a.pasta}')


if __name__ == '__main__':
    main()
