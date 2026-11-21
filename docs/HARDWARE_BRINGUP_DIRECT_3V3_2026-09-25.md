# BÁO CÁO THỰC NGHIỆM HARDWARE BRING-UP: KẾT NỐI TRỰC TIẾP 3.3V GIỮA ESP32 VÀ WCMCU-20948

> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems)  
> **Thời điểm thực hiện**: Ngày 25 tháng 09 năm 2026  
> **Mục tiêu**: Xác minh thực nghiệm trên bàn (Bench-test) khả năng giao tiếp I2C trực tiếp ở mức điện áp 3,3 V giữa bo vi điều khiển ESP32 Classic DevKit 38-pin và module cảm biến WCMCU-20948 (InvenSense ICM-20948) mà nhóm đang sở hữu.  
> **Trạng thái thực nghiệm**: `BENCH_VERIFIED_ON_OWNED_MODULE` / `DIRECT_3V3_FUNCTIONAL_CONFIRMED`  
> **Chốt chặn KiCad & BLE**: `KICAD_SYNC_STATUS: STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE`; `BLE_CONNECTION_STATUS: NOT_TESTED`

---

## 1. Bảng Bảo Toàn Bằng Chứng Số (Raw Logs SHA-256 Checksum Audit)

Toàn bộ các tệp nhật ký thô được tạo ra từ phần cứng thực tế trên cổng `COM8` được lưu trữ nguyên vẹn tại thư mục `raw_logs/` và được kiểm soát toàn vẹn bằng mã băm SHA-256:

| Tên tệp nhật ký (File Path) | Dung lượng | Mã băm SHA-256 (Checksum) | Nội dung & Mục đích kiểm chứng |
| :--- | :---: | :--- | :--- |
| `raw_logs/esptool_chip_id.log` | 551 B | `fa5eb4951cdbf100cd917d9ce6a3b5388379ff89767a5500db665e1f36735a25` | Nhận dạng vi điều khiển: ESP32-D0WD-V3 (rev v3.1), thạch anh 40 MHz. |
| `raw_logs/esptool_flash_id.log` | 604 B | `d142fd348fe31693de7ad022f397ec8ea69bf29f7a9e6ad0f15728f35fbb7fa7` | Nhận dạng bộ nhớ Flash: Dung lượng 4 MB, điện áp 3.3V, chế độ DIO. |
| `raw_logs/probe_output.log` | 3271 B | `e2f5b4b2c009b0dda17671720d4840aff2854fa2b3bbed355caa1ff1e10c9b7f` | **Lần thử đầu thất bại (Initial Failed Attempt)** do dây cắm lỏng / nhầm chân cắm. |
| `raw_logs/probe_i2c_result.log` | 4197 B | `a069f551f77dde71034966df6779e697fff4256dd1bb284c90d555fcc35d4d4d` | **Lần thử probe thành công**: Quét I2C ra ACK 0x68, WHO_AM_I = 0xEA, test 100 lần đọc ở 100k/400k. |
| `raw_logs/main_firmware_boot.log` | 2327 B | `b7703685e4b13540ed12d39b3c8b2fde8d237ab0b661bb991dbe003f575be612` | **Firmware chính chạy thực tế**: Readback thanh ghi, hiệu chuẩn 200 mẫu, phát BLE, lặp 100 Hz. |
| `raw_logs/com8_boot.log` | 106 B | `fbfc80fc0f43411644d9992dc46eefe25de900a6c29726514b80783b9d4b9bb1` | Log bắt kết nối ban đầu của cổng COM8. |

---

## 2. Ghi Nhận Lần Thử Đầu Thất Bại & Nguyên Nhân (Initial Failed Attempt Audit)

Nhóm công khai và giữ nguyên vẹn tệp `raw_logs/probe_output.log` ghi lại lần thử đầu tiên không phát hiện được cảm biến.

### 2.1 Hiện tượng ghi nhận trong `probe_output.log`
```text
>>> STARTING I2C SCAN @ 100000 Hz (SDA=21, SCL=22) <<<
[I2C SCAN RESULT] NO I2C devices found on bus!
[ERROR] Neither 0x68 nor 0x69 responded to I2C ping!
[  2194][E][Wire.cpp:499] requestFrom(): i2cWriteReadNonStop returned Error -1
[00001] Read error (code=5, whoami=0x00)
```

### 2.2 Phân tích nguyên nhân kỹ thuật
1. **Dây cắm lỏng và bố cục chân DevKit**: Trên hàng chân bên phải của bo ESP32 Classic DevKit 38-pin, chân `GPIO22 (SCL)` nằm ở chân thứ 3, tiếp theo là hai chân UART nạp `U0RXD (GPIO3)` và `U0TXD (GPIO1)`, rồi mới đến chân `GPIO21 (SDA)`. 
2. Trong lần cắm ban đầu, dây cắm jumper breadboard bị lỏng tiếp xúc và dây SDA bị cắm nhầm sang hàng chân lân cận, khiến đường truyền I2C bị hở mạch.
3. Sau khi kiểm tra lại sơ đồ chân, cắm chặt dây đúng vị trí chân vật lý (`GPIO21 = Pin 6` của hàng phải, `GPIO22 = Pin 3` của hàng phải), bus I2C lập tức hoạt động bình thường.

---

## 3. Bằng Chứng Thực Nghiệm Chi Tiết

### 3.1 Nhận dạng phần cứng vi điều khiển ESP32
Trích xuất từ `raw_logs/esptool_chip_id.log` và `raw_logs/esptool_flash_id.log`:
- Cổng kết nối: `COM8` (Silicon Labs CP210x USB to UART Bridge, `VID:PID = 10C4:EA60`).
- Chip Type: **ESP32-D0WD-V3 (revision v3.1)**, Dual Core Xtensa 240 MHz.
- Tần số thạch anh: **40 MHz**.
- Địa chỉ MAC: `MAC_REDACTED` (được bảo vệ quyền riêng tư trong tài liệu sinh viên).
- Bộ nhớ Flash: **4 MB**, SPI speed 40 MHz, SPI mode DIO, điện áp Flash **3.3V**.

### 3.2 Nhận diện cảm biến và kiểm thử bus I2C (Probe Test)
Trích xuất từ `raw_logs/probe_i2c_result.log`:
- **Quét bus I2C**: Phản hồi ACK duy nhất tại địa chỉ 7-bit **`0x68`** (đúng cấu hình AD0 nối GND).
- **Chuyển Bank**: Thanh ghi `REG_BANK_SEL` (`0x7F = 0x00`) trả về mã `Wire.endTransmission() = 0` (SUCCESS).
- **Định danh cảm biến**: Thanh ghi `REG_WHO_AM_I` (`0x00` Bank 0) trả về chính xác **`0xEA`** (khớp hoàn toàn định danh chip ICM-20948).
- **Độ ổn định bus ngắn hạn tại 100 kHz**:
  - 100/100 lần đọc WHO_AM_I thành công trong phép thử ngắn hạn. (0 NACK / 0 lỗi bus).
- **Độ ổn định bus ngắn hạn tại 400 kHz (Fast-Mode)**:
  - 100/100 lần đọc WHO_AM_I thành công trong phép thử ngắn hạn. (0 NACK / 0 lỗi bus).
- **Đặc điểm nhật ký**: Tệp log có chứa một số đoạn ký tự thừa và tín hiệu reset do DTR/RTS khi mở cổng Serial; nhóm không gọi đây là clean log tuyệt đối mà bảo tồn trung thực dữ liệu nhận từ phần cứng.
- **Đọc dữ liệu thô (Burst read 12-byte)**:
  ```text
  [00001] WHO=0xEA | A:(  +500,   +112, +16256) | G:(   -53,   -159,    +47) | OK
  [00002] WHO=0xEA | A:(  +440,   +132, +16172) | G:(   -47,   -123,    +75) | OK
  ```
  Trục Z gia tốc ghi nhận giá trị $\approx +16200 \text{ LSB}$, phản ánh gia tốc trọng trường $1g$ khi đặt cảm biến nằm yên trên mặt bàn phẳng. Chương trình probe (`firmware_probe/`) không ghi `ACCEL_CONFIG`, nên thanh ghi giữ giá trị reset `0x01` (dải $\pm 2g$, $16384\,\text{LSB}/g$ theo DS-000189 §3.2). **Firmware chính dùng dải $\pm 4g$ (`ACCEL_CONFIG = 0x1B`), khi đó $1g \approx 8192\,\text{LSB}$.**

### 3.3 Hoạt động của Firmware chính thức (`raw_logs/main_firmware_boot.log`)
Firmware chính thức (`firmware/`) biên dịch thành công (RAM: 39.628 / 327.680 byte; Flash: 1.158.973 / 1.310.720 byte) và nạp lên ESP32. Kết quả khởi động ghi nhận:
1. **Khởi tạo I2C 400 kHz**:
   ```text
   [INIT] Initializing ICM-20948 Sensor Bus (400 kHz)...
   [   557][I][esp32-hal-i2c.c:75] i2cInit(): Initialising I2C Master: sda=21 scl=22 freq=400000
   ```
2. **Firmware chính đọc lại thanh ghi vật lý thành công.** (Register Readback):
   - `WHO_AM_I` (Bank 0, 0x00): `0xEA` `[PASS]`
   - `PWR_MGMT_1` (Bank 0, 0x06): `0x01` `[PASS]` (CLKSEL=Auto-PLL, SLEEP=0)
   - `GYRO_CONFIG_1` (Bank 2, 0x01): `0x1B` `[PASS]` (FS=500dps, DLPF=51.2Hz)
   - `ACCEL_CONFIG` (Bank 2, 0x14): `0x1B` `[PASS]` (FS=4g, DLPF=50.4Hz)
   - `GYRO_SMPLRT_DIV` (Bank 2, 0x00): `10` `[PASS]` (ODR ~102.27 Hz)
   - `ACCEL_SMPLRT_DIV` (Bank 2, 0x10-11): `10` `[PASS]` (ODR ~102.27 Hz)
3. **Hiệu chuẩn trôi tĩnh khởi động**:
   - Thu thập đủ 200 mẫu đo thực tế trong 2200 ms.
   - Zero-rate bias: $X = -0.55\,\text{dps}$, $Y = -1.25\,\text{dps}$, $Z = +0.37\,\text{dps}$.
4. **Trạng thái BLE & Vòng lặp**:
   - Gọi hàm bắt đầu quảng bá BLE: `Starting BLE HID Mouse Advertising as 'AirMouse-ESP32'`.
   - Vòng lặp chính duy trì tần số $\approx 100\,\text{Hz}$ (`Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX: +0, dY: +0`).
   - **Ranh giới kiểm thử**: Phát hiện BLE (Discovery) và Kết nối chuột HID tới máy tính hiện ở trạng thái `NOT_TESTED`.

---

## 4. Ranh Giới Kỹ Thuật & Giới Hạn Kết Luận

1. **Phạm vi kết luận**:
   - Kết quả này xác nhận: **Hoạt động thành công trên đúng module WCMCU-20948 và ESP32 mà nhóm đang sở hữu.**
   - Đây là quyết định kỹ thuật ở cấp độ mẫu thử nghiệm (prototype baseline) nhằm đơn giản hóa mạch in 1 lớp, loại bỏ rủi ro tiếp xúc của các module trung gian.
2. **Quy định datasheet của IC trần**:
   - Datasheet của nhà sản xuất TDK InvenSense (DS-000189) quy định dải hoạt động của IC trần là $V_{DD} = 1.71\text{--}3.6\,\text{V}$ nhưng $V_{DDIO} = 1.71\text{--}1.95\,\text{V}$ (§3.4); giới hạn tuyệt đối của $V_{DDIO}$ là $2.5\,\text{V}$ (§3.7, Table 9).
   - Nhóm không xóa dữ kiện này và không khẳng định mọi module WCMCU-20948 trên thị trường đều chịu được 3,3 V. Tuy nhiên, trên bo mạch breakout thương phẩm WCMCU-20948 cụ thể của nhóm, không ghi nhận NACK hoặc lỗi bus trong phép thử ngắn hạn đã ghi log khi cấp nguồn 3,3 V trực tiếp từ ESP32.
3. **Ranh giới tuyên bố minh bạch (Scope of Claims)**:
   - Nhóm không đưa ra tuyên bố mang tính khẳng định tuyệt đối về độ an toàn điện trên mọi điều kiện biên, không tuyên bố mức điện áp 3,3 V này phù hợp với định mức danh định của riêng IC trần, và chưa thực hiện các phép thử stress-test để kết luận về tuổi thọ lâu dài của linh kiện.
   - Nhóm ghi nhận trạng thái kết nối Bluetooth HID tới máy tính là chưa kiểm thử (`BLE_CONNECTION_STATUS: NOT_TESTED`), không tuyên bố chuột đã ghép nối thành công.

---

## 5. Danh Mục Hành Động Đồng Bộ Hệ Thống (Next Phase Actions)

- [x] Tạo báo cáo bằng chứng `docs/HARDWARE_BRINGUP_DIRECT_3V3_2026-09-25.md`.
- [ ] Cập nhật `docs/AIR_MOUSE_HARDWARE_ARCHITECTURE.md` (chuyển sang Direct 3.3V, loại bỏ BSS138 và LDO 1.8V).
- [ ] Cập nhật `docs/BOM_V1.md` (tính toán lại số lượng đơn vị, số dòng và chi phí).
- [ ] Cập nhật `firmware/include/pin_definitions.h` (chỉ sửa chú thích kết nối, không đổi chân GPIO).
- [ ] Bổ sung phần thực nghiệm vào `docs/research/WCM20948_DIRECT_ESP32_WIRING_RESEARCH.md`.
- [ ] Tái tạo Báo cáo giữa kỳ DOCX/PDF và Cẩm nang hỏi đáp từ các script generator nguồn.
- [ ] Giữ nguyên KiCad ở trạng thái `STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE` (không can thiệp tệp EDA trong tác vụ tài liệu).
