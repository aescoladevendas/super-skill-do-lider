# Padrão visual obrigatório do PowerPoint

Este documento descreve o padrão visual extraído de um deck real de plano de negócios com
cliente, aprovado pela diretoria. **Toda apresentação em PowerPoint gerada por esta skill segue
esta paleta, tipografia e estrutura de componentes**: não é um exemplo de inspiração, é o padrão
da casa. Os valores podem vir de `saidas.pptx_executivo` do arquivo de configuração.

## Paleta de cores

| Uso | Hex | Onde aparece |
|---|---|---|
| Acento (cor da marca da empresa) | `FF007F` | Etiquetas (caixa alta pequena), faixa de destaque em cards, "PARTE N", título "LEITURA", faixas do topo e da base de capa, divisor e fechamento |
| Texto título, slate escuro | `415A6C` | Títulos de slide, números grandes de KPI, quadrado numerado do sumário |
| Texto corpo, slate médio | `64748B` | Labels de KPI ("LOJAS ATIVAS"), corpo de texto em caixas brancas |
| Texto secundário claro | `94A3B8` | Rodapé (trilha + paginação) sobre fundo claro |
| Texto sobre fundo escuro | `DEE5EA` / `FFFFFF` | Subtítulos em slides de capa e divisores de seção |
| Positivo (alta, crescimento) | `50B428` | Variações percentuais positivas |
| Negativo (queda, risco) | `C0392B` | Variações negativas, rótulo "DIVERGÊNCIA" (vermelho na mesma família de saturação do verde: verde é bom, vermelho é ruim) |
| Convergência, dependência | `00A6A5` | Rótulo "CONVERGÊNCIA", rótulo de card de dependência, delta neutro positivo |
| Risco | `F08C2A` | Rótulo dos cards de risco |
| Fundo de card | `FFFFFF` | KPI cards, caixas de tabela e leitura (borda `E2E8F0`) |
| Fundo de slide de conteúdo | `F8FAFC` | Slides de conteúdo; zebra da tabela `F1F5F9` |
| Fundo de capa, divisor e fechamento | `415A6C` | Slate escuro, com faixa de acento no topo e na base |
| Número fantasma do divisor | `51697B` | Número gigante translúcido |
| Gráfico de linha | `B7C6D6` ano anterior, `FF007F` ano atual | Série anterior em cinza azulado, atual no acento com rótulo de dado |

Nunca usar azul genérico ou paletas da lista padrão da skill pptx: a empresa tem identidade
visual própria e ela prevalece.

## Tipografia

Fonte única: **Arial** em todos os elementos (títulos, corpo, labels, números). Não trocar por
outra fonte mesmo que pareça mais "premium": consistência com o padrão da casa importa mais que
variedade.

| Elemento | Tamanho |
|---|---|
| Título de capa | 48pt, branco |
| Subtítulo de capa | 16pt |
| Etiqueta (caixa alta, acento) | 11pt (13pt na capa e no fechamento) |
| Título de slide de conteúdo | 28pt, slate `415A6C` |
| Título de slide divisor de seção | 34pt, branco |
| Subtítulo de slide divisor | 14pt |
| Número grande de KPI | 18 a 24pt, slate |
| Label de KPI (caixa alta) | 10.5pt, slate médio |
| Corpo de texto em caixa | 13 a 14pt |
| Rodapé (trilha + página) | 9pt, cinza claro |
| Número fantasma de seção | cerca de 92pt |

## Componentes recorrentes (reusar, não reinventar)

1. **Capa**: fundo slate com faixas de acento, etiqueta "DIAGNÓSTICO EXECUTIVO · [TEMA]",
   título do cliente ou projeto em branco 48pt, subtítulo descritivo, linha de assinatura
   ("[Empresa] · Gerência [Nome] · [Mês/Ano]") no rodapé.
2. **Sumário/Agenda**: lista numerada (1 a 6) com quadrado slate + número branco, título do
   bloco e descrição de uma linha; espelha os blocos temáticos do conteúdo.
3. **Divisor de seção** ("PARTE N"): fundo slate, número fantasma gigante translúcido, label
   "PARTE N" no acento, título da seção em branco, subtítulo com o resumo do que vem a seguir.
4. **Slide de conteúdo padrão**: etiqueta em caixa alta no acento + título slate 28pt + rodapé
   com trilha e paginação. O corpo varia (KPI cards, tabela, gráfico).
5. **KPI cards**: linha de 3 ou 4 cards brancos, cada um com label em caixa alta cinza, número
   grande slate e uma variação (verde se positiva) abaixo. Faixa fina de acento à esquerda do
   card.
6. **Caixa "LEITURA"**: caixa branca com etiqueta "LEITURA" (ou "LEITURA PARA A DIRETORIA" quando
   cruza várias fontes de dado, em caixa slate com texto branco) no acento + texto de insight em
   slate. Esta caixa É o "Insight estratégico" da skill: sempre que o slide tiver um KPI, gráfico
   ou tabela, inclua uma caixa LEITURA explicando o que aquilo significa para a decisão.
7. **Cards de convergência e divergência**: pares de caixas lado a lado contrastando duas
   leituras ("CONVERGÊNCIA" em `00A6A5` e "DIVERGÊNCIA" em `C0392B`) antes da caixa de leitura
   consolidada.
8. **Cards de risco**: uma caixa por risco (grade 2x2), com título em caixa alta nomeando o
   risco (`F08C2A`; dependência em `00A6A5`) e corpo explicando a dependência ou o impacto.
9. **Slide de fechamento "PRÓXIMOS PASSOS"**: lista de ações específicas (uma por marcador, cada
   uma com dono e ação concreta), fundo slate com faixas de acento, mais a linha de assinatura
   do rodapé.
10. **Rodapé padrão** em todo slide de conteúdo: `[Tema da apresentação] · [Página atual]/[Total]`.

## Como aplicar

Ao montar o PPTX final (depois da etapa de revisão do texto estruturado):

1. Parta do arquivo-base (nesta versão, `assets/template-base.pptx` da skill `book-executivo`,
   que traz capa, sumário, divisor, KPI cards, caixa LEITURA e fechamento nesta paleta); não
   comece do zero.
2. Use o fluxo de edição da skill pptx do Claude (descompactar, editar, reempacotar) ou
   python-pptx: identifique os slides cujos componentes servem de base, duplique conforme o número
   de blocos temáticos do conteúdo aprovado, substitua texto e números.
3. Não invente componentes visuais se um dos componentes acima já resolve o que o slide precisa.
   Cores e fontes vêm exclusivamente da tabela acima, não das paletas genéricas da skill pptx.
4. Mantenha o rodapé com trilha e paginação corretos em todo slide de conteúdo (atualize
   "NN/Total" conforme o número final de slides).
5. Rode a QA visual (conversão para imagem + inspeção de todas as páginas) antes de entregar:
   estouro de texto é o defeito mais comum ao reaproveitar caixas de texto com conteúdo de
   tamanho diferente do original.
