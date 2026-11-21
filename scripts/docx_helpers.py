import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Colors
C_PRIMARY = '1F4E79'      # Navy
C_SECONDARY = '2E75B6'    # Blue
C_DARK = '222222'         # Body text
C_LIGHT_BG = 'F4F6F9'     # Code/Callout fill
C_BORDER = 'D3D3D3'       # Border
C_ALT_ROW = 'F9FAFB'      # Alt table row
C_WARNING = 'D79B00'      # Amber
C_DANGER = 'C00000'       # Red
C_SUCCESS = '274E13'      # Green

def set_page_setup(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(0.8)
        s.page_width = Inches(8.27)   # A4
        s.page_height = Inches(11.69) # A4

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_padding(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_styling(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="{C_PRIMARY}"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="{C_PRIMARY}"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(borders)
    
    # Header row
    for cell in table.rows[0].cells:
        set_cell_background(cell, C_PRIMARY)
        set_cell_padding(cell, top=120, bottom=120, left=160, right=160)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(10)
    
    # Body rows
    for r_idx, row in enumerate(table.rows[1:], start=1):
        bg = C_ALT_ROW if r_idx % 2 == 1 else 'FFFFFF'
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_padding(cell, top=90, bottom=90, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGBColor(34, 34, 34)

    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(w)

def add_callout(doc, title, text, kind='note'):
    color_map = {
        'note': (C_PRIMARY, 'EBF3FA'),
        'warning': (C_WARNING, 'FFF9E6'),
        'alert': (C_DANGER, 'FDEDED'),
        'success': (C_SUCCESS, 'EDF7ED'),
        'teacher': ('6A1B9A', 'F3E5F5')
    }
    border_color, bg_color = color_map.get(kind, (C_PRIMARY, 'EBF3FA'))
    
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.4)
    set_cell_background(cell, bg_color)
    set_cell_padding(cell, top=140, bottom=140, left=200, right=200)
    
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"[{title.upper()}] ")
    run_t.font.name = 'Times New Roman'
    run_t.font.bold = True
    run_t.font.size = Pt(10)
    
    r = int(border_color[0:2], 16)
    g = int(border_color[2:4], 16)
    b = int(border_color[4:6], 16)
    run_t.font.color.rgb = RGBColor(r, g, b)
    
    run_body = p.add_run(text)
    run_body.font.name = 'Times New Roman'
    run_body.font.size = Pt(9.5)
    run_body.font.color.rgb = RGBColor(34, 34, 34)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.4)
    set_cell_background(cell, 'F8F9FA')
    set_cell_padding(cell, top=100, bottom=100, left=160, right=160)
    
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="8" w:space="0" w:color="CCCCCC"/><w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tcBorders>')
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(code_str.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(33, 37, 41)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def add_figure(doc, img_path, caption_text, width_in_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_in_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = 'Times New Roman'
        run_cap.font.size = Pt(9)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(100, 100, 100)

def add_toc_field(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run()
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>')
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fldChar3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_header_footer(doc, header_title, footer_left):
    for section in doc.sections:
        section.different_first_page_header_footer = True
        
        # Header (from page 2)
        header = section.header
        p_h = header.paragraphs[0]
        p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_h.paragraph_format.space_after = Pt(4)
        run_h = p_h.add_run(header_title)
        run_h.font.name = 'Times New Roman'
        run_h.font.size = Pt(8.5)
        run_h.font.italic = True
        run_h.font.color.rgb = RGBColor(128, 128, 128)
        
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="2" w:color="CCCCCC"/></w:pBdr>')
        p_h._p.get_or_add_pPr().append(pBdr)

        # Footer (from page 2)
        footer = section.footer
        p_f = footer.paragraphs[0]
        p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        run_fl = p_f.add_run(footer_left + "\t\tTrang ")
        run_fl.font.name = 'Times New Roman'
        run_fl.font.size = Pt(8.5)
        run_fl.font.color.rgb = RGBColor(128, 128, 128)
        
        fld_page = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        p_f._p.append(fld_page)
        
        run_slash = p_f.add_run(" / ")
        run_slash.font.name = 'Times New Roman'
        run_slash.font.size = Pt(8.5)
        run_slash.font.color.rgb = RGBColor(128, 128, 128)
        
        fld_numpages = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="NUMPAGES"/>')
        p_f._p.append(fld_numpages)
        
        pBdr_f = parse_xml(f'<w:pBdr {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="2" w:color="CCCCCC"/></w:pBdr>')
        p_f._p.get_or_add_pPr().append(pBdr_f)
