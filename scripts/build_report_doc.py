#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_report_doc.py — Generator for Air Mouse Midterm Progress Report (Week 5)
Formats: BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx & PDF
Complies with Codex review specifications:
- Concise progress report format (not exhaustive handbook)
- Theory sections condensed to a 1-page summary table
- 5-byte HID Mouse Report [Buttons, dX, dY, Wheel, Pan]
- BLE connection strictly NOT_TESTED on PC
- Correct log files: esptool_chip_id.log, esptool_flash_id.log, probe_output.log, probe_i2c_result.log, main_firmware_boot.log
- Build status: "Build thành công; RAM 39.628 byte, Flash 1.158.973 byte."
- Short-term stability: "Không ghi nhận NACK hoặc lỗi bus trong phép thử ngắn hạn đã ghi log."
- MAC note: "MAC được ẩn trong tài liệu sinh viên; raw evidence nội bộ được giữ nguyên để bảo toàn bằng chứng."
- Clean footer with "Trang X / Y" across all pages, no overlapping
- Compact ASCII block diagram instead of unreadable image
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def style_academic_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Border: Horizontal top/bottom 1pt, header divider 0.75pt, no vertical borders
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D0D0"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)
    
    for row_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        if row_idx == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        for col_idx, cell in enumerate(row.cells):
            if col_widths and col_idx < len(col_widths):
                cell.width = Inches(col_widths[col_idx])
                
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            if row_idx == 0:
                set_cell_shading(cell, "F2F2F2")
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(9.5)
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(0, 0, 0)
            else:
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(1)
                    p.paragraph_format.line_spacing = 1.05
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(9.0)
                        r.font.color.rgb = RGBColor(20, 20, 20)

def build_report():
    doc = docx.Document()
    
    # Page setup: A4 Portrait, Margins 2.0 cm (0.79 in)
    for s in doc.sections:
        s.top_margin = Inches(0.79)
        s.bottom_margin = Inches(0.95)
        s.left_margin = Inches(0.79)
        s.right_margin = Inches(0.79)
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.different_first_page_header_footer = True
        s.footer_distance = Inches(0.40)
        
        # Header empty
        header = s.header
        header.is_linked_to_previous = False
        p_h = header.paragraphs[0]
        p_h.text = ""
        
        # Footer: Right-aligned "Trang X / Y"
        footer = s.footer
        footer.is_linked_to_previous = False
        p_f = footer.paragraphs[0]
        
        ns = nsdecls("w")
        p_xml = (
            f'<w:p {ns}>'
            f'  <w:pPr><w:jc w:val="right"/><w:spacing w:before="60" w:after="0"/></w:pPr>'
            f'  <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="18"/><w:color w:val="646464"/></w:rPr><w:t xml:space="preserve">Trang </w:t></w:r>'
            f'  <w:fldSimple w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="18"/><w:color w:val="646464"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>'
            f'  <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="18"/><w:color w:val="646464"/></w:rPr><w:t xml:space="preserve"> / </w:t></w:r>'
            f'  <w:fldSimple w:instr="NUMPAGES"><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="18"/><w:color w:val="646464"/></w:rPr><w:t>8</w:t></w:r></w:fldSimple>'
            f'</w:p>'
        )
        new_p = parse_xml(p_xml)
        p_f._p.getparent().replace(p_f._p, new_p)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.0)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.bold = True
            r_pre.font.size = Pt(10.5)
            r_pre.font.color.rgb = RGBColor(0, 0, 0)
        r_body = p.add_run(text)
        r_body.font.name = 'Times New Roman'
        r_body.font.size = Pt(10.5)
        r_body.font.italic = italic
        r_body.font.color.rgb = RGBColor(20, 20, 20)
        return p

    def add_ascii_box(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(text)
        r.font.name = 'Consolas'
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(20, 20, 20)
        return p

    # -------------------------------------------------------------
    # TRANG BÌA (COVER PAGE)
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(30)
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("TRƯỜNG ĐẠI HỌC BÁCH KHOA — ĐHQG-HCM\nKHOA ĐIỆN — ĐIỆN TỬ | BỘ MÔN ĐIỆN TỬ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_divider = doc.add_paragraph()
    p_divider.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_divider.paragraph_format.space_before = Pt(0)
    p_divider.paragraph_format.space_after = Pt(40)
    r = p_divider.add_run("———————————————")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.bold = True

    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_before = Pt(0)
    p_type.paragraph_format.space_after = Pt(6)
    r = p_type.add_run("BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI GIỮA KỲ (TUẦN 5)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(10)
    r = p_title.add_run("NGHIÊN CỨU, THIẾT KẾ VÀ CHẾ TẠO CHUỘT BAY KHÔNG DÂY\n(AIR MOUSE BLE HID OVER GATT) DÙNG ESP32 VÀ ICM-20948")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(40)
    r = p_sub.add_run("Báo cáo tiến độ kỹ thuật hệ thống nhúng — Baseline Direct 3.3V Hardware Bring-up")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.italic = True
    r.font.color.rgb = RGBColor(60, 60, 60)

    # Info table
    tbl_info = doc.add_table(rows=6, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "TS. [Tên Giảng viên hướng dẫn]"),
        ("Nhóm sinh viên thực hiện:", "Nhóm đồ án (3 thành viên)"),
        ("Sinh viên thực hiện 1:", "[Họ tên sinh viên 1 — MSSV 1]"),
        ("Sinh viên thực hiện 2:", "[Họ tên sinh viên 2 — MSSV 2]"),
        ("Sinh viên thực hiện 3:", "[Họ tên sinh viên 3 — MSSV 3]"),
        ("Thời điểm báo cáo:", "Học kỳ 1 — Năm học 2026–2027 (Mốc đánh giá Tuần 5)")
    ]
    for idx, (label, val) in enumerate(info_data):
        c0, c1 = tbl_info.cell(idx, 0), tbl_info.cell(idx, 1)
        c0.width, c1.width = Inches(2.4), Inches(4.0)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p0.paragraph_format.space_before = p0.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.space_before = p1.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(label)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10.5)
        r0.font.bold = True
        r1 = p1.add_run(val)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        
    for row in tbl_info.rows:
        for c in row.cells:
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(50)
    r = p_loc.add_run("TP. HỒ CHÍ MINH — THÁNG 09/2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # MỤC 1 — MỤC TIÊU ĐỀ TÀI & KIẾN TRÚC HỆ THỐNG HIỆN TẠI
    # -------------------------------------------------------------
    add_h1("1. MỤC TIÊU ĐỀ TÀI & KIẾN TRÚC HỆ THỐNG HIỆN TẠI")
    
    add_p("Đề tài nghiên cứu, thiết kế và chế tạo thiết bị chuột không gian không dây (Air Mouse), cho phép người dùng điều khiển con trỏ chuột máy tính thông qua cử động xoay cổ tay tự nhiên trong không gian. Thiết bị hoạt động theo nguyên lý trỏ tương đối điều khiển theo tốc độ xoay (Relative Rate-Controlled Pointing Device): vận tốc góc xoay cổ tay (ω_Yaw, ω_Pitch) từ con quay hồi chuyển được ánh xạ tỉ lệ thuận sang độ dời con trỏ (dX, dY). Khi tay dừng lại (ω = 0), con trỏ lập tức đứng yên. Hệ thống không sử dụng gia tốc kế tích phân kép để tìm vị trí không gian 3D nhằm triệt tiêu hoàn toàn sai số trôi tích lũy bùng nổ theo bình phương thời gian (t²).", bold_prefix="1.1. Bản chất đề tài & Mục tiêu sản phẩm: ")

    add_p("Module cảm biến chuyển động WCMCU-20948 (mang chip ICM-20948 9-DOF) kết nối trực tiếp ở mức 3,3 V với vi điều khiển ESP32 Classic DevKit 38-pin qua bus I2C Fast-Mode (400 kHz) trên hai chân GPIO21 (SDA) và GPIO22 (SCL). Thiết kế đã loại bỏ hoàn toàn mạch chuyển mức logic BSS138 và IC ổn áp phụ AMS1117-1.8V sau khi kiểm chứng thực nghiệm Bring-up thành công trên bàn đo. ESP32 đọc định kỳ 10 ms (100 Hz), trừ trôi tĩnh (zero-rate bias), ước lượng tư thế 6 trục qua bộ lọc bù Quaternion (Gyroscope + Accelerometer), áp dụng vùng chết chống rung và đóng gói thành bản tin báo cáo chuột HID tiêu chuẩn 5 byte [Buttons, dX, dY, Wheel, Pan]. Bản tin này được phát qua giao thức Bluetooth Low Energy (BLE HID over GATT).", bold_prefix="1.2. Kiến trúc hệ thống Direct 3.3V: ")

    add_h2("1.3. Sơ đồ khối hệ thống mức kiến trúc (ASCII System Diagram)")
    ascii_diag = """===========================================================================
        SƠ ĐỒ KHỐI HỆ THỐNG AIR MOUSE DIRECT 3.3V (V4.0.0 BASELINE)
===========================================================================

 [Cell Pin LiPo 1S] (3.7V, 1000mAh)
         |
         | (Cell + -> B+, Cell - -> B-)
         v
 [Module TP4056] <== Cổng Type-C sạc 5V
         |
         |-- OUT+ ---> [SW1 (ON/OFF)] ---> V_SYS ---> [MT3608 Boost 5V]
         |                                                   |
         +-- OUT- ---> System GND ---> MT3608 VIN-           v
                                                      [ESP32 DevKit]
                                                      (LDO 3.3V Onboard)
                                                             |
                 +-------------------------------------------+
                 |                     |                     |
            I2C 400 kHz           GPIO25/26/27            GPIO32
          (Direct 3.3V)           (Active-Low)               |
                 |                     |                     v
         [WCMCU-20948]            [3 Nút Bấm]           [R1 (1k)]
         - ICM-20948 (9-DOF)      - SW_LEFT: GPIO25          |
         - Gyro + Accel 6 trục    - SW_RIGHT: GPIO26         v
         - AD0=GND (0x68)         - SW_MODE: GPIO27     [LED Xanh Lá]
         - Trở kéo 10k onboard
         - AK09916: Chưa dùng

 [V_SYS] ---> [Cầu phân áp 100k/100k + C1] ---> GPIO34 (ADC1_CH6) ESP32
                                                (Chưa gọi trong firmware)

 [ESP32 BLE Subsystem] --- BLE HID Mouse 5 byte ---> [MÁY TÍNH PC / TV]
                                                     Trạng thái: NOT_TESTED

===========================================================================
QUY ƯỚC LIÊN KẾT:
  --->  Đường nguồn điện / Điều khiển một chiều (VBAT, V_SYS, 5V, 3V3, GND)
  I2C   Bus dữ liệu số hai chiều (SDA: GPIO21, SCL: GPIO22)
  BLE   Phát sóng BLE gói tin HID chuột 5 byte ([Btn, dX, dY, W, Pan])
==========================================================================="""
    add_ascii_box(ascii_diag)
    add_p("Chi tiết mô tả bằng lời và chỉ dẫn mỹ thuật cho người thiết kế đồ họa được cung cấp đầy đủ trong tài liệu bàn giao deliverables/MO_TA_SO_DO_KHOI_AIR_MOUSE.md.", italic=True)

    # -------------------------------------------------------------
    # MỤC 2 — CÁC KHỐI PHẦN CỨNG SỬ DỤNG & DỰ TOÁN BOM V2.0.0
    # -------------------------------------------------------------
    add_h1("2. CÁC KHỐI PHẦN CỨNG SỬ DỤNG & DỰ TOÁN BOM V2.0.0")
    
    add_p("Hệ thống phần cứng được chuẩn hóa trên bo mạch mang (Carrier Board) một lớp tự gia công, tích hợp 6 khối linh kiện chính:")
    
    tbl_hw = doc.add_table(rows=7, cols=4)
    tbl_hw_headers = ["Phân hệ / Linh kiện", "Phân loại ngoại vi", "Thông số kỹ thuật cốt lõi", "Vai trò trong hệ thống Air Mouse"]
    for i, h in enumerate(tbl_hw_headers):
        tbl_hw.cell(0, i).paragraphs[0].text = h
    
    hw_rows = [
        ("ESP32 DevKit 38-pin", "Nội (Internal MCU)", "Xtensa 240MHz, 520KB SRAM, BLE 4.2, I2C Master, SAR ADC1", "Xử lý trung tâm: đọc I2C, motion pipeline, phát BLE HID."),
        ("WCMCU-20948 (ICM-20948)", "Ngoại vi I2C (External)", "IMU 9-DOF phần cứng, dung hợp 6 trục firmware, I2C 400kHz, 3.3V", "Thu thập dữ liệu vận tốc góc (Gyro) và gia tốc (Accel)."),
        ("TP4056 Type-C + Bảo vệ", "Khối Nguồn (Power)", "IC DW01A + FS8205A, dòng sạc 1A, bảo vệ quá nạp/quá xả/ngắn mạch", "Quản lý sạc pin qua Type-C; B+/B- nối cell; OUT+ qua SW1; OUT- là gốc System GND."),
        ("MT3608 DC-DC Boost", "Khối Nguồn (Power)", "Dải ngõ vào 2–24V, ngõ ra chỉnh cố định 5.0V, hiệu suất ~93%", "Nâng điện áp pin (3.0–4.2V) lên ổn định 5.0V cấp chân VIN ESP32."),
        ("Pin LiPo 1S (523450)", "Khối Nguồn (Power)", "3.7V danh định, 1000mAh, có mạch bảo vệ PCM, cọc cắm JST-PH 2.0", "Cung cấp năng lượng di động; lắp mặt đáy có đệm Kapton + EVA."),
        ("3 Nút Bấm & LED Chỉ Thị", "Giao tiếp Người Dùng", "3 Tactile 12x12mm cap Ø12mm (GPIO25, 26, 27); LED D1 3mm (GPIO32)", "Phím chuột trái/phải/mode (Active-Low); LED báo trạng thái.")
    ]
    for r_idx, r_data in enumerate(hw_rows, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_hw.cell(r_idx, c_idx).paragraphs[0].text = val
    style_academic_table(tbl_hw, [1.4, 1.3, 2.3, 1.6])

    add_h2("2.1. Dự toán linh kiện BOM V2.0.0 đã tinh giản")
    add_p("Sau khi nghiệm thu kết nối Direct 3.3V thành công trên phần cứng sở hữu, nhóm đã loại bỏ hoàn toàn module BSS138 (giảm 10.000đ), IC LDO AMS1117-1.8V (giảm 8.000đ), tụ C3/C4 (giảm 1.500đ) và thu gọn cụm Test Points (giảm 500đ). Danh mục mua mới V2.0.0 gồm đúng 23 vật phẩm vật lý (20 dòng mua hàng) với tổng chi phí dự toán 153.000 VNĐ:")

    tbl_bom = doc.add_table(rows=8, cols=5)
    tbl_bom_headers = ["Nhóm danh mục", "Trạng thái", "Số lượng", "Linh kiện cấu thành tiêu biểu", "Thành tiền (VNĐ)"]
    for i, h in enumerate(tbl_bom_headers):
        tbl_bom.cell(0, i).paragraphs[0].text = h

    bom_summary = [
        ("Linh kiện cốt lõi có sẵn", "OWNED", "2 linh kiện", "ESP32 DevKit 38-pin (U1) + Module WCMCU-20948 (U2)", "0 VNĐ (Có sẵn)"),
        ("Khối Nguồn & Sạc Pin", "BUY", "5 vật phẩm", "Pin LiPo 1S 1000mAh, TP4056 Type-C, MT3608 5V, SW1, Giắc JST", "97.500 VNĐ"),
        ("Khối Phím Bấm & Chỉ Thị", "BUY", "6 vật phẩm", "3 nút nhấn 12x12mm, LED xanh lá 3mm, Trở hạn dòng 1.0k, J2 I2C", "11.500 VNĐ"),
        ("Khối Thụ Động Đo Pin & Lọc", "BUY", "4 vật phẩm", "2 trở phân áp 100k (1%), Tụ lọc C1 100nF, Tụ hóa C2 10µF", "2.500 VNĐ"),
        ("Khối Socket Cắm Module", "BUY", "3 vật phẩm", "2 hàng cái 1x19 (ESP32) + 1 hàng cái 1x10 (WCMCU-20948)", "9.500 VNĐ"),
        ("Khối Header Test Points", "BUY", "1 vật phẩm", "1 dải đực 1x4 chân làm cọc đo kiểm Logic Analyzer (SCL, SDA, 3V3, GND)", "1.000 VNĐ"),
        ("Phụ Kiện Cơ Khí & An Toàn", "BUY", "4 vật phẩm", "3 nắp chụp nút Ø12mm + 1 bộ lót cách điện pin (Kapton + EVA Foam)", "31.000 VNĐ")
    ]
    for r_idx, r_data in enumerate(bom_summary, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_bom.cell(r_idx, c_idx).paragraphs[0].text = val
    style_academic_table(tbl_bom, [1.5, 0.8, 0.9, 2.3, 1.2])
    
    add_p("Tổng chi phí mua sắm dự toán: 153.000 VNĐ (Toàn bộ đơn giá là giá tham chiếu lịch sử; nhóm sẽ khảo sát giá thực tế tại chợ Nhật Tảo và sàn thương mại điện tử trước khi mua sắm).", italic=True)

    # -------------------------------------------------------------
    # MỤC 3 — BẢNG NỐI DÂY TÓM TẮT TOÀN HỆ THỐNG
    # -------------------------------------------------------------
    add_h1("3. BẢNG NỐI DÂY TÓM TẮT TOÀN HỆ THỐNG (PIN-TO-PIN SUMMARY)")
    
    add_p("Bảng nối dây tóm tắt định hướng vẽ sơ đồ nguyên lý (Schematic) trên KiCad theo chuẩn kết nối Direct 3.3V đã khóa:")

    tbl_wire = doc.add_table(rows=11, cols=5)
    tbl_w_headers = ["Khối mạch", "Điểm đầu (Source)", "Điểm đích (Destination)", "Mức điện áp", "Chức năng & Yêu cầu kỹ thuật"]
    for i, h in enumerate(tbl_w_headers):
        tbl_wire.cell(0, i).paragraphs[0].text = h

    wire_rows = [
        ("Nguồn IMU", "ESP32 chân 3V3 & GND", "WCMCU chân VCC & GND", "3.3 V / 0 V", "Cấp nguồn trực tiếp 3.3V từ LDO 3.3V trên board DevKit. Tuyệt đối không nối vào 5V."),
        ("Bus I2C chính", "ESP32 GPIO21 & GPIO22", "WCMCU chân SDA & SCL", "3.3 V", "Tần số 400 kHz; dùng trở kéo 10 kΩ onboard WCMCU; không dùng BSS138."),
        ("Cấu hình IMU", "ESP32 3V3 & GND", "WCMCU NCS (3V3), AD0/FSY (GND)", "3.3 V / 0 V", "NCS=3V3 chọn I2C; AD0=GND chọn địa chỉ 0x68; FSY=GND chống nhiễu."),
        ("Chân phụ IMU", "WCMCU chân INT, ACL, ADA", "Không nối (Để hở chân - NC)", "—", "Chưa dùng ngắt; cấm nối ACL/ADA vào SCL/SDA chính tránh chập bus."),
        ("Nút Chuột Trái", "ESP32 GPIO25", "Nút SW_LEFT -> GND", "3.3 V / 0 V", "Cấu hình INPUT_PULLUP Active-Low. Đấu 2 chân đối diện của nút 4 chân."),
        ("Nút Chuột Phải", "ESP32 GPIO26", "Nút SW_RIGHT -> GND", "3.3 V / 0 V", "Cấu hình INPUT_PULLUP Active-Low. Đấu 2 chân đối diện của nút 4 chân."),
        ("Nút Mode/Clutch", "ESP32 GPIO27", "Nút SW_MODE -> GND", "3.3 V / 0 V", "Cấu hình INPUT_PULLUP Active-Low. GPIO27 là RTC GPIO hỗ trợ đánh thức."),
        ("LED Chỉ Thị", "ESP32 GPIO32", "Trở R1 (1.0k) -> Anode LED -> GND", "3.3 V", "Dòng hạn chế ~1.2 mA bảo vệ ngõ ra vi điều khiển. LED 3mm xanh lá."),
        ("Phân Áp Đo Pin", "V_SYS (sau công tắc)", "R2 100k -> BAT_SENSE -> R3 100k -> GND", "1.5–2.1 V", "Đưa vào GPIO34 (ADC1_CH6) kèm tụ C1 100nF; chưa kích hoạt firmware."),
        ("Chuỗi Nguồn 5V", "Pin (Cell+/- -> B+/B-) -> TP4056; OUT+ qua SW1; OUT- -> System GND", "MT3608 (5.0V) -> VIN/GND ESP32", "5.0 V", "OUT- → system GND → MT3608 VIN-. Chỉnh MT3608 5.0V trước khi cắm ESP32; tụ C2 10µF sát VIN.")
    ]
    for r_idx, r_data in enumerate(wire_rows, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_wire.cell(r_idx, c_idx).paragraphs[0].text = val
    style_academic_table(tbl_wire, [1.1, 1.5, 1.5, 0.8, 1.7])

    add_p("Chi tiết toàn bộ 50 dòng kết nối chân-đến-chân, phân định nhãn in trên module vs GPIO ESP32 và các rào cản cấm nối được mô tả đầy đủ trong tài liệu deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md.", italic=True)

    # -------------------------------------------------------------
    # MỤC 4 — TÓM TẮT LÝ THUYẾT CỐT LÕI
    # -------------------------------------------------------------
    add_h1("4. TÓM TẮT LÝ THUYẾT CỐT LÕI (BẢNG TRÍCH YẾU 1 TRANG)")
    
    add_p("Nhóm tổng hợp ngắn gọn các nền tảng lý thuyết trọng tâm điều khiển phần cứng hệ thống nhúng trong Bảng 4.1 (chi tiết 36 câu hỏi đáp sâu được lưu giữ trong Cẩm nang hỏi đáp giữa kỳ):")

    tbl_th = doc.add_table(rows=5, cols=4)
    tbl_th_headers = ["Chủ đề lý thuyết", "Đặc tính kỹ thuật cốt lõi", "Cấu hình / Thông số dự án", "Ý nghĩa & Tác động phần cứng"]
    for i, h in enumerate(tbl_th_headers):
        tbl_th.cell(0, i).paragraphs[0].text = h

    th_rows = [
        ("Giao thức I2C &\nRepeated START",
         "Giao tiếp 2 dây cực máng hở (Open-Drain). Cần trở kéo pull-up tạo mức HIGH và logic Wired-AND. Tránh bus contention khi nhiều thiết bị chia sẻ bus.",
         "Tần số: 400 kHz (Fast-Mode).\nTrở kéo: 10 kΩ onboard WCMCU.\nĐịa chỉ: 0x68 (AD0=0).\nGhi: 0xD0, Đọc: 0xD1.",
         "Sử dụng Repeated START (Sr) đọc thanh ghi: giữ bus liên tục, chuyển từ Ghi địa chỉ sang Đọc dữ liệu mà không phát STOP, tránh xung đột bus."),
        ("ICM-20948 &\n4 User Bank Map",
         "Cảm biến chia không gian địa chỉ thành 4 Bank (mỗi Bank 128 byte) để vượt qua giới hạn địa chỉ 7-bit. Chuyển Bank qua thanh ghi REG_BANK_SEL (0x7F cố định cả 4 Bank).",
         "PWR_MGMT_1 (0x06 B0) = 0x01 (Auto-PLL, thoát Sleep).\nGYRO_CFG_1 (0x01 B2) = 0x1B (DLPF 51.2Hz, ±500°/s).\nACCEL_CFG (0x14 B2) = 0x1B (DLPF 50.4Hz, ±4g).\nSMPLRT_DIV (0x00 B2) = 10 (ODR ≈ 102.27 Hz).",
         "Cần gọi imu_selectBank() trước khi đọc/ghi thanh ghi khác Bank. 4 thanh ghi cốt lõi đã được kiểm chứng đọc lại (readback) thành công trên phần cứng thật."),
        ("ADC SAR1 ESP32 &\nĐo Điện Áp Pin",
         "SAR ADC 12-bit (4096 mức mã, LSB = V_FSR / 4096). Khối ADC2 bị xung đột khi dùng Wi-Fi; khối ADC1 (GPIO32–39) hoàn toàn độc lập, an toàn khi chạy BLE/Wi-Fi.",
         "Kênh: ADC1_CH6 (GPIO34, Input-only).\nCầu phân áp: 100k/100k (V_sense = 0.5*V_bat).\nKhi pin 4.2V, V_sense = 2.1V nằm trong dải đo tuyến tính khi suy hao 11 dB.",
         "Mạch đo pin tách biệt an toàn với nguồn 5V VIN. Chức năng đo pin hiện CHƯA KÍCH HOẠT TRONG FIRMWARE TUẦN 5 (chưa gọi analogRead trong loop chính)."),
        ("Phân tầng phần mềm\n& Assembly Xtensa",
         "Firmware viết bằng C/C++ trên Arduino/ESP-IDF, biên dịch bởi xtensa-esp32-elf-g++. CPU ESP32 là Xtensa Dual-core 32-bit LX6 (Tensilica, KHÔNG PHẢI ARM).",
         "Trích disassembly từ firmware.elf:\n400d22f0: entry a1, 32\n400d2302: movi a11, 104\n400d2307: call8 TwoWire::beginTransmission",
         "Khẳng định kiến trúc: Dự án không code bằng Assembly thô. Hàm C/C++ được biên dịch thành tập lệnh Xtensa LX6 Windowed ABI; lệnh Wire tương ứng cụm lệnh MMIO.")
    ]
    for r_idx, r_data in enumerate(th_rows, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_th.cell(r_idx, c_idx).paragraphs[0].text = val
    style_academic_table(tbl_th, [1.3, 1.7, 1.8, 1.8])

    # -------------------------------------------------------------
    # MỤC 5 — CÔNG VIỆC ĐÃ HOÀN THÀNH & KẾT QUẢ THỰC NGHIỆM
    # -------------------------------------------------------------
    add_h1("5. CÔNG VIỆC ĐÃ HOÀN THÀNH & KẾT QUẢ THỰC NGHIỆM")
    
    add_p("Đến mốc Tuần 5, nhóm đã hoàn thành toàn diện các hạng mục chuẩn bị lý thuyết, kiến trúc, kiểm thử mô phỏng và đo kiểm Bring-up trên phần cứng thực tế:")

    tbl_m = doc.add_table(rows=8, cols=5)
    tbl_m_headers = ["Mốc kiểm tra", "Đối tượng & Hạng mục", "Tiêu chí nghiệm thu", "Kết quả thực nghiệm", "Trạng thái minh bạch"]
    for i, h in enumerate(tbl_m_headers):
        tbl_m.cell(0, i).paragraphs[0].text = h

    m_rows = [
        ("M1: Chip ID & Flash", "ESP32 DevKit qua esptool COM8", "Nhận dạng đúng CPU Xtensa, flash 4MB", "ESP32-D0WD-V3 (rev v3.1), Flash 4MB DIO 40MHz", "BENCH PASS"),
        ("M2: Quét I2C Bus", "WCMCU-20948 trực tiếp 3.3V", "Phản hồi ACK tại đúng địa chỉ 0x68", "I2C device found at address 0x68 (100k & 400kHz)", "BENCH PASS"),
        ("M3: Định danh WHO_AM_I", "Đọc thanh ghi 0x00 Bank 0", "Giá trị trả về chính xác 0xEA", "100/100 lần đọc WHO_AM_I thành công trong phép thử ngắn hạn", "BENCH PASS"),
        ("M4: Readback Thanh Ghi", "Đọc lại 4 thanh ghi cấu hình", "Khớp giá trị ghi: 0x01, 0x1B, 0x1B, 10", "PWR_MGMT_1=0x01, GYRO=0x1B, ACCEL=0x1B, DIV=10", "READBACK PASS"),
        ("M5: Đọc Burst 12-byte", "Đọc 12 byte dữ liệu thô Bank 0", "Dữ liệu 6 trục đầy đủ, Accel Z ~ +1g", "Accel Z ~ +16200 LSB ≈ +1g (chương trình probe để dải mặc định ±2g = 16384 LSB/g; firmware chính dùng ±4g nên 1g ≈ 8192 LSB), Gyro tĩnh ~ 0 dps", "BENCH PASS"),
        ("M6: Host Test Suite", "Test harness trên máy tính chủ", "10/10 test cases thuật toán logic PASS", "Vượt qua toàn bộ 10/10 bài test tư thế & cử chỉ", "HOST PASS"),
        ("M7: Biên dịch Firmware", "Mã nguồn firmware.ino PlatformIO", "Biên dịch thành công 100%, đủ RAM/Flash", "Build thành công; RAM 39.628 byte, Flash 1.158.973 byte", "BUILD PASS")
    ]
    for r_idx, r_data in enumerate(m_rows, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_m.cell(r_idx, c_idx).paragraphs[0].text = val
    style_academic_table(tbl_m, [1.3, 1.4, 1.6, 1.4, 0.9])
    add_p("* Chú thích trạng thái: BENCH PASS = BENCH_VERIFIED_ON_OWNED_MODULE; READBACK PASS = PHYSICAL_READBACK_CONFIRMED; HOST PASS = HOST_VERIFIED_LOGIC_TESTS; BUILD PASS = PLATFORMIO_COMPILE_VERIFIED.", italic=True)

    add_h2("5.1. Bằng chứng thực nghiệm Hardware Bring-up trực tiếp 3.3V")
    add_p("Ngày 25/09/2026, nhóm thực hiện đo kiểm thực tế trên bàn thí nghiệm với vi điều khiển ESP32 Classic DevKit 38-pin kết nối trực tiếp module WCMCU-20948 ở mức 3,3 V qua cổng COM8:")
    add_p("Xác nhận trạng thái: Không ghi nhận NACK hoặc lỗi bus trong phép thử ngắn hạn đã ghi log (100/100 lần đọc WHO_AM_I thành công liên tục ở cả tần số 100 kHz và 400 kHz). Firmware chính đọc lại thanh ghi vật lý thành công cả 4 thanh ghi cấu hình cốt lõi.", bold_prefix="• Kết quả ổn định ngắn hạn: ")
    add_p("Trong lần thử probe đầu tiên, cổng Serial báo lỗi I2C NACK (được lưu trung thực tại raw_logs/probe_output.log). Nguyên nhân kỹ thuật: Dây cắm jumper breadboard bị lỏng tiếp xúc cơ học và bị cắm lệch hàng chân phía bên phải của ESP32 DevKit 38-pin (nơi hai chân nạp UART TX0/RX0 nằm xen kẽ giữa GPIO22 và GPIO21). Sau khi kiểm tra lại sơ đồ chân, cắm chặt dây đúng vị trí chân vật lý, toàn bộ các phép đo sau đó đều thành công 100% (raw_logs/probe_i2c_result.log và raw_logs/main_firmware_boot.log).", bold_prefix="• Ghi nhận sự cố ban đầu và giải pháp: ")
    add_p("Địa chỉ MAC được ẩn trong tài liệu sinh viên; raw evidence nội bộ được giữ nguyên để bảo toàn bằng chứng số.", bold_prefix="• Bảo vệ dữ liệu riêng tư: ")

    # SHA-256 Table
    tbl_log = doc.add_table(rows=6, cols=3)
    tbl_l_headers = ["Tệp nhật ký thực nghiệm (Raw Log)", "Dung lượng", "Mã băm SHA-256 toàn vẹn dữ liệu"]
    for i, h in enumerate(tbl_l_headers):
        tbl_log.cell(0, i).paragraphs[0].text = h

    log_rows = [
        ("raw_logs/esptool_chip_id.log", "551 B", "fa5eb4951cdbf100cd917d9ce6a3b5388379ff89767a5500db665e1f36735a25"),
        ("raw_logs/esptool_flash_id.log", "604 B", "d142fd348fe31693de7ad022f397ec8ea69bf29f7a9e6ad0f15728f35fbb7fa7"),
        ("raw_logs/probe_output.log", "3271 B", "e2f5b4b2c009b0dda17671720d4840aff2854fa2b3bbed355caa1ff1e10c9b7f"),
        ("raw_logs/probe_i2c_result.log", "4197 B", "a069f551f77dde71034966df6779e697fff4256dd1bb284c90d555fcc35d4d4d"),
        ("raw_logs/main_firmware_boot.log", "2327 B", "b7703685e4b13540ed12d39b3c8b2fde8d237ab0b661bb991dbe003f575be612")
    ]
    for r_idx, r_data in enumerate(log_rows, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_log.cell(r_idx, c_idx).paragraphs[0].text = val
    style_academic_table(tbl_log, [2.3, 0.9, 3.5])

    # -------------------------------------------------------------
    # MỤC 6 — CÔNG VIỆC CHƯA HOÀN THÀNH, HẠN CHẾ & TỒN TẠI
    # -------------------------------------------------------------
    add_h1("6. CÔNG VIỆC CHƯA HOÀN THÀNH, HẠN CHẾ & VẤN ĐỀ TỒN TẠI")
    
    add_p("Nhóm thẳng thắn nhìn nhận các hạn chế và ranh giới kỹ thuật hiện tại của dự án tại mốc giữa kỳ Tuần 5:")
    add_p("Mã nguồn firmware BLE HID đã biên dịch thành công và phát tín hiệu quảng bá 'AirMouse-ESP32', nhưng nhóm CHƯA thực hiện ghép nối thực tế với máy tính PC để đo độ trễ và kiểm tra độ ổn định chuột trên hệ điều hành. Trạng thái kết nối máy tính: NOT_TESTED. Tuyệt đối không tuyên bố con trỏ chuột đã hoạt động thực tế trên PC.", bold_prefix="1. Kết nối BLE HID với máy tính ở trạng thái NOT_TESTED: ")
    add_p("Hoạt động thành công trên đúng module WCMCU-20948 và ESP32 mà nhóm đang sở hữu (BENCH_VERIFIED_ON_OWNED_MODULE). Tuy nhiên, datasheet gốc của IC ICM-20948 (TDK DS-000189) quy định dải điện áp I/O VDDIO tối đa là 1.95V. Việc cấp 3.3V trực tiếp là độ lệch kỹ thuật trên module breakout thương phẩm cụ thể của nhóm và có rủi ro tiềm ẩn về độ bền lâu dài chưa được kiểm chứng qua các bài stress-test. Nhóm không suy rộng thành mức an toàn tối thượng hay áp dụng cho mọi điều kiện biên.", bold_prefix="2. Ranh giới điện áp 3.3V trực tiếp và datasheet raw IC: ")
    add_p("Tuân thủ nghiêm ngặt quy tắc không can thiệp thủ công file cú pháp S-expression thô của KiCad khi chưa cập nhật qua KiCad MCP Server. Do đó, hồ sơ KiCad hiện tại vẫn còn khối BSS138 và AMS1117-1.8V (trạng thái: KICAD_SYNC_STATUS: STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE), sẽ được đồng bộ chính thức ở giai đoạn tiếp theo.", bold_prefix="3. Hồ sơ thiết kế KiCad ở trạng thái chờ đồng bộ: ")
    add_p("Mạch phân áp 100k/100k đã thiết kế phần cứng hoàn chỉnh, nhưng firmware Tuần 5 chưa gọi hàm analogRead(34) trong vòng lặp chính để ưu tiên tối ưu hóa bus I2C và pipeline 100 Hz.", bold_prefix="4. Chức năng đo điện áp pin chưa kích hoạt trong firmware: ")
    add_p("Thuật toán V1 hiện triển khai dung hợp 6 trục (Gyro + Accel). Chưa tích hợp từ kế AK09916 nên trục Yaw chưa có mốc hướng tuyệt đối, dựa vào tích phân con quay. Dù đã có dead-zone triệt tiêu trôi tĩnh, việc xoay liên tục trong thời gian dài vẫn tích lũy sai số trôi nhẹ.", bold_prefix="5. Khối từ kế AK09916 chưa tham gia thuật toán dung hợp: ")

    # -------------------------------------------------------------
    # MỤC 7 — KẾ HOẠCH GIAI ĐOẠN TIẾP THEO
    # -------------------------------------------------------------
    add_h1("7. KẾ HOẠCH TRIỂN KHAI GIAI ĐOẠN TIẾP THEO (TUẦN 6 ĐẾN TUẦN 10)")
    
    add_p("Kế hoạch phân kỳ thực hiện giai đoạn 2 tập trung vào kết nối không dây, hoàn thiện bo mạch in và tinh chỉnh trải nghiệm người dùng:")

    tbl_plan = doc.add_table(rows=7, cols=4)
    tbl_plan_headers = ["Hạng mục công việc", "Kết quả mong đợi", "Tiêu chuẩn hoàn thành", "Mức ưu tiên"]
    for i, h in enumerate(tbl_plan_headers):
        tbl_plan.cell(0, i).paragraphs[0].text = h

    plan_rows = [
        ("Kiểm thử kết nối BLE HID với PC", "Máy tính nhận diện 'AirMouse-ESP32', nhận đủ báo cáo 5-byte 100 Hz.", "Độ trễ < 20 ms, không rớt gói tin trong 10 phút rê chuột liên tục.", "P0 (Bắt buộc)"),
        ("Đồng bộ KiCad qua MCP Server", "Cập nhật schematic và layout PCB loại bỏ BSS138 và AMS1117-1.8V.", "Schematic và layout KiCad vượt 100% kiểm tra ERC/DRC theo baseline V4.0.0.", "P0 (Bắt buộc)"),
        ("Gia công & Hàn bo Carrier Board", "Chế tạo PCB 1 lớp hoàn chỉnh, hàn linh kiện THT và gắn pin LiPo.", "Nguồn 5V và 3.3V ổn định, không chập cháy, test points đo chuẩn.", "P1 (Quan trọng)"),
        ("Tinh chỉnh thông số con trỏ tay", "Con trỏ di chuyển mượt mà; thao tác bấm click không làm lệch trỏ.", "Thử nghiệm thực tế trên người dùng; tối ưu Gain K và vùng chết dead-zone.", "P1 (Quan trọng)"),
        ("Kích hoạt đo điện áp pin trên ADC", "Đọc điện áp pin LiPo qua GPIO34 (ADC1_CH6), phát cảnh báo pin yếu.", "Hiệu chuẩn qua esp_adc_cal, sai số đo điện áp < 0.05V.", "P2 (Mở rộng)"),
        ("Đo kiểm năng lượng & Độ bền 3.3V", "Đo dòng tiêu thụ ở các chế độ Active/Sleep; theo dõi nhiệt độ IMU.", "Thời lượng pin > 8 giờ hoạt động; cảm biến không quá nhiệt ở 3.3V.", "P2 (Hoàn thiện)")
    ]
    for r_idx, r_data in enumerate(plan_rows, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_plan.cell(r_idx, c_idx).paragraphs[0].text = val
    style_academic_table(tbl_plan, [1.6, 2.3, 1.8, 1.0])

    # -------------------------------------------------------------
    # MỤC 8 — KẾT LUẬN & CHỮ KÝ NGHIỆM THU
    # -------------------------------------------------------------
    add_h1("8. KẾT LUẬN & XÁC NHẬN BÁO CÁO")
    
    add_p("Đến mốc đánh giá giữa kỳ ở Tuần 5, nhóm đã hoàn thành toàn diện các nhiệm vụ nền tảng: xác lập kiến trúc phần cứng V4.0.0 trực tiếp 3,3 V, tối ưu hóa bảng dự toán BOM V2.0.0 gồm 23 linh kiện (153.000 VNĐ), xây dựng driver I2C cho ICM-20948, hoàn thiện thuật toán tư thế 6 trục và xử lý con trỏ chuột, đạt 10/10 bài test logic trên máy tính chủ, và đặc biệt là hoàn thành bước Hardware Bring-up ngoại vi cảm biến thực tế: 100/100 lần đọc WHO_AM_I thành công trong phép thử ngắn hạn. Firmware chính đọc lại thanh ghi vật lý thành công cả 4 thanh ghi cấu hình. Báo cáo phân định minh bạch giữa kết quả đo kiểm trên bàn thí nghiệm và các hạng mục còn ở trạng thái chờ thử nghiệm (kết nối máy tính NOT_TESTED và hồ sơ KiCad STALE).")

    # References
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_before = Pt(6)
    p_ref.paragraph_format.space_after = Pt(2)
    r = p_ref.add_run("TÀI LIỆU THAM KHẢO CHÍNH:")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9.5)
    r.font.bold = True
    
    refs = [
        "[1] TDK InvenSense, ICM-20948 Datasheet and Register Map, Doc DS-000189, Rev 1.6, 2024.",
        "[2] NXP Semiconductors, I2C-bus Specification and User Manual, UM10204, Rev 7.0, 2021.",
        "[3] Espressif Systems, ESP32 Technical Reference Manual v5.1 & Hardware Design Guidelines v3.4.",
        "[4] Bluetooth SIG, Human Interface Device (HID) Profile Specification, Version 1.1.1."
    ]
    for rf in refs:
        p_r = doc.add_paragraph(rf)
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(1)
        p_r.paragraph_format.left_indent = Inches(0.2)
        p_r.runs[0].font.name = 'Times New Roman'
        p_r.runs[0].font.size = Pt(8.5)

    # Signature Block Table
    sig_table = doc.add_table(rows=3, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    for col, width in zip(sig_table.columns, [Inches(3.3), Inches(3.3)]):
        for cell in col.cells:
            cell.width = width
            set_cell_margins(cell, top=40, bottom=40, left=40, right=40)

    c00 = sig_table.cell(0, 0).paragraphs[0]
    c01 = sig_table.cell(0, 1).paragraphs[0]
    c01.text = "Hà Nội, ngày 25 tháng 09 năm 2026"
    c01.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c01.runs[0].font.name = "Times New Roman"
    c01.runs[0].font.size = Pt(9.5)
    c01.runs[0].font.italic = True

    c10 = sig_table.cell(1, 0).paragraphs[0]
    c10.text = "GIẢNG VIÊN HƯỚNG DẪN"
    c10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c10.runs[0].font.name = "Times New Roman"
    c10.runs[0].font.size = Pt(10.0)
    c10.runs[0].font.bold = True

    c11 = sig_table.cell(1, 1).paragraphs[0]
    c11.text = "ĐẠI DIỆN NHÓM SINH VIÊN"
    c11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c11.runs[0].font.name = "Times New Roman"
    c11.runs[0].font.size = Pt(10.0)
    c11.runs[0].font.bold = True

    c20 = sig_table.cell(2, 0).paragraphs[0]
    c20.text = "\n\n\n(Ký và ghi rõ họ tên)"
    c20.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c20.runs[0].font.name = "Times New Roman"
    c20.runs[0].font.size = Pt(9.0)
    c20.runs[0].font.italic = True

    c21 = sig_table.cell(2, 1).paragraphs[0]
    c21.text = "\n\n\n(Ký và ghi rõ họ tên)"
    c21.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c21.runs[0].font.name = "Times New Roman"
    c21.runs[0].font.size = Pt(9.0)
    c21.runs[0].font.italic = True

    out_docx = os.path.abspath("deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx")
    doc.save(out_docx)
    print(f"[SUCCESS] Generated condensed progress report docx at: {out_docx}")

if __name__ == "__main__":
    build_report()
