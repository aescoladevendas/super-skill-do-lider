---
name: painel-de-indicadores
description: Painel web Meta × Realizado × Carteira, kit de PDFs por pessoa e rotina de atualização para qualquer indicador. Use em "painel de X", "dashboard para o time", "mesma visão para X".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Painel de indicadores: o modelo de visão do negócio

Modelo completo para criar a "visão de indicadores do negócio": painel web interativo, kit de
PDFs por pessoa para o celular e rotina de atualização, no racional Meta × Realizado × +Carteira.
Nasceu do painel de Sell In (um espelho do relatório oficial de acompanhamento de Sell Out do BI
da empresa) e serve para QUALQUER indicador: Sell Out, MSL, positivação, estoque, RV, trade,
share, devoluções, cobertura.

Leia `references/implementacao-canonica.md` para o mapa de arquivos do modelo, o contrato do JSON
e o checklist de adaptação. Todo dado da operação (pessoas, clientes, marcas, metas, caminhos,
colunas dos exports) vem do arquivo de configuração, lido por `scripts/configuracao.py`. Nesta
versão 0.1 a skill traz as regras, o contrato e o leitor da configuração; os scripts do motor
(atualizar bases, recalcular, gerar painel, PDFs e Excel) entram na versão 0.2 com os nomes
listados na referência. Até lá, monte o gerador seguindo o contrato e guarde os seus scripts em
`caminhos.scripts`.

O visual segue a skill padrao-visual (fundo #F5F5F7, cards brancos arredondados sem sombra, fonte
Inter, cor de destaque só no mandatório; tokens em `saidas.identidade_visual`). Desta skill vale
a estrutura e a lógica de conteúdo.

## Quando acionar
Sempre que o usuário pedir para criar, montar, replicar ou "usar o modelo do painel" para qualquer
indicador, ou disser "quero um painel igual ao de Sell In", "mesma visão para X", "criar
acompanhamento de X", "dashboard de X para o time", "PDF por executivo". Também para EVOLUIR os
painéis existentes deste padrão. Não é para apresentação em slides (use book-executivo ou
apresentacao-executiva).

## Os 4 entregáveis (nesta ordem de prioridade)
1. **Painel web:** HTML único e autocontido (dados embutidos em JSON, SVG gerado por JS, sem
   biblioteca externa), publicado como artefato do Claude E salvo como arquivo local. O arquivo
   local é o canal de distribuição que sempre funciona (o visualizador de artefatos pode bloquear
   impressão, download e publicação pública).
2. **Kit de PDFs para o celular:** um PDF do GERENTE (visão total) + um por executivo (a área
   completa dele), em retrato, coluna única e tipos grandes, gerados por Chrome headless com
   predefinições no hash da URL (`#wa=1&ind=cx&exec=Nome`). É o formato preferido para dividir
   com o time.
3. **Rotina de republicação:** gerador Python que lê as bases, agrega num JSON compacto e injeta
   no template; roda a cada carga de bases e republica o artefato no MESMO link (guarde o link em
   `saidas.artefatos_link_fixo`).
4. **PDF sob demanda:** script que aceita os mesmos filtros do hash e salva na pasta de
   comunicação quando o usuário pedir "PDF dessa visão".

Documente o pipeline novo no protocolo do negócio (`caminhos.cerebro`): o usuário espera que
"subiu base → tudo atualiza" sem precisar pedir.

## O racional dos indicadores (o coração do modelo)
- **Atingimento = REALIZADO ÷ meta.** O número grande, a cor e a ordenação nunca usam a projeção.
  Cores: verde a partir de 100%, âmbar a partir de 90%, vermelho abaixo de 90%.
- **Realizado + Carteira (projeção) fica sempre visível como secundário:** extensão clara da
  barra, "% em cinza" ao lado do % colorido, linha própria no KPI com selo.
- **Barra bullet:** trilho cinza = meta · sólido = realizado · claro (35% de opacidade) =
  +carteira · rótulo `x% ▸ y%` · linha de valores embaixo (`Meta 51 mil · Real 19 mil · Cart 16
  mil`) · teto visual de 200% com "↗" além disso · linha tracejada nos 100%.
- **Ordem por volume realizado** (maior para menor) em todos os quadros.
- **Detalhe pai → filho:** executivos abertos em seus clientes (filhos recuados com "·"); a soma
  dos filhos TEM que bater com a linha do pai. Valide sempre.
- **Tudo aberto:** nada de grupo "Outros" escondendo linhas; listas completas com rolagem
  (max-height e overflow-y no card).
- **Conciliação entre quadros é requisito:** a soma dos segmentos de uma marca = a linha da
  marca; valide numericamente antes de entregar (o usuário confere e cobra).
- **Acumulado ano contra ano:** sempre `%` e `= diferença absoluta` juntos; selos de acumulado mês
  a mês acima da curva; destaque "PERFORMANCE NO ANO" no card; linha do tempo do ano anterior ×
  ano atual (duas cores) no ano completo; tabela Ano × meses com Var % do mês, acumulado % e
  diferença.
- **Maiores quedas × maiores crescimentos por cliente**, com status novo ou perdido.
- **Filtros:** TODOS de múltipla escolha (lista com caixas de seleção), mês de referência, troca
  de unidade (Valor R$ / Caixas). Meta indisponível num recorte → "meta n/d", nunca um
  atingimento parcial enganoso.
- **Honestidade nos dados:** tudo o que é estimado ou parcial leva rótulo ("est.", "s/ meta",
  cobertura %, fonte e data no rodapé e nas dicas).

## Identidade visual
Tokens da skill padrao-visual, lidos de `saidas.identidade_visual`, com tema claro e escuro
(declare `color-scheme` nos dois). Números com algarismos tabulares; títulos de card na cor de
texto principal; dicas em cinza itálico. Cabeçalho do painel: título "Acompanhamento de
<Indicador>", saudação "Olá, <organizacao.saudacao>", última atualização e a grade de filtros.

## Engenharia de dados: regras aprendidas (não repetir os erros)
- **Cliente é chaveado pelo CÓDIGO, nunca pelo nome** (a grafia muda entre exports e anos). As
  migrações de código ficam em `clientes.migracoes` e só entram com evidência do histórico
  contínuo na planilha mestre (regras completas na skill identidade-de-clientes).
- **Arbitre fontes divergentes contra uma âncora oficial** (padrão do relatório financeiro):
  quando dois quadros não batem, quantifique cada fonte contra a âncora e troque a fonte ruim; não
  "ajuste" números. Caso real que ensinou a regra: a planilha mestre no nível de marca cobria só
  cerca de 93% do volume, e o relatório financeiro reapresentado confirmou a base de segmentos.
- **Valores fora de escala:** linhas com R$ por caixa acima do limiar
  (`qualidade.outliers_preco.limiar_valor_por_caixa`) são reprecificadas pela mediana do próprio
  SKU; conte e reporte quantas.
- **Histórico × corrente:** `pipeline.corte_historico` separa os meses do fechamento consolidado
  dos meses da base rolante; avance o corte a cada fechamento de mês.
- **Nomes longos:** abrevie para caber no celular pelo nome de exibição da config
  (`clientes.exibicao`; ex.: "DISTRIBUIDORA HORIZONTE LTDA" → "HORIZONTE DISTR. GO", pela UF
  dominante nos dados), propagando o nome também para as metas.

## Detalhes técnicos que custaram horas (leia antes de programar)
- **SVG não se divide entre páginas na impressão:** listas altas viram PDF em branco. Fatie as
  barras em blocos de cerca de 15 linhas (vários SVGs empilhados); nunca remova esse fatiamento.
- **Animação de entrada congela em opacity:0 na impressão:** o `@media print` força
  `animation:none!important;opacity:1!important` nos cards.
- **`.chart-box{max-height:none!important;overflow:visible!important}` na impressão**, senão as
  listas com rolagem saem cortadas.
- **Declare `color-scheme` nos temas**, ou o modo escuro automático do Chrome corrompe as cores.
- **Visualizador de artefatos:** `window.print()`, downloads e publicação pública podem ser
  bloqueados; não gaste tempo, distribua pelo arquivo local e pelos PDFs.
- **Chrome headless** (caminho em `ambiente.binarios.chrome`) respeita o `@page` do CSS; use
  `--virtual-time-budget=8000` para o JS terminar de desenhar.
- **Predefinições no hash** (`#ind=cx&exec=Nome|Nome&wa=1`) geram visões filtradas por script;
  `wa=1` liga o modo retrato de coluna única.
- Rótulo de célula ou texto começando com "=" vira fórmula no Excel: evite.
- O recálculo no LibreOffice precisa do binário de `ambiente.binarios.libreoffice` e de um perfil
  temporário (`-env:UserInstallation=file:///<pasta temporária>`), senão trava se o LibreOffice estiver aberto.

## O leitor da configuração
```bash
python3 scripts/configuracao.py                       # mostra qual configuração está em uso e confere as chaves essenciais
```
Os scripts procuram a configuração em `--config arquivo.yaml`, depois em `SUPER_SKILL_CONFIG`,
`./empresa.yaml`, `~/.super-skill-do-lider/empresa.yaml` e, por último, no exemplo fictício do
plugin. No Python: `carregar`, `obter`, `caminho`, `arquivo` e `nomes_executivos`.

## Como replicar para um indicador novo (ex.: Sell Out, MSL)
1. Leia `references/implementacao-canonica.md` e o protocolo do negócio (`caminhos.cerebro`:
   glossário e fontes por indicador).
2. Copie o gerador e o template do painel de referência para nomes do novo indicador; troque só a camada de extração
   (bases, abas, colunas do indicador) mantendo o formato do JSON (`fat`, `cart`, `metas`,
   referência do ano anterior, `dims`): o template e os PDFs funcionam sem mudança.
3. Valide contra a âncora oficial do indicador (planilha mestre, histórico, relatório financeiro)
   antes de publicar; rode a conciliação pai × filhos e quadro × quadro.
4. Publique o artefato novo, gere o kit do celular, registre a rotina no protocolo do negócio e
   guarde o link fixo em `saidas.artefatos_link_fixo`.

## Integração
As rotinas agendadas (rotina-atualizar-paineis, rotina-foto-do-painel, rotina-pdf-do-painel)
chamam este motor; a skill projecao-e-cenarios lê o `dados_painel.json`; a skill sentinela lê os
números para o briefing; a revisão de saída é da skill revisao-final.
