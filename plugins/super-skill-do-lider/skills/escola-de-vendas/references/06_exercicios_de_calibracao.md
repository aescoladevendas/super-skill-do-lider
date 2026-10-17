# 06 · Exercícios de calibração

> Os 60 exercícios do livro "A Escola de Vendas", dez por capítulo, com gabarito e justificativa.
> Servem como casos de teste desta skill.

Cada exercício tem quatro alternativas e uma única resposta certa. As alternativas erradas
reproduzem enganos frequentes da profissão (dividir pela base errada, esquecer a linha de base,
confundir margem com markup, somar o crédito do fabricante ao investimento do distribuidor em vez
de subtraí-lo), e muitas justificativas explicam também o engano por trás delas.

## Como usar como teste da skill

1. Apresente à skill só o enunciado e as alternativas, sem o gabarito.
2. Compare a letra escolhida com o gabarito e o raciocínio com a justificativa: nos exercícios de
   cálculo, a conta precisa seguir a fórmula da referência do capítulo, com os mesmos números.
3. Registre acerto ou erro por exercício. Um erro aponta a referência a revisar (indicada no título
   de cada capítulo abaixo); a meta é acertar os 60.
4. Repita a bateria inteira sempre que alterar uma regra, uma fórmula ou o roteamento da skill.

## Capítulo 1 · Leitura de dados

Referência da skill: `01_leitura_de_dados.md`.

**C1-E01** (conceito e aplicação). Um atacadista acompanha semanalmente os níveis de estoque para evitar ruptura e ajusta as compras antes das datas sazonais. Esse uso dos dados está associado principalmente a qual dos três Vs?

- (A) Volume
- (B) Variedade
- (C) Velocidade
- (D) Nenhum dos três, porque se trata de uma decisão de compras

**Gabarito: C.** Acompanhar os níveis de estoque para evitar vendas perdidas por ruptura e reagir a eventos sazonais são os dois usos típicos da velocidade, o ritmo em que os dados são gerados e atualizados. Volume se refere à quantidade de dados, e variedade, aos tipos de dados combinados na análise.

**C1-E02** (conceito e aplicação). Você quer saber se as vendas de um cliente estão crescendo mais ou menos que o mercado da região. Qual fonte é a mais adequada?

- (A) Dados de PDV de categoria de terceiros (painel de varejo)
- (B) Sell-in em nível de distribuidor
- (C) Dados de PDV do próprio varejista
- (D) Painel de shopper

**Gabarito: A.** Os dados de PDV de categoria de terceiros (painel de varejo) oferecem a leitura do mercado e da categoria e permitem comparar o cliente com o mercado. O sell-in mostra o que o fabricante vendeu ao cliente, o PDV do varejista mostra apenas aquele cliente e o painel de shopper descreve o comportamento de compra dos domicílios.

**C1-E03** (cálculo). Uma promoção vendeu 20.000 unidades em um período cuja linha de base era de 8.000 unidades. Qual foi o uplift?

- (A) 40%
- (B) 60%
- (C) 150%
- (D) 250%

**Gabarito: C.** Volume incremental = volume promocional − linha de base = 20.000 − 8.000 = 12.000 unidades. Uplift = 12.000 ÷ 8.000 = 150%. A opção A divide a linha de base pelo volume da promoção (8.000 ÷ 20.000); a opção B divide o incremental pelo volume da promoção (12.000 ÷ 20.000); a opção D divide o volume total pela linha de base (20.000 ÷ 8.000), sem descontar a base.

**C1-E04** (cálculo). No caso do exercício anterior, o lucro bruto regular é de R$ 3,00 por unidade e o desconto da promoção foi de R$ 1,00 por unidade. Qual foi o lucro bruto incremental?

- (A) R$ 12.000
- (B) R$ 16.000
- (C) R$ 36.000
- (D) R$ 40.000

**Gabarito: B.** Lucro bruto da promoção por unidade = R$ 3,00 − R$ 1,00 = R$ 2,00. Lucro bruto na promoção = 20.000 × R$ 2,00 = R$ 40.000. Lucro bruto da linha de base = 8.000 × R$ 3,00 = R$ 24.000. Lucro bruto incremental = R$ 40.000 − R$ 24.000 = R$ 16.000. A opção A repete o volume incremental (12.000 unidades) como se fosse valor em reais, a opção C valoriza as unidades incrementais pela margem regular (12.000 × R$ 3,00), ignorando o desconto, e a opção D é o lucro bruto total do período.

**C1-E05** (cálculo). Ainda no mesmo caso, os custos totais da promoção somaram R$ 8.000. Qual afirmação está correta?

- (A) O ROI bruto é 2,0 e o ROI líquido é 100%, portanto o evento foi positivo.
- (B) O ROI bruto é 2,0 e o ROI líquido é 200%.
- (C) O ROI líquido é 0%, portanto o evento ficou no ponto de equilíbrio.
- (D) O ROI bruto é 5,0, porque deve ser calculado sobre o lucro bruto total do período promocional.

**Gabarito: A.** ROI bruto = R$ 16.000 ÷ R$ 8.000 = 2,0. ROI líquido = (R$ 16.000 − R$ 8.000) ÷ R$ 8.000 = 1,0, ou 100%, acima do ponto de equilíbrio de 0%. A opção B confunde ROI bruto com ROI líquido; a opção C trataria como equilíbrio um evento que gerou o dobro do custo; a opção D usa o lucro total (R$ 40.000 ÷ R$ 8.000) em vez do lucro incremental.

**C1-E06** (cálculo). Um distribuidor vendeu R$ 1,35 milhão em produtos da empresa nas últimas 12 semanas, contra R$ 1,5 milhão no mesmo período do ano anterior. Os outros distribuidores da região cresceram 4%. Um item do MSL ficou quatro semanas em ruptura e, antes disso, vendia R$ 15 mil por semana. Na base comparável, uma promoção gerou R$ 60 mil em vendas incrementais e não se repetiu. Quanto da queda continua sem explicação, e qual é o passo seguinte?

- (A) Nada; a ruptura e a promoção da base explicam a queda inteira.
- (B) R$ 90 mil; o passo seguinte é reavaliar o calendário promocional.
- (C) R$ 30 mil; o passo seguinte é pedir verba para uma promoção que compense a diferença.
- (D) R$ 30 mil; o passo seguinte é investigar preço, concorrência e sortimento.

**Gabarito: D.** Queda = R$ 1,5 milhão − R$ 1,35 milhão = R$ 150 mil, ou 10%. A primeira etapa descarta o mercado, porque os outros distribuidores da região cresceram 4%. A ruptura explica 4 × R$ 15 mil = R$ 60 mil, e o efeito de base da promoção, outros R$ 60 mil; juntos somam R$ 120 mil, e restam R$ 150 mil − R$ 120 mil = R$ 30 mil sem explicação. Percorridas as três etapas, o passo seguinte é investigar preço, concorrência e sortimento, como na última linha da Tabela 1.4. A opção A erra a soma, a opção B desconta só a promoção (R$ 150 mil − R$ 60 mil) e esquece a ruptura, e a opção C pede verba antes de conhecer a causa restante, o erro comum descrito na seção 1.3.

**C1-E07** (cálculo). Um distribuidor tem quatro lacunas de MSL, com potencial mensal estimado de R$ 52 mil (M1), R$ 28 mil (M2), R$ 12 mil (M3) e R$ 8 mil (M4). Seguindo a lógica 80/20, como priorizar a conversa?

- (A) Apresentar as quatro lacunas com o mesmo peso, para maximizar o pedido.
- (B) Concentrar a conversa em M1 e M2, que somam R$ 80 mil, ou 80% do potencial.
- (C) Começar por M3 e M4, que são menores e mais fáceis de aprovar.
- (D) Apresentar apenas M1, que sozinha representa 80% do potencial.

**Gabarito: B.** O potencial total é de R$ 100 mil. M1 representa 52% e M2, 28%; juntas, somam R$ 80 mil, ou 80% do potencial, com metade das lacunas. A opção A dilui o argumento, a opção C começa pelo menor ganho e a opção D erra a conta, porque M1 sozinha representa 52%, e não 80%.

**C1-E08** (conceito e aplicação). Antes de enviar uma análise ao cliente, um executivo conferiu somas e percentuais e testou a conclusão em outros dois períodos. Falta alguma checagem de diligência de dados?

- (A) Não, a diligência está completa.
- (B) Sim, verificar se o período escolhido é o certo para a pergunta.
- (C) Sim, verificar se os dados respondem à pergunta do cliente.
- (D) Sim, verificar se há lacunas nos dados, como lojas, filiais ou semanas faltando.

**Gabarito: D.** A diligência de dados tem três checagens: conferir os cálculos, conferir a análise em diferentes períodos e verificar se há lacunas nos dados. Faltou a terceira. As opções B e C descrevem checagens de relevância (período certo e resposta à pergunta), importantes, mas pertencentes ao outro cuidado da precisão, a relevância.

**C1-E09** (conceito e aplicação). Qual das frases a seguir é um insight, e não apenas um ponto de dado?

- (A) “A frequência de compra da Marca X é 23% menor do que a do principal produto da categoria.”
- (B) “As vendas do distribuidor cresceram 8% no trimestre.”
- (C) “A maioria dos shoppers compra produtos para gripe só quando fica doente, porque quer alívio rápido do sintoma imediato e não pensa em como os sintomas vão progredir.”
- (D) “A Marca X tem fidelidade maior que a da marca própria do varejista e, portanto, maior frequência de compra.”

**Gabarito: C.** A frase revela a motivação do shopper (alívio rápido do sintoma imediato) e explica o comportamento (comprar só quando fica doente), conectando dados e contexto ao porquê. As opções A e B descrevem métricas isoladas, isto é, o quê. A opção D usa “portanto”, mas apenas relaciona duas métricas (fidelidade e frequência), sem explicar o comportamento ou a motivação do shopper: continua sendo o quê.

**C1-E10** (conceito e aplicação). Qual das aberturas a seguir aplica melhor as técnicas de engajamento da narrativa com dados?

- (A) “Você sabia que, apesar da mesma redução de 20% no preço, as vendas da Marca X crescem 12%, quatro vezes mais rápido que as da Marca Y?”
- (B) “A Marca X superou a Marca Y no 4º trimestre, mas 50% das suas lojas ainda estão perdendo essa oportunidade.”
- (C) “As promoções do 4º trimestre da Marca X geraram 12% a mais de vendas; expandir essa ativação pode maximizar o crescimento.”
- (D) “As vendas da Marca X foram fortes no 4º trimestre.”

**Gabarito: A.** A abertura captura a atenção imediatamente com uma pergunta (“Você sabia que…”), traz um fato surpreendente e mostra a diferença com uma comparação justa: mesmo desconto, resultado quatro vezes maior. A opção B aponta uma lacuna, mas sem fato surpreendente nem comparação justa; a opção C relata um resultado e sugere uma ação sem nenhum gancho de atenção; e a opção D é um exemplo do erro de ser vago.

## Capítulo 2 · Crescimento de categorias

Referência da skill: `02_crescimento_de_categorias.md`.

**C2-E01** (conceito e aplicação). Associe cada lançamento ao Shopper More mais impactado: (I) uma linha masculina de hidratante; (II) uma cerveja sem álcool; (III) cápsulas de café; (IV) uma pasta de dente vendida com enxaguante bucal.

- (A) I mais frequentemente; II mais shoppers; III comprar mais; IV gastar mais.
- (B) I mais shoppers; II mais frequentemente; III gastar mais; IV comprar mais.
- (C) I mais shoppers; II comprar mais; III gastar mais; IV mais frequentemente.
- (D) I gastar mais; II mais frequentemente; III comprar mais; IV mais shoppers.

**Gabarito: B.** A linha masculina de hidratante trouxe um público novo, os homens, para a categoria (mais shoppers). A cerveja sem álcool criou novas ocasiões de consumo (mais frequentemente). As cápsulas de café fazem o shopper pagar mais por dose (gastar mais). A pasta de dente vendida com enxaguante acrescenta itens à rotina de higiene bucal (comprar mais).

**C2-E02** (conceito e aplicação). Um comprador cita oito necessidades: marcas fortes, crescimento do negócio, conveniência, preço baixo todo dia, caixas menores, mínimo de burocracia, melhores prazos de crédito e maior percentual de margem. Qual associação está correta?

- (A) Estratégicas: marcas fortes, crescimento. Do shopper: conveniência, preço baixo todo dia. Operacionais: caixas menores, mínimo de burocracia. Financeiras: prazos de crédito, margem.
- (B) Estratégicas: crescimento, margem. Do shopper: marcas fortes, conveniência. Operacionais: caixas menores, prazos de crédito. Financeiras: preço baixo todo dia, mínimo de burocracia.
- (C) Estratégicas: marcas fortes, mínimo de burocracia. Do shopper: conveniência, caixas menores. Operacionais: preço baixo todo dia, prazos de crédito. Financeiras: crescimento, margem.
- (D) Estratégicas: conveniência, crescimento. Do shopper: preço baixo todo dia, marcas fortes. Operacionais: mínimo de burocracia, margem. Financeiras: caixas menores, prazos de crédito.

**Gabarito: A.** Cada grupo responde a uma pergunta: prioridades corporativas (marcas fortes, crescimento do negócio), o que o shopper-alvo procura (conveniência, preço baixo todo dia), como minimizar custos e simplificar (caixas menores, mínimo de burocracia) e metas financeiras (prazos de crédito, percentual de margem).

**C2-E03** (conceito e aplicação). Uma rede de farmácias quer aumentar a rentabilidade vendendo mais de um analgésico líder da empresa. Os shoppers, quando estão doentes, muitas vezes saem sem comprar porque não encontram o produto que querem, e a empresa quer impulsionar as vendas em saúde, onde há poucos shoppers. Qual é a oportunidade de vitória tripla?

- (A) Estimular os shoppers atuais a gastar mais (trade up).
- (B) Recrutar mais shoppers para a categoria.
- (C) Estimular os shoppers atuais a comprar com mais frequência.
- (D) Estimular os shoppers atuais a comprar mais.

**Gabarito: B.** Recrutar mais shoppers resolve a barreira do shopper, que sai sem comprar porque não encontra o produto; traz novos shoppers à categoria na loja do cliente; e atende ao objetivo da empresa de crescer em saúde, onde há poucos shoppers. As outras opções atuam só sobre quem já compra.

**C2-E04** (cálculo). A escolha da loja depende em cerca de 60% da performance do cliente e de 30% a 40% do tempo de deslocamento. Em qual fator o fornecedor pode ajudar o cliente diretamente?

- (A) Tempo de deslocamento, ajudando a loja a escolher um ponto mais próximo do shopper.
- (B) Performance do cliente, definindo o preço de gôndola da loja.
- (C) Tempo de deslocamento, porque responde por até 40% da escolha.
- (D) Performance do cliente, com sortimento e navegação.

**Gabarito: D.** O tempo de deslocamento pesa de 30% a 40% na escolha, mas o fornecedor não o muda; por isso A e C estão erradas. A performance do cliente é onde o fornecedor pode ajudar, com sortimento e navegação, além de conhecimento e informação, conveniência e valor e descontos. A opção B erra o meio: o preço de gôndola é decisão exclusiva do varejista, e o fabricante trabalha o preço líquido e pode apenas sugerir um preço ao consumidor.

**C2-E05** (conceito e aplicação). Qual dos indicadores abaixo é um KPI de entrada (leading)?

- (A) Receita de vendas.
- (B) Lucro.
- (C) Cobertura de lojas.
- (D) Crescimento de margem.

**Gabarito: C.** Cobertura é um KPI de entrada: uma atividade que o time de vendas influencia e que antecipa resultados, como distribuição e acurácia da previsão. Receita, lucro e crescimento de margem são KPIs de resultado.

**C2-E06** (conceito e aplicação). Posição na gôndola, número de frentes (facings) e fluxo de produto no layout da gôndola pertencem a qual alavanca de ativação?

- (A) Preço.
- (B) Promoções.
- (C) Exposição e visibilidade.
- (D) Sortimento e distribuição.

**Gabarito: C.** Posição na gôndola, frentes, comunicação, ponto de venda e fluxo de produto no layout de gôndola compõem a alavanca de exposição e visibilidade. Sortimento e distribuição tratam de listagem, distribuição e sortimento; preço, de preço líquido e de gôndola; promoções, de duração, mecânica, desconto, local e material promocional.

**C2-E07** (cálculo). Uma loja tem 1.500 compradores de uma categoria no mês; cada um compra 2,0 vezes, leva 1,5 unidade por compra e paga em média R$ 8,00 por unidade. Qual é a venda mensal e o que acontece se uma ação de troca para produtos de maior valor elevar o preço médio para R$ 8,80, mantido o resto?

- (A) R$ 24 mil; passa a R$ 26,4 mil, pelo Shopper More comprar mais.
- (B) R$ 36 mil; passa a R$ 39,6 mil, pelo Shopper More comprar mais.
- (C) R$ 36 mil; passa a R$ 39,6 mil, pelo Shopper More gastar mais.
- (D) R$ 18 mil; passa a R$ 19,8 mil, pelo Shopper More gastar mais.

**Gabarito: C.** Venda = 1.500 × 2,0 × 1,5 × R$ 8,00 = R$ 36 mil. Com preço médio de R$ 8,80: 1.500 × 2,0 × 1,5 × R$ 8,80 = R$ 39,6 mil, um ganho de 10% obtido pela troca para produtos de maior valor, ou seja, gastar mais. A opção A esquece o volume por compra, a D esquece a frequência e a B acerta a conta, mas erra a alavanca, porque o volume por compra não mudou.

**C2-E08** (cálculo). Num cliente, a categoria tinha no ano 1: 2.000 compradores, frequência 3,0, 1,5 unidade por compra e preço médio de R$ 20,00. No ano 2: 1.900 compradores, frequência 3,0, 1,2 unidade por compra e R$ 21,00. Qual foi a variação da venda e qual Shopper More priorizar?

- (A) Queda de 5,0%; mais shoppers.
- (B) Queda de 20,2%; gastar mais.
- (C) Alta de 5,0%; gastar mais.
- (D) Queda de 20,2%; comprar mais.

**Gabarito: D.** Ano 1: 2.000 × 3,0 × 1,5 × R$ 20,00 = R$ 180 mil. Ano 2: 1.900 × 3,0 × 1,2 × R$ 21,00 = R$ 143.640. Variação: 143.640 ÷ 180.000 = 0,798, queda de 20,2%. Compradores caíram 5%, a frequência ficou estável, o preço médio subiu 5% e o volume por compra caiu 20%, a maior queda; por isso a prioridade é comprar mais. Gastar mais (opção B) é justamente a alavanca que melhorou no período.

**C2-E09** (cálculo). Num estudo hipotético, a missão de reposição representava 30% das compras de uma categoria e, um ano depois, 24%. Qual é o índice da missão em relação ao ano anterior e como lê-lo?

- (A) 80; a missão perdeu um quinto do peso que tinha.
- (B) 125; a missão ganhou 25% de peso.
- (C) 6; a missão caiu 6%.
- (D) 120; a missão ganhou 20% de peso.

**Gabarito: A.** Índice = 24 ÷ 30 × 100 = 80. A missão passou a valer 80% do que valia, isto é, perdeu um quinto (20%) do seu peso relativo. A queda é de 6 pontos percentuais, o que não equivale a 6%.

**C2-E10** (cálculo). Num cliente, a categoria vende R$ 400 mil por mês, e a Marca Y, da empresa, tem 25% de participação. O caminho A ganha 3 pontos percentuais de participação sem fazer a categoria crescer; o caminho B faz a categoria crescer 12% com participação estável. Qual é o ganho mensal para a marca e para o cliente em cada caminho?

- (A) A: marca +R$ 12 mil, cliente +R$ 12 mil. B: marca +R$ 12 mil, cliente +R$ 48 mil.
- (B) A: marca +R$ 12 mil, cliente R$ 0. B: marca +R$ 12 mil, cliente +R$ 48 mil.
- (C) A: marca +R$ 3 mil, cliente R$ 0. B: marca +R$ 12 mil, cliente +R$ 12 mil.
- (D) A: marca +R$ 12 mil, cliente R$ 0. B: marca +R$ 48 mil, cliente +R$ 48 mil.

**Gabarito: B.** Caminho A: 28% × R$ 400 mil = R$ 112 mil, ganho de R$ 12 mil para a marca, mas a categoria continua em R$ 400 mil e o cliente não ganha nada. Caminho B: a categoria vai a R$ 400 mil × 1,12 = R$ 448 mil; a marca vende 25% × R$ 448 mil = R$ 112 mil (+R$ 12 mil) e o cliente ganha R$ 48 mil. O ganho da marca é o mesmo, mas só o caminho B interessa ao comprador.

## Capítulo 3 · Rigor financeiro

Referência da skill: `03_rigor_financeiro.md`.

**C3-E01** (conceito e aplicação). Um bom rigor financeiro entrega: (I) diligência com os dados; (II) acurácia para controle financeiro; (III) entendimento do P&L da empresa e do distribuidor; (IV) decisões mais bem informadas; (V) identificação de oportunidades financeiras para fabricante, distribuidores e varejistas; (VI) crescimento sustentável e lucrativo. Quais itens estão corretos?

- (A) Apenas I e II.
- (B) Apenas III, IV e V.
- (C) Apenas VI.
- (D) Todos, de I a VI.

**Gabarito: D.** Um bom rigor financeiro entrega todos os itens: diligência com os dados, acurácia para o controle financeiro, entendimento do P&L da empresa e do distribuidor, decisões mais bem informadas, identificação de oportunidades financeiras para todos os elos e crescimento sustentável e lucrativo. Eles se reforçam entre si e nenhum se sustenta sozinho.

**C3-E02** (conceito e aplicação). Qual é a ordem correta do P&L, da linha de cima para a de baixo?

- (A) Vendas brutas, margem bruta, receita líquida, contribuição do produto, lucro operacional.
- (B) Vendas brutas, receita líquida, margem bruta, contribuição do produto, lucro operacional.
- (C) Receita líquida, vendas brutas, margem bruta, lucro operacional, contribuição do produto.
- (D) Vendas brutas, receita líquida, contribuição do produto, margem bruta, lucro operacional.

**Gabarito: B.** Vendas brutas, receita líquida, margem bruta, contribuição do produto e lucro operacional da companhia. Cada degrau subtrai um bloco: descontos e verbas, COGS, investimento em propaganda e promoção (BEI e Non-BEI) e custos fixos.

**C3-E03** (conceito e aplicação). Em que linha do P&L aparecem, respectivamente, (1) o mix de produtos vendidos, (2) a escolha entre investimento fixo e investimento em percentual e (3) o quadro de pessoal?

- (A) (1) receita líquida; (2) margem bruta; (3) lucro operacional.
- (B) (1) margem bruta; (2) vendas brutas; (3) contribuição do produto.
- (C) (1) margem bruta; (2) receita líquida; (3) lucro operacional.
- (D) (1) contribuição do produto; (2) receita líquida; (3) vendas brutas.

**Gabarito: C.** O mix muda a margem bruta, porque produtos diferentes têm margens diferentes; a escolha entre investimento fixo e investimento em percentual é decisão de desconto e verba, e por isso mexe na receita líquida; o quadro de pessoal é estrutura e aparece no lucro operacional. O mapeamento completo do método: cobertura e preço de lista afetam as vendas brutas; investimento fixo ou em percentual e investimento total negociado afetam a receita líquida; mix e estoque obsoleto afetam a margem bruta; escala de marketing afeta a contribuição; quadro de pessoal e imóveis afetam o lucro operacional.

**C3-E04** (cálculo). Com receita líquida de R$ 1.000, COGS de R$ 400 e CFC de R$ 50, qual afirmação está correta?

- (A) +1% de receita líquida vale R$ 10,00, contra R$ 4,00 de 1% de economia em COGS e R$ 0,50 em CFC.
- (B) 1% de economia em COGS vale R$ 10,00.
- (C) Os três efeitos são iguais, pois todos valem 1%.
- (D) 1% de economia em CFC vale R$ 5,00.

**Gabarito: A.** 1% × R$ 1.000 = R$ 10,00; 1% × R$ 400 = R$ 4,00; 1% × R$ 50 = R$ 0,50. Como a receita líquida é a maior base, aumentar a receita líquida gera mais contribuição do que economias equivalentes em COGS ou CFC.

**C3-E05** (cálculo). Um item tem lucro bruto de R$ 50 e margem bruta de 33,3%. Quais são o preço, o custo e o markup?

- (A) Preço R$ 100; custo R$ 50; markup 100%.
- (B) Preço R$ 150; custo R$ 50; markup 33,3%.
- (C) Preço R$ 150; custo R$ 100; markup 50,0%.
- (D) Preço R$ 133,30; custo R$ 83,30; markup 60,0%.

**Gabarito: C.** P = GP ÷ GM% = R$ 50 ÷ 0,333 ≈ R$ 150; C = P − GP = R$ 100; markup = R$ 50 ÷ R$ 100 = 50,0%. A alternativa B confunde o custo com o lucro bruto e o markup com a margem.

**C3-E06** (cálculo). Vendas de 100, 110 e 130 e lucro bruto de 50, 60 e 65 em 2022, 2023 e 2024. Quais são as margens e a leitura correta?

- (A) 50,0%, 54,5% e 50,0%; a margem está saudável porque voltou ao nível inicial.
- (B) 50,0%, 54,5% e 50,0%; vendas e lucro bruto crescem, mas a margem % preocupa, porque em 2024 as vendas cresceram mais rápido que o lucro bruto.
- (C) 50,0%, 60,0% e 65,0%; a margem melhora todo ano.
- (D) 50,0%, 54,5% e 54,5%; a margem se estabilizou.

**Gabarito: B.** 50 ÷ 100 = 50,0%; 60 ÷ 110 = 54,5%; 65 ÷ 130 = 50,0%. Vendas e lucro bruto crescem, mas a margem bruta % é uma preocupação: em 2024 as vendas cresceram cerca de 18% e o lucro bruto, cerca de 8%, diluindo a margem.

**C3-E07** (conceito e aplicação). Pela classificação do método, qual lista contém apenas custos fixos de servir?

- (A) Armazenagem, tecnologia (dispositivos SFA) e suporte de atendimento ao cliente.
- (B) Salários dos vendedores, custos de veículos e armazenagem.
- (C) Combustível, merchandising e material de PDV.
- (D) Tecnologia, salários dos vendedores e investimento comercial e crédito.

**Gabarito: A.** Pela classificação do método, os custos fixos de servir são armazenagem, tecnologia (dispositivos de automação da força de vendas, SFA) e suporte de atendimento ao cliente. Salários dos vendedores, custos de veículos, material de PDV, combustível, merchandising e investimento comercial e crédito são variáveis, porque crescem com o número de pontos, rotas e visitas.

**C3-E08** (cálculo). Um varejista recebe 10% em nota, 3% de rebate, 2% de incentivo de MSL, 2,5% de pagamento por desempenho e 1,5% de incentivo logístico. Quais são a margem front e a margem total?

- (A) Front 19%; total 19%.
- (B) Front 13%; total 19%.
- (C) Front 10%; total 10%, pois a margem back não entra na conta.
- (D) Front 10%; total 19%.

**Gabarito: D.** A margem front é o desconto em nota (10%). Rebate, incentivo de MSL, pagamento por desempenho e incentivo logístico são margem back. Margem total = 10% + 3% + 2% + 2,5% + 1,5% = 19%.

**C3-E09** (cálculo). Um distribuidor tem receita bruta de R$ 2 milhões (R$ 1,7 milhão de margem front e R$ 300 mil de margem back), despesas de R$ 1 milhão e investimento de R$ 520 mil (estoque, crédito ao mercado, reembolsos e outros), com R$ 120 mil de crédito concedido pelo fabricante. Qual é o ROI?

- (A) Cerca de 192%, usando o investimento antes do crédito do fabricante.
- (B) 500%, dividindo a receita bruta pelo investimento.
- (C) 250%, dividindo o lucro líquido de R$ 1 milhão pelo investimento de R$ 400 mil.
- (D) 100%, dividindo o lucro líquido pelas despesas.

**Gabarito: C.** Lucro líquido = R$ 2 milhões − R$ 1 milhão = R$ 1 milhão. Investimento bruto total = R$ 520 mil − R$ 120 mil = R$ 400 mil. ROI = R$ 1.000.000 ÷ R$ 400.000 = 2,5 = 250%. A alternativa A esquece de descontar o crédito concedido pelo fabricante.

**C3-E10** (cálculo). Um distribuidor pede 5% de redução no preço de um desinfetante (R$ 135,50 para R$ 128,70 por caixa; base de 100.000 caixas). Que aumento de unidades garante crescimento das vendas em valor?

- (A) 5%, porque o volume compensa exatamente o desconto.
- (B) 10%, que leva as vendas a R$ 14.157.000.
- (C) 3%, porque o desconto incide só sobre o volume adicional.
- (D) Nenhum aumento de volume compensa um desconto.

**Gabarito: B.** Com +5% (105.000 caixas × R$ 128,70) as vendas ficam em R$ 13.513.500, queda de R$ 36.500. Com +10% (110.000 × R$ 128,70) chegam a R$ 14.157.000, ganho de R$ 607.000. O volume de equilíbrio em valor é 1 ÷ (1 − 0,05) − 1 ≈ 5,3%, e o equilíbrio em margem exige ainda mais.

## Capítulo 4 · Venda persuasiva

Referência da skill: `04_venda_persuasiva.md`.

**C4-E01** (conceito e aplicação). Em qual das situações abaixo a venda persuasiva não se aplica?

- (A) Acordar o plano de negócios conjunto (JBP) com o distribuidor.
- (B) Conseguir espaço adicional de gôndola nas lojas de um varejista.
- (C) Preparar a sua reunião semanal de vendas.
- (D) Listar um novo produto em um varejista.

**Gabarito: C.** Preparar a própria reunião semanal de vendas é trabalho de organização e não envolve influenciar ninguém a fazer algo que beneficie essa pessoa e você. Acordar o JBP com o distribuidor, conseguir espaço adicional de gôndola e listar um novo produto são usos típicos da venda persuasiva, assim como obter verba promocional incremental com o time de finanças.

**C4-E02** (cálculo). Quais destes objetivos são SMART? I. Conseguir um display de balcão em 50% das lojas da sua área de cobertura até o fim do 3º trimestre. II. Tentar conseguir mais espaço na loja. III. Conseguir acordo para uma promoção de 25% no Produto Y no distribuidor X no próximo mês. IV. Discutir o potencial de novas listagens em breve. V. Listar 2 novos produtos da categoria de higiene no varejista X até 30 de junho. VI. Melhorar nossa presença na gôndola.

- (A) I, II e V.
- (B) I, III e V.
- (C) III, IV e VI.
- (D) II, IV e VI.

**Gabarito: B.** I, III e V têm resultado específico, número e prazo. II (“tentar conseguir mais espaço”), IV (“discutir… em breve”) e VI (“melhorar a presença”) não têm número, prazo ou ambos.

**C4-E03** (cálculo). Sua área tem 84 lojas, e o objetivo é ter um display de balcão em 50% delas até o fim do 3º trimestre. Hoje, 19 lojas já têm o display, e restam 6 checagens quinzenais. Quantas lojas faltam conquistar e qual é o ritmo mínimo por quinzena?

- (A) 23 lojas, 4 por quinzena.
- (B) 42 lojas, 7 por quinzena.
- (C) 61 lojas, cerca de 10 por quinzena.
- (D) 19 lojas, cerca de 3 por quinzena.

**Gabarito: A.** 84 × 50% = 42 lojas com display; 42 − 19 = 23 lojas a conquistar; 23 ÷ 6 ≈ 3,8. Como não se conquista fração de loja, o ritmo mínimo é de 4 lojas por quinzena (4 × 6 = 24 cobre as 23; 3 × 6 = 18 não basta). A alternativa B ignora as 19 lojas já conquistadas, a C soma em vez de subtrair e a D confunde as lojas que já têm display com as que faltam.

**C4-E04** (conceito e aplicação). Um atacadista tem vendas em queda, e a sua proposta é uma nova linha de limpeza ecológica. Associe cada ação ao passo do C.L.E.A.N.: (1) explicar os detalhes do lançamento e o suporte disponível; (2) pedir a aprovação e confirmar os próximos passos; (3) explorar por que as vendas estão caindo; (4) lembrar como a linha aumentaria o fluxo e estimularia a migração para itens de maior valor ( trade up ); (5) apresentar a nova linha como solução.

- (A) (1) Oportunidade principal; (2) E agora?; (3) Situação atual; (4) Executar com perfeição; (5) Benefícios incríveis.
- (B) (1) Executar com perfeição; (2) Benefícios incríveis; (3) Situação atual; (4) E agora?; (5) Oportunidade principal.
- (C) (1) Benefícios incríveis; (2) E agora?; (3) Oportunidade principal; (4) Executar com perfeição; (5) Situação atual.
- (D) (1) Executar com perfeição; (2) E agora?; (3) Situação atual; (4) Benefícios incríveis; (5) Oportunidade principal.

**Gabarito: D.** (1) Executar com perfeição; (2) E agora?; (3) Situação atual; (4) Benefícios incríveis; (5) Oportunidade principal. A conversa segue a sequência: entender o cliente, apresentar a recomendação e fechar o negócio.

**C4-E05** (conceito e aplicação). Penetração, peso médio de compra (AWOP) e frequência de compra pertencem a qual dos 7Cs?

- (A) Canal.
- (B) Consumidor.
- (C) Categoria.
- (D) Cliente.

**Gabarito: B.** O C de consumidor reúne tendências, comportamentos, penetração, peso médio de compra (AWOP) e frequência de compra. Canal trata de definição, shoppers, missões e escala; categoria, de segmentos, dinâmica, métricas, oportunidades e motores de crescimento; cliente, de tamanho, importância, estratégia, desempenho, investimento e promoções.

**C4-E06** (conceito e aplicação). Sua proposta inclui embalagem com preço impresso e reorganização do fluxo de produto na gôndola. Pela classificação das quatro alavancas, esses elementos pertencem, respectivamente, a:

- (A) Promoções; exposição e visibilidade.
- (B) Preço; exposição e visibilidade.
- (C) Preço; sortimento e distribuição.
- (D) Promoções; sortimento e distribuição.

**Gabarito: A.** A embalagem com preço impresso ( price marked pack ) é mecânica promocional e pertence a promoções; o fluxo de produto, com o layout de gôndola, pertence a exposição e visibilidade. A alavanca de preço fica apenas com o preço líquido e o preço de gôndola.

**C4-E07** (cálculo). Uma rede de 30 lojas avalia listar um novo item premium de cuidados com a roupa. Você estima uma venda incremental de 150 unidades por loja por mês, a um preço de gôndola de R$ 18. Que valor anual de vendas incrementais deve aparecer na oportunidade principal?

- (A) R$ 81 mil.
- (B) R$ 486 mil.
- (C) R$ 972 mil.
- (D) R$ 9,72 milhões.

**Gabarito: C.** 30 lojas × 150 unidades = 4.500 unidades por mês; 4.500 × R$ 18 = R$ 81 mil por mês; R$ 81 mil × 12 = R$ 972 mil por ano. A alternativa A é o valor de um único mês, a B corresponde a seis meses e a D tem um erro de casa decimal. Uma manchete possível: “Listar o novo item premium nas 30 lojas acrescenta R$ 972 mil de vendas incrementais por ano à rede.”

**C4-E08** (conceito e aplicação). Qual alternativa contém apenas benefícios para o cliente?

- (A) Embalagem pronta para gôndola, caixa menor e aumento de margem.
- (B) Oferta de lançamento, sabor morango e aumento do gasto na cesta.
- (C) Aumento das vendas da categoria, caixa menor e oferta de lançamento.
- (D) Aumento das vendas da categoria, aumento do gasto na cesta, aumento de margem e menos tempo para repor a gôndola.

**Gabarito: D.** Aumento das vendas da categoria, aumento do gasto na cesta, aumento de margem e menos tempo para repor a gôndola são resultados para o cliente. Embalagem pronta para gôndola, caixa menor, oferta de lançamento e sabor morango são características, que podem gerar benefícios, mas não são benefícios em si.

**C4-E09** (conceito e aplicação). Associe cada frase ao tipo de fechamento: (1) “Vou providenciar a entrega.” (2) “Quando você precisa das amostras dos novos produtos?” (3) “Já combinamos como os produtos serão expostos; quando volto para ajudar?” (4) “Prefere a entrega nesta semana ou na próxima?” (5) “Se está de acordo com o que conversamos, fechamos o pedido agora?”

- (A) (1) Experimental; (2) Próximo passo; (3) Ponto menor; (4) Alternativo; (5) Assumido.
- (B) (1) Assumido; (2) Ponto menor; (3) Próximo passo; (4) Alternativo; (5) Experimental.
- (C) (1) Assumido; (2) Alternativo; (3) Próximo passo; (4) Ponto menor; (5) Experimental.
- (D) (1) Próximo passo; (2) Ponto menor; (3) Assumido; (4) Alternativo; (5) Experimental.

**Gabarito: B.** (1) Assumido, porque avança sem abrir espaço para contestação; (2) ponto menor, porque decide um detalhe secundário; (3) próximo passo, porque propõe começar a execução; (4) alternativo, porque oferece duas opções, ambas positivas; (5) experimental, porque testa os sinais de compra.

**C4-E10** (conceito e aplicação). Quando é apropriado passar da venda para a negociação?

- (A) Quando o comprador interrompe no meio da proposta e diz não.
- (B) Quando o comprador não parece entender o valor da proposta.
- (C) Quando você terminou de vender e o comprador está interessado, mas sem acordo, ou quando ele está engajado, mas tem outros pedidos.
- (D) Quando você sente que precisa fazer a conversa andar.

**Gabarito: C.** Só se negocia depois de completar a venda: quando o comprador está interessado, mas ainda não há acordo, ou quando está engajado, mas tem outros pedidos. Nas alternativas A e B ainda é hora de vender (o comprador cortou a proposta ou não entendeu o valor), e a sensação de que é preciso fazer a conversa andar (D) não justifica concessões. Vender é sempre mais custo-efetivo do que negociar.

## Capítulo 5 · Negociação

Referência da skill: `05_negociacao.md`.

**C5-E01** (conceito e aplicação). Associe cada sinal ao estilo que ele indica: muitos itens a negociar; confiança crítica; forte interdependência; foco no preço; poucos itens; cliente com muitas opções.

- (A) Competitiva: muitos itens, confiança crítica, foco no preço. Colaborativa: poucos itens, forte interdependência, cliente com muitas opções.
- (B) Competitiva: foco no preço, poucos itens, cliente com muitas opções. Colaborativa: muitos itens, confiança crítica, forte interdependência.
- (C) Competitiva: foco no preço, forte interdependência, poucos itens. Colaborativa: muitos itens, confiança crítica, cliente com muitas opções.
- (D) Todas indicam negociação colaborativa, porque qualquer cliente pode se tornar parceiro.

**Gabarito: B.** Foco no preço, poucos itens a negociar e cliente com muitas opções indicam baixa complexidade e baixa dependência, portanto negociação competitiva. Muitos itens a negociar, confiança crítica e forte interdependência indicam alta complexidade e alta dependência, portanto negociação colaborativa. A alternativa C troca “forte interdependência” e “cliente com muitas opções” de lado, e a D ignora que defender é o caminho quando a colaboração não é possível.

**C5-E02** (conceito e aplicação). Um atacadista quer comprar um analgésico à base de ibuprofeno. Ele não comprou nada de você no último ano, trabalha de forma transacional, não se preocupa muito com marcas e foca principalmente em preço. Qual é a abordagem indicada?

- (A) Colaborativa: oferecer apoio promocional de trade para construir a relação.
- (B) Nenhuma: com cliente transacional não se negocia.
- (C) Colaborativa: montar o Esboço com todas as variáveis disponíveis e arrumar a mesa.
- (D) Competitiva: aplicar os três primeiros passos (meta, abertura e movimentos) e defender preço e margem.

**Gabarito: D.** Sem histórico recente, com relação transacional, pouca atenção às marcas e foco em preço, os dois eixos da matriz estão baixos: a negociação é competitiva. Aplicam-se os passos de meta, abertura e movimentos, com poucas variáveis, defendendo preço e margem. Oferecer apoio promocional (A) ou montar um Esboço amplo (C) seria entregar valor a quem não o reconhece; e com um cliente transacional se negocia, sim, só que no estilo competitivo.

**C5-E03** (cálculo). No caso do álcool em gel, o comprador normalmente paga R$ 80 por 10 caixas e pode pagar no máximo R$ 90; o vendedor normalmente cobra R$ 80 e não pode baixar de R$ 70. No papel de vendedor, onde ficam a ZOPA, o seu menor preço aceitável e a sua abertura?

- (A) ZOPA de R$ 80 a R$ 90; menor preço R$ 80; abertura R$ 90.
- (B) ZOPA de R$ 70 a R$ 90; menor preço R$ 70; abertura R$ 85.
- (C) ZOPA de R$ 70 a R$ 90; menor preço R$ 70; abertura R$ 100.
- (D) ZOPA de R$ 60 a R$ 100; menor preço R$ 60; abertura R$ 125.

**Gabarito: C.** A ZOPA vai do ponto de ruptura do vendedor (R$ 70) ao do comprador (R$ 90). O menor preço aceitável é o próprio ponto de ruptura, R$ 70, e a abertura fica fora da ZOPA, mas dentro do razoável: R$ 100. A alternativa B abre dentro da ZOPA, sem espaço para concessões; a D trata as duas aberturas (R$ 60 e R$ 100) como se fossem a ZOPA e propõe abrir em R$ 125, fora do razoável.

**C5-E04** (cálculo). Um vendedor tem ponto de ruptura de R$ 50 por caixa e estima que o comprador pague no máximo R$ 62. O acordo fecha em R$ 58. Qual é a amplitude da ZOPA e que percentual dela o vendedor capturou?

- (A) R$ 12; 33,3%.
- (B) R$ 8; 66,7%.
- (C) R$ 62; 93,5%.
- (D) R$ 12; 66,7%.

**Gabarito: D.** Amplitude = R$ 62 − R$ 50 = R$ 12. Percentual capturado = (R$ 58 − R$ 50) ÷ R$ 12 = R$ 8 ÷ R$ 12 ≈ 66,7%. A alternativa A dá a parte do comprador (R$ 4 ÷ R$ 12 ≈ 33,3%); a B confunde o ganho do vendedor com a amplitude; a C divide o preço do acordo pelo máximo do comprador (R$ 58 ÷ R$ 62).

**C5-E05** (conceito e aplicação). Responda, na ordem: (1) o que significa ZOPA; (2) a meta fica perto de qual ponto de ruptura; (3) a abertura fica dentro ou fora da ZOPA; (4) os movimentos são planejados antes ou depois de a negociação começar; (5) eles ficam menores ou maiores?

- (A) Zona de Possível Acordo; do seu; dentro; antes; menores.
- (B) Zona de Possível Acordo; do comprador; fora; antes; menores.
- (C) Zona de Preço Aceitável; do comprador; fora; depois; maiores.
- (D) Zona de Possível Acordo; do comprador; dentro; depois; menores.

**Gabarito: B.** ZOPA é a Zona de Possível Acordo; a meta fica perto do ponto de ruptura do comprador (o outro lado); a abertura fica fora da ZOPA; os movimentos são planejados antes de a negociação começar e ficam menores ao longo dela.

**C5-E06** (cálculo). A política comercial permite dar no máximo 5% de desconto adicional a um distribuidor que compra R$ 400 mil por trimestre. Qual escada de concessões respeita a regra dos movimentos e quanto ela custa, no máximo, por trimestre?

- (A) 1%, 2% e 2%; R$ 20 mil.
- (B) 3%, 1,5% e 0,5%; R$ 12 mil.
- (C) 3%, 1,5% e 0,5%; R$ 20 mil.
- (D) 2,5% e 2,5%; R$ 20 mil.

**Gabarito: C.** A escada 3%, 1,5% e 0,5% é decrescente e soma exatamente o limite de 5%. Custo máximo = 5% × R$ 400 mil = R$ 20 mil por trimestre (R$ 12 mil + R$ 6 mil + R$ 2 mil). A alternativa B considera apenas o primeiro degrau; a A tem degraus crescentes; a D repete degraus grandes e não sinaliza a aproximação do limite.

**C5-E07** (conceito e aplicação). Classifique as variáveis do Esboço do xarope para tosse: preço, distribuição, altura dos olhos, prazo de pagamento, investimento em promoção, incentivo para avarias e prazo de entrega.

- (A) Contrapartidas: distribuição e altura dos olhos. Moedas de troca: prazo de entrega, avarias, promoção e prazo de pagamento. Preço: preço.
- (B) Contrapartidas: distribuição e prazo de entrega. Moedas de troca: avarias, promoção e altura dos olhos. Preço: preço e prazo de pagamento.
- (C) Contrapartidas: prazo de pagamento e promoção. Moedas de troca: distribuição, altura dos olhos, prazo de entrega e avarias. Preço: preço.
- (D) Contrapartidas: distribuição, altura dos olhos e prazo de entrega. Moedas de troca: avarias, prazo de pagamento e preço. Preço: promoção.

**Gabarito: A.** Preço é a única variável de custo e valor iguais. Distribuição e merchandising na altura dos olhos são contrapartidas: valem muito para o fabricante e custam pouco ao atacadista. Prazo do pedido à entrega, incentivo para avarias, investimento em promoção de trade e prazo de pagamento são moedas de troca: valem muito para o atacadista e custam relativamente pouco ao fabricante (o prazo de pagamento, com a ressalva de que tem custo financeiro e mexe no capital de giro).

**C5-E08** (cálculo). Complete a troca condicional: “Se você pagar o preço de R$ 4,85…”

- (A) “…então eu reduzo o preço para R$ 4,35.”
- (B) “…então eu peço distribuição em 120 lojas.”
- (C) “…então eu lhe ofereço um prazo de entrega (lead time) melhor.”
- (D) “…então eu vejo o que consigo fazer depois.”

**Gabarito: C.** “…então eu lhe ofereço um prazo de entrega (lead time) melhor.” A frase começa pelo que o fabricante quer (o preço cheio de R$ 4,85) e oferece em troca uma moeda de troca. A alternativa A concede preço, a B pede em vez de oferecer e a D faz uma promessa vaga, sem conteúdo de troca.

**C5-E09** (conceito e aplicação). Qual foi o acordo final registrado no Quadro de negociação do lançamento com o atacadista?

- (A) Prazo de 30 dias; 4 SKUs; altura dos olhos; R$ 100 mil de investimento; R$ 4,50; 100 lojas; entrega em 7 dias.
- (B) Prazo de 25 dias; 4 SKUs; altura dos olhos; R$ 80 mil de investimento; R$ 4,80; 120 lojas; entrega em 10 dias.
- (C) Prazo de 15 dias; 3 SKUs; sem altura dos olhos; R$ 90 mil de investimento; R$ 4,70; 50 lojas; entrega em 7 dias.
- (D) Prazo de 25 dias; 3 SKUs; altura dos olhos; R$ 90 mil de investimento; R$ 4,70; 120 lojas; entrega em 7 dias.

**Gabarito: D.** Prazo de pagamento de 25 dias, 3 SKUs, exposição na altura dos olhos, investimento de lançamento de R$ 90 mil, preço de R$ 4,70, distribuição em 120 lojas e prazo do pedido à entrega de 7 dias. Cada variável fechou quando os dois lados convergiram, e o preço foi a última a fechar.

**C5-E10** (cálculo). No mesmo Quadro, o fabricante foi de R$ 4,85 para R$ 4,80 e R$ 4,70, e o atacadista, de R$ 4,35 para R$ 4,50 e R$ 4,70. Qual leitura está correta?

- (A) As concessões individuais cresceram (R$ 0,05 e R$ 0,10; R$ 0,15 e R$ 0,20), enquanto a distância caiu de R$ 0,50 para R$ 0,30 e para zero; o fabricante cedeu R$ 0,15, ou 30% da distância inicial.
- (B) As concessões de cada lado diminuíram a cada rodada (R$ 0,10 e R$ 0,05; R$ 0,20 e R$ 0,15), como manda a regra dos movimentos decrescentes; o fabricante cedeu R$ 0,15, ou 30% da distância inicial.
- (C) As concessões individuais cresceram, e a distância caiu de R$ 0,50 para R$ 0,30 e para zero; o fabricante cedeu R$ 0,35 (R$ 0,15 e R$ 0,20), ou 70% da distância inicial, e o atacadista, R$ 0,15.
- (D) Cada lado concedeu R$ 0,25 (R$ 0,10 e R$ 0,15), a distância caiu de R$ 0,50 para R$ 0,30 e para zero, e o acordo ficou exatamente no meio da distância inicial, com 50% para cada lado.

**Gabarito: A.** O fabricante concedeu R$ 0,05 e depois R$ 0,10 (total de R$ 0,15); o atacadista, R$ 0,15 e depois R$ 0,20 (total de R$ 0,35). As concessões individuais cresceram, enquanto a distância entre os lados caiu de R$ 0,50 para R$ 0,30 e para zero. O fabricante cedeu R$ 0,15 ÷ R$ 0,50 = 30% da distância inicial. A alternativa B inverte a ordem dos degraus e atribui ao Quadro uma regra que ele não ilustra: quem mostra os movimentos decrescentes é a escada do álcool em gel, e este caso se afasta dela. A C inverte os lados, e a D divide a distância ao meio e ignora que o acordo em R$ 4,70 ficou mais perto da abertura do fabricante.

## Capítulo 6 · O método integrado

Referência da skill: `SKILL.md (fluxo de dez passos) e todas as referências`.

**C6-E01** (cálculo). Um distribuidor liga pedindo 4% de desconto em nota “porque as vendas caíram”. Pelo fluxo de dez passos, qual deve ser a primeira providência?

- (A) Calcular o volume de equilíbrio do desconto e responder no mesmo dia.
- (B) Enquadrar a pergunta e checar os dados da queda antes de discutir qualquer concessão.
- (C) Abrir a negociação no extremo, oferecendo 0% de desconto.
- (D) Montar o roteiro C.L.E.A.N. com uma proposta de crescimento.

**Gabarito: B.** O pedido vem justificado por uma queda de vendas e chega antes de qualquer análise; nesse caso, o fluxo começa por enquadrar a pergunta e checar os dados (passos 1 e 2): é preciso saber se a queda existe, de que tamanho e por quê antes de discutir concessões. A opção A antecipa o passo 5 e responde sem diagnóstico; a C salta para a negociação (passo 9) sem venda completa; a D monta a venda (passo 7) sem diagnóstico nem oportunidade quantificada.

**C6-E02** (cálculo). Um relatório mostra vendas de R$ 1,52 milhão no trimestre, contra R$ 1,80 milhão no mesmo trimestre do ano anterior. Na checagem, você descobre que faltam três semanas de uma filial que vende R$ 40 mil por semana. Qual é a variação real?

- (A) −15,6%
- (B) −11,1%
- (C) −8,9%
- (D) −6,7%

**Gabarito: C.** Vendas corrigidas = R$ 1,52 milhão + 3 × R$ 40 mil = R$ 1,64 milhão. Variação = R$ 1,64 milhão ÷ R$ 1,80 milhão − 1 = −8,9%. A opção A é a variação do relatório com a lacuna (R$ 1,52 milhão ÷ R$ 1,80 milhão − 1); a B soma apenas duas semanas (R$ 1,60 milhão); a D soma quatro semanas (R$ 1,68 milhão).

**C6-E03** (cálculo). As vendas de um distribuidor caíram 6% no trimestre. O painel de varejo mostra a categoria caindo 5% na região, e os outros distribuidores da região caíram 7%. Não houve ruptura relevante nem mudança no calendário promocional. Qual é a leitura mais correta?

- (A) Problema de execução no distribuidor: plano de recuperação de distribuição.
- (B) Efeito de base promocional: reavaliar o calendário de promoções.
- (C) A queda acompanha o mercado: ajustar a previsão e buscar com o cliente alavancas de crescimento da categoria.
- (D) Conceder desconto para recuperar o volume perdido.

**Gabarito: C.** A categoria caiu 5% e os outros distribuidores, 7%: a queda de 6% acompanha o mercado. Sem ruptura nem mudança promocional, a resposta é ajustar a previsão e buscar com o cliente alavancas de crescimento da categoria, como os Shopper Mores. As opções A e B contrariam os dados, e a D trata uma queda de mercado com preço, sem contrapartida.

**C6-E04** (cálculo). As lacunas de MSL de um distribuidor com 900 clientes somam R$ 250 mil de potencial por trimestre. Os 200 maiores clientes concentram R$ 200 mil e têm, em média, 2,5 itens faltando cada um. Qual é o potencial médio por item faltante nesse grupo e que parcela do potencial total ele representa?

- (A) R$ 400 por item; 80% do potencial, com 22,2% dos clientes.
- (B) R$ 1.000 por item; 80% do potencial, com 22,2% dos clientes.
- (C) R$ 400 por item; 22,2% do potencial.
- (D) R$ 277,80 por item; 80% do potencial.

**Gabarito: A.** Itens faltantes no grupo = 200 × 2,5 = 500. Potencial por item = R$ 200.000 ÷ 500 = R$ 400. Parcela do potencial = R$ 200 mil ÷ R$ 250 mil = 80%, com 200 ÷ 900 = 22,2% dos clientes, um caso típico da lógica 80/20. A opção B divide o potencial pelo número de clientes (R$ 200.000 ÷ 200); a C troca a parcela de potencial pela parcela de clientes; a D divide o potencial total pelo total de clientes (R$ 250.000 ÷ 900).

**C6-E05** (cálculo). Lucro líquido do distribuidor na sua linha no trimestre: R$ 120 mil. Estoque médio: R$ 450 mil; crédito médio ao mercado: R$ 380 mil; reembolsos a receber: R$ 50 mil; outros investimentos: R$ 70 mil; crédito concedido pelo fabricante: R$ 350 mil. Qual é o ROI no trimestre?

- (A) 9,2%
- (B) 12,6%
- (C) 20,0%
- (D) 34,3%

**Gabarito: C.** Investimento bruto total = R$ 450 mil + R$ 380 mil + R$ 50 mil + R$ 70 mil − R$ 350 mil = R$ 600 mil. ROI = R$ 120 mil ÷ R$ 600 mil = 20,0% no trimestre. A opção A soma o crédito do fabricante em vez de subtraí-lo (R$ 1,3 milhão); a B ignora esse crédito (R$ 950 mil); a D divide o lucro apenas pelo crédito do fabricante (R$ 350 mil).

**C6-E06** (cálculo). A margem bruta do fabricante é de 40% do preço, e o distribuidor pede 4% de desconto em nota. Quanto o volume precisa crescer para manter a margem bruta em reais?

- (A) 4,0%
- (B) 4,2%
- (C) 10,0%
- (D) 11,1%

**Gabarito: D.** Com margem bruta de 40%, um desconto de 4% reduz a margem por unidade para 36% do preço original. Volume de equilíbrio em margem = 40% ÷ 36% − 1 = 11,1%. A opção B (4,2%) é o equilíbrio em valor, 1 ÷ (1 − 0,04) − 1, que não preserva a margem; a A supõe que 4% de volume paga 4% de desconto; a C divide o desconto pela margem (4% ÷ 40%) e esquece que o volume adicional também é vendido com desconto.

**C6-E07** (cálculo). O teto de verba condicionada aprovado pelo fabricante é de R$ 60 mil por trimestre, e você estima que o cliente aceitaria, no mínimo, R$ 35 mil. Qual combinação de meta e abertura segue o método?

- (A) Meta de R$ 58 mil e abertura de R$ 40 mil.
- (B) Meta de R$ 38 mil e abertura de R$ 20 mil.
- (C) Meta de R$ 38 mil e abertura de R$ 45 mil.
- (D) Meta de R$ 35 mil e abertura de R$ 60 mil.

**Gabarito: B.** A ZOPA vai de R$ 35 mil, o mínimo do cliente, a R$ 60 mil, o teto do fabricante. A meta fica perto do ponto de ruptura do cliente (R$ 38 mil) e a abertura fica fora da ZOPA, dentro do razoável (R$ 20 mil). A opção A põe a meta perto do próprio teto e abre dentro da ZOPA; a C abre dentro da ZOPA e acima da própria meta; a D abre no próprio teto, entregando todo o valor logo na primeira proposta. Se o acordo sair, por exemplo, em R$ 40 mil, o fabricante terá ficado com (R$ 60 mil − R$ 40 mil) ÷ (R$ 60 mil − R$ 35 mil) = 80% da ZOPA.

**C6-E08** (cálculo). Na medição de um encarte, a linha de base era de 8.000 unidades e a ação vendeu 20.000. O lucro bruto regular é de R$ 2,00 por unidade, o desconto foi de R$ 0,75 por unidade e os custos da ação somaram R$ 6.000. Qual foi o ROI líquido pós-evento?

- (A) 50%
- (B) 150%
- (C) 300%
- (D) 316,7%

**Gabarito: A.** Lucro bruto da promoção por unidade = R$ 2,00 − R$ 0,75 = R$ 1,25. Lucro bruto na promoção = 20.000 × R$ 1,25 = R$ 25.000. Lucro bruto da linha de base = 8.000 × R$ 2,00 = R$ 16.000. Lucro bruto incremental = R$ 9.000. ROI líquido = (R$ 9.000 − R$ 6.000) ÷ R$ 6.000 = 50%. A opção B é o ROI bruto (R$ 9.000 ÷ R$ 6.000 = 1,5) escrito como 150%; a C valoriza as 12.000 unidades incrementais pelo lucro regular e ignora o desconto, (R$ 24.000 − R$ 6.000) ÷ R$ 6.000; a D usa o lucro bruto total da promoção, (R$ 25.000 − R$ 6.000) ÷ R$ 6.000.

**C6-E09** (conceito e aplicação). Depois de ouvir a proposta, o diretor de um distribuidor diz: “Não tenho capital para carregar mais estoque.” O executivo tinha antecipado essa objeção. Pelo A.R.I.O., qual deve ser a próxima fala dele?

- (A) “Se você aceitar o estoque, então eu dou 2% de desconto em nota.”
- (B) “Sem o estoque o plano não funciona, então vamos precisar dele.”
- (C) “Tudo bem, tiramos o estoque de segurança do plano e seguimos com o resto.”
- (D) “Entendo totalmente o desafio de carregar estoque com o capital caro. Fora o capital, há mais alguma coisa que impeça você de seguir com o plano?”

**Gabarito: D.** A objeção é do tipo “há uma parte que não consigo entregar”, e o A.R.I.O. pede, depois de antecipá-la, que o executivo primeiro se relacione com ela (“entendo totalmente o desafio de…”) e depois a isole (“fora isso, há mais alguma coisa que impeça…?”), para trazer todas as barreiras à mesa antes de superá-las com o dado preparado. A opção A trata uma objeção como se fosse um “não, eu preciso de…” e concede preço antes de terminar a venda; a B insiste sem reconhecer o que o cliente disse e sem oferecer solução; a C abandona a parte do plano que resolve a causa principal da queda, sem superar a objeção.

**C6-E10** (conceito e aplicação). Qual destes objetivos para a reunião com o diretor de um distribuidor passa nos testes SMART?

- (A) “Convencer o diretor a apoiar o plano de crescimento da linha.”
- (B) “Aumentar a distribuição da linha o máximo possível nos próximos meses.”
- (C) “Obter do diretor, na reunião de quinta-feira, o aceite para completar o MSL de oito itens nos 250 maiores clientes até o fim do trimestre, com acompanhamento quinzenal.”
- (D) “Discutir com o diretor a possibilidade de rever o sortimento em breve.”

**Gabarito: C.** O objetivo diz o que se quer obter e de quem (específico), traz números verificáveis, oito itens e 250 clientes (mensurável), é um passo ambicioso e alcançável, liga-se diretamente ao plano de crescimento (relevante) e tem prazo para o aceite e para a execução, além do acompanhamento quinzenal. A opção A é a primeira versão do objetivo de Luísa, sem número nem prazo; a B não tem critério de sucesso (“o máximo possível”) nem prazo definido; a D descreve uma conversa em vez de um resultado, e “em breve” não fixa data nenhuma.

## Tabela de gabaritos

| Capítulo | E01 | E02 | E03 | E04 | E05 | E06 | E07 | E08 | E09 | E10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1. Leitura de dados | C | A | C | B | A | D | B | D | C | A |
| 2. Crescimento de categorias | B | A | B | D | C | C | C | D | A | B |
| 3. Rigor financeiro | D | B | C | A | C | B | A | D | C | B |
| 4. Venda persuasiva | C | B | A | D | B | A | C | D | B | C |
| 5. Negociação | B | D | C | D | B | C | A | C | D | A |
| 6. O método integrado | B | C | C | A | C | D | B | A | D | C |
