# -*- coding: utf-8 -*-
"""Leitura do arquivo de configuração da empresa (o "cérebro" em YAML).

Todos os scripts do motor leem caminhos, pessoas, clientes, marcas, metas e regras
daqui, em vez de constantes no código. A regra do motor fica marcada [ENGINE] no YAML;
o dado da empresa fica marcado [TENANT].

Ordem de busca do arquivo (vale o primeiro que existir):
  1. caminho passado em --config ou para carregar(caminho)
  2. variável de ambiente SUPER_SKILL_CONFIG
  3. ./empresa.yaml (pasta onde o comando foi rodado)
  4. ~/.super-skill-do-lider/empresa.yaml
  5. config/exemplo_empresa.yaml do próprio plugin (o exemplo fictício)

Uso nos scripts:
    from configuracao import carregar, obter, caminho
    cfg = carregar()
    gerente = obter(cfg, 'organizacao.gerente')
    pasta = caminho(cfg, 'caminhos.indicadores')

Rodar sozinho mostra qual arquivo está em uso e confere as chaves essenciais:
    python3 configuracao.py [--config arquivo.yaml]
"""
import os, sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit('Falta o pacote PyYAML: rode  pip install pyyaml')

ESSENCIAIS = ['meta.empresa', 'caminhos.raiz', 'organizacao.gerente', 'organizacao.executivos',
              'clientes.chave', 'produtos.marcas_foco']


def _do_plugin():
    pasta = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        cand = os.path.join(pasta, 'config', 'exemplo_empresa.yaml')
        if os.path.isfile(cand):
            return cand
        pasta = os.path.dirname(pasta)
    return None


def localizar(caminho_arquivo=None):
    if caminho_arquivo is None and '--config' in sys.argv:
        i = sys.argv.index('--config')
        if i + 1 < len(sys.argv):
            caminho_arquivo = sys.argv[i + 1]
    candidatos = [caminho_arquivo, os.environ.get('SUPER_SKILL_CONFIG'),
                  os.path.join(os.getcwd(), 'empresa.yaml'),
                  os.path.expanduser('~/.super-skill-do-lider/empresa.yaml'), _do_plugin()]
    for c in candidatos:
        if c and os.path.isfile(os.path.expanduser(c)):
            return os.path.abspath(os.path.expanduser(c))
    raise FileNotFoundError('Nenhum arquivo de configuração encontrado. Copie '
                            'config/exemplo_empresa.yaml para ~/.super-skill-do-lider/empresa.yaml '
                            'e preencha com os dados da sua operação.')


def carregar(caminho_arquivo=None):
    arq = localizar(caminho_arquivo)
    with open(arq, encoding='utf-8') as fh:
        cfg = yaml.safe_load(fh) or {}
    cfg['_arquivo'] = arq
    return cfg


def obter(cfg, chave, padrao=None):
    """obter(cfg, 'a.b.c') devolve cfg['a']['b']['c'] ou o padrão."""
    atual = cfg
    for parte in chave.split('.'):
        if isinstance(atual, dict) and parte in atual:
            atual = atual[parte]
        else:
            return padrao
    return atual


def caminho(cfg, chave, padrao=None):
    """Resolve um caminho do YAML: expande ~ e os marcadores {raiz}, {indicadores} etc."""
    valor = obter(cfg, chave, padrao)
    if valor is None:
        return None
    pastas = obter(cfg, 'caminhos', {}) or {}
    for _ in range(4):  # marcadores podem apontar para outros marcadores
        for k, v in pastas.items():
            if isinstance(v, str):
                valor = valor.replace('{' + k + '}', v)
    return os.path.abspath(os.path.expanduser(valor))


def arquivo(cfg, nome_chave, pasta_chave='caminhos.indicadores'):
    """Caminho completo de um arquivo da seção 'arquivos' dentro de uma pasta da seção 'caminhos'."""
    nome = obter(cfg, 'arquivos.' + nome_chave)
    if nome is None:
        raise KeyError(f'arquivos.{nome_chave} não está no arquivo de configuração')
    if os.path.isabs(os.path.expanduser(nome)) or nome.startswith('{'):
        return caminho(cfg, 'arquivos.' + nome_chave)
    return os.path.join(caminho(cfg, pasta_chave), nome)


def nomes_executivos(cfg):
    return [e['nome'] for e in obter(cfg, 'organizacao.executivos', []) or []]


def conferir(cfg):
    faltam = [k for k in ESSENCIAIS if obter(cfg, k) in (None, '', [])]
    return faltam


if __name__ == '__main__':
    c = carregar()
    print('Configuração em uso:', c['_arquivo'])
    print('Empresa:', obter(c, 'meta.empresa'), '| gerente:', obter(c, 'organizacao.gerente'),
          '| executivos:', ', '.join(nomes_executivos(c)))
    f = conferir(c)
    print('Chaves essenciais:', 'todas presentes' if not f else 'FALTAM ' + ', '.join(f))
    sys.exit(1 if f else 0)
