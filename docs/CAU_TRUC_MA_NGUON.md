# CẤU TRÚC MÃ NGUỒN FIRMWARE (sau khi tách file, 17/10/2026)

> Trước đây toàn bộ logic ứng dụng nằm trong `firmware.ino` (429 dòng) và `motion_pipeline.cpp` (534 dòng). Nay chia thành các mô-đun nhỏ, mỗi mô-đun một việc, nối với nhau qua file `.h`. **Hành vi không đổi** (chỉ chuyển code, giữ nguyên các dòng log); các bài test trên máy tính vẫn 24/24 PASS.

## 1. Nguyên tắc chia

Có **hai lớp**:

1. **Lõi thuần (portable core)**: chỉ dùng C/C++ chuẩn, **không gọi Arduino**. Chạy được và test được trên máy tính (`g++`). Chứa thuật toán: lọc, hiệu chuẩn, cử chỉ, chống dội.
2. **Lớp ứng dụng (`app_*`)**: gọi Arduino/ESP32 (`Serial`, `millis`, GPIO, BLE). Chỉ làm việc "dán" lõi vào phần cứng. Không chạy trên máy tính.

Quy ước: file bắt đầu bằng `app_` thì cần Arduino; file không có tiền tố `app_` là lõi thuần. Script test tự lấy "mọi file `src/*.cpp` trừ `app_*`".

## 2. Sơ đồ

```
                         firmware.ino  (điều phối: setup() + loop() ~60 dòng)
                              |
   +-----------+--------------+-----------------+----------------+-------------+
   |           |              |                 |                |             |
app_boot   app_serial_cmd  app_imu_guard     app_buttons       app_ble     app_status
(khởi động) (lệnh serial)  (sức khỏe cảm     (nút + gán nút   (gửi chuột   (log
   |           |            biến + tự đo      + chặn click)   BLE HID)    [STATUS])
   |           |            lại bias)
   |           |              |                 |                              |
   +-> app_imu (đọc cảm biến đúng hệ trục + hiệu chuẩn bias) <----------------+ (đếm Frz/Heal)
   +-> app_motion (cấu hình + log nút Mode/cử chỉ)        app_timing (nhịp 100 Hz, đồng bộ lại)
   |
   v   ------------------------ ranh giới: dưới đây là LÕI THUẦN, test trên máy tính ------------------------
motion_pipeline  ----> gesture_detector (cử chỉ gia tốc)
 (lọc, khóa đứng yên,  ----> yaw_flick (cử chỉ quay nhanh)     button_debounce (chống dội 5/20 ms)
  hệ quy chiếu, Mode,  ----> bias_checks (kiểm tra hiệu chuẩn)  click_guard (chặn con trỏ khi click)
  nhân gain, kẹp ±127)
icm20948_driver (đọc cảm biến qua I2C; bản giả lập khi chạy trên máy tính)
```

## 3. Từng file làm gì

### Lõi thuần (`firmware/src/` + `firmware/include/`)

| File | Việc | Test |
| --- | --- | --- |
| `icm20948_driver.cpp/.h`, `icm20948_registers.h` | Khởi tạo và đọc ICM-20948 qua I2C 400 kHz (thanh ghi, độ nhạy ±500 °/s, ±4 g) | N đầu |
| `motion_pipeline.cpp/.h` | Trừ bias, khóa đứng yên (0.4 °/s), tự chỉnh bias chậm, bộ lọc thái độ, hệ quy chiếu, nút Mode (khóa, cân lại sau 150 ms), nhân gain 0.3, cộng dồn phần dư, kẹp ±127 | N1–N7, N13 |
| `gesture_detector.cpp/.h` | Cử chỉ theo **gia tốc ngang** (cú giật tịnh tiến) | `test_flick_gesture` |
| `yaw_flick.cpp/.h` | Cử chỉ theo **tốc độ quay** (lắc nhanh trái = Back, phải = Forward), ngưỡng 150 °/s | N14 |
| `bias_checks.cpp/.h` | Hai hàm quyết định: hiệu chuẩn có hợp lệ không (`motion_calibration_still`) và có nên tự đo lại không (`motion_surface_rest_bias_bad`) | N8, N9 |
| `button_debounce.cpp/.h` | Chống dội phím bất đối xứng (nhấn 5 ms, nhả 20 ms) | N10, N12 |
| `click_guard.cpp/.h` | Bộ đệm 40 ms xóa cú giật lúc ấn, đóng băng con trỏ khi giữ nút < 250 ms | N11 |
| `scroll_mode.cpp/.h` | **Cuộn trang:** máy trạng thái "chạm Mode, nhấn lại nhanh và giữ" (chạm ≤ 250 ms, khoảng cách ≤ 350 ms) và **cuộn theo góc nghiêng kiểu cần điều khiển**: góc nghiêng so với tư thế lúc bắt đầu quyết định tốc độ cuộn (nấc/giây = `scroll_sens` × (góc − vùng chết)), giữ nghiêng thì cuộn liên tục; **tư thế gốc mặc định là tư thế thoải mái TRƯỚC khi nhấn đúp** (lịch sử 320 ms, lấy trung bình 250→150 ms trước lần nhấn đầu; `scroll_ref=0`), hoặc tư thế lúc nhấn (`scroll_ref=1`); 100 ms đầu không cuộn rồi tăng tốc dần trong 200 ms | N20–N23 |
| `button_map.cpp/.h` | **Gán nút:** đổi 3 nút vật lý (đã chống dội) thành nút logic theo cài đặt `btn_left/btn_right/btn_mode` (không làm gì, chuột trái/phải/giữa, Back, Forward, Mode); nhiều nút cùng chức năng thì hợp bằng OR; `bm_any_click` cho bộ chặn click | N24 |
| `imu_health.cpp/.h` | **Giám sát sức khỏe cảm biến:** bỏ ngay mẫu đọc lỗi hoặc mẫu toàn số 0 (cảm biến vừa mất trạng thái), 3 lần liên tiếp thì yêu cầu phục hồi bus I2C + khởi tạo lại; giữ luật chậm cũ (100 mẫu giống hệt, |a| < 0.5 g trong 0.5 s); thời gian khởi động 80 ms, giãn cách 300 ms (3 s nếu khởi tạo lại thất bại) | N25 |
| `air_config.cpp/.h` | **Cài đặt người dùng chỉnh được** (gain X/Y, ngưỡng lắc, bật/tắt lắc, chống click, thời gian cân lại): giá trị mặc định, khoảng cho phép, kiểm hợp lệ, và **bộ phân tích dòng lệnh `@GET/@SET/@SAVE/@DEFAULTS/@CAL`** (giao thức cho app PC) | N15–N19 |

### Lớp ứng dụng (cần Arduino)

| File | Việc |
| --- | --- |
| `app_config.h` | **Mọi hằng số chỉnh được ở một chỗ**: chu kỳ vòng lặp, thời gian chống dội, ngưỡng cử chỉ, số lần hiệu chuẩn, bước chỉnh gain |
| `app_scroll.cpp/.h` | Dán `scroll_mode` vào firmware: bật/tắt chế độ cuộn, lấy góc nghiêng từ `motion_getBodyGravity` để ra `wheel`/`hwheel`, đặt lịch cân lại khi thoát cuộn |
| `app_config_store.cpp/.h` | **Lưu/nạp cài đặt vào flash** (NVS, `Preferences`, namespace `airmouse`, một blob khóa `cfg`), áp cài đặt vào firmware đang chạy, trả lời các lệnh `@...`. Chỉ ghi flash khi `@SAVE` và khi có thay đổi |
| `app_boot.cpp/.h` | Chạy một lần lúc bật nguồn: serial, GPIO, khởi tạo cảm biến và in thanh ghi, hiệu chuẩn, bật BLE |
| `app_imu.cpp/.h` | Đọc cảm biến và **xoay trục** về hệ trục của pipeline; hiệu chuẩn bias có kiểm tra |
| `app_imu_guard.cpp/.h` | **Bước kiểm sức khỏe cảm biến** (`app_imu_health_step`: giải phóng bus I2C, khởi tạo lại, ghi log `[IMU] sensor lost ...`) và **tự đo lại bias** khi nằm yên trên bàn; đếm `Frz`/`Heal` |
| `app_buttons.cpp/.h` | Đọc 3 nút (GPIO25/26/27), chống dội, và bộ chặn click |
| `app_motion.cpp/.h` | Cấu hình pipeline (cử chỉ bật, ngưỡng 150 °/s, 150 ms) và log `[MODE]`/`[FLICK]` |
| `app_ble.cpp/.h` | Gửi BLE: chuột trái/phải (giữ để kéo-thả), Back/Forward, di chuyển, đèn LED; xử lý khi mất kết nối |
| `app_serial_cmd.cpp/.h` | Lệnh serial: một ký tự (`+ - ?` gain, `c` đo lại bias, `y Y` ngưỡng cử chỉ, `< >` bộ đệm click; **không lưu**) và dòng bắt đầu bằng `@` (giao thức cài đặt, chuyển cho `app_config_store`) |
| `app_status.cpp/.h` | Dòng `[STATUS]` mỗi giây (Rate, Stat, BiasZ, Up, Frz, Heal, Rst) |
| `app_timing.cpp/.h` | Nhịp 100 Hz và `app_resync()` sau các thao tác chặn |

### `firmware.ino`: chỉ còn điều phối

```
loop():  đọc serial -> đến nhịp 10 ms? -> đọc cảm biến -> kiểm sức khỏe cảm biến (mẫu hỏng thì bỏ, 3 lần thì
         phục hồi bus I2C + khởi tạo lại) -> tự đo lại bias -> đọc nút + gán nút -> chế độ cuộn? ->
         motion_process (chỉ khi cảm biến dùng được; nếu không: không có chuyển động nhưng nút và STATUS vẫn chạy) ->
         (cuộn: đổi sang con lăn) -> chặn click -> gửi BLE -> in STATUS
```

## 4. "Muốn sửa X thì mở file nào?"

| Muốn đổi | Mở |
| --- | --- |
| Giá trị **mặc định và khoảng cho phép** của gain, ngưỡng lắc, chống click, thời gian cân lại | `air_config.h` (một chỗ duy nhất; `app_config.h` chỉ trỏ về đây) |
| Thêm một cài đặt người dùng chỉnh được | `air_config.h/.cpp` (thêm trường + khóa), `app_config_store.cpp` (`app_config_apply`), thêm test; **tăng `AIR_CONFIG_VERSION`** nếu đổi cấu trúc |
| Độ nhạy mặc định (gain 0.3) | `air_config.h` (`AIR_CFG_GAIN_DEFAULT`); test N15 kiểm nó khớp với `motion_init` |
| Thời gian chống dội, số lần hiệu chuẩn | `app_config.h` |
| Hướng trục, cách xoay trục cảm biến | `app_imu.cpp` (`app_imu_read`) |
| Điều kiện hiệu chuẩn hợp lệ, điều kiện tự đo lại | `bias_checks.cpp` |
| Hành vi nút Mode (khóa, cân lại) | `motion_pipeline.cpp` (mục 6, Clutch) + `app_motion.cpp` |
| Gửi gì qua BLE khi bấm nút | `app_ble.cpp` |
| Thêm lệnh serial | `app_serial_cmd.cpp` |
| Thêm một dòng vào `[STATUS]` | `app_status.cpp` |
| Chân GPIO | `pin_definitions.h` |

## 5. Build và test

- **Build firmware:** `python -m platformio run -d firmware` (PlatformIO tự gom `firmware.ino` và mọi `src/*.cpp`; `platformio.ini` không cần đổi).
- **Test trên máy tính (35 test):** `bash firmware/test/run_host_tests.sh` hoặc PowerShell `.\firmware\test\run_host_tests.ps1`. Script tự biên dịch mọi `src/*.cpp` **trừ `app_*`** nên thêm file lõi mới không phải sửa lệnh.
- **Nạp:** `python -m platformio run -d firmware -t upload --upload-port COM3` (hoặc xem `release/`).

## 6. Giới hạn

- Việc chia file chỉ được kiểm bằng **build thành công** và **24 test lõi**. Lớp `app_*` **không** có test tự động; hành vi trên board phải kiểm bằng cách nạp và xem log (so với log trước khi chia). Tại thời điểm viết, bản đã chia **chưa được nạp** (`NOT_TESTED` trên phần cứng).
- Mô-đun `motion_pipeline.cpp` còn khá lớn (490 dòng) vì các hàm chia sẻ nhiều biến tĩnh (thái độ, bias, tham chiếu). Chia tiếp cần gom trạng thái vào một cấu trúc; chưa làm.
