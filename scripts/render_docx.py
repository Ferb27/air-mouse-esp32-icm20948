# -*- coding: utf-8 -*-
"""
scripts/render_docx.py
Converts a DOCX file to PDF and PNG page previews using Word COM and PyMuPDF.
"""

import os
import sys
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import win32com.client
import fitz

def render_docx(docx_path, output_dir=None, dpi=150):
    docx_path = os.path.abspath(docx_path)
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"DOCX file not found: {docx_path}")

    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(docx_path), f"{base_name}_previews")
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.abspath(os.path.join(output_dir, f"{base_name}.pdf"))

    print(f"[Word COM] Converting {docx_path} to PDF...")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0  # wdAlertsNone
    try:
        doc = word.Documents.Open(
            docx_path,
            ReadOnly=True,
            ConfirmConversions=False,
            AddToRecentFiles=False
        )
        # 17 = wdExportFormatPDF
        doc.ExportAsFixedFormat(pdf_path, 17, OpenAfterExport=False)
        doc.Close(False)
        print(f"[Word COM] Exported PDF: {pdf_path}")
    finally:
        try:
            word.Quit()
        except Exception:
            pass

    print(f"[PyMuPDF] Rendering pages to PNG at {dpi} DPI...")
    pdf_doc = fitz.open(pdf_path)
    total_pages = len(pdf_doc)
    print(f"[PyMuPDF] Total pages: {total_pages}")

    rendered_images = []
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    for page_idx in range(total_pages):
        page = pdf_doc.load_page(page_idx)
        pix = page.get_pixmap(matrix=mat)
        img_name = f"page_{page_idx + 1:02d}.png"
        img_path = os.path.join(output_dir, img_name)
        pix.save(img_path)
        rendered_images.append(img_path)
        print(f"  - Rendered Page {page_idx + 1} -> {img_path}")

    pdf_doc.close()
    print(f"[Render Complete] {total_pages} pages rendered to {output_dir}")
    return total_pages, rendered_images, pdf_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render DOCX to PDF and PNG previews")
    parser.add_argument("docx_path", help="Path to DOCX file")
    parser.add_argument("--output-dir", default=None, help="Directory to save PDF and PNGs")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for rendering images")
    args = parser.parse_args()

    render_docx(args.docx_path, args.output_dir, args.dpi)
