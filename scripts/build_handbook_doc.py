import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, '.')
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
import docx_helpers as dh

def build_handbook():
    doc = docx.Document()
    dh.set_page_setup(doc)

    # -------------------------------------------------------------
    # 1. TRANG BÌA CẨM NANG NỘI BỘ (INTERNAL HANDBOOK COVER)
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("[TRƯỜNG ĐẠI HỌC / CƠ SỞ ĐÀO TẠO]")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(0)
    p_dept.paragraph_format.space_after = Pt(24)
    r = p_dept.add_run("[KHOA / BỘ MÔN ĐIỆN TỬ - VIỄN THÔNG / HỆ THỐNG NHÚNG]")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(80, 80, 80)

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(8)
    r = p_badge.add_run("TÀI LIỆU LƯU HÀNH NỘI BỘ — ÔN LUYỆN VẤN ĐÁP BẢO VỆ GIỮA KỲ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(192, 0, 0)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(10)
    r = p_title.add_run("CẨM NANG TOÀN TẬP KIẾN THỨC VÀ BẢO VỆ ĐỒ ÁN\nCHUỘT BAY KHÔNG DÂY (AIR MOUSE BLE HID)\nESP32 CLASSIC + ICM-20948")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(17)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(30)
    r = p_sub.add_run("Kiến trúc chuẩn: \"Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion.\"\n"
                      "Dành cho 3 thành viên: Nắm vững bản chất kiến trúc, Tường minh thanh ghi, Làm chủ giải thuật xử lý (12-byte Burst Read & 6-Axis Fusion), Cẩm nang sự cố, 36 câu vấn đáp & Chuẩn bị Slide thuyết trình")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.italic = True
    r.font.color.rgb = RGBColor(80, 80, 80)

    # Info Box Table
    tbl_info = doc.add_table(rows=6, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Đối tượng sử dụng:", "Toàn thể 03 thành viên nhóm thực hiện đề tài"),
        ("Môn học / Học phần:", "Hệ thống nhúng (Embedded Systems) — Mốc Tuần 5"),
        ("Thành viên 1 (Phần cứng & ESP32):", "[Họ tên sinh viên 1 — MSSV 1]"),
        ("Thành viên 2 (I2C & Thanh ghi IMU):", "[Họ tên sinh viên 2 — MSSV 2]"),
        ("Thành viên 3 (Thuật toán 6 trục & BLE):", "[Họ tên sinh viên 3 — MSSV 3]"),
        ("Phiên bản tài liệu:", "Phiên bản V1.1.0 (Official Defense Master Handbook — 6-Axis Synchronized)")
    ]
    for idx, (label, val) in enumerate(info_data):
        c0 = tbl_info.cell(idx, 0)
        c1 = tbl_info.cell(idx, 1)
        c0.width = Inches(2.6)
        c1.width = Inches(3.8)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        
        r0 = p0.add_run(label)
        r0.font.name = 'Times New Roman'
        r0.font.bold = True
        r0.font.size = Pt(10.5)
        r0.font.color.rgb = RGBColor(31, 78, 121)
        
        r1 = p1.add_run(val)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = RGBColor(34, 34, 34)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(30)
    r = p_date.add_run("Hà Nội, Học kỳ I — Năm học 2025–2026 (Mốc Báo cáo Giữa kỳ Tuần 5)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. MỤC LỤC CẨM NANG (TABLE OF CONTENTS)
    # -------------------------------------------------------------
    p_toc_t = doc.add_paragraph()
    p_toc_t.paragraph_format.space_before = Pt(12)
    p_toc_t.paragraph_format.space_after = Pt(12)
    r = p_toc_t.add_run("MỤC LỤC CẨM NANG KIẾN THỨC NỘI BỘ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 121)
    
    dh.add_toc_field(doc)

    doc.add_page_break()

    # Setup Header / Footer for Handbook
    dh.add_header_footer(doc, 
                         "Cẩm nang kiến thức & Bảo vệ giữa kỳ | Air Mouse BLE HID (ESP32 + ICM-20948)", 
                         "Tài liệu nội bộ — Học phần Hệ thống nhúng")

    def add_h1(text):
        p = doc.add_heading(level=1)
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 121)
        return p

    def add_h2(text):
        p = doc.add_heading(level=2)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(46, 117, 182)
        return p

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(10.5)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(31, 78, 121)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.italic = italic
        r.font.color.rgb = RGBColor(34, 34, 34)
        return p

    # -------------------------------------------------------------
    # PHẦN A — HIỂU TOÀN HỆ THỐNG TRONG 5 PHÚT
    # -------------------------------------------------------------
    add_h1("PHẦN A — HIỂU TOÀN BỘ HỆ THỐNG TRONG 5 PHÚT")
    
    add_h2("A.1. Bản chất cốt lõi: Relative Rate-Control vs Absolute 3D")
    add_p("Khái niệm sống còn mọi thành viên phải nắm vững: Đề tài của nhóm là ", bold_prefix="Khái niệm sống còn: ")
    add_p("THIẾT BỊ TRỎ TƯƠNG ĐỐI ĐIỀU KHIỂN THEO TỐC ĐỘ XOAY (Relative Rate-Controlled Pointing Device).")
    add_p("Kiến trúc chuẩn của hệ thống: \"Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion.\"", bold_prefix="Tuyên bố kiến trúc chính thức: ")
    
    dh.add_callout(doc, "DỄ NHẦM LẪN — PHÂN BIỆT ROTATIONAL MOTION VỚI TRANSLATIONAL MOTION", 
                   "Air Mouse điều khiển con trỏ bằng chuyển động XOAY của cổ tay (Rotational Motion), không phải bằng sự dịch chuyển tịnh tiến của bàn tay (Translational Motion).\n"
                   "Ngay cả khi tâm bàn tay gần như đứng yên trong không gian (không dịch chuyển từ vị trí A sang B), việc xoay cổ tay quanh các trục được ánh xạ (Pitch/Yaw) vẫn tạo ra vận tốc góc (ω tính bằng °/s), firmware vẫn tính toán ra (ΔX, ΔY) và làm con trỏ di chuyển trên màn hình máy tính.\n"
                   "Con trỏ chuột chỉ dừng lại khi: vận tốc góc trên các trục điều khiển xấp xỉ 0 sau khi qua bước bù trừ sai số độ lệch tĩnh (bias) và vùng chết (dead-zone).\n"
                   "GIỚI HẠN PHẠM VI: Tuyệt đối KHÔNG nói với thầy rằng hệ thống 'đo tọa độ tuyệt đối bàn tay trong không gian', 'định vị 3D tuyệt đối', hay 'tay cầm thực tế ảo VR 6DoF'. Thiết bị hoạt động như một con chuột máy tính: chỉ gửi tín hiệu thay đổi vị trí tương đối giữa 2 lần lấy mẫu (ΔX, ΔY).",
                   kind='warning')

    add_p("Tại sao không dùng gia tốc kế (Accelerometer) tích phân 2 lần?", bold_prefix="Câu hỏi bẫy kinh điển: ")
    add_p("Gia tốc kế MEMS luôn chứa sai số độ lệch tĩnh (offset bias ε) và nhiễu ngẫu nhiên. Khi lấy tích phân lần 1 ra vận tốc, sai số tăng tuyến tính theo thời gian: v(t) = v0 + ε·t. Khi lấy tích phân lần 2 ra quãng đường, sai số bùng nổ theo hàm bình phương thời gian: s(t) = s0 + v0·t + (1/2)ε·t². Chỉ sau 2–3 giây, sai số vị trí đã lên tới vài mét, con trỏ chuột sẽ lập tức 'bay mất' khỏi màn hình ngay cả khi thiết bị nằm im trên bàn!")
    add_p("Ngược lại, con quay hồi chuyển (Gyroscope) đo trực tiếp vận tốc góc xoay của cổ tay (đơn vị: độ/giây). Ta chỉ cần nhân vận tốc góc này với một hệ số khuếch đại (Gain) để ra số pixel dịch chuyển con trỏ mà KHÔNG cần tích phân. Khi tay dừng quay (ω = 0), con trỏ dừng lại ngay lập tức, đem lại cảm giác điều khiển tự nhiên, chính xác và không bị bùng nổ trôi dạt.")
    add_p("Gia tốc kế trong hệ thống được giữ lại để phục vụ 2 mục đích sống còn: (1) Dung hợp với Gyroscope trong bộ lọc bù Quaternion 6 trục (Complementary Filter, K=2.0 s⁻¹) để ước lượng trọng trường và bù góc nghiêng cổ tay (Tilt compensation); (2) Nhận diện cử chỉ vẫy nhanh (Flick Left / Flick Right) chuyển slide thuyết trình mà không gây trôi chuột.")

    add_h2("A.2. Dòng luồng dữ liệu 1 trang (System Data Path) — 10 Bước chuẩn mực")
    dh.add_figure(doc, "deliverables/assets/fig_system_block_diagram.png", 
                  "Hình A.1 — Sơ đồ dòng dữ liệu và kiến trúc phần cứng hệ thống Air Mouse", width_in_inches=6.0)

    add_p("• Bước 1: Người dùng xoay cổ tay → Cảm biến ICM-20948 thu nhận gia tốc 3 trục và vận tốc góc 3 trục. ESP32 thực hiện lệnh đọc Burst 12 byte liên tục (imu_readBurst(0, REG_ACCEL_XOUT_H, raw_buffer, 12)) từ địa chỉ 0x2D đến 0x38 tại Bank 0; một giao dịch đọc liên tiếp 12 byte làm giảm độ lệch thời điểm so với đọc từng thanh ghi riêng (không tuyên bố đồng bộ thời gian tuyệt đối hoặc đảm bảo luôn có mẫu mới).", bold_prefix="Dòng luồng 10 bước: ")
    add_p("• Bước 2: Chuyển đổi đơn vị vật lý (LSB Conversion): Ghép 2 byte big-endian thành số nguyên 16-bit có dấu. Gia tốc chia cho 8192.0 LSB/g (dải ±4g); Vận tốc góc chia cho 65.5 LSB/(°/s) (dải ±500 °/s).")
    add_p("• Bước 3: Bù trừ sai số độ lệch tĩnh (Zero-Rate Bias Compensation): Trừ giá trị offset bias tính toán từ pha khởi động gồm 200 lần polling thành công (delay danh định 10 ms, tổng ~2.0 giây).")
    add_p("• Bước 4: Bộ lọc bù Quaternion 6 trục (6-axis Complementary Quaternion Filter): Tích phân vận tốc góc gyro theo công thức vi phân quaternion với chu kỳ lấy mẫu động dt thực tế kẹp [1, 50] ms; dùng vector gia tốc hiệu chỉnh quaternion với hệ số bù K = 2.0 s⁻¹.")
    add_p("• Bước 5: Vector trọng trường thân & Hệ quy chiếu thích nghi: Từ quaternion tư thế, tính toán vector trọng trường trong hệ tọa độ thân v_g để tự động thích nghi hệ quy chiếu tham chiếu (Adaptive Reference Frame Transform), triệt tiêu ảnh hưởng góc nghiêng cổ tay tự nhiên khi cầm thiết bị (không cần trích xuất góc Euler).")
    add_p("• Bước 6: Khung tham chiếu thích nghi & Cơ chế Clutch/Recenter: Tự động điều chỉnh hệ quy chiếu tham chiếu giúp con trỏ di chuyển trực giao khi cổ tay nghiêng. Phím Mode cho phép Clutch tạm dừng hoặc Recenter tái định tâm.")
    add_p("• Bước 7: Vùng chết (Dead-zone): Dead-zone dùng hai ngưỡng: dưới 0.8 °/s đầu ra bằng 0; từ 0.8 đến 1.4 °/s là vùng chuyển tiếp tuyến tính; trên 1.4 °/s áp dụng phần vận tốc vượt ngưỡng thấp. Giá trị 1.2 °/s là ngưỡng Gyro độc lập dùng để nhận diện trạng thái đứng yên.")
    add_p("• Bước 8: Tính toán pixel dịch chuyển con trỏ chuột (Linear Gain Scaling & Clamping): Áp dụng hệ số Gain tuyến tính (Kx = 2.2, Ky = 2.2), làm tròn roundf() và ép giá trị ΔX, ΔY nằm trong khoảng [-127, +127] theo chuẩn HID (không dùng đường cong phi tuyến hay số mũ 1.2).")
    add_p("• Bước 9: Nhận diện cử chỉ vẩy Flick (Gesture Recognition): Bộ máy trạng thái hữu hạn (FSM) giám sát gia tốc tịnh tiến khử trọng trường chiếu lên trục ngang (lateral horizontal axis: a_lateral_g; ngưỡng đỉnh 1.15g, ngưỡng hồi 0.35g, thời gian 60–450 ms, hồi phục cooldown 350 ms) để phát hiện cử chỉ Flick Left / Flick Right chuyển slide.")
    add_p("• Bước 10: Đọc trạng thái nút bấm và đóng gói bản tin BLE HID Mouse Report: Đọc 3 nút nhấn active-low (GPIO25, 26, 27) bằng cơ chế phát hiện sườn cạnh; đóng gói bản tin 5 byte và phát qua sóng vô tuyến BLE 2.4 GHz định kỳ 10–15 ms lên máy tính (kết nối máy tính hiện ở trạng thái NOT_TESTED).")

    dh.add_callout(doc, "TÀI LIỆU KỸ THUẬT BÀN GIAO THIẾT KẾ ĐÍNH KÈM",
"""Để phục vụ việc tự vẽ lại sơ đồ nguyên lý và thiết kế hình ảnh đồ họa sơ đồ khối chuẩn xác, nhóm đã lập 2 tài liệu kỹ thuật chuyên biệt:
1. deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md: Bảng nối dây chân-đến-chân chi tiết 50 dòng theo baseline Direct 3.3V khóa cứng (phân định rõ nhãn in trên module vs GPIO ESP32, quy chuẩn nút bấm 4 chân, bảo vệ cực tính pin và danh mục các chân tuyệt đối cấm nối).
2. deliverables/MO_TA_SO_DO_KHOI_AIR_MOUSE.md: Bản đặc tả chi tiết 6 khối hệ thống, sơ đồ ASCII trực quan và các chỉ dẫn bố cục mỹ thuật chuẩn A4 cho thành viên vẽ hình.""",
                   kind='note')

    add_h2("A.3. 10 điều cốt lõi phải thuộc lòng trước khi bảo vệ")
    dh.add_callout(doc, "10 ĐIỀU PHẢI THUỘC LÒNG (MUST-MEMORIZE)",
"""1. Kiến trúc chuẩn: "Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion." Đây là thiết bị trỏ tương đối điều khiển theo tốc độ xoay cổ tay (Rate-Control), KHÔNG phải định vị 3D tuyệt đối.
2. Dùng Gyroscope đo vận tốc góc (độ/giây); KHÔNG dùng Accelerometer tích phân 2 lần vì sai số trôi bùng nổ theo t². Gia tốc kế được dung hợp qua bộ lọc bù Quaternion 6 trục để ổn định hướng và nhận diện cử chỉ Flick.
3. ESP32 Classic có sẵn BLE v4.2 và xung 240 MHz; mạch đo pin BAT_SENSE dùng chân GPIO34 (ADC1_CH6, Input-Only, cầu phân áp 100kΩ/100kΩ) đã thiết kế phần cứng (trạng thái: HARDWARE_DESIGNED / NOT_YET_IMPLEMENTED_IN_FIRMWARE / NEEDS_HARDWARE_TEST; firmware hiện chưa gọi analogRead(34)).
4. KHÔNG dùng các chân Strapping Pins (GPIO0, GPIO2, GPIO12, GPIO15) cho nút bấm để tránh lỗi boot/nạp flash. Nút bấm đặt tại GPIO25, 26, 27 (active-low, edge-detected; debounce millis() 15–20ms là PLANNED). LED chỉ thị GPIO32 dùng trở 1.0 kΩ.
5. Bus I2C là Open-Drain, bắt buộc có điện trở kéo pull-up (trở kéo 10 kΩ onboard module WCMCU-20948 lên 3.3V). Địa chỉ cảm biến là 0x68 (AD0=0). Lệnh Ghi phát byte 0xD0, lệnh Đọc phát byte 0xD1.
6. ICM-20948 có 4 User Bank với không gian địa chỉ 512 byte (~80–100 thanh ghi hoạt động); muốn truy xuất phải chọn bank qua hàm void imu_selectBank(uint8_t bank) ghi vào thanh ghi REG_BANK_SEL (0x7F).
7. Thanh ghi PWR_MGMT_1 (Bank 0, Addr 0x06) = 0x01 để thoát Sleep (Bit 6=0) và tự động chọn nguồn xung PLL tốt nhất (Bits [2:0]=001, dự phòng dao động nội 20 MHz theo DS-000189 Table 16).
8. Cấu hình cảm biến ở User Bank 2: GYRO_CONFIG_1 (0x01) = 0x1B (DLPF 51.2 Hz, ±500 °/s, độ nhạy 65.5 LSB/(°/s)); ACCEL_CONFIG (0x14) = 0x1B (DLPF 50.4 Hz, Noise BW 68.8 Hz theo Table 18 — Accelerator Configuration, ±4g, độ nhạy 8192 LSB/g); ACCEL_SMPLRT_DIV = 10 cho ODR danh định ≈ 102.27 Hz.
9. Đọc dữ liệu chuyển động theo chế độ Burst 12 byte (imu_readBurst(0, REG_ACCEL_XOUT_H, raw_buffer, 12)) từ 0x2D đến 0x38, thu thập liên tiếp cả Accel (6 byte) và Gyro (6 byte) giúp giảm độ lệch thời điểm so với đọc rời rạc (đã kiểm chứng trên phần cứng thật trong phép thử ngắn hạn).
10. Bản tin chuột qua BLE phụ thuộc vào HID Report Descriptor; bản tin mở rộng thông dụng gồm 5 byte (Buttons, dX, dY, Wheel, Pan).""",
                   kind='note')

    # -------------------------------------------------------------
    # PHẦN B — VI ĐIỀU KHIỂN ESP32
    # -------------------------------------------------------------
    add_h1("PHẦN B — VI ĐIỀU KHIỂN ESP32 VÀ QUY TẮC CHÂN NGOẠI VI")
    
    add_h2("B.1. Vì sao chọn ESP32 Classic mà không chọn STM32?")
    add_p("Trong các đề tài đồ án nhúng truyền thống, sinh viên thường dùng STM32F1/F4 hoặc Arduino Uno. Nhóm chọn ESP32 vì các lý do kỹ thuật mang tính quyết định sau:")
    add_p("• Tích hợp phần cứng BLE trên chip: ESP32 tích hợp sẵn bộ thu phát vô tuyến Bluetooth Low Energy 4.2. Nếu dùng STM32, nhóm bắt buộc phải thiết kế thêm module ngoài (như nRF52 hoặc HC-05 chạy Bluetooth Classic cũ tiêu tốn pin), làm tăng diện tích bo mạch, tăng chi phí linh kiện và phức tạp hóa việc triển khai giao thức HID.", bold_prefix="Lý do 1 (Vô tuyến): ")
    add_p("• Sức mạnh xử lý vượt trội: Vi xử lý lõi kép 32-bit Xtensa LX6 tốc độ 240 MHz, 520 KB SRAM. Khả năng chạy đa nhiệm FreeRTOS cho phép phân chia nhân 0 chuyên trách ngăn xếp mạng BLE và nhân 1 chuyên trách đọc I2C và giải thuật xử lý chuyển động mà không sợ bị trễ nhịp.", bold_prefix="Lý do 2 (Xung nhịp): ")
    add_p("• Giá thành và tính phổ dụng: Bo mạch DevKit 38-pin giá thành rất rẻ, nạp firmware trực tiếp qua cổng USB bằng chip nạp CP2102/CH340 tích hợp, cộng đồng hỗ trợ mã nguồn mở cực kỳ rộng lớn.", bold_prefix="Lý do 3 (Hệ sinh thái): ")

    add_h2("B.2. Bảng quy tắc chân sống còn trên ESP32 DevKit 38-pin")
    dh.add_callout(doc, "CẨM NANG AN TOÀN CHÂN GPIO TRÊN ESP32",
"""• NHÓM CẤM DÙNG (FLASH PINS): GPIO6 đến GPIO11 được nối ngầm bên trong bo mạch với chip nhớ SPI Flash. Tuyệt đối không chạm vào các chân này, nếu cấu hình sẽ gây lỗi Crash hệ thống vĩnh viễn!
• NHÓM STRAPPING PINS: GPIO0 (bootloader), GPIO2 (flashing), GPIO12 (điện áp flash), GPIO15 (JTAG). Tuyệt đối không dùng cho nút bấm cơ khí vì người dùng vô tình bấm nút lúc cấp nguồn sẽ làm ESP32 treo chế độ nạp ROM.
• NHÓM INPUT-ONLY: GPIO34, GPIO35, GPIO36, GPIO39 chỉ có chức năng nhận tín hiệu vào (Digital/Analog In), không có bộ đệm xuất (No Output) và không có điện trở kéo nội. Rất thích hợp làm ngõ vào ADC đo điện áp pin.
• NHÓM AN TOÀN TUYỆT ĐỐI CHO NÚT BẤM VÀ NGOẠI VI:
  - GPIO21: I2C SDA (nối trực tiếp WCMCU-20948, trở kéo 10 kΩ onboard lên 3.3V).
  - GPIO22: I2C SCL (nối trực tiếp WCMCU-20948, trở kéo 10 kΩ onboard lên 3.3V).
  - GPIO25: Nút nhấn chuột trái (BTN_LEFT, Active-Low, INPUT_PULLUP).
  - GPIO26: Nút nhấn chuột phải (BTN_RIGHT, Active-Low, INPUT_PULLUP).
  - GPIO27: Nút bật/tắt chuột bay (BTN_MODE, Active-Low, INPUT_PULLUP).
  - GPIO32: Đèn LED chỉ thị trạng thái kết nối BLE (LED_STATUS) qua trở hạn dòng 1.0 kΩ (1000 Ω).
  - GPIO34: Đo điện áp pin LiPo qua cầu phân áp 100kΩ/100kΩ (thuộc ADC1_CH6).""",
                   kind='warning')

    add_h2("B.3. Bản chất xung đột ADC2 và Lý do chọn GPIO34 (ADC1_CH6)")
    add_p("Nhiều tài liệu không chính xác thường nói rằng 'Bluetooth gây xung đột với ADC2'. Đây là nhận định sai lệch về mặt cơ chế phần cứng.", bold_prefix="Làm rõ bản chất kỹ thuật: ")
    add_p("Trên ESP32 Classic, bộ chuyển đổi tương tự - số SAR ADC2 (gồm các chân GPIO0, 2, 4, 12-15, 25-27) dùng chung mạch phần cứng với bộ điều khiển Wi-Fi thông qua bộ trọng tài phần cứng (Hardware Arbiter). Khi driver Wi-Fi được kích hoạt, nó sẽ chiếm quyền bộ ADC2; nếu gọi hàm analogRead() trên các chân ADC2, hàm sẽ bị từ chối và trả về mã lỗi ESP_ERR_INVALID_STATE.")
    add_p("Giao thức Bluetooth Low Energy (BLE) không khóa ADC2 theo cơ chế này. Tuy nhiên, việc nhóm chọn chân GPIO34 (kênh ADC1_CH6) là chuẩn mực thiết kế phần cứng an toàn trên ESP32 vì: khối ADC1 hoàn toàn độc lập với Wi-Fi/BLE, đồng thời GPIO34 là chân Input-Only, giúp giải phóng các chân GPIO xuất-nhập hai chiều đa dụng cho các nút bấm.")
    add_p("LƯU Ý MINH BẠCH VỀ TIẾN ĐỘ FIRMWARE: Phân hệ đo điện áp pin trên chân GPIO34 hiện ở trạng thái HARDWARE_DESIGNED / NOT_YET_IMPLEMENTED_IN_FIRMWARE / NEEDS_HARDWARE_TEST. Thiết kế phần cứng đã hoàn chỉnh nhưng mã nguồn firmware hiện chưa gọi hàm analogRead(34) mà ưu tiên tập trung hoàn thiện pipeline chuyển động IMU và BLE HID.", italic=True)

    # -------------------------------------------------------------
    # PHẦN C — GIAO THỨC TRUYỀN THÔNG I2C
    # -------------------------------------------------------------
    add_h1("PHẦN C — GIAO THỨC TRUYỀN THÔNG I2C CHUYÊN SÂU")
    
    add_h2("C.1. Cơ chế Cực máng để hở (Open-Drain) và Điện trở kéo lên")
    add_p("Tại sao bus I2C bắt buộc phải có điện trở kéo lên nguồn (Pull-up)?", bold_prefix="Câu hỏi cốt lõi: ")
    add_p("Các chân I2C trên cả vi điều khiển Master lẫn cảm biến Slave đều sử dụng cấu trúc bán dẫn cực máng để hở (Open-Drain đối với MOSFET hoặc Open-Collector đối với BJT). Cấu trúc này chỉ gồm một transistor nối xuống GND. Khi transistor dẫn, chân bị kéo cứng xuống mức LOW (0V). Khi transistor ngắt, chân ở trạng thái thả nổi (Hi-Z), không thể tự phát ra điện áp 3.3V.")
    add_p("Do đó, bus bắt buộc phải có điện trở kéo lên nguồn (Pull-up Resistor). Khi không có linh kiện nào kéo xuống 0, điện trở sẽ kéo đường dây về mức HIGH logic. Cơ chế này tạo nên tính năng logic nối chung (Wired-AND): nếu hai thiết bị vô tình phát tín hiệu ngược nhau cùng lúc, bus chỉ đơn giản bị kéo xuống 0 mà KHÔNG bao giờ xảy ra hiện tượng ngắn mạch chập nguồn.")

    add_h2("C.2. Byte địa chỉ I2C và Bit R/W")
    add_p("Địa chỉ của cảm biến ICM-20948 là địa chỉ 7-bit: 0x68 (hệ nhị phân: 0b1101000). Khi gửi khung truyền trên bus, Master đóng gói địa chỉ này vào 7 bit cao và đặt bit R/W (Read/Write) ở bit thấp nhất (bit 0):")
    add_p("• Khung truyền GHI (Master Write): (0x68 << 1) | 0 = 0xD0 (0b11010000). Dùng khi Master muốn gửi địa chỉ thanh ghi hoặc ghi dữ liệu cấu hình vào cảm biến.")
    add_p("• Khung truyền ĐỌC (Master Read): (0x68 << 1) | 1 = 0xD1 (0b11010001). Dùng khi Master muốn yêu cầu cảm biến đẩy dữ liệu ra đường SDA.")

    add_h2("C.3. Chi tiết từng bước đọc thanh ghi với Repeated START")
    dh.add_figure(doc, "deliverables/assets/fig_i2c_transaction.png", 
                  "Hình C.1 — Sơ đồ thời gian các byte phát trên đường SDA/SCL khi đọc thanh ghi cảm biến", width_in_inches=6.0)
    add_p("Tại sao phải dùng REPEATED START (Sr) mà không phát điều kiện STOP rồi START lại?", bold_prefix="Điểm nhấn bảo vệ: ")
    add_p("Nếu sau khi gửi địa chỉ thanh ghi mục tiêu, Master phát tín hiệu STOP để giải phóng bus rồi mới phát START lại để đọc, trong hệ thống đa Master (Multi-Master) một thiết bị Master khác có thể chen ngang chiếm bus, làm mất dấu vị trí con trỏ thanh ghi vừa chỉ định. Việc sử dụng REPEATED START cho phép Master đổi hướng truyền từ Ghi sang Đọc mà vẫn giữ quyền kiểm soát đường bus liên tục.")

    # -------------------------------------------------------------
    # PHẦN D — CẢM BIẾN CHUYỂN ĐỘNG ICM-20948
    # -------------------------------------------------------------
    add_h1("PHẦN D — CẢM BIẾN CHUYỂN ĐỘNG ICM-20948")
    
    add_h2("D.1. So sánh ICM-20948 với dòng cảm biến cũ MPU-6050")
    tbl_cmp = doc.add_table(rows=7, cols=3)
    headers_cmp = ["Đặc tính kỹ thuật", "MPU-6050 (Thế hệ cũ)", "ICM-20948 (Thế hệ mới sử dụng trong đề tài)"]
    for c_idx, h_text in enumerate(headers_cmp):
        tbl_cmp.cell(0, c_idx).paragraphs[0].text = h_text

    rows_cmp = [
        ("Số trục cảm biến (DOF)", "6 trục (3 trục Gyro + 3 trục Accel)", "9 trục trên phần cứng (3 Gyro + 3 Accel + 3 Từ kế AK09916); firmware hiện triển khai dung hợp 6 trục (6-axis gyro–accelerometer fusion)"),
        ("Điện áp logic I/O (VDDIO)", "3.3 V", "1.8 V raw IC / Nối trực tiếp 3.3 V trên module WCMCU-20948 (đã bỏ BSS138/LDO 1.8V)"),
        ("Bộ lọc số phần cứng (DLPF)", "Bộ lọc DLPF cơ bản", "Hardware DLPF đa dải tần độc lập cho cả Gyroscope và Accelerometer"),
        ("Bộ xử lý chuyển động phần cứng", "DMP cơ bản", "Digital Motion Processor (DMP) thế hệ mới, hỗ trợ offload tính toán"),
        ("Kiến trúc thanh ghi", "1 Bank duy nhất (Không gian địa chỉ phẳng 128 byte)", "4 User Banks (Không gian địa chỉ 512 byte [4 x 128], ~80–100 thanh ghi hoạt động, chọn qua REG_BANK_SEL)"),
        ("Tình trạng sản xuất từ hãng", "Đã ngưng sản xuất (EOL), trôi nổi nhiều chip nhái", "Theo TDK InvenSense, ICM-20948 hiện ở trạng thái NRND / EOL; hoàn toàn phù hợp cho các đồ án nghiên cứu học thuật với phần cứng sẵn có.")
    ]

    for r_idx, r_data in enumerate(rows_cmp, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_cmp.cell(r_idx, c_idx).paragraphs[0].text = val

    dh.set_table_styling(tbl_cmp, col_widths=[1.8, 2.2, 2.4])
    add_p("Bảng D.1 — Bảng so sánh giữa cảm biến ICM-20948 và dòng MPU-6050", italic=True)

    add_h2("D.2. Cơ chế User Bank Switching")
    dh.add_figure(doc, "deliverables/assets/fig_bank_switching.png", 
                  "Hình D.1 — Bản đồ không gian 4 User Bank của cảm biến ICM-20948", width_in_inches=5.8)
    add_p("Quy tắc lập trình nằm lòng: Để đọc được thanh ghi GYRO_CONFIG_1 (nằm ở Bank 2), nếu vi điều khiển chỉ gọi writeReg(0x01, 0x1B) mà không chọn Bank trước, dữ liệu sẽ bị ghi nhầm vào thanh ghi 0x01 của Bank 0 hiện hành, gây sai lệch hoàn toàn hoạt động của cảm biến!", bold_prefix="Cảnh báo sống còn: ")
    add_p("Cấu trúc 4 User Bank theo tài liệu chính thức TDK DS-000189:")
    add_p("• User Bank 0: Chứa thanh ghi PWR_MGMT_1 (0x06), WHO_AM_I (0x00), dữ liệu chuyển động chính ACCEL_X/Y/ZOUT (0x2D–0x32) và GYRO_X/Y/ZOUT (0x33–0x38).")
    add_p("• User Bank 1: Chứa các thanh ghi tự kiểm tra Self-Test, hiệu chuẩn offset bias và timebase.")
    add_p("• User Bank 2: Chứa thanh ghi cấu hình bộ lọc GYRO_CONFIG_1 (0x01), chia tần GYRO_SMPLRT_DIV (0x00), cấu hình gia tốc ACCEL_CONFIG (0x14) và ACCEL_SMPLRT_DIV (0x10, 0x11).")
    add_p("• User Bank 3: Chứa các thanh ghi cấu hình và điều khiển giao tiếp I2C Master nội bộ (I2C_MST_CTRL, I2C_SLVx_ADDR, I2C_SLVx_REG, I2C_SLVx_CTRL).")
    add_p("Lưu ý: Tuyệt đối không nhầm lẫn giữa địa chỉ vật lý 7-bit của chip trên bus (0x68) và địa chỉ thanh ghi tương đối 8-bit trong từng Bank (0x00–0x7F).")

    add_h2("D.3. Thanh ghi định danh WHO_AM_I (Bank 0, Địa chỉ 0x00)")
    add_p("• Địa chỉ: User Bank 0, Địa chỉ 0x00, Quyền truy xuất: Read-Only.", bold_prefix="Đặc tính: ")
    add_p("• Giá trị mặc định của chip xuất xưởng: 0xEA (Hệ nhị phân: 0b11101010).", bold_prefix="Giá trị chuẩn: ")
    add_p("• Ý nghĩa kỹ thuật: Đây là thanh ghi kiểm tra đầu tiên khi khởi động hệ thống. Giá trị 0xEA xác nhận tại thời điểm đó lệnh đọc I2C đã thành công và cảm biến phản hồi đúng định danh mong đợi (đây là bước kiểm tra cần thiết đầu tiên, không phải bảo chứng tuyệt đối cho mọi lỗi phần cứng). Nếu đọc về 0x00 hoặc 0xFF, đây là những manh mối chẩn đoán sự cố (như lỏng dây cắm jumper, cắm lệch hàng chân phải DevKit bên cạnh TX0/RX0, cảm biến mất nguồn 3.3V, sai địa chỉ hoặc bus I2C bị treo kẹt). Đã kiểm chứng 100/100 lần đọc WHO_AM_I=0xEA thành công trong phép thử ngắn hạn trên phần cứng nhóm sở hữu.", bold_prefix="Mục đích: ")

    # -------------------------------------------------------------
    # PHẦN E — BA THANH GHI CỐT LÕI CẦN THUỘC LÒNG
    # -------------------------------------------------------------
    add_h1("PHẦN E — BA THANH GHI CỐT LÕI CẦN THUỘC LÒNG (PWR_MGMT_1, GYRO_CONFIG_1 & ACCEL_CONFIG)")
    
    add_h2("E.1. Thanh ghi PWR_MGMT_1 (Bank 0, Địa chỉ 0x06)")
    dh.add_figure(doc, "deliverables/assets/fig_bitfield_pwr_mgmt_1.png", 
                  "Hình E.1 — Bitfield thanh ghi PWR_MGMT_1 (Giá trị dự án: 0x01)", width_in_inches=5.6)
    
    dh.add_callout(doc, "GIẢNG VIÊN CÓ THỂ HỎI VỀ PWR_MGMT_1",
"""• Thầy hỏi: 'Tại sao lại ghi giá trị 0x01 vào thanh ghi 0x06?'
→ Trả lời ngắn: '0x01 biểu diễn nhị phân là 0b00000001. Trong đó Bit 6 = 0 để đánh thức chip khỏi chế độ ngủ tiết kiệm điện (Sleep) mặc định lúc mới cấp nguồn, và Bits [2:0] = 001 để tự động chọn nguồn xung PLL tốt nhất (dự phòng dao động nội 20 MHz theo DS-000189 Table 16) nhằm đạt xung nhịp ổn định cho ADC/Gyro.'
• Thầy hỏi: 'Bit 4 và Bit 3 có ý nghĩa gì?'
→ Trả lời: 'Theo datasheet TDK DS-000189 bảng 16, Bit 4 là Reserved (luôn ghi 0), Bit 3 là TEMP_DIS (ghi 0 để bật cảm biến nhiệt độ nội, ghi 1 để tắt).'""",
                   kind='teacher')

    add_h2("E.2. Thanh ghi GYRO_CONFIG_1 (Bank 2, Địa chỉ 0x01)")
    dh.add_figure(doc, "deliverables/assets/fig_bitfield_gyro_config_1.png", 
                  "Hình E.2 — Bitfield thanh ghi GYRO_CONFIG_1 (Giá trị dự án: 0x1B)", width_in_inches=5.6)

    dh.add_callout(doc, "GIẢNG VIÊN CÓ THỂ HỎI VỀ GYRO_CONFIG_1",
"""• Thầy hỏi: 'Giải thích giá trị 0x1B của thanh ghi GYRO_CONFIG_1?'
→ Trả lời ngắn: '0x1B biểu diễn nhị phân là 0b00011011. Trong đó:
  - Bit 0 = 1 (GYRO_FCHOICE): Cho phép kích hoạt bộ lọc số dải thông thấp (DLPF Enable).
  - Bits [2:1] = 01 (GYRO_FS_SEL): Cài đặt dải đo toàn thang của con quay hồi chuyển là ±500 °/s.
  - Bits [5:3] = 011 (GYRO_DLPFCFG): Cài đặt tần số cắt của bộ lọc DLPF là 51.2 Hz (Noise Bandwidth 73.3 Hz theo Table 16 datasheet DS-000189) nhằm làm suy giảm đáng kể dao động cơ học tần số cao.
  - Bits [7:6] = 00: Các bit dự trữ.'
• Thầy hỏi: 'Độ nhạy của dải ±500 °/s là bao nhiêu và tính thế nào?'
→ Trả lời: 'Hệ số độ nhạy là 65.5 LSB/(°/s). Được tính từ độ phân giải 16-bit có dấu: 32768 LSB / 500 °/s ≈ 65.536 LSB/(°/s).'""",
                   kind='teacher')

    add_h2("E.3. Thanh ghi ACCEL_CONFIG (Bank 2, Địa chỉ 0x14)")
    dh.add_callout(doc, "GIẢNG VIÊN CÓ THỂ HỎI VỀ ACCEL_CONFIG VÀ ACCEL_SMPLRT_DIV",
"""• Thầy hỏi: 'Giải thích giá trị 0x1B của thanh ghi ACCEL_CONFIG tại Bank 2, địa chỉ 0x14?'
→ Trả lời trực diện: '0x1B biểu diễn nhị phân là 0b00011011. Theo DS-000189 §10.2:
  - Bit 0 = 1 (ACCEL_FCHOICE): Kích hoạt bộ lọc số DLPF cho gia tốc kế.
  - Bits [2:1] = 01 (ACCEL_FS_SEL): Dải đo toàn thang gia tốc kế là ±4g (độ nhạy 8192 LSB/g).
  - Bits [5:3] = 011 (ACCEL_DLPFCFG): Tần số cắt DLPF là 50.4 Hz (3dB BW 50.4 Hz, Noise BW 68.8 Hz theo Table 18 — Accelerator Configuration).
  - Bits [7:6] = 00: Các bit dự trữ.'
• Thầy hỏi: 'Tốc độ lấy mẫu gia tốc kế được đồng bộ như thế nào?'
→ Trả lời: 'Nhóm cấu hình các thanh ghi ACCEL_SMPLRT_DIV_1 (0x10) và ACCEL_SMPLRT_DIV_2 (0x11) ở Bank 2 với giá trị 10 (0x000A). Khi đó, ODR của gia tốc kế đạt: 1125 / (1 + 10) ≈ 102.27 Hz, đồng bộ danh định với tốc độ Gyro ODR ≈ 102.27 Hz (cấu hình qua GYRO_SMPLRT_DIV = 10).'""",
                   kind='teacher')

    # -------------------------------------------------------------
    # PHẦN F — TỪ RAW GYRO ĐẾN CON TRỎ CHUỘT
    # -------------------------------------------------------------
    add_h1("PHẦN F — TỪ RAW DỮ LIỆU ĐẾN CON TRỎ CHUỘT (TOÁN HỌC & GIẢI THUẬT)")
    
    add_h2("F.1. Quy trình toán học từng bước — Pipeline 10 bước")
    dh.add_figure(doc, "deliverables/assets/fig_signal_pipeline.png", 
                  "Hình F.1 — Sơ đồ khối chi tiết Pipeline xử lý tín hiệu chuyển động 6 trục", width_in_inches=6.0)

    add_p("1. Đọc Burst 12 byte: Vi điều khiển gọi hàm imu_readBurst(0, REG_ACCEL_XOUT_H, raw_buf, 12) đọc liên tục 6 byte gia tốc (0x2D–0x32) và 6 byte con quay hồi chuyển (0x33–0x38) tại User Bank 0 trong một giao dịch I2C duy nhất, giúp giảm độ lệch thời điểm so với đọc từng thanh ghi riêng lẻ.", bold_prefix="Bước 1: ")
    add_p("2. Chuyển đổi đơn vị vật lý (LSB Scaling): Ghép 2 byte big-endian thành số nguyên 16-bit có dấu. Gia tốc chia cho 8192.0 LSB/g ra gia tốc trọng trường g; Vận tốc góc chia cho 65.5 LSB/(°/s) ra vận tốc góc (°/s).", bold_prefix="Bước 2: ")
    add_p("3. Bù trừ độ lệch tĩnh Gyro (Zero-Rate Bias): Trừ giá trị offset bias tính toán từ pha khởi động gồm 200 lần polling thành công (delay danh định 10 ms, ~2.0 s): ω_cal = ω_raw - Bias.", bold_prefix="Bước 3: ")
    add_p("4. Bộ lọc bù Quaternion 6 trục (6-axis Complementary Quaternion Filter): Tích phân con quay hồi chuyển tạo quaternion tư thế với chu kỳ động dt kẹp [1, 50] ms. Ước lượng vector sai số hướng từ gia tốc kế e = a_meas × v_g và hiệu chỉnh với hệ số bù liên tục K = 2.0 s⁻¹ (tau ≈ 0.5s), chuẩn hóa quaternion sau mỗi chu kỳ.", bold_prefix="Bước 4: ")
    add_p("5. Vector trọng trường thân & Thích nghi hệ quy chiếu: Firmware tính toán vector trọng trường trong hệ tọa độ thân v_g trực tiếp từ quaternion để tự động duy trì hệ quy chiếu tham chiếu (Adaptive Reference Frame), triệt tiêu ảnh hưởng góc nghiêng cổ tay tự nhiên khi cầm thiết bị (không trích xuất góc Euler).", bold_prefix="Bước 5: ")
    add_p("6. Biến đổi hệ quy chiếu tương đối thích nghi (Adaptive Reference Frame): Chiếu vận tốc góc lên hệ quy chiếu mặt phẳng màn hình tương đối, bù trừ góc nghiêng cổ tay tự nhiên của người dùng. Phím Mode cho phép Clutch tạm dừng hoặc Recenter tái định tâm.", bold_prefix="Bước 6: ")
    add_p("7. Vùng chết (Dead-zone): Dead-zone dùng hai ngưỡng: dưới 0.8 °/s đầu ra bằng 0; từ 0.8 đến 1.4 °/s là vùng chuyển tiếp tuyến tính; trên 1.4 °/s áp dụng phần vận tốc vượt ngưỡng thấp. Giá trị 1.2 °/s là ngưỡng Gyro độc lập dùng để nhận diện trạng thái đứng yên.", bold_prefix="Bước 7: ")
    add_p("8. Tính toán pixel dịch chuyển tuyến tính (Linear Gain Scaling & Clamping): Áp dụng hệ số Gain tuyến tính: ΔX = roundf(K_x · ω_horizontal), ΔY = roundf(-K_y · ω_vertical) với Kx = 2.2, Ky = 2.2; giới hạn chặn Clamping trong khoảng [-127, +127] theo chuẩn HID (không sử dụng hàm phi tuyến hay số mũ 1.2).", bold_prefix="Bước 8: ")
    add_p("9. Nhận diện cử chỉ Flick (Gesture Recognition FSM): Theo dõi gia tốc tịnh tiến khử trọng trường chiếu lên trục ngang (a_lateral_g): vượt ngưỡng đỉnh 1.15g, hoàn hồi dưới 0.35g trong khoảng 60–450 ms, thời gian hồi phục cooldown 350 ms để kích hoạt phím chuyển slide (Flick Left / Flick Right).", bold_prefix="Bước 9: ")
    add_p("10. Đóng gói bản tin BLE HID Mouse Report: Đọc 3 nút nhấn cơ khí active-low (GPIO25, 26, 27) bằng cơ chế phát hiện sườn cạnh; đóng gói bản tin 5 byte (Buttons, ΔX, ΔY, Wheel, Pan) và gửi qua sóng BLE định kỳ 10–15 ms.", bold_prefix="Bước 10: ")

    add_h2("F.2. Phân tích chuyên sâu về Định lý Nyquist và 4 Miền thời gian")
    dh.add_callout(doc, "LÀM RÕ ĐỊNH LÝ NYQUIST — TRÁNH PHÓNG ĐẠI",
"""Thầy có thể hỏi: 'Tần số cắt DLPF 51.2 Hz và chu kỳ lấy mẫu chuột 100 Hz có đảm bảo triệt tiêu hoàn toàn hiện tượng chồng phổ (Aliasing) không?'
→ Cách trả lời chuẩn kỹ thuật:
'Dạ thưa thầy, theo định lý Nyquist-Shannon, tần số lấy mẫu fs = 100 Hz có tần số Nyquist là fN = 50 Hz. Bộ lọc số DLPF với 3dB Bandwidth = 51.2 Hz có đặc tuyến suy hao hữu hạn (chứ không phải bộ lọc đứng dốc lý tưởng), do đó nó chỉ làm suy giảm đáng kể năng lượng nhiễu cao tần chứ KHÔNG triệt tiêu 100% chồng phổ.'
Để bảo vệ luận điểm khoa học vững chắc, nhóm phân định 4 miền thời gian riêng biệt:
1. Đường lấy mẫu tương tự sơ cấp nội bộ cảm biến: Bộ lọc tương tự trước ADC nội (~1.1 kHz).
2. Tốc độ xuất dữ liệu Gyro ODR: Cấu hình qua GYRO_SMPLRT_DIV = 10 cho ra ODR ≈ 102.27 Hz (Nyquist ≈ 51.1 Hz).
3. Chu kỳ vòng lặp đọc của Firmware: Đọc I2C mỗi 10 ms (100 Hz).
4. Chu kỳ gửi gói tin BLE HID (Connection Interval): Gửi báo cáo 10–15 ms lên PC.
Hai phương án đánh đổi nhóm đề xuất khi thử nghiệm firmware:
• Phương án A: Giữ DLPF 51.2 Hz, tăng Gyro ODR lên cao hơn (~200 Hz hoặc 1.1 kHz) để đẩy tần số Nyquist lên trên 100 Hz.
• Phương án B: Giữ ODR ~100 Hz, chọn tần số cắt DLPF thấp hơn (23.9 Hz hoặc 11.6 Hz) để độ suy hao tại 50 Hz sâu hơn.""",
                   kind='teacher')

    # -------------------------------------------------------------
    # PHẦN G — PHÂN HỆ TRUYỀN THÔNG BLE HID
    # -------------------------------------------------------------
    add_h1("PHẦN G — PHÂN HỆ TRUYỀN THÔNG BLE HID (BLUETOOTH LOW ENERGY)")
    
    add_h2("G.1. Kiến trúc HID over GATT Profile (HOGP)")
    add_p("Giao thức BLE hoạt động theo cấu trúc cây phân cấp GATT (Generic Attribute Profile):")
    add_p("• Profile: Human Interface Device (HID) Profile v1.1.1.")
    add_p("• Services: Gồm HID Service (UUID 0x1812), Battery Service (UUID 0x180F) và Device Information Service (UUID 0x180A).")
    add_p("• Characteristics: Nổi bật là Report Characteristic (UUID 0x2A4D) cho phép Server (ESP32) gửi thông báo (Notification) chứa bản tin chuột định kỳ lên Client (Máy tính chủ).")

    add_h2("G.2. Bản tin báo cáo chuột (HID Mouse Report)")
    add_p("Định dạng bản tin chuột KHÔNG cố định mà được quy định bởi HID Report Descriptor. Bản tin 5-byte mở rộng:")
    add_p("• Byte 0 (Buttons): Bit 0 = Nút Trái (1 = Click, 0 = Nhả), Bit 1 = Nút Phải, Bit 2 = Nút Giữa.")
    add_p("• Byte 1 (ΔX): Kiểu số nguyên có dấu 8-bit (int8_t, phạm vi -127 đến +127). Giá trị âm: sang trái; dương: sang phải.")
    add_p("• Byte 2 (ΔY): Kiểu số nguyên có dấu 8-bit (int8_t, phạm vi -127 đến +127). Giá trị âm: lên trên; dương: xuống dưới.")
    add_p("• Byte 3 (Wheel): Cuộn dọc (Vertical Scroll).")
    add_p("• Byte 4 (hWheel): Cuộn ngang (Horizontal Pan).")

    # -------------------------------------------------------------
    # PHẦN H — NGOẠI VI NÚT BẤM, ADC VÀ PIN
    # -------------------------------------------------------------
    add_h1("PHẦN H — NGOẠI VI NÚT BẤM, ADC VÀ QUẢN LÝ NGUỒN PIN")
    
    add_h2("H.1. Nút bấm cơ khí và Thuật toán chống rung phím (Software Debounce)")
    add_p("Khi lá kim loại bên trong nút nhấn cơ học chạm vào nhau, do tính đàn hồi cơ học, chúng bật nhả liên tục trong khoảng 1–5 mili-giây gây ra một chuỗi xung kích ảo (Button Bouncing). Nếu không khử rung, một lần bấm nhẹ của người dùng có thể bị vi điều khiển diễn giải nhầm thành 5–10 cú click chuột liên tiếp!")
    add_p("Mã nguồn firmware hiện tại triển khai cơ chế phát hiện sườn cạnh phím nhấn (Edge Detection) với chân cấu hình INPUT_PULLUP Active-Low. Thuật toán chống rung dội phím trễ millis() 15–20 ms đang ở trạng thái quy hoạch và chuẩn bị kiểm chứng với nút bấm phần cứng thực tế.", bold_prefix="Hiện trạng triển khai: ")
    add_p("Ghi chú phân loại: Ngưỡng debounce 15–20 ms là THÔNG SỐ KHỞI TẠO DỰ ÁN (PROJECT INITIAL VALUE / PLANNED / NEEDS_HARDWARE_TEST).", italic=True)

    add_h2("H.2. Mạch đo áp pin qua ADC1_CH6 (GPIO34)")
    add_p("Điện áp pin LiPo biến thiên từ 3.2V đến 4.2V. Nhóm thiết kế phần cứng sử dụng cầu phân áp gồm R1 = R2 = 100 kΩ để chia đôi điện áp:")
    add_p("V_ADC = V_BAT / 2  →  V_BAT = 2 × V_ADC")
    add_p("Với dải đo 12-bit của ESP32 (giá trị đọc về từ 0 đến 4095) và cấu hình suy hao 11 dB (điện áp toàn thang ~2.45V):")
    add_p("V_ADC = (Raw_ADC / 4095.0) × 2.45 V  →  V_BAT = 2 × ((Raw_ADC / 4095.0) × 2.45 V)")
    add_p("Ghi chú phân loại: Phân hệ đo áp pin BAT_SENSE tại GPIO34 là THIẾT KẾ PHẦN CỨNG ĐÃ HOÀN CHỈNH (HARDWARE_DESIGNED / NOT_YET_IMPLEMENTED_IN_FIRMWARE / NEEDS_HARDWARE_TEST). Firmware hiện chưa gọi hàm analogRead(34) trong vòng lặp chính nhằm tập trung tối đa cho pipeline 6 trục và BLE.", italic=True)

    # -------------------------------------------------------------
    # PHẦN I — BẢNG ĐỐI CHIẾU CÁC QUYẾT ĐỊNH THIẾT KẾ
    # -------------------------------------------------------------
    add_h1("PHẦN I — BẢNG ĐỐI CHIẾU CÁC QUYẾT ĐỊNH THIẾT KẾ (DESIGN TRADE-OFFS)")
    
    add_p("Khi giảng viên hỏi: 'Tại sao nhóm lại làm cách A mà không làm cách B?', các thành viên sử dụng bảng đối chiếu dưới đây để bảo vệ luận điểm khoa học theo cấu trúc: Ràng buộc đề tài → Đánh đổi kỹ thuật → Quyết định của nhóm:")

    trade_offs = [
        ("1. ESP32 Classic vs STM32F4/F1", 
         "Ràng buộc: Cần kết nối không dây BLE HID gọn nhẹ.\nĐánh đổi: STM32 cần mua thêm module BLE ngoài (nRF52/HC-05), làm tăng diện tích PCB và khó cấu hình GATT.\nQuyết định: Chọn ESP32 Classic vì tích hợp sẵn BLE v4.2 và CPU 240 MHz mạnh mẽ."),
        ("2. Giao tiếp I2C vs SPI", 
         "Ràng buộc: Mạch in 1 lớp tự làm (Carrier Board), hạn chế số lượng đường dây.\nĐánh đổi: SPI chạy nhanh hơn (lên tới 7 MHz) nhưng tốn 4 dây (SCK, MOSI, MISO, CS), rất khó đi dây 1 lớp. I2C chỉ cần 2 dây (SDA, SCL), tốc độ 400 kHz hoàn toàn thừa đáp ứng chu kỳ lấy mẫu chuột 100 Hz (đọc 12 byte burst chỉ mất ~0.38 ms, chiếm ~3.8% chu kỳ 10 ms).\nQuyết định: Chọn I2C Fast Mode 400 kHz cho V1."),
        ("3. Tự viết driver thanh ghi vs Dùng thư viện trọn gói", 
         "Ràng buộc: Báo cáo giữa kỳ yêu cầu giải thích cặn kẽ thanh ghi và bitfield trước giảng viên.\nĐánh đổi: Thư viện lớn (như SparkFun DMP) nạp firmware nhị phân DMP vài chục KB biến hệ thống thành 'hộp đen' khó giải thích, tốn Flash/RAM.\nQuyết định: Tự viết driver thanh ghi mỏng qua Wire.h để làm chủ hoàn toàn bitfield."),
        ("4. Dùng Gyroscope vs Accelerometer tích phân 2 lần", 
         "Ràng buộc: Con trỏ chuột phải phản hồi tức thời theo tay và không bị trôi.\nĐánh đổi: Gia tốc kế đo gia tốc tịnh tiến, tích phân 2 lần làm sai số bias bùng nổ theo hàm bình phương thời gian (t²). Gyroscope đo trực tiếp vận tốc góc (độ/giây), tỉ lệ thuận với ý định di chuột, không cần tích phân. Tuy nhiên, gia tốc kế vẫn được giữ lại để dung hợp trong bộ lọc bù Quaternion 6 trục và nhận diện cử chỉ Flick.\nQuyết định: Dùng Gyroscope điều khiển tốc độ trỏ (Rate Control) và Accel để ổn định hướng + cử chỉ."),
        ("5. Vì sao không dùng Magnetometer trong V1", 
         "Ràng buộc: Hoạt động ổn định trong văn phòng và tiết kiệm pin.\nĐánh đổi: Từ kế AK09916 đo từ trường Trái Đất để định hướng tuyệt đối hướng Bắc, nhưng môi trường văn phòng có quá nhiều nhiễu từ (loa laptop, khung sắt bàn). Hiệu chuẩn từ trường cứng/mềm rất phức tạp và chuột trỏ chỉ cần chuyển động tương đối.\nQuyết định: Tắt từ kế trong V1 để giảm tải bus I2C và tiết kiệm năng lượng."),
        ("6. Vì sao chọn Bộ lọc bù Quaternion 6 trục thay vì Kalman Filter", 
         "Ràng buộc: Tối ưu thời gian xử lý, giảm độ trễ phản hồi con trỏ chuột và tiết kiệm tài nguyên vi điều khiển.\nĐánh đổi: Bộ lọc Kalman Filter yêu cầu nghịch đảo ma trận hiệp phương sai 4x4 hoặc 6x6, tiêu tốn năng lực tính toán dấu phẩy động và có nguy cơ trễ nhịp vòng lặp 10 ms. Bộ lọc bù Quaternion 6 trục với hệ số K = 2.0 s⁻¹ cho phép ước lượng tư thế ổn định với thời gian thực thi cực ngắn (< 0.05 ms) mà không cần nghịch đảo ma trận.\nQuyết định: Triển khai 6-axis Complementary Quaternion filter cho pipeline V1."),
        ("7. Vì sao chọn GPIO34 (ADC1_CH6)", 
         "Ràng buộc: Tránh xung đột tài nguyên phần cứng và tối ưu chân IO.\nĐánh đổi: Khối SAR ADC2 bị xung đột phần cứng với Wi-Fi trên ESP32. GPIO34 thuộc ADC1 (không xung đột) và là chân Input-Only, giúp dành các chân IO 2 chiều cho nút bấm.\nQuyết định: Chọn GPIO34 cho tín hiệu đo áp pin BAT_SENSE.")
    ]

    for title, content in trade_offs:
        add_p(content, bold_prefix=title + ":\n")

    # -------------------------------------------------------------
    # PHẦN J — CẨM NANG XỬ LÝ SỰ CỐ PHẦN CỨNG & PHẦN MỀM
    # -------------------------------------------------------------
    add_h1("PHẦN J — CẨM NANG XỬ LÝ SỰ CỐ PHẦN CỨNG & PHẦN MỀM (TROUBLESHOOTING GUIDE)")
    
    add_p("Khi đem mạch lên lớp demo mà xảy ra lỗi, các thành viên bình tĩnh tra cứu cẩm nang sự cố 3 cột: Triệu chứng → Nguyên nhân khả dĩ → Cách kiểm tra khắc phục:")

    tbl_debug = doc.add_table(rows=12, cols=3)
    headers_debug = ["Hiện tượng / Triệu chứng (Symptom)", "Nguyên nhân khả dĩ (Possible Causes)", "Cách kiểm tra và khắc phục (Actionable Checks)"]
    for c_idx, h_text in enumerate(headers_debug):
        tbl_debug.cell(0, c_idx).paragraphs[0].text = h_text

    rows_debug = [
        ("Serial Monitor báo: WHO_AM_I = 0x00 hoặc 0xFF", 
         "• Đứt/lỏng dây SDA hoặc SCL, cắm lỏng jumper hoặc cắm lệch hàng chân phải DevKit (chân TX0/RX0 nằm xen giữa GPIO22 và GPIO21)\n• Cảm biến mất nguồn 3.3V\n• Sai địa chỉ I2C hoặc bus bị kẹt", 
         "1. Đo VOM chân VCC của ICM-20948 xem có đủ 3.3V không.\n2. Kiểm tra cắm đúng chân GPIO21/22, tránh cắm nhầm hàng chân TX0/RX0.\n3. Kiểm tra thông mạch dây SDA/SCL và tiếp xúc jumper.\n4. Chạy I2C Scanner dò tìm phản hồi ACK."),
        ("Hàm Wire.endTransmission() trả về mã lỗi 2 (NACK Addr)", 
         "• Sai địa chỉ I2C của cảm biến\n• Chân AD0 đang nối lên 3.3V thay vì nối GND (địa chỉ biến thành 0x69)", 
         "1. Đo chân AD0 trên module cảm biến: phải ở mức 0V.\n2. Nạp code I2C Scanner để quét địa chỉ thực tế trên bus."),
        ("Bus I2C bị treo vĩnh viễn (Wire.endTransmission() đứng im)", 
         "• Slave bị reset giữa chừng, giữ chặt đường SDA ở mức LOW\n• Thiếu điện trở kéo pull-up", 
         "1. Đo áp trên SDA/SCL lúc nghỉ: phải ở mức 3.3V.\n2. Viết hàm phát 9 xung clock trên chân SCL lúc khởi động để ép Slave giải phóng SDA."),
        ("Ghi thanh ghi không có tác dụng hoặc đọc dữ liệu rác", 
         "• Quên chọn User Bank tương ứng trước khi truy xuất", 
         "1. Kiểm tra lại mã nguồn: trước khi ghi thanh ghi ở Bank 2 (như GYRO_CONFIG_1, ACCEL_CONFIG), bắt buộc phải có lệnh imu_selectBank(2) ghi vào thanh ghi 0x7F."),
        ("Cảm biến đặt yên trên bàn nhưng con trỏ chuột tự trôi (Drift)", 
         "• Chưa thực hiện hiệu chuẩn bù sai số tĩnh (Zero-Rate Bias)\n• Lúc khởi động bị rung tay", 
         "1. Giữ chuột bất động hoàn toàn trong 2.0 giây đầu bật nguồn.\n2. Kiểm tra thuật toán lấy mẫu 200 lần polling thành công (delay 10 ms) xem có tính trung bình cộng chính xác không."),
        ("Con trỏ chuột rung rinh tại chỗ khi cố định tay (Jitter)", 
         "• Ngưỡng vùng chết (Dead-zone) quá nhỏ\n• Rung tay sinh lý chưa được triệt tiêu", 
         "1. Đề xuất thực nghiệm tương lai: Tinh chỉnh tăng ngưỡng Dead-zone vượt qua mức rung sinh lý thực tế (ví dụ từ 0.8 °/s lên 1.4 °/s hoặc cao hơn).\n2. Kiểm tra xem Bit 0 (GYRO_FCHOICE) của GYRO_CONFIG_1 đã kích hoạt bộ lọc DLPF chưa."),
        ("Con trỏ chuột rê quá nhanh hoặc quá chậm", 
         "• Nhầm lẫn hệ số độ nhạy Sensitivity (65.5 LSB/(°/s))\n• Hệ số Gain phần mềm K chưa phù hợp", 
         "1. Kiểm tra công thức: phải chia cho 65.5 trước khi nhân Gain.\n2. Điều chỉnh hệ số Gain K trong mã nguồn firmware."),
        ("Đột ngột mất kết nối BLE (BLE Disconnect)", 
         "• Nguồn pin LiPo bị sụt áp khi mạch phát sóng RF đỉnh cao\n• Khoảng cách xa hoặc ăng-ten bị kim loại che chắn", 
         "1. Đo điện áp pin LiPo xem có bị tụt dưới 3.4V không.\n2. Bổ sung tụ hóa 100uF song song nguồn 5V/3.3V để gánh dòng đỉnh RF."),
        ("Nhấn nút 1 lần nhưng máy tính nhận thành 2-3 click", 
         "• Hiện tượng dội phím cơ học (Button Bouncing)", 
         "1. Kiểm tra cơ chế phát hiện sườn cạnh phím nhấn trong mã nguồn (thuật toán millis() debounce 15–20 ms đang ở trạng thái quy hoạch kiểm chứng thực nghiệm)."),
        ("Điện áp đo pin ADC trả về giá trị cố định hoặc sai lệch", 
         "• Chân phân áp bị hở mạch\n• Cấu hình sai mức suy hao Attenuation\n• Phân hệ ADC chưa được firmware gọi", 
         "1. Đo áp thực tế tại chân GPIO34 bằng đồng hồ VOM (phải bằng 1/2 áp pin).\n2. Ghi nhớ rằng phân hệ đo pin hiện là HARDWARE_DESIGNED, firmware chưa gọi analogRead(34)."),
        ("Bo mạch ESP32 bị reset liên tục lúc bật nguồn (Bootloop)", 
         "• Chân GPIO0 hoặc GPIO2 bị kéo xuống LOW bất thường\n• Sụt áp nguồn 5V VIN", 
         "1. Rút dây nối nút bấm kiểm tra xem có chân strapping nào bị chập mass lúc boot không.")
    ]

    for r_idx, r_data in enumerate(rows_debug, start=1):
        for c_idx, val in enumerate(r_data):
            tbl_debug.cell(r_idx, c_idx).paragraphs[0].text = val

    dh.set_table_styling(tbl_debug, col_widths=[2.1, 2.1, 2.2])
    add_p("Bảng J.1 — Cẩm nang chẩn đoán và khắc phục 11 sự cố kỹ thuật điển hình", italic=True)

    # -------------------------------------------------------------
    # PHẦN K — BẢNG TỔNG HỢP RESEARCH GAPS CÒN LẠI
    # -------------------------------------------------------------
    add_h1("PHẦN K — BẢNG TỔNG HỢP RESEARCH GAPS CÒN LẠI (HẠNG MỤC CẦN KIỂM CHỨNG)")
    
    add_p("Để đảm bảo tính trung thực khoa học tuyệt đối, nhóm công khai các hạng mục kỹ thuật đã hoàn thành Bring-up và các hạng mục còn lại cần kiểm chứng thực nghiệm:")

    dh.add_callout(doc, "HẠNG MỤC ĐÃ HOÀN THÀNH BRING-UP (BENCH_VERIFIED_ON_OWNED_MODULE)",
"""1. Giao tiếp I2C trực tiếp 3.3V giữa ESP32 DevKit 38-pin và module WCMCU-20948 (GPIO21 SDA, GPIO22 SCL, 400 kHz).
2. Định danh cảm biến WHO_AM_I (0x00 Bank 0): 100/100 lần đọc trả về đúng 0xEA trong phép thử ngắn hạn.
3. Đọc lại 4 thanh ghi cấu hình vật lý thành công: PWR_MGMT_1 (0x01), GYRO_CONFIG_1 (0x1B), ACCEL_CONFIG (0x1B), SMPLRT_DIV (10).
4. Đọc burst 12 byte dữ liệu thô (Accel + Gyro) ổn định, dữ liệu Accel Z ~ +1g và Gyro tĩnh ~ 0 dps.""",
                   kind='note')

    dh.add_callout(doc, "HẠNG MỤC CÒN LẠI CẦN KIỂM CHỨNG (REMAINING GAPS)",
"""1. Kiểm thử kết nối không dây BLE HID thực tế với PC và đo độ trễ truyền gói tin chuột 100 Hz (trạng thái: NOT_TESTED).
2. Đồng bộ sơ đồ nguyên lý KiCad và layout loại bỏ BSS138/AMS1117-1.8V qua KiCad MCP Server.
3. Gia công mạch in Carrier Board 1 lớp và lắp ráp tích hợp bo hoàn chỉnh.
4. Tinh chỉnh thực tế hai ngưỡng vùng chết Dead-zone (0.8 °/s và 1.4 °/s) cùng Gain K trên tay người dùng.
5. Triển khai lệnh analogRead(34) trong firmware để đo điện áp pin LiPo thực tế.
6. Đo kiểm dòng tiêu thụ năng lượng và đánh giá độ bền hoạt động lâu dài ở mức 3.3V.""",
                   kind='warning')

    # -------------------------------------------------------------
    # PHẦN L — NGÂN HÀNG 36 CÂU HỎI VẤN ĐÁP BẢO VỆ GIỮA KỲ
    # -------------------------------------------------------------
    add_h1("PHẦN L — NGÂN HÀNG 36 CÂU HỎI VẤN ĐÁP BẢO VỆ GIỮA KỲ (Q&A DEFENSE BANK)")
    
    add_p("Toàn bộ 36 câu hỏi dưới đây được chuẩn hóa và phân chia theo 12 nhóm chủ đề kỹ thuật cốt lõi, trang bị đầy đủ câu trả lời trực diện (15–30 giây), giải thích chuyên sâu, từ khóa cốt lõi và nguồn tài liệu trích dẫn để cả 3 thành viên tự tin bảo vệ đề tài trước hội đồng:")

    # Read the Q&A from docs/MIDTERM_QA_BANK.md and inject into document with beautiful structure
    qa_path = 'docs/MIDTERM_QA_BANK.md'
    if os.path.exists(qa_path):
        with open(qa_path, 'r', encoding='utf-8') as fp:
            qa_content = fp.read()
        
        # Split by ### Câu
        import re
        q_blocks = re.split(r'### Câu\s+(\d+):', qa_content)
        # q_blocks[0] is header, then 1, text1, 2, text2, ...
        q_count = 0
        for i in range(1, len(q_blocks), 2):
            q_num = q_blocks[i].strip()
            q_body = q_blocks[i+1].strip()
            q_count += 1
            
            # Extract question title
            lines = q_body.split('\n')
            q_title = lines[0].strip()
            
            p_q = doc.add_paragraph()
            p_q.paragraph_format.space_before = Pt(8)
            p_q.paragraph_format.space_after = Pt(2)
            p_q.paragraph_format.keep_with_next = True
            rq_num = p_q.add_run(f"Câu {q_num}: {q_title}")
            rq_num.font.name = 'Times New Roman'
            rq_num.font.bold = True
            rq_num.font.size = Pt(11)
            rq_num.font.color.rgb = RGBColor(31, 78, 121)
            
            # Print body lines
            for line in lines[1:]:
                line_s = line.strip()
                if not line_s:
                    continue
                if line_s.startswith("- **Trả lời ngắn**:"):
                    ans_short = line_s.replace("- **Trả lời ngắn**:", "").strip()
                    add_p(ans_short, bold_prefix="• Trả lời trực diện (15–30s): ")
                elif line_s.startswith("- **Giải thích chuyên sâu**:"):
                    ans_deep = line_s.replace("- **Giải thích chuyên sâu**:", "").strip()
                    add_p(ans_deep, bold_prefix="• Giải thích chuyên sâu: ")
                elif line_s.startswith("- **Nguồn chứng minh**:"):
                    ans_src = line_s.replace("- **Nguồn chứng minh**:", "").strip()
                    add_p(ans_src, bold_prefix="• Nguồn trích dẫn: ", italic=True)
                elif line_s.startswith("- ") or line_s.startswith("  - "):
                    add_p("  " + line_s)
                else:
                    add_p(line_s)
        print(f"Loaded and formatted {q_count} Q&A questions into handbook.")

    # -------------------------------------------------------------
    # PHẦN M — CHEAT SHEET 2 TRANG TÓM TẮT SIÊU TỐC
    # -------------------------------------------------------------
    doc.add_page_break()
    add_h1("PHẦN M — CHEAT SHEET 2 TRANG TÓM TẮT SIÊU TỐC (IN 2 MẶT A4 TRƯỚC GIỜ THI)")
    
    add_p("Phần tóm lược ngắn gọn nhất toàn bộ thông số kỹ thuật cốt lõi của đề tài, thiết kế để 3 thành viên có thể in ra 2 mặt của một tờ giấy A4 để xem lại nhanh trong 5 phút trước khi bước vào phòng vấn đáp:")

    dh.add_callout(doc, "CHEAT SHEET — MẶT TRƯỚC: THÔNG SỐ VÀ THANH GHI CỐT LÕI",
"""1. BẢN CHẤT HỆ THỐNG & KIẾN TRÚC CHUẨN:
   • "Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion."
   • Relative Rate-Controlled Pointing Device: Con trỏ di chuyển tỉ lệ thuận với vận tốc góc xoay cổ tay (ω).
   • Dừng tay (ω = 0) → Con trỏ dừng ngay lập tức. KHÔNG định vị 3D tuyệt đối, KHÔNG dùng gia tốc kế tích phân 2 lần (trôi t²).

2. PHẦN CỨNG & BỐ TRÍ CHÂN (CURRENT DESIGN / PROVISIONAL):
   • I2C SDA: GPIO21  |  I2C SCL: GPIO22 (Fast Mode 400 kHz, WCMCU-20948 nối trực tiếp ESP32 3.3V, trở kéo 10kΩ tích hợp sẵn trên module lên 3.3V; đã BENCH_VERIFIED_ON_OWNED_MODULE).
   • NÚT BẤM: BTN_LEFT (GPIO25), BTN_RIGHT (GPIO26), BTN_MODE (GPIO27) — Cấu hình INPUT_PULLUP Active-Low.
   • CHỈ THỊ: LED_STATUS (GPIO32) qua trở hạn dòng 1.0 kΩ (1000 Ω).
   • ĐO PIN: BAT_SENSE (GPIO34 / ADC1_CH6) — Input-Only, thuộc ADC1 tránh xung đột Wi-Fi, cầu phân áp 100kΩ/100kΩ.
     Trạng thái: HARDWARE_DESIGNED / NOT_YET_IMPLEMENTED_IN_FIRMWARE / NEEDS_HARDWARE_TEST; firmware hiện chưa gọi analogRead(34).
   • CẤM DÙNG: GPIO6-11 (Flash nội), GPIO0, 2, 12, 15 (Strapping pins).

3. BA THANH GHI SỐNG CÒN CỦA ICM-20948 (TDK DS-000189):
   • PWR_MGMT_1 (User Bank 0, Địa chỉ 0x06) = 0x01 (0b00000001):
     - Bit 7: DEVICE_RESET = 0 (Bình thường)
     - Bit 6: SLEEP = 0 (Thoát chế độ ngủ mặc định, đánh thức chip)
     - Bit 5: LP_EN = 0 (Tắt chế độ tiết kiệm năng lượng, đo liên tục)
     - Bit 4: Reserved = 0 (Bit dành riêng)
     - Bit 3: TEMP_DIS = 0 (Bật cảm biến nhiệt độ nội)
     - Bits [2:0]: CLKSEL = 001 (Tự động chọn nguồn xung PLL tốt nhất, dự phòng dao động nội 20 MHz theo DS-000189 Table 16)
   • GYRO_CONFIG_1 (User Bank 2, Địa chỉ 0x01) = 0x1B (0b00011011):
     - Bits [7:6]: Reserved = 00
     - Bits [5:3]: GYRO_DLPFCFG = 011 (DLPF 51.2 Hz, Noise BW 73.3 Hz theo Table 16)
     - Bits [2:1]: GYRO_FS_SEL = 01 (Dải đo con quay hồi chuyển ±500 °/s, độ nhạy 65.5 LSB/(°/s))
     - Bit 0: GYRO_FCHOICE = 1 (Kích hoạt bộ lọc số DLPF)
   • ACCEL_CONFIG (User Bank 2, Địa chỉ 0x14) = 0x1B (0b00011011):
     - Bits [7:6]: Reserved = 00
     - Bits [5:3]: ACCEL_DLPFCFG = 011 (DLPF 50.4 Hz, Noise BW 68.8 Hz theo Table 18 — Accelerator Configuration)
     - Bits [2:1]: ACCEL_FS_SEL = 01 (Dải đo gia tốc kế ±4g, độ nhạy 8192 LSB/g)
     - Bit 0: ACCEL_FCHOICE = 1 (Kích hoạt bộ lọc số DLPF)
     - ACCEL_SMPLRT_DIV (0x10, 0x11) = 10 cho ODR danh định ≈ 102.27 Hz đồng bộ Gyro.

4. CƠ CHẾ CHUYỂN USER BANK VÀ CÁC LỆNH API CHUẨN C:
   • Thanh ghi REG_BANK_SEL tại địa chỉ 0x7F (cố định trên cả 4 Bank): Ghi 0x00 (Bank 0), 0x10 (Bank 1), 0x20 (Bank 2), 0x30 (Bank 3).
   • Danh mục API C chính thức:
     - void imu_selectBank(uint8_t bank): Chọn User Bank (0, 1, 2, 3) qua thanh ghi REG_BANK_SEL (0x7F).
     - bool imu_writeReg(uint8_t bank, uint8_t reg, uint8_t val): Ghi 1 byte cấu hình vào thanh ghi mục tiêu; trả về bool (true: ACK/thành công, false: NACK/thất bại).
     - uint8_t imu_readReg(uint8_t bank, uint8_t reg): Đọc 1 byte từ thanh ghi mục tiêu; trả về byte đọc được (0x00 nếu lỗi, không có kênh mã lỗi riêng).
     - bool imu_readBurst(uint8_t bank, uint8_t reg, uint8_t* buffer, size_t length): Đọc Burst liên tục nhiều byte từ bank chỉ định; trả về bool (true: thành công, false: lỗi).
     - bool imu_readData(imu_data_t* data): Đọc burst 12 byte từ Bank 0 và giải mã số học 16-bit vào struct imu_data_t; trả về bool (true: thành công, false: lỗi).""",
                   kind='note')

    dh.add_callout(doc, "CHEAT SHEET — MẶT SAU: TOÁN HỌC, PIPELINE VÀ 5 CÂU HỎI TRỌNG TÂM CỦA THẦY",
"""5. CÔNG THỨC TOÁN HỌC & ĐỘ NHẠY:
   • Độ nhạy Gyro (dải ±500 °/s): 32768 / 500 = 65.536 LSB/(°/s) → ω = (Raw_Gyro - Bias) / 65.5 (°/s).
   • Độ nhạy Accel (dải ±4g): 32768 / 4 = 8192 LSB/g → a = Raw_Accel / 8192.0 (g).
   • Điện áp pin LiPo: V_BAT = 2 × V_ADC = 2 × ((Raw_ADC / 4095.0) × 2.45 V) (Hardware designed).

6. PIPELINE XỬ LÝ CHUYỂN ĐỘNG 10 BƯỚC:
   12-byte Burst Read (0x2D–0x38 tại Bank 0) → Đổi đơn vị vật lý (/8192, /65.5) → Bù Offset Bias (200 polls, ~2.0s) →
   6-axis Complementary Quaternion (K=2.0 s⁻¹, dynamic dt) → Vector trọng trường thân v_g & Adaptive Reference Frame →
   Vùng chết Dead-zone hai ngưỡng chuyển tiếp (0.8 °/s và 1.4 °/s) → Linear Gain Scaling (Kx=2.2, Ky=2.2) & Clamping [-127, +127] →
   Nhận diện cử chỉ Flick (1.15g / 0.35g, 60–450 ms) → Đọc nút bấm Active-Low & Đóng gói BLE HID Report (5 bytes).

7. 5 CÂU HỎI TRỌNG TÂM CỦA GIẢNG VIÊN VÀ TỪ KHÓA TRẢ LỜI TRỰC DIỆN:
   1. Đề tài làm gì? Kiến trúc ra sao?
      → "Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion." Thiết bị trỏ tương đối theo tốc độ xoay cổ tay (Rate-Control), không phải định vị 3D tuyệt đối.
   2. Phân bổ ngoại vi ESP32 thế nào? Chân nào tuyệt đối cấm dùng?
      → Phân định ngoại vi ESP32 vs ICM-20948. Tuyệt đối cấm GPIO6-11 (Flash) và GPIO0, 2, 12, 15 (Strapping). GPIO34 Input-Only thuộc ADC1 (tránh xung đột Wi-Fi). LED GPIO32 trở 1.0 kΩ. Nút bấm GPIO25, 26, 27.
   3. Giao tiếp I2C hoạt động ra sao? Tại sao cần trở kéo? Địa chỉ cảm biến?
      → Cực máng để hở Open-Drain cần trở kéo pull-up (10kΩ tích hợp sẵn trên module WCMCU-20948 lên 3.3V) để tạo mức HIGH và Wired-AND. Module nối trực tiếp 3.3V không qua BSS138. Địa chỉ 0x68 (AD0=0). Ghi phát 0xD0, Đọc phát 0xD1. Dùng Repeated START giữ bus.
   4. Cảm biến ICM-20948 có kiến trúc ra sao? Nêu chi tiết bitfield 3 thanh ghi cốt lõi?
      → 4 User Bank chọn qua REG_BANK_SEL (0x7F). PWR_MGMT_1 (0x06) = 0x01 (thoát Sleep, auto PLL). GYRO_CONFIG_1 (0x01) = 0x1B (DLPF 51.2Hz, ±500 °/s, 65.5 LSB/(°/s)). ACCEL_CONFIG (0x14) = 0x1B (DLPF 50.4Hz, ±4g, 8192 LSB/g, ODR ≈ 102.27 Hz theo Table 18 — Accelerator Configuration). Đọc 12 byte burst từ 0x2D đến 0x38.
   5. Dòng dữ liệu từ cổ tay đến con trỏ máy tính đi qua các bước nào?
      → 10 bước pipeline: 12-byte burst read → LSB scale (/8192, /65.5) → Bias comp (200 polls) → 6-axis Complementary Quaternion (K=2.0 s⁻¹) → Adaptive frame → Deadzone hai ngưỡng chuyển tiếp (0.8 °/s và 1.4 °/s) → Linear Gain scaling & Clamping → Flick gesture (1.15g / 0.35g, 60–450 ms) → BLE HID Report (5 bytes).""",
                   kind='success')

    # -------------------------------------------------------------
    # PHẦN N — BẢN ĐỒ DÀN Ý CHUẨN BỊ SLIDE THUYẾT TRÌNH
    # -------------------------------------------------------------
    add_h1("PHẦN N — BẢN ĐỒ DÀN Ý CHUẨN BỊ SLIDE THUYẾT TRÌNH (10 SLIDES CHUẨN)")
    
    add_p("Nhóm không tạo file PowerPoint trong task này, nhưng chuẩn bị sẵn cấu trúc dàn ý 10 Slide thuyết trình chuẩn mực để các thành viên tự thiết kế slide sau đó:")

    slides_map = [
        ("Slide 1: Đặt vấn đề & Mục tiêu đề tài", 
         "• Giới thiệu đề tài: Air Mouse BLE HID dùng ESP32 + ICM-20948.\n• Tuyên bố kiến trúc: Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion.\n• Nêu bật bản chất: Relative Rate-Controlled Pointing Device.\n• Mục tiêu: Thuyết trình, Smart TV, hỗ trợ người khuyết tật vận động.", 
         "Hình ảnh mô phỏng thao tác vung cổ tay điều khiển con trỏ chuột.", 
         "TUYỆT ĐỐI KHÔNG ghi 'định vị tuyệt đối 3D' hoặc hình ảnh kính thực tế ảo VR 6DOF."),
        ("Slide 2: Sơ đồ kiến trúc toàn hệ thống", 
         "• Dòng luồng dữ liệu từ Cổ tay → IMU 6 trục → ESP32 → BLE HID → PC.\n• Nêu rõ vai trò của từng khối linh kiện (Nguồn LiPo/TP4056/MT3608, MCU ESP32 DevKit, IMU WCMCU-20948 nối trực tiếp 3.3V, Nút bấm, LED trở 1.0 kΩ).", 
         "Sơ đồ khối toàn hệ thống (Hình 1.1 trong báo cáo).", 
         "Không vẽ sơ đồ nguyên lý mạch quá chi tiết ở slide này."),
        ("Slide 3: Thiết kế phần cứng & Phân bổ GPIO", 
         "• Bảng phân loại ngoại vi ESP32 vs Thiết bị ngoài ICM-20948.\n• Bảng chân GPIO (SDA 21, SCL 22, BTN 25/26/27, LED 32 trở 1.0 kΩ, ADC 34).\n• Giải thích lý do chọn GPIO34 (Input-only, ADC1_CH6, hardware-designed).", 
         "Hình chụp bo mạch ESP32 DevKit 38-pin và module WCMCU-20948.", 
         "Không đưa các chân strapping pins vào danh sách sử dụng."),
        ("Slide 4: Giao tiếp I2C & Cơ chế Open-Drain", 
         "• ESP32 Master, ICM-20948 Slave (Địa chỉ 0x68 AD0=0).\n• Cực máng để hở Open-Drain và điện trở kéo pull-up 10kΩ tích hợp sẵn trên module WCMCU-20948 lên 3.3V (nối trực tiếp 3.3V, loại bỏ BSS138).\n• Chuỗi giao dịch đọc thanh ghi với Repeated START.", 
         "Sơ đồ chuỗi xung giao dịch I2C (Hình 4.1 trong báo cáo).", 
         "Không đi quá sâu vào thông số thời gian rise-time/fall-time."),
        ("Slide 5: Cảm biến ICM-20948 & Kiến trúc User Bank", 
         "• IMU 9-DOF phần cứng, firmware V1 triển khai dung hợp 6 trục (Gyro + Accel).\n• Lý do phân chia 4 User Bank (không gian địa chỉ 512 byte [4 x 128], ~80-100 thanh ghi hoạt động).\n• Cơ chế chuyển Bank qua hàm void imu_selectBank(uint8_t bank) ghi vào REG_BANK_SEL (0x7F).", 
         "Sơ đồ 4 User Bank và thanh ghi REG_BANK_SEL (Hình 5.1).", 
         "Không nói rằng I2C chỉ có 7-bit register address."),
        ("Slide 6: Phân tích 3 thanh ghi cốt lõi (Trọng tâm nhất)", 
         "• PWR_MGMT_1 (Bank 0, 0x06) = 0x01 (Thoát Sleep, tự động chọn xung PLL tốt nhất).\n• GYRO_CONFIG_1 (Bank 2, 0x01) = 0x1B (DLPF 51.2Hz, Dải đo ±500 °/s, 65.5 LSB/(°/s)).\n• ACCEL_CONFIG (Bank 2, 0x14) = 0x1B (DLPF 50.4Hz, Dải đo ±4g, 8192 LSB/g, ODR ≈ 102.27 Hz theo Table 18 — Accelerator Configuration).\n• Bảng bitfield chi tiết đối chiếu TDK DS-000189.", 
         "Sơ đồ trực quan 8-bit của 3 thanh ghi (Hình 6.1, 6.2 và callout).", 
         "Không ghi sai vị trí bit TEMP_DIS (Bit 3) và Reserved (Bit 4)."),
        ("Slide 7: Pipeline xử lý dữ liệu từ Raw đến Con trỏ", 
         "• 12-byte Burst Read (0x2D–0x38 tại Bank 0) giảm độ lệch thời điểm (~0.38 ms).\n• Đổi đơn vị LSB (/8192, /65.5) → Bù Bias tĩnh (200 polls, ~2.0s).\n• Bộ lọc bù Quaternion 6 trục (K=2.0 s⁻¹) → Adaptive Reference Frame → Dead-zone hai ngưỡng chuyển tiếp (0.8 °/s và 1.4 °/s) → Linear Gain scaling & Clamping.\n• Nhận diện cử chỉ Flick (1.15g / 0.35g, 60–450 ms) chuyển slide.", 
         "Sơ đồ Pipeline xử lý tín hiệu (Hình 8.1 trong báo cáo).", 
         "Không tuyên bố dùng lọc Kalman ma trận phức tạp."),
        ("Slide 8: Danh mục lệnh và API điều khiển ngoại vi", 
         "• Bảng đối chiếu lệnh: Input, Return Value, Hardware Effect.\n• void imu_selectBank(), bool imu_writeReg(), uint8_t imu_readReg(), bool imu_readBurst(), bool imu_readData().\n• Phân biệt giá trị trả về phần mềm và tác động vật lý phần cứng.", 
         "Bảng đối chiếu API rút gọn (Bảng 9.1 trong báo cáo).", 
         "Không copy-paste toàn bộ file mã nguồn C/C++ lên slide."),
        ("Slide 9: Tiến độ thực nghiệm & Minh bạch trạng thái", 
         "• Các mốc chức năng: WHO_AM_I (0xEA), PWR_MGMT_1 (0x01), Gyro/Accel thô, 6-axis pipeline, Flick detection.\n• Báo cáo trạng thái minh bạch: CODE_IMPLEMENTED, HOST_TESTED, COMPILE_VERIFIED, PLANNED, NEEDS_HARDWARE_TEST.", 
         "Bảng tiến độ Milestone hoặc video ngắn minh họa.", 
         "Không tuyên bố tính năng đã chạy thật trên phần cứng nếu chưa kiểm chứng tại phòng thí nghiệm."),
        ("Slide 10: Đánh giá kết quả & Kế hoạch giai đoạn 2", 
         "• Tóm tắt kết quả nghiên cứu giữa kỳ Tuần 5: Hoàn tất kiến trúc, schematic, firmware baseline 6 trục.\n• Kế hoạch giai đoạn 2: Gia công PCB 1 lớp, hàn linh kiện, mang mạch lên lab test phần cứng thật, tích hợp BLE HID thực tế.\n• Lời cảm ơn và mời thầy đặt câu hỏi vấn đáp.", 
         "Lộ trình Gantt chart hoặc danh sách các đầu việc giai đoạn 2.", 
         "Không kết luận hời hợt hoặc đưa ra các mốc thời gian phi thực tế.")
    ]

    for s_title, s_content, s_img, s_avoid in slides_map:
        add_p(f"• Mục tiêu & Nội dung cốt lõi:\n{s_content}\n• Hình ảnh/Bảng biểu đề xuất: {s_img}\n• ĐIỀU CẤM KỴ: {s_avoid}", 
              bold_prefix=s_title + "\n")

    # -------------------------------------------------------------
    # PHẦN O — GỢI Ý PHÂN CÔNG NHIỆM VỤ 3 THÀNH VIÊN
    # -------------------------------------------------------------
    add_h1("PHẦN O — GỢI Ý PHÂN CÔNG NHIỆM VỤ VÀ PHỐI HỢP 3 THÀNH VIÊN")
    
    add_p("Để việc chuẩn bị slide và ôn thi vấn đáp đạt hiệu quả cao nhất, nhóm đề xuất phương án phân công chuyên sâu theo thế mạnh từng người, nhưng vẫn đảm bảo khối kiến thức chung bắt buộc cả 3 cùng nắm vững:")

    dh.add_callout(doc, "PHÂN CÔNG CHUYÊN SÂU THEO THẾ MẠNH",
"""• THÀNH VIÊN 1 (Chuyên trách Phần cứng & ESP32):
  - Trách nhiệm thuyết trình: Slide 1, Slide 2, Slide 3, Slide 10.
  - Chuyên môn bảo vệ: Kiến trúc ESP32, quy tắc chân GPIO, strapping pins, ADC1_CH6 (GPIO34, 100k/100k, hardware-designed), mạch nguồn pin LiPo/TP4056/MT3608, chuyển dịch kiến trúc WCMCU-20948 nối trực tiếp 3.3V (loại bỏ LDO 1.8V và BSS138), LED chỉ thị GPIO32 với trở hạn dòng 1.0 kΩ.
• THÀNH VIÊN 2 (Chuyên trách Giao tiếp I2C & Cảm biến ICM-20948):
  - Trách nhiệm thuyết trình: Slide 4, Slide 5, Slide 6.
  - Chuyên môn bảo vệ: Giao thức I2C, Open-Drain, địa chỉ 0x68 (AD0=0), Repeated START, 4 User Bank, thanh ghi REG_BANK_SEL (0x7F), phân tích chi tiết từng bit của PWR_MGMT_1 (0x01), GYRO_CONFIG_1 (0x1B) và ACCEL_CONFIG (0x1B).
• THÀNH VIÊN 3 (Chuyên trách Xử lý tín hiệu 6 trục, BLE HID & Demo):
  - Trách nhiệm thuyết trình: Slide 7, Slide 8, Slide 9.
  - Chuyên môn bảo vệ: 12-byte Burst Read từ Bank 0, đổi đơn vị 65.5 LSB/(°/s) và 8192 LSB/g, bù trừ Bias, bộ lọc bù Quaternion 6 trục (K=2.0 s⁻¹), Dead-zone, Linear Gain scaling & Clamping, Flick gesture, bản tin BLE HID Report, danh mục API C chuẩn và kế hoạch kiểm chứng phần cứng.""",
                   kind='note')

    dh.add_callout(doc, "KHỐI KIẾN THỨC BẮT BUỘC CẢ 3 THÀNH VIÊN ĐỀU PHẢI NẮM VỮNG (5 CÂU HỎI TRỌNG TÂM CỦA THẦY)",
"""Dù được phân công phần nào, bất kỳ thành viên nào khi được giảng viên chỉ định đột xuất đều PHẢI trả lời trôi chảy 5 câu hỏi sau:
1. Đề tài đang làm gì? Kiến trúc ra sao?
   → "Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion." Bản chất là thiết bị trỏ tương đối điều khiển theo tốc độ xoay cổ tay (Rate-Control).
2. Phân bổ ngoại vi ESP32 thế nào? Chân nào tuyệt đối cấm dùng?
   → Phân định ngoại vi ESP32 vs ICM-20948. Tuyệt đối cấm GPIO6-11 (Flash) và GPIO0, 2, 12, 15 (Strapping). GPIO34 Input-Only thuộc ADC1 (tránh xung đột Wi-Fi). LED GPIO32 trở 1.0 kΩ. Nút bấm GPIO25, 26, 27.
3. Giao tiếp I2C hoạt động ra sao? Tại sao cần trở kéo? Địa chỉ cảm biến?
   → Cực máng để hở Open-Drain cần trở kéo pull-up (10kΩ tích hợp sẵn trên module WCMCU-20948 lên 3.3V) để tạo mức HIGH và Wired-AND. Module nối trực tiếp 3.3V không qua BSS138. Địa chỉ 0x68 (AD0=0). Ghi phát 0xD0, Đọc phát 0xD1. Dùng Repeated START giữ bus.
4. Cảm biến ICM-20948 có kiến trúc ra sao? Nêu chi tiết bitfield 3 thanh ghi cốt lõi?
   → 4 User Bank chọn qua REG_BANK_SEL (0x7F). PWR_MGMT_1 (0x06) = 0x01 (thoát Sleep, auto PLL). GYRO_CONFIG_1 (0x01) = 0x1B (DLPF 51.2Hz, ±500 °/s, 65.5 LSB/(°/s)). ACCEL_CONFIG (0x14) = 0x1B (DLPF 50.4Hz, ±4g, 8192 LSB/g, ODR ≈ 102.27 Hz theo Table 18 — Accelerator Configuration). Đọc 12 byte burst từ 0x2D đến 0x38.
5. Dòng dữ liệu từ cổ tay đến con trỏ máy tính đi qua các bước nào?
   → 10 bước pipeline: 12-byte burst read → LSB scale (/8192, /65.5) → Bias comp (200 polls) → 6-axis Complementary Quaternion (K=2.0 s⁻¹) → Adaptive frame → Deadzone hai ngưỡng chuyển tiếp (0.8 °/s và 1.4 °/s) → Linear Gain scaling & Clamping → Flick gesture (1.15g / 0.35g, 60–450 ms) → BLE HID Report (5 bytes).""",
                   kind='alert')

    # Save handbook document
    output_path = "deliverables/CAM_NANG_KIEN_THUC_AIR_MOUSE_MIDTERM.docx"
    doc.save(output_path)
    print(f"Handbook document generated successfully at: {output_path}")

if __name__ == '__main__':
    build_handbook()
