---
name: diagnostico-de-rede
description: Diagnóstico de rede do atendimento direto só com painel de varejo, loja a loja e com plano de ação. Use quando pedirem "diagnóstico da rede X", "onde cresce e onde cai" ou "abertura por loja".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Diagnóstico de rede · painel de varejo

Um exercício, sempre igual, para qualquer rede do atendimento direto: só dado do painel de
varejo (dados de ponto de venda, PDV), sem base própria do cliente e sem Sell In, mês
fechado, base comparável explicitada, abertura por loja e plano de ação com dono.
Resultado: `DIAGNOSTICO_<REDE>_PAINEL_VAREJO_LOJAS.xlsx` na pasta do cliente
(`caminhos.clientes/<cliente>`) e os dados brutos em `diagnostico_rede.subpasta_dados`
(`_dados_painel_varejo_P0X/`). O Excel alimenta a skill plano-de-negocios-com-cliente.

## 1. Extração no portal do painel de varejo (navegador)

Login do usuário: se cair na tela de login, pedir para ele entrar e responder "ABERTO".
Nunca digitar senha; nunca resolver verificação anti-robô. Se o painel abrir em branco,
voltar à página inicial do portal e reabrir o relatório. Janela larga (cerca de 1500 x 800).

### 1.1 KPIs por SKU (total da empresa) · mensal, de setembro de dois anos atrás até o mês corrente
A ordem dos filtros importa: a cascata reseta os valores dos filtros de baixo.
1. **Filtro de compartilhamento de dados do cliente = (Tudo).** O padrão costuma ser "libera
   tudo": redes que não liberam a concorrência ficam VAZIAS até marcar (Tudo). Elas entregam
   a empresa em detalhe e a concorrência agregada como `OUTRA MARCA / OUTROS PRODUTOS` por
   categoria (`diagnostico_rede.rotulos_concorrencia_agregada`).
2. **Rede = nome exato.** Buscar; clicar (Tudo) para desmarcar tudo antes; marcar a rede e
   conferir no zoom que só ela está marcada. Cuidado com homônimos: duas redes com o mesmo
   nome em estados diferentes podem ser independentes, de uma loja cada.
3. **Unidade, segmento e categoria = (Tudo).** Filtros de unidade ou categoria que vêm
   pré-selecionados escondem segmentos inteiros (um tira-manchas em pó, tabletes de
   lava-louças); sem isso uma marca aparece até 20 vezes menor.
4. **Top SKU** num valor que cubra todo o universo (ex.: 1000).
5. Export: clicar numa célula da tabela, clicar na margem branca à direita, abrir o ícone de
   download (pode precisar de dois cliques), escolher "tabela cruzada" e CSV. O arquivo sai em
   UTF-16 separado por tabulação. Mover e renomear NA HORA (o navegador reaproveita a
   numeração): `kpi_REDE.csv`.
6. Repetir por estado do PDV (`kpi_UF_PA.csv`, `kpi_UF_TO.csv`...): abrir a lista, desmarcar
   tudo, marcar o estado, Aplicar, clicar na margem branca. NUNCA apertar Escape logo depois
   de Aplicar: reverte o filtro para (Tudo) sem avisar. Se só UM estado sair, o cubo deriva
   "Demais estados = rede menos esse estado" (aritmética exata).
7. Conferir cada arquivo pelo primeiro valor da tabela E pelo SKU da primeira linha contra a
   tela antes de renomear: a ordem dos SKUs muda de um estado para outro.

### 1.2 Análise por rede, abertura por loja · semanal
Ordem: compartilhamento = (Tudo) → rede (buscar e marcar) → unidade = (Tudo) (o padrão
esconde segmentos) → semana = (Tudo). Clicar célula → download → tabela cruzada → planilha da
abertura → CSV → renomear para `abertura_lojas.csv` (loja x categoria x fabricante x marca x
SKU x semana, cinco métricas por semana). O filtro de rede em "(valores múltiplos)" pode
trazer outras redes marcadas que não aparecem na busca (já veio uma rede com outras duas
juntas): o script filtra pelo PREFIXO do nome da loja, por isso sempre passar `--prefixo`.
Loja a loja só existe a partir da primeira semana que o portal abre: é leitura de TENDÊNCIA
dentro do ano (P1 = 12 semanas x P2 = 12 semanas), nunca contra o ano anterior. Visões
automáticas do portal (ex.: diagnóstico por loja) só existem para algumas redes: testar e
registrar.

### 1.3 Armadilhas de clique já mapeadas
- Escape dentro de uma lista de filtro reverte a seleção (fechar clicando no título).
- (Tudo) com seleção parcial marca tudo; clicar de novo desmarca tudo.
- As opções do diálogo de export são exclusivas; o tooltip de célula cobre o ícone de
  download: clicar na margem branca antes.
- Clicar numa célula abre "manter apenas / excluir": nunca clicar nessas opções.
- Listas de estado têm vizinhos parecidos (Mato Grosso e Mato Grosso do Sul; Pará, Paraíba e
  Paraná) e alguns só aparecem rolando: zoom antes de Aplicar.
- A consulta pode levar até 20 s: esperar e reler a tela em vez de clicar Aplicar de novo.
- Quando o portal permite abrir o relatório fora do quadro embutido, o quadro maior é mais
  estável. Conferir no disco que cada arquivo chegou.
- Não salvar exibição personalizada sem o usuário pedir.

## 2. Processamento (scripts/)
```bash
python3 scripts/painel_varejo_cubo.py  --rede "REDE EXEMPLO NORTE" --pasta <dados>     # kpi_*.csv → cubo_rede.json
python3 scripts/painel_varejo_lojas.py --prefixo "REDE EXEMPLO NORTE" --pasta <dados>  # abertura_lojas.csv → cubo_lojas.json
python3 scripts/montar_diagnostico.py  --rede "Rede Exemplo Norte" --executivo "Executivo B" \
    --pasta <dados> --lojas-desc "PA 14, TO 4"
```
- A empresa = `produtos.marcas_foco`; a config é lida por `scripts/configuracao.py`.
- `uf_map.json` (`{"NOME DA LOJA": "UF"}`) na pasta de dados quando nem o nome nem o endereço
  trazem o estado (lojas numeradas LJ1, LJ2...). Para achar a loja de outro estado: comparar
  o `kpi_UF_<UF>` (R$ do mês, mercado e empresa) com a soma das semanas de cada loja no mesmo
  mês; a que bate é a do estado.
- Mês fechado: o último mês do export é parcial e fica fora (`--mes-fechado` para forçar).
- Depois: recalcular no LibreOffice (`soffice --headless --convert-to xlsx --outdir recalc
  <arquivo>` com HOME temporário), ler com openpyxl `data_only` e procurar células "#..."
  (os cabeçalhos "#" das abas SKUs, LOJAS e PLANO não são erro); zero erro de fórmula é
  necessário, não suficiente. Conferir zero travessão. Copiar o Excel para a pasta do cliente
  e os CSVs, o `uf_map.json` e os cubos para a subpasta de dados; abrir o arquivo para o
  usuário.
- Teste de regressão (sempre que mexer nos scripts): `scripts/gerar_dados_exemplo.py --pasta
  <rascunho>` cria a rede fictícia no formato do portal; rodar os três scripts e conferir 10
  abas (11 com `--liberada`) e zero erro de fórmula. Nunca gerar teste dentro do plugin.

O montador é 100% dirigido a dado: leitura C-level, ganhos e perdas de share por categoria,
plano de ação (categorias em perda, presença por marca, lojas em queda, gaps, defesa do motor,
categoria sem marca da empresa com peso de 3% ou mais do mercado) e FONTE mudam sozinhos por
rede. Ações por categoria em `diagnostico_rede.acoes_por_categoria`; limiares em
`LIMIARES_PADRAO` (troca em `diagnostico_rede.limiares`).

## 3. O Excel padrão (10 abas)
LEITURA (fechamento rede e estados, últimos 3 meses de mesma base, categorias mercado x
empresa com leitura, C-level) · MÊS A MÊS (set de dois anos atrás até o mês fechado, fórmulas
vivas) · MARCAS E CATEGORIAS · SKUs DA EMPRESA (lojas com venda, sinal: perdeu lojas, saiu,
novo) · LOJAS (resumo por UF e ranking, P2 vs P1, mix, SKUs ativos, movimento) · LOJAS x
SEMANA · LOJAS x CATEGORIA (gaps em cinza) · LOJAS x SKU (top 30 x lojas, cinza = gap de
sortimento) · CONCORRÊNCIA (só se a rede libera as marcas) · PLANO DE AÇÃO (linhas geradas do
dado, com dono e prazo) · FONTE.

## 4. Regras inegociáveis
- Só painel de varejo. Nada de base própria do cliente, BI do cliente ou Sell In neste
  arquivo (o plano-de-negocios-com-cliente cruza depois).
- A empresa = `produtos.marcas_foco`. Marcas de `diagnostico_rede.marcas_fora_da_empresa`
  contam como mercado. Categoria de `produtos.categoria_sem_marca_da_empresa` = "categoria
  sem marca da empresa".
- Meses fechados; mês corrente parcial fica fora. Base comparável sempre escrita (lojas com
  venda por mês).
- Cada rede fala só de si mesma (não comparar redes no material do cliente).
- Números em R$ e pt-BR (1.234,5; +12,3%); zero travessão; visual da skill padrao-visual;
  revisão final pela skill revisao-final.
- Excluir as linhas "Total" do export (marca, categoria ou SKU = Total) antes de somar,
  senão dobra. CSV do portal: ler como texto e converter o milhar brasileiro à mão.
