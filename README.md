# Super Skill do Líder

A máquina de governança comercial do livro **A Máquina do Líder**, de Anderson Jerônimo, livro bônus de *A Escola de Vendas*.
Versão 0.1.0.

## Instalar

**No Claude (site ou aplicativo, planos Pro e Max).** Em *Settings › Capabilities*, ligue *Code execution and file creation*.
Baixe o arquivo [super-skill-do-lider.zip](https://github.com/aescoladevendas/super-skill-do-lider/releases/latest/download/super-skill-do-lider.zip) e envie em *Customize › Plugins › Add › Upload plugin*.

**Para a equipe inteira (Team e Enterprise).** O dono da organização envia o mesmo arquivo em
*Organization settings › Plugins & skills › Add › Upload a plugin* e marca o acesso como *Installed by default*.

**No Claude Code.** Digite, um por vez:

```
/plugin marketplace add aescoladevendas/super-skill-do-lider
/plugin install super-skill-do-lider@a-maquina-do-lider
```

Para receber versões novas no Claude Code, rode `/plugin marketplace update`.

## O que vem no pacote

| Skill | Para que serve |
|---|---|
| `apresentacao-executiva` | Apresentação para diretoria, conselho ou comitê com um slide por ideia, insight que liga dado a decisão e recomendação por bloco. Use em "deck para a diretoria", "review executivo" ou "QBR". |
| `book-executivo` | Book executivo mensal ou trimestral para a diretoria, 11 slides fixos com KPIs, tabela e recomendações. Use em "atualiza o book do mês", "monta o book com estes números" ou "mesmo modelo". |
| `diagnostico-de-rede` | Diagnóstico de rede do atendimento direto só com painel de varejo, loja a loja e com plano de ação. Use quando pedirem "diagnóstico da rede X", "onde cresce e onde cai" ou "abertura por loja". |
| `escola-de-vendas` | Método comercial do livro A Escola de Vendas, do dado ao acordo em dez passos. Use em "por que o cliente caiu", "essa promoção valeu", "prepare a negociação" ou num pedido de desconto. |
| `identidade-de-clientes` | Cliente se identifica pelo código, nunca pelo nome. Consolida grupos, filiais, migrações de cadastro e operações por UF. Use ao cruzar bases de clientes ou quando um cliente some e outro nasce. |
| `padrao-visual` | Padrão visual de todo material novo (fundo cinza, cards brancos, título em dois tons) e gerador de deck em PDF. Use ao pedir "monta o deck", "PDF para o cliente" ou "material para a diretoria". |
| `painel-de-indicadores` | Painel web Meta × Realizado × Carteira, kit de PDFs por pessoa e rotina de atualização para qualquer indicador. Use em "painel de X", "dashboard para o time", "mesma visão para X". |
| `plano-de-negocios-com-cliente` | Deck C-level de diagnóstico e plano conjunto de negócios para conta do atendimento direto. Use quando pedirem "plano de negócios do cliente X", "JBP da rede" ou "material C-level do cliente". |
| `projecao-e-cenarios` | Melhor estimativa (BE) do mês e do trimestre, com cenários de queda, estabilização e crescimento cliente a cliente. Use em "BE", "como pousa o trimestre", "quanto falta para a meta". |
| `revisao-final` | As dez diretrizes de revisão que toda resposta e todo entregável cumprem antes de sair. Use como última etapa de qualquer material e quando o usuário pedir "revisão final" ou "calibrar". |
| `rotina-atualizar-paineis` | Rotina agendada que pega os exports do sistema (realizado e carteira), padroniza as bases, recalcula as planilhas e atualiza os painéis. Use em "subi as bases", "atualiza os painéis". |
| `rotina-foto-do-painel` | Rotina diária que gera o PDF das abas completas da planilha mestre (painel e carteira) para o grupo do time, sem alterar o original. Use no horário agendado ou quando pedirem "update". |
| `rotina-pdf-do-painel` | Rotina diária e silenciosa que gera o PDF do painel em formato de cartão vertical para celular, com os KPIs gerais do mês. Use no horário agendado ou em "PDF do painel de hoje". |
| `sentinela` | Vigia dos indicadores da governança comercial. Devolve um briefing de decisão em 4 blocos fixos. Use em "rodar o sentinela", "briefing da semana" ou ao anexar números pedindo leitura. |

Os plugins oficiais (Small Business, Sales, Data, Finance e outros) e os conectores (Microsoft 365, Google Drive, Slack,
CRM) completam a máquina e são instalados pelo diretório oficial do Claude, com o login de cada leitor. A lista recomendada
está em `plugins/super-skill-do-lider/PLUGINS_E_CONECTORES.md`.

## Antes de ativar

Leia as skills antes de ativar, como a Anthropic recomenda para qualquer skill de terceiros. Nenhuma skill deste pacote
pede senha nem envia dados para fora; os dados da sua empresa ficam no seu arquivo de configuração, no seu computador.
