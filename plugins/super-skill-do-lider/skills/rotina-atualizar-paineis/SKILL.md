---
name: rotina-atualizar-paineis
description: Rotina agendada que pega os exports do sistema (realizado e carteira), padroniza as bases, recalcula as planilhas e atualiza os painéis. Use em "subi as bases", "atualiza os painéis".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Rotina: atualizar os painéis com as bases novas

Alimenta todos os painéis do indicador de Sell In com até três bases (realizado, carteira aberta
e carteira resumo), detectadas pelo cabeçalho. Não mexe em Sell Out nem nos volumes mensais
consolidados da planilha mestre. Nesta versão 0.1 os scripts do motor ainda não vêm no pacote (entram na 0.2, na pasta `scripts/` da skill painel-de-indicadores, com os nomes citados abaixo); até lá, a rotina roda os scripts equivalentes que o usuário guardou em `caminhos.scripts`.

## Contexto (autossuficiente)
- Pasta do projeto: `caminhos.raiz` do arquivo de configuração (peça acesso se não estiver
  montada). Leia primeiro o protocolo do negócio em `caminhos.cerebro`.
- O usuário sobe ATÉ TRÊS ARQUIVOS (ordem habitual: primeiro o realizado, depois a carteira). O
  script detecta o tipo pelo CONTEÚDO do cabeçalho, conforme `contratos_entrada`:
  * REALIZADO: tem as colunas de `contratos_entrada.realizado.assinatura` (caixas faturadas e mês
    GIT);
  * CARTEIRA EM ABERTO: tem a coluna de caixas da carteira e NÃO tem a de caixas faturadas;
  * CARTEIRA RESUMO: o cabeçalho começa com `contratos_entrada.carteira_resumo.assinatura_inicio`.
- Fonte dos arquivos: os anexados na conversa; senão, os exports mais recentes da pasta
  `caminhos.entrada` (valide o cabeçalho de cada um e use no máximo um de cada tipo).

## Passos
1. Rode `python3 <scripts do motor>/atualizar_bases.py <arq1> [arq2] [arq3]`. Ele classifica,
   faz backup em `caminhos.backups`, guarda as cópias `BASE_*_ATUAL.xlsx` (nomes em `arquivos`) e
   alimenta as planilhas de trabalho declaradas na configuração (MSL, BI do trimestre, RV e a aba
   CARTEIRA da planilha mestre), com casamento pelo CÓDIGO do cliente e fórmulas preservadas.
2. Verifique: recalcule cópias com `recalcular.py` (LibreOffice headless) e confira que a soma do
   NR realizado no controle de RV do período bate com o NR do período na base de realizado.
   Reporte os valores por executivo e o TOTAL da carteira da planilha mestre. Rode em seguida
   `gerar_painel.py` para republicar o painel web e o JSON.
3. NUNCA altere os volumes mensais consolidados da planilha mestre com base rolante: só com base
   mensal completa e a pedido explícito. NUNCA toque em nada de Sell Out (base separada); o bloco
   do canal indireto do MSL fica intocado.
4. Responda com um resumo curto: tipo detectado de cada arquivo, linhas, caixas e R$ por mês de
   fatura, linhas escritas em cada planilha, clientes de carteira atualizados e pendências
   (clientes sem linha na planilha), e o resultado da verificação.
5. Mensagem para o gerente (só se `saidas.mensageiro.ativo` for verdadeiro e o conector
   estiver disponível): mensagem direta para o próprio usuário no canal de
   `saidas.mensageiro.canal`, com foco no BI do trimestre:
   * título: "📊 BI do trimestre · Sell In atualizado <data>";
   * volumes por mês de fatura (caixas e R$);
   * VOLUME EM CAIXAS do período (o período do mês GIT) no TOTAL e POR EXECUTIVO (tabela executivo
     × caixas, do maior para o menor), conforme a aba de realizado do BI;
   * linhas escritas no realizado e na carteira do BI;
   * verificação RV × BI (✅ ou ⚠️);
   * SEMPRE no final, os links `file://` dos arquivos atualizados, com o caminho real na máquina
     do usuário (nunca o caminho de uma área temporária).

   Se o conector não estiver disponível, registre no resumo que a mensagem não foi enviada: isso
   não é erro da atualização.
6. Pedido permanente: SEMPRE incluir, no final de QUALQUER resumo desta rotina (na mensagem e na
   resposta da conversa), os links `file://` dos arquivos atualizados, com o caminho real.

## Como agendar
Crie uma tarefa agendada (no aplicativo do Claude ou no Claude Code) com o texto "rode a skill
rotina-atualizar-paineis com os exports mais recentes", no horário em que os exports costumam
chegar. A rotina também roda sob demanda quando o usuário diz "subi as bases".

## Integração
Motor da skill painel-de-indicadores; regras de cliente da skill identidade-de-clientes; os PDFs
do dia saem pelas skills rotina-foto-do-painel e rotina-pdf-do-painel.
