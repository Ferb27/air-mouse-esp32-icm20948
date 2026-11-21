# Đọc trước khi hàn Air Mouse

Gói này hướng dẫn lắp ESP32 + WCMCU-20948 trên perfboard 90×150 mm, dùng socket, TP4056 và MT3608. Pin 1S PCM chưa chọn; mọi ô đo còn trống, chưa có kiểm chứng phần cứng của gói.

**Thứ tự đọc:** [quy tắc AI](01_AI_CONTEXT.md) → [hướng dẫn V2](02_HUONG_DAN_HAN_PERFBOARD.md) → [hình tổng hợp để mở/in](hinh/00_TONG_HOP_HINH.html) → [kiểm bằng đồng hồ](09_KIEM_TRA_KHONG_FIRMWARE.md) → [nhật ký](07_NHAT_KY_DO_DAC.md). BOM, netlist, GPIO và kích thước tham khảo nằm cùng thư mục. BOM giữ bản gốc: dòng pin 17 và tổng giá là lịch sử; ưu tiên quyết định V2, không mua pin theo dòng cũ.

**Dùng với AI:** gửi cả thư mục hoặc zip. Nếu không nhận nhiều tệp, dán `01_AI_CONTEXT.md`, rồi `02_HUONG_DAN_HAN_PERFBOARD.md`, rồi `SO_DO_MO_TA_BANG_CHU.md`; gửi nhật ký và ảnh rõ khi cần. AI không xem được ảnh vẫn đọc mô tả từng hình. Không cần mạng để mở hình HTML; nguồn web chỉ để đối chiếu bổ sung.

**Năm điều tuyệt đối không làm:**

1. Không nối B- với OUT-/GND ngoài TP4056: mất bảo vệ pin.
2. Không USB ESP32 khi J5V còn cắm: có thể cấp nguồn ngược; chạy pin phải rút USB.
3. Không nối GPIO34 trực tiếp 5V/V_SYS: có thể hỏng ADC; chỉ điểm giữa R2/R3.
4. Không cắm tải ESP32 vào boost chưa chỉnh 5.0V (4.9–5.1V); không cấp điện trước đo nguội/soi cầu thiếc.
5. Không chập/đâm/ép pin, hàn lên túi/tab/PCM hay đặt chân hàn dưới pin. Đo cực ngay đầu pin trước ghép; nóng/phồng/mùi thì ngắt khi an toàn và tránh xa.

Chuẩn bị đồng hồ vạn năng, mỏ/đế, thiếc/flux, hút thiếc, kính, kìm, kẹp, thước, cách điện và thông gió theo mục 3.1. Phần mềm do chủ dự án làm sau; phép đo điện không chứng minh đã quét I2C hay có chuột hoạt động.

Có 11 nhóm hình, nhóm 4 tách nguồn/tín hiệu nên có **12 SVG**. Tệp `hinh/00_TONG_HOP_HINH.html` chứa SVG inline, font hệ thống, in A4 từng hình; đây không phải mẫu khoan 1:1. Thông tin PNG và kết quả kiểm nằm trong [báo cáo kiểm tra](tools/KET_QUA_KIEM_TRA.md). Sinh lại bằng `python tools/sinh_hinh.py`; kiểm/nén bằng `python tools/kiem_tra_goi.py`. Các script dùng thư viện chuẩn; xuất PNG là tùy chọn bằng trình duyệt đã có, không cài thêm.
