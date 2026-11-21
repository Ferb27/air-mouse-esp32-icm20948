#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
format_report_essay.py — Định dạng lại BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx theo kiểu tiểu luận.

CHỈ ĐỔI ĐỊNH DẠNG (font, cỡ chữ, giãn dòng, lề, tiêu đề, chân trang, độ rộng bảng).
KHÔNG đổi nội dung chữ. Các đoạn trống dùng để "nhấn Enter" bị gỡ vì giãn dòng 1.5 sẽ biến
chúng thành khoảng trắng lớn.

Thông số chuẩn tiểu luận (sửa ở đây nếu thầy muốn khác):
  Font Times New Roman 13 pt, giãn dòng 1.5, canh đều, thụt đầu dòng 1 cm, cách đoạn 6 pt
  Lề: trái 3.0 cm (đóng quyển), phải 2.0, trên 2.0, dưới 2.0
  Tiêu đề: cấp 1 IN HOA đậm 14 pt; cấp 2 đậm 13 pt; cấp 3 đậm-nghiêng 13 pt
  Bảng: 10.5 pt, giãn dòng đơn, rộng đúng bằng vùng chữ
  Chân trang: "Trang X / Y" canh giữa 12 pt, có cả trang 1

Usage: python scripts/format_report_essay.py [đường_dẫn.docx]   (mặc định: file ở thư mục gốc)
"""
import os
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.text.paragraph import Paragraph

FONT = 'Times New Roman'
BODY_PT = 13
H1_PT, H2_PT, H3_PT = 14, 13, 13
TABLE_PT = 10.5
LINE = 1.5
INDENT_CM = 1.0
MARGIN = dict(left=3.0, right=2.0, top=2.0, bottom=2.0)
FOOTER_DIST_CM = 1.0

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = os.path.join(ROOT, 'BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx')


def set_font(run, size, bold=None, italic=None):
    run.font.name = FONT
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), FONT)
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic


def classify(p):
    t = p.text.strip()
    runs = [r for r in p.runs if r.text.strip()]
    all_bold = bool(runs) and all(r.bold for r in runs)
    if all_bold and len(t) < 130:
        if re.match(r'^\d+\.\d+\.\d+\.', t):
            return 'h3'
        if re.match(r'^\d+\.\d+\.', t):
            return 'h2'
        if re.match(r'^\d+\.\s', t) and t == t.upper():
            return 'h1'
    return 'body'


def fmt_heading(p, level):
    size = {1: H1_PT, 2: H2_PT, 3: H3_PT}[level]
    pf = p.paragraph_format
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.first_line_indent = Cm(0)
    pf.left_indent = Cm(0)
    pf.space_before = Pt({1: 18, 2: 12, 3: 8}[level])
    pf.space_after = Pt(6)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    pf.widow_control = True
    for r in p.runs:
        set_font(r, size, bold=True, italic=(level == 3))


def fmt_body(p, after_table=False):
    pf = p.paragraph_format
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Cm(INDENT_CM)
    pf.left_indent = Cm(0)
    pf.space_before = Pt(6 if after_table else 0)  # đoạn ngay sau khung/bảng cần cách ra
    pf.space_after = Pt(6)
    pf.line_spacing = LINE
    pf.widow_control = True
    if p.text.rstrip().endswith(':'):
        pf.keep_with_next = True  # câu dẫn vào bảng không bị tách khỏi bảng
    for r in p.runs:
        set_font(r, BODY_PT)


def fmt_figure(p, doc):
    pf = p.paragraph_format
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.first_line_indent = Cm(0)
    pf.left_indent = Cm(0)
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.0
    text_w = 21.0 - MARGIN['left'] - MARGIN['right']
    for sh in doc.inline_shapes:
        if sh.width.cm > text_w:
            ratio = text_w / sh.width.cm
            sh.height = int(sh.height * ratio)
            sh.width = Cm(text_w)


def is_code_table(tbl):
    """Khung mã nguồn: bảng 1 ô, chữ Consolas. Chỉ chỉnh độ rộng, giữ nguyên font."""
    try:
        runs = tbl.cell(0, 0).paragraphs[0].runs
        return len(tbl.rows) == 1 and len(tbl.columns) == 1 and bool(runs) and runs[0].font.name == 'Consolas'
    except IndexError:
        return False


def fmt_table(tbl, text_w_cm):
    code = is_code_table(tbl)
    el = tbl._tbl
    grid = el.find(qn('w:tblGrid')).findall(qn('w:gridCol'))
    old = [int(g.get(qn('w:w'))) for g in grid]
    target = int(text_w_cm * 567)
    new = [int(round(w * target / sum(old))) for w in old]
    new[-1] += target - sum(new)
    for g, w in zip(grid, new):
        g.set(qn('w:w'), str(w))
    tblPr = el.tblPr
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None:
        tblW = OxmlElement('w:tblW')
        tblPr.insert(0, tblW)
    tblW.set(qn('w:w'), str(target))
    tblW.set(qn('w:type'), 'dxa')
    ind = tblPr.find(qn('w:tblInd'))
    if ind is not None:
        tblPr.remove(ind)
    for ri, row in enumerate(tbl.rows):
        for ci, cell in enumerate(row.cells):
            tcW = cell._tc.get_or_add_tcPr().find(qn('w:tcW'))
            if tcW is not None and ci < len(new):
                tcW.set(qn('w:w'), str(new[ci]))
                tcW.set(qn('w:type'), 'dxa')
            if code:
                continue
            for p in cell.paragraphs:
                pf = p.paragraph_format
                pf.first_line_indent = Cm(0)
                pf.left_indent = Cm(0)
                pf.space_before = Pt(1)
                pf.space_after = Pt(1)
                pf.line_spacing = 1.0
                if ri == 0:
                    pf.keep_with_next = True  # dòng tiêu đề bảng luôn đi cùng dòng dữ liệu đầu
                if ri == 0 or p.alignment == WD_ALIGN_PARAGRAPH.CENTER:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    set_font(r, TABLE_PT, bold=True if ri == 0 else None)


def fmt_footer(section):
    section.different_first_page_header_footer = False  # trang 1 là nội dung, cũng có số trang
    section.footer_distance = Cm(FOOTER_DIST_CM)
    for p in section.footer.paragraphs:
        pPr = p._p.get_or_add_pPr()
        jc = pPr.find(qn('w:jc'))
        if jc is None:
            jc = OxmlElement('w:jc')
            pPr.append(jc)
        jc.set(qn('w:val'), 'center')
    for rpr in section.footer._element.iter(qn('w:rPr')):
        for tag, val in (('w:sz', '24'), ('w:szCs', '24')):
            e = rpr.find(qn(tag))
            if e is None:
                e = OxmlElement(tag)
                rpr.append(e)
            e.set(qn('w:val'), val)
        c = rpr.find(qn('w:color'))
        if c is None:
            c = OxmlElement('w:color')
            rpr.append(c)
        c.set(qn('w:val'), '000000')


def main(path):
    doc = docx.Document(path)
    sec = doc.sections[0]
    sec.left_margin, sec.right_margin = Cm(MARGIN['left']), Cm(MARGIN['right'])
    sec.top_margin, sec.bottom_margin = Cm(MARGIN['top']), Cm(MARGIN['bottom'])
    text_w = sec.page_width.cm - MARGIN['left'] - MARGIN['right']

    normal = doc.styles['Normal']
    normal.font.name = FONT
    normal.font.size = Pt(BODY_PT)
    rf = normal.element.get_or_add_rPr().find(qn('w:rFonts'))
    if rf is not None:
        rf.set(qn('w:eastAsia'), FONT)

    body = doc.element.body
    children = list(body.iterchildren())
    kinds = {'h1': 0, 'h2': 0, 'h3': 0, 'body': 0, 'figure': 0, 'removed': 0, 'tables': 0}
    for idx, el in enumerate(children):
        tag = el.tag.split('}')[1]
        if tag == 'tbl':
            fmt_table(docx.table.Table(el, doc._body), text_w)
            kinds['tables'] += 1
        elif tag == 'p':
            p = Paragraph(el, doc._body)
            has_img = bool(el.findall('.//' + qn('w:drawing')))
            is_last = idx + 1 < len(children) and children[idx + 1].tag.endswith('sectPr')
            if has_img:
                fmt_figure(p, doc)
                kinds['figure'] += 1
            elif not p.text.strip():
                if is_last:  # Word cần 1 đoạn sau bảng cuối; thu nhỏ để không sinh trang trắng
                    pf = p.paragraph_format
                    pf.space_before = pf.space_after = Pt(0)
                    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                    pf.line_spacing = Pt(2)
                else:
                    body.remove(el)
                    kinds['removed'] += 1
            else:
                kind = classify(p)
                if kind == 'h1':
                    fmt_heading(p, 1)
                elif kind == 'h2':
                    fmt_heading(p, 2)
                elif kind == 'h3':
                    fmt_heading(p, 3)
                else:
                    fmt_body(p, after_table=idx > 0 and children[idx - 1].tag.endswith('}tbl'))
                kinds[kind] += 1
    fmt_footer(sec)
    doc.save(path)
    print('[OK]', path)
    print('     ', kinds)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)
