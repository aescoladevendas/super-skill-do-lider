# -*- coding: utf-8 -*-
"""Gera do zero o template do book executivo (assets/template-base.pptx) com python-pptx.

O que faz: monta os 11 slides fixos do book (capa, agenda de 5 itens, 4 pares divisor +
conteúdo, fechamento), todos com placeholders genéricos entre colchetes. Os 4 slides de
conteúdo saem do próprio build_content_slide.py, então template e gerador nunca divergem.
Depois limpa o pacote: sem miniatura, sem configuração de impressora e com as propriedades
do documento (título, autor, lista de títulos) genéricas.

Entradas: caminho de saída (opcional) e --config arquivo.yaml (opcional: cores e fonte de
saidas.pptx_executivo).
Saídas: o .pptx (padrão: ../assets/template-base.pptx, ao lado desta pasta de scripts).
Rodar:
    python3 scripts/gerar_template.py
    python3 scripts/gerar_template.py /outra/pasta/template-base.pptx
"""
import datetime
import os
import re
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from build_content_slide import PALETA, escrever_no_slide  # noqa: E402

from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN  # noqa: E402
from pptx.util import Emu, Pt  # noqa: E402

TOTAL = 11
LARGURA, ALTURA = 12192000, 6858000
ESCURO_FANTASMA = "51697B"     # número gigante do divisor
TEXTO_SOBRE_ESCURO = "DEE5EA"  # subtítulos e rodapé sobre o fundo slate
RODAPE = "[Empresa] · [Nome do Book] · [Período]"
ASSINATURA = "[Empresa] · Gerência [Nome] · [Mês/Ano]"
ALINHA = {"l": PP_ALIGN.LEFT, "r": PP_ALIGN.RIGHT, "ctr": PP_ALIGN.CENTER}


def cor(c):
    return RGBColor.from_string(PALETA.get(c, c))


def caixa(slide, x, y, w, h, texto, sz, c, bold=False, spc=None, algn="l", ancora="t", entre_linhas=None):
    """caixa de texto sem margem, que cresce com o texto (como no template original)."""
    tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE if ancora == "ctr" else MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = ALINHA[algn]
    if entre_linhas:
        p.line_spacing = entre_linhas
    r = p.add_run()
    r.text = texto
    f = r.font
    f.size = Pt(sz / 100)
    f.bold = bold
    f.italic = False
    f.name = PALETA["fonte"]
    f.color.rgb = cor(c)
    if spc:
        r._r.get_or_add_rPr().set("spc", str(spc))
    return tb


def retangulo(slide, x, y, w, h, c, borda=None):
    """retângulo chapado, sem sombra; borda fina opcional."""
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = cor(c)
    if borda:
        sh.line.color.rgb = cor(borda)
        sh.line.width = Emu(9525)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def fundo(slide, c):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = cor(c)


def rodape(slide, n, escuro):
    c = TEXTO_SOBRE_ESCURO if escuro else "slate_claro"
    caixa(slide, 502920, 6547104, 7772400, 274320, RODAPE, 900, c)
    caixa(slide, 10972800, 6547104, 713232, 274320, f"{n:02d}/{TOTAL}", 900, c, algn="r")


def capa(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fundo(s, "slate")
    retangulo(s, 0, 0, LARGURA, 128016, "acento")
    caixa(s, 868680, 1005840, 10058400, 365760, "DIAGNÓSTICO EXECUTIVO · [NOME DO BOOK]", 1300, "acento", True, 400)
    caixa(s, 822960, 2331720, 10241280, 1737360, "[Nome do Projeto / Cliente]", 4800, "FFFFFF", True)
    caixa(s, 868680, 3383280, 10058400, 548640, "[Área / Regional] · [Empresa]", 1600, TEXTO_SOBRE_ESCURO)
    retangulo(s, 868680, 4160520, 502920, 36576, "acento")
    caixa(s, 868680, 4343400, 9601200, 1188720, "[Resumo do escopo do book em uma frase]", 1500, "FFFFFF", entre_linhas=1.3)
    caixa(s, 868680, 6263640, 7315200, 365760, ASSINATURA, 1100, "slate_claro")
    retangulo(s, 0, 6729984, LARGURA, 128016, "acento")


def agenda(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fundo(s, "fundo_conteudo")
    caixa(s, 502920, 411480, 10515600, 292608, "SUMÁRIO", 1100, "acento", True, 400)
    caixa(s, 502920, 713232, 10515600, 777240, "Agenda", 2800, "slate", True)
    rodape(s, 2, False)
    itens = [(f"[Bloco {i}: título]", f"[Uma frase resumindo o bloco {i}]") for i in range(1, 5)]
    itens.append(("Próximos Passos", "[Uma frase resumindo as recomendações finais]"))
    for i, (tit, desc) in enumerate(itens):
        y = 1691640 + i * 786384
        retangulo(s, 502920, y, 10515600, 713232, "FFFFFF", borda="borda")
        retangulo(s, 502920, y, 64008, 713232, "acento")
        retangulo(s, 758952, y + 105156, 502920, 502920, "slate")
        caixa(s, 758952, y + 105156, 502920, 502920, str(i + 1), 1600, "FFFFFF", True, algn="ctr", ancora="ctr")
        caixa(s, 1399032, y + 128016, 9436608, 310896, tit, 1400, "slate", True)
        caixa(s, 1399032, y + 438912, 9436608, 219456, desc, 1000, "slate_medio", entre_linhas=1.1)


def divisor(prs, n, pagina):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fundo(s, "slate")
    caixa(s, 822960, 1965960, 2194560, 1463040, f"{n:02d}", 9200, ESCURO_FANTASMA, True)
    retangulo(s, 868680, 1828800, 64008, 365760, "acento")
    caixa(s, 1051560, 1874519, 3200400, 365760, f"PARTE {n}", 1200, "acento", True, 400)
    caixa(s, 868680, 3246120, 10058400, 1188720, f"[Título do Bloco {n}]", 3400, "FFFFFF", True, entre_linhas=1.05)
    caixa(s, 868680, 4526280, 9601200, 1005840, f"[Diagnóstico do bloco {n} em uma ou duas frases]", 1400,
          TEXTO_SOBRE_ESCURO, entre_linhas=1.25)
    retangulo(s, 0, 6729984, LARGURA, 128016, "acento")
    rodape(s, pagina, True)


def conteudo(prs, n, pagina):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    cards = []
    for k in range(1, 5):
        cards.append({"label": f"[LABEL KPI {k}]", "value": "[Valor]", "delta": "[Contexto/variação]",
                      "deltacolor": "neutro" if k == 2 else "negativo"})
    linhas = [[f"[Item {i}]"] + [f"[Col{c}]" for c in range(2, 9)] for i in range(1, 7)]
    linhas.append(["TOTAL", "-"] + [f"[Total Col{c}]" for c in range(3, 9)])
    escrever_no_slide(
        s, eyebrow=f"[ETIQUETA BLOCO {n}]", title=f"[Título do Bloco {n}, página de conteúdo]",
        page=f"{pagina:02d}/{TOTAL}", footer=RODAPE, cards_spec=cards,
        headers=["[Nome/ID]", "[Segmento]"] + [f"[Coluna {c}]" for c in range(3, 9)], data_rows=linhas,
        leitura=f"[Diagnóstico do bloco {n} em uma frase + insight que conecta ao próximo passo; "
                "no máximo 2 linhas para não colidir com o rodapé.]")


def fechamento(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fundo(s, "slate")
    retangulo(s, 0, 0, LARGURA, 128016, "acento")
    caixa(s, 868680, 1188720, 7315200, 365760, "PRÓXIMOS PASSOS", 1300, "acento", True, 400)
    caixa(s, 868680, 1691640, 10241280, 1005840, "[Empresa / Projeto] · Recomendações [Período]", 3400, "FFFFFF", True)
    for i in range(4):
        y = 2880360 + i * 566928
        retangulo(s, 868680, y + 91440, 109728, 109728, "acento")
        caixa(s, 1143000, y, 9875520, 502920, f"[Recomendação {i + 1}: ação específica, com dono e prazo]", 1400,
              "FFFFFF", entre_linhas=1.2)
    caixa(s, 868680, 6263640, 7315200, 365760, ASSINATURA, 1100, "slate_claro")
    retangulo(s, 0, 6729984, LARGURA, 128016, "acento")
    rodape(s, TOTAL, True)


def limpar_pacote(caminho, titulo, n_slides):
    """tira miniatura e configuração de impressora e reescreve as propriedades do documento."""
    with zipfile.ZipFile(caminho) as z:
        itens = [(i, z.read(i.filename)) for i in z.infolist()]
    fora = ("docProps/thumbnail.jpeg", "ppt/printerSettings/")
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           f'<TotalTime>0</TotalTime><Application>python-pptx</Application><PresentationFormat>Widescreen</PresentationFormat>'
           f'<Slides>{n_slides}</Slides><Notes>0</Notes><HiddenSlides>0</HiddenSlides>'
           f'<TitlesOfParts><vt:vector size="1" baseType="lpstr"><vt:lpstr>{titulo}</vt:lpstr></vt:vector></TitlesOfParts>'
           '<Company></Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
           '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')
    tmp = caminho + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for info, dados in itens:
            nome = info.filename
            if nome.startswith(fora):
                continue
            if nome == "docProps/app.xml":
                dados = app.encode("utf-8")
            elif nome in ("_rels/.rels", "ppt/_rels/presentation.xml.rels"):
                t = dados.decode("utf-8")
                t = re.sub(r'<Relationship [^>]*Target="[^"]*(thumbnail\.jpeg|printerSettings[^"]*)"[^>]*/>', "", t)
                dados = t.encode("utf-8")
            elif nome == "[Content_Types].xml":
                t = dados.decode("utf-8")
                t = re.sub(r'<Override [^>]*PartName="/ppt/printerSettings/[^"]*"[^>]*/>', "", t)
                dados = t.encode("utf-8")
            z.writestr(nome, dados)
    os.replace(tmp, caminho)


def gerar(saida):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(LARGURA), Emu(ALTURA)
    capa(prs)
    agenda(prs)
    pagina = 3
    for n in range(1, 5):
        divisor(prs, n, pagina)
        conteudo(prs, n, pagina + 1)
        pagina += 2
    fechamento(prs)
    titulo = "Modelo de book executivo"
    cp = prs.core_properties
    cp.title, cp.subject, cp.author, cp.last_modified_by = titulo, "", "Super Skill do Líder", "Super Skill do Líder"
    cp.keywords, cp.comments, cp.category, cp.revision = "", "", "", 1
    cp.created = cp.modified = datetime.datetime(2026, 10, 1)
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    prs.save(saida)
    limpar_pacote(saida, titulo, len(prs.slides))
    print("gravado", saida, f"({len(prs.slides)} slides)")


if __name__ == "__main__":
    args = [a for i, a in enumerate(sys.argv[1:], 1) if a != "--config" and sys.argv[i - 1] != "--config"]
    gerar(os.path.abspath(args[0]) if args else os.path.join(AQUI, "..", "assets", "template-base.pptx"))
