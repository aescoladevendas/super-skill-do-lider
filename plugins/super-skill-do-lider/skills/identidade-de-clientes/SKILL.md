---
name: identidade-de-clientes
description: Cliente se identifica pelo código, nunca pelo nome. Consolida grupos, filiais, migrações de cadastro e operações por UF. Use ao cruzar bases de clientes ou quando um cliente some e outro nasce.
license: Consulte LICENSE.md na raiz do plugin
metadata:
  versao: "0.1.0"
  pacote: super-skill-do-lider
---

# Identidade de clientes: código, grupo e operação por UF

Regra de negócio que vale para **todo** material da máquina: Excel, PPTX, painel, e-mail e
mensagem. Nenhum número por cliente sai sem passar por ela. Os valores (códigos, migrações,
grupos, nomes de exibição e operações por UF) ficam na seção `clientes` do arquivo de
configuração; esta skill guarda as regras e o script `scripts/identidade_clientes.py`.

## Quando acionar
- Sempre que aparecer qualquer entidade, filial, CNPJ ou código de cliente de um grupo com mais de
  uma operação, em Sell Out, Sell In, positivação, plano de negócios ou painel.
- Ao cruzar bases de fontes diferentes (ERP da empresa, sistema de dados do distribuidor,
  relatório próprio do distribuidor, painel de varejo, base histórica).
- Quando um cliente "some" e outro "nasce" no mesmo período, ou quando o usuário pedir "o
  conceito do grupo por estado", "consolidar o grupo", "separar o atacado" ou a história do
  negócio de um grupo.

## Parte 1 · As regras de identidade (valem para qualquer cliente)

1. **A chave é o CÓDIGO do cliente no ERP, nunca o nome** (`clientes.chave` e
   `clientes.coluna_codigo`). A grafia do nome muda entre exports e entre anos; o código não.
2. **Migração de código é alias, e alias só com evidência.** Mesmo relacionamento comercial com
   cadastro novo vira uma linha em `clientes.migracoes` (de, para, vigência, evidência). A
   evidência exigida: no histórico contínuo, um código para de faturar exatamente quando o outro
   começa, com volume parecido.
3. **Investigação obrigatória antes de falar em perda ou ganho de carteira.** Cliente que zera
   enquanto outro nasce com volume parecido é suspeita de troca de código. O script lista os
   pares suspeitos (`--suspeitas`); só depois de checar é que se reporta "perdemos" ou
   "ganhamos" um cliente.
4. **Grupo econômico se analisa somado.** Códigos que são a mesma operação (duas entidades
   jurídicas paralelas, matriz e satélite, dois códigos para o mesmo distribuidor) ficam em
   `clientes.merges_grupo` e nunca são lidos isoladamente; usar só um dos códigos dá, por
   exemplo, um MSL falso e baixíssimo.
5. **Nome de exibição único em todos os materiais** (`clientes.exibicao`), abreviado para caber no
   celular e propagado também para as metas. Prefixos técnicos de relatório (`clientes.prefixos_remover`)
   saem do nome antes de exibir.
6. **Cliente final do distribuidor não se consolida com ele.** Quem compra DO distribuidor é
   comprador a jusante; prove pelo relatório de sell out do próprio distribuidor antes de decidir
   (`clientes.casos_especiais`).

## Parte 2 · Grupo com várias operações por UF (as "caixas")

Alguns grupos (no exemplo, a Distribuidora Horizonte) têm várias áreas de distribuição
contratadas, uma por UF. Tudo o que fatura para UF fora das contratadas é **atacado**. A
configuração (`clientes.grupos_por_uf.<grupo>`) define:

| Campo | O que é | Exemplo fictício |
|---|---|---|
| `ufs_distribuicao` | UFs com área de distribuição contratada | GO, MS, TO, PA |
| `caixas` | nomes de saída, exatamente como aparecem nos materiais | HORIZONTE DISTR. GO, ... MS, ... TO, ... PA, HORIZONTE ATACADO |
| `caixa_atacado` | a caixa de tudo o que está fora das UFs contratadas | HORIZONTE ATACADO |
| `recorte_da_area` | as caixas que entram na área do gerente | GO, MS e TO (PA é contrato do grupo mas fica fora da área) |
| `fontes` | como reconhecer cada caixa em cada fonte (trecho do texto → caixa) | filial "GO - Cidade" → DISTR. GO |

A nomenclatura de saída é sempre a da config, com ponto e espaço iguais, para casar com a
estrutura do BI da empresa.

### As duas camadas da regra
**Camada 1, por entidade.** Classifica pela filial ou pelo código de origem. É a que se aplica
sempre, em qualquer base.

**Camada 2, por UF do PDV.** Dentro de uma caixa de distribuição, o faturamento para PDV de UF
fora das contratadas é atacado. Importa porque uma operação pode carregar historicamente PDVs de
outros estados (no caso real que originou a regra, mais de um terço de uma caixa não era da UF dela).
Só aplique quando a base tiver a UF do PDV confiável; sem UF confiável, fique na camada 1 e
registre a ressalva.

### Como classificar em cada fonte
O script lê as regras de `fontes` da config, na ordem: a primeira regra cujo trecho aparece no
texto da coluna define a caixa; nada casou, vale `resto` (o atacado). Três tipos de fonte são
previstos no exemplo:
- **sistema de dados do distribuidor** (uma linha por filial, coluna `filial`);
- **relatório próprio do distribuidor** (coluna `DISTRIBUIDOR`, com siglas por UF);
- **base oficial da empresa** (código ou nome do cliente no ERP). Se a cobertura dessa base for
  amostral, use para tendência e não para volume absoluto.

## Ressalvas obrigatórias em qualquer entregável
1. **Meça a UF do PDV antes de usar a camada 2.** Calcule a fatia do faturamento com UF em branco
   em cada fonte. Se for relevante (no caso real passou de dois terços em um mês), nunca leia o
   grupo por UF do PDV naquela fonte: classifique pela filial.
2. **Não some positivação entre caixas.** O mesmo PDV compra de mais de uma operação. Use contagem
   distinta de CNPJ dentro de cada caixa e informe a interseção quando somar.
3. **Comparabilidade.** Se o grupo só entra numa fonte a partir de certo mês, qualquer comparação
   ano contra ano de um total que o inclua é inválida. Mantenha sempre a coluna "base comparável",
   sem o grupo.
4. **Recorte explícito.** Diga sempre qual recorte está sendo somado: as caixas do
   `recorte_da_area`, o contrato inteiro do grupo ou a leitura de atacado.

## Qual fonte usar para cada período
Use a fonte que tem histórico para o passado e a fonte completa e diária para o período corrente,
e escreva a troca na aba LEIA-ME. Antes de emendar as duas, faça a **validação cruzada nos meses
sobrepostos**, caixa a caixa: registre onde batem quase exatos, onde uma fonte zera por falha de
carga e onde uma caixa está sub-representada (no caso real, o relatório do distribuidor só passou
a capturar uma das filiais de uma UF depois de certo mês e, antes disso, registrava uma fração do
volume). Feche com a convergência do total nos meses em que as duas fontes estão completas.

## Como extrair
Uma dimensão de linha por consulta: a filial (ou o código) na linha e o mês na coluna, com três
medidas: valor líquido (soma), quantidade (soma) e clientes distintos (contagem distinta). Exporte
cada consulta e guarde o arquivo bruto junto do entregável.

## O script
`scripts/identidade_clientes.py` (lê a config pelo `configuracao.py` da mesma pasta):

```bash
python3 scripts/identidade_clientes.py --teste                     # confere as regras da config com casos de exemplo
python3 scripts/identidade_clientes.py --classificar base.csv \
        --grupo distribuidora_horizonte --fonte sistema_do_distribuidor \
        [--coluna-uf uf_pdv] --saida base_classificada.csv          # acrescenta a coluna "caixa" (camadas 1 e 2)
python3 scripts/identidade_clientes.py --suspeitas serie.csv        # pares de códigos com cara de troca de cadastro
```
No Python: `resolver_codigo`, `chave_grupo`, `nome_exibicao`, `caixa`, `caixa_por_uf_pdv` e
`suspeitas_troca_de_codigo`.

## Entregável padrão
Abas mínimas: LEIA-ME com as ressalvas · série mensal por caixa (R$, caixas e positivação) ·
comparativo entre as fontes nos meses sobrepostos · a caixa de atacado separada · diagnóstico.
Visual da skill padrao-visual; zero travessão; revisão da skill revisao-final antes de sair.
