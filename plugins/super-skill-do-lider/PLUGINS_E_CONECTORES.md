# Plugins oficiais e conectores que trabalham junto com a Super Skill do Líder

A Super Skill do Líder não vem sozinha na máquina original: ela trabalha ao lado dos plugins
oficiais do Claude e de conectores com as ferramentas do dia a dia. Nenhum arquivo desses plugins
vem neste pacote, porque eles pertencem à Anthropic e aos parceiros que os publicam. Este guia
diz quais instalar, o que cada um faz para um líder comercial e quais skills da Super Skill do
Líder se apoiam em cada um.

## 1. Plugins oficiais recomendados

### Como instalar
- **No Claude (site e aplicativo):** abra **Customize › Plugins › Browse**, procure o plugin pelo
  nome e clique em instalar. Em planos de equipe, o administrador pode liberar o plugin para todos.
- **No Claude Code:** digite `/plugin` e use a aba de descoberta, que lista o diretório oficial. Os
  plugins de trabalho do conhecimento também podem ser instalados a partir do catálogo público da
  Anthropic: `/plugin marketplace add anthropics/knowledge-work-plugins` e, em seguida,
  `/plugin install <plugin>@<nome do catálogo>` (o nome do catálogo aparece na confirmação do
  primeiro comando).

### O que cada um faz para um líder comercial
| Plugin | Para que serve na rotina comercial | Skills dele que mais ajudam |
|---|---|---|
| Sales | Preparar visitas e reuniões, pesquisar contas, revisar negócios e carteira, escrever a previsão de vendas, tratar objeções e fazer o fechamento da semana. | call-prep, account-research, account-plan, deal-review, pipeline-review, forecast, handle-objection, weekly-wrap |
| Data | Explorar e validar bases, escrever consultas, montar gráficos e painéis, análise estatística. | explore-data, validate-data, analyze, create-viz, build-dashboard |
| Finance | Ler variação de resultado, fechamento do mês e conciliações; apoiar a leitura de P&L. | variance-analysis, close-management, reconciliation |
| Marketing | Brief de concorrência, plano de campanha e relatório de desempenho para ações de trade. | competitive-brief, campaign-plan, performance-report |
| Operations | Documentar processos e rotinas, relatório de status, análise de risco e de fornecedores. | process-doc, runbook, status-report, risk-assessment |
| Product Management | Atualização para a liderança, revisão de métricas e de roteiro. | stakeholder-update, metrics-review |
| Productivity | Memória de trabalho (glossário, siglas, quem é quem) e lista de tarefas. | memory-management, task-management |
| Enterprise Search | Busca única em e-mail, chat, documentos e wikis da empresa. | search, digest, knowledge-synthesis |
| Customer Support | Escalonamento de problema de cliente e rascunho de resposta. | customer-escalation, draft-response |
| Small Business | Pulso do negócio, relatório pronto, proposta comercial e lista de ligações. | business-pulse, report-builder, proposal-builder, call-list |
| Design | Crítica de layout e acessibilidade dos decks e painéis. | design-critique, accessibility-review |
| PDF Viewer | Ler, anotar, preencher e assinar PDFs (contratos e planos com cliente). | view-pdf, annotate, fill-form, sign |
| Cowork Plugin Management | Criar e ajustar plugins, inclusive adaptar esta Super Skill para a sua empresa. | create-cowork-plugin, cowork-plugin-customizer |

Além dos plugins, o Claude traz as **skills nativas de documentos** (Word, Excel, PowerPoint e
PDF). Confira nas configurações do Claude se elas estão ativas: várias skills deste pacote
dependem delas.

Outros plugins instalados na máquina original, de ciência de dados, observabilidade de sistemas e
banco de dados, não fazem parte da rotina comercial e ficam fora desta recomendação.

## 2. Conectores recomendados por função

Cada leitor conecta as próprias contas, com o próprio login, em **Customize › Connectors** (no
site e no aplicativo) ou pelo comando `/mcp` (no Claude Code). Nenhuma credencial vem no pacote e
nenhuma deve ser escrita no arquivo de configuração.

| Função | Conectores | Para quê |
|---|---|---|
| Arquivos e planilhas | Google Drive; Microsoft 365 (OneDrive, SharePoint, Excel) | Ler as bases e as planilhas mestres, salvar painéis, PDFs e decks na pasta do time. |
| Comunicação | Slack; Gmail e Google Calendar; Microsoft 365 (Outlook e Teams); Zoom | Mandar o resumo das rotinas, preparar agendas, achar o que foi combinado. |
| CRM | Salesforce; HubSpot; Zoho CRM; Close | Carteira, oportunidades e histórico de cada cliente para os planos de negócios e a previsão. |
| Conversas de venda | Gong; Fireflies; Otter.ai; Zoom | Resumo de reuniões, objeções reais dos compradores, próximos passos. |
| Inteligência de contas | Apollo; ZoomInfo; Crunchbase; Lusha; Clay; Similarweb | Pesquisa de conta e de mercado antes da visita. |
| Dados e BI | BigQuery; Snowflake; Databricks; Hex; Amplitude | Puxar as bases direto do repositório de dados da empresa, quando houver. |
| Projetos e documentos | Asana; Atlassian (Jira e Confluence); Monday; Notion; ClickUp; Trello; DocuSign | Plano de ação com dono e prazo, documentação das rotinas, assinatura de acordos. |

Conecte só o que a sua empresa usa e respeite a política de dados dela: a máquina lê o que o seu
login enxerga.

## 3. Quais skills da Super Skill do Líder usam cada um

| Skill | Plugins e recursos | Conectores |
|---|---|---|
| escola-de-vendas | Sales (call-prep, account-research, handle-objection, deal-review, forecast); Finance (variance-analysis) para a leitura de P&L | CRM; conversas de venda; inteligência de contas |
| painel-de-indicadores | skill nativa de Excel; Data (validate-data, create-viz) | Google Drive ou Microsoft 365 para ler as bases e guardar o painel |
| projecao-e-cenarios | skill nativa de Excel; Data (analyze) | Google Drive ou Microsoft 365 para o arquivo oficial de BE |
| sentinela | Data (explore-data); Productivity (task-management) para a ação da semana | Slack ou e-mail para distribuir o briefing |
| book-executivo | skill nativa de PowerPoint; Design (design-critique) | Google Drive ou Microsoft 365 para salvar o book |
| apresentacao-executiva | skill nativa de PowerPoint; Product Management (stakeholder-update) | Google Drive ou Microsoft 365 |
| plano-de-negocios-com-cliente | skill nativa de PowerPoint e de Excel; Sales (account-plan, account-research); PDF Viewer para anotar e assinar | CRM; Google Drive ou Microsoft 365 |
| diagnostico-de-rede | skill nativa de Excel; Data (validate-data); navegador do Claude para exportar do portal do painel de varejo | Google Drive ou Microsoft 365 |
| identidade-de-clientes | Data (validate-data) | CRM e repositório de dados, para conferir códigos |
| revisao-final | nenhuma dependência | nenhum |
| padrao-visual | skills nativas de PowerPoint e PDF; Design (accessibility-review) | nenhum obrigatório |
| rotina-atualizar-paineis | skill nativa de Excel; tarefas agendadas do Claude | Google Drive ou Microsoft 365 (bases); Slack (resumo opcional) |
| rotina-foto-do-painel | skill nativa de Excel e de PDF; tarefas agendadas | Google Drive ou Microsoft 365; Slack (resumo opcional) |
| rotina-pdf-do-painel | skill nativa de PDF; tarefas agendadas | Google Drive ou Microsoft 365 |

O motor de scripts da skill painel-de-indicadores roda localmente (Python, LibreOffice e Google
Chrome) e não precisa de conector; os conectores entram para buscar as bases e distribuir os
resultados.
