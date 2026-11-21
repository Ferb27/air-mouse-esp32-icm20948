# NHẬT KÝ DẠY ÔN VẤN ĐÁP AIR MOUSE — 2026-10-24 — phiên 1

- Giờ bắt đầu: 07:45
- Giáo trình: deliverables/CAM_NANG_ON_VAN_DAP_AIR_MOUSE.md
- Người dạy: Anti | Người học: (sinh viên thực hiện đề tài)
- Phiên trước: không có
- Trình độ ban đầu (tóm tắt từ 5 câu chẩn đoán): đang chẩn đoán

### Câu Đ1 — Chẩn đoán — Mô tả đề tài — lần trả lời 1 — Chế độ: CHẨN ĐOÁN
- Giờ: 07:46
- **Anti hỏi (nguyên văn):**
  > Bạn tự mô tả Air Mouse làm gì trong 30 giây.
- **Người học trả lời (nguyên văn):**
  > bỏ hết mấy câu về mô tả các thứ đi, vào thẳng trọng tâm giúp tôi
- **Đánh giá:** KHÔNG ĐÁNH GIÁ (người học yêu cầu bỏ qua chẩn đoán để vào thẳng trọng tâm)
- **Lý do chấm:** Người học chủ động muốn bỏ qua các câu hỏi mô tả và chẩn đoán chung, tập trung trực tiếp vào bài học và mã nguồn.
- **Anti phản hồi cho người học (tóm tắt 1–3 câu):** Đồng ý vào thẳng nội dung trọng tâm. Bắt đầu ngay Bài 1: Đọc hiểu mã nguồn C/C++ trong dự án Air Mouse.
- **Điểm yếu cần ôn:** Cần theo dõi khả năng đọc code thực tế ở Bài 1.

## Bài 1 — Đọc code C/C++ (Phần 1) — 07:47
- Đã giảng:
  - Khung chương trình setup() (chạy 1 lần) và loop() (lặp nhịp 10 ms).
  - Khái niệm biến static: bộ nhớ lưu trạng thái giữa các vòng lặp (bias, bộ đếm đứng yên, quaternion tư thế).
  - Cấu trúc struct imu_data_t: gói 6 số đo vật lý (3 trục gia tốc ax, ay, az và 3 trục vận tốc góc gx, gy, gz).
  - Phân tích hàm apply_tightening(): nhận diện dòng điều kiện if và dòng tính toán thu nhỏ tỉ lệ.
  - Kiểu dữ liệu int8_t (-128..127) và lý do dùng cho gói chuột HID (kẹp giới hạn ±127).
- File code đã mở: firmware/src/motion_pipeline.cpp (dòng 9–36, 50–54), firmware/include/icm20948_driver.h (dòng 26–33).
- Hình dung đời thường đã dùng: Biến static như cuốn sổ tay ghi nhớ việc ca trước; Struct như hộp đựng 6 ngăn; Hàm như máy ép nhận quả trả nước ép.

### Người học yêu cầu — Bài 1 — 07:48
- **Người học nói (nguyên văn):**
  > dạy tôi từng dòng code đi, tôi chưa đọc dòng nào của code cả luôn đó, dạy từ đầu của phần code
- **Anti phản hồi (tóm tắt):** Đồng ý dạy từng dòng từ điểm bắt đầu của toàn bộ chương trình (file firmware/firmware.ino), giải thích cặn kẽ từng từ khóa và ý nghĩa thực tế của từng dòng trước khi sang dòng tiếp theo.
- **Nguồn:** firmware/firmware.ino dòng 19–28; giáo trình Phần 1 và Phần 2.

### Người học phản hồi — 08:01
- **Người học nói (nguyên văn):**
  > tôi nghĩ là thầy không hỏi code kiểu này đâu
- **Anti phản hồi (tóm tắt):** Đồng ý hoàn toàn với nhận định của người học. Thầy vấn đáp hệ thống nhúng không kiểm tra cú pháp ngữ pháp C thông thường (như lệnh return hay biến), mà hỏi bản chất kiến trúc hệ thống và thuật toán nhúng: (1) Tại sao dùng nhịp 10 ms non-blocking thay vì delay()? (2) Tại sao rê chuột bằng Gyro mà không bằng Accel? (3) Chống trôi bằng tightening khác deadzone thế nào? (4) Con số lấy từ đâu và cái gì chưa đo? Điều chỉnh ngay cách tiếp cận: gắn code trực tiếp vào bài toán kỹ thuật mà thầy sẽ hỏi vặn.
- **Nguồn:** giáo trình Phần 0.1 và Phần 2.

### Người học điều chỉnh phương pháp — 08:03
- **Người học nói (nguyên văn):**
  > ý là vẫn học code từ đầu nhưng mà những cái code setup các thứ như trên thì chỉ cần đưa ra cho tôi đọc qua để biết thôi, không cần hỏi câu hỏi hay gì cả đâu
- **Anti phản hồi (tóm tắt):** Thống nhất hoàn toàn. Quy ước: các đoạn code hạ tầng/khởi tạo/luồng tổng quát sẽ được giải thích nhanh, mạch lạc từ đầu file để người học nắm bức tranh toàn cảnh, không đặt câu hỏi kiểm tra. Chỉ dừng lại hỏi kiểm tra khi chạm vào các khối thuật toán cốt lõi (xử lý cảm biến, chống trôi, I2C, lọc dội nút, cử chỉ) là những nơi thầy sẽ chất vấn sâu.
- **Nguồn:** firmware/firmware.ino dòng 19–79; giáo trình Phần 2.

## Bài 2 — Bức tranh tổng thể: Luồng chạy của firmware.ino (Phần 2) — 08:04
- Đã giảng:
  - Khởi tạo app_boot(): mở Serial, nạp cấu hình, cấu hình I2C/ICM-20948, BLE HID.
  - Vòng lặp loop() 10 ms (100 Hz): cơ chế non-blocking với micros() thay vì delay(10).
  - 5 công đoạn chính trong một vòng lặp:
    1. Đọc và giám sát cảm biến (app_imu_read, app_imu_health_step, app_imu_self_heal).
    2. Đọc và chống dội nút bấm (app_buttons_read, bm_apply).
    3. Đường ống chuyển động (motion_process, cuộn chuột app_scroll).
    4. Bộ chặn giật click_guard (app_buttons_filter_motion).
    5. Phát gói BLE HID và in log định kỳ.
- File code đã mở: firmware/firmware.ino (dòng 19–79).
- Hình dung đời thường đã dùng: Dây chuyền sản xuất 5 công đoạn hoạt động tuần hoàn mỗi 10 ms.

## Bài 3 — Cảm biến ICM-20948 và giao tiếp I²C (Phần 3) — 08:42
- Đã giảng:
  - Bản chất hai cảm biến: Gyroscope đo vận tốc góc (°/s) tỉ lệ thuận trực tiếp với vận tốc con trỏ; Accel đo gia tốc (g) gồm cả 1g trọng lực, nếu tích phân 2 lần tìm vị trí sẽ bùng nổ sai số trôi theo t^2.
  - Giao thức I2C: tốc độ 400 kHz Fast-Mode, địa chỉ 0x68 (chân AD0 nối GND), đọc burst 12 byte (6 byte Accel + 6 byte Gyro) trong ~438 µs.
  - Cấu hình thanh ghi: WHO_AM_I kiểm tra chip (0xEA), dải đo Gyro ±500 °/s (hệ số chia 65.5 LSB/dps), Accel ±4g (hệ số chia 8192 LSB/g), tốc độ lấy mẫu 102.27 Hz (lệch 2.27% so với loop 100 Hz).
  - Phép xoay trục trong app_imu.cpp (x_mới = y_cũ, y_mới = -x_cũ) dựa trên đo đạc 11 cử động chuẩn để khớp hướng cầm điều khiển TV.
- File code đã mở: firmware/src/icm20948_driver.cpp (dòng 143–198, 223–251), firmware/src/app_imu.cpp (dòng 8–14).
- Hình dung đời thường đã dùng: Accel như cảm giác nặng trong thang máy (cho biết hướng rơi xuống); Gyro như công-tơ-mét đo tốc độ quay (cho biết đang xoay nhanh hay chậm).
