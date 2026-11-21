---
title: BÁO CÁO CHI TIẾT KIẾN THỨC — CHUỘT BAY AIR MOUSE BLE HID
subtitle: Tài liệu đi kèm Báo cáo giữa kỳ Tuần 5 — trả lời chuyên sâu theo kiểu câu hỏi của giảng viên
course: Môn Hệ thống nhúng — GVHD: TS. Nguyễn Mạnh Hùng
date: 03/10/2026 (số liệu đo thực nghiệm ngày 01/10/2026)
---

# 0. CÁCH ĐỌC TÀI LIỆU VÀ KIỂU CÂU HỎI CỦA THẦY

Tài liệu này giữ nguyên khung của báo cáo giữa kỳ (mục 1–7) nhưng đi sâu tới từng bit, từng công thức và từng con số đo. Nội dung được xây dựng từ bản ghi các nhóm báo cáo trước (nhóm STM32 điều khiển tốc độ động cơ, nhóm SPI/servo). Qua đó, thầy hỏi theo 5 kiểu lặp lại, cộng thêm kiểu thứ 6 (đọc hiểu code) vì thầy ở bản ghi còn hỏi "câu lệnh viết như thế nào":

| Kiểu | Thầy hỏi nhóm trước | Câu tương ứng thầy có thể hỏi nhóm mình | Mục trả lời |
| --- | --- | --- | --- |
| 1. "X trong ứng dụng này dùng để làm gì?" | "ADC dùng để làm gì?" → đọc biến trở để đặt RPM, **không** dùng để đọc encoder | "ADC trong dự án dùng để làm gì? Cảm biến ICM đọc bằng ADC à?" | 2, 4 |
| 2. Chuỗi đại lượng → con số | "Biến trở 0–5 V thì tốc độ bao nhiêu? Tại sao em chắc là 300?" | "Xoay tay 30 °/s thì con trỏ đi bao nhiêu? Tại sao gain là 2.2?" | 1, 9 |
| 3. Cấu hình tới bit | "Timer cấu hình bằng bit nào? Mode mấy? BR[2:0] có mấy mức?" | "0x1B là bit nào? Chọn bank bằng bit nào? 400 kHz tạo ra thế nào?" | 5, 6, 7 |
| 4. Quan hệ số học & giới hạn | "Duty so với ARR hay 0xFFFF? PID ra lớn hơn ARR thì sao?" | "Ghi DIV = 255 được không? dX vượt 127 thì sao? 12-bit là bao nhiêu mức?" | 4, 6, 9 |
| 5. Đào sâu đến khi hết hiểu | "Tốc độ ngõ ra là gì? Đơn vị ms có phải độ rộng xung không?" | "LSB là gì? Pull-up ở đâu? Ai quyết định 100 Hz?" | mọi mục |
| 6. Đọc hiểu code | "Câu lệnh viết như thế nào? Dòng này làm gì?" | "Hàm `imu_readData` ghép hai byte thế nào? Vì sao dịch trái 8 bit? Vì sao kẹp ±127?" | 12 |

**Quy ước trạng thái** (ghi trung thực, không nói quá):

| Nhãn | Ý nghĩa |
| --- | --- |
| BENCH_VERIFIED | Đã đo trên đúng board ESP32 + WCMCU-20948 của nhóm, có log trong `raw_logs/` |
| HOST_TESTED | Thuật toán chạy bộ test trên máy tính (10/10 PASS theo baseline 26/09) |
| NOT_TESTED | Có thiết kế/code nhưng chưa thử trên phần cứng |
| NOT_IMPLEMENTED | Mới là thiết kế, firmware chưa có |

> [!NOTE] Phần cứng lúc đo ngày 01/10/2026
> Breadboard chỉ có ESP32 DevKit (ESP32-D0WD-V3, cổng COM3) và module WCMCU-20948 nối trực tiếp 3.3 V. Chưa lắp nút bấm, LED, cầu chia áp đo pin, TP4056 và MT3608. Vì vậy số liệu đo thật chỉ có ở phần I2C/IMU/vòng lặp; các phần còn lại là thiết kế + phép tính.

# 1. MỤC TIÊU ĐỀ TÀI & NGUYÊN LÝ ĐIỀU KHIỂN

## 1.1. Bản chất: chuột điều khiển theo vận tốc xoay (relative rate-control)

Con trỏ **không** đi theo vị trí tuyệt đối của tay. Mỗi 10 ms, ESP32 đọc **vận tốc góc** ω (°/s) của cổ tay và gửi cho máy tính một **độ dời tương đối** dX, dY. Tay đứng yên (ω = 0) thì dX = dY = 0 và con trỏ đứng yên. Đây cũng là cách chuột quang hoạt động: gửi độ dời, không gửi tọa độ.

## 1.2. Chuỗi đại lượng từ cổ tay tới con trỏ

| Bước | Đại lượng | Nơi xử lý | Ví dụ số (xoay ngang 30 °/s) |
| --- | --- | --- | --- |
| 1 | Vận tốc góc thật ω | Cơ khí MEMS trong ICM-20948 | 30 °/s |
| 2 | Số 16-bit bù hai (LSB) | **ADC 16-bit bên trong ICM-20948** | 30 × 65.5 = 1965 LSB (+ bias) |
| 3 | Đọc qua I2C (2 byte, big-endian) | ESP32 `imu_readBurst()` | 0x07AD |
| 4 | Đổi đơn vị: LSB ÷ 65.5 | `imu_readData()` | 30.0 °/s |
| 5 | Trừ bias (sai số điểm 0) | `motion_process()` | 30.0 − b |
| 6 | Vùng chết 0.8–1.4 °/s | `apply_deadzone()` | 30 − 0.8 = 29.2 |
| 7 | Chiếu lên trục ngang/dọc theo tư thế | `motion_process()` bước 9 | 29.2 |
| 8 | Nhân gain 2.2, làm tròn | `roundf(2.2 × ω)` | 64 |
| 9 | Kẹp vào int8 [−127, 127] | `clamp_i8()` | dX = +64 |
| 10 | Gửi gói HID 5 byte qua BLE | `bleMouse.move()` | 64 count / 10 ms = 6 400 count/s |

**Hai giới hạn phải thuộc** (thầy rất hay hỏi "lớn hơn max thì sao"):
- **Dưới ngưỡng:** |ω| < 0.8 °/s thì dX = 0. Ví dụ ω = 1.0 °/s cho kết quả 2.2 × (0.2 × 0.33) = 0.15, làm tròn thành 0; ω = 2 °/s cho 2.2 × 1.2 = 2.64, làm tròn thành 3.
- **Bão hòa:** dX tối đa là 127 (1 byte có dấu của gói HID). 2.2 × (ω − 0.8) = 127 khi ω ≈ 58.5 °/s. Xoay nhanh hơn 58.5 °/s thì con trỏ không nhanh thêm nữa (12 700 count/s). Đây là "bão hòa đầu ra", giống câu hỏi PID vượt ARR ở nhóm STM32: firmware **phải kẹp** giá trị, vì nếu không, ép kiểu int32 → int8 sẽ tràn và đổi dấu (ví dụ 200 thành −56, con trỏ chạy ngược).

> [!HOI] Thầy có thể hỏi: "Xoay 30 độ/giây thì con trỏ đi bao nhiêu? Tại sao em chắc?"
> Trả lời ngắn: firmware gửi dX = round(2.2 × (30 − 0.8)) = 64 count mỗi 10 ms. Nếu thầy đào sâu: "count" là đơn vị của HID (mickey), không phải pixel. Windows còn áp pointer acceleration nên số pixel thật phụ thuộc cài đặt máy. Gain 2.2 là **giá trị ban đầu, chưa tinh chỉnh trên người dùng**; nhóm không khẳng định con số pixel. Phần chắc chắn và kiểm chứng được là công thức trong code và dX gửi đi (HOST_TESTED).

## 1.3. Vì sao không tích phân kép gia tốc để lấy vị trí

Nếu gia tốc kế lệch một offset b, vị trí tính ra sai lệch ½·b·t². Offset đo thật trên board của nhóm: |A| = 0.9884 g, tức lệch 11.6 mg (mục 11). Với b = 11.6 mg = 0.114 m/s²:
- sau 1 s: 0.5 × 0.114 × 1² = **5.7 cm**;
- sau 10 s: **5.7 m**.

Sai số tăng theo bình phương thời gian, nên nhóm chọn rate-control (dùng trực tiếp ω). Accelerometer chỉ dùng để biết hướng trọng lực (tư thế) và phát hiện cử chỉ Flick.

## 1.4. Chế độ Clutch và cử chỉ

Nút Mode/Clutch (GPIO27) nhấn giữ thì khóa con trỏ (dX = dY = 0) và bật nhận cử chỉ. Lắc nhanh sang trái rồi hồi về thì gửi `MOUSE_BACK`, sang phải thì gửi `MOUSE_FORWARD`. Thả nút mà không có cử chỉ thì lấy lại mốc tư thế (recenter). Trạng thái: HOST_TESTED; nút chưa lắp trên breadboard nên phần cứng NOT_TESTED.

# 2. CÁC KHỐI PHẦN CỨNG & VAI TRÒ TỪNG NGOẠI VI

## 2.1. Ngoại vi nào được dùng và dùng để làm gì trong ứng dụng này

| Ngoại vi ESP32 | Dùng để làm gì **trong Air Mouse** | Vì sao chọn | Trạng thái |
| --- | --- | --- | --- |
| I2C0 (Master, 400 kHz) | Đọc 12 byte gyro + accel của ICM-20948 mỗi 10 ms; ghi thanh ghi cấu hình lúc khởi động | Chỉ 2 dây, module có sẵn chế độ I2C; tốc độ đủ (chiếm 4.4 % thời gian, mục 5.5) | BENCH_VERIFIED |
| GPIO input (GPIO25, 26, 27) | Đọc 3 nút: trái, phải, clutch (active-low, pull-up nội) | Không phải chân strapping/flash, có pull-up nội | NOT_TESTED (chưa lắp nút) |
| GPIO output (GPIO32) | Bật/tắt LED trạng thái | Không phải strapping; GPIO34–39 không xuất được | NOT_TESTED (chưa lắp LED) |
| SAR ADC1 kênh 6 (GPIO34) | **Chỉ để đo điện áp pin** qua cầu chia 100k/100k | ADC1 độc lập với Wi-Fi; GPIO34 là chân chỉ-vào, hợp để đo | NOT_IMPLEMENTED |
| UART0 (115200 baud) | In log chẩn đoán qua cổng USB (CP210x) | Có sẵn trên DevKit | BENCH_VERIFIED |
| Bluetooth LE | Gửi gói chuột HID 5 byte tới máy tính | Máy tính nhận là chuột Bluetooth, không cần driver | Code chạy, ghép nối NOT_TESTED |
| esp_timer (`micros()`) | Nhịp vòng lặp 10 ms, tính dt cho bộ lọc | Độ phân giải 1 µs, không tốn timer phần cứng | BENCH_VERIFIED |

## 2.2. Ngoại vi **không** dùng và lý do (thầy hay hỏi ngược)

| Không dùng | Lý do |
| --- | --- |
| ADC để đọc cảm biến chuyển động | Tín hiệu đã được **số hóa bên trong ICM-20948** và truyền dạng số qua I2C. Giống nhóm STM32: encoder đọc bằng timer, không bằng ADC |
| SPI | ICM hỗ trợ SPI 7 MHz nhưng I2C 400 kHz đã đủ; SPI tốn thêm 2 dây. Chân NCS nối 3.3 V để khóa chế độ I2C |
| PWM (LEDC) | LED chỉ cần bật/tắt/nhấp nháy; không cần điều chỉnh độ sáng |
| ADC2 | Driver Wi-Fi chiếm ADC2 khi Wi-Fi hoạt động; dùng ADC1 thì không phụ thuộc cấu hình vô tuyến |
| Chân INT của ICM (ngắt dữ liệu sẵn sàng) | V1 dùng polling đều 10 ms, đơn giản và đủ; INT để dành cho bản sau |
| Từ kế AK09916 | Chưa dung hợp 9 trục; yaw hiện chỉ là tương đối |

> [!HOI] Thầy có thể hỏi: "Trong ứng dụng này ADC dùng để làm gì?"
> Trả lời ngắn: ADC1 của ESP32 chỉ dùng để đo điện áp pin (GPIO34, qua cầu chia 1:2), và phần firmware này **chưa làm**. Dữ liệu chuyển động không đi qua ADC của ESP32: ADC nằm **bên trong** ICM-20948, ESP32 nhận số 16-bit qua I2C. Nếu thầy hỏi tiếp "mạch sạc có ADC không": không; TP4056/DW01A/MT3608 dùng bộ so sánh + điện áp chuẩn (mục 4.1).

# 3. NỐI DÂY & CÁC RÀNG BUỘC ĐIỆN

## 3.1. Bảng nối chính (đầy đủ 50 dòng ở `BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md`)

| Tín hiệu | ESP32 | WCMCU-20948 / linh kiện | Ghi chú |
| --- | --- | --- | --- |
| Nguồn cảm biến | 3V3 | VCC | LDO 3.3 V **trên board DevKit** (không phải trong chip ESP32) |
| Mass | GND | GND | Chung mass hệ thống (gốc tại OUT− của TP4056) |
| I2C data | GPIO21 | SDA | Trở kéo 10 kΩ có sẵn trên module |
| I2C clock | GPIO22 | SCL | 400 kHz |
| Chọn giao tiếp | 3V3 | NCS | NCS = 1 thì tắt SPI, dùng I2C |
| Chọn địa chỉ | GND | AD0 | AD0 = 0 cho địa chỉ 0x68 |
| Đồng bộ khung | GND | FSY | Không dùng |
| Nút trái / phải / clutch | GPIO25 / 26 / 27 | Nút → GND | INPUT_PULLUP, nhấn = 0 |
| LED | GPIO32 | 1 kΩ → LED → GND | Mức 1 thì sáng |
| Đo pin | GPIO34 | Điểm giữa 100k/100k | Từ V_SYS (sau công tắc) |

## 3.2. Các ràng buộc phải giải thích được

- **Trở kéo I2C**: bus I2C là open-drain. Thiết bị chỉ kéo xuống 0; mức 1 do trở kéo tạo ra. Module có sẵn 2 trở 10 kΩ lên VCC. Thời gian lên (30 % → 70 % VDD) ≈ 0.8473·R·C. Với tụ bus ước tính 50 pF: 0.8473 × 10 kΩ × 50 pF ≈ 0.42 µs, **lớn hơn** giới hạn 300 ns của chuẩn Fast-mode. Thực tế bus vẫn chạy 0 lỗi trên 2 000 lần đọc (mục 5.5) vì dây ngắn trên breadboard. Nhưng đây là lý do nên giảm trở kéo xuống khoảng 4.7 kΩ nếu làm PCB có dây dài hơn. Tụ 50 pF là ƯỚC TÍNH, chưa đo bằng máy hiện sóng.
- **Không nối ACL/ADA** của module vào bus chính: đó là bus I2C phụ mà ICM làm master để đọc cảm biến ngoài.
- **Chân cấm/cẩn thận của ESP32**: GPIO6–11 nối flash SPI (cấm dùng); GPIO0, 2, 5, 12, 15 là strapping (ảnh hưởng lúc boot); GPIO34–39 chỉ vào, không có pull-up nội, không xuất được.
- **TP4056: tách B− và OUT−**. Cực âm cell chỉ vào B− (mạng `GND_BAT_CELL`); mass hệ thống lấy từ OUT−. Giữa hai chân là MOSFET bảo vệ FS8205A, do DW01A điều khiển. Nối tắt B− với GND bên ngoài sẽ vô hiệu hóa bảo vệ quá xả và ngắn mạch.

# 4. CHƯƠNG ADC — CÁC BỘ CHUYỂN ĐỔI TƯƠNG TỰ–SỐ TRONG HỆ THỐNG

## 4.1. Hệ thống có những ADC nào? (câu bẫy)

| Khối | Có ADC? | Chuyển đổi cái gì | Kết quả đi đâu |
| --- | --- | --- | --- |
| ICM-20948: con quay 3 trục | **Có**, 16-bit (DS-000189 §3.1 "ADC Word Length 16 bits") | Tín hiệu điện dung của khối MEMS → số | Thanh ghi GYRO_xOUT (Bank 0, 0x33–0x38) |
| ICM-20948: gia tốc kế 3 trục | **Có**, 16-bit (§3.2) | Như trên | ACCEL_xOUT (0x2D–0x32) |
| ICM-20948: cảm biến nhiệt | **Có** | Nhiệt độ die → số | TEMP_OUT (0x39–0x3A) |
| Từ kế AK09916 (trong ICM) | Có, 16-bit | Từ trường | Chưa dùng |
| ESP32 SAR ADC1 | **Có**, 12-bit | Điện áp pin đã chia đôi | Dự kiến: `analogReadMilliVolts(34)` |
| TP4056 (sạc) | **Không** | Dùng khuếch đại sai số + điện áp chuẩn để giữ 4.2 V và giới hạn dòng | Chân CHRG/STDBY (số 0/1) |
| DW01A (bảo vệ pin) | **Không** | Bộ so sánh điện áp cell với các ngưỡng cố định | Bật/tắt MOSFET FS8205A |
| MT3608 (boost 5 V) | **Không** | So chân FB với chuẩn 0.6 V để chỉnh độ rộng xung | Tự điều áp |

**Ý chính:** "đo điện áp" không có nghĩa là "có ADC". Mạch sạc, bảo vệ và boost đo bằng **bộ so sánh analog** với điện áp chuẩn nội và phản ứng liên tục, không tạo ra con số. Số liệu từ datasheet:

| IC | Thông số (datasheet) | Cách "đo" |
| --- | --- | --- |
| TP4056 | Điện áp nạp cuối (float) 4.137–4.2–4.263 V; ngưỡng trickle 2.9 V (2.8–3.0 V), dòng trickle 130 mA khi R_PROG = 1.2 kΩ; I_BAT = 1200 / R_PROG (R_PROG = 1.2 kΩ cho 1 A); kết thúc khi dòng còn C/10 | Vòng hồi tiếp dòng/áp hằng (CC/CV) tuyến tính |
| DW01A | Quá nạp V_OCP = 4.30 ± 0.05 V (nhả 4.10 V); quá xả V_ODP = 2.40 ± 0.10 V (nhả 3.0 V); quá dòng V_OI1 = 150 ± 30 mV đo trên MOSFET | Bộ so sánh + trễ thời gian nội |
| MT3608 | Chuẩn FB = 0.588–0.600–0.612 V; tần số đóng cắt cố định 1.2 MHz; Vout = 0.6 × (1 + R1/R2) | Khuếch đại sai số điều chỉnh PWM |

Với Vout = 5.0 V: R1/R2 = 5.0 / 0.6 − 1 = 7.33. Biến trở trên module MT3608 chính là R1 trong công thức, nên **phải chỉnh bằng đồng hồ về 5.0 V trước khi cắm ESP32**.

> [!HOI] Thầy có thể hỏi: "Mạch sạc đo điện áp pin bằng ADC phải không? Vậy ESP32 cần đo pin làm gì?"
> Trả lời ngắn: không. TP4056 và DW01A dùng bộ so sánh với điện áp chuẩn để tự quyết định sạc/ngắt, không xuất số ra ngoài. ESP32 cần ADC riêng để **biết** pin còn bao nhiêu và báo cho người dùng (LED hoặc BLE Battery Service), việc mà mạch sạc không làm.

## 4.2. ADC bên trong ICM-20948

### 4.2.1. Đường đi của tín hiệu

```
Khối MEMS (điện dung thay đổi khi xoay/gia tốc)
   -> mạch đọc điện dung + khuếch đại
   -> ADC 16-bit
   -> bộ lọc thông thấp số DLPF (GYRO_DLPFCFG / ACCEL_DLPFCFG)
   -> chia tần số lấy mẫu: ODR = 1125 Hz / (1 + SMPLRT_DIV)
   -> thanh ghi dữ liệu 16-bit, byte cao trước (big-endian)
   -> I2C -> ESP32
```

ESP32 **chỉ đọc số đã chuyển đổi**; toàn bộ phần analog nằm trong ICM. Đây là điểm tương tự encoder AB của nhóm STM32: tín hiệu cảm biến tới MCU ở dạng số, không qua ADC của MCU.

### 4.2.2. Độ phân giải: 1 LSB bằng bao nhiêu?

Số 16-bit bù hai có dải −32 768 … +32 767 (65 536 mức). Full-scale (FS) quyết định 1 LSB ứng với bao nhiêu đơn vị vật lý:

| Cấu hình | Độ nhạy (datasheet) | 1 LSB = | Giá trị lớn nhất 0x7FFF | Giá trị nhỏ nhất 0x8000 |
| --- | --- | --- | --- | --- |
| Gyro ±500 °/s (GYRO_FS_SEL = 01) | 65.5 LSB/(°/s) | 0.0153 °/s | +500.3 °/s | −500.3 °/s |
| Accel ±4 g (ACCEL_FS_SEL = 01) | 8 192 LSB/g | 0.122 mg | +4.0 g | −4.0 g |
| Accel ±2 g (mặc định sau reset) | 16 384 LSB/g | 0.061 mg | +2.0 g | −2.0 g |
| Nhiệt độ | 333.87 LSB/°C, mốc 0 LSB tại 21 °C | 0.003 °C | — | — |

**Đánh đổi FS và độ nhạy**: FS càng lớn thì đo được chuyển động càng mạnh nhưng mỗi LSB càng "thô". Nhóm chọn ±500 °/s vì cổ tay lắc nhanh có thể vượt 250 °/s, và ±250 °/s sẽ bão hòa. Accel chọn ±4 g vì cú Flick cần ngưỡng 1.15 g **cộng thêm** 1 g trọng lực; ±2 g dễ bão hòa khi lắc mạnh.

**Vì sao con số 16 200 LSB trong log probe lại khác 8 192?** Chương trình probe không ghi ACCEL_CONFIG, nên thanh ghi giữ giá trị reset 0x01 (FS = ±2 g): 1 g ≈ 16 384 LSB. Firmware chính ghi ACCEL_CONFIG = 0x1B (FS = ±4 g), nên 1 g ≈ 8 192 LSB. Phép đo ngày 01/10 (firmware ±4 g) cho |A| = 8 097 LSB, xem bảng dưới.

### 4.2.3. Số liệu đo thật ngày 01/10/2026 (BENCH_VERIFIED)

Board đặt yên trên bàn; 1 000 mẫu cách nhau 10 ms; log: `raw_logs/bench_2026-10-01_icm20948_timing_noise_run2.log` (SHA-256 `89bdae09…a3dedc4`).

| Trục | Trung bình (LSB) | Đổi ra đơn vị | Độ lệch chuẩn σ | σ đổi đơn vị |
| --- | --- | --- | --- | --- |
| AX | +125.8 | +0.0154 g | 15.0 LSB | 1.8 mg |
| AY | −48.1 | −0.0059 g | 17.5 LSB | 2.1 mg |
| AZ | +8 095.8 | +0.9883 g | 17.7 LSB | 2.2 mg |
| GX | −36.8 | −0.56 °/s | 5.7 LSB | 0.087 °/s |
| GY | −96.0 | −1.46 °/s | 5.6 LSB | 0.086 °/s |
| GZ | +21.0 | +0.32 °/s | 6.3 LSB | 0.096 °/s |
| \|A\| | 8 097.0 | 0.9884 g | — | — |
| TEMP_OUT | 4 528 | 4528 / 333.87 + 21 = 34.6 °C (nhiệt độ die, không phải nhiệt độ phòng) | — | — |

**So với datasheet** (đây là cách trả lời "tại sao em chắc"):
- **Nhiễu accel**: mật độ nhiễu 230 µg/√Hz (§3.2) × √(NBW 68.8 Hz) ≈ **1.9 mg** dự đoán; đo được **1.8–2.2 mg**, khớp.
- **Nhiễu gyro**: 0.015 °/s/√Hz (§3.1, công bố ở FS ±250) × √73.3 ≈ 0.13 °/s dự đoán; đo được **0.09 °/s**, tốt hơn con số điển hình.
- **Bias gyro** −0.56 / −1.46 / +0.32 °/s nằm trong dung sai ZRO ban đầu ±5 °/s (§3.1). Firmware chính tự hiệu chuẩn ra −0.54 / −1.49 / +0.32 °/s (log `main_firmware_boot_com3_2026-10-01.log`), khớp với phép đo độc lập.
- **|A| = 0.988 g** lệch 11.6 mg so với 1 g, nằm trong dung sai zero-g mức board ±50 mg và dung sai độ nhạy ±0.5 % (§3.2).
- **Ý nghĩa cho thiết kế**: vùng chết dưới 0.8 °/s ≈ 9σ nhiễu gyro, nên nhiễu thuần túy không làm con trỏ trôi. Vấn đề chính là bias (tới 1.5 °/s), vì vậy phải trừ bias lúc khởi động và tự cập nhật khi đứng yên.

### 4.2.4. Tần số lấy mẫu và câu "ghi giá trị lớn nhất được không"

ODR = 1125 Hz / (1 + SMPLRT_DIV). Nhóm ghi DIV = 10, nên ODR = 102.27 Hz (chu kỳ 9.78 ms).

| Thanh ghi | Độ rộng | DIV = 0 | DIV = 10 (dự án) | DIV lớn nhất |
| --- | --- | --- | --- | --- |
| GYRO_SMPLRT_DIV (Bank 2, 0x00) | 8 bit | 1125 Hz | 102.27 Hz | 255 → 4.39 Hz |
| ACCEL_SMPLRT_DIV_1/2 (0x10–0x11) | 12 bit, chia làm 2 thanh ghi (bit [11:8] ở 0x10, bit [7:0] ở 0x11) | 1125 Hz | 102.27 Hz | 4095 → 0.27 Hz |

"Ghi 0xFFFF vào DIV gyro" là không được: thanh ghi chỉ có 8 bit. Accel 12 bit nên phải ghi 2 byte, 0x00 và 0x0A.

**Quan hệ với vòng lặp 100 Hz**: cảm biến tạo 102.27 mẫu/s, ESP32 đọc 100 lần/s. Cứ 1 / (102.27 − 100) ≈ 0.44 s thì một mẫu mới bị bỏ qua. Chọn ODR hơi **lớn hơn** tốc độ đọc để không bao giờ đọc lại một mẫu cũ hai lần. Mất 1 mẫu mỗi 0.44 s là không đáng kể với chuyển động tay.

> [!HOI] Thầy có thể hỏi: "LSB là gì? Tại sao chia 65.5?"
> LSB (least significant bit) là bước nhỏ nhất của số đầu ra ADC. Ở FS ±500 °/s, datasheet cho độ nhạy 65.5 LSB ứng với 1 °/s (vì 32 768 / 500 ≈ 65.5). Muốn đổi số thô ra °/s thì chia cho 65.5. Nếu đổi FS sang ±2000 °/s thì phải chia 16.4; chia sai hệ số thì con trỏ nhanh/chậm gấp 4 lần.

## 4.3. SAR ADC1 của ESP32 dùng để đo pin (NOT_IMPLEMENTED)

### 4.3.1. Thông số ADC ESP32 (datasheet ESP32 v5.3, Table 4-3 và 4-4)

| Thông số | Giá trị |
| --- | --- |
| Kiểu, độ phân giải | SAR (xấp xỉ liên tiếp), 12 bit, mã 0–4095 (4 096 mức) |
| Số kênh | 2 bộ ADC, tối đa 18 chân; ADC1 = GPIO32–39 |
| Sai số phi tuyến (100 nF ở đầu vào, Wi-Fi/BT tắt) | DNL ±7 LSB, INL ±12 LSB |
| Tốc độ | Bộ điều khiển RTC ≤ 200 ksps; bộ DIG ≤ 2 Msps |
| Chênh lệch giữa các chip nếu không hiệu chuẩn | ±6 % |
| Dải đo hiệu quả sau hiệu chuẩn eFuse Vref | atten 0: 100–950 mV (±23 mV); 1: 100–1250 mV (±30 mV); 2: 150–1750 mV (±40 mV); **3 (11 dB): 150–2450 mV (±60 mV)** |

**Suy hao (attenuation) là gì**: ADC đo trực tiếp chỉ khoảng dưới 1 V. Bộ suy hao đứng trước ADC chia nhỏ điện áp vào để mở rộng dải đo. Mỗi kênh có 2 bit chọn trong `SENS_SAR_ATTEN1_REG` (bit [1:0] cho kênh 0, bit [3:2] cho kênh 1…, nên kênh 6 là bit [13:12]). Giá trị 11 là mức lớn nhất (11 dB). Bản TRM ghi "11: 1 dB", đây là lỗi đánh máy; ESP-IDF gọi mức này là `ADC_ATTEN_DB_11/12`.

### 4.3.2. Thiết kế cầu chia áp

| Đại lượng | Phép tính | Kết quả |
| --- | --- | --- |
| Tỷ lệ chia | R3 / (R2 + R3) = 100k / 200k | 0.5 |
| Pin đầy 4.2 V | 4.2 × 0.5 | 2.10 V (dưới 2.45 V, trong dải chính xác của atten 3) |
| Pin cạn 3.0 V | 3.0 × 0.5 | 1.50 V |
| Dòng tiêu hao của cầu | 4.2 V / 200 kΩ | 21 µA ≈ 0.5 mAh/ngày (không đáng kể so với pin 1000 mAh) |
| Trở kháng nguồn nhìn từ ADC | 100k // 100k | 50 kΩ |
| Tụ C1 100 nF | τ = 50 kΩ × 100 nF | 5 ms. Tụ cấp điện tích tức thời cho tụ lấy mẫu của SAR, tránh sụt áp khi lấy mẫu; datasheet cũng đo DNL/INL với tụ 100 nF |
| Sai số quy về pin | ±60 mV × 2 | ±120 mV (≈ 10 % dải 3.0–4.2 V) nên chỉ dùng để báo mức pin thô |

**Vì sao không chia ít hơn (ví dụ 1:1.5)?** 4.2 / 1.5 = 2.8 V > 2.45 V, rơi vào vùng datasheet cảnh báo độ chính xác kém hơn (mã > 3000).
**Vì sao không dùng trở nhỏ hơn (10k/10k)?** Dòng rò tăng lên 210 µA, pin hao ≈ 5 mAh/ngày.

### 4.3.3. Đọc ADC tới mức thanh ghi (TRM, chương 31 On-Chip Sensors)

| Thanh ghi / trường | Vai trò |
| --- | --- |
| `SENS_SAR_READ_CTRL_REG.SENS_SAR1_SAMPLE_BIT` (bit [17:16]) | Độ phân giải: 00 = 9 bit … 11 = 12 bit |
| `SENS_SAR_READ_CTRL_REG.SENS_SAR1_CLK_DIV` (bit [7:0]) | Chia xung cho ADC |
| `SENS_SAR_ATTEN1_REG` (2 bit/kênh) | Mức suy hao của từng kênh ADC1 |
| `SENS_SAR_MEAS_START1_REG.SENS_SAR1_EN_PAD` (bit [30:19]) | Chọn kênh (bitmap) |
| `SENS_SAR_MEAS_START1_REG.SENS_MEAS1_START_SAR` (bit 17) | Ra lệnh bắt đầu chuyển đổi |
| `SENS_SAR_MEAS_START1_REG.SENS_MEAS1_DONE_SAR` (bit 16) | Cờ báo đã xong |
| `SENS_SAR_MEAS_START1_REG.SENS_MEAS1_DATA_SAR` (bit [15:0]) | Kết quả số |

Trong Arduino, `analogSetPinAttenuation()` / `analogReadResolution()` là nhóm lệnh **cấu hình** (ghi ATTEN và SAMPLE_BIT một lần). `analogRead()` là lệnh **tác động thiết bị** (bật START, chờ DONE, đọc DATA). Hàm `analogReadMilliVolts()` còn dùng giá trị Vref hiệu chuẩn lưu trong eFuse để đổi mã ra mV, giảm sai số giữa các chip.

### 4.3.4. Code đề xuất (chưa có trong firmware)

```
// Cấu hình: chạy 1 lần trong setup()
analogReadResolution(12);                  // SAMPLE_BIT = 11 (12 bit, 0..4095)
analogSetPinAttenuation(PIN_BAT_SENSE, ADC_11db);   // dải ~150..2450 mV

// Runtime: 1 lần mỗi giây là đủ (điện áp pin thay đổi chậm)
uint32_t mv_node = 0;
for (int i = 0; i < 16; ++i) mv_node += analogReadMilliVolts(PIN_BAT_SENSE);
mv_node /= 16;                             // lấy trung bình giảm DNL/nhiễu
float v_bat = 2.0f * mv_node / 1000.0f;    // bù hệ số cầu chia 1:2
```

Việc đổi điện áp ra phần trăm pin **không tuyến tính** (điện áp LiPo gần như phẳng ở khoảng 3.7–3.9 V), nên chỉ nên báo 3–4 mức (đầy / trung bình / yếu / cần sạc) và hiệu chỉnh bằng phép đo thực tế. Nhóm chưa đo đường cong xả của pin này.

> [!HOI] Thầy có thể hỏi: "ADC 12 bit thì đọc 4.2 V ra số bao nhiêu? Được ghi 4095 không?"
> Không nên nói "4.2 V ứng với 4095", vì hai lẽ: (1) cầu chia cho 2.1 V vào chân; (2) ở atten 11 dB, đặc tuyến ADC ESP32 không tuyến tính và lệch giữa các chip ±6 %. Vì vậy dùng `analogReadMilliVolts` (có hiệu chuẩn) thay vì tự nhân mã × 3.3 / 4095. Mã 4095 là **đọc ra** khi điện áp ≥ ngưỡng trên, không phải giá trị "ghi vào".

# 5. GIAO TIẾP I2C CHUYÊN SÂU

## 5.1. Khung truyền một lần đọc 12 byte

```
S | 0xD0 (0x68<<1 | W) | A | 0x2D (ACCEL_XOUT_H) | A | Sr | 0xD1 (0x68<<1 | R) | A |
  | AX_H A | AX_L A | AY_H A | AY_L A | AZ_H A | AZ_L A | GX_H A | ... | GZ_L NA | P
S = START, Sr = Repeated START, A = ACK, NA = NACK (master báo byte cuối), P = STOP
```

- **Địa chỉ 7 bit 0x68** (vì AD0 = 0). Byte gửi trên dây = địa chỉ dịch trái 1 bit + bit R/W: ghi 0xD0, đọc 0xD1.
- **Repeated START**: sau khi gửi địa chỉ thanh ghi 0x2D, master không phát STOP mà phát Sr để chuyển sang đọc (`Wire.endTransmission(false)`). Datasheet DS-000189 §6.3 quy định đúng trình tự này: S → AD+W → RA → Sr → AD+R → DATA → NACK → P, và nhóm làm đúng theo trình tự đó. Theo chuẩn I2C, bus vẫn ở trạng thái "bận" khi dùng Sr thay cho STOP, nên master khác không chen vào giữa lúc ghi địa chỉ thanh ghi và lúc đọc dữ liệu. Hiện chỉ có 1 master nên lợi ích chống chen bus chưa thể hiện; còn cách tách bằng STOP rồi START lại thì datasheet không mô tả, nên nhóm không dùng và không khẳng định kết quả của nó.
- **Burst tự tăng địa chỉ**: ICM tự tăng con trỏ thanh ghi sau mỗi byte, nên 1 lệnh đọc lấy liền 12 byte 0x2D → 0x38 (6 byte accel + 6 byte gyro). Lợi ích: 6 trục được lấy gần như cùng một thời điểm (không bảo đảm đồng bộ tuyệt đối) và tiết kiệm địa chỉ.
- **ACK/NACK**: slave kéo SDA xuống ở bit thứ 9 để báo đã nhận. Không có ACK (NACK) thì `Wire` báo lỗi, `imu_readBurst()` trả `false` và vòng lặp **bỏ qua chu kỳ đó**, không dùng dữ liệu rác.

## 5.2. Chọn bank thanh ghi

ICM-20948 có 4 bank × 128 thanh ghi. Thanh ghi `REG_BANK_SEL` ở địa chỉ **0x7F có mặt trong cả 4 bank**. Chỉ bit [5:4] (USER_BANK) có nghĩa, nên code ghi `(bank & 0x03) << 4`: bank 0 = 0x00, bank 1 = 0x10, bank 2 = 0x20, bank 3 = 0x30. Driver nhớ bank hiện tại (`s_current_bank`) để không ghi lại khi không cần.

## 5.3. Bộ điều khiển I2C của ESP32 tới mức thanh ghi (TRM chương 21)

| Thanh ghi / trường | Ý nghĩa |
| --- | --- |
| `I2C_CTR_REG.I2C_MS_MODE` (bit 4) | 1 = làm Master |
| `I2C_CTR_REG.I2C_TRANS_START` (bit 5) | Bắt đầu thực thi chuỗi lệnh |
| `I2C_SCL_LOW_PERIOD_REG` (bit [13:0]) | Số chu kỳ APB SCL ở mức thấp |
| `I2C_SCL_HIGH_PERIOD_REG` (bit [13:0]) | Số chu kỳ APB SCL ở mức cao |
| `I2C_COMDn_REG` (16 thanh ghi lệnh) | Mỗi lệnh có `op_code`: 0 = RSTART, 1 = WRITE, 2 = READ, 3 = STOP, 4 = END |

**400 kHz được tạo ra thế nào**: xung APB = 80 MHz (log bench: `APB 80000000 Hz`). Một chu kỳ SCL 400 kHz = 2.5 µs = 200 chu kỳ APB, chia cho LOW_PERIOD + HIGH_PERIOD (+ thời gian lọc/cạnh do driver bù). Giá trị cụ thể do driver `Wire` tính khi gọi `Wire.begin(21, 22, 400000)`. 100 kHz ứng với 800 chu kỳ.
**"Trường 14 bit thì chậm nhất được bao nhiêu?"**: tối đa 16 383 chu kỳ cho mỗi nửa, nên f_min ≈ 80 MHz / (2 × 16 383) ≈ 2.4 kHz.

Một lần `imu_readBurst()` được driver dịch thành chuỗi lệnh: RSTART → WRITE(0xD0, 0x2D) → RSTART → WRITE(0xD1) → READ(11 byte, ACK) → READ(1 byte, NACK) → STOP.

## 5.4. 100 kHz hay 400 kHz?

Standard-mode tối đa 100 kHz, Fast-mode tối đa 400 kHz; ICM hỗ trợ tới 400 kHz (DS-000189). Nhóm dùng 400 kHz để giảm thời gian chiếm bus còn khoảng 1/3. Phép thử 100/100 lần đọc WHO_AM_I ở cả 100 kHz và 400 kHz đều không có NACK (log 25/09).

## 5.5. Ngân sách thời gian: tính toán và đo thật

**Tính lý thuyết**: 1 lần đọc có 15 byte trên dây (địa chỉ ghi, thanh ghi, địa chỉ đọc, 12 byte dữ liệu). Mỗi byte 9 bit (8 dữ liệu + 1 ACK), cộng START/Sr/STOP, tổng ≈ 137 chu kỳ SCL.

| Tốc độ | Lý thuyết | **Đo thật** (N = 1 000, 0 lỗi) | Chênh lệch | % của chu kỳ 10 ms |
| --- | --- | --- | --- | --- |
| 400 kHz | 137 / 400 kHz ≈ 343 µs | min 431 / **tb 438.3** / max 505 µs | ≈ 96 µs | 4.4 % |
| 100 kHz | 137 / 100 kHz ≈ 1 370 µs | min 1 470 / **tb 1 471** / max 1 502 µs | ≈ 101 µs | 14.7 % |

**Giải thích chênh lệch**: phần dư gần như **không đổi (~100 µs)** dù tốc độ bus đổi 4 lần. Đó là chi phí phần mềm: driver nạp chuỗi lệnh, chờ ngắt báo xong, sao chép FIFO. Phần thời gian trên dây thì tỷ lệ đúng với tốc độ bus. Max 505 µs là do thỉnh thoảng bị tác vụ khác của hệ điều hành FreeRTOS chen vào.

> [!HOI] Thầy có thể hỏi: "Tại sao phải có trở kéo? Tại sao cần Repeated START? Nếu cảm biến không trả lời thì sao?"
> Trở kéo: I2C là open-drain; không có trở kéo thì đường dây không bao giờ lên mức 1. Module có sẵn 10 kΩ. Repeated START: giữ quyền bus giữa lúc "ghi địa chỉ thanh ghi" và lúc "đọc dữ liệu". Không trả lời (NACK): hàm trả false, vòng lặp bỏ chu kỳ đó; nếu lúc khởi động WHO_AM_I ≠ 0xEA thì firmware dừng và nháy LED 5 Hz báo lỗi.

# 6. THANH GHI CẤU HÌNH ICM-20948 TỪNG BIT

| Thanh ghi (bank, địa chỉ) | Giá trị | Phân tích bit | Tại sao chọn |
| --- | --- | --- | --- |
| WHO_AM_I (B0, 0x00) | đọc được 0xEA | Chỉ đọc; mã nhận dạng chip | Kiểm tra đúng chip, đúng dây trước khi cấu hình |
| PWR_MGMT_1 (B0, 0x06) | 0x01 = 0000 0001b | bit 7 DEVICE_RESET = 0; bit 6 SLEEP = 0 (thức dậy); bit 5 LP_EN = 0; bit 4 dự trữ; bit 3 TEMP_DIS = 0 (bật cảm biến nhiệt); bit [2:0] CLKSEL = 001 (tự chọn nguồn xung tốt nhất, ưu tiên PLL) | Sau reset chip đang **ngủ** (SLEEP = 1), phải ghi đầu tiên; PLL ổn định hơn dao động RC nội |
| REG_BANK_SEL (mọi bank, 0x7F) | 0x00 / 0x20 | bit [5:4] USER_BANK | Chuyển giữa bank 0 (dữ liệu) và bank 2 (cấu hình) |
| GYRO_SMPLRT_DIV (B2, 0x00) | 10 = 0x0A | 8 bit DIV | ODR = 1125 / 11 = 102.27 Hz |
| GYRO_CONFIG_1 (B2, 0x01) | 0x1B = 0001 1011b | bit [5:3] GYRO_DLPFCFG = 011 (3 dB 51.2 Hz, NBW 73.3 Hz, Table 16); bit [2:1] GYRO_FS_SEL = 01 (±500 °/s); bit 0 GYRO_FCHOICE = 1 (bật DLPF) | Lọc rung tay tần số cao; FS đủ cho cổ tay |
| ACCEL_SMPLRT_DIV_1/2 (B2, 0x10/0x11) | 0x00 / 0x0A | DIV 12 bit | Đồng bộ ODR với gyro |
| ACCEL_CONFIG (B2, 0x14) | 0x1B = 0001 1011b | bit [5:3] ACCEL_DLPFCFG = 011 (3 dB 50.4 Hz, NBW 68.8 Hz, Table 18); bit [2:1] ACCEL_FS_SEL = 01 (±4 g); bit 0 ACCEL_FCHOICE = 1 | Đủ dải cho Flick + trọng lực |
| TEMP_OUT (B0, 0x39–0x3A) | đọc | 16 bit; °C = TEMP_OUT / 333.87 + 21 | Đo 34.6 °C ngày 01/10 |

**Hai điểm dễ bị bắt lỗi:**
1. DLPF 51.2 Hz là **tần số cắt 3 dB**, không phải tần số lấy mẫu. Datasheet (Table 16/18) **không công bố độ trễ** cho các cấu hình này, nên nhóm không nêu con số độ trễ.
2. Cả 7 giá trị cấu hình đều được **đọc lại** (readback) sau khi ghi. Log 25/09 và 01/10 đều khớp; khớp hết thì firmware mới chạy tiếp.

> [!HOI] Thầy có thể hỏi: "0x1B là bao nhiêu nhị phân, từng bit làm gì? Nếu ghi 0x1F thì sao?"
> 0x1B = 0001 1011b; ý nghĩa từng bit như bảng trên. 0x1F = 0001 1111b làm FS_SEL = 11, thành ±2000 °/s. Chip vẫn chạy nhưng độ nhạy chỉ còn 16.4 LSB/(°/s); nếu code vẫn chia 65.5 thì con trỏ chậm đi 4 lần. Vì vậy hằng số chia trong code phải đi cùng giá trị thanh ghi (`ICM20948_GYRO_SCALE_500DPS`).

# 7. GPIO: ĐỌC NÚT VÀ ĐIỀU KHIỂN LED

## 7.1. Đường đi của một chân GPIO

Trên ESP32, tín hiệu đi qua **IO_MUX** (chọn chức năng, pull-up/pull-down, drive) và **GPIO Matrix** (định tuyến ngoại vi tới chân bất kỳ). Mỗi chân có một thanh ghi `IO_MUX_x_REG` với các trường:

| Trường | Ý nghĩa |
| --- | --- |
| `MCU_SEL` | Chọn chức năng (function 0, 1, …) |
| `FUN_IE` | Bật bộ đệm đầu vào |
| `FUN_WPU` / `FUN_WPD` | Bật trở kéo lên / kéo xuống nội (≈ 45 kΩ, datasheet Table 5-3) |
| `FUN_DRV` (2 bit) | **Độ mạnh ngõ ra** (drive strength), mặc định 2; GPIO34–39 luôn là 0 vì không có mạch xuất |

`pinMode(25, INPUT_PULLUP)` bật FUN_IE và FUN_WPU, xóa bit 25 của `GPIO_ENABLE_REG` (hướng vào).
`pinMode(32, OUTPUT)` bật bit 0 của `GPIO_ENABLE1_REG` (0x3FF4402C) vì GPIO32 thuộc nhóm 32–39.

## 7.2. Thanh ghi đọc/ghi mức logic

| Thanh ghi | Địa chỉ | Dùng cho |
| --- | --- | --- |
| `GPIO_IN_REG` | 0x3FF4403C | Bit 25, 26, 27 = mức của 3 nút (thả = 1, nhấn = 0) |
| `GPIO_IN1_REG` | 0x3FF44040 | GPIO32–39 (bit 2 = GPIO34 nếu đọc số) |
| `GPIO_OUT_REG` / `W1TS` / `W1TC` | 0x3FF44004 / 08 / 0C | GPIO0–31 |
| `GPIO_OUT1_REG` / `W1TS` / `W1TC` | 0x3FF44010 / 14 / 18 | GPIO32–39; **bit 0 = LED GPIO32** |

W1TS/W1TC ("write 1 to set/clear"): ghi 1 vào bit nào thì chỉ bit đó đổi, các bit khác giữ nguyên. Không cần đọc-sửa-ghi, nên an toàn khi có ngắt chen vào.

## 7.3. Các con số của nút và LED

| Đại lượng | Tính | Kết quả |
| --- | --- | --- |
| Dòng khi nhấn nút | 3.3 V / 45 kΩ | ≈ 73 µA |
| Dòng LED | (3.3 − V_f) / 1 kΩ, V_f LED xanh ≈ 2.0–2.2 V (ƯỚC TÍNH) | ≈ 1.1–1.3 mA |
| Khả năng dòng của chân | IOH 40 mA, IOL 28 mA ở drive tối đa (datasheet Table 5-3) | LED dùng < 5 % khả năng |
| Chống dội phím | Chưa có. Code chỉ bắt cạnh; đề xuất bỏ qua thay đổi trong 20 ms | NOT_IMPLEMENTED |

> [!HOI] Thầy có thể hỏi: "Tốc độ ngõ ra là gì?" (thầy từng hỏi nhóm STM32)
> STM32 có thanh ghi OSPEEDR chọn tốc độ ngõ ra, tức tốc độ sườn lên/xuống, ảnh hưởng tần số tối đa và nhiễu EMI. ESP32 **không** có thanh ghi "speed" riêng mà có `FUN_DRV` (độ mạnh dòng ra): drive càng mạnh thì sườn càng dốc, dòng càng lớn và nhiễu càng nhiều. LED bật/tắt chậm nên để mặc định. Nút bấm là **đầu vào**, nên khái niệm tốc độ ngõ ra không áp dụng cho chân nút.

# 8. ĐỊNH THỜI VÀ UART

## 8.1. Ai quyết định nhịp 100 Hz?

Vòng `loop()` so `micros()` với mốc trước. Chưa đủ 10 000 µs thì thoát; đủ thì xử lý. `micros()` lấy từ **esp_timer** (bộ đếm 64 bit, bước 1 µs) nên **không dùng ngắt timer phần cứng**.

| Cách | Ưu | Nhược |
| --- | --- | --- |
| Polling `micros()` (dự án dùng) | Đơn giản, xử lý I2C/BLE trong ngữ cảnh bình thường, không lo "gọi I2C trong ngắt" | CPU bận chờ; nếu một vòng chạy lố thì các vòng sau lệch pha (không bù lại) |
| Ngắt timer phần cứng (`timerBegin`…) | Nhịp chính xác | Không được gọi I2C/BLE dài trong ISR; phải dùng cờ hoặc hàng đợi |

**Đo thật** (bench, không có BLE/Serial chen vào): 500 chu kỳ, min = tb = max = **10 000 µs**, không vòng nào vượt 10.1 ms. Firmware chính đầy đủ (có BLE) báo "Rate: 100 Hz" liên tục; riêng giây đầu 88 Hz do khởi động BLE (log 01/10).

**dt cho bộ lọc** được tính lại mỗi vòng từ `millis()` và kẹp trong [1, 50] ms. Nếu một vòng bị trễ, phép tích phân quaternion vẫn đúng đơn vị; nếu trễ bất thường (> 50 ms) thì không để một bước tích phân quá lớn làm sai tư thế.

## 8.2. UART 115200 baud

- Khung 8N1 = 1 start + 8 data + 1 stop = 10 bit mỗi byte, nên 115 200 / 10 = **11 520 byte/s**.
- Dòng STATUS ≈ 75 ký tự mất ≈ 6.5 ms trên dây, in 1 lần/giây. Dữ liệu vào bộ đệm TX của driver nên không chặn vòng lặp khi bộ đệm còn chỗ.
- **Baud là số ký hiệu mỗi giây**; với UART nhị phân thì 1 ký hiệu = 1 bit, nên baud = bit/s. Nhưng byte/s nhỏ hơn 10 lần vì phải có start/stop.

# 9. THUẬT TOÁN XỬ LÝ CHUYỂN ĐỘNG

## 9.1. Các bước và tham số (lấy từ code)

| Bước | Tham số | Ý nghĩa / tại sao |
| --- | --- | --- |
| Hiệu chuẩn bias lúc khởi động | 200 mẫu × 10 ms (log: 2 200 ms) | Trung bình 200 mẫu giảm nhiễu √200 ≈ 14 lần: 0.09 → 0.006 °/s |
| Phát hiện đứng yên | \|ω\| < 1.2 °/s **và** \|\|a\| − 1\| < 0.08 g liên tục 30 mẫu (≈ 0.3 s) | Khi đứng yên thì khóa dX = dY = 0 |
| Tự cập nhật bias khi đứng yên | α = 0.002 mỗi mẫu | Hằng số thời gian ≈ 1/α = 500 mẫu ≈ 5 s: theo kịp trôi nhiệt chậm, không bị cú giật nhất thời kéo lệch |
| Bộ lọc bù quaternion | K = 2 s⁻¹, chỉ tin accel khi 0.75 g < \|a\| < 1.25 g | Gyro cho đáp ứng nhanh; accel kéo pitch/roll về đúng với τ = 1/K = 0.5 s. **Yaw không sửa được bằng accel** (trọng lực không chứa thông tin hướng ngang) |
| Vùng chết | 0.8 / 1.4 °/s, có dốc nối giữa hai ngưỡng | < 0.8: bằng 0; 0.8–1.4: tăng dần (tránh giật); > 1.4: trừ 0.8 |
| Chiếu theo tư thế tham chiếu | Trục dọc = vector trọng lực lúc recenter | Cầm nghiêng vẫn điều khiển đúng hướng màn hình |
| Gain và kẹp | 2.2; kẹp ±127 | Mục 1.2 |

Công thức vùng chết (với a = |ω|, L = 0.8, H = 1.4):
- a < L → 0
- L ≤ a ≤ H → dấu(ω) · (a − L)² / (H − L)
- a > H → dấu(ω) · (a − L)

## 9.2. Nhận diện cử chỉ Flick (máy trạng thái)

```
IDLE  --(giữ clutch)----------------> ARMED
ARMED --(a_lat < -1.15 g)-----------> PEAK_LEFT
PEAK_LEFT  --(a_lat > +0.35 g, sau 60..450 ms)--> gửi BACK    -> COOLDOWN 350 ms
ARMED --(a_lat > +1.15 g)-----------> PEAK_RIGHT
PEAK_RIGHT --(a_lat < -0.35 g, sau 60..450 ms)--> gửi FORWARD -> COOLDOWN 350 ms
PEAK_x --(quá 450 ms, không có pha hãm)--> ARMED
|ω| > 600 °/s bất kỳ lúc nào --> ARMED  (xoay mạnh, không phải lắc ngang)
```

- a_lat là gia tốc **đã trừ trọng lực**, chiếu lên trục ngang. Chỉ nhận cử chỉ khi pitch trong ±45° và roll trong ±30°.
- Cần **2 pha** (tăng tốc rồi hãm) để phân biệt cú lắc có chủ đích với va chạm một chiều.
- Trạng thái: HOST_TESTED (test 7 và 10). Ngưỡng là giá trị ban đầu, cần tinh chỉnh trên tay người thật.

> [!HOI] Thầy có thể hỏi: "Kp, Ki, Kd ở đâu? Dự án có PID không?"
> Không có vòng PID, vì không điều khiển cơ cấu chấp hành (động cơ). Tuy nhiên có hai hằng số đóng vai trò tương tự: K = 2 s⁻¹ của bộ lọc bù (giống hệ số tỷ lệ kéo sai số tư thế về 0, τ = 0.5 s) và α = 0.002 của auto-zero bias (giống khâu tích phân rất chậm). Đầu ra cũng được **giới hạn** (kẹp ±127), tương tự việc giới hạn đầu ra PID trong khoảng ARR.

## 9.3. Giải thích bằng hình ảnh đời thường

Mỗi khái niệm dưới đây có một hình ảnh để mở đầu và dễ nhớ, kèm điều **phải nói đúng về kỹ thuật**. Khi trả lời thầy, nên mở bằng hình ảnh (1 câu) rồi nêu ngay con số và tên đại lượng. Hình ảnh chỉ để hiểu, không thay thế cho số liệu.

| Khái niệm | Hình ảnh đời thường | Điều phải nói đúng về kỹ thuật | Mục |
| --- | --- | --- | --- |
| Gia tốc kế 3 trục (ax, ay, az) | Ba chiếc lò xo đặt theo ba hướng X, Y, Z; trọng lực kéo mỗi lò xo giãn một đoạn khác nhau tùy thiết bị đang nghiêng thế nào | Khi nằm yên, ba giá trị cho biết trọng lực "nằm" ở trục nào của thiết bị. Nằm phẳng thì AZ ≈ +1 g, AX và AY ≈ 0 (đo thật: AZ +0.988 g, AX +0.015 g, AY −0.006 g). Nghiêng thì giá trị chuyển sang trục khác nên tính được pitch/roll. Chip đo bằng cấu trúc MEMS, không có lò xo thật | 4.2.3 |
| Bộ lọc bù (K = 2 s⁻¹) | Hai người cùng chỉ đường: người nhanh nhưng lâu dần chỉ lệch (gyro), người chậm và hay run khi đi nhanh nhưng luôn biết đâu là hướng xuống đất (accel). Lấy người nhanh làm chính, liên tục kéo nhẹ về phía người kia | Chạy mỗi chu kỳ 10 ms, **kể cả khi đang giữ Clutch**. Hằng số thời gian τ = 1/K = 0.5 s. Chỉ nghe accel khi 0.75 g < \|a\| < 1.25 g: vung tay mạnh thì \|a\| lệch xa 1 g, accel không còn phản ánh đúng hướng trọng lực nên bị bỏ qua. Accel không sửa được yaw vì trọng lực song song với trục quay thẳng đứng | 9.1 |
| Chiếu theo tư thế tham chiếu | Cầm điều khiển TV nghiêng 45° cho đỡ mỏi, nhưng xoay cổ tay sang trái/phải thì con trỏ vẫn chạy ngang màn hình | Vector trọng lực được **chụp một lần lúc căn lại tâm** (recenter, khi thả Clutch) và dùng làm trục dọc. dX lấy từ thành phần vận tốc góc **dọc theo trục đó** (quay quanh phương thẳng đứng, tức yaw); dY lấy từ thành phần theo trục ngang vuông góc. Vector này không cập nhật liên tục: đổi cách cầm thì giữ rồi thả Clutch để căn lại tâm | 1.2, 9.1 |
| Nút Clutch | Nhấc chuột quang lên khỏi mặt bàn để dịch tay về chỗ thoải mái rồi đặt xuống lại | Giữ nút: dX = dY = 0 và bật nhận cử chỉ. Thả nút mà chưa có cử chỉ nào thì căn lại tâm (recenter) | 1.4, 9.2 |
| Vùng chết 2 ngưỡng (0.8 / 1.4 °/s) | Bàn đạp ga: đạp nhẹ thì xe chưa chạy, đạp dần thì tăng tốc mượt, đạp sâu thì tăng đều | Dưới 0.8 °/s bằng 0 (dập rung tay); 0.8–1.4 °/s tăng theo đường parabol (a − 0.8)² / 0.6; trên 1.4 °/s tăng tuyến tính (a − 0.8). Hai ngưỡng giúp con trỏ không giật khựng như khi chỉ có một ngưỡng cứng | 9.1 |
| Cử chỉ Flick 2 pha | Gõ cửa: một cú đập rồi tay rút về; còn vật bị va vào thì chỉ có một chiều | Vượt 1.15 g rồi hãm ngược quá 0.35 g trong 60–450 ms, sau đó nghỉ 350 ms. Cần cả hai pha để loại bỏ va chạm một chiều | 9.2 |
| Tạo xung SCL 400 kHz | Một máy gõ nhịp 80 triệu tích tắc mỗi giây; muốn mỗi nhịp SCL dài 2.5 µs thì đếm 200 tích tắc | 80 MHz / 400 kHz = 200 chu kỳ APB cho một chu kỳ SCL, chia cho thời gian SCL ở mức thấp và mức cao. Giá trị chính xác của từng nửa do driver `Wire` đặt | 5.3 |
| 343 µs tính toán so với 438 µs đo thật | Xe chạy trên đường (tín hiệu trên dây) cộng thời gian bốc dỡ hàng ở hai đầu (phần mềm) | 343 µs là 137 chu kỳ SCL ở 400 kHz. Phần dôi khoảng 100 µs gần như không đổi khi đổi tốc độ bus (≈ 95 µs ở 400 kHz, ≈ 101 µs ở 100 kHz) nên là chi phí phần mềm của driver (nạp lệnh, chờ ngắt, chép FIFO), không phải thời gian trên dây | 5.5 |

# 10. BLUETOOTH LOW ENERGY HID

| Byte | Nội dung | Kiểu | Dải |
| --- | --- | --- | --- |
| 0 | Nút (bit 0 trái, bit 1 phải, bit 2 giữa, bit 3 back, bit 4 forward) | bitmask | — |
| 1 | dX | int8 | −127 … +127 |
| 2 | dY | int8 | −127 … +127 |
| 3 | Wheel (cuộn dọc) | int8 | luôn 0 |
| 4 | Pan (cuộn ngang) | int8 | luôn 0 |

- Gói **5 byte** do thư viện `t-vk/ESP32 BLE Mouse` 0.3.1 định nghĩa trong HID Report Descriptor.
- Tốc độ gửi tối đa phụ thuộc **connection interval** do máy tính (central) chọn trong khoảng 7.5 ms – 4 s theo chuẩn BLE; firmware không đặt giá trị này. Nếu interval > 10 ms thì các gói 100 Hz sẽ bị gom hoặc xếp hàng. Chưa đo.
- Trạng thái: phát quảng bá "AirMouse-ESP32" thấy trong log; **ghép nối với PC: NOT_TESTED**.

# 11. KẾT QUẢ, HẠN CHẾ VÀ KẾ HOẠCH

## 11.1. Bảng kết quả kiểm chứng

| Hạng mục | Kết quả | Bằng chứng | Trạng thái |
| --- | --- | --- | --- |
| Nhận dạng chip ESP32 | ESP32-D0WD-V3 rev 3.1, flash 4 MB | `raw_logs/esptool_chip_id.log` | BENCH_VERIFIED |
| WHO_AM_I + readback 7 thanh ghi | 0xEA, 0x01, 0x1B, 0x1B, 10, 10 | log 25/09 và 01/10 | BENCH_VERIFIED |
| Thời gian đọc burst 12 byte | 438 µs (400 kHz), 1 471 µs (100 kHz), 0/2 000 lỗi | `bench_2026-10-01_…_run2.log` | BENCH_VERIFIED |
| Nhiễu tĩnh | gyro σ ≈ 0.09 °/s, accel σ ≈ 2 mg | như trên | BENCH_VERIFIED |
| Bias gyro | −0.56 / −1.46 / +0.32 °/s | bench + boot log | BENCH_VERIFIED |
| Nhịp vòng lặp | 100 Hz ổn định | boot log 01/10 | BENCH_VERIFIED |
| Thuật toán (lọc, đứng yên, clutch, flick) | 10/10 test | `firmware/test/` (baseline 26/09) | HOST_TESTED |
| Build firmware | RAM 39 628 B (12.1 %), Flash 1 158 957 B (88.4 %) | `pio run -d firmware` ngày 01/10 | BUILD OK |
| Nút, LED | Chưa lắp | — | NOT_TESTED |
| Đo pin bằng ADC | Chưa có code | — | NOT_IMPLEMENTED |
| Ghép nối BLE với PC | Chưa thử | — | NOT_TESTED |

## 11.2. Hạn chế

1. Ghép nối BLE với máy tính chưa thử; độ trễ thực tế chưa đo.
2. Đo pin (ADC1) và chống dội phím chưa có trong firmware.
3. Yaw chỉ tương đối (chưa dùng từ kế), xoay liên tục lâu có thể trôi nhẹ.
4. Nối trực tiếp 3.3 V: datasheet IC trần quy định V_DDIO = 1.71–1.95 V (§3.4), trong khi V_DD cho phép 1.71–3.6 V. Kết quả tốt chỉ áp dụng cho đúng module của nhóm, chưa thử bền lâu dài.
5. Sơ đồ KiCad vẫn là bản 1.8 V cũ (STALE); netlist tài liệu đã cập nhật (V2.1.0).
6. Gain, ngưỡng cử chỉ là giá trị ban đầu, chưa tinh chỉnh với người dùng.

## 11.3. Kế hoạch

1. Lắp nút/LED/cầu chia áp lên breadboard; thêm code ADC đo pin và debounce 20 ms.
2. Ghép nối BLE với laptop, đo độ trễ và thử duyệt slide.
3. Cập nhật KiCad qua KiCad MCP theo netlist V2.1.0, sau đó mới làm PCB.
4. Tinh chỉnh gain/ngưỡng trên người dùng thật.

# 12. ĐỌC HIỂU CODE: CÁC ĐOẠN NGẮN THẦY CÓ THỂ BẮT GIẢI THÍCH

Phần này viết cho người **chưa học lập trình**. Mọi đoạn code dưới đây đều **trích nguyên văn từ firmware đang chạy trên board** (thư mục `firmware/`). Chỉ lược bớt phần dành cho chạy thử trên máy tính và các dòng lặp lại (đánh dấu `...`); không viết lại hay thêm code mới. Mỗi đoạn có bốn phần: nói bằng lời, giải thích từng dòng, ví dụ bằng số, và câu thầy có thể hỏi.

**Báo cáo nộp có 4 đoạn code. Đây là phần thầy đọc được, nên là ưu tiên số 1.** Mục 4.4 của báo cáo nộp (`BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5`) trích đúng bốn đoạn dưới đây. Thầy chỉ vào đoạn nào thì giải thích ở mục tương ứng; mục 12.11 có sẵn lời trả lời 30 giây cho từng đoạn.

| Mục trong báo cáo nộp | Đoạn code (file) | Đọc giải thích ở | Lời trả lời 30 giây |
| --- | --- | --- | --- |
| 4.4.1 | Ghép 2 byte và chia 65.5 (`icm20948_driver.cpp`) | 12.4 | 12.11 |
| 4.4.2 | Vùng chết, hệ số 2.2 và kẹp ±127 (`motion_pipeline.cpp`) | 12.6 | 12.11 |
| 4.4.3 | Bộ lọc bù, cổng 0.75–1.25 g và K = 2 (`motion_pipeline.cpp`) | 12.7 | 12.11 |
| 4.4.4 | Máy trạng thái Flick (`gesture_detector.cpp`) | 12.9 | 12.11 |

Đoạn 4.4.1 trong báo cáo nộp chỉ lấy trục X của con quay (`raw_gx`) làm đại diện; mục 12.4 giải thích thêm cả trục Z của gia tốc kế, cùng một logic.

Cách học: đọc phần "Nói bằng lời" trước, rồi nhìn code và tự đoán nghĩa từng dòng, sau đó đối chiếu bảng giải thích, cuối cùng làm bài tự kiểm tra ở mục 12.10.

## 12.0. Đọc code trong 10 phút

### Bản đồ: hàm nào gọi hàm nào

```
firmware.ino : loop()                  <- chạy lặp mãi, mỗi 10 ms một vòng
  |-- imu_readData()                   <- icm20948_driver.cpp: lấy số đo của ICM
  |     `-- imu_readBurst()            <- đọc 12 byte qua I2C (thư viện Wire)
  |-- digitalRead(...)                 <- đọc 3 nút bấm
  |-- motion_process()                 <- motion_pipeline.cpp: toàn bộ thuật toán
  |     |-- apply_deadzone()           <- vùng chết
  |     |-- clamp_i8()                 <- kẹp dX, dY trong ±127
  |     `-- gesture_update()           <- gesture_detector.cpp: cử chỉ Flick
  `-- bleMouse.move(dX, dY, 0)         <- gửi gói chuột qua Bluetooth
```

| File | Vai trò |
| --- | --- |
| `firmware.ino` | Chương trình chính: `setup()` chạy 1 lần lúc bật nguồn, `loop()` chạy lặp mãi |
| `include/pin_definitions.h` | Tên chân: `PIN_I2C_SDA` = 21, `PIN_BTN_LEFT` = 25, `PIN_LED_STATUS` = 32… |
| `include/icm20948_registers.h` | Địa chỉ thanh ghi và giá trị cấu hình của ICM-20948 |
| `src/icm20948_driver.cpp` | Nói chuyện với ICM-20948 qua I2C: chọn bank, ghi/đọc thanh ghi, đọc dữ liệu |
| `src/motion_pipeline.cpp` | Xử lý chuyển động: trừ bias, bộ lọc, vùng chết, gain, kẹp |
| `src/gesture_detector.cpp` | Nhận diện cử chỉ Flick bằng máy trạng thái |

### Từ vựng C/C++ cần biết

| Ký hiệu | Nghĩa | Ví dụ trong dự án |
| --- | --- | --- |
| `// ...` | Ghi chú, máy bỏ qua | `// 400 kHz Fast-Mode` |
| `#define TÊN giá_trị` | Đặt tên cho một con số; trước khi biên dịch, chữ `TÊN` được thay bằng giá trị. Không tốn bộ nhớ | `#define REG_WHO_AM_I 0x00` |
| `0x1B` | Số hệ 16 (`0x` là tiền tố). 0x1B = 0001 1011b = 27 | `0x1B`, `0xEA` |
| `uint8_t`, `uint16_t`, `uint32_t` | Số nguyên **không dấu** 8/16/32 bit: 0…255, 0…65 535, 0…4 294 967 295 | `uint32_t now_us` |
| `int8_t`, `int16_t` | Số nguyên **có dấu** (bù hai): −128…127, −32 768…32 767 | `int16_t raw_az` |
| `float` | Số thực 32 bit; hậu tố `f` báo đó là float | `65.5f`, `2.2f` |
| `bool` | Đúng/sai (`true`/`false`) | `bool btn_left_pressed` |
| `static` (ngoài hàm) | Biến chỉ file này thấy, giữ giá trị suốt chương trình | `static float s_bias_x` |
| `=`, `==`, `!=` | Gán giá trị; so sánh bằng; so sánh khác | `if (id == 0xEA)` |
| `&&`, `\|\|`, `!` | "và", "hoặc", "phủ định" | `a && !b` |
| `&`, `\|`, `<<` | Phép bit: AND, OR, dịch trái | `(bank & 0x03) << 4` |
| `a += b` | Cộng dồn: `a = a + b` | `sum_x += data.gx` |
| `cond ? A : B` | Nếu `cond` đúng lấy A, sai lấy B | `(val > 0.0f) ? x : -x` |
| `if / else`, `for` | Rẽ nhánh; lặp `for (int i = 0; i < n; ++i)` là lặp n lần | vòng 200 mẫu |
| `kiểu tên(tham số) { ... }` | Định nghĩa hàm; `void` là không trả về gì; `return` thoát hàm | `bool imu_readBurst(...)` |
| `uint8_t* buffer`, `&imu_data` | **Con trỏ**: địa chỉ của một biến/mảng. Hàm ghi kết quả thẳng vào biến của nơi gọi | `imu_readData(&imu_data)` |
| `p->x`, `s.x` | Lấy trường `x` của nhóm biến (qua con trỏ `p` / trực tiếp `s`) | `data->az`, `s_diag.who_am_i` |
| `(int16_t)x` | **Ép kiểu**: bắt máy hiểu `x` theo kiểu khác | `(int16_t)(...)` |

## 12.1. Hằng số và cấu hình thanh ghi

**Nguồn:** `include/icm20948_registers.h`, `src/icm20948_driver.cpp` dòng 137–138 và 154–157.

```
#define REG_BANK_SEL            0x7F
#define REG_WHO_AM_I            0x00
#define VAL_WHO_AM_I_EXPECTED   0xEA
#define REG_PWR_MGMT_1          0x06
#define VAL_PWR_MGMT_1_WAKE     0x01
#define VAL_GYRO_CONFIG_1_DEFAULT 0x1B
#define ICM20948_GYRO_SCALE_500DPS   65.5f
#define ICM20948_ACCEL_SCALE_4G      8192.0f
```

```
imu_writeReg(2, REG_GYRO_CONFIG_1, VAL_GYRO_CONFIG_1_DEFAULT);
s_diag.gyro_config_1 = imu_readReg(2, REG_GYRO_CONFIG_1);
...
s_diag.init_success = (s_diag.who_am_i == VAL_WHO_AM_I_EXPECTED) &&
                      (s_diag.pwr_mgmt_1 == VAL_PWR_MGMT_1_WAKE) &&
                      (s_diag.gyro_config_1 == VAL_GYRO_CONFIG_1_DEFAULT) &&
                      (s_diag.accel_config == VAL_ACCEL_CONFIG_DEFAULT) &&
                      ...
```

**Nói bằng lời:** `#define` đặt tên dễ đọc cho các con số của datasheet. Sau khi ghi cấu hình, firmware **đọc lại** chính thanh ghi đó để kiểm tra chip đã nhận đúng; chỉ khi cả 7 giá trị đọc lại đều khớp thì khởi tạo mới được coi là thành công.

| Dòng code | Ý nghĩa |
| --- | --- |
| `#define REG_WHO_AM_I 0x00` | Chữ `REG_WHO_AM_I` sẽ được thay bằng `0x00` trước khi biên dịch. Không chiếm RAM, không có kiểu dữ liệu |
| `0xEA` | Số hệ 16 = 1110 1010b = 234: mã nhận dạng của chip ICM-20948 |
| `65.5f`, `8192.0f` | Số thực (`f` = float). Là độ nhạy: 65.5 LSB ứng với 1 °/s; 8 192 LSB ứng với 1 g |
| `imu_writeReg(2, REG_GYRO_CONFIG_1, 0x1B)` | Ghi 0x1B vào thanh ghi GYRO_CONFIG_1 (địa chỉ 0x01) của **bank 2** |
| `s_diag.gyro_config_1 = imu_readReg(...)` | Đọc lại chính thanh ghi đó và cất vào biến chẩn đoán `s_diag` (dấu `.` lấy một trường) |
| `a == b` | So sánh bằng (khác với `=` là gán) |
| `&&` | "và": cả hai vế phải đúng |
| `s_diag.init_success = (...) && (...) && ...` | `init_success` chỉ đúng khi **mọi** so sánh đều đúng |

**Ví dụ bằng số:** 0x1B = 0001 1011b → bit [5:3] = 011 (lọc 51.2 Hz), bit [2:1] = 01 (±500 °/s), bit 0 = 1 (bật lọc). Đó chính là bảng ở mục 6.

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** `#define` khác một biến thông thường ở điểm nào?
> **Đáp:** `#define` chỉ là thay chữ trước khi biên dịch nên không chiếm bộ nhớ và không có kiểu dữ liệu; biến thì nằm trong RAM và có kiểu.
> **Hỏi:** Vì sao ghi xong còn đọc lại?
> **Đáp:** Để chắc chip đã nhận đúng cấu hình (đúng dây, đúng bank). Nếu có giá trị không khớp, `imu_init()` trả về `false`; trong `setup()` chương trình in `[FATAL]` và nháy LED mãi, không chạy tiếp.

## 12.2. Chọn bank thanh ghi

**Nguồn:** `src/icm20948_driver.cpp` dòng 16 và 19–34 (đã bỏ phần `#ifdef` dành cho chạy thử trên máy tính).

```
static uint8_t s_current_bank = 0xFF;
...
void imu_selectBank(uint8_t bank) {
    if (s_current_bank == bank) {
        return;
    }
    Wire.beginTransmission(ICM20948_I2C_ADDR);
    Wire.write(REG_BANK_SEL);
    Wire.write((bank & 0x03) << 4);
    Wire.endTransmission();
    s_current_bank = bank & 0x03;
}
```

**Nói bằng lời:** ICM-20948 có hơn 128 thanh ghi nên chia làm 4 bank. Muốn đọc/ghi thanh ghi ở bank nào thì phải ghi số bank vào thanh ghi 0x7F trước. Hàm nhớ bank hiện tại để khỏi ghi lại khi không cần.

| Dòng code | Ý nghĩa |
| --- | --- |
| `static uint8_t s_current_bank = 0xFF;` | Biến nhớ bank đang chọn. Ban đầu 0xFF (255), không trùng bank thật (0–3) nên **lần gọi đầu luôn ghi** |
| `if (s_current_bank == bank) { return; }` | Đang đúng bank rồi thì thoát, không gửi gì lên dây |
| `Wire.beginTransmission(ICM20948_I2C_ADDR);` | Chuẩn bị truyền tới địa chỉ 0x68 (chưa gửi gì lên dây) |
| `Wire.write(REG_BANK_SEL);` | Xếp byte thứ nhất vào hàng đợi: địa chỉ thanh ghi 0x7F |
| `Wire.write((bank & 0x03) << 4);` | Byte thứ hai: số bank. `& 0x03` giữ 2 bit thấp (chỉ còn 0–3); `<< 4` dịch trái 4 bit để đặt vào bit [5:4] |
| `Wire.endTransmission();` | **Lúc này mới gửi** cả hàng đợi lên dây: START, 0xD0, 0x7F, giá trị, STOP |
| `s_current_bank = bank & 0x03;` | Ghi nhớ bank vừa chọn |

**Ví dụ bằng số:**

| `bank` | `bank & 0x03` | `<< 4` | Giá trị ghi vào 0x7F |
| --- | --- | --- | --- |
| 0 | 0 | 0000 0000b | 0x00 |
| 2 | 2 | 0010 0000b | 0x20 |
| 3 | 3 | 0011 0000b | 0x30 |
| 5 (nhập sai) | 1 | 0001 0000b | 0x10 (phép `& 0x03` chặn không cho vượt bank 3) |

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** `(bank & 0x03) << 4` làm gì?
> **Đáp:** `& 0x03` giữ lại 2 bit thấp để bank chỉ là 0–3; `<< 4` dịch số bank vào bit [5:4] của thanh ghi 0x7F (USER_BANK). Bank 2 thành 0x20.
> **Hỏi:** Vì sao `s_current_bank` bắt đầu bằng 0xFF?
> **Đáp:** 0xFF không phải bank hợp lệ nên lần đầu hàm luôn ghi lên chip, sau đó mới có thể bỏ qua khi bank không đổi.
> **Hỏi:** `Wire.write` có gửi dữ liệu ngay không?
> **Đáp:** Không. `write` chỉ xếp byte vào hàng đợi; `endTransmission` mới phát lên dây.

## 12.3. Đọc liên tiếp nhiều byte (burst)

**Nguồn:** `src/icm20948_driver.cpp` dòng 69–85 (đã bỏ phần `#ifdef`).

```
bool imu_readBurst(uint8_t bank, uint8_t reg, uint8_t* buffer, size_t length) {
    if (!buffer || length == 0) return false;
    imu_selectBank(bank);
    Wire.beginTransmission(ICM20948_I2C_ADDR);
    Wire.write(reg);
    uint8_t err = Wire.endTransmission(false);
    if (err != 0) return false;
    size_t received = Wire.requestFrom((uint8_t)ICM20948_I2C_ADDR, length);
    if (received != length) return false;
    for (size_t i = 0; i < length; ++i) {
        buffer[i] = Wire.read();
    }
    return true;
}
```

**Nói bằng lời:** hàm này thực hiện đúng trình tự đọc của datasheet: gửi địa chỉ thanh ghi đầu, phát Repeated START, rồi đọc liền `length` byte. Mỗi bước đều kiểm tra lỗi; có lỗi thì trả `false` để nơi gọi bỏ chu kỳ đó.

| Dòng code | Ý nghĩa |
| --- | --- |
| `bool imu_readBurst(..., uint8_t* buffer, size_t length)` | Trả `true`/`false`. `uint8_t* buffer` là **con trỏ**: địa chỉ mảng do nơi gọi cấp; hàm ghi dữ liệu thẳng vào đó |
| `if (!buffer \|\| length == 0) return false;` | Kiểm tra đầu vào: `!buffer` là con trỏ rỗng, `\|\|` là "hoặc". Đầu vào sai thì thất bại ngay |
| `imu_selectBank(bank);` | Chọn đúng bank trước (mục 12.2) |
| `Wire.write(reg);` | Gửi địa chỉ thanh ghi đầu tiên cần đọc (ví dụ 0x2D) |
| `Wire.endTransmission(false)` | Tham số `false` nghĩa là **không phát STOP** mà phát Repeated START (Sr). Trả về 0 nếu chip ACK |
| `if (err != 0) return false;` | Khác 0 là lỗi (ví dụ không có ACK) → thất bại |
| `Wire.requestFrom(0x68, length)` | Master yêu cầu đọc `length` byte; trả về số byte thực nhận |
| `if (received != length) return false;` | Nhận thiếu byte → thất bại |
| `buffer[i] = Wire.read();` trong vòng `for` | Lấy từng byte cất vào mảng; `i` chạy từ 0 đến `length − 1` |
| `return true;` | Thành công |

**Đối chiếu với khung truyền ở mục 5.1:** `endTransmission(false)` tạo ra `S, 0xD0, 0x2D, Sr`; `requestFrom` tạo ra `0xD1, 12 byte dữ liệu, NACK, P`.

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** `endTransmission(false)` khác `endTransmission()` thế nào?
> **Đáp:** `false` là giữ bus và phát Repeated START để chuyển sang đọc, đúng trình tự datasheet DS-000189 §6.3. Không có tham số thì phát STOP.
> **Hỏi:** Nếu hàm trả `false` thì chương trình làm gì?
> **Đáp:** Trong `loop()`, `if (!imu_readData(&imu_data)) { return; }` bỏ qua chu kỳ đó, không dùng dữ liệu rác. Phép đo ngày 01/10: 0 lỗi trên 2 000 lần đọc.

## 12.4. Ghép hai byte thành một số và đổi ra đơn vị thật (có trong báo cáo nộp, mục 4.4.1)

**Nguồn:** `src/icm20948_driver.cpp` dòng 192–212 (chỉ giữ trục Z của accel và trục X của gyro, hai trục còn lại làm y hệt).

```
uint8_t raw[12];
if (!imu_readBurst(0, REG_ACCEL_XOUT_H, raw, 12)) {
    return false;
}
int16_t raw_az = (int16_t)(((uint16_t)raw[4] << 8) | raw[5]);
int16_t raw_gx = (int16_t)(((uint16_t)raw[6] << 8) | raw[7]);
data->az = (float)raw_az / ICM20948_ACCEL_SCALE_4G;
data->gx = (float)raw_gx / ICM20948_GYRO_SCALE_500DPS;
```

**Nói bằng lời:** mỗi trục là một số 16 bit nhưng I2C chỉ chuyển từng byte, nên chip gửi **byte cao trước, byte thấp sau**. Firmware ghép hai byte lại thành một số có dấu, rồi chia cho độ nhạy để ra đơn vị g hoặc °/s.

| Dòng code | Ý nghĩa |
| --- | --- |
| `uint8_t raw[12];` | Mảng 12 byte: `raw[0..5]` là accel X, Y, Z (mỗi trục 2 byte); `raw[6..11]` là gyro X, Y, Z |
| `imu_readBurst(0, REG_ACCEL_XOUT_H, raw, 12)` | Đọc 12 byte từ thanh ghi 0x2D của bank 0 vào mảng `raw` |
| `(uint16_t)raw[4] << 8` | Lấy byte cao của accel Z, ép thành số 16 bit rồi **dịch trái 8 bit** để nó nằm ở nửa trên |
| `\| raw[5]` | Phép OR **ghép** byte thấp vào nửa dưới |
| `(int16_t)(...)` | Hiểu số 16 bit đó là số **có dấu** (bù hai), để biết âm hay dương |
| `(float)raw_az / ICM20948_ACCEL_SCALE_4G` | Đổi sang số thực rồi chia 8 192 để ra đơn vị g |
| `data->az = ...` | Ghi kết quả vào biến của nơi gọi qua con trỏ `data` (mũi tên `->` lấy một trường) |

**Ví dụ bằng số thật** (board nằm yên, mục 4.2.3): `raw[4]` = 0x1F, `raw[5]` = 0xA0.
- 0x1F << 8 = 0x1F00 = 7 936.
- 0x1F00 OR 0xA0 = 0x1FA0 = 8 096 LSB.
- 8 096 / 8 192 = **0.988 g**, đúng với số đo AZ.

**Ví dụ số âm** (gyro): `raw` = {0xFF, 0x38} → 0xFF38. Khi hiểu là có dấu thì bằng 65 336 − 65 536 = **−200 LSB** → −200 / 65.5 = **−3.05 °/s**. Nếu quên ép sang `int16_t` thì được 65 336 → 65 336 / 65.5 ≈ 997 °/s, sai hoàn toàn.

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** Vì sao phải dịch trái 8 bit rồi mới OR?
> **Đáp:** Số 16 bit gồm byte cao và byte thấp. Dịch byte cao lên nửa trên, OR byte thấp vào nửa dưới thì ra đúng số gốc.
> **Hỏi:** Vì sao chia cho 65.5 và 8 192?
> **Đáp:** Đó là độ nhạy của datasheet ở dải ±500 °/s và ±4 g. Đổi dải đo thì phải đổi hằng số chia, nếu không số liệu sai (mục 6).

## 12.5. Vòng lặp 10 ms và đọc nút bấm

**Nguồn:** `firmware.ino` dòng 83, 129–143, 146 và 168–173 (rút gọn: bỏ chú thích, giữ nút trái làm đại diện).

```
pinMode(PIN_BTN_LEFT, INPUT_PULLUP);
...
void loop() {
    uint32_t now_us = micros();
    if (now_us - s_last_loop_us < 10000) {
        return;
    }
    s_last_loop_us = now_us;
    ...
    imu_data_t imu_data;
    if (!imu_readData(&imu_data)) {
        return;
    }
    bool btn_left_pressed  = (digitalRead(PIN_BTN_LEFT) == LOW);
    ...
    if (btn_left_pressed && !s_last_btn_l) {
        bleMouse.press(MOUSE_LEFT);
    } else if (!btn_left_pressed && s_last_btn_l) {
        bleMouse.release(MOUSE_LEFT);
    }
    s_last_btn_l = btn_left_pressed;
```

**Nói bằng lời:** `loop()` được gọi lặp mãi. Mỗi lần gọi, nếu chưa đủ 10 000 µs kể từ vòng trước thì thoát ngay (gọi lại liền); đủ thì mới làm việc. Cách chờ bằng cách hỏi giờ liên tục này gọi là **polling**. Với nút bấm, chương trình chỉ gửi lệnh khi nút **vừa đổi trạng thái**, không gửi lặp mỗi 10 ms.

| Dòng code | Ý nghĩa |
| --- | --- |
| `pinMode(PIN_BTN_LEFT, INPUT_PULLUP);` | Chân GPIO25 làm ngõ vào và bật trở kéo lên nội (≈ 45 kΩ): thả nút đọc 1, nhấn nút nối GND đọc 0 |
| `uint32_t now_us = micros();` | Số µs kể từ lúc bật nguồn (số 32 bit không dấu) |
| `if (now_us - s_last_loop_us < 10000) { return; }` | Chưa đủ 10 000 µs thì thoát hàm; Arduino gọi lại `loop()` ngay |
| `s_last_loop_us = now_us;` | Đủ rồi: đặt mốc mới cho vòng kế tiếp |
| `imu_readData(&imu_data)` | `&imu_data` là **địa chỉ** của biến `imu_data`; hàm điền số đo vào đó. Thất bại thì `return` bỏ chu kỳ |
| `(digitalRead(PIN_BTN_LEFT) == LOW)` | `true` khi chân đọc mức thấp, tức là **đang nhấn** (active-low) |
| `btn_left_pressed && !s_last_btn_l` | "Bây giờ đang nhấn **và** lần trước không nhấn" = vừa nhấn |
| `!btn_left_pressed && s_last_btn_l` | "Bây giờ không nhấn **và** lần trước đang nhấn" = vừa thả |
| `s_last_btn_l = btn_left_pressed;` | Nhớ trạng thái cho vòng sau |

**Bảng trạng thái của nút:**

| Đang nhấn? | Lần trước nhấn? | Việc làm |
| --- | --- | --- |
| có | không | `press`: giữ nút trái ở máy tính |
| không | có | `release`: nhả nút trái |
| có | có | không làm gì (đang giữ) |
| không | không | không làm gì |

Máy tính giữ nút trái từ lúc `press` đến lúc `release`, nhờ vậy kéo-thả được.

**Ví dụ bằng số về tràn bộ đếm:** `micros()` là số 32 bit nên tràn sau 2³² µs ≈ 71.6 phút. Giả sử `s_last_loop_us` = 4 294 960 000 và `now_us` vừa quay về 3 704. Phép trừ số không dấu cho 3 704 − 4 294 960 000 + 4 294 967 296 = **11 000 µs**, vẫn đúng. Vì vậy chương trình không sai khi bộ đếm quay vòng.

**Trạng thái trung thực:** nút bấm chưa lắp trên breadboard (NOT_TESTED); chưa có chống dội phím (NOT_IMPLEMENTED).

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** Vì sao không dùng `delay(10)`?
> **Đáp:** `delay(10)` chờ 10 ms **cộng thêm** thời gian xử lý nên chu kỳ dài hơn 10 ms. Bằng chứng trong chính dự án: vòng hiệu chuẩn dùng `delay(10)` cho 200 mẫu mất 2 200 ms chứ không phải 2 000 ms. Cách so `micros()` giữ chu kỳ đo được đúng 10 000 µs (mục 8.1).
> **Hỏi:** `&&` và `!` ở đoạn nút bấm làm gì?
> **Đáp:** Đó là phép phát hiện "cạnh": chỉ khi trạng thái đổi mới gửi lệnh, tránh gửi lặp mỗi 10 ms.
> **Hỏi:** Nhấn nút có bị dội không?
> **Đáp:** Có thể. Nhóm chưa làm chống dội phím và nút chưa lắp trên breadboard, nên ghi là chưa kiểm chứng.

## 12.6. Vùng chết, hệ số khuếch đại và kẹp giá trị (có trong báo cáo nộp, mục 4.4.2)

**Nguồn:** `src/motion_pipeline.cpp` dòng 37–54 và 389–393 (bỏ chú thích).

```
static float apply_deadzone(float val, float low, float high) {
    float abs_val = fabsf(val);
    if (abs_val < low) {
        return 0.0f;
    }
    if (abs_val > high) {
        return (val > 0.0f) ? (abs_val - low) : -(abs_val - low);
    }
    float factor = (abs_val - low) / (high - low);
    return factor * ((val > 0.0f) ? (abs_val - low) : -(abs_val - low));
}

static int8_t clamp_i8(int32_t val) {
    if (val > 127) return 127;
    if (val < -127) return -127;
    return (int8_t)val;
}
...
int32_t dx = (int32_t)roundf( s_cfg.gain_x * omega_horizontal);
int32_t dy = (int32_t)roundf(-s_cfg.gain_y * omega_vertical);
out.delta_x = clamp_i8(dx);
out.delta_y = clamp_i8(dy);
```

**Nói bằng lời:** vận tốc góc nhỏ hơn 0.8 °/s coi là rung tay nên bỏ; lớn hơn thì trừ đi 0.8 và nhân hệ số 2.2 để ra số đơn vị chuột; cuối cùng kẹp trong ±127 vì gói HID chỉ chứa số 8 bit có dấu.

| Dòng code | Ý nghĩa |
| --- | --- |
| `static float apply_deadzone(float val, float low, float high)` | Hàm riêng của file, nhận 3 số thực và trả về một số thực |
| `fabsf(val)` | Trị tuyệt đối của số thực |
| `if (abs_val < low) return 0.0f;` | Dưới 0.8 °/s: kết quả 0 |
| `if (abs_val > high) return ...;` | Trên 1.4 °/s: kết quả là `abs_val − low` (giữ dấu của `val`) |
| `(val > 0.0f) ? (abs_val - low) : -(abs_val - low)` | Toán tử `? :`: dương thì lấy giá trị dương, âm thì đổi dấu |
| `factor = (abs_val - low) / (high - low);` | Đoạn đệm 0.8–1.4: `factor` tăng đều từ 0 lên 1 |
| `return factor * (abs_val - low)` | Nhân thêm một lần `(abs_val − low)` nên kết quả tăng theo **parabol** |
| `clamp_i8(int32_t val)` | Nhận số 32 bit, trả số 8 bit có dấu đã bị kẹp trong ±127 |
| `(int32_t)roundf(gain_x * omega_horizontal)` | Nhân hệ số 2.2, làm tròn gần nhất, ép sang số nguyên 32 bit (đủ rộng, không tràn trước khi kẹp) |
| `-s_cfg.gain_y * omega_vertical` | Có **dấu trừ** vì trục Y màn hình hướng xuống: ngẩng lên (pitch dương) thì dY âm, con trỏ đi lên |

Chú thích trong code ghi "linear ramp" vì hệ số `factor` tăng tuyến tính, nhưng kết quả cuối nhân thêm `(abs_val − low)` nên là đường cong parabol (a − 0.8)² / 0.6, nối liền với đoạn thẳng tại 1.4 °/s.

**Ví dụ bằng số** (gain 2.2):

| ω (°/s) | `apply_deadzone` | × 2.2 | dX sau làm tròn và kẹp |
| --- | --- | --- | --- |
| 0.5 | 0 | 0 | **0** |
| 1.0 | 0.2² / 0.6 = 0.067 | 0.147 | **0** |
| 1.4 | 0.6 | 1.32 | **1** |
| 2.0 | 1.2 | 2.64 | **3** |
| 30 | 29.2 | 64.24 | **64** |
| 60 | 59.2 | 130.24 | 130 bị kẹp xuống **127** |

Nếu **không kẹp**, `(int8_t)130` cho 130 − 256 = **−126**: con trỏ chạy ngược chiều tay.

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** Vì sao có hai ngưỡng 0.8 và 1.4 chứ không chỉ một?
> **Đáp:** Một ngưỡng cứng làm con trỏ giật khựng khi vừa vượt ngưỡng. Đoạn đệm 0.8–1.4 cho đầu ra tăng mượt dần, giống đạp ga từ từ.
> **Hỏi:** Vì sao tính bằng `int32_t` rồi mới kẹp xuống `int8_t`?
> **Đáp:** Tính trên kiểu rộng để không tràn, kiểm tra vượt 127 xong mới ép xuống 8 bit. Kẹp ±127 cùng vai trò với việc giới hạn đầu ra PID trong khoảng ARR của nhóm STM32.
> **Hỏi:** Vì sao dY có dấu trừ?
> **Đáp:** Gốc tọa độ màn hình ở góc trên-trái, Y tăng khi đi xuống; ngẩng tay lên phải cho dY âm.

## 12.7. Bộ lọc bù: khi nào nghe gia tốc kế (có trong báo cáo nộp, mục 4.4.3)

**Nguồn:** `src/motion_pipeline.cpp` dòng 212, 242–256 và 272–273 (rút gọn các dòng lặp lại).

```
float accel_norm = sqrtf(imu->ax * imu->ax + imu->ay * imu->ay + imu->az * imu->az);
...
float e_tilt_x = 0.0f;
float e_tilt_y = 0.0f;
float e_tilt_z = 0.0f;
if (accel_norm > 0.75f && accel_norm < 1.25f) {
    ...
    e_tilt_x = ay_n * vg_z - az_n * vg_y;
    e_tilt_y = az_n * vg_x - ax_n * vg_z;
    e_tilt_z = ax_n * vg_y - ay_n * vg_x;
}
...
const float tilt_correction_rate_s_inv = 2.0f; // s^-1
float wx = (gx_c * RAD_PER_DEG) + (tilt_correction_rate_s_inv * e_tilt_x);
```

**Nói bằng lời:** con quay (gyro) cho tư thế nhanh nhưng lâu dần bị lệch; gia tốc kế biết hướng trọng lực nhưng nhiễu khi vung tay. Firmware lấy gyro làm chính và cộng thêm một lượng nhỏ kéo về phía hướng trọng lực do gia tốc kế đo, **chỉ khi** độ lớn gia tốc gần 1 g (tay không đang vung mạnh).

| Dòng code | Ý nghĩa |
| --- | --- |
| `accel_norm = sqrtf(ax² + ay² + az²)` | Độ lớn vector gia tốc (Pythagoras 3 chiều). Nằm yên ≈ 1 g (đo thật 0.988 g) |
| `float e_tilt_x = 0.0f; ...` | Sai lệch tư thế `e_tilt`, mặc định **0** |
| `if (accel_norm > 0.75f && accel_norm < 1.25f)` | Chỉ khi \|a\| nằm giữa 0.75 g và 1.25 g mới tính `e_tilt` |
| `e_tilt_x = ay_n * vg_z - az_n * vg_y;` | Tích có hướng (cross product) giữa hướng trọng lực **đo** (`ax_n, ay_n, az_n`) và hướng trọng lực **ước lượng** (`vg_x, vg_y, vg_z`). Bằng 0 khi hai hướng trùng nhau, càng lệch càng lớn |
| `const float tilt_correction_rate_s_inv = 2.0f;` | Hệ số K = 2 s⁻¹ (τ = 1/K = 0.5 s) |
| `wx = gx_c * RAD_PER_DEG + K * e_tilt_x` | Vận tốc xoay áp dụng = gyro (đã đổi từ °/s sang rad/s) **cộng** phần kéo về phía gia tốc kế |

**Ví dụ:** nằm yên |a| = 0.988 g, nằm trong khoảng, nên `e_tilt` được dùng để kéo tư thế về đúng. Vung tay mạnh làm |a| = 1.6 g, ngoài khoảng, nên `e_tilt` giữ 0 và `wx` chỉ còn phần gyro; gia tốc kế bị bỏ qua lúc đó vì nó không còn phản ánh đúng hướng trọng lực.

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** Vì sao chỉ nghe gia tốc kế trong khoảng 0.75–1.25 g?
> **Đáp:** Khi tay đứng yên, gia tốc kế chỉ đo trọng lực nên |a| ≈ 1 g. Lệch xa 1 g tức là đang có gia tốc của chuyển động, đo ra không còn đúng hướng trọng lực nên bỏ qua.
> **Hỏi:** Gia tốc kế có sửa được góc yaw không?
> **Đáp:** Không. `e_tilt` là tích có hướng nên không có thành phần dọc theo trục trọng lực, mà xoay yaw chính là xoay quanh trục đó.
> **Hỏi:** `RAD_PER_DEG` để làm gì?
> **Đáp:** Đổi °/s sang rad/s (nhân π/180 ≈ 0.01745), vì công thức cập nhật tư thế dùng radian.

## 12.8. Phát hiện đứng yên, tự chỉnh bias và hiệu chuẩn lúc khởi động

**Nguồn:** `src/motion_pipeline.cpp` dòng 215–228; `firmware.ino` dòng 39–61 và 65 (rút gọn).

```
if (gyro_norm < s_cfg.stat_gyro_thresh && accel_err < s_cfg.stat_accel_thresh) {
    if (s_stat_counter < s_cfg.stat_window_count) {
        s_stat_counter++;
    } else {
        s_is_stationary = true;
        s_bias_x += s_cfg.auto_zero_alpha * gx_c;
        s_bias_y += s_cfg.auto_zero_alpha * gy_c;
        s_bias_z += s_cfg.auto_zero_alpha * gz_c;
    }
} else {
    s_stat_counter = 0;
    s_is_stationary = false;
}
```

```
const int SAMPLES = 200;
float sum_x = 0.0f, sum_y = 0.0f, sum_z = 0.0f;
int valid_count = 0;
for (int i = 0; i < SAMPLES; ++i) {
    imu_data_t data;
    if (imu_readData(&data)) {
        sum_x += data.gx;
        ...
        valid_count++;
    }
    delay(10);
}
float bx = (valid_count > 0) ? (sum_x / valid_count) : 0.0f;
...
motion_setBias(bx, by, bz);
```

**Nói bằng lời:** *Hiệu chuẩn:* lúc bật nguồn, để yên board, lấy trung bình 200 mẫu gyro, kết quả chính là sai số điểm 0 (bias) và được trừ đi ở mọi mẫu sau. *Đứng yên:* nếu gyro và gia tốc đều "lặng" liên tục đủ lâu thì coi là đứng yên, khóa con trỏ, và nhích bias một chút để theo kịp trôi chậm.

| Dòng code | Ý nghĩa |
| --- | --- |
| `gyro_norm < stat_gyro_thresh && accel_err < stat_accel_thresh` | Gyro nhỏ hơn 1.2 °/s **và** \|a\| lệch 1 g chưa tới 0.08 g |
| `s_stat_counter++` | Đếm số mẫu liên tiếp thỏa điều kiện (`++` là cộng 1) |
| `else { s_is_stationary = true; ... }` | Đủ `stat_window_count` = 30 mẫu (≈ 0.3 s) thì kết luận **đứng yên** |
| `s_bias_x += s_cfg.auto_zero_alpha * gx_c;` | Nhích bias thêm 0.2 % phần dư (`auto_zero_alpha` = 0.002). `gx_c` là gyro đã trừ bias, nên đứng yên mà `gx_c` còn khác 0 nghĩa là bias đang lệch |
| `else { s_stat_counter = 0; ... }` | Vi phạm điều kiện dù chỉ một mẫu thì đếm lại từ đầu |
| `for (int i = 0; i < SAMPLES; ++i)` | Lặp 200 lần |
| `sum_x += data.gx;` | Cộng dồn gyro trục X |
| `delay(10);` | Chờ 10 ms giữa hai mẫu |
| `(valid_count > 0) ? (sum_x / valid_count) : 0.0f` | Có mẫu hợp lệ thì lấy trung bình, không có thì dùng 0 (tránh chia cho 0) |
| `motion_setBias(bx, by, bz);` | Cất bias để trừ ở các mẫu sau |

**Ví dụ bằng số:**
- Kết quả hiệu chuẩn lần chạy ngày 01/10: bias = −0.54 / −1.49 / +0.32 °/s (cùng cỡ phép đo độc lập −0.56 / −1.46 / +0.32 °/s).
- Trung bình 200 mẫu giảm nhiễu √200 ≈ 14 lần: từ 0.09 xuống khoảng 0.006 °/s.
- Auto-zero: mỗi mẫu bias nhích 0.002 × `gx_c`. Hằng số thời gian ≈ 1/0.002 = 500 mẫu ≈ 5 s, tức sau 5 s bias đã đi được khoảng 63 % quãng cần chỉnh. Nhích chậm để một cú giật tay ngắn không kéo bias đi sai.
- Thời gian hiệu chuẩn: lý thuyết 200 × 10 ms = 2 000 ms, log thực tế **2 200 ms** (≈ 11 ms mỗi vòng, vì ngoài `delay(10)` còn thời gian đọc I2C và các lệnh khác; nhóm chưa tách riêng phần dôi).

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** Bias là gì, vì sao phải trừ?
> **Đáp:** Là số mà gyro báo ra khi hoàn toàn đứng yên (đo được −1.49 °/s ở trục Y). Không trừ thì con trỏ trôi đều dù tay đứng yên, vì giá trị này lớn hơn cả vùng chết 0.8 °/s.
> **Hỏi:** Sao đứng yên mà còn cập nhật bias?
> **Đáp:** Bias thay đổi chậm theo nhiệt độ. Cập nhật rất chậm (α = 0.002) và chỉ khi chắc chắn đứng yên để không "học" nhầm chuyển động thật thành bias.
> **Hỏi:** Vì sao cần liên tiếp 30 mẫu?
> **Đáp:** Để loại trường hợp tay chỉ khựng lại một khoảnh khắc; cần yên ổn đủ lâu (≈ 0.3 s) mới kết luận đứng yên.

## 12.9. Máy trạng thái nhận diện cử chỉ Flick (có trong báo cáo nộp, mục 4.4.4)

**Nguồn:** `src/gesture_detector.cpp` dòng 58–81 (bỏ chú thích).

```
case SM_GESTURE_ARMED:
    if (a_lateral_g < -s_cfg.peak_accel_thresh) {
        s_state = SM_GESTURE_PEAK_LEFT;
        s_state_start_ms = now_ms;
    } else if (a_lateral_g > s_cfg.peak_accel_thresh) {
        s_state = SM_GESTURE_PEAK_RIGHT;
        s_state_start_ms = now_ms;
    }
    break;

case SM_GESTURE_PEAK_LEFT:
    if (elapsed > s_cfg.max_duration_ms) {
        s_state = SM_GESTURE_ARMED;
    } else if (a_lateral_g > s_cfg.return_accel_thresh && elapsed >= s_cfg.min_duration_ms) {
        s_state = SM_GESTURE_COOLDOWN;
        s_cooldown_start_ms = now_ms;
        return GESTURE_EVENT_FLICK_LEFT;
    }
    break;
```

**Nói bằng lời:** **máy trạng thái** là cách nhớ "đang ở bước nào". Biến `s_state` giữ bước hiện tại; mỗi lần hàm được gọi, chỉ nhánh `case` của bước hiện tại được chạy. Ở đây cử chỉ lắc trái có hai bước: gia tốc vượt ngưỡng về bên trái, rồi bật ngược lại trong khoảng thời gian cho phép.

| Dòng code | Ý nghĩa |
| --- | --- |
| `case SM_GESTURE_ARMED:` | Bước "đã sẵn sàng" (đang giữ Clutch, chờ cú lắc) |
| `a_lateral_g < -s_cfg.peak_accel_thresh` | Gia tốc ngang nhỏ hơn −1.15 g: cú đập sang **trái** |
| `s_state = SM_GESTURE_PEAK_LEFT;` | Chuyển sang bước "đã có đỉnh trái" |
| `s_state_start_ms = now_ms;` | Ghi lại thời điểm vào bước này |
| `case SM_GESTURE_PEAK_LEFT:` | Bước chờ pha hãm. `elapsed` là thời gian đã trôi kể từ lúc vào bước này |
| `elapsed > s_cfg.max_duration_ms` | Quá 450 ms mà không có pha hãm → bỏ cử chỉ, quay về `ARMED` |
| `a_lateral_g > return_accel_thresh && elapsed >= min_duration_ms` | Gia tốc bật ngược quá +0.35 g **và** đã qua tối thiểu 60 ms |
| `s_state = SM_GESTURE_COOLDOWN; return GESTURE_EVENT_FLICK_LEFT;` | Phát sự kiện Flick trái (gửi `MOUSE_BACK`) và nghỉ 350 ms để không bị kích hoạt lặp |
| `break;` | Kết thúc nhánh `case` này |

**Ví dụ theo dòng thời gian** (đang giữ Clutch):

| Thời điểm | `a_lateral_g` | Chuyện gì xảy ra |
| --- | --- | --- |
| 0 ms | −1.30 g | Vượt −1.15 g: chuyển sang `PEAK_LEFT` |
| 40 ms | +0.50 g | Lớn hơn 0.35 g nhưng mới 40 ms (< 60 ms): **chưa tính**, ở lại `PEAK_LEFT` |
| 80 ms | +0.50 g | Đủ điều kiện: phát **FLICK_LEFT**, sang `COOLDOWN` 350 ms |
| (kịch bản khác) 500 ms không có pha hãm | — | Quá 450 ms: về `ARMED`, không phát gì |

Các ngưỡng 1.15 g / 0.35 g / 60–450 ms / 350 ms là **giá trị ban đầu** (HOST_TESTED, chưa tinh chỉnh trên tay người thật). Ý đồ của ngưỡng 60 ms là loại các xung nhiễu quá ngắn.

> [!HOI] Câu hỏi về đoạn code này
> **Hỏi:** Máy trạng thái là gì, vì sao dùng?
> **Đáp:** Là cách lập trình có nhớ "đang ở bước nào" để một hành động gồm nhiều bước theo thời gian (đập rồi hãm) được nhận diện đúng thứ tự.
> **Hỏi:** Vì sao Flick cần hai pha?
> **Đáp:** Cú đập một chiều (va chạm) chỉ có pha đầu. Cử chỉ thật có thêm pha hãm ngược trong 60–450 ms, nên đòi đủ cả hai pha để loại va chạm thụ động.

## 12.11. Trả lời 30 giây khi thầy chỉ vào đoạn code trong báo cáo nộp

Mỗi đoạn có cùng một khuôn: **câu mở đầu** (đoạn này để làm gì), **ba ý** (đi từng bước), **câu chốt bằng số liệu**, rồi **câu thầy hay hỏi tiếp**. Không cần thuộc lòng từng chữ; nhớ khuôn và các con số.

### Đoạn 4.4.1: ghép byte và đổi đơn vị

| Bước | Nói gì |
| --- | --- |
| Mở đầu | "Dạ đoạn này đổi số đo thô 16 bit của cảm biến thành vận tốc góc tính bằng độ trên giây ạ." |
| Ý 1 | "Cảm biến gửi mỗi trục hai byte, byte cao trước, nên em dịch byte cao lên 8 bit rồi OR với byte thấp để ghép lại." |
| Ý 2 | "Em ép sang `int16_t` để hiểu là số có dấu, vì tay xoay ngược chiều thì giá trị âm." |
| Ý 3 | "Rồi chia cho 65.5, vì ở dải ±500 độ/giây datasheet cho 65.5 LSB ứng với 1 độ/giây." |
| Chốt bằng số | "Ví dụ hai byte `0xFF`, `0x38` là −200 LSB, chia ra −3.05 độ/giây ạ." |
| Thầy hỏi tiếp | "Vì sao phải `int16_t`?" → để có số âm (nếu không thì 65 336 → 997 °/s). "Đổi dải đo thì sao?" → phải đổi hằng số chia, nếu không số liệu sai. |

### Đoạn 4.4.2: vùng chết, hệ số và kẹp

| Bước | Nói gì |
| --- | --- |
| Mở đầu | "Dạ đoạn này biến vận tốc góc thành độ dời con trỏ dX, dY ạ." |
| Ý 1 | "Dưới 0.8 độ/giây em bỏ vì là rung tay; từ 0.8 đến 1.4 thì tăng dần theo đường parabol cho con trỏ mượt; trên 1.4 thì trừ đi 0.8." |
| Ý 2 | "Rồi nhân hệ số 2.2 và làm tròn thành số nguyên." |
| Ý 3 | "Hàm `clamp_i8` kẹp trong ±127 vì dX, dY của gói HID là số 8 bit có dấu; dấu trừ ở dy là vì trục Y màn hình hướng xuống." |
| Chốt bằng số | "Xoay 30 độ/giây thì dX = 64 mỗi 10 ms; xoay nhanh quá khoảng 58.5 độ/giây thì bão hòa ở 127 ạ." |
| Thầy hỏi tiếp | "Không kẹp thì sao?" → `(int8_t)130` bằng −126, con trỏ chạy ngược. "Sao có hai ngưỡng?" → một ngưỡng cứng làm giật khựng, hai ngưỡng cho tăng mượt. |

### Đoạn 4.4.3: bộ lọc bù

| Bước | Nói gì |
| --- | --- |
| Mở đầu | "Dạ đoạn này là bộ lọc bù, kết hợp con quay và gia tốc kế để ước lượng độ nghiêng ạ." |
| Ý 1 | "Con quay nhanh nhưng lâu dần bị trôi; gia tốc kế biết hướng trọng lực nhưng bị nhiễu khi vung tay." |
| Ý 2 | "`e_tilt` là độ lệch giữa hướng trọng lực đo và hướng em đang ước lượng. Em chỉ tính khi độ lớn gia tốc nằm trong 0.75 đến 1.25 g; ngoài khoảng đó để bằng 0 nên chỉ dùng con quay." |
| Ý 3 | "Vận tốc xoay áp dụng bằng con quay, đổi ra rad/s, cộng K nhân `e_tilt`, với K = 2 trên giây, tức hằng số thời gian 0.5 giây." |
| Chốt bằng số | "Nằm yên em đo độ lớn gia tốc 0.988 g nên nằm trong khoảng; vung mạnh vượt 1.25 g thì bỏ qua gia tốc kế. Gia tốc kế không sửa được góc yaw ạ." |
| Thầy hỏi tiếp | "Vì sao 0.75–1.25?" → lệch xa 1 g tức đang có gia tốc chuyển động, gia tốc kế không còn đo đúng hướng trọng lực. "`RAD_PER_DEG` để làm gì?" → đổi độ sang radian (π/180). |

### Đoạn 4.4.4: máy trạng thái Flick

| Bước | Nói gì |
| --- | --- |
| Mở đầu | "Dạ đoạn này nhận diện cử chỉ lắc Flick bằng máy trạng thái ạ." |
| Ý 1 | "Biến `s_state` nhớ đang ở bước nào; giữ nút Clutch thì vào trạng thái sẵn sàng `ARMED`." |
| Ý 2 | "Gia tốc ngang vượt −1.15 g thì sang `PEAK_LEFT`; ở đó phải có pha hãm ngược trên +0.35 g trong 60 đến 450 ms thì mới phát Flick trái, tức lệnh Browser Back, rồi nghỉ 350 ms." |
| Ý 3 | "Quá 450 ms mà không có pha hãm thì hủy, quay về `ARMED`." |
| Chốt bằng số | "Cần hai pha để loại va chạm một chiều. Các ngưỡng là giá trị ban đầu, đã chạy qua host test, chưa tinh chỉnh trên người thật; nút chưa lắp nên chưa thử trên phần cứng ạ." |
| Thầy hỏi tiếp | "Máy trạng thái là gì?" → cách nhớ đang ở bước nào để nhận diện hành động nhiều bước theo thời gian. "Vì sao tối thiểu 60 ms?" → để loại các xung nhiễu rất ngắn (ý đồ thiết kế, chưa tinh chỉnh). |

## 12.10. Bài tự kiểm tra đọc code (có đáp án)

| STT | Đề bài | Đáp án |
| --- | --- | --- |
| 1 | `bank = 3` thì giá trị ghi vào thanh ghi 0x7F là bao nhiêu? | (3 & 3) << 4 = 0011 0000b = **0x30** |
| 2 | `bank = 5` (nhập nhầm) thì sao? | 5 & 3 = 1, ghi 0x10 (bank 1): phép `& 0x03` chặn không cho vượt 3 |
| 3 | Ghép `raw[4] = 0x1F`, `raw[5] = 0xA0` ra bao nhiêu g (±4 g)? | 0x1FA0 = 8 096 LSB → 8 096 / 8 192 = **0.988 g** |
| 4 | Gyro `raw` = {0xFF, 0x38} ra bao nhiêu °/s? | −200 LSB → −200 / 65.5 = **−3.05 °/s** |
| 5 | Accel X, `raw` = {0x00, 0x41} ra bao nhiêu g? | 0x0041 = 65 → 65 / 8 192 = **0.0079 g** |
| 6 | `s_last_loop_us` = 4 294 960 000, `now_us` = 3 704 (vừa tràn). Hiệu bằng bao nhiêu, có xử lý vòng này không? | 11 000 µs, ≥ 10 000 nên **có** xử lý |
| 7 | ω = 1.0 °/s thì dX bằng bao nhiêu? | 0.067 × 2.2 = 0.147 → **0** |
| 8 | ω = 45 °/s thì dX bằng bao nhiêu? | (45 − 0.8) × 2.2 = 97.24 → **97** |
| 9 | ω = 70 °/s: dX tính ra, sau kẹp, và nếu không kẹp? | 69.2 × 2.2 = 152.24 → 152; kẹp còn **127**; không kẹp `(int8_t)152` = 152 − 256 = **−104** |
| 10 | `btn_left_pressed` = 1 và `s_last_btn_l` = 1 thì làm gì? | Không làm gì (đang giữ nút) |
| 11 | `accel_norm` = 1.6 g thì `e_tilt` bằng bao nhiêu? | Ngoài [0.75; 1.25] → `e_tilt` giữ **0**, chỉ dùng gyro |
| 12 | `gx_c` = 0.2 °/s liên tục khi đứng yên: mỗi mẫu bias nhích bao nhiêu? | 0.002 × 0.2 = **0.0004 °/s** mỗi mẫu |
| 13 | Vòng hiệu chuẩn 200 mẫu, `delay(10)`: thời gian lý thuyết và log thực? | 2 000 ms lý thuyết; log **2 200 ms** |
| 14 | `a_lateral_g` = −1.3 g rồi sau 40 ms là +0.5 g: có phát Flick chưa? | **Chưa** (mới 40 ms < 60 ms, còn ở `PEAK_LEFT`) |

# PHỤ LỤC A. NGÂN HÀNG CÂU HỎI NGẮN (THEO 6 KIỂU HỎI)

## A.1. Kiểu 1 — "Dùng để làm gì trong ứng dụng này?"

| Câu hỏi | Trả lời ngắn | Mục |
| --- | --- | --- |
| ADC dùng để làm gì? | Chỉ đo điện áp pin (GPIO34, ADC1_CH6), chưa làm firmware | 4.3 |
| Cảm biến đọc bằng ADC à? | Không: ADC nằm trong ICM, ESP32 đọc số qua I2C | 4.2 |
| Gyro dùng để làm gì, accel dùng để làm gì? | Gyro: vận tốc góc → di chuột. Accel: hướng trọng lực (tư thế) + cử chỉ Flick | 1, 9 |
| Nút clutch để làm gì? | Khóa con trỏ khi đổi tư thế tay; bật nhận cử chỉ; thả ra thì recenter | 1.4 |
| Timer dùng để làm gì? | Không dùng timer phần cứng; esp_timer qua `micros()` tạo nhịp 10 ms và dt | 8.1 |
| UART để làm gì? | In log chẩn đoán; không tham gia điều khiển chuột | 8.2 |
| Cầu chia áp để làm gì? | Hạ 4.2 V xuống 2.1 V cho vừa dải đo chính xác của ADC | 4.3.2 |
| Tụ 100 nF ở chân ADC để làm gì? | Cấp điện tích cho tụ lấy mẫu SAR, lọc nhiễu | 4.3.2 |

## A.2. Kiểu 2 — Chuỗi đại lượng, "tại sao em chắc"

| Câu hỏi | Trả lời ngắn | Mục |
| --- | --- | --- |
| Xoay 30 °/s thì dX bao nhiêu? | round(2.2 × 29.2) = 64 mỗi 10 ms | 1.2 |
| Đứng yên có trôi không? | Nhiễu 0.09 °/s ≪ vùng chết 0.8 °/s; bias được trừ và tự cập nhật | 4.2.3, 9 |
| 1 g là bao nhiêu LSB? | 8 192 ở ±4 g (firmware); 16 384 ở ±2 g (probe). Đo được 8 097 LSB = 0.988 g | 4.2 |
| Sao đo ra 0.988 g, không phải 1 g? | Sai số zero-g và độ nhạy, trong dung sai ±50 mg, ±0.5 % của datasheet | 4.2.3 |
| Nhiệt độ bao nhiêu? | Die 34.6 °C (không phải nhiệt độ phòng) | 4.2.3 |
| Pin 3.7 V thì ADC thấy bao nhiêu? | 1.85 V ở chân GPIO34 | 4.3.2 |
| Tại sao gain 2.2? | Giá trị ban đầu cho cảm giác 1:1, chưa tinh chỉnh; không khẳng định pixel | 1.2 |

## A.3. Kiểu 3 — Cấu hình tới bit

| Câu hỏi | Trả lời ngắn | Mục |
| --- | --- | --- |
| Địa chỉ I2C? Tại sao 0xD0? | 0x68 (AD0 = 0); 0x68 << 1 = 0xD0 (ghi), 0xD1 (đọc) | 5.1 |
| Chọn bank thế nào? | Ghi 0x7F, bit [5:4]; bank 2 = 0x20 | 5.2 |
| PWR_MGMT_1 = 0x01 nghĩa là gì? | SLEEP = 0, CLKSEL = 001 (tự chọn PLL) | 6 |
| 0x1B của GYRO_CONFIG_1? | DLPFCFG 011, FS_SEL 01 (±500), FCHOICE 1 | 6 |
| 400 kHz cấu hình ở đâu? | I2C_SCL_LOW/HIGH_PERIOD (đếm chu kỳ APB 80 MHz): tổng ≈ 200 chu kỳ | 5.3 |
| Chọn suy hao ADC ở đâu? | SENS_SAR_ATTEN1_REG, 2 bit/kênh; kênh 6 = bit [13:12] | 4.3.1 |
| Bật pull-up bằng bit nào? | FUN_WPU trong IO_MUX_x_REG | 7.1 |
| LED GPIO32 ghi bit nào? | Bit 0 của GPIO_OUT1_W1TS (bật) / W1TC (tắt) | 7.2 |

## A.4. Kiểu 4 — Số bit, giá trị lớn nhất, bão hòa

| Câu hỏi | Trả lời ngắn | Mục |
| --- | --- | --- |
| ADC ICM mấy bit? Dải số? | 16 bit bù hai: −32 768 … +32 767 | 4.2.2 |
| ADC ESP32 mấy bit, bao nhiêu mức? | 12 bit, 4 096 mức (0–4095) | 4.3.1 |
| Ghi 255 vào GYRO_SMPLRT_DIV được không? | Được: ODR = 4.39 Hz, quá chậm cho chuột | 4.2.4 |
| Ghi 0xFFFF được không? | Không: thanh ghi 8 bit (gyro), 12 bit tách 2 byte (accel) | 4.2.4 |
| dX vượt 127 thì sao? | Bị kẹp ở 127; không kẹp thì tràn int8 và đổi dấu | 1.2 |
| Xoay nhanh hơn bao nhiêu thì bão hòa? | ≈ 58.5 °/s → 12 700 count/s | 1.2 |
| Đọc I2C tốn bao lâu? | 438 µs (đo), 4.4 % chu kỳ 10 ms | 5.5 |
| I2C chậm nhất được bao nhiêu? | Trường 14 bit → ≈ 2.4 kHz | 5.3 |

## A.5. Kiểu 5 — Đào sâu khái niệm

| Câu hỏi | Trả lời ngắn | Mục |
| --- | --- | --- |
| LSB là gì? | Bước nhỏ nhất của số ADC; 1 LSB gyro = 0.0153 °/s ở ±500 | 4.2.2 |
| DLPF 51.2 Hz có phải tần số lấy mẫu? | Không: là tần số cắt 3 dB; tần số lấy mẫu là ODR 102.27 Hz | 6 |
| Baud là gì? | Số ký hiệu/giây; UART 8N1 115 200 baud = 11 520 byte/s | 8.2 |
| Open-drain là gì? | Chân chỉ kéo xuống 0; mức 1 do trở kéo | 5.1, 3.2 |
| Sao không dùng SPI? | I2C đủ nhanh (4.4 % bus), ít dây hơn | 2.2 |
| Tốc độ ngõ ra trên ESP32? | Không có OSPEEDR; có FUN_DRV (drive strength) | 7 |
| Mạch sạc có ADC không? | Không: bộ so sánh + điện áp chuẩn (TP4056 4.2 V, DW01A 2.4/4.3 V, MT3608 FB 0.6 V) | 4.1 |
| Tại sao không tích phân kép? | Offset 11.6 mg → sai 5.7 cm sau 1 s, 5.7 m sau 10 s | 1.3 |
| Vector trọng lực chỉ xuống đất, làm sao chip biết hướng? | Chip không "biết" hướng đất; nó đo thành phần trọng lực trên 3 trục của chính thiết bị. Nằm phẳng thì AZ ≈ +1 g, AX và AY ≈ 0; nghiêng thì giá trị chuyển sang trục khác | 9.3 |
| Bộ lọc bù có chạy khi đang giữ Clutch không? | Có: các bước lọc chạy mỗi chu kỳ 10 ms trước nhánh Clutch; Clutch chỉ khóa dX, dY và bật nhận cử chỉ | 9.3 |

## A.6. Kiểu 6 — Đọc hiểu code

| Câu hỏi | Trả lời ngắn | Mục |
| --- | --- | --- |
| `(bank & 0x03) << 4` làm gì? | `& 0x03` giữ 2 bit thấp (bank 0–3); `<< 4` đặt vào bit [5:4] của thanh ghi 0x7F. Bank 2 thành 0x20 | 12.2 |
| `#define` khác biến ở đâu? | Thay chữ trước khi biên dịch, không chiếm RAM, không có kiểu | 12.1 |
| Vì sao ghi thanh ghi xong còn đọc lại? | Để chắc chip nhận đúng; có giá trị lệch thì `imu_init` trả `false`, chương trình báo `[FATAL]` | 12.1 |
| `endTransmission(false)` khác `endTransmission()`? | `false` không phát STOP mà phát Repeated START để chuyển sang đọc | 12.3 |
| `((uint16_t)raw[4] << 8) \| raw[5]` làm gì? | Ghép byte cao (dịch lên nửa trên) với byte thấp thành số 16 bit; `(int16_t)` hiểu là số có dấu | 12.4 |
| Vì sao chia cho 8 192.0f? | Độ nhạy ±4 g: 8 192 LSB ứng với 1 g. Đo thật 8 096 LSB = 0.988 g | 12.4 |
| Vì sao `now_us - s_last_loop_us` vẫn đúng khi `micros()` tràn? | Phép trừ số 32 bit không dấu tự quay vòng: 3 704 − 4 294 960 000 cho 11 000 µs | 12.5 |
| `btn && !last` nghĩa là gì? | Vừa nhấn (nay nhấn, trước không nhấn); chỉ gửi `press` một lần khi trạng thái đổi | 12.5 |
| ω = 1.0 °/s thì dX bằng mấy? | 0.067 × 2.2 = 0.147, làm tròn thành 0 | 12.6 |
| Vì sao `dy` có dấu trừ? | Trục Y màn hình hướng xuống; ngẩng tay lên phải cho dY âm | 12.6 |
| Vì sao kẹp ±127, không kẹp thì sao? | Gói HID là `int8_t`; `(int8_t)130` bằng −126, con trỏ chạy ngược | 12.6 |
| Vì sao chỉ nghe gia tốc kế khi 0.75–1.25 g? | Lệch xa 1 g tức đang có gia tốc chuyển động, nên accel không còn đo đúng hướng trọng lực | 12.7 |
| `s_bias_x += alpha * gx_c` làm gì? | Nhích bias 0.2 % phần dư mỗi mẫu khi đứng yên để theo kịp trôi chậm | 12.8 |
| Máy trạng thái Flick hoạt động thế nào? | ARMED → vượt 1.15 g (PEAK) → hãm ngược quá 0.35 g trong 60–450 ms → phát Flick, nghỉ 350 ms | 12.9 |

# PHỤ LỤC B. MƯỜI CÂU DỄ MẤT ĐIỂM NHẤT VÀ CÁCH NÓI ĐÚNG TRẠNG THÁI

## B.1. Mười câu thầy dễ gài nhất (đã gom từ buổi ôn luyện)

Mỗi câu trả lời được rút gọn để nói trong 20–30 giây; số mục là nơi có phần giải thích đầy đủ.

| STT | Câu thầy có thể hỏi | Trả lời mẫu | Mục |
| --- | --- | --- | --- |
| 1 | ADC dùng để làm gì? Cảm biến ICM đọc bằng ADC à? TP4056 có ADC không? | ADC1 của ESP32 chỉ để đo điện áp pin (GPIO34, qua cầu chia 1:2) và firmware chưa làm phần này. Chuyển động được số hóa bởi ADC 16 bit bên trong ICM-20948, ESP32 nhận số qua I2C. TP4056, DW01A, MT3608 không có ADC; chúng dùng mạch analog (bộ so sánh hoặc khuếch đại sai số) so với điện áp chuẩn nội | 4.1 |
| 2 | Bật LED ở GPIO32 thì ghi bit nào của thanh ghi nào? | Bit 0 của `GPIO_OUT1_W1TS_REG` (0x3FF44014) để bật, `GPIO_OUT1_W1TC_REG` (0x3FF44018) để tắt, vì `GPIO_OUT_REG` chỉ chứa GPIO0–31. LED chưa lắp trên breadboard | 7.2 |
| 3 | Chỉ có 1 ESP32 thì tranh chấp với ai mà dùng Repeated START? | Datasheet §6.3 quy định trình tự đọc có Sr và nhóm làm đúng trình tự đó. Sr giữ bus ở trạng thái bận nên master khác không chen vào được; hiện chỉ có 1 master nên lợi ích này chưa thể hiện | 5.1 |
| 4 | dX tính ra 200 thì sao? Accel có sửa được yaw không? | Kẹp về 127; nếu không kẹp, ép sang `int8_t` sẽ tràn thành −56 và con trỏ chạy ngược. Accel không sửa được yaw vì trọng lực song song với trục quay thẳng đứng | 1.2, 9.1 |
| 5 | Chuột đã chạy ổn trên máy tính chưa? Gói tin dài mấy byte? | Gói 5 byte: [Nút, dX, dY, Wheel, Pan]. Firmware phát quảng bá `AirMouse-ESP32`, nhưng nhóm chưa ghép nối với máy tính lần nào (NOT_TESTED) | 10, 11 |
| 6 | Bộ lọc bù hoạt động thế nào? Khi nào bỏ accel? | Gyro cho tư thế tức thời, accel kéo từ từ về đúng hướng trọng lực với K = 2 s⁻¹ (τ = 0.5 s), chạy mỗi 10 ms. Chỉ nghe accel khi 0.75 g < \|a\| < 1.25 g | 9.1, 9.3 |
| 7 | Cầm nghiêng 45° mà lắc ngang thì con trỏ vẫn chạy ngang màn hình, nhờ đâu? | Nhờ chiếu theo tư thế tham chiếu: vector trọng lực chụp lúc recenter làm trục dọc; dX lấy từ vận tốc góc dọc theo trục đó (yaw), dY từ trục ngang vuông góc | 1.2, 9.3 |
| 8 | Nút Clutch để làm gì? Flick vì sao phải 2 pha? | Clutch như nhấc chuột quang: giữ thì dX = dY = 0, thả thì căn lại tâm. Flick cần vượt 1.15 g rồi hãm ngược quá 0.35 g trong 60–450 ms để loại va chạm một chiều | 1.4, 9.2 |
| 9 | Tại sao tính 343 µs mà đo 438 µs? | 343 µs là 137 chu kỳ SCL ở 400 kHz; phần dôi khoảng 100 µs gần như không đổi theo tốc độ bus (≈ 101 µs ở 100 kHz) nên là chi phí phần mềm của driver | 5.5 |
| 10 | Tách chân B− và OUT− của TP4056 để làm gì? | Cực âm cell chỉ vào B−, mass hệ thống lấy từ OUT−; giữa hai chân là MOSFET bảo vệ do DW01A điều khiển. Nối tắt thì mất bảo vệ quá xả (dưới 2.40 V) và ngắn mạch | 3.2, 4.1 |

## B.2. Cách nói đúng trạng thái (tránh nói quá)

| Hạng mục | Nên nói | Không nên nói |
| --- | --- | --- |
| Bluetooth với máy tính | "Firmware phát quảng bá `AirMouse-ESP32`; nhóm chưa ghép nối với máy tính." | "Chưa test dài hạn" (hàm ý đã test ngắn hạn); "chuột mượt, ổn định 100 %" |
| Repeated START | "Nhóm làm đúng theo trình tự datasheet mô tả." | "Gặp STOP thì cảm biến tự reset con trỏ về 0x00" (datasheet không nói); "tuân thủ 100 %" |
| Đo pin | "Đã thiết kế cầu chia 100k/100k; firmware chưa có code đọc ADC." | "Đã đo được điện áp pin" |
| Nút bấm, LED | "Chưa lắp trên breadboard; các thuật toán liên quan đã chạy trong host test." | "Đã kiểm chứng nút và LED trên phần cứng" |
| Điện áp cấp ICM | "VDD cho phép 1.71–3.6 V nhưng VDDIO chỉ 1.71–1.95 V; nối thẳng 3.3 V mới kiểm chứng ngắn hạn trên đúng module của nhóm." | "An toàn tuyệt đối"; "đúng datasheet" |
| Độ trễ của bộ lọc DLPF | "Datasheet chỉ công bố tần số cắt và băng thông nhiễu (73.3 Hz và 68.8 Hz)." | Nêu con số độ trễ theo ms |
| Số đo I2C | "438 µs, đo 1 000 lần trên board của nhóm, 0 lỗi." | "Luôn ổn định", "không bao giờ lỗi" |

# PHỤ LỤC C. NGUỒN THAM KHẢO

| Tài liệu | Phần đã dùng |
| --- | --- |
| TDK InvenSense ICM-20948 Datasheet DS-000189 rev 1.3 | §3.1 Gyro (độ nhạy, ZRO ±5 °/s, nhiễu 0.015 °/s/√Hz); §3.2 Accel (8 192 LSB/g, zero-g ±50 mg, 230 µg/√Hz); §3.4 nguồn (VDD 1.71–3.6 V, VDDIO 1.71–1.95 V); §3.7 Table 9 (VDDIO tối đa 2.5 V); Table 16/18 DLPF; §8.31 công thức nhiệt độ (333.87 LSB/°C) |
| Espressif ESP32 Series Datasheet v5.3 | Table 4-3 (DNL ±7, INL ±12 LSB), Table 4-4 (dải đo theo suy hao, ±6 % khi không hiệu chuẩn), Table 5-3 (pull-up 45 kΩ, IOH 40 mA, IOL 28 mA) |
| Espressif ESP32 Technical Reference Manual v5.8 | Ch. 6 IO_MUX/GPIO (GPIO_OUT1_W1TS, FUN_DRV, FUN_WPU); Ch. 21 I2C (I2C_CTR_REG, SCL_LOW/HIGH_PERIOD, op_code); Ch. 31 SAR ADC (SENS_SAR_READ_CTRL, ATTEN1, MEAS_START1) |
| NanJing Top Power TP4056 | V_FLOAT 4.137–4.263 V, V_TRIKL 2.9 V, I_BAT = 1200 / R_PROG |
| Fortune DW01A | V_OCP 4.30 V, V_ODP 2.40 V, V_OI1 150 mV |
| Aerosemi MT3608 | FB 0.6 V (0.588–0.612), 1.2 MHz |
| Log thực nghiệm | `raw_logs/bench_2026-10-01_icm20948_timing_noise_run2.log` (SHA-256 89bdae09c58ea1ca0cff784524d76914d18ab2e09a627d3f62defbe44a3dedc4); `raw_logs/main_firmware_boot_com3_2026-10-01.log` (fb5a3cea2a59484cd17a0e22ff28d5e2912e534b9cb6043653dfb1296437a71b) |
