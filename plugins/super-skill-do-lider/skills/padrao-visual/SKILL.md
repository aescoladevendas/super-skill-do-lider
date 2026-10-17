---
name: padrao-visual
description: Padrão visual de todo material novo (fundo cinza, cards brancos, título em dois tons) e gerador de deck em PDF. Use ao pedir "monta o deck", "PDF para o cliente" ou "material para a diretoria".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Padrão visual

É o padrão de **todo** material novo: PDFs, decks, painéis, one-pagers e materiais de cliente,
mesmo quando o pedido não cita o padrão. Foi aprovado pelo gerente depois de seis rodadas num
deck real de cliente. Substitui, no visual, o template rosa/slate da skill `book-executivo` (a
estrutura do book continua valendo lá). A skill `revisao-final` continua valendo por cima: abrir
com "Revisão final em uso.", zero travessão, premissas declaradas e recomendação no fim.

O visual se descreve pelos tokens: fundo cinza #F5F5F7, cards brancos arredondados sem sombra,
título em dois tons e a cor de destaque da empresa só no que é mandatório. Os valores ficam em
`saidas.identidade_visual` do arquivo de configuração; os hexadecimais abaixo são o padrão.

## Regras visuais (não negociáveis)

1. **Fundo cinza #F5F5F7 em toda a página.** Nunca fundo preto, navy ou branco puro.
2. **Um card branco por bloco de conteúdo**, com raio de 18px, **sem sombra e sem borda**. A
   sombra cria uma moldura cinza ("tom sobre tom") que já foi rejeitada.
3. **Nunca coloque um card dentro de outro card.** Também nunca use um fundo cinza dentro de um
   card branco.
4. **Fonte:** Inter (uso livre, SIL Open Font License), com fallback para Helvetica Neue e Arial.
   Títulos com peso 600 e letras levemente apertadas.
5. **Título em dois tons:** a afirmação em grafite #1D1D1F e a continuação em cinza #6E6E73,
   separadas por ponto ("A demanda se manteve. Quem caiu foi a compra."). O `two_tone()` faz
   isso sozinho quando o título tem "; ", ": " ou ". ".
6. **Etiqueta acima do título** em laranja #B64400, em maiúsculas.
7. **Cor de destaque (#FF007F no exemplo) só no que é mandatório:**
   * o número-manchete da proposta;
   * o % e o valor do investimento;
   * os percentuais da régua;
   * a numeração 01, 02;
   * os pontos da linha do tempo;
   * as barras do período atual.

   O destaque nunca vai em títulos, texto corrido ou tabelas inteiras.
8. **Semáforo só em números com significado:** verde #248A3D para crescimento, amarelo #B88400
   para atenção e vermelho #D70015 para perda.
9. **Marcas:** cada marca com cor própria (`produtos.cores_marcas` da configuração), só no nome
   da marca dentro de tabelas. As demais marcas ficam em grafite.
10. **Gráficos de barras:** período anterior em cinza #D2D2D7, atual na cor de destaque, meta ou
    referência em #6E6E73. Sem eixo, sem grade e com o valor em cima da barra.
11. **Fotos** do cliente vêm do site oficial dele, nunca do acervo histórico. Elas entram em
    cards: na capa, como uma prateleira de 3 cards; nos capítulos, como uma foto em card ao lado
    do título. Sem foto, o deckkit desenha um marcador em traço fino no lugar.

Especificação completa de tokens, tamanhos e o que evitar: `references/padrao-visual.md`.

## Como gerar

```python
import sys, os; sys.path.insert(0, '<pasta desta skill>/assets')
from deckkit import *
d = Deck('Empresa × Cliente · Tema · Período', logos=[logo('logo_empresa.svg'), logo('logo_cliente.png')])
d.cover(['Título', 'Linha 2'], 'Frase que resume a decisão.', ['Nome · Cargo', ...],
        'Mês de AAAA.', 'Continuação em cinza.', shelf=[(etiqueta, nome, desc, img(foto), '50% 50%'), ...])
d.chapter('01', 'Como foi o ano', 'Subtítulo em cinza.', img(foto))
d.slide('ETIQUETA', 'Afirmação. Continuação.', tab(cab, linhas, total, cls='big'), read='leitura curta')
pngs = d.save('saida.pdf')   # gera HTML + PDF 1600x900 e as montagens de QA
```

* Os logos são opcionais e entram por caminho (`logo('arquivo')`); o primeiro é o da empresa.
  Para um SVG branco sobre o fundo cinza, use `logo('arquivo.svg', cor_svg=GRAFITE)`.
* Foto ausente (`None` na prateleira ou no capítulo) vira o marcador desenhado.
* As cores vêm da configuração em uso (`--config`, `SUPER_SKILL_CONFIG`,
  `~/.super-skill-do-lider/empresa.yaml` ou o exemplo do plugin). Para trocar uma cor só num
  deck: `import deckkit; deckkit.DESTAQUE = '#0071E3'` antes do `save()`.
* O PDF sai pelo Chrome sem janela (headless): caminho em `ambiente.binarios.chrome`. A fonte
  Inter é buscada na Google Fonts na hora de gerar (`carregar_fonte_web`); sem internet, o deck
  cai para Helvetica Neue e Arial sem quebrar o layout.

O `slide()` decide sozinho: os blocos `kpis`, `statement`, `two`, `invest` e `pillars` ficam
direto no cinza (cada parte já é um card); qualquer outro conteúdo é embrulhado em um único
card, com a leitura dentro dele.

| Componente | Uso |
|---|---|
| `statement((label, valor, sub, cor), ...)` | até 3 números gigantes ("o ano em números") |
| `kpis(kpi(...), ...)` / `stack(...)` | linha ou coluna de KPIs |
| `hero(label, valor, sub)` | número-manchete na cor de destaque (valor da proposta) |
| `tab(cab, linhas, total, cls)` | tabela; `cls`: `big` poucas linhas, `mid`, `tight` muitas linhas, `nw` sem quebra |
| `two(a, b, wide_left)` | duas colunas, cada uma um card |
| `bars`, `hbars`, `columns` | barras agrupadas, variação horizontal, colunas de ano e meta |
| `invest(pct, valor, sub, partes)` + `timeline([...])` | investimento e agenda |
| `pillars([...], regua=[...])` | programa com pilares e régua de atingimento |
| `numbered([...])` / `checklist([...])` | plano por frente e fechamento "o que sai desta sala" |
| `var(x)`, `marca(nome)`, `destaque(txt)` | variação colorida, cor da marca, destaque pontual |
| `logo(caminho)`, `img(caminho)`, `placeholder()` | logo, foto e marcador desenhado |

Os formatadores BR são `n0`, `d1`, `mil`, `mi(x, casas)`, `rsk`, `pc` e `p0`. Use `mi(x, 2)`
quando o número tiver de bater com a proposta (R$ 15,75 Mi, e não R$ 15,8 Mi).

## Fluxo obrigatório

1. **Roteiro:** um slide, uma ideia (skill `apresentacao-executiva`). O título é a conclusão e a
   leitura vira o texto curto.
2. **Dados:** gere só a partir de base verificada e declare as premissas na leitura ou numa nota.
3. **Gerar** com `deckkit`.
4. **QA visual:** o `save()` devolve PNGs em montagem 2x2. Leia todos e corrija estouro de
   tabela, texto cortado, card encostado no rodapé e número arredondado diferente do Excel.
   Só depois entregue.
5. **Entregar:**
   * salve na pasta do cliente (`caminhos.clientes`, uma subpasta por cliente) e na pasta
     compartilhada do time (`caminhos.compartilhada`);
   * abra com `open`;
   * registre a entrega, com data, no log (`caminhos.log_entregas`);
   * envie o arquivo na conversa.

## Outros formatos no mesmo padrão

* **Excel:** fundo branco nas abas de dados.
  * Cabeçalho de tabela em grafite #1D1D1F com texto branco.
  * Título da aba em grafite.
  * Destaque só no número mandatório.
  * Semáforo verde, amarelo e vermelho nos status.
  * Fonte Arial (`saidas.identidade_visual.fonte_office`): a Inter nem sempre está instalada
    em quem abre a planilha.
* **Painel web (artefato):** mesmos tokens; o fundo da página é #F5F5F7 e os cards são brancos,
  com raio de 18px e sem sombra.
* **PPTX** (só se pedido): reproduza os tokens com Arial e cards brancos arredondados sobre fundo
  #F5F5F7.

## Exemplos

* `examples/exemplo_minimo.py` gera um slide de cada componente. Rode esse exemplo para validar
  o ambiente: `python3 examples/exemplo_minimo.py saida/exemplo_minimo.pdf`.
* `examples/exemplo_completo.py` gera o deck inteiro de uma proposta de reposição para a
  Distribuidora Horizonte (caso fictício): capa, três capítulos, números-manchete, tabelas,
  barras, proposta, programa com régua, investimento, linha do tempo, onde fecha o ano, plano
  por UF e fechamento. Os números ficam no bloco `CASO` do próprio arquivo.

Licença da fonte: a Inter é de uso livre (SIL Open Font License) e pode ir em material
distribuído fora da empresa. Para trocar de fonte, mude `saidas.identidade_visual.fonte_web`.
