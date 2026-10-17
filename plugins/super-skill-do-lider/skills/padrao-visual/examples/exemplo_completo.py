# -*- coding: utf-8 -*-
"""Exemplo completo do padrão visual: o deck inteiro de uma proposta de reposição.

Caso fictício do livro: a Distribuidora Horizonte, com centros de distribuição (CDs) em Goiás,
Mato Grosso do Sul e Pará, recebe a proposta de pedido do quarto trimestre (T4). O deck tem
capa, três capítulos, números-manchete, tabelas, barras, proposta, programa com régua,
investimento, linha do tempo, onde fecha o ano, plano por UF e fechamento.

Entradas: caminho do PDF de saída (opcional), --config arquivo.yaml (opcional) e
--logo arquivo (opcional, pode repetir: o primeiro é o da empresa, o segundo o do cliente).
Saídas: PDF, HTML e PNGs de conferência (montagem 2x2) ao lado do PDF.
Rodar:
    python3 examples/exemplo_completo.py saida/exemplo_completo.pdf

Empresa, gerente, executiva, marcas e cores vêm da configuração (o exemplo fictício do plugin,
se nenhuma outra estiver em uso). Os números e os contatos do cliente ficam no bloco CASO
abaixo: troque pelo seu caso. Todo total é somado das partes, para o arredondamento da tela
bater com a planilha.
"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'scripts'))
sys.path.insert(0, os.path.join(AQUI, '..', 'assets'))
from deckkit import *  # noqa: E402,F401
from deckkit import CFG, _obter as obter  # noqa: E402

# ---------------- argumentos
args, logos, i = [], [], 1
while i < len(sys.argv):
    a = sys.argv[i]
    if a in ('--config', '--logo'):
        if a == '--logo' and i + 1 < len(sys.argv):
            logos.append(logo(sys.argv[i + 1]))
        i += 2
        continue
    args.append(a)
    i += 1
out = os.path.abspath(args[0] if args else 'exemplo_completo.pdf')
os.makedirs(os.path.dirname(out), exist_ok=True)

# ---------------- quem é quem (da configuração)
EMPRESA = obter(CFG, 'meta.empresa', 'Empresa Exemplo')
GERENTE = obter(CFG, 'organizacao.gerente', 'Pedro')
EXECS = obter(CFG, 'organizacao.executivos', []) or []
EXECUTIVA = EXECS[0]['nome'] if EXECS else 'Luísa Andrade'
MARCAS = ((obter(CFG, 'produtos.marcas_foco', []) or []) + ['Marca X', 'Marca Y', 'Marca Z', 'Marca W'])[:4]
X, Y, Z, W = MARCAS

# ---------------- CASO (dados fictícios: troque pelo seu caso)
CASO = {
    'cliente': 'Distribuidora Horizonte',
    'contatos': ['Sérgio Prado · Sócio e diretor comercial', 'Fátima · Compradora'],
    'periodo': 'T4 2026',
    'mes': 'Outubro de 2026.',
}
CLIENTE = CASO['cliente']
MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
SI25 = [44, 60, 52, 64, 58, 49, 55, 61, 57, 66, 70, 74]               # sell in, mil caixas
SI26 = [29, 67, 43, 42, 38, 36, 52, 63, 58, None, None, None]
# sell in em receita líquida (R$) por CD e trimestre de 2026, e o mesmo recorte de 2025
NR26 = {'Goiás': (9.80e6, 7.10e6, 11.20e6), 'Mato Grosso do Sul': (1.90e6, 2.30e6, 2.60e6), 'Pará': (1.40e6, 1.50e6, 1.60e6)}
NR25 = {'Goiás': (14.20e6, 15.30e6, 11.00e6), 'Mato Grosso do Sul': (0.10e6, 0.12e6, 0.15e6), 'Pará': (1.32e6, 1.45e6, 1.52e6)}
SO_VAR = -0.027                                                      # sell out jan a set contra 2025
SO_RS = 48.6e6
ESTOQUE_GO_SEM = 6.7                                                  # semanas de estoque no CD Goiás
PDV_Q3_Q2 = [('Tocantins', .27), ('Goiás', .13), ('Mato Grosso do Sul', .09), ('Pará', -.02), ('Atacado', -.11)]
# segmentos: (marca, segmento, venda do cliente no T3 em caixas, semanas GO, MS, PA)
SEG = [(X, 'Multiuso', 41200, 3.1, 5.2, 13.4), (X, 'Piso', 28800, 4.6, 8.1, 9.7), (Y, 'Líquido', 19500, 3.8, 6.4, 12.9),
       (Y, 'Pó', 15100, 5.9, 9.3, 7.8), (X, 'Banheiro', 11700, 7.4, 3.6, 10.2), (Z, 'Gel', 9800, 2.9, 7.7, 15.1),
       (W, 'Tabletes', 6400, 8.8, 11.6, 6.1), (Z, 'Pastilha', 4900, 12.6, 4.4, None)]
# proposta: R$ por CD e período (P10, P11, P12)
PROP = {'Goiás': (4136000.00, 4988000.00, 3524000.00), 'Mato Grosso do Sul': (635000.00, 766000.00, 541000.00),
        'Pará': (380837.82, 458510.31, 323116.04)}
FIM_T4_SEM = {'Goiás': 9.4, 'Mato Grosso do Sul': 9.1, 'Pará': 9.0}
PROP_MARCA = {X: 10.63e6, Y: 3.43e6, Z: 1.11e6, W: 0.58e6}
BASE_INV, PCT_PROGRAMA, PCT_ACELERADOR = 16e6, 0.010, 0.025
NR25_ANO, NR26_PEDIDO_T4, JBP = 58.4e6, 14.9e6, 0.075

# ---------------- contas (totais sempre somados das partes)
nr26_tri = [sum(v[q] for v in NR26.values()) for q in range(3)]
nr25_tri = [sum(v[q] for v in NR25.values()) for q in range(3)]
nr26_ytd, nr25_ytd = sum(nr26_tri), sum(nr25_tri)
prop_per = [sum(v[k] for v in PROP.values()) for k in range(3)]
PV = sum(prop_per)
INV = BASE_INV * (PCT_PROGRAMA + PCT_ACELERADOR)
ANO26 = nr26_ytd + NR26_PEDIDO_T4
META_ANO = NR25_ANO * (1 + JBP)
mi2 = lambda x: mi(x, 2)


def semanas(v):
    """semáforo de estoque: abaixo de 4 vermelho, 4 a 7 amarelo, 7 a 12 verde, acima de 12 excesso."""
    if v is None:
        return '-'
    c = VERMELHO if v < 4 else (AMARELO if v < 7 else (VERDE if v <= 12 else APOIO))
    return f'<b style="color:{c}">{d1(v)}</b>'


d = Deck(f'{EMPRESA} × {CLIENTE} · Planejamento de reposição {CASO["periodo"]}', logos=logos,
         title=f'{EMPRESA} × {CLIENTE}')

# 1 capa (sem fotos: o deckkit desenha o marcador; com foto, passe img('arquivo.png'))
d.cover(['Reposição', CASO['periodo']], f'O pedido que fecha o trimestre da {CLIENTE}.',
        CASO['contatos'] + [f'{GERENTE} e {EXECUTIVA} · {EMPRESA}'],
        CASO['mes'], 'Como foi o ano, onde está o estoque e a proposta.',
        shelf=[('Capítulo 01', 'Como foi o ano', 'Sell in, sell out e positivação', None, '50% 50%'),
               ('Capítulo 02', 'Onde está o estoque', 'Semanas por segmento e o CD Goiás', None, '50% 50%'),
               ('Capítulo 03', 'A proposta do T4', 'Pedido, investimento e agenda', None, '50% 50%')])

# capítulo 01
d.chapter('01', 'Como foi o ano', 'Sell in e sell out por trimestre e por operação.')
d.slide('O ano em números', f'A demanda da {CLIENTE} se manteve. Quem caiu foi a compra.',
        statement(('Sell out · jan a set/26', pc(SO_VAR, 1), f'{mi(SO_RS)} vendidos aos clientes da distribuidora, contra jan a set/25', AMARELO),
                  ('Sell in · jan a set/26', pc(nr26_ytd / nr25_ytd - 1, 1), f'{mi(nr26_ytd)} em receita líquida', VERMELHO),
                  ('Estoque de Goiás hoje', f'{n0(ESTOQUE_GO_SEM * 7)} dias', f'{d1(ESTOQUE_GO_SEM)} semanas · meta contratual de 9', VERMELHO)),
        read='2025 terminou com estoque alto e o 1º semestre de 2026 consumiu esse estoque. Agora Goiás está curto e o trimestre que mais vende está começando.')
d.slide('Sell in · mês a mês', 'O 2º trimestre foi o vale. No 3º a compra voltou ao nível de 2025.',
        bars(MES, SI25, SI26, 'Sell in 2025', 'Sell in 2026', 'mil caixas'))
linhas = []
for cd in NR26:
    a, b = sum(NR25[cd]), sum(NR26[cd])
    cel = [f'<b>{cd}</b>']
    for q in range(3):
        base = NR25[cd][q]
        cel.append(f'{mi(NR26[cd][q])}<br><small>{pc(NR26[cd][q] / base - 1) if base > 3e5 else "CD novo"}</small>')
    cel.append(f'<b>{mi(b)}</b><br><small>{pc(b / a - 1) if a > 1e6 else "CD novo"}</small>')
    linhas.append(cel)
total = ['<b>TOTAL</b>'] + [f'<b>{mi(nr26_tri[q])}</b><br><small>{pc(nr26_tri[q] / nr25_tri[q] - 1)}</small>' for q in range(3)] + \
        [f'<b>{mi(nr26_ytd)}</b><br><small>{pc(nr26_ytd / nr25_ytd - 1)}</small>']
d.slide('Sell in · por operação', 'Em valor, a distribuidora comprou menos. MS virou CD de compra própria e Goiás recuperou no T3.',
        tab(['Operação (receita líquida)', 'T1/26', 'T2/26', 'T3/26', 'Jan a set/26'], linhas, total, cls='big'),
        read='Parte da queda de Goiás é a migração do MS: em 2025 o CD Goiás abastecia Campo Grande; em 2026 o MS compra direto. Setembro ainda provisório.')
d.slide('Marcas e positivação', f'{X} e {Y} são {p0((PROP_MARCA[X] + PROP_MARCA[Y]) / PV)} do pedido. A base de clientes voltou a crescer.',
        two(tab(['Marca', 'Proposta T4', 'Peso'], [[marca(m), mi2(v), p0(v / PV)] for m, v in PROP_MARCA.items()],
                ['TOTAL', mi2(sum(PROP_MARCA.values())), p0(sum(PROP_MARCA.values()) / PV)], cls='mid'),
            hbars(PDV_Q3_Q2, W=640) + note('PDVs positivados por mês, média do T3 contra a média do T2.')))

# capítulo 02
d.chapter('02', 'Onde está o estoque', 'Semanas por segmento e o CD Goiás hoje.')
d.slide('Segmentos · venda e estoque', 'Os segmentos que mais vendem. E as semanas de estoque em cada CD.',
        tab(['Marca · segmento', 'Venda do cliente T3 (cx)', 'CD Goiás (sem.)', 'CD MS (sem.)', 'CD Pará (sem.)'],
            [[f'<b>{m}</b> · {s}', mil(v), semanas(go), semanas(ms), semanas(pa)] for m, s, v, go, ms, pa in SEG], cls='tight') +
        note(f'<b style="color:{VERMELHO}">●</b> abaixo de 4 semanas · <b style="color:{AMARELO}">●</b> 4 a 7 (atenção) · '
             f'<b style="color:{VERDE}">●</b> 7 a 12 · <b style="color:{APOIO}">●</b> acima de 12 (excesso)'))

# capítulo 03
d.chapter('03', 'A proposta do T4', 'O pedido, o investimento e a agenda.')
linhas = [[f'<b>{cd}</b>', mi2(v[0]), mi2(v[1]), mi2(v[2]), f'<b>{mi2(sum(v))}</b>', f'{d1(FIM_T4_SEM[cd])} sem · {n0(FIM_T4_SEM[cd] * 7)} dias']
          for cd, v in PROP.items()]
d.slide('A proposta', f'Pedido de {mi2(PV)} no T4 em três entradas. Sem carregar o Pará.',
        hero(f'Proposta de pedido do T4 · {CLIENTE}', mi2(PV), ' · '.join(f'{p} <b>{mi2(v)}</b>' for p, v in zip(('P10', 'P11', 'P12'), prop_per))) +
        tab(['CD (R$ faturado)', 'P10 · outubro', 'P11 · novembro', 'P12 · dezembro', 'T4', 'Estoque no fim do T4'], linhas,
            ['<b>TOTAL</b>'] + [f'<b>{mi2(v)}</b>' for v in prop_per] + [f'<b>{mi2(PV)}</b>', ''], cls='mid'))
d.slide('Programa de parceria · mecânica', 'Dois pilares mais o acelerador para a execução no T4',
        pillars([(1, 'EXECUÇÃO', 600, 'Indicadores que sustentam o ponto de venda.', [('1.1', 'Giro no PDV', 300), ('1.2', 'MSL', 300)]),
                 (2, 'FOCO', 400, 'Indicadores do crescimento prioritário.', [('2.1', 'Segmento foco', 200), ('2.2', 'Positivação', 200)]),
                 (3, 'ACELERADOR', 600, 'Impulso adicional ao sell in.', [('3.1', 'Sell in contra a meta', 300), ('3.2', 'Ponto extra', 300)])],
                regua=[(f'{a}%', d1(p * 100) + '%', f'{rsk(BASE_INV * p)} na distribuidora') for a, p in ((60, .010), (70, .015), (80, .020))]))
d.slide('Investimento e agenda', f'A empresa investe até {d1((PCT_PROGRAMA + PCT_ACELERADOR) * 100)}%, {rsk(INV)}, para antecipar e fechar o T4',
        invest(d1((PCT_PROGRAMA + PCT_ACELERADOR) * 100) + '%', rsk(INV), f'sobre {mi(BASE_INV, 0)} de sell in do T4',
               [('Programa de parceria', d1(PCT_PROGRAMA * 100) + '%', f'<b>{rsk(BASE_INV * PCT_PROGRAMA)}</b> · régua de entrada (60%)'),
                ('Acelerador de fechamento', d1(PCT_ACELERADOR * 100) + '%', f'<b>{rsk(BASE_INV * PCT_ACELERADOR)}</b> · antecipação na agenda')]) +
        timeline([('14/10', 'Entrada dos pedidos P10 dos três CDs'), ('até 31/10', 'Faturamento do P10 e da antecipação'),
                  ('2ª quinzena', 'Entrada do pedido P11'), ('novembro', 'Entrada do pedido P12')]),
        read='O programa só abre para quem bater o sell in contra a meta em P10 e P11. O acelerador é pago sobre o faturado na agenda, em verba de sell out por resultado.')
d.slide('Onde fechamos 2026', f'Com o pedido, 2026 fecha em {mi(ANO26)}. A meta de +7,5% pede {mi(META_ANO - ANO26)} a mais.',
        two(columns([('2025|realizado', NR25_ANO, BARRA_ANTERIOR), ('2026|jan a set + pedido T4', ANO26, DESTAQUE),
                     ('Meta 2026|+7,5%', META_ANO, BARRA_REFERENCIA)], fmt=mi),
            stack(kpi('Ano 2026 com o pedido', mi(ANO26), pc(ANO26 / NR25_ANO - 1, 1) + ' contra 2025', DESTAQUE),
                  kpi('T4 com o pedido', mi(NR26_PEDIDO_T4), 'receita líquida do pedido faturado'),
                  kpi('Para a meta de +7,5%', mi(META_ANO - ANO26) + ' a mais', 'vem do sell out: giro acima do ritmo atual', CINZA)),
            wide_left=True))
d.slide('O plano de sell out', 'A reposição só se sustenta com sell out. Uma frente por UF.',
        numbered([('Goiás', 'Sustentar a base de PDVs do T3 sem ruptura: reposição semanal dos itens com menos de 4 semanas.'),
                  ('Tocantins', f'Converter a base nova em volume: ticket médio caiu, foco em {X} Multiuso.'),
                  ('Atacado', 'Recuperar a base perdida em 2026: lista de clientes sem compra e campanha de reativação.'),
                  ('Mato Grosso do Sul', f'O CD que mais acelera: garantir abastecimento de {X} Multiuso e {Y} Líquido.'),
                  ('Pará', 'Girar o estoque acima de 12 semanas antes de novas compras: ação de sell out nos itens parados.')]))
d.slide('O que sai desta sala', 'Pedidos do T4 na mão. Agenda combinada.',
        checklist([f'Pedido P10 dos três CDs: <b>{mi2(prop_per[0])}</b>, entrada em 14/10 e faturamento até 31/10',
                   f'Pedido P11: <b>{mi2(prop_per[1])}</b>, entrada na 2ª quinzena de outubro',
                   f'Pedido P12: <b>{mi2(prop_per[2])}</b>, entrada em novembro',
                   f'Investimento de até <b>{rsk(INV)}</b>: <b>{rsk(BASE_INV * PCT_PROGRAMA)}</b> do programa + <b>{rsk(BASE_INV * PCT_ACELERADOR)}</b> de acelerador',
                   f'Plano de sell out por UF com acompanhamento quinzenal ({GERENTE}, {EXECUTIVA} e o time de compras)']))
print(d.save(out))
