# Super Skill do Líder · versão 0.1.0

A máquina de governança comercial do livro **A Máquina do Líder**, em forma de plugin para o
Claude. São todas as skills da máquina, o motor de scripts que atualiza bases, planilhas, painéis
e PDFs, e um arquivo de configuração onde moram os dados da sua operação. Nada aqui traz dado de
empresa real: o exemplo é o caso fictício da Distribuidora Horizonte, do livro A Escola de Vendas.

## O que vem no pacote

| Skill | O que faz |
|---|---|
| `escola-de-vendas` | O método inteiro de A Escola de Vendas: dados, categoria, valor, venda e acordo, no fluxo de dez passos. |
| `painel-de-indicadores` | Painel web Meta × Realizado × Carteira com link fixo, kit de PDFs por pessoa, contrato de dados e leitor da configuração. |
| `sentinela` | Briefing semanal de decisão em quatro blocos: o que mudou, o porquê, o que observar e a ação. |
| `projecao-e-cenarios` | Melhor estimativa de fechamento do mês e do trimestre, com cenários de queda, estabilização e crescimento. |
| `book-executivo` | Relatório recorrente para a diretoria: capa, agenda, quatro blocos de indicadores e recomendações. |
| `apresentacao-executiva` | Deck para diretoria e conselho: uma ideia por slide, insight, dado de suporte e recomendação. |
| `plano-de-negocios-com-cliente` | Plano conjunto de negócios e diagnóstico executivo de uma rede, com projeção e plano de ação. |
| `diagnostico-de-rede` | Diagnóstico de uma rede com dados de PDV: rede contra mercado, estados, categorias e loja a loja. |
| `identidade-de-clientes` | Consolidação de grupos, filiais e mudanças de cadastro pelo código do cliente, nunca pelo nome. |
| `revisao-final` | As dez diretrizes de revisão que toda entrega cumpre antes de sair. |
| `padrao-visual` | Identidade visual única para deck, PDF, painel e planilha. |
| `rotina-atualizar-paineis` | Rotina agendada: export do sistema, bases padronizadas, planilhas recalculadas e painéis publicados. |
| `rotina-foto-do-painel` | Rotina diária: PDF das abas completas da planilha mestre, pronto para o grupo do time. |
| `rotina-pdf-do-painel` | Rotina diária: PDF do painel em cartão vertical para o celular. |

Estrutura:
```
.claude-plugin/plugin.json        manifesto do plugin
.claude-plugin/marketplace.json   catálogo para instalar pelo Claude Code
config/exemplo_empresa.yaml       o "cérebro do negócio" em dados (fictício)
skills/<nome>/SKILL.md            cada skill, com references/, scripts/ e assets/
PLUGINS_E_CONECTORES.md           plugins oficiais e conectores que trabalham junto
```

A máquina também usa plugins oficiais do Claude (Sales, Data, Finance e outros), as skills
nativas de documentos e conectores com as suas ferramentas (Drive, Microsoft 365, Slack, CRM).
Nada disso vem no pacote: o guia `PLUGINS_E_CONECTORES.md` diz o que instalar e conectar, e
quais skills usam cada um.

## Instalar no Claude (site e aplicativo)
1. Baixe o arquivo `super-skill-do-lider.zip` (o endereço está no QR code do livro).
2. No Claude, abra **Customize › Plugins › Add › Upload plugin** e escolha o arquivo.
3. Ative o plugin. As skills passam a ser acionadas pelas frases de cada uma (ex.: "rodar o
   sentinela", "como pousa o trimestre", "prepare a negociação").

## Instalar no Claude Code
Com o repositório publicado (o endereço está no livro):
```
/plugin marketplace add aescoladevendas/super-skill-do-lider
/plugin install super-skill-do-lider@a-maquina-do-lider
```
Para testar a partir de uma pasta local, use o caminho da pasta no lugar do endereço.

## Configurar para a sua empresa
1. Copie `config/exemplo_empresa.yaml` para `~/.super-skill-do-lider/empresa.yaml`.
2. Troque cada bloco marcado **[TENANT]** pelos dados da sua operação (pessoas, clientes e
   códigos, marcas, metas, caminhos, colunas dos exports do seu sistema). Os blocos **[ENGINE]**
   são as regras do método: mexa só se quiser mudar uma regra.
3. Confira: `python3 skills/painel-de-indicadores/scripts/configuracao.py`.

Os scripts procuram a configuração nesta ordem: `--config arquivo.yaml`, a variável
`SUPER_SKILL_CONFIG`, `./empresa.yaml`, `~/.super-skill-do-lider/empresa.yaml` e, por último, o
exemplo fictício do plugin.

## O que precisa estar instalado
- Python 3.9 ou mais novo: `pip install pandas openpyxl pyyaml python-pptx pymupdf pillow matplotlib`
- LibreOffice (recalcula as planilhas e converte documentos)
- Google Chrome (gera os PDFs dos painéis em modo headless)

## Primeiro teste (com o exemplo fictício)
```bash
python3 skills/painel-de-indicadores/scripts/configuracao.py                  # qual configuração está em uso
python3 skills/identidade-de-clientes/scripts/identidade_clientes.py --teste  # regras de cliente da config
python3 skills/padrao-visual/examples/exemplo_completo.py /tmp/exemplo_completo.pdf   # deck de exemplo
python3 skills/diagnostico-de-rede/scripts/gerar_dados_exemplo.py --pasta /tmp/teste_rede   # dados fictícios de uma rede
```
Os scripts do motor do painel (atualizar bases, recalcular, gerar painel, PDFs e Excel) entram na
versão 0.2; nesta versão, a skill painel-de-indicadores traz as regras, o contrato de dados e o
leitor da configuração.

Depois, faça cinco perguntas ao Claude para conferir se a máquina ligou:
1. "Rode o sentinela com os números do painel desta semana."
2. "Como pousa o trimestre? Quero a projeção de setembro com os três cenários."
3. "A Distribuidora Horizonte pediu 5% de desconto. Prepare a negociação."
4. "Consolide a Distribuidora Horizonte por UF e separe o atacado."
5. "Faça a revisão final deste texto antes de eu mandar para a diretoria."

## Licença
Todos os direitos reservados ao autor. Para outros usos, fale com o autor.
