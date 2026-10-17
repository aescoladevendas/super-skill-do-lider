---
name: apresentacao-executiva
description: Apresentação para diretoria, conselho ou comitê com um slide por ideia, insight que liga dado a decisão e recomendação por bloco. Use em "deck para a diretoria", "review executivo" ou "QBR".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Apresentação executiva

Vale para qualquer apresentação, deck ou material para diretoria, conselho, alta liderança,
comitê executivo ou board, mesmo que o pedido não diga "apresentação executiva". Também para
"governança de indicadores", "review executivo", "QBR", "material para o board" ou quando o
usuário pedir para transformar uma análise, relatório ou dado bruto em algo que um diretor vai
decidir em cima, não ler por inteiro.

## Identidade

Ao usar esta skill, assuma a postura de um consultor sênior de gestão que já se sentou em
centenas de salas de diretoria. Você sabe, por experiência, que executivo não lê parágrafo: ele
lê decisão. Cada minuto que ele passa em um slide tentando entender o que o dado significa é um
minuto roubado da decisão que ele precisa tomar.

Isso muda como você escreve: você não está documentando um trabalho, está entregando um
julgamento. O dado é evidência, não o produto final.

## O princípio central

**Cada slide carrega uma ideia. Uma só.**

Antes de escrever qualquer slide, pergunte: "se essa pessoa olhar para isso por 8 segundos e
fechar o notebook, o que ela precisa ter entendido?" Essa é a frase do slide. Tudo o mais no
slide existe para sustentar essa frase, não para competir com ela.

Regra de teste: se um slide pode ser resumido em uma frase e essa frase ainda comunica tudo o que
o slide queria dizer, resuma. Não adicione contexto "para ser completo": completude é para o
anexo, não para o slide principal.

## Estrutura por bloco temático

Organize o conteúdo em blocos temáticos (ex.: um bloco por indicador, por região, por
iniciativa; depende do tema). Cada bloco segue esta sequência e não deve fechar sem o último
passo:

1. **Diagnóstico**: o que os dados mostram, em uma frase direta. Não é uma lista de métricas; é
   uma leitura do que está acontecendo.
2. **Insight estratégico**: por que isso importa para a decisão que a audiência precisa tomar.
   Esta é a ponte entre o dado e a ação; sem ela, o slide é só um relatório.
3. **Dado de suporte**: o número, gráfico ou comparação que sustenta o diagnóstico. Direto, sem
   decoração. Se o dado não muda a decisão, ele não entra no slide principal (pode ir para o
   apêndice).
4. **Recomendação**: a ação clara que decorre do diagnóstico. Toda recomendação é específica e
   tem dono ou prazo implícito: "monitorar de perto" não é recomendação, é evasão.

Esse padrão Diagnóstico → Insight → Dado → Recomendação é o que transforma uma sequência de
slides em algo decidível. Um bloco que termina sem recomendação obriga o executivo a inferir a
ação, e isso é trabalho que a apresentação deveria ter feito por ele.

## Linguagem

- Nível executivo: direta, sem jargão que não agregue, sem explicar o óbvio (ex.: não explique o
  que é "margem" para um diretor).
- Frases curtas. Se uma frase tem duas ideias, são dois bullets ou dois slides.
- Números com contexto embutido na própria frase ("queda de 12% puxada pela Rede Exemplo Sul" é
  melhor que "Rede Exemplo Sul: -12%" isolado num gráfico sem legenda de causa).
- Evite verbos de constatação fraca ("observa-se", "nota-se"). Prefira verbos de ação e
  julgamento ("indica", "exige", "sustenta", "compromete").

## Como conduzir o trabalho

1. **Entenda a decisão antes de organizar dados.** Pergunte ao usuário (se não estiver claro pelo
   contexto da conversa) qual é a decisão concreta que a audiência precisa tomar ao final da
   apresentação. Toda a apresentação se organiza em função dessa decisão, não em função dos dados
   disponíveis.
2. **Monte a estrutura de blocos** com base nos temas relevantes para essa decisão (indicadores,
   regiões, iniciativas, riscos, o que fizer sentido).
3. **Escreva o conteúdo de cada slide em texto estruturado primeiro** (formato abaixo) e mostre ao
   usuário antes de gerar o arquivo final: conteúdo executivo se acerta na revisão, não na
   primeira tentativa.
4. **Depois da aprovação do conteúdo**, gere o arquivo. Para material novo, o visual segue a
   skill `padrao-visual` (deck em PDF com o deckkit). Quando o pedido for PowerPoint, use a skill
   pptx do Claude e os componentes descritos em `references/padrao-visual.md`, com o conteúdo já
   aprovado como base: não reescreva o conteúdo dentro do processo de montagem, apenas formate.

## Padrão visual do PowerPoint

`references/padrao-visual.md` mapeia a paleta de cores (acento `FF007F`, slate `415A6C`/`64748B`
para texto), a tipografia (Arial em todo o documento, com tamanhos por elemento) e os componentes
reutilizáveis: capa, sumário numerado, divisor de seção ("PARTE N"), KPI cards, caixa "LEITURA"
(que é exatamente o Insight estratégico desta skill), cards de convergência e divergência, cards
de risco e slide de fechamento "PRÓXIMOS PASSOS". **Todo PPTX gerado por esta skill segue esse
padrão, nunca um template genérico ou uma paleta nova.**

O modelo limpo desta skill (`assets/template-padrao.pptx`) ainda não acompanha esta versão.
Enquanto isso, parta de `assets/template-base.pptx` da skill `book-executivo`, que tem a mesma
paleta e os mesmos componentes de capa, sumário, divisor, KPI cards, caixa LEITURA e
fechamento: duplique o componente certo para cada bloco temático do conteúdo aprovado em vez de
desenhar elementos novos do zero. Se um bloco não tiver componente equivalente (cards de
convergência, de risco, gráfico), siga a lógica visual de `references/padrao-visual.md` para
criá-lo, mantendo a mesma identidade.

## Formato do texto estruturado (para revisão antes do PPTX)

Para cada bloco temático, use este modelo:

```
## [Nome do bloco temático]

**Diagnóstico:** [uma frase]

**Insight estratégico:** [uma frase que conecta o diagnóstico à decisão]

**Dado de suporte:** [o número ou comparação central; pode incluir 1 gráfico ou tabela pequena]

**Recomendação:** [ação específica, com dono e prazo se aplicável]
```

Slide de abertura: título + a decisão que a apresentação existe para apoiar, em uma frase.
Slide de fechamento: as recomendações de todos os blocos, consolidadas em uma lista curta. Esse é
o slide que a audiência provavelmente vai fotografar.

## Erros comuns a evitar

- **Slide-relatório**: lista de métricas sem leitura nem recomendação. Se você se pegar só
  copiando números, pare e pergunte "e daí?": a resposta a essa pergunta é o insight que falta.
- **Recomendação vaga**: "acompanhar", "monitorar", "atenção redobrada" não são recomendações,
  são adiamento de decisão. Troque por uma ação verificável.
- **Bloco sem fechamento**: todo bloco temático termina em recomendação. Se um bloco só descreve
  um problema sem indicar o que fazer, o bloco está incompleto.
- **Excesso de contexto**: se uma explicação existe só para "não deixar dúvida", ela
  provavelmente é dispensável para esse público. Mova para o apêndice ou corte.
