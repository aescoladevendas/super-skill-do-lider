# Padrão visual · tokens e regras

Ajustado em seis rodadas num deck real de cliente. Cada token tem o nome usado no `deckkit.py`,
a chave correspondente em `saidas.identidade_visual` do arquivo de configuração e o valor padrão
(o que vale quando a chave não existe).

## Cores

| Token (deckkit) | Chave na configuração | Hex padrão | Uso |
|---|---|---|---|
| FUNDO | fundo | #F5F5F7 | fundo de todas as páginas |
| CARD | card | #FFFFFF | cards (raio 18px, sem sombra, sem borda) |
| GRAFITE | grafite | #1D1D1F | texto principal, títulos, totais |
| CINZA | cinza_texto | #6E6E73 | continuação do título, subtítulos, leitura, legendas |
| APOIO | apoio | #86868B | apoio fraco |
| LINHA | linha | #D2D2D7 | linha sob o cabeçalho da tabela; trilho da linha do tempo |
| LINHA_TABELA | linha_tabela | #ECECEF | linhas entre registros |
| DESTAQUE | destaque | #FF007F | só o mandatório: manchete da proposta, % e valor do investimento, régua, numeração, pontos da linha do tempo, barras do período atual, marca que tenha o destaque como cor própria |
| ETIQUETA | etiqueta | #B64400 | etiqueta acima do título e rótulos de card, em maiúsculas |
| LINK | link | #0066CC | nomes de participantes na capa, com "›" |
| VERDE | verde | #248A3D | crescimento |
| AMARELO | amarelo | #B88400 | atenção (faixa intermediária, ex.: 4 a 7 semanas de estoque) |
| VERMELHO | vermelho | #D70015 | perda e falta |
| BARRA_ANTERIOR | barra_anterior | #D2D2D7 | barra do período anterior |
| BARRA_REFERENCIA | barra_referencia | #6E6E73 | meta ou referência nos gráficos de colunas |
| MARCAS | produtos.cores_marcas | (por marca) | nome da marca nas tabelas |

## Tipografia (página 1600x900)

Fonte: Inter (`fonte_web`), fallback Helvetica Neue e Arial. Em Excel e PowerPoint, Arial
(`fonte_office`).

| Elemento | Tamanho | Peso |
|---|---|---|
| Título da capa | 104px | 600 |
| Título do capítulo | 78px | 600 |
| Título do slide (h1) | 48px | 600, letras apertadas -0.015em |
| Etiqueta | 17px | 600, maiúsculas, laranja |
| Subtítulo e leitura | 19 a 21px | 400, CINZA |
| Número gigante (declaração) | 112px | 600 |
| Manchete de destaque (proposta) | 104px | 700 |
| Investimento | 128px % + 64px R$ | 700 |
| Tabela | 26 (big), 22 (padrão), 18 (mid), 16px (tight) | 400; total 600 |
| Rodapé | 13px | 400, CINZA, logos à direita |

## Estrutura de página

* A margem lateral é de 80px. O título vem no topo, o conteúdo ocupa o resto e o rodapé fica a 22px da base.
* Use 20px de espaço entre cards.
* A capa tem cabeçalho em duas colunas:
  * à esquerda, título grande e logos;
  * à direita, a frase de apoio e os participantes na cor de link;
  * embaixo, uma faixa com 3 cards de foto, um por capítulo.
* No capítulo, o título em dois tons fica à esquerda e a foto em card à direita.
* Sem foto, o card recebe um marcador desenhado em traço fino (nunca um bloco cinza dentro do card).
* O fechamento é uma checklist numerada em um card, com os valores em grafite e negrito.

## O que já foi rejeitado (não repetir)

1. Quatro cards iguais em toda página, com caixa colorida de LEITURA (cara de modelo de IA).
2. Fundo preto ou navy.
3. Blocos cinza dentro de cards brancos, ou sombra nos cards ("quadro sobre quadro", "tom sobre tom").
4. Texto inteiro ou tabelas na cor de destaque.
5. Foto antiga e histórica do cliente na capa.
6. Arredondamento que diverge do Excel (R$ 15,8 Mi no lugar de R$ 15,75 Mi).
7. Tabela estourando a página ou card encostado no rodapé.
