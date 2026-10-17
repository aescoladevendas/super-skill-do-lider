# Implementação de referência: o painel de Sell In

O painel de Sell In é a implementação de referência do modelo. Tudo vive na pasta
`caminhos.indicadores` do arquivo de configuração; o protocolo de rotina e os cuidados com os
dados ficam no protocolo do negócio (`caminhos.cerebro`), na seção do painel web. Leia os dois
juntos antes de adaptar.

## Mapa de arquivos (nomes do motor da versão 0.2)
| Arquivo | Papel |
|---|---|
| `assets/painel_template.html` | Template do painel (tokens de cor claro e escuro, todos os desenhos em JS, marcador `/*__DATA__*/` onde entra o JSON). É A REFERÊNCIA de layout e de uso: copie daqui. |
| `scripts/gerar_painel.py` | Lê as bases → agrega em `dados_painel.json` → injeta no template → `PAINEL_WEB.html`. Faz a reprecificação de valores fora de escala, a chave por código com as migrações da config, os nomes de exibição e a leitura de metas, RV e referência do ano anterior. |
| `scripts/gerar_pdfs_por_pessoa.py` | Kit do celular: um PDF do GERENTE + um por executivo, via Chrome headless com `#wa=1&ind=cx&exec=...`. |
| `scripts/exportar_pdf_visao.py` | PDF sob demanda com filtros livres (os argumentos são o hash do painel). |
| `scripts/gerar_excel_time.py` | Planilha espelho (mesmo racional e identidade; formato secundário, porque o time prefere os PDFs). |
| `scripts/atualizar_bases.py` | Classifica os exports pelo cabeçalho, faz backup e grava as cópias `BASE_*_ATUAL`. |
| `scripts/recalcular.py` | Recalcula planilhas no LibreOffice headless e lista erros de fórmula. |
| `dados_painel.json` | Contrato de dados do template (abaixo). |
| `caminhos.comunicacao` | Pasta de distribuição (HTML para compartilhar, PDFs, subpasta do celular). |

O link fixo do artefato publicado fica em `saidas.artefatos_link_fixo`: republique SEMPRE no
mesmo link.

## Contrato do JSON (mantenha o formato ao trocar de indicador)
- `dims`: {exec, canal, cat, marca, seg, cli, uf}, listas de nomes; as tuplas usam os índices.
- `fat`: [mes "AAAA-MM", exec, canal, cat, marca, seg, cli, uf, caixas, valor]
- `cart`: [status, exec, canal, cat, marca, seg, cli, uf, caixas, valor]
- `metas`: [mes, exec, CANAL, MARCA, CLIENTE, SEGMENTO, caixas, nr]
- `ref_ano_anterior`: [exec, CANAL, cli, mês 1 do ano corrente, [12 meses do ano anterior]], no
  nível de cliente (planilha mestre)
- `ref_ano_anterior_marca`: [exec, CANAL, cli, MARCA, mês 1 do ano corrente, [12 meses]], no
  nível de marca (relatório financeiro reapresentado)
- `fat_ano_anterior`: como `fat`, com os meses do ano anterior (base de fatura)
- `rv`: por executivo, as missões de RV do mês (Gatilho, NR contra meta, missões de segmento,
  volume) com a meta e o realizado de cada uma
- `atualizado`, `cart_data`, `corrigidas`: metadados que aparecem no rodapé (data da base, data da
  carteira e quantas linhas foram reprecificadas)

A skill projecao-e-cenarios lê este JSON (aceita também os nomes antigos `ref25`, `refM` e
`fat25`, usados no painel de origem).

## Estrutura de cards do painel (ordem atual)
1. Cabeçalho: título, saudação, filtros de múltipla escolha (todos), troca Valor/Caixas, mês de
   referência, limpar.
2. Total da regional (KPI: % realizado grande + linha Realizado + Carteira com selo) ·
   Atingimento por executivo (aberto em clientes) · Atingimento por marca.
3. Composição do fechamento projetado (cascata com a linha da meta) · Atingimento por segmento
   (todos, com rolagem).
4. Indicadores de RV: as missões do mês por executivo.
5. Análise do acumulado do ano: marcas e segmentos (ano atual × anterior, Var % e diferença).
6. Maiores quedas × maiores crescimentos por cliente.
7. Histórico mensal (linhas dos dois anos, selos de acumulado % e diferença, destaque, tabela Ano
   × meses).
8. Rodapé com fontes e notas de honestidade.

## Checklist de adaptação para um indicador novo
1. Identifique as bases e a âncora oficial do indicador (o protocolo do negócio tem o mapa de
   KPIs). Valide os totais da extração contra a âncora ANTES de montar o visual.
2. Duplique gerador e template com nomes novos; troque só a camada de extração.
3. Confira as taxonomias entre fontes (segmentos e nomes mudam): monte o mapa de segmentos e os
   aliases com evidência e deixe "s/ mapa" onde não houver mapeamento seguro.
4. Rode as conciliações: pai × filhos; quadro × quadro; acumulado contra a âncora.
5. Publique o artefato (guarde o link fixo), gere o kit do celular, atualize o protocolo do
   negócio (rotina) e a memória (link e pipeline).
