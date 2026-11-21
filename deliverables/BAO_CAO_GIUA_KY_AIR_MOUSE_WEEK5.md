# BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỀ TÀI GIỮA KỲ (TUẦN 5)
## HỌC PHẦN: HỆ THỐNG NHÚNG (EMBEDDED SYSTEMS)

---

### THÔNG TIN CHUNG
* **Cơ sở đào tạo**: TRƯỜNG ĐẠI HỌC BÁCH KHOA — ĐHQG-HCM
* **Đơn vị quản lý**: KHOA ĐIỆN — ĐIỆN TỬ | BỘ MÔN ĐIỆN TỬ
* **Đề tài**: **NGHIÊN CỨU, THIẾT KẾ VÀ CHẾ TẠO CHUỘT BAY KHÔNG DÂY (AIR MOUSE BLE HID OVER GATT) DÙNG ESP32 VÀ ICM-20948**
* **Kiến trúc phần cứng**: Baseline Direct 3.3V Hardware Bring-up (ESP32 Classic DevKit 38-pin + WCMCU-20948)
* **Giảng viên hướng dẫn**: TS. [Tên Giảng viên hướng dẫn]
* **Nhóm sinh viên thực hiện (03 thành viên)**:
  1. Thành viên 1: [Họ tên sinh viên 1 — MSSV 1]
  2. Thành viên 2: [Họ tên sinh viên 2 — MSSV 2]
  3. Thành viên 3: [Họ tên sinh viên 3 — MSSV 3]
* **Thời điểm báo cáo**: Học kỳ 1 — Năm học 2026–2027 (Mốc đánh giá Tuần 5)

---

## MỤC LỤC BÁO CÁO
1. [MỤC TIÊU ĐỀ TÀI & KIẾN TRÚC HỆ THỐNG HIỆN TẠI](#1-mục-tiêu-đề-tài--kiến-trúc-hệ-thống-hiện-tại)
2. [CÁC KHỐI PHẦN CỨNG SỬ DỤNG & DỰ TOÁN BOM V2.0.0](#2-các-khối-phần-cứng-sử-dụng--dự-toán-bom-v200)
3. [BẢNG NỐI DÂY TÓM TẮT TOÀN HỆ THỐNG](#3-bảng-nối-dây-tóm-tắt-toàn-hệ-thống)
4. [TÓM TẮT LÝ THUYẾT CỐT LÕI (BẢNG TRÍCH YẾU)](#4-tóm-tắt-lý-thuyết-cốt-lõi-bảng-trích-yếu)
5. [CÔNG VIỆC ĐÃ HOÀN THÀNH & KẾT QUẢ THỰC NGHIỆM](#5-công-việc-đã-hoàn-thành--kết-quả-thực-nghiệm)
6. [CÔNG VIỆC CHƯA HOÀN THÀNH, HẠN CHẾ & VẤN ĐỀ TỒN TẠI](#6-công-việc-chưa-hoàn-thành-hạn-chế--vấn-đề-tồn-tại)
7. [KẾ HOẠCH TRIỂN KHAI GIAI ĐOẠN TIẾP THEO](#7-kế-hoạch-triển-khai-giai-đoạn-tiếp-theo)
8. [KẾT LUẬN & XÁC NHẬN BÁO CÁO](#8-kết-luận--xác-nhận-báo-cáo)

---

## 1. MỤC TIÊU ĐỀ TÀI & KIẾN TRÚC HỆ THỐNG HIỆN TẠI

### 1.1. Bản chất đề tài & Mục tiêu sản phẩm
Đề tài nghiên cứu, thiết kế và chế tạo thiết bị chuột không gian không dây (Air Mouse), cho phép người dùng điều khiển con trỏ chuột máy tính thông qua cử động xoay cổ tay tự nhiên trong không gian. Thiết bị hoạt động theo nguyên lý trỏ tương đối điều khiển theo tốc độ xoay (**Relative Rate-Controlled Pointing Device**): vận tốc góc xoay cổ tay ($\omega_{\text{Yaw}}, \omega_{\text{Pitch}}$) từ con quay hồi chuyển được ánh xạ tỉ lệ thuận sang độ dời con trỏ ($dX, dY$). Khi tay dừng lại ($\omega = 0$), con trỏ lập tức đứng yên. Hệ thống không sử dụng gia tốc kế tích phân kép để tìm vị trí không gian 3D nhằm triệt tiêu hoàn toàn sai số trôi tích lũy bùng nổ theo bình phương thời gian ($t^2$).

### 1.2. Kiến trúc hệ thống Direct 3.3V
Module cảm biến chuyển động WCMCU-20948 (mang chip ICM-20948 9-DOF) kết nối trực tiếp ở mức 3,3 V với vi điều khiển ESP32 Classic DevKit 38-pin qua bus I2C Fast-Mode ($400\,\text{kHz}$) trên hai chân GPIO21 (SDA) và GPIO22 (SCL). Thiết kế đã **loại bỏ hoàn toàn mạch chuyển mức logic BSS138 và IC ổn áp phụ AMS1117-1.8V** sau khi kiểm chứng thực nghiệm Bring-up thành công trên bàn đo. ESP32 đọc định kỳ $10\,\text{ms}$ ($100\,\text{Hz}$), trừ trôi tĩnh (zero-rate bias), ước lượng tư thế 6 trục qua bộ lọc bù Quaternion (Gyroscope + Accelerometer), áp dụng vùng chết chống rung và đóng gói thành bản tin báo cáo chuột HID tiêu chuẩn **5 byte: `[Buttons, dX, dY, Wheel, Pan]`**. Bản tin này được phát qua giao thức Bluetooth Low Energy (BLE HID over GATT).

### 1.3. Sơ đồ khối hệ thống mức kiến trúc (ASCII System Diagram)

```text
===========================================================================
        SƠ ĐỒ KHỐI HỆ THỐNG AIR MOUSE DIRECT 3.3V (V4.0.0 BASELINE)
===========================================================================

 [Cell Pin LiPo 1S] (3.7V, 1000mAh)
         |
         | (Cell + -> B+, Cell - -> B-)
         v
 [Module TP4056] <== Cổng Type-C sạc 5V
         |
         |-- OUT+ ---> [SW1 (ON/OFF)] ---> V_SYS ---> [MT3608 Boost 5V]
         |                                                   |
         +-- OUT- ---> System GND ---> MT3608 VIN-           v
                                                      [ESP32 DevKit]
                                                      (LDO 3.3V Onboard)
                                                             |
                 +-------------------------------------------+
                 |                     |                     |
            I2C 400 kHz           GPIO25/26/27            GPIO32
          (Direct 3.3V)           (Active-Low)               |
                 |                     |                     v
         [WCMCU-20948]            [3 Nút Bấm]           [R1 (1k)]
         - ICM-20948 (9-DOF)      - SW_LEFT: GPIO25          |
         - Gyro + Accel 6 trục    - SW_RIGHT: GPIO26         v
         - AD0=GND (0x68)         - SW_MODE: GPIO27     [LED Xanh Lá]
         - Trở kéo 10k onboard
         - AK09916: Chưa dùng

 [V_SYS] ---> [Cầu phân áp 100k/100k + C1] ---> GPIO34 (ADC1_CH6) ESP32
                                                (Chưa gọi trong firmware)

 [ESP32 BLE Subsystem] --- BLE HID Mouse 5 byte ---> [MÁY TÍNH PC / TV]
                                                     Trạng thái: NOT_TESTED

===========================================================================
QUY ƯỚC LIÊN KẾT:
  --->  Đường nguồn điện / Điều khiển một chiều (VBAT, V_SYS, 5V, 3V3, GND)
  I2C   Bus dữ liệu số hai chiều (SDA: GPIO21, SCL: GPIO22)
  BLE   Phát sóng BLE gói tin HID chuột 5 byte ([Btn, dX, dY, W, Pan])
===========================================================================
```

*Ghi chú*: Chi tiết mô tả bằng lời và chỉ dẫn mỹ thuật cho người thiết kế đồ họa được cung cấp đầy đủ trong tài liệu bàn giao [`deliverables/MO_TA_SO_DO_KHOI_AIR_MOUSE.md`](deliverables/MO_TA_SO_DO_KHOI_AIR_MOUSE.md).

---

## 2. CÁC KHỐI PHẦN CỨNG SỬ DỤNG & DỰ TOÁN BOM V2.0.0

Hệ thống phần cứng được chuẩn hóa trên bo mạch mang (Carrier Board) một lớp tự gia công, tích hợp 6 khối linh kiện chính:

| Phân hệ / Linh kiện | Phân loại ngoại vi | Thông số kỹ thuật cốt lõi | Vai trò trong hệ thống Air Mouse |
| :--- | :--- | :--- | :--- |
| **ESP32 DevKit 38-pin** | Nội (Internal MCU) | Xtensa 240MHz, 520KB SRAM, BLE 4.2, I2C Master, SAR ADC1 | Xử lý trung tâm: đọc I2C, motion pipeline, phát BLE HID. |
| **WCMCU-20948 (ICM-20948)** | Ngoại vi I2C (External) | IMU 9-DOF phần cứng, dung hợp 6 trục firmware, I2C 400kHz, 3.3V | Thu thập dữ liệu vận tốc góc (Gyro) và gia tốc (Accel). |
| **TP4056 Type-C + Bảo vệ** | Khối Nguồn (Power) | IC DW01A + FS8205A, dòng sạc 1A, bảo vệ quá nạp/quá xả/ngắn mạch | Quản lý sạc pin qua Type-C; B+/B- nối cell; OUT+ qua SW1; OUT- là gốc System GND. |
| **MT3608 DC-DC Boost** | Khối Nguồn (Power) | Dải ngõ vào 2–24V, ngõ ra chỉnh cố định 5.0V, hiệu suất ~93% | Nâng điện áp pin (3.0–4.2V) lên ổn định 5.0V cấp chân VIN ESP32. |
| **Pin LiPo 1S (523450)** | Khối Nguồn (Power) | 3.7V danh định, 1000mAh, có mạch bảo vệ PCM, cọc cắm JST-PH 2.0 | Cung cấp năng lượng di động; lắp mặt đáy có đệm Kapton + EVA. |
| **3 Nút Bấm & LED Chỉ Thị** | Giao tiếp Người Dùng | 3 Tactile 12x12mm cap Ø12mm (GPIO25, 26, 27); LED D1 3mm (GPIO32) | Phím chuột trái/phải/mode (Active-Low); LED báo trạng thái. |

### 2.1. Dự toán linh kiện BOM V2.0.0 đã tinh giản
Sau khi nghiệm thu kết nối Direct 3.3V thành công trên phần cứng sở hữu, nhóm đã loại bỏ hoàn toàn module BSS138 (giảm 10.000đ), IC LDO AMS1117-1.8V (giảm 8.000đ), tụ C3/C4 (giảm 1.500đ) và thu gọn cụm Test Points (giảm 500đ). Danh mục mua mới V2.0.0 gồm đúng **23 vật phẩm vật lý (20 dòng mua hàng)** với tổng chi phí dự toán **153.000 VNĐ**:

| Nhóm danh mục | Trạng thái | Số lượng | Linh kiện cấu thành tiêu biểu | Thành tiền (VNĐ) |
| :--- | :---: | :---: | :--- | :---: |
| **Linh kiện cốt lõi có sẵn** | `OWNED` | 2 linh kiện | ESP32 DevKit 38-pin (U1) + Module WCMCU-20948 (U2) | 0 VNĐ (Có sẵn) |
| **Khối Nguồn & Sạc Pin** | `BUY` | 5 vật phẩm | Pin LiPo 1S 1000mAh, TP4056 Type-C, MT3608 5V, SW1, Giắc JST | 97.500 VNĐ |
| **Khối Phím Bấm & Chỉ Thị** | `BUY` | 6 vật phẩm | 3 nút nhấn 12x12mm, LED xanh lá 3mm, Trở hạn dòng 1.0k, J2 I2C | 11.500 VNĐ |
| **Khối Thụ Động Đo Pin & Lọc** | `BUY` | 4 vật phẩm | 2 trở phân áp 100k (1%), Tụ lọc C1 100nF, Tụ hóa C2 10µF | 2.500 VNĐ |
| **Khối Socket Cắm Module** | `BUY` | 3 vật phẩm | 2 hàng cái 1x19 (ESP32) + 1 hàng cái 1x10 (WCMCU-20948) | 9.500 VNĐ |
| **Khối Header Test Points** | `BUY` | 1 vật phẩm | 1 dải đực 1x4 chân làm cọc đo kiểm Logic Analyzer (SCL, SDA, 3V3, GND) | 1.000 VNĐ |
| **Phụ Kiện Cơ Khí & An Toàn** | `BUY` | 4 vật phẩm | 3 nắp chụp nút Ø12mm + 1 bộ lót cách điện pin (Kapton + EVA Foam) | 31.000 VNĐ |
| **TỔNG CHI PHÍ DỰ TOÁN MUA MỚI** | **`BUY`** | **23 vật phẩm** | **20 dòng mua hàng** | **153.000 VNĐ** |

*Ghi chú*: Toàn bộ đơn giá là giá tham chiếu lịch sử; nhóm sẽ khảo sát giá thực tế tại chợ Nhật Tảo và sàn thương mại điện tử trước khi mua sắm.

---

## 3. BẢNG NỐI DÂY TÓM TẮT TOÀN HỆ THỐNG

Bảng nối dây tóm tắt định hướng vẽ sơ đồ nguyên lý (Schematic) trên KiCad theo chuẩn kết nối Direct 3.3V đã khóa:

| Khối mạch | Điểm đầu (Source) | Điểm đích (Destination) | Mức điện áp | Chức năng & Yêu cầu kỹ thuật |
| :--- | :--- | :--- | :---: | :--- |
| **Nguồn IMU** | ESP32 chân 3V3 & GND | WCMCU chân VCC & GND | 3.3 V / 0 V | Cấp nguồn trực tiếp 3.3V từ LDO 3.3V trên board DevKit. Tuyệt đối không nối vào 5V. |
| **Bus I2C chính** | ESP32 GPIO21 & GPIO22 | WCMCU chân SDA & SCL | 3.3 V | Tần số 400 kHz; dùng trở kéo 10 kΩ onboard WCMCU; không dùng BSS138. |
| **Cấu hình IMU** | ESP32 3V3 & GND | WCMCU NCS (3V3), AD0/FSY (GND) | 3.3 V / 0 V | NCS=3V3 chọn I2C; AD0=GND chọn địa chỉ 0x68; FSY=GND chống nhiễu. |
| **Chân phụ IMU** | WCMCU chân INT, ACL, ADA | Không nối (Để hở chân - NC) | — | Chưa dùng ngắt; cấm nối ACL/ADA vào SCL/SDA chính tránh chập bus. |
| **Nút Chuột Trái** | ESP32 GPIO25 | Nút SW_LEFT -> GND | 3.3 V / 0 V | Cấu hình INPUT_PULLUP Active-Low. Đấu 2 chân đối diện của nút 4 chân. |
| **Nút Chuột Phải** | ESP32 GPIO26 | Nút SW_RIGHT -> GND | 3.3 V / 0 V | Cấu hình INPUT_PULLUP Active-Low. Đấu 2 chân đối diện của nút 4 chân. |
| **Nút Mode/Clutch** | ESP32 GPIO27 | Nút SW_MODE -> GND | 3.3 V / 0 V | Cấu hình INPUT_PULLUP Active-Low. GPIO27 là RTC GPIO hỗ trợ đánh thức. |
| **LED Chỉ Thị** | ESP32 GPIO32 | Trở R1 (1.0k) -> Anode LED -> GND | 3.3 V | Dòng hạn chế ~1.2 mA bảo vệ ngõ ra vi điều khiển. LED 3mm xanh lá. |
| **Phân Áp Đo Pin** | V_SYS (sau công tắc) | R2 100k -> BAT_SENSE -> R3 100k -> GND | 1.5–2.1 V | Đưa vào GPIO34 (ADC1_CH6) kèm tụ C1 100nF; chưa kích hoạt firmware. |
| **Chuỗi Nguồn 5V** | Pin (Cell+/- -> B+/B-) -> TP4056; OUT+ qua SW1; OUT- -> System GND | MT3608 (5.0V) -> VIN/GND ESP32 | 5.0 V | OUT- → system GND → MT3608 VIN-. Chỉnh MT3608 5.0V trước khi cắm ESP32; tụ C2 10µF sát VIN. |

*Chi tiết bàn giao*: Toàn bộ 50 dòng kết nối chân-đến-chân, phân định nhãn in trên module vs GPIO ESP32 và các rào cản cấm nối được mô tả đầy đủ trong tài liệu [`deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md`](deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md).

---

## 4. TÓM TẮT LÝ THUYẾT CỐT LÕI (BẢNG TRÍCH YẾU)

Nhóm tổng hợp ngắn gọn các nền tảng lý thuyết trọng tâm điều khiển phần cứng hệ thống nhúng trong Bảng 4.1:

| Chủ đề lý thuyết | Đặc tính kỹ thuật cốt lõi | Cấu hình / Thông số dự án | Ý nghĩa & Tác động phần cứng |
| :--- | :--- | :--- | :--- |
| **Giao thức I2C & Repeated START** | Giao tiếp 2 dây cực máng hở (Open-Drain). Cần trở kéo pull-up tạo mức HIGH và logic Wired-AND. Tránh bus contention khi nhiều thiết bị chia sẻ bus. | Tần số: 400 kHz (Fast-Mode).<br>Trở kéo: 10 kΩ onboard WCMCU.<br>Địa chỉ: 0x68 (AD0=0).<br>Ghi: 0xD0, Đọc: 0xD1. | Sử dụng Repeated START (Sr) đọc thanh ghi: giữ bus liên tục, chuyển từ Ghi địa chỉ sang Đọc dữ liệu mà không phát STOP, tránh xung đột bus. |
| **ICM-20948 & 4 User Bank Map** | Cảm biến chia không gian địa chỉ thành 4 Bank (mỗi Bank 128 byte) để vượt qua giới hạn địa chỉ 7-bit. Chuyển Bank qua thanh ghi REG_BANK_SEL (0x7F cố định cả 4 Bank). | `PWR_MGMT_1` (0x06 B0) = 0x01 (Auto-PLL, thoát Sleep).<br>`GYRO_CFG_1` (0x01 B2) = 0x1B (DLPF 51.2Hz, ±500°/s).<br>`ACCEL_CFG` (0x14 B2) = 0x1B (DLPF 50.4Hz, ±4g).<br>`SMPLRT_DIV` (0x00 B2) = 10 (ODR ≈ 102.27 Hz). | Cần gọi `imu_selectBank()` trước khi đọc/ghi thanh ghi khác Bank. 4 thanh ghi cốt lõi đã được kiểm chứng đọc lại (readback) thành công trên phần cứng thật. |
| **ADC SAR1 ESP32 & Đo Điện Áp Pin** | SAR ADC 12-bit (4096 mức mã, LSB = V_FSR / 4096). Khối ADC2 bị xung đột khi dùng Wi-Fi; khối ADC1 (GPIO32–39) hoàn toàn độc lập, an toàn khi chạy BLE/Wi-Fi. | Kênh: ADC1_CH6 (GPIO34, Input-only).<br>Cầu phân áp: 100k/100k (V_sense = 0.5*V_bat).<br>Khi pin 4.2V, V_sense = 2.1V nằm trong dải đo tuyến tính khi suy hao 11 dB. | Mạch đo pin tách biệt an toàn với nguồn 5V VIN. Chức năng đo pin hiện CHƯA KÍCH HOẠT TRONG FIRMWARE TUẦN 5 (chưa gọi analogRead trong loop chính). |
| **Phân tầng phần mềm & Assembly Xtensa** | Firmware viết bằng C/C++ trên Arduino/ESP-IDF, biên dịch bởi xtensa-esp32-elf-g++. CPU ESP32 là Xtensa Dual-core 32-bit LX6 (Tensilica, KHÔNG PHẢI ARM). | Trích disassembly từ firmware.elf:<br>`400d22f0: entry a1, 32`<br>`400d2302: movi a11, 104`<br>`400d2307: call8 TwoWire::beginTransmission` | Khẳng định kiến trúc: Dự án không code bằng Assembly thô. Hàm C/C++ được biên dịch thành tập lệnh Xtensa LX6 Windowed ABI; lệnh Wire tương ứng cụm lệnh MMIO. |

---


### 4.2. Chi tiết 2 loại thanh ghi điều khiển phần cứng (Mỗi bit làm nhiệm vụ gì)

#### 4.2.1. Loại 1 — Thanh ghi Digital Out và Digital In của ESP32 (Kiểm soát mức logic 0, 1)
Vi điều khiển ESP32 quản lý các chân ngoại vi số thông qua vùng thanh ghi Memory-Mapped I/O (MMIO) cấp thấp tại địa chỉ cơ sở `0x3FF44000`. Để đảm bảo độ trễ thấp nhất và tối ưu hóa thời gian thực, CPU Xtensa truy xuất trực tiếp các thanh ghi 32-bit sau:

| Tên thanh ghi | Địa chỉ MMIO | Chức năng & Phân tích từng bit | Ứng dụng trong hệ thống Air Mouse |
| :--- | :---: | :--- | :--- |
| **GPIO_OUT1_REG**<br>(Digital Out, GPIO32–39) | `0x3FF44010` | `GPIO_OUT_REG` (`0x3FF44004`) chỉ chứa GPIO0–31; các chân GPIO32–39 nằm ở `GPIO_OUT1_REG`, bit $j$ ứng với chân GPIO$(32+j)$.<br>• **Bit $i$ = 1**: Xuất mức HIGH (3.3V).<br>• **Bit $i$ = 0**: Xuất mức LOW (0V). | **Bit 0 của GPIO_OUT1_REG** điều khiển LED báo trạng thái (GPIO32). Thường dùng **GPIO_OUT1_W1TS_REG** (`0x3FF44014`) để bật và **GPIO_OUT1_W1TC_REG** (`0x3FF44018`) để tắt nguyên tử mà không cần Read-Modify-Write. |
| **GPIO_IN_REG**<br>(Digital In) | `0x3FF4403C` | Mỗi bit $i$ phản ánh giá trị logic thực tế đọc từ chân GPIO $i$.<br>• **Bit $i$ = 1**: Điện áp chân ở mức HIGH (3.3V).<br>• **Bit $i$ = 0**: Điện áp chân ở mức LOW (0V). | Đọc trạng thái 3 nút bấm (Active-Low):<br>• **Bit 25**: Nút Trái (thả=1, bấm=0).<br>• **Bit 26**: Nút Phải (thả=1, bấm=0).<br>• **Bit 27**: Nút Clutch (thả=1, bấm=0). |
| **GPIO_ENABLE_REG / GPIO_ENABLE1_REG**<br>(Hướng I/O) | `0x3FF44020` / `0x3FF4402C` | Cấu hình chiều truyền dữ liệu (Direction):<br>• **Bit $i$ = 1**: Chân GPIO $i$ làm Ngõ Ra (Output).<br>• **Bit $i$ = 0**: Chân GPIO $i$ làm Ngõ Vào (Input). | **GPIO_ENABLE1_REG bit 0 = 1** (GPIO32 – LED ngõ ra);<br>**GPIO_ENABLE_REG bits 25, 26, 27 = 0** (cấu hình các nút bấm ngõ vào kèm trở kéo lên nội pull-up). |

#### 4.2.2. Loại 2 — Mổ xẻ từng bit của các thanh ghi cấu hình cảm biến ICM-20948
Cảm biến ICM-20948 chia không gian địa chỉ thành 4 Bank (mỗi Bank 128 byte) để vượt qua giới hạn địa chỉ 7-bit. Nhóm mổ xẻ tường minh ý nghĩa từng bit của 4 thanh ghi vật lý cốt lõi đã được kiểm chứng đọc lại (readback) thành công trên phần cứng thật:

| Thanh ghi & Vị trí | Giá trị ghi | Bóc tách chi tiết từng bit (Bitfield Analysis) | Ý nghĩa trong hệ thống |
| :--- | :---: | :--- | :--- |
| **PWR_MGMT_1**<br>(Bank 0, 0x06) | `0x01`<br>(`00000001b`) | • **Bit 7 (`DEVICE_RESET` = 0)**: Không reset chip.<br>• **Bit 6 (`SLEEP` = 0)**: Đánh thức chip thoát khỏi chế độ ngủ.<br>• **Bit 5 (`LP_EN` = 0)**: Tắt chế độ tiết kiệm điện năng thấp.<br>• **Bit 3 (`TEMP_DIS` = 0)**: Kích hoạt cảm biến nhiệt độ.<br>• **Bits [2:0] (`CLKSEL` = 001)**: Chọn nguồn xung Auto-select PLL từ con quay trục tốt nhất (thay cho dao động RC 20MHz nội). | Bắt buộc ghi đầu tiên khi khởi động; chip chỉ hoạt động bình thường khi SLEEP=0 và dùng Auto-PLL. |
| **GYRO_CONFIG_1**<br>(Bank 2, 0x01) | `0x1B`<br>(`00011011b`) | • **Bits [5:3] (`GYRO_DLPFCFG` = 011)**: Chọn bộ lọc thông thấp số DLPF tần số cắt 51.2 Hz (NBW 73.3 Hz theo Table 16 datasheet DS-000189).<br>• **Bits [2:1] (`GYRO_FS_SEL` = 01)**: Chọn dải đo $\pm 500\,\text{dps}$ (Độ nhạy $65.5\,\text{LSB/dps}$).<br>• **Bit 0 (`GYRO_FCHOICE` = 1)**: Bật mạch lọc số DLPF. | Dải đo $\pm 500\,\text{dps}$ tối ưu chuyển động vẩy cổ tay; lọc DLPF 51.2 Hz triệt tiêu rung tay sinh lý tần số cao. |
| **ACCEL_CONFIG**<br>(Bank 2, 0x14) | `0x1B`<br>(`00011011b`) | • **Bits [5:3] (`ACCEL_DLPFCFG` = 011)**: Chọn bộ lọc số gia tốc kế DLPF tần số cắt 50.4 Hz (NBW 68.8 Hz theo Table 18 datasheet DS-000189).<br>• **Bits [2:1] (`ACCEL_FS_SEL` = 01)**: Chọn dải đo $\pm 4\,\text{g}$ (Độ nhạy $8192\,\text{LSB/g}$).<br>• **Bit 0 (`ACCEL_FCHOICE` = 1)**: Bật mạch lọc số DLPF. | Dải đo $\pm 4\,\text{g}$ vừa vặn đo vector trọng trường 1g và phát hiện gia tốc vung tay cử chỉ Flick mà không bị bão hòa. |
| **GYRO_SMPLRT_DIV** (Bank 2, 0x00) &<br>**ACCEL_SMPLRT_DIV** (Bank 2, 0x10-11) | `10` (thập phân)<br>(`0x0A`) | • **Bits [7:0] (`SMPLRT_DIV` = 10)**: Chia tần số lấy mẫu cơ sở.<br>Công thức ODR: $\text{ODR} = 1125\,\text{Hz} / (1 + \text{SMPLRT\_DIV}) = 1125 / 11 \approx 102.27\,\text{Hz}$. | Đồng bộ tốc độ sinh dữ liệu của phần cứng (102.27 Hz) với chu kỳ đọc 10 ms (100 Hz) của vòng lặp ESP32. |

### 4.3. Phân loại lệnh thư viện điều khiển bọt ngoại vi (Port/Board)
Nhóm phân định rành mạch giữa các lệnh thư viện tác động lên CẤU HÌNH (chạy 1 lần trong setup hoặc khi thay đổi chế độ) và các lệnh tác động lên THIẾT BỊ / RUNTIME (chạy lặp lại trong chu kỳ 10 ms):

| Ngoại vi / Module | Nhóm lệnh tác động lên CẤU HÌNH (Configuration APIs) | Nhóm lệnh tác động lên THIẾT BỊ / RUNTIME (Device & I/O APIs) | Cơ chế phần cứng bên dưới |
| :--- | :--- | :--- | :--- |
| **GPIO (Digital In / Out)** | • `pinMode(GPIO25/26/27, INPUT_PULLUP);`<br>• `pinMode(GPIO32, OUTPUT);` | • `digitalRead(GPIO25/26/27);` (Đọc nút bấm)<br>• `digitalWrite(GPIO32, HIGH/LOW);` (Bật/tắt LED) | Cấu hình ghi vào `GPIO_ENABLE_REG` / `GPIO_ENABLE1_REG` và `IO_MUX`; xuất LED ghi vào `GPIO_OUT1_REG` (GPIO32), đọc nút từ `GPIO_IN_REG` (GPIO25–27). |
| **Bus I2C & Cảm biến IMU** | • `Wire.begin(21, 22, 400000);`<br>• `Wire.setClock(400000);`<br>• `imu_selectBank(0/2);`<br>• `imu_writeReg(reg, val);` | • `Wire.beginTransmission(0x68);`<br>• `Wire.write(reg_addr);`<br>• `Wire.endTransmission(false);`<br>• `Wire.requestFrom(0x68, 12);`<br>• `Wire.read();` (Đọc dữ liệu thô 6 trục) | Khởi tạo điều khiển I2C Master controller; Đọc/ghi kích hoạt máy trạng thái phần cứng I2C (START, Byte, ACK, STOP). |
| **Bluetooth Low Energy (BLE HID)** | • `BleMouse bleMouse("AirMouse", "HCMUT", 100);`<br>• `bleMouse.begin();` | • `bleMouse.move(dx, dy, wheel, pan);`<br>• `bleMouse.click(MOUSE_LEFT/RIGHT);`<br>• `bleMouse.click(MOUSE_BACK/FORWARD);`<br>• `bleMouse.isConnected();` | Khởi tạo BLE GATT Server, HID Service và Advertising; Runtime gửi gói tin HID Report 5 byte qua GATT Characteristic. |
| **SAR ADC1 (Đo Pin)** | • `analogReadResolution(12);`<br>• `analogSetAttenuation(ADC_11db);` | • `uint16_t raw = analogRead(34);`<br>*(Chưa kích hoạt trong firmware Tuần 5)* | Cấu hình dải suy hao và thanh ghi điều khiển `SENS_SAR_START_FORCE_REG`; Runtime kích hoạt mạch SAR chuyển đổi 12-bit. |

---

## 5. CÔNG VIỆC ĐÃ HOÀN THÀNH & KẾT QUẢ THỰC NGHIỆM

Đến mốc Tuần 5, nhóm đã hoàn thành toàn diện các hạng mục chuẩn bị lý thuyết, kiến trúc, kiểm thử mô phỏng và đo kiểm Bring-up trên phần cứng thực tế:

| Mốc kiểm tra | Đối tượng & Hạng mục | Tiêu chí nghiệm thu | Kết quả thực nghiệm | Trạng thái minh bạch |
| :--- | :--- | :--- | :--- | :---: |
| **M1: Chip ID & Flash** | ESP32 DevKit qua esptool COM8 | Nhận dạng đúng CPU Xtensa, flash 4MB | ESP32-D0WD-V3 (rev v3.1), Flash 4MB DIO 40MHz | `BENCH PASS` |
| **M2: Quét I2C Bus** | WCMCU-20948 trực tiếp 3.3V | Phản hồi ACK tại đúng địa chỉ 0x68 | I2C device found at address 0x68 (100k & 400kHz) | `BENCH PASS` |
| **M3: Định danh WHO_AM_I** | Đọc thanh ghi 0x00 Bank 0 | Giá trị trả về chính xác 0xEA | 100/100 lần đọc WHO_AM_I thành công trong phép thử ngắn hạn | `BENCH PASS` |
| **M4: Readback Thanh Ghi** | Đọc lại 4 thanh ghi cấu hình | Khớp giá trị ghi: 0x01, 0x1B, 0x1B, 10 | PWR_MGMT_1=0x01, GYRO=0x1B, ACCEL=0x1B, DIV=10 | `READBACK PASS` |
| **M5: Đọc Burst 12-byte** | Đọc 12 byte dữ liệu thô Bank 0 | Dữ liệu 6 trục đầy đủ, Accel Z ~ +1g | Accel Z ~ +16200 LSB ≈ +1g (chương trình probe để dải mặc định ±2g = 16384 LSB/g; firmware chính dùng ±4g nên 1g ≈ 8192 LSB), Gyro tĩnh ~ 0 dps | `BENCH PASS` |
| **M6: Host Test Suite** | Test harness trên máy tính chủ | 10/10 test cases thuật toán logic PASS | Vượt qua toàn bộ 10/10 bài test tư thế & cử chỉ | `HOST PASS` |
| **M7: Biên dịch Firmware** | Mã nguồn firmware.ino PlatformIO | Biên dịch thành công 100%, đủ RAM/Flash | Build thành công; RAM 39.628 byte, Flash 1.158.973 byte | `BUILD PASS` |

*Chú thích trạng thái: BENCH PASS = BENCH_VERIFIED_ON_OWNED_MODULE; READBACK PASS = PHYSICAL_READBACK_CONFIRMED; HOST PASS = HOST_VERIFIED_LOGIC_TESTS; BUILD PASS = PLATFORMIO_COMPILE_VERIFIED.*

### 5.1. Bằng chứng thực nghiệm Hardware Bring-up trực tiếp 3.3V
Ngày 25/09/2026, nhóm thực hiện đo kiểm thực tế trên bàn thí nghiệm với vi điều khiển ESP32 Classic DevKit 38-pin kết nối trực tiếp module WCMCU-20948 ở mức 3,3 V qua cổng COM8:
* **Kết quả ổn định ngắn hạn**: Không ghi nhận NACK hoặc lỗi bus trong phép thử ngắn hạn đã ghi log (100/100 lần đọc WHO_AM_I thành công liên tục ở cả tần số 100 kHz và 400 kHz). Firmware chính đọc lại thanh ghi vật lý thành công cả 4 thanh ghi cấu hình cốt lõi.
* **Ghi nhận sự cố ban đầu và giải pháp**: Trong lần thử probe đầu tiên, cổng Serial báo lỗi I2C NACK (được lưu trung thực tại `raw_logs/probe_output.log`). Nguyên nhân kỹ thuật: Dây cắm jumper breadboard bị lỏng tiếp xúc cơ học và bị cắm lệch hàng chân phía bên phải của ESP32 DevKit 38-pin (nơi hai chân nạp UART TX0/RX0 nằm xen kẽ giữa GPIO22 và GPIO21). Sau khi kiểm tra lại sơ đồ chân, cắm chặt dây đúng vị trí chân vật lý, toàn bộ các phép đo sau đó đều thành công 100% (`raw_logs/probe_i2c_result.log` và `raw_logs/main_firmware_boot.log`).
* **Bảo vệ dữ liệu riêng tư**: Địa chỉ MAC được ẩn trong tài liệu sinh viên; raw evidence nội bộ được giữ nguyên để bảo toàn bằng chứng số.

#### Bảng đối chiếu tệp nhật ký thực nghiệm (Raw Logs) và mã băm SHA-256

| Tệp nhật ký thực nghiệm (Raw Log) | Dung lượng | Mã băm SHA-256 toàn vẹn dữ liệu |
| :--- | :---: | :--- |
| `raw_logs/esptool_chip_id.log` | 551 B | `fa5eb4951cdbf100cd917d9ce6a3b5388379ff89767a5500db665e1f36735a25` |
| `raw_logs/esptool_flash_id.log` | 604 B | `d142fd348fe31693de7ad022f397ec8ea69bf29f7a9e6ad0f15728f35fbb7fa7` |
| `raw_logs/probe_output.log` | 3271 B | `e2f5b4b2c009b0dda17671720d4840aff2854fa2b3bbed355caa1ff1e10c9b7f` |
| `raw_logs/probe_i2c_result.log` | 4197 B | `a069f551f77dde71034966df6779e697fff4256dd1bb284c90d555fcc35d4d4d` |
| `raw_logs/main_firmware_boot.log` | 2327 B | `b7703685e4b13540ed12d39b3c8b2fde8d237ab0b661bb991dbe003f575be612` |

---


### 5.2. Danh mục tính năng và kịch bản Demo hoạt động (Demo Topic & Capabilities)
Dựa trên kết quả đo kiểm trên phần cứng sở hữu và bộ test harness tự động (10/10 PASS), nhóm tổng hợp danh mục toàn bộ các tính năng đã sẵn sàng demo cùng ranh giới kiểm chứng thực tế:

| STT | Tính năng / Kịch bản Demo | Hành vi thiết bị & Thao tác người dùng | Cơ chế kỹ thuật / Phản hồi phần mềm | Trạng thái kiểm chứng |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **Rê chuột không gian (Air Mouse)** | Người dùng cầm thiết bị xoay cổ tay tự nhiên theo phương ngang / dọc. | Thuật toán Rate-Control: $dX = \text{round}(K_x \cdot \omega_{\text{yaw}})$, $dY = \text{round}(-K_y \cdot \omega_{\text{pitch}})$. Vùng chết 0.8–1.4 dps khử rung tay. | **BENCH & HOST PASS**<br>(Vòng lặp 100 Hz ổn định) |
| 2 | **Chống trôi khi đặt yên (Stationary Lock)** | Để chuột nằm yên trên bàn hoặc giữ tay đứng yên trong 200 ms. | Bộ nhận diện tĩnh tự động khóa $dX=dY=0$ và cập nhật trừ bias tĩnh tự động (Auto-zero). | **HOST PASS**<br>(Test 3 PASS) |
| 3 | **Nhấp phím chuột (Click Left / Right)** | Bấm phím SW_LEFT (GPIO25) hoặc SW_RIGHT (GPIO26). | Mức LOW kích hoạt gửi bitmask nút bấm tương ứng trong Byte 0 của bản tin HID chuột. | **BENCH PASS**<br>(Logic Active-Low) |
| 4 | **Ly hợp Clutch (Đóng băng trỏ)** | Nhấn giữ nút SW_MODE (GPIO27) để nhấc tay chuyển vị trí. | Con trỏ chuột bị khóa cứng $dX=dY=0$, cho phép người dùng thoải mái đổi tư thế tay mà không làm dịch chuyển con trỏ. | **HOST PASS**<br>(Test 5 PASS) |
| 5 | **Cử chỉ Vẫy tay trái (Flick Left)** | Giữ nút Clutch + vung tay nhanh sang trái rồi phanh hồi ngược. | Máy trạng thái 2 pha nhận diện gia tốc vung > 1.15g và hãm > 0.35g $\to$ Phát sự kiện MOUSE_BACK (lùi trang/slide). | **HOST PASS**<br>(Test 7 & 10 PASS) |
| 6 | **Cử chỉ Vẫy tay phải (Flick Right)** | Giữ nút Clutch + vung tay nhanh sang phải rồi phanh hồi ngược. | Máy trạng thái 2 pha nhận diện gia tốc bên phải $\to$ Phát sự kiện MOUSE_FORWARD (tiến trang/slide). | **HOST PASS**<br>(Test 7 & 10 PASS) |
| 7 | **Căn lại tâm tham chiếu (Recenter)** | Thả nút Clutch mà không thực hiện thao tác vẫy tay nào. | Hàm `motion_recenter()` chụp lại vector trọng lực hiện tại làm mốc thẳng đứng tham chiếu mới, chống lệch tư thế. | **HOST PASS**<br>(Test 5 PASS) |
| 8 | **Phát sóng BLE HID không dây** | Cấp nguồn pin/USB cho mạch. | ESP32 khởi động stack BLE và phát sóng quảng bá tên thiết bị "AirMouse-ESP32". | **BENCH PASS**<br>(Ghi nhận trong boot log) |
| 9 | **Điều khiển thực tế trên máy tính PC** | Ghép nối Bluetooth với laptop để di chuột và duyệt slide thực tế. | Đo độ trễ gói tin, độ mượt rê chuột và kiểm tra rớt gói tin trên hệ điều hành Windows/macOS. | **NOT_TESTED**<br>(Chưa thử nghiệm ghép nối PC) |

---

## 6. CÔNG VIỆC CHƯA HOÀN THÀNH, HẠN CHẾ & VẤN ĐỀ TỒN TẠI

Nhóm thẳng thắn nhìn nhận các hạn chế và ranh giới kỹ thuật hiện tại của dự án tại mốc giữa kỳ Tuần 5:
1. **Kết nối BLE HID với máy tính ở trạng thái NOT_TESTED**: Mã nguồn firmware BLE HID đã biên dịch thành công và phát tín hiệu quảng bá `AirMouse-ESP32`, nhưng nhóm CHƯA thực hiện ghép nối thực tế với máy tính PC để đo độ trễ và kiểm tra độ ổn định chuột trên hệ điều hành. Trạng thái kết nối máy tính: `NOT_TESTED`. Tuyệt đối không tuyên bố con trỏ chuột đã hoạt động thực tế trên PC.
2. **Ranh giới điện áp 3.3V trực tiếp và datasheet raw IC**: Hoạt động thành công trên đúng module WCMCU-20948 và ESP32 mà nhóm đang sở hữu (`BENCH_VERIFIED_ON_OWNED_MODULE`). Tuy nhiên, datasheet gốc của IC ICM-20948 (TDK DS-000189) quy định dải điện áp I/O $V_{\text{DDIO}}$ tối đa là $1.95\,\text{V}$. Việc cấp 3.3V trực tiếp là độ lệch kỹ thuật trên module breakout thương phẩm cụ thể của nhóm và có rủi ro tiềm ẩn về độ bền lâu dài chưa được kiểm chứng qua các bài stress-test. Nhóm không suy rộng thành mức an toàn tối thượng hay áp dụng cho mọi điều kiện biên.
3. **Hồ sơ thiết kế KiCad ở trạng thái chờ đồng bộ**: Tuân thủ nghiêm ngặt quy tắc không can thiệp thủ công file cú pháp S-expression thô của KiCad khi chưa cập nhật qua KiCad MCP Server. Do đó, hồ sơ KiCad hiện tại vẫn còn khối BSS138 và AMS1117-1.8V (trạng thái: `KICAD_SYNC_STATUS: STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE`), sẽ được đồng bộ chính thức ở giai đoạn tiếp theo.
4. **Chức năng đo điện áp pin chưa kích hoạt trong firmware**: Mạch phân áp 100k/100k đã thiết kế phần cứng hoàn chỉnh, nhưng firmware Tuần 5 chưa gọi hàm `analogRead(34)` trong vòng lặp chính để ưu tiên tối ưu hóa bus I2C và pipeline 100 Hz.
5. **Khối từ kế AK09916 chưa tham gia thuật toán dung hợp**: Thuật toán V1 hiện triển khai dung hợp 6 trục (Gyro + Accel). Chưa tích hợp từ kế AK09916 nên trục Yaw chưa có mốc hướng tuyệt đối, dựa vào tích phân con quay. Dù đã có dead-zone triệt tiêu trôi tĩnh, việc xoay liên tục trong thời gian dài vẫn tích lũy sai số trôi nhẹ.

---

## 7. KẾ HOẠCH TRIỂN KHAI GIAI ĐOẠN TIẾP THEO

Kế hoạch phân kỳ thực hiện giai đoạn 2 tập trung vào kết nối không dây, hoàn thiện bo mạch in và tinh chỉnh trải nghiệm người dùng:

| Hạng mục công việc | Kết quả mong đợi | Tiêu chuẩn hoàn thành | Mức ưu tiên |
| :--- | :--- | :--- | :---: |
| **Kiểm thử kết nối BLE HID với PC** | Máy tính nhận diện 'AirMouse-ESP32', nhận đủ báo cáo 5-byte 100 Hz. | Độ trễ < 20 ms, không rớt gói tin trong 10 phút rê chuột liên tục. | **P0 (Bắt buộc)** |
| **Đồng bộ KiCad qua MCP Server** | Cập nhật schematic và layout PCB loại bỏ BSS138 và AMS1117-1.8V. | Schematic và layout KiCad vượt 100% kiểm tra ERC/DRC theo baseline V4.0.0. | **P0 (Bắt buộc)** |
| **Gia công & Hàn bo Carrier Board** | Chế tạo PCB 1 lớp hoàn chỉnh, hàn linh kiện THT và gắn pin LiPo. | Nguồn 5V và 3.3V ổn định, không chập cháy, test points đo chuẩn. | **P1 (Quan trọng)** |
| **Tinh chỉnh thông số con trỏ tay** | Con trỏ di chuyển mượt mà; thao tác bấm click không làm lệch trỏ. | Thử nghiệm thực tế trên người dùng; tối ưu Gain K và vùng chết dead-zone. | **P1 (Quan trọng)** |
| **Kích hoạt đo điện áp pin trên ADC** | Đọc điện áp pin LiPo qua GPIO34 (ADC1_CH6), phát cảnh báo pin yếu. | Hiệu chuẩn qua esp_adc_cal, sai số đo điện áp < 0.05V. | **P2 (Mở rộng)** |
| **Đo kiểm năng lượng & Độ bền 3.3V** | Đo dòng tiêu thụ ở các chế độ Active/Sleep; theo dõi nhiệt độ IMU. | Thời lượng pin > 8 giờ hoạt động; cảm biến không quá nhiệt ở 3.3V. | **P2 (Hoàn thiện)** |

---

## 8. KẾT LUẬN & XÁC NHẬN BÁO CÁO

Đến mốc đánh giá giữa kỳ ở Tuần 5, nhóm đã hoàn thành toàn diện các nhiệm vụ nền tảng: xác lập kiến trúc phần cứng V4.0.0 trực tiếp 3,3 V, tối ưu hóa bảng dự toán BOM V2.0.0 gồm 23 linh kiện (153.000 VNĐ), xây dựng driver I2C cho ICM-20948, hoàn thiện thuật toán tư thế 6 trục và xử lý con trỏ chuột, đạt 10/10 bài test logic trên máy tính chủ, và đặc biệt là hoàn thành bước Hardware Bring-up ngoại vi cảm biến thực tế: 100/100 lần đọc WHO_AM_I thành công trong phép thử ngắn hạn. Firmware chính đọc lại thanh ghi vật lý thành công cả 4 thanh ghi cấu hình. Báo cáo phân định minh bạch giữa kết quả đo kiểm trên bàn thí nghiệm và các hạng mục còn ở trạng thái chờ thử nghiệm (kết nối máy tính `NOT_TESTED` và hồ sơ KiCad `STALE`).

### TÀI LIỆU THAM KHẢO CHÍNH:
[1] TDK InvenSense, *ICM-20948 Datasheet and Register Map*, Doc DS-000189, Rev 1.6, 2024.  
[2] NXP Semiconductors, *I2C-bus Specification and User Manual*, UM10204, Rev 7.0, 2021.  
[3] Espressif Systems, *ESP32 Technical Reference Manual v5.1 & Hardware Design Guidelines v3.4*.  
[4] Bluetooth SIG, *Human Interface Device (HID) Profile Specification*, Version 1.1.1.  

---

| GIẢNG VIÊN HƯỚNG DẪN | ĐẠI DIỆN NHÓM SINH VIÊN |
| :---: | :---: |
| *(Ký và ghi rõ họ tên)* | *(Ký và ghi rõ họ tên)* |
