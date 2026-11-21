#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_code_to_report.py — Chèn mục "4.4. Mã nguồn thuật toán xử lý chuyển động" vào
BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx (báo cáo nộp), ngay trước mục "5. CÔNG VIỆC ĐÃ HOÀN THÀNH".

- Code trích NGUYÊN VĂN từ firmware (các khối đã được check_code kiểm tra trùng khớp),
  lấy từ deliverables/BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md mục 12 để hai file luôn giống nhau.
- Sau khi chèn, chạy scripts/format_report_essay.py để đồng bộ định dạng tiểu luận.
- Chạy lại sẽ không chèn trùng (dừng nếu đã có mục 4.4).

Usage: python scripts/add_code_to_report.py
"""
import os
import re
import sys

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, 'BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx')
DETAIL = os.path.join(ROOT, 'deliverables', 'BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md')
CODE_PT = 8.5

# --- lấy các khối code từ mục 12 của file chi tiết -------------------------------------------
md = open(DETAIL, encoding='utf-8').read()
sec12 = md[md.index('# 12. ĐỌC HIỂU CODE'):md.index('# PHỤ LỤC A')]
blocks = re.findall(r'```\n(.*?)```', sec12, re.S)


def block_starting(prefix):
    for b in blocks:
        if b.lstrip().startswith(prefix):
            return b.rstrip('\n')
    raise SystemExit('Không tìm thấy khối code bắt đầu bằng: ' + prefix)


CODE_BYTES = '''uint8_t raw[12];
if (!imu_readBurst(0, REG_ACCEL_XOUT_H, raw, 12)) {
    return false;
}
int16_t raw_gx = (int16_t)(((uint16_t)raw[6] << 8) | raw[7]);
data->gx = (float)raw_gx / ICM20948_GYRO_SCALE_500DPS;'''
CODE_DEADZONE = block_starting('static float apply_deadzone')
CODE_FILTER = block_starting('float accel_norm = sqrtf')
CODE_FSM = block_starting('case SM_GESTURE_ARMED')

# --- nội dung mục 4.4 (văn phong tiểu luận, chỉ nói về báo cáo/firmware, không nhắc tài liệu khác) ---
INTRO = ('Mục này trích bốn đoạn mã ngắn từ firmware (thư mục firmware/) để minh họa các bước chính của '
         'chuỗi xử lý chuyển động ở mục 1.2. Các đoạn mã được trích nguyên văn, chỉ lược bỏ chú thích và '
         'những dòng lặp lại (đánh dấu bằng dấu ...).')

ITEMS = [
    ('4.4.1. Từ số đo thô của cảm biến đến vận tốc góc (icm20948_driver.cpp)', CODE_BYTES,
     'Cảm biến ICM-20948 gửi mỗi trục dưới dạng một số 16 bit, byte cao được gửi trước. Phép dịch trái 8 bit '
     'rồi OR (|) ghép hai byte thành một số; ép sang int16_t để hiểu đó là số có dấu (bù hai); chia cho 65.5 '
     '(độ nhạy LSB trên °/s ở dải ±500 °/s) để ra vận tốc góc tính bằng °/s. Với gia tốc kế, phép chia '
     'tương tự dùng 8192 LSB/g ở dải ±4 g.'),
    ('4.4.2. Vùng chết, hệ số khuếch đại và kẹp giá trị (motion_pipeline.cpp)', CODE_DEADZONE,
     'Vận tốc góc nhỏ hơn 0.8 °/s được coi là rung tay nên bị bỏ qua; từ 0.8 đến 1.4 °/s đầu ra tăng dần theo '
     'đường parabol để con trỏ không bị giật; trên 1.4 °/s đầu ra tăng tuyến tính. Kết quả được nhân hệ số 2.2 '
     'và làm tròn thành độ dời dX, dY. Hàm clamp_i8 kẹp kết quả trong ±127 vì các trường dX, dY của gói HID '
     'là số nguyên 8 bit có dấu; nếu không kẹp, giá trị lớn hơn 127 sẽ tràn và đổi dấu. Dấu trừ ở dy là do '
     'trục Y của màn hình hướng xuống.'),
    ('4.4.3. Bộ lọc bù: khi nào sử dụng gia tốc kế (motion_pipeline.cpp)', CODE_FILTER,
     'Con quay cho tư thế nhanh nhưng bị trôi theo thời gian; gia tốc kế biết hướng trọng lực nhưng bị nhiễu khi '
     'tay chuyển động. Sai lệch e_tilt (tích có hướng giữa hướng trọng lực đo được và hướng trọng lực ước '
     'lượng) chỉ được tính khi độ lớn gia tốc nằm trong khoảng 0.75–1.25 g, tức là tay gần như không có gia '
     'tốc chuyển động; ngoài khoảng này e_tilt bằng 0 và chỉ dùng con quay. Vận tốc xoay áp dụng bằng vận tốc '
     'con quay (đổi sang rad/s) cộng K = 2 s⁻¹ nhân e_tilt, tương ứng hằng số thời gian 0.5 s. Gia tốc kế '
     'không hiệu chỉnh được góc yaw.'),
    ('4.4.4. Nhận diện cử chỉ Flick bằng máy trạng thái (gesture_detector.cpp)', CODE_FSM,
     'Biến s_state lưu bước hiện tại của máy trạng thái. Khi giữ nút Clutch, nếu gia tốc ngang vượt −1.15 g '
     'thì chuyển sang trạng thái PEAK_LEFT; tại đây phải xuất hiện pha hãm ngược lớn hơn +0.35 g trong khoảng '
     '60–450 ms thì mới phát sự kiện Flick trái (lệnh Browser Back) và nghỉ 350 ms; quá 450 ms mà không có pha '
     'hãm thì hủy. Việc đòi hỏi cả hai pha giúp loại bỏ các va chạm một chiều. Flick phải (Browser Forward) '
     'được xử lý đối xứng với chiều ngược lại.'),
]
STATUS = ('Các đoạn mã trên đã được biên dịch thành công bằng PlatformIO và các thuật toán đã chạy qua bộ kiểm '
          'thử trên máy tính (10/10 PASS, xem mục 5). Riêng nút Clutch và các nút bấm chưa được kiểm chứng trên '
          'phần cứng vì breadboard hiện chưa lắp nút; các ngưỡng nêu trên là giá trị ban đầu, chưa được tinh '
          'chỉnh trên người dùng thật.')


def make_par(doc, text, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    return p


def make_code_table(doc, code):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="F4F4F4"/>'))
    tcPr.append(parse_xml(
        f'<w:tcMar {nsdecls("w")}><w:top w:w="80" w:type="dxa"/><w:left w:w="140" w:type="dxa"/>'
        f'<w:bottom w:w="80" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tcMar>'))
    tcPr.append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        + ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="BBBBBB"/>' for s in ('top', 'left', 'bottom', 'right'))
        + '</w:tcBorders>'))
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Cm(0)
    r = p.add_run(code)
    r.font.name = 'Consolas'
    rpr = r._r.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), 'Consolas')
    r.font.size = Pt(CODE_PT)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return tbl


def main():
    doc = docx.Document(REPORT)
    if any(p.text.strip().startswith('4.4.') for p in doc.paragraphs):
        raise SystemExit('Mục 4.4 đã tồn tại, không chèn lại.')
    target = next((p for p in doc.paragraphs if p.text.strip().startswith('5. CÔNG VIỆC ĐÃ HOÀN THÀNH')), None)
    if target is None:
        raise SystemExit('Không tìm thấy mục 5 để chèn trước.')

    def put(el):
        target._p.addprevious(el)

    put(make_par(doc, '4.4. Mã nguồn thuật toán xử lý chuyển động (trích từ firmware)', bold=True)._p)
    put(make_par(doc, INTRO)._p)
    for title, code, expl in ITEMS:
        put(make_par(doc, title, bold=True)._p)
        put(make_code_table(doc, code)._tbl)
        put(make_par(doc, expl)._p)
    put(make_par(doc, STATUS)._p)
    doc.save(REPORT)
    print('[OK] đã chèn mục 4.4 vào', REPORT)


if __name__ == '__main__':
    main()
