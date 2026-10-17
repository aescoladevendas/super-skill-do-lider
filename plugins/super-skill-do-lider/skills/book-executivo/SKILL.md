---
name: book-executivo
description: Book executivo mensal ou trimestral para a diretoria, 11 slides fixos com KPIs, tabela e recomendações. Use em "atualiza o book do mês", "monta o book com estes números" ou "mesmo modelo".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

> **VISUAL SUBSTITUÍDO:** cores, fontes, fundo e cards seguem a skill `padrao-visual` (fundo
> cinza #F5F5F7, cards brancos arredondados sem sombra, Inter, título em dois tons, cor de
> destaque só no mandatório). Desta skill vale a estrutura e a lógica de conteúdo. O template
> rosa/slate abaixo continua disponível para quando a diretoria pedir o PowerPoint editável.

# Book executivo

## O que esta skill entrega

Um `.pptx` de 11 slides no template visual fixo (cor de acento #FF007F + slate
`415A6C`/`64748B`, fundo `F8FAFC` nos slides de conteúdo, Arial em tudo), pronto para
apresentar à diretoria. A estrutura é sempre a mesma; o que muda a cada uso são os números,
nomes e período. Cores e fonte podem vir de `saidas.pptx_executivo` do arquivo de configuração.
Leia `references/padrao-visual.md` para a paleta completa, tamanhos de fonte e a lista de
defeitos já vistos (estouro de texto, contagem de colunas de tabela) e como evitá-los
**antes de montar o pptx**.

## Quando usar

- Fechamento mensal ou trimestral com KPIs por executivo, loja, produto, região etc. que sempre
  seguem o padrão "aqui está o resultado, aqui está o destaque, aqui está a recomendação".
- O usuário já usou este book antes (mesmo em outro projeto ou cliente) e quer o mesmo padrão de
  letras, cores e formato, só trocando os dados reais.
- Pedidos como "atualiza o book de [mês]", "monta o book executivo com estes números", "quero o
  mesmo template para [outro cliente ou projeto]".

Se o pedido for uma apresentação avulsa sem essa estrutura fixa de KPI + tabela + insight (um
pitch, uma proposta comercial, um one-pager), não force esta skill: use a skill
`apresentacao-executiva`.

## Como montar (fluxo)

Há dois caminhos. Os dois usam `scripts/build_content_slide.py` para GERAR os 4 slides de
conteúdo (KPI cards + tabela + LEITURA) inteiros via Python, em vez de editar célula a célula:
é muito mais rápido e evita o erro mais comum (contagem de colunas da tabela).

1. **Entenda a decisão e o conteúdo antes de montar.** Pergunte ao usuário (se não estiver
   claro): quais são os 4 blocos temáticos deste book (ex.: Visão Geral, Sell In, um indicador de
   distribuição, RV, ou o que fizer sentido para o negócio), quais os KPIs de cada bloco e qual a
   lista de itens (executivos, lojas, produtos) que viram linhas da tabela.
2. **Descreva o conteúdo em texto estruturado primeiro** (Diagnóstico → Insight → Dado →
   Recomendação, como na skill `apresentacao-executiva`) e mostre ao usuário para aprovar antes
   de gerar o arquivo.
3. **Copie `assets/template-base.pptx`** para a pasta de trabalho: é o arquivo com a estrutura de
   11 slides e placeholders genéricos (`[Bloco 1: título]`, `[LABEL KPI 1]`, `[Item 1]` etc.).
   Para regenerar o template com outras cores: `python3 scripts/gerar_template.py`.
4. **Caminho A, com python-pptx (mais simples):** abra a cópia com `Presentation`, troque os
   textos da capa, agenda, 4 divisores e fechamento e escreva os 4 slides de conteúdo com
   `escrever_no_slide(prs.slides[i], ...)` (slides 4, 6, 8 e 10). Salve.
5. **Caminho B, editando o XML:** descompacte (unpack) com a skill pptx do Claude, edite os slides
   simples com localizar e substituir nos `<a:t>`, gere cada slide de conteúdo com
   `build_slide(..., out_path=".../ppt/slides/slideN.xml")`, que sobrescreve o XML do slide por
   completo, e depois limpe e reempacote (clean e pack) com a skill pptx do Claude. Ajuste
   `presentation.xml`, rels e `[Content_Types].xml` só se os nomes dos slides mudarem.
6. **QA visual obrigatório**: converta para PDF e imagens (LibreOffice + PyMuPDF) e confira CADA
   slide, especialmente: texto da LEITURA não colide com o rodapé, delta dos KPI cards não quebra
   linha, tabela com todas as colunas certas (sem célula "fantasma" azul). Corrija e renderize de
   novo antes de entregar.
7. **Salve o arquivo final na pasta real do projeto** (`caminhos.clientes` ou
   `caminhos.compartilhada` da configuração), nunca só na pasta de trabalho temporária, que pode
   ser apagada entre sessões.

## Adaptando para um novo projeto ou cliente

Trocar apenas: nome do book, do cliente e da empresa na capa e nos rodapés, os 4 títulos de bloco
(agenda + divisores), os 4 conjuntos de KPI cards, os cabeçalhos e linhas da tabela de cada bloco
e as 4 recomendações finais. Manter sempre: paleta de cores, tamanhos de fonte, estrutura de 11
slides, o padrão de "linha TOTAL em negrito" e a regra de "LEITURA em no máximo 2 linhas".

## Arquivos desta skill

- `assets/template-base.pptx`: o arquivo-base com a estrutura completa e placeholders genéricos
  (nunca sobrescreva este arquivo à mão: copie antes de editar).
- `scripts/build_content_slide.py`: gera um slide de conteúdo completo (etiqueta + título + 4
  KPI cards + tabela + LEITURA) a partir de dados Python. Tem uma validação embutida que impede o
  bug de contagem de colunas e monta a grade com o número de colunas do cabeçalho. Teste rápido:
  `python3 scripts/build_content_slide.py demo.xml`.
- `scripts/gerar_template.py`: regenera `assets/template-base.pptx` do zero.
- `scripts/configuracao.py`: leitura do arquivo de configuração (cópia idêntica à do
  `painel-de-indicadores`).
- `references/padrao-visual.md`: paleta, tamanhos de fonte, estrutura detalhada dos 11 slides e
  lista de defeitos já vistos.
