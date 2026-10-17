---
name: plano-de-negocios-com-cliente
description: Deck C-level de diagnóstico e plano conjunto de negócios para conta do atendimento direto. Use quando pedirem "plano de negócios do cliente X", "JBP da rede" ou "material C-level do cliente".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

> **VISUAL:** cores, fontes, fundo e cards seguem a skill padrao-visual (tokens em
> `saidas.identidade_visual`: fundo claro, cards brancos arredondados sem sombra, cor de
> destaque da empresa só no mandatório, Arial no Office). Desta skill vale a estrutura e a
> lógica de conteúdo.

# Plano de negócios com o cliente

Deck de diagnóstico executivo C-level e plano conjunto de negócios (Joint Business Plan, JBP)
para contas do atendimento direto (redes e clientes com executivo dedicado), com Excel de
suporte. Modelo validado com uma rede regional de três lojas; o deck real ficou fora do
pacote. A base de Sell Out da rede vem da skill diagnostico-de-rede.

## Identidade visual
- Chassi = padrao-visual. Formato 13,333 x 7,5 pol.
- Identidade do cliente preservada nos momentos do cliente: logo oficial dentro de um "chip"
  com a cor primária da marca do cliente (capa e fechamento), anos da linha do tempo na cor
  do cliente, fotos das lojas. Buscar logo, cores e história no site oficial do cliente;
  extrair a cor dominante do logo com PIL. Sem logo, chip com o nome do cliente na cor
  `plano_de_negocios.cor_cliente_padrao`.
- Capa clara com faixa de destaque inferior; fechamento escuro com o número-síntese na cor de
  destaque.

## Estrutura do deck (18 slides; adaptar blocos conforme o dado disponível)
1. **Capa**: sobretítulo "DIAGNÓSTICO EXECUTIVO · <tema>", título grande, chip do cliente,
   faixa com período e autoria.
2. **Quem é o cliente**: história e linha do tempo (anos na cor do cliente), fotos das lojas,
   posicionamento. Fonte: site institucional.
3. **Por que este material existe**: o marco (ex.: primeira vez com Sell Out compartilhado) e
   o card "O LIMITE ATUAL" com a honestidade do dado.
4. **Números-chave**: 4 cards de KPI, caixa "A LEITURA" e gráfico de rosca do mix por marca.
5. **Marcas**: barras agrupadas ano anterior x ano corrente (anterior em cinza, corrente na
   cor de destaque) e painel DESTAQUES com a variação colorida.
6 a 8. **Um slide por marca relevante**: motor, apostas, ponto de atenção. Padrão: 4 cards de
   KPI e caixa com 3 parágrafos (diagnóstico → insight → **Ação:** na cor de destaque).
9. **Portfólio vivo**: entradas x saídas de SKUs (R$ ganho x perdido).
10. **Segmentos**: linhas com variação colorida e faixa de leitura.
11. **MSL e execução**: fonte = relatório de execução (MSL) do BI da empresa, filtrando
    gerente e rede. KPIs: MSL % da auditoria, MSL 12 meses, % de inovação, visitação; gráfico
    de linha mensal; tabela por categoria; SKUs reprovados nominais.
12. **Espaço de gôndola (share of shelf)**: barras horizontais com delta contra o ano
    anterior; apontar o espaço em branco (categoria com espaço baixo).
13. **Sell In x Sell Out**: barras mensais de Sell In contra a meta oficial revisada; carteira
    aberta; leitura cruzada (ex.: desestocagem = Sell Out muito acima do Sell In com gôndola
    saudável). Fonte: o contrato de dados do painel (`arquivos.dados_painel`, skill
    painel-de-indicadores). Conferir a ordem das colunas da linha de faturamento antes de
    filtrar o cliente (no layout de referência: mês, executivo, canal, categoria, marca,
    segmento, CLIENTE, UF, caixas, valor; o cliente é a 7ª posição).
14. **Alavancas de execução**: o que o BI mostra e a conta ainda não usa (ponto extra, preço
    auditado, gap de inovação) e faixa "pacote de execução".
15. **Projeção mensal jan a dez, ano anterior x ano corrente**: anterior em cinza, corrente na
    cor de destaque (realizado sólido, meses futuros = desafio HACHURADO com borda de
    destaque), linha pontilhada separando REALIZADO | DESAFIO, 3 cards (ano anterior, alvo do
    ano, desafio restante). Se a base vier em blocos acumulados, usar a média mensal do bloco
    e ESCREVER NOTA DE DADO no slide.
16. **Síntese executiva**: 3 colunas (forte, pede ação, pedir ao cliente).
17. **Próximos passos**: 5 linhas com número em destaque, ação, descrição, DONO e PRAZO.
18. **Fechamento**: fundo escuro, frase-síntese, número do ano na cor de destaque.

## Storytelling (arco fixo)
Contexto e confiança → prova de crescimento → onde cresce e por quê (marcas) → o alerta
honesto (nunca esconder a marca em queda) → a execução comprova ou absolve → tamanho do
desafio → plano com dono e prazo. Uma ideia por slide; todo bloco termina em recomendação
(skill apresentacao-executiva). Português de negócio, sem jargão. Números pt-BR
("R$ 1,48 Mi", "+22,4%").

## Regras de dado (inegociáveis)
- **Cada plano fala só do próprio cliente; nunca comparar com outras redes** ("são redes
  diferentes"). Achado entre contas (ex.: SKU com gap sistêmico na região) é pauta interna da
  empresa, não entra em material de cliente. Nem no nome do arquivo.
- **Todos os números em R$ ou em CAIXAS; nunca em unidades.**
- **Sell Out sempre da operação de varejo (lojas) do cliente** (ex.: painel de varejo das
  lojas); nunca misturar sell out do atacado; rotular a operação na fonte.
- **Uma régua de mês só por gráfico** (mês de trânsito x data de fatura): escolher uma série
  consistente nos dois anos e conferir que a soma fecha com o painel oficial.
- Bases de rede costumam ter LINHA DE TOTAL embutida (SKU vazio): filtrar antes de somar,
  senão dobra tudo.
- Nunca inventar abertura mensal ou sazonalidade que a base não tem: usar média de bloco com
  nota de dado explícita no slide e registrar "pedir abertura mensal" como próximo passo.
- Checar o rótulo de filtro do BI (ex.: "Fabricante: Tudo" = mercado total, não a empresa)
  antes de atribuir crescimento à empresa.
- Excel de suporte com FÓRMULAS (SOMASE por marca e segmento e linha "Demais" para o total
  fechar exato) e recálculo no LibreOffice até zero erro. Armadilha: `insert_rows` do
  openpyxl NÃO ajusta fórmulas.

## Ferramentas e QA
- Montar o deck com python-pptx (skill pptx do Claude). Gráficos em matplotlib (Agg), Arial,
  grade `plano_de_negocios.cor_grade`, sem bordas de cima e da direita; salvar PNG a 200 dpi
  fora do plugin e inserir como imagem.
- QA obrigatória: LibreOffice headless → PDF → PyMuPDF → inspeção visual de TODAS as páginas
  (subagente para o deck completo). Vigiar: caixas superdimensionadas (espaço morto), tabela
  estourando o quadro ao ganhar coluna, rótulo de gráfico atrás de barra. Pptx com imagem
  nova: validar o content_type com python-pptx. Revisão final pela skill revisao-final.
- Entrega: `caminhos.compartilhada/<plano_de_negocios.subpasta_compartilhada>` e
  `caminhos.clientes/<cliente>/<plano_de_negocios.subpasta_cliente>`; scripts adaptados em
  `caminhos.scripts`; entrada datada em `caminhos.log_entregas`; abrir o deck no PowerPoint
  ao final.
