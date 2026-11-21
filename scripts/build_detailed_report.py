#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_detailed_report.py — Dựng "Báo cáo chi tiết kiến thức Air Mouse" từ Markdown.

Nguồn : deliverables/BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md
Đầu ra: deliverables/BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.docx (+ .pdf qua Word COM)

Định dạng giống báo cáo giữa kỳ: Times New Roman, A4, lề ~2 cm, bảng kiểu học thuật
(style_academic_table của build_report_doc.py), footer "Trang X / Y".
Markdown hỗ trợ: front matter, # / ## / ###, đoạn văn, - và 1. danh sách,
bảng |...|, khối ``` code ```, callout "> [!HOI] tiêu đề" / "> [!NOTE] tiêu đề",
inline **đậm** và `code`.
"""
import os
import re
import sys

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Inches, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_report_doc import style_academic_table  # noqa: E402
from docx_helpers import set_cell_background, set_cell_padding  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'deliverables', 'BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md')
OUT_DOCX = os.path.join(ROOT, 'deliverables', 'BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.docx')
OUT_PDF = os.path.join(ROOT, 'deliverables', 'BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.pdf')

FONT = 'Times New Roman'
MONO = 'Consolas'
BODY_PT = 10.5
TEXT_WIDTH_IN = 6.69  # A4 8.27in - 2 x 0.79in
CALLOUT = {  # kind -> (nhãn, màu viền, màu nền)
    'HOI': ('THẦY CÓ THỂ HỎI', '6A1B9A', 'F3E5F5'),
    'NOTE': ('LƯU Ý', '1F4E79', 'EBF3FA'),
}

INLINE = re.compile(r'(\*\*[^*]+\*\*|`[^`]+`)')


def add_inline(p, text, size=BODY_PT, bold=False, color=(20, 20, 20)):
    """Thêm text có **đậm** và `code` vào paragraph p."""
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2])
            r.font.bold = True
            r.font.name = FONT
        elif part.startswith('`') and part.endswith('`'):
            r = p.add_run(part[1:-1])
            r.font.name = MONO
            r.font.bold = bold
        else:
            r = p.add_run(part)
            r.font.name = FONT
            r.font.bold = bold
        r.font.size = Pt(size if r.font.name == FONT else size - 1)
        r.font.color.rgb = RGBColor(*color)


def setup_document():
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.79)
        s.bottom_margin = Inches(0.95)
        s.left_margin = Inches(0.79)
        s.right_margin = Inches(0.79)
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.different_first_page_header_footer = True
        s.footer_distance = Inches(0.40)
        run = ('<w:r><w:rPr><w:rFonts w:ascii="{f}" w:hAnsi="{f}"/><w:sz w:val="18"/>'
               '<w:color w:val="646464"/></w:rPr>{inner}</w:r>')
        t = lambda s_: run.format(f=FONT, inner=f'<w:t xml:space="preserve">{s_}</w:t>')
        fld = lambda instr: (f'<w:fldSimple w:instr="{instr}">'
                             + run.format(f=FONT, inner='<w:t>1</w:t>') + '</w:fldSimple>')
        p_xml = (f'<w:p {nsdecls("w")}><w:pPr><w:jc w:val="right"/></w:pPr>'
                 + t('Báo cáo chi tiết kiến thức Air Mouse — Trang ') + fld('PAGE')
                 + t(' / ') + fld('NUMPAGES') + '</w:p>')
        p_f = s.footer.paragraphs[0]
        p_f._p.getparent().replace(p_f._p, parse_xml(p_xml))

    # Heading styles thật để Word dựng được mục lục; định dạng giống báo cáo (đen, Times)
    for name, size in (('Heading 1', 13), ('Heading 2', 11.5), ('Heading 3', 10.5)):
        st = doc.styles[name]
        st.font.name = FONT
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.italic = False
        st.font.color.rgb = RGBColor(0, 0, 0)
        rpr = st.element.get_or_add_rPr()
        rpr.append(parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{FONT}" w:hAnsi="{FONT}" '
                             f'w:eastAsia="{FONT}" w:cs="{FONT}"/>'))
        pf = st.paragraph_format
        pf.space_before = Pt(10 if name == 'Heading 1' else 6)
        pf.space_after = Pt(3)
        pf.keep_with_next = True
    normal = doc.styles['Normal']
    normal.font.name = FONT
    normal.font.size = Pt(BODY_PT)
    return doc


def add_cover(doc, meta):
    def line(text, size, bold=False, italic=False, before=0, after=4):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = RGBColor(0, 0, 0)

    line(meta.get('course', ''), 12, bold=True, before=70, after=40)
    line(meta.get('title', ''), 18, bold=True, after=10)
    line(meta.get('subtitle', ''), 12, italic=True, after=40)
    line('Tài liệu học tập và phản biện của nhóm — đi kèm báo cáo giữa kỳ đã nộp, không thay thế báo cáo đó.', 10.5, italic=True, after=6)
    line(meta.get('date', ''), 11, after=30)
    toc_title = doc.add_paragraph()
    toc_title.paragraph_format.space_before = Pt(20)
    r = toc_title.add_run('MỤC LỤC')
    r.font.name = FONT
    r.font.size = Pt(12)
    r.font.bold = True
    p = doc.add_paragraph()
    run = p.add_run()
    run._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>'))
    run._r.append(parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText>'))
    run._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>'))
    run2 = p.add_run('(Mục lục được cập nhật khi xuất PDF)')
    run2.font.italic = True
    run._r.addnext(run2._r)
    end = p.add_run()
    end._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>'))
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def add_paragraph(doc, text, indent=0.0, prefix=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(1)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.15
    if indent:
        pf.left_indent = Inches(indent)
        pf.first_line_indent = Inches(-0.18)
    if prefix:
        r = p.add_run(prefix)
        r.font.name = FONT
        r.font.size = Pt(BODY_PT)
    add_inline(p, text)
    return p


def col_widths(rows):
    ncol = len(rows[0])
    lens = [max(len(r[c]) if c < len(r) else 0 for r in rows) for c in range(ncol)]
    weights = [max(6, min(l, 90)) ** 0.8 for l in lens]
    tot = sum(weights)
    return [max(0.55, TEXT_WIDTH_IN * w / tot) for w in weights]


def add_table(doc, rows):
    ncol = len(rows[0])
    rows = [r + [''] * (ncol - len(r)) for r in rows]
    table = doc.add_table(rows=len(rows), cols=ncol)
    for i, row in enumerate(rows):
        for j, cell_text in enumerate(row):
            cell = table.cell(i, j)
            add_inline(cell.paragraphs[0], cell_text, size=9.0, bold=(i == 0))
    style_academic_table(table, col_widths(rows))
    for cell in table.rows[0].cells:  # dòng tiêu đề luôn đi cùng dòng dữ liệu đầu, không bị bỏ lơ lửng cuối trang
        for p in cell.paragraphs:
            p.paragraph_format.keep_with_next = True
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_code(doc, lines):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(TEXT_WIDTH_IN)
    set_cell_background(cell, 'F8F9FA')
    set_cell_padding(cell, top=80, bottom=80, left=140, right=140)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run('\n'.join(lines))
    r.font.name = MONO
    r.font.size = Pt(8.0)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_callout(doc, kind, title, body_lines):
    label, border, bg = CALLOUT.get(kind, CALLOUT['NOTE'])
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(TEXT_WIDTH_IN)
    set_cell_background(cell, bg)
    set_cell_padding(cell, top=110, bottom=110, left=180, right=180)
    cell._tc.get_or_add_tcPr().append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border}"/>'
        f'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>'))
    rgb = tuple(int(border[i:i + 2], 16) for i in (0, 2, 4))
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(f'[{label}] ')
    r.font.name = FONT
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(*rgb)
    add_inline(p, title.replace('Thầy có thể hỏi: ', ''), size=9.5, bold=True, color=rgb)
    for line in body_lines:
        q = cell.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.line_spacing = 1.1
        add_inline(q, line, size=9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def split_row(line):
    line = line.strip().strip('|').replace('\\|', '\u0000')
    return [c.strip().replace('\u0000', '|') for c in line.split('|')]


def build():
    src = open(SRC, encoding='utf-8').read().splitlines()
    meta, i = {}, 0
    if src and src[0].strip() == '---':
        i = 1
        while src[i].strip() != '---':
            k, _, v = src[i].partition(':')
            meta[k.strip()] = v.strip()
            i += 1
        i += 1

    doc = setup_document()
    add_cover(doc, meta)
    first_h1 = True
    while i < len(src):
        line = src[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith('```'):
            block = []
            i += 1
            while not src[i].strip().startswith('```'):
                block.append(src[i])
                i += 1
            add_code(doc, block)
            i += 1
            continue
        if s.startswith('|'):
            rows = []
            while i < len(src) and src[i].strip().startswith('|'):
                cells = split_row(src[i])
                if not all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            add_table(doc, rows)
            continue
        m = re.match(r'>\s*\[!(\w+)\]\s*(.*)', s)
        if m:
            kind, title, body = m.group(1), m.group(2), []
            i += 1
            while i < len(src) and src[i].strip().startswith('>'):
                body.append(src[i].strip()[1:].strip())
                i += 1
            add_callout(doc, kind, title, body)
            continue
        m = re.match(r'(#{1,3})\s+(.*)', s)
        if m:
            level = len(m.group(1))
            if level == 1 and not first_h1 and m.group(2).startswith('PHỤ LỤC'):
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            first_h1 = first_h1 and level != 1
            h = doc.add_heading(level=level)
            add_inline(h, m.group(2), size={1: 13, 2: 11.5, 3: 10.5}[level], bold=True, color=(0, 0, 0))
            i += 1
            continue
        m = re.match(r'(\s*)- (.*)', line)
        if m:
            add_paragraph(doc, m.group(2), indent=0.3 + 0.25 * (len(m.group(1)) // 2), prefix='•  ')
            i += 1
            continue
        m = re.match(r'(\s*)(\d+)\. (.*)', line)
        if m:
            add_paragraph(doc, m.group(3), indent=0.3 + 0.25 * (len(m.group(1)) // 2), prefix=f'{m.group(2)}.  ')
            i += 1
            continue
        add_paragraph(doc, s)
        i += 1

    doc.save(OUT_DOCX)
    print('[DOCX]', OUT_DOCX)


def export_pdf():
    import win32com.client
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        d = word.Documents.Open(OUT_DOCX)
        for toc in d.TablesOfContents:
            toc.Update()
        d.Fields.Update()
        d.Save()
        d.SaveAs(OUT_PDF, FileFormat=17)
        pages = d.ComputeStatistics(2)
        d.Close(False)
        print('[PDF]', OUT_PDF, '| pages:', pages)
    finally:
        word.Quit()


if __name__ == '__main__':
    build()
    if '--no-pdf' not in sys.argv:
        export_pdf()
