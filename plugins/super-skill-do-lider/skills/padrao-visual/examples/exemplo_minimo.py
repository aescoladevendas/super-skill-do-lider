# -*- coding: utf-8 -*-
"""Exemplo mínimo do padrão visual: um slide de cada componente do deckkit.

Entradas: caminho do PDF de saída (opcional) e --config arquivo.yaml (opcional).
Saídas: PDF, HTML e PNGs de conferência (montagem 2x2) ao lado do PDF.
Rodar para validar o ambiente:
    python3 examples/exemplo_minimo.py saida/exemplo_minimo.pdf
Nomes, marcas e cores vêm da configuração (o exemplo fictício do plugin, se nenhuma outra
estiver em uso). Os números são ilustrativos.
"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'scripts'))
sys.path.insert(0, os.path.join(AQUI, '..', 'assets'))
from deckkit import *  # noqa: E402,F401
from deckkit import CFG, _obter as obter  # noqa: E402

args = [a for i, a in enumerate(sys.argv[1:], 1) if a != '--config' and sys.argv[i - 1] != '--config']
out = os.path.abspath(args[0] if args else 'exemplo_padrao_visual.pdf')
os.makedirs(os.path.dirname(out), exist_ok=True)

empresa = obter(CFG, 'meta.empresa', 'Empresa Exemplo')
gerente = obter(CFG, 'organizacao.gerente', 'Gerente')
marcas = (obter(CFG, 'produtos.marcas_foco', []) or []) + ['Marca X', 'Marca Y', 'Marca Z']
m1, m2, m3 = marcas[0], marcas[1], marcas[2]

d = Deck(f'{empresa} × Cliente · Exemplo do padrão visual')
d.cover(['Reposição', 'T4 2026'], 'Frase de apoio que resume a decisão.',
        ['Nome · Diretor', 'Nome · Gerente', f'{gerente} · {empresa}'],
        'Outubro de 2026.', 'O ano, o estoque e a proposta.',
        shelf=[('Capítulo 01', 'Como foi o ano', 'sell in e sell out', None, '50% 50%'),
               ('Capítulo 02', 'Onde está o estoque', 'semanas por segmento', None, '50% 50%'),
               ('Capítulo 03', 'A proposta', 'pedido, investimento e agenda', None, '50% 50%')])
d.chapter('01', 'Como foi o ano', 'Sell in e sell out por trimestre.')
d.slide('O ano em números', 'A demanda se manteve. Quem caiu foi a compra.',
        statement(('Sell out', '-2,7%', 'contra 2025', AMARELO), ('Sell in', '-13,0%', 'em receita líquida', VERMELHO),
                  ('Estoque', '47 dias', 'meta de 9 semanas', VERMELHO)),
        read='Leitura curta que explica o porquê.')
d.slide('Sell in · mês a mês', 'O 2º trimestre foi o vale. No 3º a compra voltou.',
        bars(['jan', 'fev', 'mar', 'abr'], [44e3, 60e3, 52e3, 64e3], [29e3, 67e3, 43e3, 42e3],
             'Sell in 2025', 'Sell in 2026', 'mil caixas', fmt=lambda v: n0(v / 1e3)))
d.slide('Por operação', 'Pará e MS crescem. Atacado não vem.',
        tab(['Operação', 'T3 (R$ Mi)', 'x T2'], [['<b>Goiás</b>', '11,2', var(0.018)], ['<b>Atacado</b>', '0,9', var(-0.112)]],
            ['GRUPO', '12,1', var(0.008)], cls='big'),
        read='Fonte e recorte em uma frase.')
d.slide('Marcas', f'{m1} e {m2} são 89% do pedido. Goiás concentra 80%.',
        two(tab(['Marca', 'T4'], [[marca(m1), 'R$ 10,63 Mi'], [marca(m2), 'R$ 3,43 Mi'], [marca(m3), 'R$ 0,58 Mi']], cls='mid'),
            hbars([('Goiás', .13), ('Pará', -.02)], W=600)))
d.slide('A proposta', 'Pedido de R$ 15,75 Mi no T4 em três entradas',
        hero('Proposta do T4', 'R$ 15,75 Mi', 'P10 <b>R$ 5,15 Mi</b> · P11 <b>R$ 6,21 Mi</b> · P12 <b>R$ 4,39 Mi</b>') +
        tab(['CD', 'T4'], [['<b>Goiás</b>', 'R$ 12,65 Mi'], ['<b>Outros CDs</b>', 'R$ 3,10 Mi']], ['GRUPO', 'R$ 15,75 Mi'], cls='big'))
d.slide('Programa', 'Dois pilares mais o acelerador',
        pillars([(1, 'EXECUÇÃO', 600, 'Indicadores de ponto de venda.', [('1.1', 'Giro no PDV', 300), ('1.2', 'MSL', 300)]),
                 (2, 'FOCO', 400, 'Crescimento prioritário.', [('2.1', 'Segmento foco', 200), ('2.2', 'Positivação', 200)]),
                 (3, 'ACELERADOR', 600, 'Impulso adicional.', [('3.1', 'Sell in contra a meta', 300), ('3.2', 'Ponto extra', 300)])],
                regua=[('60%', '1,0%', 'R$ 160 mil'), ('70%', '1,5%', 'R$ 240 mil'), ('80%', '2,0%', 'R$ 320 mil')]))
d.slide('Investimento e agenda', 'A empresa investe até 3,5%, R$ 560 mil, para fechar o T4',
        invest('3,5%', 'R$ 560 mil', 'sobre R$ 16 Mi de sell in',
               [('Programa de parceria', '1,0%', '<b>R$ 160 mil</b> · régua de entrada'), ('Acelerador', '2,5%', '<b>R$ 400 mil</b> · antecipação')]) +
        timeline([('14/10', 'pedido P10'), ('31/10', 'faturamento'), ('2ª quinzena', 'pedido P11'), ('novembro', 'pedido P12')]),
        read='Regra do investimento em uma frase.')
d.slide('Plano', 'A reposição só se sustenta com sell out. Uma frente por UF.',
        numbered([('Goiás', 'texto'), ('Tocantins', 'texto'), ('Pará', 'texto')]))
d.slide('O que sai desta sala', 'Pedidos na mão. Agenda combinada.',
        checklist(['Pedido P10: <b>R$ 5,15 Mi</b>, entrada em 14/10', 'Investimento de até <b>R$ 560 mil</b>']))
print(d.save(out))
