# Motor de projeção: detalhe e exemplo numérico

Exemplo fictício, reproduzível: dados de teste do caso da Distribuidora Horizonte, mês alvo
setembro de 2026, base com 11 de 21 dias úteis de agosto faturados. Todos os parâmetros vêm da
seção `projecao` do arquivo de configuração.

## Passos por cliente (Rede Exemplo Norte, código 100201)
| Passo | Fórmula | Exemplo |
|---|---|---|
| mês fechado (jul) | painel | 11.599 |
| mês em curso parcial (ago) | painel, 11 de 21 dias úteis | 4.955 |
| mês em curso projetado | parcial >= 0,9 × fechado → = parcial; senão min(parcial × 21 ÷ 11, maior mês do ano) | 4.955 < 10.439 → min(9.460; 12.039) = 9.460 |
| ritmo curto | média(fechado, em curso projetado) | 10.530 |
| ritmo longo | média de fev a jul (positivos) | 10.976 |
| BASE | 50% curto + 50% longo | 10.753 |
| sazonalidade | set do ano anterior ÷ média(jul, ago) do ano anterior, entre 0,6 e 1,4 | 17.001 ÷ 12.533 = 1,36 |
| ESTABILIZAÇÃO | BASE × sazonalidade | 14.586 |
| QUEDA / CRESCIMENTO | × 0,9 / maior entre × 1,075 e o necessário para o acumulado +7,5%, teto 1,5× ou a meta | 13.127 / 21.879 (bateu no teto) |
| regras de evidência | carteira 4.000 (piso de 60% = 2.400, abaixo da estabilização); sem régua de trimestre | sem ajuste |
| PROJEÇÃO | | **14.586** (110% da meta de 13.200) |
| mix por marca | três últimos meses do cliente: 74/20/3/3 | Marca X 10.793 · Marca Y 2.917 · Marca Z 438 · Marca W 438 |

Outros casos da mesma rodada:
- **Distribuidora Horizonte (100101), mês feito.** Agosto parcial de 41.000 já passou de 90% de
  julho (32.944), então o mês em curso não se extrapola. Ritmo curto 36.972, longo 31.416, base
  34.194, sazonalidade 1,15 → estabilização e projeção de 39.377 (102% da meta de 38.500).
- **Horizonte MS (100102), mês em curso zerado e régua do trimestre.** Agosto sem pedido e julho de
  5.211: a base fica limitada ao mês fechado e a estabilização dá 4.205. A conta tem régua de
  verba: 85% da meta do trimestre (27.000) menos julho, agosto e carteira (9.000) deixa um gap de
  8.739, maior que a estabilização; a projeção sobe até o teto de 1,3× (5.466), que também passa
  do piso de 60% da carteira (5.400).

Total da rodada: projeção de 87.672 caixas, 102% da meta de 85.800; BE final depois do ajuste
colaborativo de -10%: cerca de 78.905 (92%).

## Cenários no total da regional (mesma rodada)
QUEDA 77.769 · ESTABILIZAÇÃO 86.410 · CRESCIMENTO 126.990 · carteira aberta 55.000. Leia sempre os
três contra a meta e contra o mesmo mês do ano anterior.

## Pouso do trimestre e acumulado do ano (estrutura da conta)
- **Trimestre** = 1º mês fechado + 2º mês projetado (parcial + a fração da carteira que fatura no
  mês; dê uma faixa) + 3º mês (entre o BE final e a projeção cheia). Exemplo ilustrativo: 100 mil +
  cerca de 95 mil + cerca de 98 mil = cerca de 293 mil contra a meta de 270 mil → +23 mil (109%).
- **Acumulado do ano** = gap do semestre (use a âncora do usuário, ex.: -90 mil) + Δ do trimestre →
  -67 mil (gap no fim do trimestre); % recuperado do buraco = 23 ÷ 90 = 26%; e o ano contra ano no
  mesmo intervalo de meses.
- **Trimestre seguinte**: caixas acima da régua para fechar 100% no ano = gap acumulado ÷ 3 por
  mês; ambição de +7,5% sobre o ano anterior (ex.: 1.000 mil → 1.075 mil) → trimestre necessário =
  1.075 mil menos o acumulado até aqui. Quando o necessário estiver fora do alcance (muito acima do
  melhor trimestre do ano), diga isso com todas as letras.

## Saídas
- Na pasta de comunicação (`caminhos.comunicacao`): a cópia do arquivo oficial com o sufixo de
  `projecao.arquivo_be.sufixo_saida`, com a aba `PROJECAO_<mês>` de memória (Executivo, Cliente,
  Código, Meta, Mês fechado, Mês em curso parcial e projetado, Média de 6 meses, Sazonalidade, Mês
  alvo no ano anterior, Carteira, QUEDA, ESTABILIZAÇÃO, CRESCIMENTO, PROJEÇÃO, Δ, % da meta, uma
  coluna por marca e Observações) e o RESUMO dos cenários. Sem o arquivo oficial, sai só a planilha
  de memória.
- Cópia na pasta compartilhada do time (`caminhos.compartilhada`), na subpasta de metas e cenários.
- Abrir a planilha, falar o resumo e escrever as tabelas na resposta.
