# BÁO CÁO KỸ THUẬT & BASELINE GIỮA KỲ (TUẦN 5) — AIR MOUSE BLE HID
## KIẾN TRÚC: HYBRID 9-AXIS AIR MOUSE

> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems)  
> **Phần cứng mục tiêu**: ESP32 Classic DevKit 38-pin + Breakout ICM-20948 (WCMCU-20948)  
> **Phiên bản**: V2.0.0 — Hybrid Midterm Week 5 Baseline  
> **Trạng thái**: `CANONICAL_HYBRID_MIDTERM_BASELINE`  

---

## 1. Đề tài Hiện tại (Project Definition & Concept)

### 1.1 Khái niệm & Bản chất Kỹ thuật
Hệ thống là thiết bị chuột bay không gian không dây mang tên **Hybrid 9-Axis Air Mouse**, kết hợp vi điều khiển **ESP32 Classic** và cảm biến quán tính 9 trục **ICM-20948** truyền dữ liệu qua giao thức chuẩn **Bluetooth Low Energy (BLE) Human Interface Device (HID)**.

- **Con quay hồi chuyển (Gyroscope)**: Đo vận tốc góc xoay cổ tay ($\pm 500^{\circ}/\text{s}$) phục vụ điều khiển con trỏ theo nguyên lý vận tốc tương đối (Relative Rate-Control).
- **Gia tốc kế (Accelerometer)**: Đo gia tốc 3 trục ($\pm 4g$) làm chức năng phụ trợ thông minh: (1) Nhận diện trạng thái đứng yên để tự động bù trôi (Stationary Auto-Zero); (2) Ước lượng vector trọng trường để thiết lập hệ quy chiếu thích nghi; (3) Nhận diện cử chỉ vung tịnh tiến ngắn (Translational Flick Gesture: Back/Forward).
- **Cơ chế Ly hợp & Tái định tâm (Clutch & Recenter)**: Bấm giữ `BTN_MODE` để đóng băng chuột và đổi tư thế cầm tự do (kể cả chĩa lên trời), nhả nút để xác lập mặt phẳng điều khiển trực quan mới.
- **Đầu ra máy tính**: Chuẩn chuột BLE HID tiêu chuẩn nhận diện cắm-là-chạy (plug-and-play) trên Windows / macOS / Linux / Android.

### 1.2 Luồng Dữ liệu Toàn Hệ Thống (Hybrid End-to-End Data Path)
```text
[ Chuyển động xoay & vung tay người dùng ]
                 │
                 ▼
[ Cảm biến ICM-20948 (Phần cứng cảm biến 1.8V) ]
   ├── (1) Khối MEMS Gyroscope 3 trục (Pitch, Yaw, Roll) + Hardware DLPF 51.2 Hz
   ├── (2) Khối MEMS Accelerometer 3 trục (X, Y, Z) + Hardware DLPF 50.4 Hz
   ├── (3) Bộ chuyển đổi ADC 16-bit nội bộ độc lập
   └── (4) Xuất dữ liệu qua User Bank 0: ACCEL_X/Y/ZOUT (0x2D) & GYRO_X/Y/ZOUT (0x33)
                 │
                 ▼ (Giao tiếp I2C Fast-Mode 400 kHz nối trực tiếp 3.3V (BENCH_VERIFIED_ON_OWNED_MODULE))
[ Vi điều khiển ESP32 Classic (Firmware Engine) ]
   ├── (5) Đọc Burst liên tục 12 byte qua I2C Master (Wire.h)
   ├── (6) Chuyển đổi đơn vị vật lý: ω = Raw / 65.5 (°/s), a = Raw / 8192.0 (g)
   ├── (7) Bộ nhận diện đứng yên (Stationary Detector): ||ω|| < 1.2 dps & |||a|| - 1g| < 0.08g
   │         ├── ĐỨNG YÊN: Cập nhật Auto-Zero Bias thích nghi & ép Delta = 0 (Anti-creep)
   │         └── CHUYỂN ĐỘNG: Trừ Bias tĩnh (ω - Bias) & qua vùng chết Deadzone (0.8 dps)
   ├── (8) Quản lý Ly hợp & Tái định tâm (Clutch / Recenter via BTN_MODE):
   │         ├── ĐANG GIỮ NÚT: Đóng băng con trỏ, phân tích cử chỉ Flick Trái/Phải
   │         └── NHẢ NÚT: Chụp lại hướng trọng trường làm mặt phẳng điều khiển tham chiếu mới
   ├── (9) Phép chiếu tọa độ thích nghi (Adaptive Reference Frame Transform):
   │         Chiếu vận tốc góc vào mặt phẳng vuông góc với mắt nhìn (giữ trực quan khi chĩa lên trời)
   └── (10) Ánh xạ độ nhạy & Clamping: Gyro Rate → Relative Mouse Delta (dX, dY)
                 │
                 ▼ (Bản tin BLE HID Mouse Report định kỳ 10 ms)
[ Máy tính / Host PC (Con trỏ di chuyển tương đối; nhận phím Back/Forward) ]
```

### 1.3 Cam kết Bản chất: Relative Rate-Control vs Translational Gesture vs True Position
> [!IMPORTANT]
> **CAM KẾT KỸ THUẬT RẠCH RÒI**:
> 1. **Relative Rate-Control**: Con trỏ điều khiển theo vận tốc xoay cổ tay tương đối. Ngay cả khi bàn tay đứng yên trong không gian, việc xoay cổ tay vẫn tạo ra $(\Delta X, \Delta Y)$. Dừng xoay là chuột dừng.
> 2. **Translational Flick Gesture**: Nhận dạng mẫu xung gia tốc có chu kỳ (Vung đi + Giật lại) để kích hoạt sự kiện nút Back/Forward. **KHÔNG ĐO QUÃNG ĐƯỜNG DI CHUYỂN**.
> 3. **Vị trí Thực 3D (True XYZ Position)**: **TUYỆT ĐỐI KHÔNG TÍCH PHÂN GIA TỐC KẾ 2 LẦN** vì sai số trôi bùng nổ theo bình phương thời gian ($t^2$) phá hủy khả năng điều khiển.
> 4. **Orientation Estimation**: Chỉ là **HÀM HỖ TRỢ NỘI BỘ** để thiết lập khung tham chiếu góc cầm; **KHÔNG PHẢI 3DoF ABSOLUTE POINTER**.

---

## 2. Bốn Câu hỏi Trọng tâm của Giảng viên (Week 5 Focus)

Hệ thống tài liệu và kiến thức của nhóm được tổ chức bám sát các câu hỏi kiểm tra giữa kỳ của giảng viên:

1. **Nội dung nhóm đang làm gì?**  
   $\rightarrow$ Thiết kế, chế tạo và lập trình chuột bay Hybrid 9-Axis Air Mouse BLE HID: Gyroscope điều khiển con trỏ tương đối, Accelerometer hỗ trợ chống trôi, đứng yên và nhận dạng cử chỉ vung tịnh tiến ngắn, tích hợp tái định tâm góc nhìn tự do.
2. **Để làm ứng dụng này cần những ngoại vi nào?**  
   $\rightarrow$ Liệt kê tường minh và phân biệt rõ: ngoại vi nội tại bên trong chip ESP32 (I2C Controller, GPIO In, GPIO Out, ADC1, BLE) và thiết bị ngoại vi kết nối bên ngoài (Cảm biến ICM-20948).
3. **Chọn 1 ngoại vi để phân tích chi tiết:**  
   - Thanh ghi cấu hình là gì? Địa chỉ bao nhiêu?
   - Độ rộng bao nhiêu bit?
   - Từng bit/nhóm bit có chức năng gì?
   - Cấu hình thực tế nằm ở đâu trong mã nguồn?
   - Giá trị cấu hình thực tế khi vận hành là bao nhiêu?
   - Phân tích chi tiết 1 ngoại vi với khoảng 2 thanh ghi cốt lõi.
4. **Sử dụng thư viện gì và tập lệnh tác động phần cứng như thế nào?**  
   - Các hàm/lệnh thực sự được gọi trong chương trình.
   - Mỗi lệnh tác động đến thanh ghi/phần cứng nào.
   - Tham số đầu vào (Input) của lệnh.
   - Kết quả trả về (Output) và hiệu ứng phần cứng thực tế (Hardware Effect) của lệnh.

---

## 3. Bản đồ Ngoại vi Hệ thống (Peripherals Baseline)

Nhóm phân định rạch ròi giữa các khối ngoại vi tích hợp sẵn trong vi điều khiển ESP32 và thiết bị ngoại vi phần cứng bên ngoài:

```
+-------------------------------------------------------------------------+
| ESP32 CLASSIC DUAL-CORE MCU                                             |
|                                                                         |
|  [ I2C0 Master Controller ] <====== (I2C Bus: SDA/SCL) ======> [ICM-20948]
|  [ GPIO Input Controller  ] <------ (Active-Low Buttons) <---- [3x PushButtons]
|  [ GPIO Output Controller ] ------> (Current-Limited) --------> [Status LED]
|  [ SAR ADC1 Controller    ] <------ (1:1 Voltage Divider) <--- [LiPo Battery]
|  [ 2.4GHz BLE Subsystem   ] ~ ~ ~ ~ (HID GATT Over-the-Air) ~> [Host PC]
+-------------------------------------------------------------------------+
```

### 3.1 Bảng Phân nhóm & Vai trò Ngoại vi

| Nhóm | Tên Ngoại vi | Ký hiệu / Kênh | Vai trò trong Ứng dụng Air Mouse |
|---|---|---|---|
| **Nội vi ESP32** | I2C Controller | I2C0 Master | Khởi tạo giao dịch đọc/ghi dữ liệu với cảm biến ICM-20948 ở tốc độ $400\,\text{kHz}$. |
| **Nội vi ESP32** | GPIO Input | GPIO25, 26, 27 | Đọc trạng thái 3 nút bấm cơ học: Chuột Trái (Left), Chuột Phải (Right), Nút Chế độ (Mode). |
| **Nội vi ESP32** | GPIO Output | GPIO32 | Điều khiển bật/tắt LED trạng thái hệ thống (báo nguồn, trạng thái kết nối BLE, hiệu chuẩn). |
| **Nội vi ESP32** | Analog-to-Digital Converter | SAR ADC1 (ADC1_CH6 - GPIO34) | Đo điện áp pin LiPo 1S thông qua cầu phân áp $100\,\text{k}\Omega / 100\,\text{k}\Omega$ để giám sát dung lượng nguồn. |
| **Nội vi ESP32** | Bluetooth Low Energy | 2.4GHz BLE Radio / Link Layer | Quảng bá dịch vụ HID (Human Interface Device over GATT), duy trì kết nối và gửi bản tin chuyển động chuột. |
| **Ngoại vi Ngoài**| Cảm biến Chuyển động | ICM-20948 (WCMCU-20948) | Đo tốc độ góc xoay của cổ tay (Gyroscope 3 trục X, Y, Z) và gia tốc tuyến tính (Accelerometer 3 trục). |

> [!NOTE]
> Không đưa các ngoại vi không sử dụng (như SPI, UART2, I2S, CAN/TWAI, DAC, Timer PWM động cơ) vào báo cáo để giữ đúng trọng tâm đồ án.

---

## 4. Bố trí Chân GPIO (Provisional Hardware Baseline)

> [!WARNING]
> **TRẠNG THÁI: `CURRENT DESIGN / PROVISIONAL`**  
> Toàn bộ sơ đồ nối chân dưới đây đã được kiểm tra trên sơ đồ nguyên lý mạch mang (Carrier Board V1) và tuân thủ các quy tắc cấm của ESP32 (tránh Strapping pins GPIO0, GPIO2, GPIO15; tránh Flash pins GPIO6-GPIO11; tận dụng chân input-only GPIO34 cho ADC). Sơ đồ này sẽ chuyển thành `HARDWARE_VERIFIED` ngay khi nạp kiểm chứng trên bo thực tế.

| Tín hiệu | Chân ESP32 | Chiều tín hiệu | Cấu hình & Điện áp | Ghi chú Thiết kế & An toàn |
|---|---|---|---|---|
| **I2C_SDA** | `GPIO21` | In/Out (Open-Drain) | $3.3\,\text{V}$ Logic (Direct 3.3V to WCMCU-20948) | Bus dữ liệu I2C, có điện trở kéo ngoài $10\,\text{k}\Omega$. |
| **I2C_SCL** | `GPIO22` | Output (Open-Drain) | $3.3\,\text{V}$ Logic (Direct 3.3V to WCMCU-20948) | Xung nhịp I2C Master, tốc độ chuẩn $400\,\text{kHz}$. |
| **BTN_LEFT** | `GPIO25` | Input | $3.3\,\text{V}$, Internal Pull-Up | Nút nhấn Chuột Trái (Left Click). Nhấn = LOW. |
| **BTN_RIGHT**| `GPIO26` | Input | $3.3\,\text{V}$, Internal Pull-Up | Nút nhấn Chuột Phải (Right Click). Nhấn = LOW. |
| **BTN_MODE** | `GPIO27` | Input | $3.3\,\text{V}$, Internal Pull-Up | Nút Chế độ / Bật-Tắt Air Mouse. Nhấn = LOW. |
| **LED_STATUS**| `GPIO32`| Output (Push-Pull) | $3.3\,\text{V}$, Nối tiếp trở $1\,\text{k}\Omega$ | Điều khiển LED báo trạng thái kết nối và hiệu chuẩn. |
| **BAT_SENSE**| `GPIO34` | Input (Analog) | $0\text{--}2.1\,\text{V}$ (từ cầu phân áp $1:1$) | Chân Input-Only thuộc ADC1 (kênh ADC1_CH6); tránh xung đột tài nguyên với driver Wi-Fi (vốn chiếm dụng ADC2). |

---

## 5. Định hướng Tiếp cận Mức Thanh ghi (Register-Level Direction)

Nhóm thống nhất phương pháp triển khai firmware theo định hướng: **Không phụ thuộc vào thư viện bên thứ ba đồ sộ của ICM-20948 (như SparkFun/InvenSense eMPL) để giải thích mạch lạc mức thanh ghi trước giảng viên**.

### 5.1 Kiến trúc Phần mềm Phân lớp
```text
[ Ứng dụng Air Mouse: Motion Processing & BLE HID Dispatcher ]
                              │
                              ▼
[ Driver Cảm biến mỏng tự viết (ICM20948_Minimal_Driver) ]
   ├── Quản lý chuyển Bank: selectBank(bank_number)
   ├── Ghi thanh ghi: writeReg(reg_addr, data_byte)
   ├── Đọc thanh ghi: readReg(reg_addr)
   └── Đọc cụm dữ liệu: readRegs(reg_addr, buffer, length)
                              │
                              ▼
[ Lớp Trừu tượng Giao tiếp Phần cứng: Arduino Wire.h (I2C Master) ]
                              │
                              ▼
[ Phần cứng I2C Controller của ESP32 ]
```

### 5.2 Lý do Kỹ thuật
- **Làm chủ cấu trúc chip**: Cảm biến ICM-20948 chia không gian thanh ghi thành 4 User Banks (Bank 0, 1, 2, 3). Thư viện tự viết giúp sinh viên hiểu rõ cơ chế chuyển bank và quản lý địa chỉ.
- **Minh bạch tham số vận hành**: Tự tay cấu hình từng bit của bộ lọc thông thấp (DLPF), dải đo toàn thang (Full-scale range) và chế độ quản lý nguồn (Power Management).
- **Tránh xung đột bộ nhớ**: Thư viện lớn thường chiếm dung lượng Flash/RAM lớn và chứa mã nguồn xử lý DMP (Digital Motion Processor) không cần thiết cho mục tiêu con trỏ chuột tương đối ở V1.

---

## 6. Ngoại vi Lựa chọn Phân tích: Con quay hồi chuyển (ICM-20948 Gyroscope)

Ngoại vi được chọn để trả lời câu hỏi 3 của giảng viên là **khối cảm biến con quay hồi chuyển (Gyroscope)** bên trong IC cảm biến ICM-20948.

> [!NOTE]
> **TRẠNG THÁI GIÁ TRỊ THANH GHI**: `VERIFIED AGAINST OFFICIAL TDK DOCUMENTATION`  
> Toàn bộ địa chỉ thanh ghi, tên bit, giá trị cấu hình (`PWR_MGMT_1 = 0x01`, `GYRO_CONFIG_1 = 0x1B`, `WHO_AM_I = 0xEA`, `REG_BANK_SEL = 0x7F`) đã được đối chiếu và xác minh chính xác theo *TDK InvenSense ICM-20948 Datasheet, Register Map and Descriptions DS-000189 v1.3/v1.5*.

### 6.1 Thanh ghi 1: `PWR_MGMT_1` (Quản lý Nguồn & Xung nhịp Hệ thống)
- **User Bank**: `Bank 0`
- **Địa chỉ thanh ghi (Address)**: `0x06` (`VERIFIED`)
- **Độ rộng**: `8 bit`
- **Giá trị cấu hình thực tế khi vận hành**: `0x01` (`0b00000001`)

#### Phân tích Chi tiết Từng Bit (Verified Bitfield Breakdown theo DS-000189):
| Bit | Tên Bit | Giá trị ghi | Chức năng Kỹ thuật |
|---|---|---|---|
| **7** | `DEVICE_RESET` | `0` | `1` = Reset toàn bộ thanh ghi nội về mặc định (tự xóa sau khi reset xong). Đặt `0` để duy trì hoạt động bình thường. |
| **6** | `SLEEP` | `0` | `1` = Đưa chip vào chế độ ngủ tiết kiệm điện (tắt toàn bộ khối analog). Đặt `0` để đánh thức chip hoạt động. |
| **5** | `LP_EN` | `0` | `1` = Chế độ Low-Power. Đặt `0` để cho phép ghi thanh ghi và chạy đo liên tục hiệu năng cao. |
| **4** | Reserved | `0` | Bit dự trữ, ghi mặc định `0`. |
| **3** | `TEMP_DIS` | `0` | `1` = Tắt cảm biến nhiệt độ. Đặt `0` để kích hoạt cảm biến nhiệt độ onboard. |
| **2:0** | `CLKSEL[2:0]` | `001` | Lựa chọn nguồn xung nhịp hệ thống: `001` = Tự động chọn nguồn xung nhịp tốt nhất (Auto selects the best available clock source — PLL nếu sẵn sàng, ngược lại dùng bộ dao động nội 20 MHz). |

- **Tác động phần cứng khi ghi `0x01`**: Đánh thức chip ICM-20948 ra khỏi trạng thái Sleep mặc định sau khi cấp nguồn và cấu hình mạch xung nhịp tự động chọn PLL con quay hồi chuyển khi ổn định để dữ liệu đo đạt độ chính xác cao nhất theo datasheet.

---

### 6.2 Thanh ghi 2: `GYRO_CONFIG_1` (Cấu hình Dải đo & Bộ lọc Gyro)
- **User Bank**: `Bank 2`
- **Địa chỉ thanh ghi (Address)**: `0x01` (`VERIFIED`)
- **Độ rộng**: `8 bit`
- **Giá trị cấu hình thực tế khi vận hành**: `0x1B` (`0b00011011`)

#### Phân tích Chi tiết Từng Bit (Verified Bitfield Breakdown):
| Bit | Tên Bit / Nhóm | Giá trị ghi | Chức năng Kỹ thuật |
|---|---|---|---|
| **7:6** | Reserved | `00` | Các bit dự trữ, ghi mặc định `0`. |
| **5:3** | `GYRO_DLPFCFG[2:0]` | `011` (`3`) | Cấu hình tần số cắt của bộ lọc dải thông thấp số (DLPF 3dB Bandwidth $\approx 51.2\,\text{Hz}$, độ trễ nhóm $\approx 5.9\,\text{ms}$). |
| **2:1** | `GYRO_FS_SEL[1:0]` | `01` (`1`) | Lựa chọn dải đo toàn thang (Full-Scale Range). `00` = $\pm 250^{\circ}/\text{s}$; `01` = $\pm 500^{\circ}/\text{s}$; `10` = $\pm 1000^{\circ}/\text{s}$; `11` = $\pm 2000^{\circ}/\text{s}$. Chọn $\pm 500^{\circ}/\text{s}$ phù hợp nhất với vận tốc vung cổ tay người. |
| **0** | `GYRO_FCHOICE` | `1` | Cho phép kích hoạt bộ lọc số DLPF (`1` = Enable DLPF theo cấu hình `GYRO_DLPFCFG`). |

- **Độ nhạy cảm biến (Sensitivity Scale Factor)**:
  Ứng với dải đo $\pm 500^{\circ}/\text{s}$, độ nhạy lý thuyết của bộ chuyển đổi ADC 16-bit là:
  $$\text{Sensitivity} = \frac{2^{15} - 1}{500^{\circ}/\text{s}} \approx 65.5\,\text{LSB}/(^{\circ}/\text{s})$$
- **Công thức chuyển đổi sang đơn vị vật lý**:
  $$\text{Vận tốc góc } \omega_z (^{\circ}/\text{s}) = \frac{\text{Raw\_Data} - \text{Bias}}{65.5}$$

---

## 7. Cơ chế Chuyển Bank Thanh ghi (Bank Switching Architecture)

Cảm biến ICM-20948 tổ chức bản đồ thanh ghi thành 4 User Bank riêng biệt (Bank 0, Bank 1, Bank 2, Bank 3) với tổng không gian địa chỉ 512 byte (4 x 128 byte, trong đó có khoảng 80–100 thanh ghi hoạt động thực tế). Cơ chế này giúp quản lý hệ thống cấu hình cảm biến 9 trục trong khi giao thức truyền thông thanh ghi tiêu chuẩn sử dụng địa chỉ 1 byte trực tiếp (0x00–0x7F).

- **Thanh ghi chọn Bank**: `REG_BANK_SEL`
- **Địa chỉ cố định trên mọi Bank**: `0x7F` (`VERIFIED`)
- **Phân bổ chức năng các Bank**:
  - **User Bank 0 (`0x00`)**: Chứa các thanh ghi dữ liệu chuyển động chính (`GYRO_X/Y/ZOUT`, `ACCEL_X/Y/ZOUT`), cấu hình nguồn `PWR_MGMT_1` (`0x06`), định danh chip `WHO_AM_I` (`0x00 = 0xEA`), và bộ đệm dữ liệu cảm biến ngoài `EXT_SLV_SENS_DATA_00..23`.
  - **User Bank 1 (`0x10`)**: Chứa các thanh ghi tự kiểm tra (Self-Test), hiệu chuẩn offset bias và cơ sở thời gian (Time-base).
  - **User Bank 2 (`0x20`)**: Chứa cấu hình bộ lọc số DLPF và dải đo con quay `GYRO_CONFIG_1` (`0x01 = 0x1B`), bộ chia tần số mẫu `GYRO_SMPLRT_DIV` (`0x00`), và cấu hình gia tốc kế.
  - **User Bank 3 (`0x30`)**: Chứa các thanh ghi cấu hình và điều khiển giao tiếp I2C Master nội bộ (`I2C_MST_CTRL`, `I2C_SLVx_ADDR`, `I2C_SLVx_REG`, `I2C_SLVx_CTRL`).
- **Cơ chế hoạt động**:
  - Muốn truy cập `PWR_MGMT_1` (nằm ở Bank 0): Ghi giá trị `0x00` (bits [5:4] = `00`) vào địa chỉ `0x7F`, sau đó đọc/ghi địa chỉ `0x06`.
  - Muốn truy cập `GYRO_CONFIG_1` (nằm ở Bank 2): Ghi giá trị `0x20` (bits [5:4] = `10`) vào địa chỉ `0x7F`, sau đó đọc/ghi địa chỉ `0x01`.

```cpp
void selectBank(uint8_t bank) {
    Wire.beginTransmission(ICM20948_I2C_ADDR); // Địa chỉ thiết bị 0x68
    Wire.write(0x7F);                          // Thanh ghi chọn Bank REG_BANK_SEL
    Wire.write(bank << 4);                     // Chuyển sang User Bank tương ứng
    Wire.endTransmission();
}
```

---

## 8. Bảng Đối chiếu Lệnh & Tác động Phần cứng (API / Command Baseline)

| Lệnh / Hàm trong Mã nguồn | Tham số Đầu vào (Input) | Kết quả Trả về (Output) | Tác động Phần cứng / Ngoại vi Thực tế (Hardware Effect) |
|---|---|---|---|
| `Wire.begin(21, 22, 400000)` | SDA pin (`21`), SCL pin (`22`), tần số xung nhịp (`400000` Hz) | `bool` (Thành công / Thất bại) | Bật bộ điều khiển ngoại vi I2C0 của ESP32, cấu hình chân GPIO21/22 sang chế độ Open-Drain, tạo xung nhịp SCL chuẩn $400\,\text{kHz}$. |
| `selectBank(bank)` | Số thứ tự User Bank (`0` đến `3`) | `void` | Gửi frame I2C ghi vào thanh ghi `0x7F` của ICM-20948, chuyển con trỏ bộ nhớ nội bộ của chip sang vùng thanh ghi mong muốn. |
| `writeReg(reg, val)` | Địa chỉ thanh ghi (`reg`), giá trị ghi (`val`) | `bool` (ACK / NACK) | Thực hiện chu kỳ I2C Master Write: START $\rightarrow$ Gửi Addr+W $\rightarrow$ Gửi Reg $\rightarrow$ Gửi Data $\rightarrow$ STOP. Cập nhật trực tiếp giá trị vào thanh ghi phần cứng của cảm biến. |
| `readReg(reg)` | Địa chỉ thanh ghi (`reg`) | `uint8_t` (Byte dữ liệu) | Thực hiện chu kỳ I2C Master Read: START $\rightarrow$ Gửi Reg $\rightarrow$ RESTART $\rightarrow$ Đọc Data $\rightarrow$ NACK $\rightarrow$ STOP. Thu nhận trạng thái thực tế của thanh ghi. |
| `readRegs(reg, buf, len)` | Địa chỉ bắt đầu (`reg`), con trỏ mảng (`buf`), số byte cần đọc (`len`) | `bool` | Thực hiện đọc liên tục nhiều byte (Burst Read) nhờ bộ tự động tăng con trỏ địa chỉ của ICM-20948, đọc nhanh 6 byte Gyro X, Y, Z trong 1 khung truyền. |
| `pinMode(pin, INPUT_PULLUP)` | Số chân GPIO (`25, 26, 27`), chế độ | `void` | Kích hoạt mạch điện trở kéo lên nguồn $3.3\,\text{V}$ nội bộ bên trong chân GPIO của ESP32; chân giữ mức HIGH khi nút nhả. |
| `digitalRead(pin)` | Số chân GPIO cần đọc | `int` (`HIGH` hoặc `LOW`) | Đọc trạng thái điện áp logic tại thanh ghi đệm đầu vào (Input Buffer) của chân GPIO. Nút nhấn làm ngắn mạch xuống GND $\rightarrow$ đọc được `LOW`. |
| `digitalWrite(pin, val)` | Số chân GPIO (`32`), giá trị (`HIGH/LOW`) | `void` | Đặt tầng khuếch đại kéo-đẩy (Push-pull driver) của GPIO32 lên $3.3\,\text{V}$ hoặc xuống $0\,\text{V}$, cấp dòng làm sáng LED hoặc tắt LED. |
| `analogRead(34)` | Số chân ADC (`34`) | `uint16_t` ($0\text{--}4095$) | Kích hoạt bộ chuyển đổi xấp xỉ liên tiếp (SAR ADC1) 12-bit chuyển đổi mức điện áp từ cầu phân áp thành giá trị số nguyên để tính dung lượng pin. |
| `bleMouse.move(dx, dy, wheel, hWheel)` | Độ dịch chuyển tương đối $\Delta X$, $\Delta Y$, con lăn cuộn | `void` | Đóng gói bản tin HID Mouse Report theo định dạng quy định bởi HID Report Descriptor (dự án dùng thư viện `T-vK/ESP32-BLE-Mouse`, bản tin **5 byte**: `[Buttons, dX, dY, Wheel, hWheel/Pan]`) và đẩy vào hàng đợi thông báo (GATT Notification) của ngăn xếp BLE. |

---

## 9. Mục tiêu Trình diễn Kỹ thuật Giữa kỳ (Week 5 Demo Target)

Để đảm bảo chắc chắn vượt qua các câu hỏi vấn đáp và thực hành giữa kỳ, nhóm xác định mục tiêu demo theo thứ tự ưu tiên:

### 9.1 Demo Tối thiểu Bắt buộc (Core Firmware Bring-up)
1. **Kiểm tra nhận diện phần cứng (`WHO_AM_I`)**:
   - Đọc thanh ghi `WHO_AM_I` (Bank 0, địa chỉ `0x00`).
   - Phản hồi mong đợi trên Serial Monitor: Giá trị cố định `0xEA` xác nhận ESP32 đã nối dây I2C chuẩn xác với ICM-20948.
2. **Ghi và Đọc lại cấu hình thanh ghi (Register Read-back Verification)**:
   - Ghi `PWR_MGMT_1` = `0x01`, đọc lại xác nhận = `0x01` (đã thoát Sleep, bật Clock).
   - Ghi `GYRO_CONFIG_1` = `0x1B`, đọc lại xác nhận = `0x1B` (đã cài đặt dải $\pm 500^{\circ}/\text{s}$, kích hoạt DLPF).
3. **Thu nhận và Chuyển đổi Vận tốc góc theo thời gian thực (Real-time Gyro Stream)**:
   - Đọc liên tục 6 thanh ghi Gyro Data (`GYRO_XOUT_H/L`, `GYRO_YOUT_H/L`, `GYRO_ZOUT_H/L`).
   - Ghép byte 16-bit có dấu (2's complement), trừ offset tĩnh (bias), chia cho hệ số $65.5\,\text{LSB}/(^{\circ}/\text{s})$.
   - Hiển thị trực tiếp đồ thị vận tốc góc ($^{\circ}/\text{s}$) trên Serial Plotter của Arduino IDE khi lắc cổ tay.

### 9.2 Demo Nâng cao (Bonus Milestone — Không làm Blocker)
- Khởi tạo stack BLE HID Mouse trên ESP32.
- Ghép nối Bluetooth với Laptop, khi lắc cổ tay con trỏ chuột trên màn hình máy tính dịch chuyển tương ứng.
- Nhấn các nút bấm GPIO25, GPIO26 thực hiện thao tác click chuột trái / chuột phải thực tế.
