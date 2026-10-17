---
name: rotina-pdf-do-painel
description: Rotina diária e silenciosa que gera o PDF do painel em formato de cartão vertical para celular, com os KPIs gerais do mês. Use no horário agendado ou em "PDF do painel de hoje".
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Rotina: o PDF diário do painel para o celular

Gere o PDF diário do painel de Sell In no formato de cartão vertical (o formato de status de
aplicativo de mensagem), pronto para o gerente mandar ao time.

## Contexto
- A planilha mestre (`arquivos.painel_master`, em `caminhos.indicadores`) tem uma aba de painel
  cuja linha de KPIs gerais já vem calculada por fórmula: meta, realizado, % de atingimento,
  carteira + processo, realizado + carteira, % realizado + carteira, acumulado do ano anterior,
  acumulado do ano, variação absoluta e variação % do acumulado. A aba e as células ficam
  declaradas no arquivo de configuração.
- Nesta versão 0.1 os scripts do motor ainda não vêm no pacote (entram na 0.2, na pasta `scripts/` da skill painel-de-indicadores, com os nomes citados abaixo); até lá, a rotina roda os scripts equivalentes que o usuário guardou em `caminhos.scripts`.
- O script `gerar_pdf_resumo.py` lê essa planilha, recalcula as fórmulas no LibreOffice headless,
  extrai os KPIs e gera o cartão vertical em `arquivos.pdf_resumo` (sobrescrevendo o anterior).

## Passos
1. Localize a pasta dos scripts e rode `python3 <scripts do motor>/gerar_pdf_resumo.py`. Se faltar
   alguma dependência Python ou o LibreOffice, instale ou siga se já estiver presente.
2. Confirme que o PDF foi atualizado (data de modificação e tamanho).
3. Não peça confirmação ao usuário nem envie o PDF por nenhum canal: só gere e salve o arquivo
   atualizado na pasta. Não envie mensagens, não publique nada.
4. Responda em uma ou duas frases confirmando que o painel foi atualizado com os números do dia
   (cite meta, realizado e % de atingimento do mês), ou diga objetivamente o que falhou (planilha
   não encontrada, script ausente).

Não faça mais nada além disso: é uma tarefa silenciosa de atualização de arquivo.

## Como agendar
Tarefa agendada diária com o texto "rode a skill rotina-pdf-do-painel", depois da
rotina-atualizar-paineis.
