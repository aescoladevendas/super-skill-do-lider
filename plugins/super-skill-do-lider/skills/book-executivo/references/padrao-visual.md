# Padrão visual: book executivo

## Paleta de cores

Chave entre parênteses: `saidas.pptx_executivo` do arquivo de configuração.

| Uso | Cor | Hex |
|---|---|---|
| Acento (etiqueta, faixas dos cards, faixa do KPI, linha da agenda, faixa de rodapé da capa, divisor e fechamento) | Acento (acento) | `FF007F` |
| Texto principal, títulos, valores de KPI | Slate escuro (slate) | `415A6C` |
| Texto secundário, labels de KPI, segmento | Slate médio (slate_medio) | `64748B` |
| Texto de rodapé (rodapé, numeração de página) | Slate claro (slate_claro) | `94A3B8` |
| Fundo dos slides de conteúdo (tabela e KPI) | Quase branco (fundo_conteudo) | `F8FAFC` |
| Fundo dos slides de capa, divisor e fechamento | Slate escuro (slate) | `415A6C` |
| Linha zebrada da tabela (linhas ímpares) | Cinza muito claro (zebra) | `F1F5F9` |
| Cabeçalho da tabela | Slate escuro | `415A6C` (texto branco `FFFFFF`) |
| Negativo, alerta, abaixo da meta | Vermelho (negativo) | `C0392B` |
| Positivo, acima da meta (usar com moderação: a maioria dos books reais tem mais alerta que elogio) | Verde (positivo) | `50B428` |
| Bordas de card, linhas de tabela | Cinza claro (borda) | `E2E8F0` |
| Subtítulo e rodapé sobre fundo slate | Cinza azulado | `DEE5EA` |
| Número gigante do divisor | Slate translúcido | `51697B` |

Regra de ouro: o acento é SEMPRE acento (nunca fundo de texto longo), slate é texto,
vermelho e verde são só para o "delta" dos KPI cards e para o texto que precisa saltar aos olhos.
Não inventar cores novas: se precisar de mais uma categoria, reusar uma das acima.

## Tipografia

Arial em 100% do documento. Tamanhos usados (em `sz` do OOXML, ou seja, valor ÷ 100 = pt):

| Elemento | sz | pt |
|---|---|---|
| Etiqueta (em caixa alta) | 1100 | 11pt, negrito, `spc="400"` |
| Título de slide de conteúdo | 2800 | 28pt, negrito |
| Título de capa | 4800 | 48pt, negrito, branco |
| Subtítulo de capa e divisor | 1400 a 1600 | 14 a 16pt |
| Número gigante do divisor ("01" a "04") | 9200 | negrito, cor `51697B` (translúcido) |
| "PARTE N" do divisor | 1200 | negrito, `spc="400"` |
| Label do KPI card | 1050 | negrito, `spc="200"`, cor `64748B` |
| Valor do KPI card | 2000 (reduzir para 1400 a 1500 se o texto for longo, tipo "Nome Sobrenome: 57%") | negrito, cor `415A6C` |
| Delta do KPI card | 1100 | negrito, cor `C0392B`, `415A6C` ou `50B428` conforme o caso |
| Cabeçalho de tabela | 950 | negrito, branco |
| Célula de tabela | 950 | normal (negrito só na linha TOTAL) |
| "LEITURA" (label) | 1100 | negrito, `spc="300"`, acento |
| Texto da LEITURA | 1300 | normal, slate: **máx. 2 linhas** (confira os defeitos já vistos) |
| Rodapé (texto + página) | 900 | cor `94A3B8` |

## Estrutura de 11 slides

1. **Capa**: fundo slate, etiqueta no acento, título branco grande, 2 linhas de subtítulo,
   linha curta no acento, rodapé.
2. **Agenda**: fundo claro, "SUMÁRIO" + "Agenda", 5 cards numerados (1 a 5) com faixa de acento
   à esquerda, título + descrição de 1 frase cada. O item 5 é sempre "Próximos Passos".
3-4, 5-6, 7-8, 9-10. **4 pares Divisor + Conteúdo**, um por bloco temático:
   - Divisor: fundo slate, "PARTE N", número gigante translúcido, título branco, 1 ou 2 frases
     de diagnóstico, rodapé.
   - Conteúdo: fundo claro, etiqueta + título, **4 KPI cards**, **1 tabela** (cabeçalho slate +
     linhas zebradas + linha TOTAL em negrito), **1 caixa LEITURA** com o insight que conecta o
     bloco à recomendação.
11. **Fechamento / Próximos Passos**: fundo slate, título, lista de 4 recomendações com
    marcador no acento (cada uma é uma ação específica, com dono ou prazo implícito: nunca
    "monitorar" ou "acompanhar" sozinho).

Numeração de página: `NN/11` no rodapé de cada slide (exceto a capa).

## Padrão dos 4 KPI cards (por slide de conteúdo)

Cada card = 5 formas: retângulo branco de fundo, faixa vertical fina de acento à esquerda,
label (caixa alta, cinza), valor (grande, slate, negrito), delta (cor conforme o sinal). Ordem
recomendada (ajuste ao conteúdo real):

1. O número mais importante do bloco (ex.: resultado total, % de atingimento).
2. Um número de contexto ou meta (neutro, cor slate).
3. O destaque específico: melhor ou pior desempenho, ou o mais próximo ou mais distante de uma
   meta.
4. O alerta: pior caso, maior risco, ou o que precisa de ação imediata.

## Padrão da tabela

- 8 colunas é o padrão (1 coluna larga para nome ou ID à esquerda, 6 colunas médias de dado, 1
  coluna larga à direita para uma leitura textual como "Situação", "Farol" ou "% Fech Proj").
  Pode variar (o script monta a grade com o número de colunas do cabeçalho), mas mantenha o
  cabeçalho slate + zebra + TOTAL em negrito.
- Uma linha por item (por executivo, loja, SKU) + **sempre** uma última linha TOTAL em negrito,
  com fundo `F1F5F9` como as linhas pares.
- Use `scripts/build_content_slide.py` em vez de escrever XML de tabela na mão: é MUITO mais
  rápido e evita erros de contagem de coluna.

## Defeitos já vistos e como evitar

1. **Texto da LEITURA maior que 2 linhas colide com o rodapé.** A caixa de LEITURA fica a
   795528/5998464 EMU do canto superior esquerdo, com só cerca de 550.000 EMU (0,6") até o
   rodapé em 6547104 EMU. A 13pt com 125% de espaçamento de linha, isso dá umas 2,5 linhas.
   Escreva a LEITURA pensando em no máximo 2 linhas: se não couber, corte, não deixe estourar.
2. **Delta do KPI card com texto longo quebra linha e vaza da borda do card.** O card tem só
   1234440 EMU de altura. Se o delta for uma frase longa (ex.: "NR negativo (devolução > venda)"),
   encurte para caber em uma linha (ex.: "NR negativo no mês").
3. **Toda linha da tabela (inclusive TOTAL) precisa ter o mesmo número de células que os
   `<a:gridCol>` definidos.** Se uma linha tiver uma célula a menos, PowerPoint e LibreOffice não
   dão erro de XML: "improvisam" uma célula extra com uma cor de reserva (apareceu como um bloco
   azul sólido cobrindo cerca de 2 linhas de altura). O script tem uma validação que pega isso
   antes de gerar o arquivo.
4. **Nome ou valor longo no card ("Luísa Andrade: 51,7%")**: reduza `valsz` de 2000 para 1400
   a 1500 (parâmetro `valsz` no card) para não estourar a largura do card.
5. **A pasta de trabalho temporária do ambiente é apagada entre sessões.** Nunca deixe o
   `.pptx` final só lá: copie para o destino real (pasta do projeto do usuário) assim que
   possível.
