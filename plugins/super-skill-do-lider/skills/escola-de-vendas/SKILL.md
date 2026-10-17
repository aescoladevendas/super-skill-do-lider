---
name: escola-de-vendas
description: Método comercial do livro A Escola de Vendas, do dado ao acordo em dez passos. Use em "por que o cliente caiu", "essa promoção valeu", "prepare a negociação" ou num pedido de desconto.
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Escola de Vendas: o método comercial em cinco etapas e dez passos

Esta skill é a camada de raciocínio comercial da máquina. Ela aplica o método do livro "A Escola de
Vendas" para transformar dado em insight, insight em oportunidade de categoria, oportunidade em valor
nos dois P&Ls (o da empresa e o do cliente) e valor em acordo com o cliente. Ela define o que dizer e
em que ordem; o formato da entrega (deck, painel, planilha, PDF) fica com as skills de entrega do
plugin, descritas em "Integração".

## Quando usar

Use sempre que o pedido envolver uma destas situações, mesmo que o usuário não cite o método:

- diagnóstico de performance (Sell In, Sell Out, positivação, MSL, ruptura) de distribuidor,
  atacadista ou rede: "por que as vendas caíram", "por que o cliente caiu", "o que está acontecendo
  com o cliente X";
- avaliação ou desenho de promoção, encarte ou ação de trade (linha de base, uplift, ROI): "essa
  promoção valeu?", "vale repetir o encarte?";
- lacuna de MSL, positivação ou sortimento;
- plano de crescimento de categoria ou plano de negócios conjunto (joint business plan, JBP), com os
  4 Shopper Mores (os quatro "mais" do shopper), os 5W, a Lente Tripla e as Perguntas de Ouro;
- leitura de P&L, margem e mix, margem front e back, P&L e ROI do distribuidor;
- pedido de desconto, verba, prazo ou bonificação;
- preparação de visita ou de reunião com comprador, apresentação interna (finanças, marketing de
  trade) ou externa, argumento de venda;
- objeção do cliente;
- preparação e condução de negociação: "prepare a negociação", ZOPA, moedas de troca e contrapartidas,
  "Se você… então eu…";
- quando o usuário citar SMART, C.L.E.A.N., A.R.I.O., ZOPA, Esboço, Quadro de negociação, Lente
  Tripla, Perguntas de Ouro ou o método de negociação em seis passos.

**Não use sozinha** para gerar o arquivo final (book, painel, PDF, deck): use esta skill para o
conteúdo e a skill de entrega para o formato.

## Fio condutor: as cinco etapas do método

O método segue a curva de aprendizado do livro, em cinco etapas que se acumulam: ninguém negocia bem
sem saber vender, ninguém vende bem sem saber quanto vale a proposta, e ninguém sabe quanto vale uma
proposta sem dados confiáveis e sem entender o shopper. Cada etapa corresponde a um capítulo do livro
e a uma referência desta skill.

| Etapa | Módulo (capítulo do livro) | Pergunta central | Ferramentas principais | Referência |
|---|---|---|---|---|
| 1. Dados | Leitura de dados (data acumen), Capítulo 1 | O que está acontecendo e por quê? | Diagnóstico de queda, avaliação de promoções, lacunas de MSL, diligência e relevância, O quê / Por quê / E daí / E agora | `references/01_leitura_de_dados.md` |
| 2. Categoria | Crescimento de categorias, Capítulo 2 | Onde está a oportunidade de crescer? | 5W, 4 Shopper Mores, necessidades do cliente, Perguntas de Ouro, Lente Tripla, alavancas de ativação | `references/02_crescimento_de_categorias.md` |
| 3. Valor | Rigor financeiro, Capítulo 3 | Quanto vale, e para quem? | Cascata do P&L, regra do 1%, margem e markup, margem total do cliente, P&L e ROI do distribuidor, volume de equilíbrio | `references/03_rigor_financeiro.md` |
| 4. Venda | Venda persuasiva, Capítulo 4 | Como levar o cliente a dizer sim? | SMART, C.L.E.A.N., 7Cs, funil de perguntas, benefícios, fechamentos, A.R.I.O. | `references/04_venda_persuasiva.md` |
| 5. Acordo | Negociação, Capítulo 5 | Como fechar quando o cliente pede algo em troca? | Estilos, ZOPA, método de negociação em seis passos, Esboço, Quadro de negociação | `references/05_negociacao.md` |

A introdução do método (canais de venda, estratégia omnicanal, régua de proficiência) está em
`references/00_introducao.md`, e o Capítulo 6 do livro, "O método integrado", é o fluxo de dez passos
descrito abaixo.

Regra-mãe: **venda mais, venda primeiro** (sell more, sell first). Quanto mais você vende, menos
precisa negociar.

## O fluxo de dez passos

1. **Enquadrar.** Escreva a pergunta de negócio, o cliente ou canal, a medida, o período e o objetivo
   (a ficha de enquadramento) e combine com quem pediu. Se faltar algo essencial, pergunte antes de
   analisar.
2. **Checar os dados** (diligência e relevância): cálculos, outros períodos e lacunas; os dados
   respondem à pergunta, cobrem o universo certo e o período certo?
3. **Diagnosticar (O quê / Por quê).** Numa queda de vendas, siga a ordem: (1) o mercado ou a região
   caiu também? → (2) houve ruptura ou perda de distribuição ou de MSL? → (3) a base de comparação
   tinha promoção que não se repetiu? Separe o **fato** (o quê) do **insight** (por quê) e decomponha a
   variação em causas quantificadas cuja soma feche com o total.
4. **Encontrar a oportunidade.** Qual dos 4 Shopper Mores mover (mais shoppers, mais frequentemente,
   comprar mais, gastar mais)? Perfil do shopper pelos 5W; necessidades do cliente (estratégicas, do
   shopper, operacionais, financeiras); teste da **Lente Tripla** (é bom para o shopper, para o cliente
   e para a empresa?).
5. **Quantificar.** P&L da empresa (regra do 1%, margem bruta %, mix, receita líquida) e P&L do cliente
   ou do distribuidor (margem total front + back, ROI = lucro líquido ÷ investimento); ROI da ação
   (líquido acima de 0%).
6. **Definir o objetivo SMART** da conversa: específico, mensurável, ambicioso e atingível, relevante,
   com prazo e rastreável.
7. **Montar a venda com o C.L.E.A.N.** Situação atual (current situation: 7Cs, funil de perguntas,
   necessidades) → frase de ligação → oportunidade principal (leading opportunity: ideia + R$ +
   necessidade) → executar com perfeição (execute flawlessly: sortimento e distribuição, exposição e
   visibilidade, preço, promoções) → benefícios incríveis (amazing: um benefício por necessidade) → E
   agora? (now what: fechamento e primeiro passo fácil).
8. **Antecipar objeções com A.R.I.O.**: antecipar, relacionar-se, isolar e superar; preparar um dado ou
   uma solução para cada objeção provável.
9. **Negociar só se necessário** (venda completa e resposta "Não, eu preciso de…"): escolher o estilo
   (complexidade × dependência) → ZOPA (meta perto do ponto de ruptura do outro lado; abrir fora da
   ZOPA; movimentos planejados e decrescentes) → Esboço (preço, moedas de troca, contrapartidas;
   binária ou faixa) → arrumar a mesa → troca condicional "Se você… então eu…" → registrar no Quadro de
   negociação.
10. **Medir e aprender.** KPIs de entrada (distribuição, cobertura, acurácia da previsão) e de
    resultado (receita, lucro, margem); ROI pós-evento, comparado com o previsto; atualizar o plano e
    voltar ao passo 1.

Três regras tornam o fluxo eficiente. Nenhum passo começa sem o entregável do anterior (não se
negocia uma proposta que não foi vendida). Dado faltante vira pergunta ou premissa declarada, nunca
número inventado. E toda análise termina em E daí e E agora, com recomendação, responsável e prazo.

## Roteamento rápido

Nem todo pedido exige os dez passos. O que não muda é a ordem dos passos usados.

| Pedido do usuário | Passos | Referência |
|---|---|---|
| "Por que o cliente X caiu?" | 1 a 3 (+4 para recomendação) | `references/01_leitura_de_dados.md` |
| "Essa promoção (ou esse encarte) valeu a pena?" | 2, 5 | `01_leitura_de_dados.md`, `03_rigor_financeiro.md` |
| "Plano de crescimento" ou "plano de negócios conjunto (JBP)" | 3 a 7 | `02_crescimento_de_categorias.md`, `04_venda_persuasiva.md` |
| "O distribuidor pede desconto, verba ou prazo" | 5, 9 | `03_rigor_financeiro.md`, `05_negociacao.md` |
| "Prepare minha reunião com o comprador" | 4 a 8 | `04_venda_persuasiva.md` |
| "Como respondo a essa objeção?" | 8 | `04_venda_persuasiva.md` |
| "Prepare a negociação" | 5, 9 | `05_negociacao.md` |
| "Como vender neste canal?" ou plano por canal | 1 | `00_introducao.md` |
| Testar ou calibrar esta skill | todos | `06_exercicios_de_calibracao.md` |

Se o pedido de desconto vier justificado por uma queda de vendas, o caminho começa antes, pelos
passos 1 a 3: a queda precisa ser confirmada e explicada antes de qualquer concessão.

## Checklists essenciais

**Antes de mandar qualquer número:** cálculos conferidos · outros períodos conferidos · lacunas (lojas,
filiais, cadastros, semanas) · responde à pergunta · universo certo · período comparável.

**Avaliação de promoção:** objetivo (empresa + cliente) · linha de base · volume incremental e uplift ·
lucro bruto por unidade regular e promocional · custos totais · ROI líquido acima de 0% · efeito
pós-promoção · mecânica escolhida pelo objetivo (no exemplo de referência do livro, o corte de 50%
maximiza vendas e o de 20% maximiza lucro bruto).

**Proposta de crescimento:** Shopper More-alvo · 5W do shopper · necessidade do cliente atendida ·
alavanca de ativação · Lente Tripla · KPIs de entrada e de resultado.

**Antes de conceder desconto ou verba:** objetivo · volume de equilíbrio em valor e em margem ·
contrapartida mensurável · front (na nota) ou back (condicionado) · como medir o ROI.

**Apresentação de venda:** objetivo SMART · 7Cs do cliente · necessidades confirmadas · ideia em uma
frase com R$ · execução (quatro alavancas) · um benefício por necessidade · tipo de fechamento ·
objeções antecipadas.

**Negociação:** venda completa · estilo definido · meu ponto de ruptura · ponto de ruptura deles
estimado · ZOPA · meta · abertura · escada de concessões decrescentes · Esboço (moedas de troca e
contrapartidas custeadas) · Quadro de negociação pronto.

## Fórmulas essenciais

| Indicador | Fórmula |
|---|---|
| Uplift | Volume incremental ÷ volume de linha de base |
| Lucro bruto incremental da promoção | (Un. promo × LB promo/un) − (Un. base × LB regular/un) |
| ROI da promoção | Líquido: (LB incremental − custos) ÷ custos (equilíbrio = 0%) · Bruto: LB incremental ÷ custos (equilíbrio = 1,0) |
| Cascata do P&L | Vendas brutas − descontos e verbas = receita líquida − COGS = margem bruta − A&P (BEI e Non-BEI) = contribuição do produto − custos fixos = lucro operacional |
| Regra do 1% | +1% de receita líquida vale mais que 1% de economia em COGS ou em custos fixos comerciais (CFC) |
| Margem % | (Preço − custo) ÷ preço |
| Markup % | (Preço − custo) ÷ custo (markup de 50% = margem de 33,3%) |
| Margem total do cliente | Front (desconto em nota) + back (rebates, pagamento por desempenho, incentivos de MSL, cobertura e logística) |
| ROI do distribuidor | Lucro líquido ÷ (estoque + crédito ao mercado + reembolsos a receber + outros − crédito do fabricante) |
| Volume de equilíbrio de um corte de preço | 1 ÷ (1 − % de corte) − 1 (−5% → +5,3% só para empatar em valor) |
| ZOPA | [ponto de ruptura do vendedor ; ponto de ruptura do comprador] (exemplo do álcool em gel: R$ 70 a R$ 90, abertura em R$ 100, acordo em R$ 85) |
| % da ZOPA capturado pelo vendedor | (Acordo − ponto de ruptura do vendedor) ÷ (ponto de ruptura do comprador − ponto de ruptura do vendedor) |

## Modelos de frases

- **Insight:** "O quê: [fato]. Por quê: [causa ou comportamento]. E daí: [oportunidade ou ameaça em
  R$]. E agora: [ação, responsável, prazo]."
- **Abertura que engaja:** "Você sabia que [fato surpreendente]?" · "[Marca] cresce, mas você trabalha
  só [1 de 3] SKUs." · "Lojas com [MSL completo] cresceram [x]% mais que as sem."
- **Funil de perguntas:** "Que oportunidades você vê para crescer suas vendas?" → "Pode me contar
  mais?" → "Então o desafio é [resumo], certo?" → "Posso mostrar uma ideia?"
- **Frase de ligação:** "Você disse que [necessidade]. Se eu pudesse mostrar [benefício], você teria
  interesse?"
- **Oportunidade principal:** "Minha proposta é [ideia], que vai [benefício] e acrescentar [R$] por
  [período]."
- **Benefícios incríveis:** "Você disse que [necessidade 1]; por isso [benefício 1]. Você quer
  [necessidade 2]; mostrei que [benefício 2 em R$]."
- **Fechamentos:** experimental "Está de acordo em seguir com…?" · alternativo "Fazemos em outubro ou
  em novembro?" · assumido "Vou providenciar o pedido." · ponto menor "Quer o material de PDV agora ou
  na próxima visita?" · próximo passo "Trago as amostras na semana que vem."
- **A.R.I.O.:** "Entendo totalmente o desafio de…" → "Fora isso, há mais alguma coisa que impeça…?" →
  "Para resolver, analisamos… Qual destas opções faz sentido?"
- **Troca condicional:** "Se você [contrapartida ou preço]… então eu [moeda de troca]…" (comece sempre
  pelo que você quer).
- **Perguntas de Ouro (abertura do plano anual ou do JBP):** "O que fizemos bem no ano passado e o que
  poderíamos ter feito melhor?" · "Quais são suas prioridades e KPIs para o próximo ano?" · "Qual o
  papel da categoria no seu negócio?" · "Haverá revisão de sortimento ou de espaço?" · "Quais são suas
  metas financeiras?"

## Padrão de qualidade (antes de entregar)

- [ ] Nenhum número sem fonte, período e universo explícitos; nenhum número inventado: dado faltante
      vira pergunta ou premissa declarada.
- [ ] Toda análise termina em **E daí? / E agora?**, com recomendação, responsável e prazo.
- [ ] Fato e insight separados; correlação não tratada como causa.
- [ ] A proposta diz qual Shopper More move e passa na Lente Tripla.
- [ ] Impacto quantificado nos dois P&Ls (empresa e cliente), com memória de cálculo.
- [ ] Margem % lida junto com valores absolutos; margem não é markup.
- [ ] Toda concessão tem contrapartida ("Se você… então eu…") e cabe na ZOPA.
- [ ] Linguagem adaptada ao público (cliente: giro, margem e crescimento do negócio dele; liderança da
      empresa: incrementalidade, ROI e lucro).
- [ ] Valores em R$ no padrão brasileiro (R$ 4,85; R$ 100 mil; R$ 1,7 milhão). Os números das
      referências são casos ilustrativos do livro, com as contas conferidas; nos projetos reais, use os
      dados verificados do cliente.

## Integração com as outras skills do plugin

Esta skill define **o que dizer**; as skills de entrega definem **o formato**:

- `plano-de-negocios-com-cliente`: plano de negócios conjunto (JBP) e diagnóstico executivo de cliente;
- `diagnostico-de-rede`: diagnóstico de rede ou cliente com dados de ponto de venda (PDV);
- `painel-de-indicadores`: painéis de indicadores e kit de PDFs por pessoa;
- `book-executivo` e `apresentacao-executiva`: decks para diretoria;
- `padrao-visual`: identidade visual de todo material;
- `projecao-e-cenarios`: projeções de fechamento e cenários;
- `sentinela`: briefing semanal de decisão sobre os indicadores;
- `revisao-final`: revisão final de toda resposta e de todo entregável.

## Referências

- `references/00_introducao.md`: o papel do executivo comercial, estratégia omnicanal (dois alicerces
  e seis frentes), os sete canais de venda, as cinco etapas do método e a régua de proficiência
  (básico, intermediário, avançado, mentor).
- `references/01_leitura_de_dados.md`: três Vs, fontes de dados, diagnóstico de queda, promoções, MSL e
  análise de lacunas, fato e insight, narrativa com dados.
- `references/02_crescimento_de_categorias.md`: mentalidade de categoria, 5W, missões de compra, 4
  Shopper Mores, necessidades do cliente, Perguntas de Ouro, Lente Tripla, ativação.
- `references/03_rigor_financeiro.md`: P&L, regra do 1%, margem e markup, cadeia de valor, rota ao
  mercado e custo de servir, front e back, P&L e ROI do distribuidor, volume de equilíbrio.
- `references/04_venda_persuasiva.md`: SMART, C.L.E.A.N., 7Cs, perguntas e escuta, benefícios,
  fechamentos, A.R.I.O., vender ou negociar.
- `references/05_negociacao.md`: competitiva ou colaborativa, complexidade e dependência, ZOPA, método
  de negociação em seis passos, Esboço, arrumar a mesa, troca condicional, Quadro de negociação.
- `references/06_exercicios_de_calibracao.md`: os 60 exercícios do livro, com gabarito e justificativa,
  para usar como casos de teste da skill (a resposta da skill deve coincidir com o gabarito).

## Versão

0.1.0
