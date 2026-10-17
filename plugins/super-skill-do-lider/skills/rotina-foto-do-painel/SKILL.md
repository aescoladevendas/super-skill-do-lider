---
name: rotina-foto-do-painel
description: Rotina diária que gera o PDF das abas completas da planilha mestre (painel e carteira) para o grupo do time, sem alterar o original. Use no horário agendado ou quando pedirem "update".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Rotina: a foto diária do painel

Gere a atualização diária do Sell In em PDF. Sempre que o usuário pedir "update" do arquivo
diário, execute este mesmo procedimento na hora, e não apenas no horário agendado.

## Contexto
- O único arquivo de trabalho é a planilha mestre (`arquivos.painel_master`, na pasta
  `caminhos.indicadores`). O usuário atualiza esse arquivo diretamente. Peça acesso à pasta
  `caminhos.raiz` se ela não estiver montada. Nunca use cópias em cache nem versões antigas
  arquivadas da planilha.
- Nesta versão 0.1 os scripts do motor ainda não vêm no pacote (entram na 0.2, na pasta `scripts/` da skill painel-de-indicadores, com os nomes citados abaixo); até lá, a rotina roda os scripts equivalentes que o usuário guardou em `caminhos.scripts`.

## Passos
1. Rode `python3 <scripts do motor>/gerar_pdf_abas_completas.py`. O script SEMPRE trabalha numa
   cópia temporária (nunca altera a planilha mestre), recalcula as fórmulas no LibreOffice
   headless e gera o PDF de `arquivos.pdf_abas_completas` com as duas abas completas (painel e
   carteira), preservando cores, fontes e layout do modelo, além de imagens auxiliares que não
   precisam ser apresentadas. Se faltar dependência Python (pypdf, openpyxl, PyMuPDF), instale com
   `pip install <pacote>`.
2. Abra e confira visualmente o PDF gerado: legível, sem texto sobreposto e com as cores do
   modelo (cabeçalho escuro, verde e vermelho nas variações).
3. Apresente ao usuário SOMENTE estes dois arquivos, nesta ordem: o PDF das abas completas e a
   planilha mestre (só para leitura e conferência; NÃO a modifique nesta tarefa). Não apresente
   as imagens auxiliares.
4. Mensagem para o gerente (só se `saidas.mensageiro.ativo` for verdadeiro e o conector estiver
   disponível): mensagem direta para o próprio usuário com o título "🗞️ Foto diária do painel ·
   <data>" e um resumo dos números principais lidos da cópia recalculada (totais da aba do painel
   e TOTAL da carteira: meta, realizado, %, carteira atual). Se o conector não aceitar arquivo,
   não tente anexar o PDF: ele segue entregue na conversa. Sem conector, siga normalmente e
   registre que a mensagem não foi enviada.
5. NÃO altere a planilha mestre nesta tarefa: só leia e recalcule cópias temporárias. NÃO envie
   nada automaticamente por WhatsApp ou e-mail: gere e deixe os arquivos prontos para o usuário
   enviar.
6. Responda de forma breve confirmando que o PDF e a planilha estão com a data de hoje e se a
   mensagem saiu, ou diga objetivamente o que falhou.

## Como agendar
Tarefa agendada diária (no aplicativo do Claude ou no Claude Code) com o texto "rode a skill
rotina-foto-do-painel", depois do horário da rotina-atualizar-paineis.
