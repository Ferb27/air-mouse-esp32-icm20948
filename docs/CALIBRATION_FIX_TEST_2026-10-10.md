# BÁO CÁO THỰC NGHIỆM: HIỆU CHUẨN CÓ KIỂM TRA (CALIBRATION VALIDATION) VÀ LỆNH ĐO LẠI 'c'

> **Thời gian thực hiện**: 2026-10-10 22:50 đến 2026-10-14 20:53  
> **Thực hiện bởi**: Anti (theo chỉ đạo tại `docs/HANDOFF_ANTI_NAP_HIEU_CHUAN_HOP_LE.md` của Claude)  
> **Trạng thái thực tế**: `BENCH_VERIFIED` trên phần cứng thật (ESP32 DevKit 38-pin + ICM-20948)

---

## 1. Điều kiện Thực nghiệm

- **Phần cứng**: ESP32 Classic DevKit 38-pin cắm cảm biến ICM-20948 (WCMCU-20948) qua breadboard (4 dây: 3.3V, GND, SDA=GPIO21, SCL=GPIO22).
- **Kết nối vật lý**:
  - Giai đoạn nạp và kiểm tra Ca A/B: Cáp micro-USB cắm trực tiếp cổng USB sau lưng PC (mainboard), nhận diện `COM3` (Silicon Labs CP210x USB to UART Bridge).
  - Giai đoạn kiểm tra Ca C: Cáp micro-USB cắm qua laptop của người dùng, kết nối từ xa qua cầu RFC2217 (`rfc2217://<LAPTOP_IP>:4000?ign_set_control`).
- **Tư thế đặt board**: Đặt ngửa phẳng trên mặt bàn, cổng micro-USB hướng về phía người cầm (cổ tay), đầu đối diện là mũi hướng về màn hình, mặt chip hướng lên trời.
- **Hành động của người dùng**:
  - **Ca A** (`calib_fix_2026-10-10_A_still_retry2.log`): Board nằm yên tĩnh hoàn toàn trên mặt bàn suốt 40 giây.
  - **Ca B lần 1** (`calib_fix_2026-10-10_B_held.log`): Board nằm yên lúc bật nguồn nên Attempt 1 được chấp nhận ở giây thứ 3; người dùng nhấc board lên lắc ở giây thứ 18–28.
  - **Ca B retry 1** (`calib_fix_2026-10-10_B_held_retry1.log`): Người dùng cầm board trên tay và lắc liên tục suốt 11 giây bao trùm toàn bộ 5 lượt hiệu chuẩn khởi động.
  - **Ca C** (`calib_fix_2026-10-10_C_cmd.log`): Board khởi động khi người dùng đang cầm lắc (5 lượt REJECTED), sau đó rơi vào vòng lặp chính với bias lệch. Người dùng đặt board nằm yên trên bàn, Anti gửi lệnh `c`. Board thực hiện đo lại, Attempt 1 chấp nhận (ACCEPTED) và khôi phục bias chuẩn.

---

## 2. Kết quả Nạp Firmware (Bước 3)

- **Lệnh thực thi**:
  ```powershell
  python -m platformio run -d firmware -t upload --upload-port COM3
  ```
- **Kết quả PlatformIO**: `[SUCCESS]`
- **Thời gian nạp**: 22.50 giây (tốc độ baud mặc định 460800 baud của PlatformIO upload).
- **Kích thước flash ghi**:
  - `bootloader.bin`: 17,520 bytes tại `0x1000`
  - `partitions.bin`: 3,072 bytes tại `0x8000`
  - `boot_app0.bin`: 8,192 bytes tại `0xe000`
  - `firmware.bin`: 1,167,680 bytes tại `0x10000`
- **Xác minh tính toàn vẹn**:
  - `Hash of data verified.`
  - `Leaving... Hard resetting via RTS pin...`

---

## 3. Ca A: Khởi động khi Board Nằm Yên (Kiểm tra "Đúng")

- **Tệp log**: `raw_logs/calib_fix_2026-10-10_A_still_retry2.log`
- **SHA-256**: `063d8867e973b81bd539a40dae9448e8ba2fbc71e565f50a27bb023080ab4ebe`
- **Nguyên văn nhật ký hiệu chuẩn**:
  ```text
  [23:08:52.339] [CALIBRATION] Commencing Gyro Bias Calibration (2 s per attempt)...
  [23:08:52.345] [CALIBRATION] Please leave the device completely STATIONARY on the table.
  [23:08:54.558] [CALIBRATION] Attempt 1: 2200 ms, 200 polls, sd = 0.17/0.08/0.10 dps, half-mean diff = 0.02/0.00/0.01 dps -> ACCEPTED
  [23:08:54.564] [CALIBRATION] Zero-Rate Bias: X =  -1.34 dps | Y =  +0.55 dps | Z =  +0.32 dps
  [23:08:54.570] [BLE] Starting BLE HID Mouse Advertising as 'AirMouse-ESP32'...
  [23:08:54.576] [SYSTEM] Air Mouse System Ready. Entering 100 Hz Main Loop.
  ```
- **Bảng số liệu thống kê (Bước 7)**:

| Chỉ số | Giá trị quan sát | Nhận xét |
|---|---|---|
| Tổng số dòng `[STATUS]` | 36 | Tần số báo cáo đúng 1.0 s / dòng (~100 Hz ODR) |
| Số dòng `Stat: 1` (Đứng yên) | 20 | Khóa trạng thái đứng yên thành công |
| Số dòng `Stat: 0` (Chuyển động) | 16 | Xuất hiện ở giai đoạn đầu khi bộ lọc hội tụ |
| Số dòng có `dX`/`dY` khác 0 | **0** (0%) | **100% không phát sinh bất kỳ tick trôi dạt nào** |
| `BiasZ` ban đầu / cuối | `+0.32 dps` / `+0.32 dps` | Cực kỳ ổn định, khớp hoàn toàn với kỳ vọng |
| Lỗi I2C (`Wire.cpp`) | 0 | Không có lỗi bus |

---

## 4. Ca B: Khởi động khi Board Bị Cầm và Lắc (Kiểm tra Cơ chế Tự từ chối)

### 4.1. Lần đo 1 (`raw_logs/calib_fix_2026-10-10_B_held.log`)
- **SHA-256**: `32fa298852d67a56f334c56a6f3c1a348d805c398534bd491b61bf94eea7efc7`
- **Diễn biến**: Attempt 1 đo lúc 23:12:00 khi board vẫn còn trên bàn (`sd = 0.13/0.10/0.09 dps -> ACCEPTED`). Người dùng nhấc board lên lắc ở giây thứ 18 (23:12:16 đến 23:12:26) tạo ra các giá trị `dX: +7, dY: +13`. Khi đặt lại xuống bàn (23:12:28 trở đi), board trở về `Stat: 1` và `dX: +0, dY: +0`.

### 4.2. Lần đo lại có kiểm soát (`raw_logs/calib_fix_2026-10-10_B_held_retry1.log`)
- **SHA-256**: `f2af2c409d4eb5f20bec835cba11cef87e6e061c11f71191d8fdb631894fe0e1`
- **Nguyên văn toàn bộ các dòng `Attempt`**:
  ```text
  [23:14:57.017] [CALIBRATION] Attempt 1: 2200 ms, 200 polls, sd = 122.06/26.25/35.53 dps, half-mean diff = 24.41/0.87/14.66 dps -> REJECTED (board not still), retrying
  [23:14:59.227] [CALIBRATION] Attempt 2: 2199 ms, 200 polls, sd = 99.46/31.07/33.12 dps, half-mean diff = 9.82/7.65/10.47 dps -> REJECTED (board not still), retrying
  [23:15:01.438] [CALIBRATION] Attempt 3: 2200 ms, 200 polls, sd = 112.41/36.12/13.85 dps, half-mean diff = 9.68/4.85/6.71 dps -> REJECTED (board not still), retrying
  [23:15:03.649] [CALIBRATION] Attempt 4: 2200 ms, 200 polls, sd = 126.87/30.06/17.36 dps, half-mean diff = 9.82/1.01/8.04 dps -> REJECTED (board not still), retrying
  [23:15:05.860] [CALIBRATION] Attempt 5: 2200 ms, 200 polls, sd = 115.18/29.53/18.83 dps, half-mean diff = 20.52/9.82/5.47 dps -> REJECTED (board not still), retrying
  [23:15:05.871] [CALIBRATION][WARN] Board never held still; using the last attempt. Send 'c' over serial once it is resting to recalibrate.
  [23:15:05.878] [CALIBRATION] Zero-Rate Bias: X =  -6.35 dps | Y =  +4.10 dps | Z =  -0.58 dps
  ```
- **Bảng số liệu thống kê (Bước 7)**:

| Chỉ số | Giá trị quan sát | Nhận xét |
|---|---|---|
| Tổng số dòng `[STATUS]` | 32 | Thu thập đầy đủ 32 giây sau khởi động |
| Số dòng `Stat: 1` (Đứng yên) | **0** (0%) | Board không bao giờ khóa được trạng thái đứng yên |
| Số dòng `Stat: 0` (Chuyển động) | **32** (100%) | Liên tục nhận diện là đang chuyển động |
| Số dòng có `dX`/`dY` khác 0 | **32** (100%) | Con trỏ liên tục bị trôi dạt do bias lệch |
| `BiasZ` đo được | `-0.58 dps` | Lệch lớn so với giá trị thực (`+0.32 dps`) |
| Lỗi I2C (`Wire.cpp`) | 0 | Không có lỗi bus |

> **Ý nghĩa thực nghiệm**: Ca B chứng minh chính xác giả thuyết của Claude: Khi board bị rung lúc khởi động, thuật toán mới đã **từ chối liên tiếp 5 lần** (`REJECTED`). Khi hết 5 lần bắt buộc phải lấy mẫu cuối, bias bị sai lệch dẫn đến hiện tượng trôi dạt liên tục (`Stat: 0`, `dX/dY != 0`), hoàn toàn trùng khớp với hiện tượng người dùng gặp phải ngày 08/10.

---

## 5. Ca C: Lệnh Đo lại Bias Trực tiếp Qua Serial (`c`)

- **Tệp log**: `raw_logs/calib_fix_2026-10-10_C_cmd.log`
- **SHA-256**: `84208174ef29eb0532e7a8b701f7171a890216a225a3cba4cf9ebc6f56fa3e9f`
- **Tệp lệnh**: `raw_logs/calib_fix_2026-10-10_C_cmd_input.txt` (nội dung gửi: `cSTOP`)
- **Diễn biến thực tế**:
  1. Khi mở kết nối, board khởi động trong lúc người dùng đang lắc: cả 5 lượt từ chối (`REJECTED`), board cảnh báo và nhận bias sai: `X = +2.28 dps, Y = -1.44 dps, Z = +0.46 dps`.
  2. Trong vòng lặp chính, do bias Z lệch, board liên tục báo `Stat: 0` và trôi nhẹ `dX: +0, dY: -1` dù người dùng đã đặt board nằm yên trên bàn.
  3. Lúc `20:52:31`, Anti gửi lệnh `c` qua tệp lệnh.
  4. Firmware nhận lệnh `c` và lập tức kích hoạt hàm `calibrate_startup_bias()`:
  ```text
  [20:52:31.428] [CALIBRATION] Commencing Gyro Bias Calibration (2 s per attempt)...
  [20:52:31.434] [CALIBRATION] Please leave the device completely STATIONARY on the table.
  [20:52:33.644] [CALIBRATION] Attempt 1: 2200 ms, 200 polls, sd = 0.13/0.09/0.09 dps, half-mean diff = 0.01/0.01/0.01 dps -> ACCEPTED
  [20:52:33.650] [CALIBRATION] Zero-Rate Bias: X =  -1.38 dps | Y =  +0.57 dps | Z =  +0.36 dps
  [20:52:34.651] [STATUS] Rate: 107 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.36
  [20:52:35.652] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.36
  [20:52:36.653] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.36
  [20:52:37.652] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.36
  ```
  5. Ngay sau khi `Attempt 1 -> ACCEPTED`, `BiasZ` trở về đúng `+0.36 dps`. Toàn bộ các chu kỳ telemetry sau đó đạt **100% `Stat: 1` và `dX: +0, dY: +0`**, chấm dứt hoàn toàn hiện tượng trôi dạt!

- **Bước 8 (Thử Bluetooth với PC)**: `NOT_TESTED` (Người dùng đang kết nối board với laptop qua RFC2217; board đã tự động kết nối BLE HID thành công với laptop qua sự kiện `ESP_GAP_BLE_AUTH_CMPL_EVT` tại `20:51:59.418`).

---

## 6. Danh mục Tệp tin và Mã băm Toàn vẹn SHA-256

### 6.1. Các tệp nhật ký đo kiểm mới tạo (trong `raw_logs/`)
| Tệp nhật ký | Kích thước | SHA-256 đầy đủ |
|---|---|---|
| `raw_logs/calib_fix_2026-10-10_A_still_retry2.log` | 6,482 B | `063d8867e973b81bd539a40dae9448e8ba2fbc71e565f50a27bb023080ab4ebe` |
| `raw_logs/calib_fix_2026-10-10_B_held.log` | 6,957 B | `32fa298852d67a56f334c56a6f3c1a348d805c398534bd491b61bf94eea7efc7` |
| `raw_logs/calib_fix_2026-10-10_B_held_retry1.log` | 7,190 B | `f2af2c409d4eb5f20bec835cba11cef87e6e061c11f71191d8fdb631894fe0e1` |
| `raw_logs/calib_fix_2026-10-10_C_cmd.log` | 8,231 B | `84208174ef29eb0532e7a8b701f7171a890216a225a3cba4cf9ebc6f56fa3e9f` |
| `raw_logs/calib_fix_2026-10-10_C_cmd_input.txt` | 5 B | `1215bb453f6057a6217482a4666498801d90471b072fdfbb7d9435b80eeae3f0` |

### 6.2. Kiểm tra tính bất biến của 8 tệp gốc do Claude chuẩn bị
| Tệp nguồn | SHA-256 mong đợi (16 ký tự đầu) | SHA-256 đo được thực tế | Trạng thái |
|---|---|---|---|
| `firmware/firmware.ino` | `1f1213b5a24b6698` | `1f1213b5a24b669883095a2948f871bb4179393a496ab340ca8a54caf1a087cd` | **MATCH** |
| `firmware/src/motion_pipeline.cpp` | `0681b298b7e98d05` | `0681b298b7e98d05cff9845ac1fc60e38061e0a8627a5d4c405ce1c21154b5be` | **MATCH** |
| `firmware/include/motion_pipeline.h` | `0d95adb9a6d21ef6` | `0d95adb9a6d21ef6da4c5ea2b866391a698aa0b2fbc6bf66eb731bebba44ce3d` | **MATCH** |
| `firmware/.pio/build/esp32dev/firmware.bin` | `d45365983a5e72fe` | `d45365983a5e72febf52d1ae2154781a0618d6a2b5cc0c118db0f2c075a30dbd` | **MATCH** |
| `firmware/.pio/build/esp32dev/bootloader.bin` | `3d234a7471f67b01` | `3d234a7471f67b013686dabd4dee7c1fa915c9928463616a94bc9297acf1abf8` | **MATCH** |
| `firmware/.pio/build/esp32dev/partitions.bin` | `148b959cbff1c38a` | `148b959cbff1c38aa8e1d5c0ba9d612c54997b945e56a63f41223eef650653a1` | **MATCH** |
| `scripts/capture_serial.py` | `c3675d7c86a9b2c4` | `c3675d7c86a9b2c4a56b954e647b0a370318b635be10cb5151b3fc49b3535816` | **MATCH** |
| `scripts/gain_tuner.py` | `7daa843ca7035c6d` | `7daa843ca7035c6dad5727f14fed188a98f32e07d0029933aa205d03496f8f66` | **MATCH** |

---

## 7. Các Hiện tượng Bất thường Đã Xử lý và Khuyến nghị

1. **Sụt áp cổng USB trước PC (Brownout)**:
   - *Hiện tượng*: Khi cắm board vào cổng USB trước của vỏ case PC, lúc ESP32 kích hoạt khối phát sóng BLE radio, nguồn 5V bị sụt áp làm ESP32 reset (`rst:0x10 (RTCWDT_RTC_RESET)`).
   - *Xử lý*: Chuyển cáp USB sang cắm trực tiếp vào cổng USB trên bo mạch chủ (mainboard) sau lưng PC, nguồn cấp ổn định 100%, không còn brownout.
2. **Xung đột mã hóa ký tự (Encoding Glitch) trên Windows**:
   - *Hiện tượng*: Python 3.14 trên Windows console mặc định cp1252 bị vấp lỗi `UnicodeEncodeError` khi gặp các ký tự rác nhị phân đầu tiên lúc chip khởi động.
   - *Xử lý*: Thiết lập biến môi trường `$env:PYTHONIOENCODING = "utf-8"` trong phiên chạy PowerShell mà không can thiệp sửa mã nguồn script.
3. **Bộ lọc ký tự của `scripts/gain_tuner.py`**:
   - *Hiện tượng*: Tại dòng 73, `gain_tuner.py` chỉ cho phép các ký tự `+-?` (`ser.write(bytes(c for c in data if chr(c) in "+-?"))`), dẫn đến ký tự `c` bị lọc bỏ.
   - *Xử lý*: Để tuân thủ Luật 1 (bảo toàn SHA-256 của `scripts/gain_tuner.py`), Anti không sửa file trong repo mà tạo bản chạy tạm trong thư mục Temp hệ thống (`$env:TEMP\tuner_c.py`) mở rộng thêm ký tự `c`.
4. **Hạng mục còn chờ (Next Steps)**:
   - Ghép nối BLE với PC (nếu người dùng cần điều khiển trực tiếp chuột trên màn hình PC).
   - Tinh chỉnh hệ số Gain mặc định trong code theo cảm giác tay nếu 0.3 chưa tối ưu.
   - Lập trình nút Clutch (GPIO27) giữ lâu (>2s) để tự kích hoạt hiệu chuẩn lại trên phần cứng mà không cần mở Serial.

---

## 8. Sai lệch so với Kế hoạch Handoff

1. **Môi trường đo Ca C**: Do người dùng di chuyển sang sử dụng laptop, Ca C được tiến hành qua cầu RFC2217 (`rfc2217://<LAPTOP_IP>:4000?ign_set_control`) thay vì cổng `COM3` cục bộ.
2. **Khởi chạy Ca C**: Khởi chạy qua `$env:TEMP\tuner_c.py` do `scripts/gain_tuner.py` lọc cứng chỉ nhận `+-?`.
3. Ngoài hai điểm trên, toàn bộ quy trình, phương thức thu thập log, tính toán số liệu và cam kết không sửa mã nguồn dự án đều được tuân thủ nghiêm ngặt 100%.
