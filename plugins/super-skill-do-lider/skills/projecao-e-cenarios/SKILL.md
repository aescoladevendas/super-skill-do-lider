---
name: projecao-e-cenarios
description: Melhor estimativa (BE) do mês e do trimestre, com cenários de queda, estabilização e crescimento cliente a cliente. Use em "BE", "como pousa o trimestre", "quanto falta para a meta".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Projeção e cenários: a melhor estimativa (BE) do Sell In

Método para a melhor estimativa (best estimate, BE) que a empresa pede à regional, para a
projeção de fechamento do mês e do trimestre e para os cenários de reversão do ano (queda,
estabilização e crescimento), com diagnóstico falado e memória de cálculo cliente a cliente.
Implementação: `scripts/projetar_cenarios.py`; o detalhe do motor, com exemplo numérico, está em
`references/motor-projecao.md`. Parâmetros na seção `projecao` do arquivo de configuração.

## Quando acionar
"BE", "best estimate", "projeção do mês", "como pousa o trimestre", "quanto falta para a meta" ou
"para os 85%", "cenários", "plano de reversão", "quanto fica o acumulado do ano", "gap acumulado",
"quanto preciso no próximo trimestre", "gap por cliente contra a meta", ou quando o usuário anexar
o arquivo oficial de BE da regional. Não é para painel (use painel-de-indicadores) nem para deck
(use book-executivo ou apresentacao-executiva).

## O arquivo oficial de BE (estrutura em `projecao.arquivo_be`)
- Semanal (W1 a W4), um arquivo por regional e unidade; uma linha por cliente.
- Colunas fixas (letras na config): meta do mês · carteira atual · em trânsito no mês · data limite
  de pedido · **data prevista de subida** (preencher) · **previsão de subida em caixas por marca**
  (o que o gerente preenche, uma coluna por marca de `produtos.marcas_foco`) · soma · validação
  da data contra o limite · **ajuste colaborativo** (desconto da empresa sobre carteira + subidas,
  `ajuste_colaborativo_pct`) · **BE final** = carteira + trânsito + subidas + ajuste · BE contra a
  meta · histórico das semanas anteriores.
- Portanto o que se escreve nas colunas de marca vira BE final × (1 + ajuste). Reporte SEMPRE os
  dois números ("146 mil nas subidas → BE final de cerca de 132 mil").
- Filtre as linhas pelo gerente (`filtro_coluna` = `organizacao.gerente`). Um mesmo cliente pode
  aparecer em várias linhas com o mesmo nome (operações por UF): separe pela descrição e pelo
  código (regras da skill identidade-de-clientes). Clientes com dois códigos ou com código migrado
  seguem `clientes.migracoes` e `clientes.merges_grupo`.
- Nunca altere fórmulas do arquivo oficial: escreva só a data de subida e as colunas de marca.
  Entregue uma cópia com o sufixo de `sufixo_saida` e uma aba nova de memória
  (`PROJECAO_<mês>`), e copie para a pasta compartilhada do time (`caminhos.compartilhada`).

## Fontes (nesta ordem, sempre a base mais fresca)
1. `dados_painel.json` da skill painel-de-indicadores: faturado do ano por cliente e mês, carteira
   aberta, mix por marca e referência do ano anterior por cliente. Confira a data de modificação
   antes de usar: outra sessão pode ter atualizado a base. Sem o JSON (o motor do painel entra na
   versão 0.2), use os CSVs `--historico` e `--carteira`, no formato descrito no script.
2. A planilha de metas (`arquivos.metas`): meta por cliente e mês, e o histórico do primeiro
   semestre contra o ano anterior.
3. As metas do trimestre das contas com régua de verba (`projecao.contas_regua_trimestre`).
4. Números-âncora do usuário quando divergirem da base (ex.: "o semestre fechou em -148 mil"): use
   o número dele como âncora e declare a diferença e a provável origem (mês fora da base, fonte
   financeira diferente).

## O motor de projeção por cliente (resumo; detalhe em references/)
```
ritmo curto = média(mês fechado, mês em curso projetado)
              mês em curso projetado = parcial × dias úteis totais ÷ decorridos, LIMITADO ao maior
              mês do ano do cliente; se o parcial já é >= 90% do mês fechado → "mês feito"
ritmo longo = média dos seis meses até o mês fechado (positivos)
BASE = 50% curto + 50% longo
ESTABILIZAÇÃO = BASE × sazonalidade (mês alvo ÷ média dos dois meses anteriores, no ano anterior,
                do próprio cliente, entre 0,6 e 1,4)
QUEDA = × 0,90 · CRESCIMENTO = maior entre × 1,075 e o necessário para o acumulado +7,5%,
                com teto de 1,5× ou a meta
PROJEÇÃO (vai para o BE) = ESTABILIZAÇÃO + regras de evidência:
  (a) mês em curso zerado e fechado > 0 → base = mês fechado   (b) sem venda nos dois → média do ano
  (c) piso de 60% da carteira aberta
  (d) contas com régua de verba: no último mês do trimestre, puxar até o gap de 85% da meta do
      trimestre (teto 1,3×)
Mix por marca = mix dos três últimos meses do cliente (senão `produtos.mix_padrao_regional`)
Data de subida = sexta-feira da 2ª semana, dentro de todos os limites de pedido
```
Contas de pedido grande e irregular (distribuidores e atacados) NUNCA extrapolam pelo dia útil
sem o teto: foi o erro da primeira rodada do método, que projetou uma conta muito acima do que
ela já tinha feito em qualquer mês do ano; com o teto, a projeção voltou para o patamar real.

```bash
python3 scripts/projetar_cenarios.py --dados <dados_painel.json> --metas metas.csv \
        --mes-alvo 2026-09 --dias-decorridos 11 [--be BE_oficial.xlsx] [--falar]
# ou, sem o painel: --historico historico.csv --carteira carteira.csv
```

## Diagnóstico: a estrutura fixa da resposta (falada e escrita)
1. Ponto de partida: o semestre (realizado contra meta, gap, % contra o ano anterior) e a origem
   do plano de três cenários.
2. Mês a mês do trimestre: fechado / em curso (dias úteis e carteira) / BE → total do trimestre
   contra a meta.
3. Como chegou: o método em um parágrafo e os 8 a 10 maiores clientes com o número.
4. Acumulado do ano: gap do semestre + Δ do trimestre → gap no fim do trimestre; % recuperado;
   ano contra ano.
5. Trimestre seguinte: quanto acima da régua para fechar 100%; teste da ambição (+7,5%), dizendo
   claramente quando está fora do alcance.
6. Diagnóstico em três pontos: em que cenário estamos de fato · riscos concentrados (contas e
   pedidos que movem o número) · recomendação (BE sem inflar, argumento de calibração de metas,
   onde pôr a energia comercial).

Fale o resumo (`--falar` usa `projecao.voz_resumo`, no macOS) e deixe as tabelas por escrito.
Rótulos honestos: faixa para o mês em curso, dependência de um pedido, colunas com teto de
sazonalidade.

## Regras que o método quer ver evoluir (próximas versões)
- A régua de verba comercial (`projecao.regua_meta`, 85% da meta) aparece sempre: mostre "falta
  para 100%" e "falta para 85%".
- Abrir **Sell Out** e **estoque dos clientes** (regra: cerca de 9 semanas de estoque) para
  calibrar o Sell In projetado por cliente (pedido = demanda menos estoque em excesso).
- Histórico cada vez mais fiel: trocar a referência do ano anterior da planilha mestre pelo
  relatório financeiro reapresentado e pelas bases por cliente; incluir no painel o mês que faltar.
- Reaproveitar o script toda semana (W2, W3...) só trocando a base.

## Acompanhamento da acurácia e da rotina do gerente (planilha de governança pessoal)
Modelo de planilha para o gerente acompanhar a própria rotina com a máquina, regravada toda
segunda com a base nova (as colunas semanais guardam a evolução):
- Abas: LEITURA · CALENDARIO (grade mensal: BE e entregas, rotina automática, limites de pedido,
  fechamentos, cada um com uma cor) · ROTINA (diário, semanal, mensal) · RECOMENDACOES (status e
  uma coluna por semana) · CENARIOS · ACURACIA_BE (W1 a W4 contra o real, erro por cliente e
  executivo) · CADENCIA_CLIENTES (ciclo = mediana dos intervalos entre semanas com pedido,
  faturado + carteira; semáforo; colunas de Sell Out e estoque → semanas de estoque, alvo de até
  9) · ACOES_HOJE (5 clientes por executivo, por pontuação) · CAMADAS (topo, meio e cauda).
- Planilha de acurácia do time, na pasta compartilhada: o time preenche a coluna EXECUTIVO da
  semana vigente; a máquina preenche MOTOR toda segunda e REAL no fechamento, e atualiza a célula
  de semana vigente e o destaque. Regra: só o time escreve nas colunas EXECUTIVO; ao regravar,
  PRESERVE o que o time preencheu (ler antes, reescrever depois). Todo BE recebido da empresa vai
  para uma subpasta de originais, sempre.
- Comentário sempre falado.

## Integração
Lê o JSON da skill painel-de-indicadores e as regras da skill identidade-de-clientes; o raciocínio
de diagnóstico segue a skill escola-de-vendas; o texto passa pela skill revisao-final.
