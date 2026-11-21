# CẢM BIẾN ĐƠ / LỖI I2C: BẰNG CHỨNG, SỬA GÌ, ĐO THẾ NÀO (2026-10-23)

> Trạng thái trung thực: **phần lõi `HOST_TESTED`** (35 test, N25), đã nạp (`release/2026-10-23_i2c/`) và **đo trên board một lần 120 s** (`BENCH_VERIFIED`, một phiên, xem mục 5). Nguyên nhân gốc của việc cảm biến mất trạng thái vẫn **nghi là phần cứng** (dây lỏng trên breadboard, nguồn 3.3 V); sửa này chỉ rút ngắn hậu quả, **không** chứng minh được đã hết lỗi.

## 1. Bằng chứng từ log (đọc lại ngày 2026-10-23)

- Trong toàn bộ `raw_logs/` có **68 dòng `i2cWriteReadNonStop returned Error -1`** và **9 dòng `Error 263`** (mã 263 = hết thời gian chờ của ESP-IDF; −1 = lỗi chung/NACK).
- Lần thử gán nút (`raw_logs/gan_nut_handtest_2026-10-22.log`, 120 giây, chỉ bấm nút): **cảm biến đơ hai lần** (20:58:27 và 20:58:32). Lỗi đọc `Error -1` xuất hiện **đúng lúc** một lần nhấn nút trái (`[BTN] LEFT down` lúc 20:58:32.254 trùng với hai dòng lỗi cùng mili giây). Nhấn nút làm rung breadboard là cách giải thích phù hợp nhất, nhưng đây là suy luận từ trùng thời điểm, chưa phải bằng chứng trực tiếp.
- Cảm biến "đơ" thực ra là **tự mất trạng thái**: sau khi khởi tạo lại (`imu_init`) nó chạy được ngay (PASS sau khoảng 1 ms), tức đường I2C không kẹt; cảm biến trả toàn số 0 (đúng kiểu ICM-20948 vừa reset về chế độ ngủ). Giả thuyết: chân nguồn/dây chập chờn làm cảm biến sụt nguồn thoáng qua.
- **Lỗ hổng trong code cũ** (đọc từ mã nguồn):
  1. Chó canh chỉ chạy **sau khi đọc thành công**. Nếu đọc lỗi liên tục (bus lỗi), vòng lặp chỉ `return` mỗi nhịp, **không đếm, không phục hồi**.
  2. Chó canh cần **50 mẫu (0,5 s)** |a| < 0,5 g mới nhận ra cảm biến chết; suốt thời gian đó mẫu toàn 0 đi vào bộ xử lý ((0 − bias) ≈ hằng số 1,3 °/s) và **con trỏ trôi**.
  3. `imu_init()` gọi `Wire.begin()` lần hai **không khởi tạo lại bộ ngoại vi I2C** (log không có dòng `i2cInit` sau lần khởi tạo lại; chỉ có một dòng ở lúc boot). Cần `Wire.end()` trước.
  4. Thời gian chờ I2C mặc định **50 ms**, dài hơn nhiều so với nhịp 10 ms nếu bus lỗi.

## 2. Đã sửa gì

| Mục | Trước | Sau |
| --- | --- | --- |
| Mẫu đọc lỗi | bị bỏ qua, không đếm | đếm (`Err`), 3 lần liên tiếp → phục hồi bus + khởi tạo lại |
| Mẫu toàn số 0 (accel 0,0,0) hoặc NaN | đi vào bộ xử lý ≥ 0,5 s | **bỏ ngay**; 3 mẫu liên tiếp (30 ms) → khởi tạo lại |
| Phục hồi bus | không có | `imu_busRecover()`: `Wire.end()`, nếu SDA bị giữ thấp thì phát tới 9 xung SCL, rồi điều kiện STOP; đếm (`Rec`) |
| Khởi tạo lại | `Wire.begin()` lần hai (không đủ) | `Wire.end()` + `Wire.begin()` thật, `Wire.setTimeOut(10)` |
| Sau khi khởi tạo lại | không chờ | bỏ mẫu **80 ms** (cảm biến cần khởi động), không đếm |
| Giới hạn tần suất | 1 lần/3 s | 300 ms nếu lần trước thành công, **3 s nếu lần trước thất bại** (cảm biến thật sự vắng thì không quay vòng) |
| Luật chậm cũ | 100 mẫu giống hệt; \|a\| < 0,5 g 50 mẫu | **giữ nguyên** làm lưới an toàn |
| Log | `[IMU] Sensor frozen/dead ...` | `[IMU] sensor lost (<lý do>) -> I2C bus recover OK/FAILED, imu_init PASS/FAIL, N ms (fails, re-inits)` |
| `[STATUS]` | `... Frz | Heal | Rst` | thêm `Err` (lần đọc lỗi) và `Rec` (lần phục hồi bus) |

Bias cũ **được giữ nguyên** (không đo lại chặn); vẫn như thiết kế trước.

Test N25 (35 test cả bộ) kiểm: cảm biến khỏe không bao giờ bị loại; mẫu 0 bị bỏ ngay và khởi tạo lại ở mẫu thứ 3; 80 ms khởi động không đếm; giãn cách 300 ms và 3 s; ba lần đọc lỗi; luật cũ; rơi tự do ngắn (0,2 g trong 200 ms) không bị coi là lỗi; NaN; 100 000 mẫu có nhiễu ngắt quãng 1–2 mẫu liên tiếp không bao giờ kích hoạt; đồng hồ 32 bit quay vòng.

## 3. Cách đo trên board (để biết có tốt hơn không)

Cơ sở so sánh (bản cũ): trong lần thử 120 s trên, **2 lần đơ**, mỗi lần con trỏ chịu mẫu sai tới **0,5–3 s** (`[IMU] Sensor frozen/dead` rồi `imu_init = PASS` mới thấy sau khoảng 0,5 s).
Quy trình: nạp bản mới, cầm board như dùng thật, **120 giây**: nhấn nút trái/phải/Mode nhiều lần, thỉnh thoảng lắc nhẹ và gõ nhẹ lên breadboard. Ghi lại:
- số dòng `[IMU] sensor lost` (và lý do), thời gian `N ms` mỗi lần; cột `Frz`, `Err`, `Rec` của `[STATUS]` cuối cùng;
- cảm giác của bạn: con trỏ có còn trôi vài giây khi cảm biến mất không (kỳ vọng: gián đoạn dưới khoảng 0,1 s).
So sánh số lần mất giữa hai bản **chỉ có nghĩa nếu cách thử giống nhau**; số lần mất là chuyện ngẫu nhiên (phần cứng), thời gian mỗi lần mới là thứ sửa này cải thiện.

## 4. Việc phần cứng vẫn nên làm (không thể thay bằng phần mềm)
Hàn chắc 4 dây SDA, SCL, VCC, GND của module (hoặc dùng perfboard), thêm tụ 10–100 µF gần chân VCC của module, dây ngắn. Nếu sau đó số lần `Err`/`Frz` giảm rõ rệt thì xác nhận nguyên nhân là tiếp xúc/nguồn.

## 5. Kết quả đo trên board (2026-10-23, `raw_logs/i2c_handtest_2026-10-23.log`, 120 s, một người, một phiên)

- **2 lần cảm biến mất** (cả hai ngay sau khi ghép BLE, trong 8 giây đầu); cả hai được phục hồi: `[IMU] sensor lost (all zeros) -> I2C bus recover OK, imu_init PASS, 33 ms`. `[STATUS]` cuối: `Frz: 2 | Err: 2 | Rec: 2`; **không có lần mất nào trong ~115 s còn lại**.
- **Thời gian mỗi lần (giờ của board):** lỗi đọc đầu tiên ở 5588 ms, `i2cInit` (khởi tạo lại bộ I2C) ở 5620 ms, tức **~32 ms** để phát hiện (3 nhịp) rồi **33 ms** khởi tạo lại, cộng 80 ms chờ cảm biến khởi động: **dưới 0,15 s không có chuyển động** (lần hai: 7325 → 7356 ms, cùng kiểu). Bản cũ: 0,5–3 s, và suốt thời gian đó mẫu sai làm con trỏ trôi.
- Dòng `i2cInit()` xuất hiện sau mỗi lần khởi tạo lại: xác nhận `Wire.end()` + `Wire.begin()` thật sự khởi tạo lại bộ ngoại vi (bản cũ không có dòng này).
- **Chưa kết luận được về số lần mất**: chỉ 4 lần nhấn nút trong phiên này (8 sự kiện `[BTN]`), nên không so sánh được tần suất với bản cũ (2 lần trong 120 s lần thử gán nút). Con trỏ trôi hay không trong 0,15 s đó: người dùng chưa báo.
- **Sai số hiển thị đã gặp:** `Rate: 172 Hz` và `169 Hz` hai lần: do `app_resync()` đặt lại đồng hồ in `[STATUS]` nhưng không đặt lại bộ đếm vòng lặp, nên dòng kế tiếp đếm số vòng của hơn 1 giây (`Up` nhảy 2 giây). **Không phải vòng lặp chạy quá 100 Hz.** Đã sửa trong mã (`app_status_resync` đặt `s_loop_count = 0`), sẽ có trong bản nạp kế tiếp; bản đang trên board vẫn còn hiện tượng này.
