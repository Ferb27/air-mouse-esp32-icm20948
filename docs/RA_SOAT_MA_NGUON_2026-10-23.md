# RÀ SOÁT TOÀN BỘ MÃ NGUỒN ĐỂ CHỐT (2026-10-23)

> Mục đích: đọc lại mã trước khi chuyển sang viết báo cáo, tìm lỗi cần sửa. **Trạng thái trung thực:** các sửa dưới đây đã `HOST_TESTED` (phần lõi, 35 test) hoặc chỉ **build SUCCESS** (lớp `app_*` không có test tự động). **Chưa nạp lên board, chưa thử tay** (`NOT_TESTED`) cho bản chốt `release/2026-10-23_chot/`.

## 1. Phạm vi và cách làm

**Đã đọc từng dòng (trong đợt rà soát này):** `firmware.ino`; lõi thuần `motion_pipeline`, `gesture_detector`, `yaw_flick`, `bias_checks`, `air_config`; `app_timing`, `app_serial_cmd`, `app_boot`, `icm20948_registers.h`, `pin_definitions.h`; thư viện `ESP32 BLE Mouse` (hàm `press/release/move/click`). Các file `scroll_mode`, `imu_health`, `button_map`, `click_guard`, `button_debounce`, `app_ble`, `app_buttons`, `app_imu`, `app_imu_guard`, `app_config_store`, `app_scroll`, `app_status`, `app_motion`, `icm20948_driver` đã đọc/viết/sửa trong các phiên trước cùng ngày và được đọc lại khi cần.

**Công cụ tự động:**
- Biên dịch phần lõi thuần với `-Wall -Wextra -Wshadow -Wconversion -Wdouble-promotion`: **không cảnh báo**.
- `cppcheck` (warning, style, performance, portability, inconclusive) trên mọi `src/*.cpp` và `firmware.ino`: **không có cảnh báo nghiêm trọng**; chỉ ghi chú phong cách (tên tham số khác khai báo, mảng nên `const`, `memset` struct có số thực: hợp lệ trên ESP32 vì 0.0f là toàn bit 0). Đã dọn các ghi chú phong cách đầu tiên.
- 35 test trên máy tính PASS; build `esp32dev` SUCCESS (Flash 90.0 %, RAM 12.4 %).

**Chưa đọc kỹ (nói rõ để khỏi hiểu lầm):** thân file test `test_motion_pipeline.cpp` (khoảng 1 900 dòng, đã chạy PASS nhưng không đọc lại từng test), các script trong `scripts/` và công cụ đo cũ `firmware_bench/`, `firmware_bias_drift/`, `firmware_orient/`; trang web `tools/config_page/air_mouse_config.html` chỉ đọc lại phần kết nối Web Serial (phần còn lại đã kiểm bằng board giả lập và bằng việc người dùng thử trên board thật).

## 2. Lỗi tìm thấy và đã sửa

| # | Mức | Vấn đề (bằng chứng) | Sửa |
| --- | --- | --- | --- |
| 1 | Trung bình | **Khi cảm biến hỏng/mất, vòng lặp `return` trước khi đọc nút và in `[STATUS]`**: nút bấm chết theo cảm biến, và đúng lúc cần chẩn đoán lại **không có dòng `[STATUS]` nào** (đọc từ `firmware.ino`) | Cảm biến không dùng được thì **không có chuyển động nhưng nút, BLE, nhật ký nút và `[STATUS]` vẫn chạy**; chuyển động và cuộn chỉ chạy khi cảm biến tốt |
| 2 | Trung bình–thấp | **Nút kẹt sau khi BLE ngắt rồi nối lại**: thư viện BLE giữ bit nút trong biến riêng và đặt vào **mọi** báo cáo; khi mất kết nối lúc đang giữ nút thì mã chỉ xóa cờ của mình, không nhả bit của thư viện (đọc `BleMouse.cpp`: `buttons()` đổi `_buttons` cả khi chưa kết nối, `move()` chỉ chặn việc gửi). Chưa tái hiện trên board | Khi chuyển sang trạng thái mất kết nối, **nhả toàn bộ 5 bit nút** của thư viện (không gửi gì vì chưa kết nối) |
| 3 | Thấp | **Cử chỉ lắc Back/Forward dùng `click()`**, mà `click()` ghi đè toàn bộ trạng thái nút rồi về 0: nếu đang giữ một nút (kéo thả) thì cử chỉ làm **nhả nút đó** (đọc `BleMouse::click`) | Dùng `press` rồi `release` đúng nút Back/Forward, không đụng các nút khác |
| 4 | Trung bình | **Một lần `imu_init()` thất bại lúc bật nguồn → treo vô hạn nhấp nháy LED `[FATAL]`** cho tới khi bật lại nguồn (đọc `app_boot.cpp`); cảm biến trên breadboard đã được thấy mất trạng thái chớp nhoáng | Thử lại tối đa 5 lần, mỗi lần giải phóng bus I2C và chờ 100 ms; chỉ báo FATAL nếu cả 5 lần thất bại |
| 5 | Nhỏ | Board mới (chưa lưu cài đặt) in dòng lỗi `[E] nvs_get_blob len fail: cfg NOT_FOUND` (có trong log) | Kiểm `isKey()` trước, không còn dòng lỗi giả |
| 6 | Nhỏ | Tên tham số khác khai báo, mảng không `const`, một chú thích cũ ("firmware tắt cử chỉ lúc này") sai, mô tả vòng lặp trong tài liệu cũ | Dọn lại; cập nhật `docs/CAU_TRUC_MA_NGUON.md` |

Ghi chú: sửa 1–5 nằm ở lớp `app_*`/`firmware.ino` nên **không có test tự động**; chỉ kiểm bằng build SUCCESS và đọc lại. Cần nạp và thử tay (mục 4).

## 3. Quan sát không sửa (hạn chế đã biết, chấp nhận hoặc để lại)

- **Phím lệnh cũ `+`/`-` (chỉ dùng khi gỡ lỗi qua serial)** nhân/chia cả hai gain cùng lúc và, chạm giới hạn thì ép cả hai bằng nhau (mất tỉ lệ nếu đã đặt gain X/Y khác nhau bằng `@SET`). Trang cấu hình không dùng phím này.
- **Phản hồi `@ERR unknown-key <khóa>`** in lại tối đa 24 ký tự của khóa người gửi (không ảnh hưởng gì ngoài cổng serial).
- **Nhịp vòng lặp:** lịch đặt `s_last_loop_us = now_us` thay vì cộng thêm chu kỳ, nên chu kỳ thực là 10 ms cộng độ trễ xử lý; đo được vẫn 100 vòng/giây. Cảm biến lấy mẫu 102,27 Hz nên thỉnh thoảng (khoảng mỗi 0,44 s) bỏ một mẫu; ảnh hưởng không đáng kể.
- **Cảm biến mất trạng thái khi rung/nhấn nút**: giảm hậu quả xuống dưới khoảng 0,15 s (`docs/I2C_ROBUSTNESS_2026-10-23.md`) nhưng **nguyên nhân gốc là phần cứng** (breadboard), chưa xử lý bằng phần mềm.
- **Run tay không được lọc** (chỉ là thử nghiệm ưu tiên thấp, `docs/NGHIEN_CUU_CHONG_RUN_TAY_2026-10-22.md`).
- **Không có kiểm thử tự động cho lớp `app_*`** (cần Arduino/phần cứng); hành vi trên board chỉ kiểm bằng nhật ký và người dùng thử.
- **Flash 90,0 %** (còn khoảng 131 KB): thêm tính năng lớn sẽ khó; chưa dùng OTA hay bảng phân vùng khác.
- `CORE_DEBUG_LEVEL=3` còn in log thông tin của thư viện (BLE, I2C): hữu ích để chẩn đoán, tốn một ít flash và băng thông serial.
- Các hằng số **đoán, chưa tối ưu bằng đo**: ngưỡng chạm 250 ms / nhấn lại 350 ms của chế độ cuộn, vùng chết 2,5°, độ nhạy cuộn 2,0, độ trễ bộ chặn click 40 ms (bản chốt giữ đúng các giá trị người dùng đã thử và thấy ổn).

## 4. Việc cần làm để coi là chốt
1. **Nạp** `release/2026-10-23_chot/` (`firmware.bin` bắt đầu `46B47DBC53252988`) lên board (nạp trực tiếp trên laptop như các lần trước).
2. **Thử tay tối thiểu** (khoảng 5 phút): nút trái/phải/Mode, cuộn (chạm Mode, nhấn lại, giữ, nghiêng), trang cấu hình đọc/đổi/lưu, và bắt log để thấy `[STATUS]` có `Err`/`Rec`, hiển thị `Rate` không còn nhảy 140–170.
3. Nếu thử tay ổn: ghi `BENCH_VERIFIED`/`USER_FEEDBACK` cho các sửa 1–5 ở đây (sửa 2 và 4 khó tái hiện: chỉ ghi "đã đọc và build", không ghi "đã kiểm").
4. Sao lưu mã nguồn chốt: `backups/2026-10-23_ma_nguon_chot/` (kèm `SOURCE_SHA256.txt`).

## 5. Kết quả nạp và thử tay bản chốt (2026-10-23, một phiên 150 s, một người)

- **Đã nạp** bản `release/2026-10-23_chot/` trực tiếp trên laptop (báo cáo của Anti: hash verified; **log và báo cáo của Anti chưa đồng bộ về PC nên mình không tự đọc được**). Mình kiểm độc lập: 1 KB đầu vùng ứng dụng (`0x10000`) đọc từ flash của board **trùng với release chốt và khác bản `i2c`** (chứa mô tả ứng dụng ESP-IDF với mã băm riêng từng bản build); chưa đối chiếu toàn bộ 1,1 MB.
- **Boot bình thường** (`raw_logs/chot_boot_2026-10-23.log`): hiệu chuẩn được chấp nhận lần 1, `@GET` `ver=5`, `[STATUS]` có `Err`/`Rec`.
- **Thử tay 150 s** (`raw_logs/chot_handtest_2026-10-23_b.log`, `BENCH_VERIFIED` cho các điểm dưới; log đầu `chot_handtest_2026-10-23.log` bị ngắt, không có sự kiện nào): 22 lần nhấn trái (có giữ 3–4,5 s), 1 lần nhấn phải, 6 lần nhấn Mode; **vào chế độ cuộn 2 lần** (17 s và 13 s) bằng chạm-nhấn-giữ, trong lúc cuộn `dX`/`dY` luôn bằng 0 (con trỏ đứng yên) và thoát có cân lại sau 0,2 s; không có `[BTN] ... (BLE not connected)` (Bluetooth giữ kết nối suốt phiên); **không có lần cảm biến mất**, `Err: 0 | Rec: 0`; vòng lặp **100 Hz ổn định** (152 dòng `Rate: 100`, 1 dòng 92 ở giây đầu) và không còn nhảy 140–170 sau phục hồi (chưa có lần phục hồi nào để thử lại lỗi hiển thị đó).
- **Không được thử trong phiên này (nên các sửa 1–4 ở mục 2 vẫn `NOT_TESTED` trên phần cứng):** cảm biến mất trạng thái (không xảy ra), Bluetooth ngắt và nối lại lúc đang giữ nút, cử chỉ lắc Back/Forward (không có `[FLICK]`), khởi tạo cảm biến thất bại lúc bật nguồn. Người dùng chưa nói cảm giác dùng thế nào (`USER_FEEDBACK` chưa có cho bản này).
