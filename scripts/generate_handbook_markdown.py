# -*- coding: utf-8 -*-
"""
scripts/generate_handbook_markdown.py
The single master generator for deliverables/CAM_NANG_KIEN_THUC_AIR_MOUSE_MIDTERM.md
Single Source of Truth for the Air Mouse Midterm Study Guide / Handbook.
"""

import os
import sys

def get_p0():
    return r"""# PHẦN 0 — NHỮNG GÌ PHẢI HỌC TRONG 2 NGÀY (QUICK DEFENSE CORE)

Cẩm nang 20 câu hỏi cốt lõi bao quát toàn bộ đề tài, kèm câu trả lời trực diện (15–30 giây), công thức / bitfield trọng tâm và câu hỏi bẫy cần phòng tránh cho buổi bảo vệ giữa kỳ:

---

## NHÓM 1: HỆ THỐNG & VI ĐIỀU KHIỂN ESP32 (CÂU 1–5)

### Câu 1: Bản chất kỹ thuật cốt lõi và nguyên lý hoạt động của đề tài Air Mouse
1. **Quick Answer**: Thiết bị trỏ tương đối điều khiển theo tốc độ xoay (Relative Rate-Control), dùng ESP32 và ICM-20948 qua BLE HID. Vận tốc góc xoay cổ tay ($\omega$) từ Gyroscope được ánh xạ trực tiếp thành độ dịch chuyển con trỏ ($\Delta X, \Delta Y$). Gia tốc kế neo Roll/Pitch qua bộ lọc bù Quaternion 6 trục, nhận diện đứng yên chống trôi và bắt cử chỉ Flick.
2. **Công thức / Bitfield phải nhớ**:
   $$\Delta X = \text{roundf}(K_x \cdot \omega_{\text{horizontal}}), \quad \Delta Y = \text{roundf}(-K_y \cdot \omega_{\text{vertical}}); \quad \text{HID 5B: } [Buttons, dX, dY, Wheel, Pan]$$
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Chuột bay có tracking vị trí 3D VR không?"
   * *Cách né*: Tuyệt đối không nhận tracking 3D hay tích phân 2 lần gia tốc kế. Khẳng định đây là chuột trỏ 2D theo vận tốc xoay tương đối.

---

### Câu 2: Vì sao chọn ESP32 Classic thay vì STM32 và kiến trúc CPU thực tế
1. **Quick Answer**: ESP32 Classic tích hợp sẵn BLE 4.2 trên chip, CPU Xtensa LX6 lõi kép 32-bit 240 MHz và 520 KB SRAM dồi dào, loại bỏ module Bluetooth rời ngoài (như HC-05 hay nRF24L01). STM32F1/F4 không có BLE tích hợp, làm tăng diện tích PCB 1 lớp và số linh kiện. CPU là Xtensa LX6, không phải ARM.
2. **Công thức / Bitfield phải nhớ**:
   Xtensa LX6 32-bit dual-core, 240 MHz, 520 KB SRAM; BLE HID 2.4 GHz không dây.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "ESP32 dùng nhân vi xử lý ARM Cortex-M đúng không?"
   * *Cách né*: Khẳng định ESP32 dùng nhân Xtensa Dual-Core 32-bit LX6 của Tensilica/Cadence, không phải ARM.

---

### Câu 3: Các chân Strapping Pins trên ESP32 và quy tắc an toàn phần cứng
1. **Quick Answer**: Các chân strapping gồm GPIO0, GPIO2, GPIO12, GPIO15, được chốt mức logic tại cạnh lên Reset (CHIP_PU) để cấu hình boot (nạp UART, điện áp Flash SPI). Các chân này vẫn có thể dùng làm I/O nếu bảo đảm mức logic khi khởi động, nhưng đề tài chủ động tránh nút bấm trên các chân này để loại bỏ rủi ro boot failure khi người dùng giữ nút lúc bật nguồn.
2. **Công thức / Bitfield phải nhớ**:
   GPIO0: LOW = UART bootloader, HIGH = Flash boot; GPIO12: áp Flash SPI (1.8V vs 3.3V); GPIO6–11: cấm dùng vì nối Flash SPI nội.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Các chân strapping có hoàn toàn cấm sử dụng trong mạch không?"
   * *Cách né*: Vẫn dùng làm I/O được nếu bảo đảm mức logic lúc boot, nhưng tránh nối nút bấm; không nói 'hoàn toàn không thể sử dụng'.

---

### Câu 4: ICM-20948 là 9-DOF, vì sao firmware Tuần 5 chỉ kích hoạt 6 trục?
1. **Quick Answer**: Chuột chỉ cần điều khiển tương đối trên màn hình 2D. Môi trường phòng học nhiều nhiễu từ (khung sắt bàn, loa, nguồn xung) làm từ kế AK09916 dễ méo nếu chưa hiệu chuẩn phức tạp. Nhóm tắt từ kế để tiết kiệm pin, giảm tải I2C và tránh giật con trỏ. Trục Yaw trôi chậm được bù bằng dead-zone và phím Clutch/Recenter.
2. **Công thức / Bitfield phải nhớ**:
   Đọc burst 12 byte (`0x2D`–`0x38`) Bank 0. Không bật mạch I2C Master nội (`I2C_MST_EN = 0`).
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Không có từ kế thì trục Yaw trôi góc, xử lý ra sao?"
   * *Cách né*: Chuột điều khiển theo vận tốc góc tức thời ($\omega_z$), không cần hướng Bắc tuyệt đối; góc Yaw tương đối được đặt lại qua phím Clutch/Recenter.

---

### Câu 5: Phân tầng kiến trúc phần mềm và dẫn chứng Assembly Xtensa LX6
1. **Quick Answer**: Dự án không lập trình bằng Assembly. Toàn bộ firmware viết bằng C/C++ trên nền Arduino / ESP-IDF, biên dịch bởi `xtensa-esp32-elf-g++`. Thư viện `Wire.h` gọi driver ESP-IDF ghi dữ liệu vào thanh ghi MMIO. Dẫn chứng hàm `imu_selectBank` tại địa chỉ `0x400d22f0`: `entry a1, 32`, `movi a11, 104`, `call8 TwoWire::beginTransmission`, `movi a11, 127`, `call8 TwoWire::write`, `retw.n`.
2. **Công thức / Bitfield phải nhớ**:
   Kiến trúc Xtensa LX6 Register Window xoay 8 thanh ghi (`call8`), địa chỉ 32-bit.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Em dùng lệnh Assembly nào để phát tín hiệu START trên bus I2C?"
   * *Cách né*: Không viết Assembly trực tiếp; START do phần cứng I2C Controller thực thi qua thanh ghi MMIO trong driver C/C++.

---

## NHÓM 2: GIAO THỨC I2C & THANH GHI CẢM BIẾN ICM-20948 (CÂU 6–10)

### Câu 6: Địa chỉ I2C 0x68 và phân biệt với byte bus ghi 0xD0 / đọc 0xD1
1. **Quick Answer**: Địa chỉ logic 7-bit là `0x68` (`0b1101000`) khi AD0 nối GND (nối VDDIO là `0x69`). Trên bus vật lý, byte truyền gồm 7 bit địa chỉ kèm bit R/W (0: Ghi, 1: Đọc). Byte xuất hiện trên bus khi ghi là `0xD0` (`(0x68 << 1) | 0`), khi đọc là `0xD1` (`(0x68 << 1) | 1`).
2. **Công thức / Bitfield phải nhớ**:
   $$\text{Write} = (0\text{x}68 \ll 1) \mid 0 = 0\text{xD0}; \quad \text{Read} = (0\text{x}68 \ll 1) \mid 1 = 0\text{xD1}$$
   Code Arduino: truyền `0x68` vào `Wire.beginTransmission(0x68)`, thư viện tự dịch bit.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Bắt được byte 0xD0 trên bus, vậy địa chỉ cảm biến là 0xD0?"
   * *Cách né*: `0xD0` là bus byte 8-bit. Địa chỉ cảm biến là 7-bit (`0x68`). Không truyền `0xD0`/`0xD1` vào `Wire.beginTransmission()`.

---

### Câu 7: Cấu trúc Open-Drain và điện trở kéo lên trên bus I2C
1. **Quick Answer**: Chân SDA/SCL trên ESP32 và ICM-20948 đều là cực máng để hở (Open-Drain). Transistor bên trong chỉ có thể kéo dây xuống GND ($0\,\text{V}$), không thể tự xuất mức cao. Bắt buộc có điện trở kéo pull-up lên nguồn ($3.3\,\text{V}$ hoặc $1.8\,\text{V}$) để đưa đường dây về mức HIGH logic khi các bên thả nổi.
2. **Công thức / Bitfield phải nhớ**:
   Cấu trúc Wired-AND. Trở kéo: $10\,\text{k}\Omega$ onboard module WCMCU-20948 lên $3.3\,\text{V}$.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Cấu hình chân ESP32 thành Push-Pull cho I2C SDA được không?"
   * *Cách né*: Push-Pull gây ngắn mạch chập nguồn nếu Master xuất HIGH ($3.3\,\text{V}$) trong khi Slave kéo LOW ($0\,\text{V}$) ở xung ACK.

---

### Câu 8: Đấu nối trực tiếp ESP32 3.3V với module WCMCU-20948 và ranh giới với datasheet raw IC
1. **Quick Answer**: Module WCMCU-20948 được đấu nối trực tiếp ở mức $3.3\,\text{V}$ với ESP32 (VCC $\rightarrow$ 3V3, GND $\rightarrow$ GND, SDA $\rightarrow$ GPIO21, SCL $\rightarrow$ GPIO22, NCS $\rightarrow$ 3V3, AD0 $\rightarrow$ GND, FSY $\rightarrow$ GND). Mạch hoạt động thành công trên đúng module WCMCU-20948 và ESP32 mà nhóm đang sở hữu (100/100 lần đọc WHO_AM_I=0xEA thành công trong phép thử ngắn hạn, đọc lại 4 thanh ghi vật lý chuẩn xác). Nhóm đã loại bỏ hoàn toàn BSS138 và LDO 1.8V giúp đơn giản hóa mạch và giảm giá thành BOM xuống 153.000 VNĐ.
2. **Công thức / Bitfield phải nhớ**:
   Trở kéo $10\,\text{k}\Omega$ onboard module kéo lên $3.3\,\text{V}$; I2C Fast-Mode $400\,\text{kHz}$; địa chỉ 7-bit $0\text{x}68$ (AD0=GND); WHO_AM_I = $0\text{x}EA$.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Datasheet IC ICM-20948 ghi VDDIO tối đa 1.95V, tại sao nhóm nối trực tiếp 3.3V?"
   * *Cách né*: Thừa nhận minh bạch: Theo datasheet TDK DS-000189 §3.4, dải hoạt động của IC raw ICM-20948 là $V_{\text{DD}} = 1.71\text{--}3.6\,\text{V}$ nhưng $V_{\text{DDIO}} = 1.71\text{--}1.95\,\text{V}$; giới hạn tuyệt đối (§3.7, Table 9) của $V_{\text{DDIO}}$ là $2.5\,\text{V}$. Tuy nhiên trên module breakout thương mại WCMCU-20948, mạch đã được thử nghiệm thực tế chạy trực tiếp ở $3.3\,\text{V}$ và đạt kết quả kiểm thử Bring-up hoàn hảo ngắn hạn trên phần cứng nhóm sở hữu. Nhóm xác nhận đây là độ lệch kỹ thuật trên mẫu thử và có rủi ro tiềm ẩn về độ bền lâu dài chưa kiểm chứng; không khẳng định "an toàn tuyệt đối" hay "tuân thủ 100% datasheet raw IC".

---

### Câu 9: Kiến trúc 4 User Bank của ICM-20948 và thanh ghi REG_BANK_SEL (0x7F)
1. **Quick Answer**: Không gian thanh ghi 512 byte chia làm 4 User Bank (0, 1, 2, 3), trong đó khoảng 80–100 thanh ghi hoạt động. Muốn truy xuất thanh ghi ở Bank nào, Master ghi giá trị chọn Bank vào `REG_BANK_SEL` tại địa chỉ cố định `0x7F` (có mặt trên cả 4 Bank). Bank 0: dữ liệu raw, WHO_AM_I, nguồn; Bank 1: bias; Bank 2: cấu hình gyro/accel/ODR; Bank 3: I2C master nội.
2. **Công thức / Bitfield phải nhớ**:
   Tại địa chỉ `0x7F`: Ghi `0x00` $\rightarrow$ Bank 0; `0x10` $\rightarrow$ Bank 1; `0x20` $\rightarrow$ Bank 2; `0x30` $\rightarrow$ Bank 3.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Đang ở Bank 0 mà ghi vào địa chỉ 0x01 để cấu hình Gyro thì sao?"
   * *Cách né*: Dữ liệu ghi nhầm vào `0x01` của Bank 0, không tác động đến `GYRO_CONFIG_1` ở Bank 2, làm cấu hình dải đo không có tác dụng.

---

### Câu 10: Ba thanh ghi cấu hình cốt lõi: PWR_MGMT_1, GYRO_CONFIG_1, ACCEL_CONFIG
1. **Quick Answer**: Gồm: `PWR_MGMT_1` (Bank 0, `0x06`) ghi `0x01` thoát ngủ và chọn PLL clock; `GYRO_CONFIG_1` (Bank 2, `0x01`) ghi `0x1B` bật DLPF (3dB BW 51.2 Hz) và chọn dải $\pm 500^{\circ}/\text{s}$ (độ nhạy 65.5 LSB/(°/s)); `ACCEL_CONFIG` (Bank 2, `0x14`) ghi `0x1B` theo Table 18 TDK DS-000189 bật DLPF (3dB BW 50.4 Hz, NBW 68.8 Hz) lọc dao động/nhiễu cao tần trong tín hiệu gia tốc (DLPF cảm biến không thay thế chống rung phím bấm bằng phần mềm) và chọn dải $\pm 4g$ (8192 LSB/g). Trạng thái: `PHYSICAL_READBACK_VERIFIED / BENCH_VERIFIED_ON_OWNED_MODULE` (Firmware chính đọc lại 4 thanh ghi vật lý thành công: PWR_MGMT_1=0x01, GYRO_CONFIG_1=0x1B, ACCEL_CONFIG=0x1B, SMPLRT_DIV=10 trên đúng phần cứng nhóm sở hữu).
2. **Công thức / Bitfield phải nhớ**:
   `PWR_MGMT_1` = `0x01`; `GYRO_CONFIG_1` = `0x1B`; `ACCEL_CONFIG` = `0x1B`.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Nhóm đã đọc lại các thanh ghi này trên cảm biến thật và kết luận PASS chưa?"
   * *Cách né*: Báo cáo trung thực: mới xác nhận logic trên mô hình mock register của host test, chưa chạy readback trên cảm biến vật lý.

---

## NHÓM 3: TOÁN HỌC & XỬ LÝ TÍN HIỆU CHUYỂN ĐỘNG (CÂU 11–15)

### Câu 11: Tại sao không dùng gia tốc kế tích phân 2 lần tìm vị trí chuột?
1. **Quick Answer**: Do sai số lệch tĩnh (bias $\epsilon$) và nhiễu của gia tốc kế MEMS. Tích phân lần 1 ra vận tốc ($v = v_0 + \epsilon t$). Tích phân lần 2 ra quãng đường ($s = s_0 + v_0 t + \frac{1}{2}\epsilon t^2$), sai số bùng nổ theo $t^2$. Sau vài giây, sai số vị trí lên hàng mét, con trỏ trôi mất khỏi màn hình dù chuột đặt yên.
2. **Công thức / Bitfield phải nhớ**:
   $$s(t) = s_0 + v_0 t + \frac{1}{2}\epsilon t^2 \quad (\text{Sai số bùng nổ theo } t^2)$$
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Bộ lọc Kalman có triệt tiêu được sai số tích phân 2 lần không?"
   * *Cách né*: Kalman không thể cứu nếu thiếu mốc vị trí tuyệt đối bên ngoài. Dùng Gyroscope đo vận tốc góc ($\omega$), nhân Gain ra pixel mà không cần tích phân.

---

### Câu 12: Đọc burst 12 byte thô và ghép số nguyên bù 2 16-bit
1. **Quick Answer**: ESP32 đọc burst 12 byte từ `0x2D` đến `0x38` Bank 0 trong 1 giao dịch I2C (`ACCEL_X/Y/Z` và `GYRO_X/Y/Z`). Burst read giảm overhead gửi lại địa chỉ so với 6 giao dịch rời (mức tiết kiệm cụ thể chưa đo trên phần cứng). Ghép byte bù 2 16-bit: `raw = (int16_t)(((uint16_t)buf[high] << 8) | buf[low])`, dải $[-32768, +32767]$.
2. **Công thức / Bitfield phải nhớ**:
   `raw = (int16_t)(((uint16_t)buf[high] << 8) | buf[low])`. Ví dụ tính toán / host test: Gyro raw +6550 ra $+100.0^{\circ}/\text{s}$; Accel raw +8192 ra $+1.0g$ (số liệu giả định kiểm tra logic, chưa phải đo từ cảm biến thật).
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Đọc burst 12 byte giảm chính xác bao nhiêu phần trăm thời gian bus?"
   * *Cách né*: Không khẳng định các tỷ lệ phần trăm tiết kiệm chưa được đo đạc thực nghiệm. Giải thích định tính: giảm overhead địa chỉ; mức tiết kiệm cụ thể chưa đo trên phần cứng.

---

### Câu 13: Tần số lấy mẫu cảm biến (ODR) và quy đổi vận tốc góc
1. **Quick Answer**: Với dải $\pm 500^{\circ}/\text{s}$, độ nhạy là $32768 / 500 \approx 65.5\,\text{LSB}/(^{\circ}/\text{s})$. Vận tốc góc tính bằng: $\omega = (\text{raw} - \text{bias}) / 65.5$. Khi ghi bộ chia `SMPLRT_DIV = 10`, theo datasheet TDK DS-000189: $\text{ODR} = 1125 / (1 + 10) \approx 102.27\,\text{Hz}$ (chu kỳ $\approx 9.78\,\text{ms}$, xấp xỉ đồng bộ chu kỳ đọc $10\,\text{ms}$ của ESP32).
2. **Công thức / Bitfield phải nhớ**:
   $\text{ODR} = 1125 / (1 + \text{DIV}) \approx 102.27\,\text{Hz}$; $\omega = (\text{raw} - \text{bias}) / 65.5$. Bước lượng tử $\approx 0.0153^{\circ}/\text{s}/\text{LSB}$.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Cảm biến xuất dữ liệu ở tần số đúng 100.0 Hz tròn không?"
   * *Cách né*: Không phải 100.0 Hz tròn; do bộ chia số nguyên từ clock cơ sở 1125 Hz, giá trị chính xác là $1125 / 11 \approx 102.27\,\text{Hz}$.

---

### Câu 14: Pipeline xử lý chuyển động: Dead-Zone hai ngưỡng, Gain và Clamping
1. **Quick Answer**: Vận tốc góc $\omega$ sau trừ bias được lọc qua dead-zone hai ngưỡng: dưới $0.8^{\circ}/\text{s}$ bằng 0 triệt rung tay; $0.8\text{--}1.4^{\circ}/\text{s}$ chuyển tiếp tuyến tính; trên $1.4^{\circ}/\text{s}$ áp dụng phần vượt ngưỡng thấp. Tiếp đó nhân Gain $K_x = K_y = 2.2$, làm tròn `roundf()`, và Clamping kẹp $[-127, +127]$ theo chuẩn HID `int8_t`.
2. **Công thức / Bitfield phải nhớ**:
   $\Delta X = \text{roundf}(K_x \cdot \omega_z), \Delta Y = \text{roundf}(-K_y \cdot \omega_y)$; kẹp biên $\max(-127, \min(127, \Delta X))$. Ngưỡng đứng yên độc lập: $|\omega| < 1.2^{\circ}/\text{s}$.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Tại sao không dùng đường cong gia tốc phi tuyến (mũ 1.2)?"
   * *Cách né*: Đường cong phi tuyến làm mất cảm giác tỉ lệ trực quan 1:1 và gây khó kiểm soát con trỏ khi vung nhanh.

---

### Câu 15: Vai trò bộ lọc bù Quaternion 6 trục và cơ chế Clutch/Recenter
1. **Quick Answer**: Dung hợp Gyro với trọng trường Accel ($K = 2.0\,\text{s}^{-1}$, $\tau \approx 0.5\,\text{s}$) ước lượng tư thế Roll/Pitch không bị Gimbal Lock. Trục Yaw trôi tự do; khi nghiêng cổ tay, Adaptive Reference Frame xoay hệ quy chiếu giữ hướng chuột trực giao. Nút Mode đóng vai trò Clutch (ngắt tạm chuột) hoặc Recenter (đặt lại tâm).
2. **Công thức / Bitfield phải nhớ**:
   $\mathbf{q} = [q_0, q_1, q_2, q_3], \dot{\mathbf{q}} = \frac{1}{2}\mathbf{q} \otimes \mathbf{\omega}_{\text{corrected}}$. Trọng trường: $\vec{v}_g = [2(q_1 q_3 - q_0 q_2), 2(q_0 q_1 + q_2 q_3), q_0^2 - q_1^2 - q_2^2 + q_3^2]^T$.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Bộ lọc bù Quaternion này có triệt tiêu được trôi góc Yaw không?"
   * *Cách né*: Không triệt tiêu hoàn toàn drift Yaw vì gia tốc kế chỉ đo trọng trường hướng xuống đất (neo Roll/Pitch, không neo Yaw).

---

## NHÓM 4: BLE HID, NÚT BẤM & QUẢN LÝ NGUỒN PIN (CÂU 16–20)

### Câu 16: Phân biệt bản chất clock I2C 400 kHz, baud UART 115200 và BLE HID
1. **Quick Answer**: I2C 400 kHz là xung nhịp đồng bộ có dây giữa ESP32 và cảm biến. UART 115200 là baud rate bất đồng bộ qua cáp USB, đồng bộ bằng bit START/STOP. BLE HID là mạng vô tuyến $2.4\,\text{GHz}$, không dùng baud rate mà truyền theo chu kỳ kết nối (Connection Interval $10\text{--}15\,\text{ms}$) qua bản tin GATT Notification.
2. **Công thức / Bitfield phải nhớ**:
   I2C: 400 kHz (chu kỳ $2.5\,\mu\text{s}$). UART: 115200 baud (bit $\approx 8.68\,\mu\text{s}$). BLE: Connection Interval $10\text{--}15\,\text{ms}$ (Report 5 byte).
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Tốc độ baud của kết nối Bluetooth HID là bao nhiêu?"
   * *Cách né*: BLE không dùng baud rate; dữ liệu truyền theo gói tin GATT Notification trong các Connection Event.

---

### Câu 17: Cấu trúc bản tin BLE HID Mouse Report (5 byte)
1. **Quick Answer**: Gồm 5 byte: Byte 0 là nút bấm (Bit 0: Trái, Bit 1: Phải, Bit 2: Giữa); Byte 1 là dịch chuyển ngang $\Delta X$ (`int8_t`, $-127$ đến $+127$); Byte 2 là dịch chuyển dọc $\Delta Y$ (`int8_t`); Byte 3 là cuộn dọc `Wheel`; Byte 4 là cuộn ngang `Pan`. Mọi giá trị vượt quá dải đều phải kẹp biên (clamping).
2. **Công thức / Bitfield phải nhớ**:
   `uint8_t report[5] = {buttons, (uint8_t)dX, (uint8_t)dY, wheel, pan};`.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Byte dX có thể truyền giá trị 500 pixel trong 1 bản tin không?"
   * *Cách né*: Không; `int8_t` chỉ lưu tối đa $+127$, nên mọi giá trị vượt quá đều phải kẹp biên (clamping) tại $\pm 127$.

---

### Câu 18: Ngoại vi nút bấm: Bắt cạnh (Edge Detection) vs Chống rung phần mềm (Debounce)
1. **Quick Answer**: Nút bấm nối GPIO25, 26, 27 cấu hình `INPUT_PULLUP` (Active-Low). Bắt cạnh (Edge Detection) là phát hiện thời điểm chuyển trạng thái logic (HIGH sang LOW khi nhấn). Chống rung phần mềm (Debounce) là lọc bỏ nảy tiếp điểm cơ học (khoảng 1–5 ms hoặc 15–20 ms là giá trị tham khảo/đề xuất). Bắt cạnh không phải là debounce; hệ thống cần cả hai.
2. **Công thức / Bitfield phải nhớ**:
   `pinMode(pin, INPUT_PULLUP)`. Nhấn: `digitalRead() == LOW`. Kiểm tra: `millis() - last_press_time > DEBOUNCE_MS`.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Hàm digitalRead() có tự động lọc bỏ rung nảy tiếp điểm cơ học không?"
   * *Cách né*: Không; `digitalRead()` chỉ đọc mức điện áp tức thời tại chân GPIO tại thời điểm gọi hàm.

---

### Câu 19: Bộ chuyển đổi ADC của ESP32, mạch đo điện áp pin và trạng thái hiện tại
1. **Quick Answer**: ESP32 dùng SAR ADC 12-bit (4096 mức). Do phi tuyến hai đầu thang đo (dưới 0.1V và trên 2.6V với suy hao 11dB) và Vref dao động, cần dùng thư viện `esp_adc_cal` hiệu chuẩn eFuse. Cầu phân áp 100k/100k từ $V_{\text{SYS}}$ về GND nối GPIO34 (ADC1_CH6 input-only, thuộc ADC1 tránh xung đột RF). Trạng thái Tuần 5: `HARDWARE_DESIGNED / FIRMWARE_NOT_IMPLEMENTED`.
2. **Công thức / Bitfield phải nhớ**:
   $V_{\text{sense}} = V_{\text{bat}} \times \frac{100\,\text{k}}{100\,\text{k} + 100\,\text{k}} = 0.5 \times V_{\text{bat}}$; khi pin đầy $4.2\,\text{V} \rightarrow V_{\text{sense}} = 2.1\,\text{V}$.
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Tính điện áp pin bằng công thức `V = analogRead(34) * 3.3 / 4095 * 2` có chuẩn xác không?"
   * *Cách né*: Không; công thức ngây thơ này bỏ qua sai lệch Vref và đặc tính phi tuyến của ADC ESP32. Báo cáo trung thực: firmware Tuần 5 chưa triển khai đọc pin.

---

### Câu 20: Kịch bản mất kết nối BLE, phục hồi và xử lý lỗi cảm biến (WHO_AM_I)
1. **Quick Answer**: Khi mất kết nối BLE, callback sự kiện ngắt kết nối tự động bật lại Advertising để máy tính kết nối lại; vòng lặp chính lập tức đặt $(\Delta X, \Delta Y) = (0, 0)$ tránh kẹt chuột. Nếu đọc `WHO_AM_I` không ra `0xEA` (nhận `0x00` hoặc `0xFF`), firmware ghi log báo lỗi I2C qua UART, chuyển sang chế độ an toàn và thử khởi động lại cảm biến.
2. **Công thức / Bitfield phải nhớ**:
   `WHO_AM_I` (Bank 0, `0x00`) có giá trị mặc định là `0xEA` (`0b11101010`).
3. **Bẫy phản biện & Cách né**:
   * *Bẫy*: "Nếu đang rê chuột mà Bluetooth ngắt kết nối thì máy tính có bị trôi chuột liên tục không?"
   * *Cách né*: Không; hệ điều hành chỉ di chuyển chuột khi nhận bản tin HID mới; khi ngắt kết nối, driver dừng gửi bản tin.

---
"""

def generate_handbook_markdown():
    md = []

    # -------------------------------------------------------------
    # 1. TIÊU ĐỀ VÀ THÔNG TIN BÌA CẨM NANG NỘI BỘ
    # -------------------------------------------------------------
    md.append(r"""# CẨM NANG TOÀN TẬP KIẾN THỨC VÀ BẢO VỆ ĐỒ ÁN
## CHUỘT BAY KHÔNG DÂY (AIR MOUSE BLE HID) SỬ DỤNG ESP32 CLASSIC VÀ CẢM BIẾN ICM-20948

---

### THÔNG TIN CHUNG TÀI LIỆU
* **Cơ sở đào tạo**: [TRƯỜNG ĐẠI HỌC / CƠ SỞ ĐÀO TẠO]
* **Đơn vị quản lý**: [KHOA / BỘ MÔN ĐIỆN TỬ - VIỄN THÔNG / HỆ THỐNG NHÚNG]
* **Tên đề tài**: **Nghiên cứu, Thiết kế và Chế tạo Chuột bay không dây (Air Mouse BLE HID) sử dụng ESP32 Classic và Cảm biến ICM-20948**
* **Kiến trúc cốt lõi**: **Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion.**
* **Môn học / Học phần**: Hệ thống nhúng (Embedded Systems) — Mốc Đánh giá Giữa kỳ (Tuần 5)
* **Phân loại tài liệu**: **TÀI LIỆU LƯU HÀNH NỘI BỘ — ÔN LUYỆN VẤN ĐÁP BẢO VỆ GIỮA KỲ (OFFICIAL MASTER DEFENSE HANDBOOK)**
* **Mục tiêu tài liệu**: Dành cho cả 03 thành viên nhóm thực hiện đề tài: Nắm vững bản chất kiến trúc, tường minh cơ chế thanh ghi & bitfield, làm chủ giải thuật xử lý tín hiệu chuyển động, cẩm nang xử lý 11 sự cố kỹ thuật, ngân hàng 36 câu hỏi vấn đáp chuyên sâu, cheat sheet 2 trang tóm tắt trọng tâm và bản đồ dàn ý 10 slide thuyết trình.
* **Thời gian hoàn thành**: Tháng 9 / Năm 2026
* **Phiên bản tài liệu**: V1.0.0

| Thông tin | Chi tiết |
|---|---|
| **Đối tượng sử dụng** | Toàn thể 03 thành viên nhóm thực hiện đề tài |
| **Môn học / Học phần** | Hệ thống nhúng (Embedded Systems) — Mốc Tuần 5 |
| **Thành viên 1 (Phần cứng & Nguồn)** | [Họ tên sinh viên 1 — MSSV 1] |
| **Thành viên 2 (I2C & Thanh ghi IMU)** | [Họ tên sinh viên 2 — MSSV 2] |
| **Thành viên 3 (Thuật toán & BLE HID)** | [Họ tên sinh viên 3 — MSSV 3] |
| **Phiên bản chuẩn mực** | Phiên bản V1.0.0 (Official Defense Master Handbook) |

---

## MỤC LỤC CẨM NANG KIẾN THỨC NỘI BỘ

0. [PHẦN 0 — NHỮNG GÌ PHẢI HỌC TRONG 2 NGÀY (QUICK DEFENSE CORE)](#phần-0--những-gì-phải-học-trong-2-ngày-quick-defense-core)
1. [PHẦN A — HIỂU TOÀN BỘ HỆ THỐNG TRONG 5 PHÚT](#phần-a--hiểu-toàn-bộ-hệ-thống-trong-5-phút)
   * A.1. Bản chất cốt lõi: Relative Rate-Control vs Absolute 3D
   * A.2. Dòng luồng dữ liệu toàn hệ thống (Burst Read 12-Byte & 10 Bước)
   * A.3. 10 điều cốt lõi phải thuộc lòng trước khi bảo vệ
2. [PHẦN B — VI ĐIỀU KHIỂN ESP32 VÀ QUY TẮC CHÂN NGOẠI VI](#phần-b--vi-điều-khiển-esp32-và-quy-tắc-chân-ngoại-vi)
   * B.1. Vì sao chọn ESP32 Classic mà không chọn STM32?
   * B.2. Bảng quy tắc phân bổ chân ngoại vi trên ESP32 DevKit 38-pin
   * B.3. Bản chất xung đột ADC2 và Lý do chọn GPIO34 (ADC1_CH6)
3. [PHẦN C — GIAO THỨC TRUYỀN THÔNG I2C CHUYÊN SÂU](#phần-c--giao-thức-truyền-thông-i2c-chuyên-sâu)
   * C.1. Cơ chế Cực máng để hở (Open-Drain) và Điện trở kéo lên
   * C.2. Byte địa chỉ I2C và Bit R/W
   * C.3. Chi tiết từng bước đọc thanh ghi với Repeated START
4. [PHẦN D — CẢM BIẾN CHUYỂN ĐỘNG ICM-20948](#phần-d--cảm-biến-chuyển-động-icm-20948)
   * D.1. So sánh ICM-20948 với dòng cảm biến cũ MPU-6050
   * D.2. Cơ chế User Bank Switching
   * D.3. Thanh ghi định danh WHO_AM_I (Bank 0, Địa chỉ 0x00)
5. [PHẦN E — CÁC THANH GHI CỐT LÕI CẦN THUỘC LÒNG (PWR_MGMT_1, GYRO_CONFIG_1, ACCEL_CONFIG)](#phần-e--các-thanh-ghi-cốt-lõi-cần-thuộc-lòng-pwr_mgmt_1-gyro_config_1-accel_config)
   * E.1. Thanh ghi PWR_MGMT_1 (Bank 0, Địa chỉ 0x06)
   * E.2. Thanh ghi GYRO_CONFIG_1 (Bank 2, Địa chỉ 0x01)
   * E.3. Thanh ghi ACCEL_CONFIG (Bank 2, Địa chỉ 0x14)
   * E.4. Trạng thái kiểm chứng các cấu hình thanh ghi
6. [PHẦN F — TỪ RAW DỮ LIỆU ĐẾN CON TRỎ CHUỘT (TOÁN HỌC & GIẢI THUẬT)](#phần-f--từ-raw-dữ-liệu-đến-con-trỏ-chuột-toán-học--giải-thuật)
   * F.1. Quy trình toán học từng bước (Burst 12-Byte, Bù Bias, Complementary Quaternion)
   * F.2. Phân tích chuyên sâu về Định lý Nyquist và 4 Miền thời gian
7. [PHẦN G — PHÂN HỆ TRUYỀN THÔNG BLE HID (BLUETOOTH LOW ENERGY)](#phần-g--phân-hệ-truyền-thông-ble-hid-bluetooth-low-energy)
   * G.1. Kiến trúc HID over GATT Profile (HOGP)
   * G.2. Bản tin báo cáo chuột (HID Mouse Report)
8. [PHẦN H — NGOẠI VI NÚT BẤM, ADC VÀ QUẢN LÝ NGUỒN PIN](#phần-h--ngoại-vi-nút-bấm-adc-và-quản-lý-nguồn-pin)
   * H.1. Nút bấm cơ khí và Quản lý chống rung phím (Edge-detected & Debounce)
   * H.2. Mạch đo áp pin qua ADC1_CH6 (GPIO34)
9. [PHẦN I — BẢNG ĐỐI CHIẾU CÁC QUYẾT ĐỊNH THIẾT KẾ (DESIGN TRADE-OFFS)](#phần-i--bảng-đối-chiếu-các-quyết-định-thiết-kế-design-trade-offs)
10. [PHẦN J — CẨM NANG XỬ LÝ SỰ CỐ PHẦN CỨNG & PHẦN MỀM (TROUBLESHOOTING GUIDE)](#phần-j--cẩm-nang-xử-lý-sự-cố-phần-cứng--phần-mềm-troubleshooting-guide)
11. [PHẦN K — BẢNG TỔNG HỢP RESEARCH GAPS CÒN LẠI (HẠNG MỤC CẦN KIỂM CHỨNG)](#phần-k--bảng-tổng-hợp-research-gaps-còn-lại-hạng-mục-cần-kiểm-chứng)
12. [PHẦN L — NGÂN HÀNG 36 CÂU HỎI VẤN ĐÁP BẢO VỆ GIỮA KỲ (Q&A DEFENSE BANK)](#phần-l--ngân-hàng-36-câu-hỏi-vấn-đáp-bảo-vệ-giữa-kỳ-qa-defense-bank)
13. [PHẦN M — CHEAT SHEET 2 TRANG TÓM TẮT TRỌNG TÂM (IN 2 MẶT A4 TRƯỚC GIỜ BẢO VỆ)](#phần-m--cheat-sheet-2-trang-tóm-tắt-trọng-tâm-in-2-mặt-a4-trước-giờ-bảo-vệ)
14. [PHẦN N — BẢN ĐỒ DÀN Ý CHUẨN BỊ SLIDE THUYẾT TRÌNH (10 SLIDES CHUẨN)](#phần-n--bản-đồ-dàn-ý-chuẩn-bị-slide-thuyết-trình-10-slides-chuẩn)
15. [PHẦN O — GỢI Ý PHÂN CÔNG NHIỆM VỤ VÀ PHỐI HỢP 3 THÀNH VIÊN](#phần-o--gợi-ý-phân-công-nhiệm-vụ-và-phối-hợp-3-thành-viên)

---
""")

    # -------------------------------------------------------------
    # PHẦN 0 — NHỮNG GÌ PHẢI HỌC TRONG 2 NGÀY (QUICK DEFENSE CORE)
    # -------------------------------------------------------------
    p0_text = get_p0()
    p0_words = len(p0_text.split())
    assert 2500 <= p0_words <= 3500, f"Section 0 words {p0_words} out of range [2500, 3500]"
    md.append(p0_text)

    # -------------------------------------------------------------
    # PHẦN A
    # -------------------------------------------------------------
    md.append(r"""# PHẦN A — HIỂU TOÀN BỘ HỆ THỐNG TRONG 5 PHÚT

## A.1. Bản chất cốt lõi: Relative Rate-Control vs Absolute 3D

* **Khái niệm cốt lõi cần nhớ**: Đề tài của nhóm là **THIẾT BỊ TRỎ TƯƠNG ĐỐI ĐIỀU KHIỂN THEO TỐC ĐỘ XOAY** (Relative Rate-Controlled Pointing Device).
* **Định nghĩa kiến trúc chuẩn**: **Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion.**
  * *Hardware*: 9-DOF SiP (Gyro 3 trục, Accel 3 trục, Mag AK09916 3 trục).
  * *Firmware V1*: Triển khai dung hợp 6 trục Gyro-Accelerometer bằng bộ lọc bù Quaternion (`CODE_IMPLEMENTED + HOST_TESTED`).
  * *Magnetometer AK09916*: Chưa khởi tạo / chưa dùng ở V1. Không gọi thuật toán là "9-axis sensor fusion".
  * *Đặc tính Yaw*: Yaw là góc xoay tương đối và có trôi chậm theo thời gian do chưa có la bàn tham chiếu; gia tốc kế chỉ neo Roll/Pitch. Cơ chế Clutch/Recenter cho phép người dùng đặt lại hệ quy chiếu tương đối tức thì.

> [!IMPORTANT]
> **PHÂN BIỆT RÕ RÀNG: ROTATIONAL MOTION KHÁC TRANSLATIONAL MOTION**:  
> Air Mouse V1 điều khiển con trỏ bằng **chuyển động XOAY của cổ tay (Rotational Motion)**, không phải bằng sự dịch chuyển tịnh tiến của bàn tay (Translational Motion).  
> Ngay cả khi tâm bàn tay gần như đứng yên trong không gian (không dịch chuyển từ vị trí A sang vị trí B), việc xoay cổ tay quanh các trục được ánh xạ (Pitch/Yaw) vẫn tạo ra vận tốc góc ($\omega$ tính bằng $^{\circ}/\text{s}$), vi điều khiển vẫn tính toán ra $(\Delta X, \Delta Y)$ và làm con trỏ chuột di chuyển trên màn hình.  
> Con trỏ chuột chỉ dừng lại khi: vận tốc góc trên các trục điều khiển xấp xỉ 0 sau khi qua bước bù sai số tĩnh (bias) và vùng chết (dead-zone).  
> **GIỚI HẠN PHẠM VI V1**: Phiên bản V1 của nhóm **KHÔNG** triển khai tracking vị trí 3D hoặc bộ điều khiển VR 6DoF (đây là giới hạn phạm vi thiết kế của phiên bản V1, không phải giới hạn tuyệt đối của bản thân cảm biến IMU).

* **Câu hỏi bẫy kinh điển: Tại sao không dùng gia tốc kế (Accelerometer) tích phân 2 lần?**
  * Gia tốc kế MEMS luôn chứa sai số độ lệch tĩnh (offset bias $\epsilon$) và nhiễu ngẫu nhiên.
  * Khi lấy tích phân lần 1 ra vận tốc, sai số tăng tuyến tính theo thời gian:
    $$v(t) = v_0 + \epsilon \cdot t$$
  * Khi lấy tích phân lần 2 ra quãng đường, sai số bùng nổ theo hàm bình phương thời gian ($t^2$):
    $$s(t) = s_0 + v_0 \cdot t + \frac{1}{2}\epsilon \cdot t^2$$
  * Chỉ sau 2–3 giây, sai số vị trí đã lên tới vài mét, con trỏ chuột sẽ lập tức "bay mất" khỏi màn hình ngay cả khi thiết bị nằm im trên mặt bàn!
* **Giải pháp khoa học của nhóm**: Con quay hồi chuyển (Gyroscope) đo trực tiếp vận tốc góc xoay của cổ tay ($\omega_x, \omega_y, \omega_z$ tính bằng $^{\circ}/\text{s}$). Ta nhân vận tốc góc này với hệ số khuếch đại (Gain $K$) để ra số pixel dịch chuyển con trỏ chuột mà **KHÔNG CẦN TÍCH PHÂN**. Gia tốc kế được dung hợp qua bộ lọc bù Quaternion 6 trục để neo góc nghiêng Roll/Pitch, nhận diện đứng yên và bắt cử chỉ Flick.

## A.2. Dòng luồng dữ liệu toàn hệ thống (System Data Path)

![Hình A.1 — Sơ đồ dòng dữ liệu và kiến trúc phần cứng hệ thống Air Mouse](assets/fig_system_block_diagram.png)  
*Hình A.1 — Sơ đồ dòng dữ liệu và kiến trúc phần cứng hệ thống Air Mouse BLE HID*

Dòng luồng dữ liệu tuần tự gồm 10 bước khép kín:
1. **Bước 1**: Người dùng xoay cổ tay tạo vận tốc góc cơ học và gia tốc.
2. **Bước 2**: Khối vi cơ MEMS Gyroscope và Accelerometer bên trong ICM-20948 cảm ứng chuyển động.
3. **Bước 3**: Bộ lọc dải thông thấp số phần cứng nội bộ (**Hardware Gyro DLPF $51.2\,\text{Hz}$** và **Hardware Accel DLPF $50.4\,\text{Hz}$**) lọc mượt tín hiệu và khối ADC 16-bit nội bộ số hóa thành dữ liệu bù 2 lưu vào các thanh ghi tại User Bank 0 từ `0x2D` đến `0x38`.
4. **Bước 4**: ESP32 đóng vai trò I2C Master đọc một lần 12 byte dữ liệu thô qua bus I2C Fast Mode $400\,\text{kHz}$ nối trực tiếp ở mức $3.3\,\text{V}$ với module WCMCU-20948 (trở kéo $10\,\text{k}\Omega$ onboard lên $3.3\,\text{V}$). Một giao dịch đọc liên tiếp 12 byte làm giảm độ lệch thời điểm so với đọc từng thanh ghi riêng (đã kiểm chứng đọc burst 12 byte thành công trên phần cứng thật trong phép thử ngắn hạn).
5. **Bước 5**: Firmware ESP32 quy đổi dữ liệu thô sang đơn vị vật lý: Accel chia cho $8192\,\text{LSB}/g$, Gyro chia cho $65.5\,\text{LSB}/(^{\circ}/\text{s})$; trừ sai số độ lệch tĩnh (Zero-Rate Bias Compensation) thu được từ 200 lần polling lúc khởi động.
6. **Bước 6**: Bộ lọc bù Quaternion 6 trục (**6-axis Complementary Quaternion Filter**, $K = 2.0\,\text{s}^{-1}$, $\tau \approx 0.5\,\text{s}$, dynamic $\Delta t$ kẹp $[1, 50]\,\text{ms}$) ước lượng tư thế Roll/Pitch và tự động duy trì hệ quy chiếu tham chiếu thích nghi (**Adaptive Reference Frame**).
7. **Bước 7**: Dead-zone dùng hai ngưỡng: dưới $0.8^{\circ}/\text{s}$ đầu ra bằng 0; từ $0.8$ đến $1.4^{\circ}/\text{s}$ là vùng chuyển tiếp tuyến tính; trên $1.4^{\circ}/\text{s}$ áp dụng phần vận tốc vượt ngưỡng thấp. Giá trị $1.2^{\circ}/\text{s}$ là ngưỡng Gyro độc lập dùng để nhận diện trạng thái đứng yên.
8. **Bước 8**: Nhân hệ số khuếch đại tuyến tính (Linear Gain $K_x = 2.2, K_y = 2.2$), làm tròn `roundf()`, ánh xạ trục và chặn biên Clamping $[-127, +127]$ theo chuẩn HID để tạo ra độ dịch chuyển pixel tương đối $(\Delta X, \Delta Y)$ (không dùng đường cong phi tuyến hay số mũ 1.2). Đồng thời phát hiện cử chỉ vung nhanh Flick dựa trên gia tốc tịnh tiến khử trọng trường chiếu lên trục ngang ($a_{\text{lateral}}$, peak $1.15g$, return $0.35g$, duration $60\text{--}450\,\text{ms}$, cooldown $350\,\text{ms}$) cho chức năng Back/Forward và cơ chế Clutch/Recenter.
9. **Bước 9**: Vi điều khiển quét trạng thái các nút bấm cơ khí (Active-Low trên GPIO25, 26, 27), đóng gói vào bản tin chuẩn HID Mouse Report.
10. **Bước 10**: Bản tin được phát qua sóng vô tuyến BLE $2.4\,\text{GHz}$ theo chuẩn HID Mouse Report 5 byte; kết nối thực tế tới hệ điều hành máy tính PC hiện ở trạng thái `[NOT_TESTED]` (chưa kiểm thử trên máy tính thật).

> [!NOTE]
> **TÀI LIỆU KỸ THUẬT BÀN GIAO THIẾT KẾ ĐÍNH KÈM**:  
> Nhóm đã lập 2 tài liệu kỹ thuật chi tiết phục vụ việc vẽ schematic và thiết kế đồ họa sơ đồ khối:
> 1. [`deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md`](deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md): Bảng nối dây chân-đến-chân chi tiết 50 dòng theo baseline Direct 3.3V đã khóa (phân định rõ nhãn in trên module vs GPIO ESP32, quy chuẩn nút bấm 4 chân, bảo vệ cực tính pin và danh mục các chân tuyệt đối cấm nối).
> 2. [`deliverables/MO_TA_SO_DO_KHOI_AIR_MOUSE.md`](deliverables/MO_TA_SO_DO_KHOI_AIR_MOUSE.md): Bản đặc tả chi tiết 6 khối hệ thống, sơ đồ ASCII trực quan và các chỉ dẫn bố cục mỹ thuật chuẩn A4 cho thành viên vẽ hình.

## A.3. 10 điều cốt lõi phải thuộc lòng trước khi bảo vệ

> [!NOTE]
> **10 ĐIỀU PHẢI THUỘC LÒNG (MUST-MEMORIZE CHECKLIST):**
> 1. Air Mouse là **thiết bị trỏ tương đối điều khiển theo tốc độ xoay cổ tay** (Relative Rate-Controlled Pointing Device); kiến trúc chuẩn là: **Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion**.
> 2. Dùng **Gyroscope đo trực tiếp vận tốc góc** ($^{\circ}/\text{s}$); **KHÔNG** dùng Accelerometer tích phân 2 lần vì sai số trôi bùng nổ theo hàm $t^2$. Accelerometer được dùng để neo Roll/Pitch qua bộ lọc bù Quaternion 6 trục, nhận diện đứng yên và bắt cử chỉ Flick.
> 3. ESP32 Classic có sẵn **phần cứng BLE v4.2 và CPU 240 MHz dual-core**; chọn chân **GPIO34 (ADC1_CH6)** để đo áp pin vì là chân Input-Only và thuộc khối ADC1 không xung đột Wi-Fi. Chân ADC hoàn toàn tách biệt khỏi nguồn 5V VIN.
> 4. **Tránh bố trí nút bấm** vào các chân Strapping Pins (GPIO0, GPIO2, GPIO12, GPIO15) để loại bỏ rủi ro boot failure khi người dùng vô tình giữ nút lúc bật nguồn (các chân này vẫn có thể dùng làm I/O thông thường nếu bảo đảm mức logic khi khởi động). Đèn LED chỉ thị gắn chân GPIO32 qua trở hạn dòng $1.0\,\text{k}\Omega$.
> 5. Bus I2C là cấu trúc **Cực máng để hở (Open-Drain)**, bắt buộc có điện trở kéo pull-up ($10\,\text{k}\Omega$ có sẵn trên module WCMCU-20948 kéo lên $3.3\,\text{V}$, kết nối Direct 3.3V, không dùng BSS138). Địa chỉ cảm biến là `0x68` (AD0=0).
> 6. ICM-20948 tổ chức thanh ghi thành **4 User Bank** với không gian địa chỉ 512 byte (~80–100 thanh ghi hoạt động); muốn truy xuất thanh ghi ở Bank nào phải chuyển qua thanh ghi `REG_BANK_SEL` (`0x7F`) trước (`imu_selectBank()`).
> 7. Thanh ghi `PWR_MGMT_1` (Bank 0, Địa chỉ `0x06`) ghi giá trị `0x01` để **thoát chế độ ngủ Sleep** (Bit 6=0) và **khóa xung vào bộ dao động PLL** (Bits [2:0]=001, dự phòng dao động nội theo DS-000189 Table 16).
> 8. Thanh ghi `GYRO_CONFIG_1` (Bank 2, Địa chỉ `0x01`) ghi `0x1B` để **kích hoạt DLPF 51.2 Hz** (Bit 0=1, Bits [5:3]=011, Noise BW 73.3 Hz) và **dải đo $\pm 500^{\circ}/\text{s}$** (Bits [2:1]=01). Thanh ghi `ACCEL_CONFIG` (Bank 2, Địa chỉ `0x14`) ghi `0x1B` để kích hoạt DLPF 50.4 Hz (Noise BW 68.8 Hz theo Table 18 — Accelerator Configuration) và dải đo $\pm 4g$.
> 9. Độ nhạy danh định: Gyroscope dải $\pm 500^{\circ}/\text{s}$ là **$65.5\,\text{LSB}/(^{\circ}/\text{s})$**; Accelerometer dải $\pm 4g$ là **$8192\,\text{LSB}/g$**. Đọc dữ liệu bằng 1 lần Burst Read 12 byte (`imu_readBurst(0, 0x2D, raw_buf, 12)` từ `0x2D` đến `0x38` tại Bank 0).
> 10. Bản tin chuột gửi qua BLE **phụ thuộc vào HID Report Descriptor** đăng ký với máy tính; bản tin mở rộng thông dụng gồm 5 byte `[Buttons, dX, dY, Wheel, Pan]`.

---
""")

    # -------------------------------------------------------------
    # PHẦN B
    # -------------------------------------------------------------
    md.append(r"""# PHẦN B — VI ĐIỀU KHIỂN ESP32 VÀ QUY TẮC CHÂN NGOẠI VI

## B.1. Vì sao chọn ESP32 Classic mà không chọn STM32?

Trong các đề tài đồ án môn Hệ thống nhúng truyền thống, sinh viên thường sử dụng dòng vi điều khiển STM32F1/F4 hoặc Arduino Uno. Nhóm quyết định lựa chọn ESP32 Classic (ESP-WROOM-32) dựa trên 3 lý do kỹ thuật:
1. **Tích hợp sẵn phần cứng BLE trên chip**: ESP32 tích hợp sẵn bộ thu phát vô tuyến Bluetooth Low Energy v4.2. Nếu dùng STM32, nhóm bắt buộc phải thiết kế thêm mạch ngoài gắn module Bluetooth rời (như module nRF52 hoặc HC-05 chạy Bluetooth Classic 2.0 cũ tiêu thụ pin lớn), làm tăng diện tích bo mạch PCB, tăng chi phí và phức tạp hóa việc đồng bộ tín hiệu.
2. **Sức mạnh xử lý và hỗ trợ FreeRTOS đa nhiệm**: Vi xử lý lõi kép 32-bit Xtensa LX6 tốc độ xung nhịp lên tới $240\,\text{MHz}$, bộ nhớ $520\,\text{KB}$ SRAM. Khả năng chạy đa nhiệm FreeRTOS cho phép phân chia Nhân 0 chuyên trách xử lý ngăn xếp mạng không dây BLE, và Nhân 1 chuyên trách đọc cảm biến I2C và giải thuật xử lý chuyển động.
3. **Chi phí và hệ sinh thái**: Bo mạch ESP32 DevKit 38-pin giá thành rẻ, tích hợp sẵn mạch nạp tự động CP2102/CH340 qua cổng USB, được hỗ trợ toàn diện bởi cộng đồng mã nguồn mở và dễ dàng tích hợp thư viện BLE HID chuẩn.

## B.2. Bảng quy tắc phân bổ chân ngoại vi trên ESP32 DevKit 38-pin

> [!WARNING]
> **CẨM NANG AN TOÀN CHÂN GPIO TRÊN BO MẠCH ESP32:**
> * **NHÓM CẤM DÙNG (SPI FLASH PINS)**: `GPIO6` đến `GPIO11` được nối ngầm trực tiếp trên module ESP-WROOM-32 với chip nhớ SPI Flash. Tuyệt đối không can thiệp các chân này trong phần mềm, nếu cấu hình sẽ gây lỗi Crash CPU và Reset hệ thống vĩnh viễn!
> * **NHÓM STRAPPING PINS (BOOT CONFIGURATION)**: `GPIO0` (chọn chế độ bootloader), `GPIO2` (chế độ flashing), `GPIO12` (điện áp cấp SPI flash), `GPIO15` (chế độ debug JTAG). Các chân này vẫn có thể dùng làm I/O thông thường nếu bảo đảm mức logic khi khởi động, nhưng đề tài chủ động tránh nút bấm trên các chân này để loại bỏ rủi ro boot failure khi người dùng vô tình giữ nút lúc bật nguồn.
> * **NHÓM INPUT-ONLY (CHỈ NHẬN TÍN HIỆU VÀO)**: `GPIO34`, `GPIO35`, `GPIO36` (VP), `GPIO39` (VN). Các chân này không có mạch đệm ngõ ra (No Output Driver) và không có điện trở kéo nội bộ. Rất lý tưởng để làm ngõ vào tương tự cho khối ADC đo điện áp nguồn pin.
> * **NHÓM AN TOÀN CHO NÚT BẤM VÀ NGOẠI VI**: `GPIO21` (I2C SDA), `GPIO22` (I2C SCL), `GPIO25` (BTN_LEFT), `GPIO26` (BTN_RIGHT), `GPIO27` (BTN_MODE), `GPIO32` (LED_STATUS với trở hạn dòng $1.0\,\text{k}\Omega$).

## B.3. Bản chất xung đột ADC2 và Lý do chọn GPIO34 (ADC1_CH6)

* **Làm rõ bản chất kỹ thuật**: Nhiều tài liệu không chính xác thường nói rằng *"Bluetooth gây khóa hoàn toàn khối ADC2"*. Đây là một ngộ nhận về cơ chế phần cứng.
* **Cơ chế phần cứng thực tế**: Trên chip ESP32 Classic, bộ chuyển đổi tương tự - số SAR ADC2 (quản lý các chân GPIO0, 2, 4, 12–15, 25–27) dùng chung mạch phần cứng với bộ điều khiển vô tuyến Wi-Fi thông qua bộ trọng tài phần cứng (Hardware Arbiter). Khi driver Wi-Fi được kích hoạt, nó chiếm quyền độc quyền bộ SAR ADC2; nếu ứng dụng gọi hàm `analogRead()` trên các chân này, driver sẽ từ chối và trả về mã lỗi `ESP_ERR_INVALID_STATE`.
* **Đối với Bluetooth Low Energy (BLE)**: BLE không sử dụng chung cơ chế khóa phần cứng này của Wi-Fi. Tuy nhiên, việc nhóm quyết định chọn chân **GPIO34 (kênh ADC1_CH6)** để đo điện áp pin là chuẩn mực thiết kế an toàn trên ESP32 vì:
  1. Khối SAR ADC1 hoàn toàn độc lập về mặt vật lý với cả bộ điều khiển Wi-Fi và BLE, triệt tiêu nguy cơ xung đột phần cứng tiềm ẩn.
  2. GPIO34 là chân Input-Only, việc gán chân này cho cảm biến analog giúp tiết kiệm và giải phóng các chân GPIO xuất-nhập hai chiều đa năng cho các nút bấm cơ khí.

---
""")

    # -------------------------------------------------------------
    # PHẦN C
    # -------------------------------------------------------------
    md.append(r"""# PHẦN C — GIAO THỨC TRUYỀN THÔNG I2C CHUYÊN SÂU

## C.1. Cơ chế Cực máng để hở (Open-Drain) và Điện trở kéo lên

* **Vì sao bus I2C bắt buộc phải có điện trở kéo lên nguồn (Pull-up Resistors)?**
  * Các chân SDA và SCL trên cả vi điều khiển Master lẫn cảm biến Slave đều sử dụng cấu trúc bán dẫn **Cực máng để hở (Open-Drain)**. Cấu trúc này chỉ gồm một transistor N-MOSFET nối chân xuống mass GND. Khi transistor dẫn, chân bị kéo về mức $0\,\text{V}$ (LOW). Khi transistor ngắt, chân rơi vào trạng thái trở kháng cao (High-Z / Floating), không thể tự phát ra điện áp dương $3.3\,\text{V}$ hay $1.8\,\text{V}$.
  * Do đó, đường dây bắt buộc phải được gắn điện trở kéo lên nguồn điện áp (Pull-up Resistor). Khi không có thiết bị nào kéo chân xuống mass, điện trở sẽ kéo đường dây về mức điện áp HIGH logic.
* **Đặc tính logic nối chung (Wired-AND)**: Cơ chế Open-Drain tạo ra tính năng Wired-AND an toàn. Nếu hai thiết bị vô tình phát tín hiệu trái ngược nhau cùng một thời điểm, đường dây chỉ đơn giản bị kéo về mức 0 mà **KHÔNG** xảy ra hiện tượng ngắn mạch chập nguồn gây cháy chân linh kiện.
* **Cấu hình điện trở kéo trên mạch Air Mouse**:
  * Miền điện áp $3.3\,\text{V}$ (phía ESP32): Điện trở kéo $4.7\,\text{k}\Omega$ lên $3.3\,\text{V}$.
  * Miền điện áp $1.8\,\text{V}$ (phía WCMCU-20948): Điện trở kéo $10\,\text{k}\Omega$ lên $1.8\,\text{V}$.

## C.2. Byte địa chỉ I2C và Bit R/W

Địa chỉ vật lý của cảm biến ICM-20948 là địa chỉ 7-bit: `0x68` (`0b1101000`) khi chân AD0 được nối xuống GND. Khi giao tiếp trên đường truyền, I2C Master đóng gói 7 bit địa chỉ này vào các bit từ [7:1], và đặt bit chọn hướng truyền `R/W` ở bit có trọng số thấp nhất (Bit 0):
* **Khung truyền GHI (Master Write)**:
  $$(0\text{x}68 \ll 1) \mid 0 = 0\text{xD0} \quad (\text{Hệ nhị phân: } 0\text{b}11010000)$$
* **Khung truyền ĐỌC (Master Read)**:
  $$(0\text{x}68 \ll 1) \mid 1 = 0\text{xD1} \quad (\text{Hệ nhị phân: } 0\text{b}11010001)$$

## C.3. Chi tiết từng bước đọc thanh ghi với Repeated START

![Hình C.1 — Sơ đồ thời gian các byte phát trên đường SDA/SCL khi đọc thanh ghi](assets/fig_i2c_transaction.png)  
*Hình C.1 — Sơ đồ thời gian các byte phát trên đường SDA/SCL khi đọc thanh ghi cảm biến ICM-20948*

Chuỗi giao dịch đọc thanh ghi chuẩn mực:
1. Master phát điều kiện **START (S)**: Kéo đường SDA từ HIGH xuống LOW trong khi SCL vẫn ở mức HIGH.
2. Master gửi byte địa chỉ ghi **$0\text{xD0}$** `[0x68 + W]`.
3. Slave ICM-20948 nhận diện đúng địa chỉ, phản hồi xung **ACK** (kéo SDA xuống LOW ở xung clock thứ 9).
4. Master gửi byte địa chỉ thanh ghi mục tiêu: ví dụ **$0\text{x00}$** (thanh ghi `WHO_AM_I`).
5. Slave phản hồi xung **ACK**. Con trỏ địa chỉ nội bộ của cảm biến lúc này đã trỏ vào thanh ghi $0\text{x00}$.
6. Master phát điều kiện **REPEATED START (Sr)**: Kéo SDA từ HIGH xuống LOW khi SCL đang HIGH mà **KHÔNG PHÁT ĐIỀU KIỆN STOP** (sử dụng `Wire.endTransmission(false)` để đệm/phát mà không dừng bus).
7. Master gửi byte địa chỉ đọc **$0\text{xD1}$** `[0x68 + R]` thông qua `Wire.requestFrom()`.
8. Slave phản hồi xung **ACK**.
9. Slave nắm quyền điều khiển đường SDA, đẩy 8 bit dữ liệu nội bộ ra ngoài (ví dụ byte giá trị $0\text{xEA}$).
10. Master nhận dữ liệu, phát tín hiệu **NACK** để báo dừng đọc, sau đó phát điều kiện **STOP (P)** để giải phóng bus.

> [!TIP]
> **VÌ SAO DÙNG REPEATED START THAY VÌ STOP RỒI START LẠI?**  
> Trong các hệ thống đa Master (Multi-Master), nếu Master phát STOP sau khi chỉ định địa chỉ thanh ghi, thiết bị khác có thể chen ngang chiếm bus, làm mất con trỏ địa chỉ vừa thiết lập. **Repeated START** cho phép Master đảo chiều từ Ghi sang Đọc mà vẫn duy trì quyền kiểm soát bus liên tục.

---
""")

    # -------------------------------------------------------------
    # PHẦN D
    # -------------------------------------------------------------
    md.append(r"""# PHẦN D — CẢM BIẾN CHUYỂN ĐỘNG ICM-20948

## D.1. So sánh ICM-20948 với dòng cảm biến cũ MPU-6050

| Tiêu chí kỹ thuật | MPU-6050 (Thế hệ cũ) | ICM-20948 (Thế hệ mới — Đề tài sử dụng) | Lợi ích trong thiết kế Air Mouse |
|---|---|---|---|
| **Số bậc tự do (DOF)** | 6-DOF (3-axis Gyro + 3-axis Accel) | **9-DOF** (3 Gyro + 3 Accel + 3 Mag AK09916) | Tích hợp sẵn la bàn số, mở rộng được định hướng không gian tuyệt đối ở V2 |
| **Điện áp logic I/O ($V_{\text{DDIO}}$)** | $3.3\,\text{V}$ (tương thích trực tiếp ESP32) | **$1.8\,\text{V}$ raw IC / Nối trực tiếp $3.3\,\text{V}$ trên module WCMCU** | Module WCMCU-20948 nối trực tiếp 3.3V ESP32; loại bỏ BSS138 và LDO 1.8V |
| **Dòng tiêu thụ ở chế độ đo** | $\approx 3.9\,\text{mA}$ | **$\approx 3.11\,\text{mA}$ (chế độ 6 trục)** | Kéo dài thời lượng vận hành của viên pin LiPo 1S dung lượng nhỏ |
| **Bộ nhớ đệm FIFO** | $1024\,\text{Byte}$ | **$4096\,\text{Byte}$ (4 KB)** | Chứa được nhiều mẫu hơn, chống tràn dữ liệu khi nhân BLE bận xử lý RF |
| **Không gian thanh ghi** | Phẳng 128 byte ($0\text{x}00\text{--}0\text{x}7\text{F}$) | **4 User Bank** (512 byte tổng cộng) | Phân tầng cấu hình chuyên sâu, tránh trùng lặp địa chỉ thanh ghi |

## D.2. Cơ chế User Bank Switching

![Hình D.1 — Bản đồ bộ nhớ 4 User Bank của chip ICM-20948](assets/fig_user_bank_map.png)  
*Hình D.1 — Cấu trúc phân chia 4 User Bank và vị trí thanh ghi đặc biệt REG_BANK_SEL (0x7F)*

* **Tại sao ICM-20948 lại chia thành 4 User Bank?**  
  Do số lượng thanh ghi cấu hình của chip vượt quá 128 địa chỉ (chuẩn I2C thanh ghi 7-bit địa chỉ nội bộ), TDK đã thiết kế cơ chế chuyển ngân hàng bộ nhớ (Bank Switching). Toàn bộ không gian 512 byte được chia làm 4 Bank:
  * **Bank 0**: Chứa mã định danh `WHO_AM_I`, thanh ghi quản lý nguồn `PWR_MGMT_1`, dữ liệu đo thô 12-byte của Gyro/Accel, và cờ ngắt.
  * **Bank 1**: Chứa các thanh ghi cấu hình bù sai số lệch tĩnh (Offset/Bias Cancellation) của cảm biến.
  * **Bank 2**: Chứa toàn bộ các thanh ghi cấu hình dải đo và bộ lọc: `GYRO_CONFIG_1`, `ACCEL_CONFIG`, bộ chia tần số lấy mẫu `SMPLRT_DIV`.
  * **Bank 3**: Chứa các thanh ghi điều khiển khối I2C Master nội bộ dùng để giao tiếp với từ kế AK09916.
* **Thanh ghi chọn Bank `REG_BANK_SEL` (Địa chỉ $0\text{x}7\text{F}$)**:  
  Thanh ghi này có mặt đồng thời trên cả 4 Bank tại địa chỉ $0\text{x}7\text{F}$. Để truy xuất thanh ghi ở Bank nào, Master bắt buộc phải ghi giá trị tương ứng vào thanh ghi này trước:
  * Ghi `0x00` $\rightarrow$ Chuyển về **User Bank 0**.
  * Ghi `0x10` $\rightarrow$ Chuyển sang **User Bank 1**.
  * Ghi `0x20` $\rightarrow$ Chuyển sang **User Bank 2**.
  * Ghi `0x30` $\rightarrow$ Chuyển sang **User Bank 3**.

## D.3. Thanh ghi định danh WHO_AM_I (Bank 0, Địa chỉ 0x00)

* **Địa chỉ**: User Bank 0, Địa chỉ `0x00`, Độ rộng 8-bit, Chỉ đọc (Read-Only).
* **Giá trị mặc định cố định**: `0xEA` (Hệ nhị phân: `0b11101010`).
* **Ý nghĩa trong quy trình khởi tạo phần cứng**:  
  Đây là thanh ghi đầu tiên ESP32 bắt buộc phải đọc ngay sau khi cấp nguồn. Nếu đọc về đúng `0xEA`, xác nhận tại thời điểm đó:
  1. Module cảm biến WCMCU-20948 đã được cấp nguồn 3.3V ổn định từ chân 3V3 của ESP32.
  2. Đường truyền I2C (SDA GPIO21, SCL GPIO22) nối trực tiếp tiếp xúc tốt, trở kéo 10 kΩ onboard lên 3.3V hoạt động chuẩn xác.
  3. Cảm biến ICM-20948 phản hồi đúng định danh mong đợi, sẵn sàng nhận lệnh cấu hình tiếp theo.
  *(Minh chứng thực nghiệm: 100/100 lần đọc WHO_AM_I=0xEA thành công trong phép thử ngắn hạn trên phần cứng nhóm sở hữu).*

---
""")

    # -------------------------------------------------------------
    # PHẦN E
    # -------------------------------------------------------------
    md.append(r"""# PHẦN E — CÁC THANH GHI CỐT LÕI CẦN THUỘC LÒNG (PWR_MGMT_1, GYRO_CONFIG_1, ACCEL_CONFIG)

## E.1. Thanh ghi PWR_MGMT_1 (Bank 0, Địa chỉ 0x06)

* **Vị trí**: User Bank 0, Địa chỉ `0x06`, Độ rộng 8-bit.
* **Cấu hình dự án**: Giá trị `0x01` (Hệ nhị phân: `0b00000001`).
* **Phân loại**: `PROJECT CONFIGURATION`.

![Hình E.1 — Bitfield thanh ghi PWR_MGMT_1](assets/fig_bitfield_pwr_mgmt_1.png)  
*Hình E.1 — Cấu trúc bitfield chi tiết của thanh ghi PWR_MGMT_1 (Bank 0, Địa chỉ 0x06)*

| Bit | Tên Bitfield | Giá trị ghi | Chức năng theo Datasheet TDK DS-000189 §10.2 Table 16 | Ý nghĩa cấu hình trong dự án |
|---|---|---|---|---|
| **Bit 7** | `DEVICE_RESET` | 0 | 1: Reset phần mềm toàn bộ thanh ghi nội về mặc định; 0: Hoạt động bình thường | Không phát lệnh reset chip trong lúc đang vận hành bình thường |
| **Bit 6** | `SLEEP` | 0 | 1: Đưa chip vào chế độ ngủ tiết kiệm điện; 0: Đánh thức chip hoạt động | **Đánh thức chip** khỏi trạng thái Sleep mặc định sau khi cấp nguồn |
| **Bit 5** | `LP_EN` | 0 | 1: Bật chế độ Low-Power duty-cycled; 0: Tắt Low-Power, chạy đo liên tục | Chạy cảm biến ở chế độ đo liên tục để lấy mẫu tín hiệu ổn định |
| **Bit 4** | `Reserved` | 0 | Bit dành riêng của hãng sản xuất TDK | Luôn ghi mức 0 theo quy định chính thức của hãng |
| **Bit 3** | `TEMP_DIS` | 0 | 1: Tắt cảm biến nhiệt độ nội; 0: Bật cảm biến nhiệt độ nội | Bật cảm biến nhiệt độ (chuẩn bị cho thuật toán bù trôi nhiệt sau này) |
| **Bits [2:0]** | `CLKSEL[2:0]` | 001<br>(0x01) | 000: Dao động nội 20 MHz; 001–005: Tự động chọn nguồn xung tốt nhất (PLL nếu sẵn sàng, else 20MHz) | **Tự động chọn nguồn xung tốt nhất** (khóa vào PLL khi sẵn sàng, dự phòng dao động nội) |

## E.2. Thanh ghi GYRO_CONFIG_1 (Bank 2, Địa chỉ 0x01)

* **Vị trí**: User Bank 2, Địa chỉ `0x01`, Độ rộng 8-bit.
* **Cấu hình dự án**: Giá trị `0x1B` (Hệ nhị phân: `0b00011011`).
* **Phân loại**: `PROJECT CONFIGURATION`.

![Hình E.2 — Bitfield thanh ghi GYRO_CONFIG_1](assets/fig_bitfield_gyro_config_1.png)  
*Hình E.2 — Cấu trúc bitfield chi tiết của thanh ghi GYRO_CONFIG_1 (Bank 2, Địa chỉ 0x01)*

| Bit | Tên Bitfield | Giá trị ghi | Chức năng theo Datasheet TDK DS-000189 §14.2 | Ý nghĩa cấu hình trong dự án |
|---|---|---|---|---|
| **Bits [7:6]** | `Reserved` | 00 | Các bit dành riêng của nhà sản xuất | Luôn ghi 00 theo quy định datasheet |
| **Bits [5:3]** | `GYRO_DLPFCFG[2:0]` | 011<br>(Số 3) | Chọn tần số cắt bộ lọc dải thông thấp số (DLPF):<br>011: 3dB Bandwidth = 51.2 Hz, Noise BW = 73.3 Hz (TDK DS-000189 Table 16) | Thiết lập băng thông lọc 51.2 Hz, làm suy giảm đáng kể dao động cơ học tần số cao |
| **Bits [2:1]** | `GYRO_FS_SEL[1:0]` | 01<br>(Số 1) | Cài đặt dải đo toàn thang con quay hồi chuyển:<br>00: ±250 °/s / 01: ±500 °/s<br>10: ±1000 °/s / 11: ±2000 °/s | Cài đặt dải đo toàn thang $\pm 500^{\circ}/\text{s}$, tối ưu cho cử động vung cổ tay người |
| **Bit 0** | `GYRO_FCHOICE` | 1 | 1: Kích hoạt bộ lọc số dải thông thấp DLPF<br>0: Bỏ qua bộ lọc DLPF | Cho phép tín hiệu đi qua bộ lọc số DLPF trước khi ghi vào thanh ghi dữ liệu |

* **Độ nhạy Gyroscope**: $\text{Sensitivity}_{\text{gyro}} = \frac{32768\,\text{LSB}}{500^{\circ}/\text{s}} = 65.536\,\text{LSB}/(^{\circ}/\text{s}) \approx 65.5\,\text{LSB}/(^{\circ}/\text{s})$.

## E.3. Thanh ghi ACCEL_CONFIG (Bank 2, Địa chỉ 0x14)

* **Vị trí**: User Bank 2, Địa chỉ `0x14`, Độ rộng 8-bit.
* **Cấu hình dự án**: Giá trị `0x1B` (Hệ nhị phân: `0b00011011`).
* **Phân loại**: `PROJECT CONFIGURATION`.

| Bit | Tên Bitfield | Giá trị ghi | Chức năng theo Datasheet TDK DS-000189 Table 18 | Ý nghĩa cấu hình trong dự án |
|---|---|---|---|---|
| **Bits [7:6]** | `Reserved` | 00 | Các bit dành riêng của nhà sản xuất | Luôn ghi 00 theo quy định datasheet |
| **Bits [5:3]** | `ACCEL_DLPFCFG[2:0]` | 011<br>(Số 3) | Chọn tần số cắt DLPF gia tốc kế (Table 18 — Accelerator Configuration):<br>011: 3dB Bandwidth = 50.4 Hz, Noise BW = 68.8 Hz | Thiết lập băng thông lọc 50.4 Hz để lọc thành phần dao động/nhiễu tần số cao trong tín hiệu gia tốc (DLPF của cảm biến không thay thế chống rung phím bấm bằng phần mềm) |
| **Bits [2:1]** | `ACCEL_FS_SEL[1:0]` | 01<br>(Số 1) | Cài đặt dải đo toàn thang gia tốc kế:<br>00: ±2g / 01: ±4g<br>10: ±8g / 11: ±16g | Cài đặt dải đo toàn thang $\pm 4g$, bao quát cả trọng trường $1g$ và gia tốc vung tay nhanh |
| **Bit 0** | `ACCEL_FCHOICE` | 1 | 1: Kích hoạt bộ lọc số dải thông thấp DLPF<br>0: Bỏ qua bộ lọc DLPF | Kích hoạt bộ lọc số phần cứng cho gia tốc kế |

* **Độ nhạy Accelerometer**: $\text{Sensitivity}_{\text{accel}} = \frac{32768\,\text{LSB}}{4g} = 8192\,\text{LSB}/g$.

## E.4. Trạng thái kiểm chứng các cấu hình thanh ghi

* **Trạng thái thực tế**: `MOCK_REGISTER_MODEL_TESTED / HARDWARE_READBACK_NOT_RUN`.
* **Bản chất kỹ thuật**: Trong Test Suite số 2 của host test (`#ifndef ARDUINO`), driver chạy trên mảng giả lập 4 bank thanh ghi:
  `static uint8_t s_mock_regs[4][256];`
  Toàn bộ chuỗi cấu hình `PWR_MGMT_1` (`0x01`), `GYRO_CONFIG_1` (`0x1B`), `ACCEL_CONFIG` (`0x1B`) và chuyển bank `REG_BANK_SEL` (`0x7F`) đã được kiểm thử tính đúng đắn logic của hàm driver trên mô hình giả lập này.
* **Giới hạn phạm vi**: Chưa thực hiện đọc lại (readback) trực tiếp từ chip ICM-20948 vật lý trên phần cứng thật trong mốc Tuần 5.

---
""")

    # -------------------------------------------------------------
    # PHẦN F
    # -------------------------------------------------------------
    md.append(r"""# PHẦN F — TỪ RAW DỮ LIỆU ĐẾN CON TRỎ CHUỘT (TOÁN HỌC & GIẢI THUẬT)

## F.1. Quy trình toán học từng bước (Burst 12-Byte, Bù Bias, Complementary Quaternion)

![Hình F.1 — Quy trình pipeline xử lý tín hiệu chuyển động](assets/fig_motion_pipeline.png)  
*Hình F.1 — Sơ đồ luồng xử lý tín hiệu phân định rõ ràng giữa Hardware DLPF và Firmware Engine*

Quy trình biến đổi dữ liệu toán học trong firmware được thực hiện qua các giai đoạn nghiêm ngặt:

### Bước 1: Đọc Burst 12-Byte và Ghép Số nguyên bù 2 (16-bit Signed Integer)
Cảm biến xuất dữ liệu dưới dạng số bù 2 có dấu 16-bit (Signed 16-bit 2's Complement), lưu trữ trong 2 thanh ghi 8-bit liên tiếp: Byte trọng số cao (High Byte) và Byte trọng số thấp (Low Byte).
Công thức ghép bit toán học:
$$\text{RawValue} = (\text{int16\_t}) \left( ((\text{uint16\_t})\text{Buffer}[\text{High}] \ll 8) \mid \text{Buffer}[\text{Low}] \right)$$
Giá trị số nguyên sau ghép nằm trong dải số học: $[-32768, +32767]$.

### Bước 2: Đổi sang Đơn vị Vật lý và Bù Sai số Lệch tĩnh (Zero-Rate Bias Compensation)
* Vận tốc góc thực tế của con quay:
  $$\omega_{\text{dps}} = \frac{\text{Raw}_{\text{gyro}} - \text{Bias}_{\text{gyro}}}{65.5} \quad (^{\circ}/\text{s})$$
* Gia tốc thực tế:
  $$a_{\text{g}} = \frac{\text{Raw}_{\text{accel}}}{8192.0} \quad (g)$$
* *Phương pháp tính Bias*: Khi khởi động thiết bị, người dùng giữ yên chuột trên mặt phẳng cố định trong khoảng thời gian $\approx 2\,\text{giây}$. Firmware đọc liên tiếp $N = 200$ mẫu, tính giá trị trung bình cộng để làm sai số lệch tĩnh:
  $$\text{Bias} = \frac{1}{N} \sum_{i=1}^{N} \text{Raw}_i$$

### Bước 3: Bộ lọc bù Quaternion 6 trục và Hệ quy chiếu thích nghi (Adaptive Reference Frame)
* Khi người dùng cầm chuột bay trên không, bàn tay luôn có xu hướng nghiêng tự nhiên (Roll và Pitch khác 0). Nếu ánh xạ trực tiếp trục cảm biến vào màn hình, chuyển động xoay ngang cổ tay sẽ làm con trỏ di chuyển chéo.
* Giải pháp: Firmware sử dụng bộ lọc bù Quaternion 6 trục (**6-axis Complementary Quaternion Filter**, hệ số hồi tiếp trọng trường $K = 2.0\,\text{s}^{-1}$, hằng số thời gian $\tau \approx 0.5\,\text{s}$) để ước lượng hướng trọng lực và tư thế không gian. Ma trận xoay thích nghi tự động chiếu vector vận tốc góc về mặt phẳng trực giao với màn hình máy tính:
  $$\vec{\omega}_{\text{screen}} = \mathbf{R}(\mathbf{q}) \cdot \vec{\omega}_{\text{sensor}}$$

### Bước 4: Vùng chết hai ngưỡng (Dual-Threshold Dead-Zone)
Để triệt tiêu hiện tượng rung sinh lý tự nhiên của tay người (Hand Tremor) mà vẫn đảm bảo độ nhạy khi rê chuột:
* **Dưới $0.8^{\circ}/\text{s}$**: Đầu ra hoàn toàn bằng 0 (triệt tiêu rung tay khi dừng ngắm mục tiêu).
* **Từ $0.8^{\circ}/\text{s}$ đến $1.4^{\circ}/\text{s}$**: Vùng chuyển tiếp tuyến tính mượt mà (Linear Transition Zone).
* **Trên $1.4^{\circ}/\text{s}$**: Áp dụng độ nhạy đầy đủ trừ đi thành phần chuyển tiếp để đường cong đáp ứng liên tục:
  $$\omega_{\text{out}} = \text{sign}(\omega) \cdot (|\omega| - 0.8^{\circ}/\text{s})$$
* *Ngưỡng nhận diện đứng yên (Stationary Detection)*: Độc lập với dead-zone điều khiển, ngưỡng $|\omega| < 1.2^{\circ}/\text{s}$ trên cả 3 trục được dùng để kích hoạt trạng thái chuột đứng yên và khóa trôi con trỏ.

### Bước 5: Nhân Gain Tuyến tính và Chặn biên Clamping (Linear Gain & Clamping)
Độ dịch chuyển con trỏ chuột trên 2 trục màn hình được tính toán:
$$\Delta X = \text{roundf}(K_x \cdot \omega_{\text{horizontal}}), \quad \Delta Y = \text{roundf}(-K_y \cdot \omega_{\text{vertical}})$$
* **Hệ số Gain**: $K_x = 2.2, K_y = 2.2$ (Phản hồi 1:1 trực quan, không dùng hàm phi tuyến hay số mũ 1.2).
* **Chặn biên Clamping**: Chuẩn HID quy định độ dịch chuyển chuột là số nguyên có dấu 8-bit (`int8_t`), do đó bắt buộc phải kẹp biên trong dải $[-127, +127]$:
  $$\Delta X_{\text{clamped}} = \max(-127, \min(127, \Delta X))$$

## F.2. Phân tích chuyên sâu về Định lý Nyquist và 4 Miền thời gian

* **Định lý lấy mẫu Nyquist-Shannon**: Tần số lấy mẫu ($f_s$) phải lớn hơn ít nhất 2 lần tần số cao nhất có ích của tín hiệu ($f_{\text{max}}$):
  $$f_s \ge 2 \cdot f_{\text{max}}$$
* Cử động xoay cổ tay của con người có dải tần số vật lý dao động từ $0.5\,\text{Hz}$ đến $8\,\text{Hz}$ (tần số vung tay tối đa hiếm khi vượt quá $12\,\text{Hz}$).
* Phân tích 4 miền thời gian trong hệ thống Air Mouse:
  1. **Miền phần cứng IMU (ODR)**: Bộ chia $\text{SMPLRT\_DIV} = 10 \Rightarrow \text{ODR} = \frac{1125\,\text{Hz}}{1 + 10} \approx 102.27\,\text{Hz}$ (Chu kỳ $\approx 9.78\,\text{ms}$).
  2. **Miền lấy mẫu Firmware**: Vòng lặp chính `loop()` polling với chu kỳ mục tiêu $\Delta t = 10\,\text{ms}$ ($100\,\text{Hz}$).
  3. **Miền truyền thông BLE HID**: Chu kỳ kết nối (Connection Interval) được thương lượng trong khoảng $10\text{--}15\,\text{ms}$ ($66.7\text{--}100\,\text{Hz}$).
  4. **Miền hiển thị màn hình máy tính**: Màn hình tiêu chuẩn hiển thị ở tần số $60\,\text{Hz}$ (chu kỳ làm tươi $\approx 16.6\,\text{ms}$).
* **Đánh giá đồng bộ**: Cả 4 miền thời gian đều được thiết kế quanh mốc $\approx 10\text{--}15\,\text{ms}$, đảm bảo dữ liệu chuyển động liên tục, không gây hiện tượng giật hình (stuttering) hay trễ tích lũy (buffering lag).

---
""")

    # -------------------------------------------------------------
    # PHẦN G
    # -------------------------------------------------------------
    md.append(r"""# PHẦN G — PHÂN HỆ TRUYỀN THÔNG BLE HID (BLUETOOTH LOW ENERGY)

## G.1. Kiến trúc HID over GATT Profile (HOGP)

* **Vì sao máy tính / điện thoại nhận diện được Air Mouse mà không cần cài đặt driver ngoài?**  
  Nhóm triển khai cấu hình theo đúng tiêu chuẩn công nghiệp **HID over GATT Profile (HOGP)** do hiệp hội Bluetooth SIG ban hành. HOGP ánh xạ chuẩn giao tiếp Human Interface Device (vốn chạy trên USB) sang tầng GATT (Generic Attribute Profile) của Bluetooth Low Energy. Mọi hệ điều hành hiện đại (Windows 10/11, macOS, Linux, Android, iOS) đều tích hợp sẵn driver HID tiêu chuẩn này.
* **Cấu trúc bảng dịch vụ GATT của Air Mouse**:
  * **Primary Service: Human Interface Device (`0x1812`)**: Quản lý trao đổi dữ liệu chuột.
  * **Primary Service: Battery Service (`0x180F`)**: Báo cáo mức năng lượng phần trăm pin.
  * **Primary Service: Device Information (`0x180A`)**: Cung cấp tên nhà sản xuất, phiên bản phần cứng/phần mềm.

## G.2. Bản tin báo cáo chuột (HID Mouse Report)

Cấu trúc bản tin 5 byte chuẩn được gửi từ ESP32 sang máy tính dưới dạng bản tin thông báo (GATT Notification):

![Hình G.1 — Cấu trúc chi tiết bản tin HID Mouse Report 5-Byte](assets/fig_ble_hid_report.png)  
*Hình G.1 — Cấu trúc chi tiết từng byte và từng bit trong bản tin BLE HID Mouse Report*

```
┌───────────────┬───────────────┬───────────────┬───────────────┬───────────────┐
│    Byte 0     │    Byte 1     │    Byte 2     │    Byte 3     │    Byte 4     │
│    Buttons    │   Delta X     │   Delta Y     │  Wheel (Cuộn) │   Pan (Ngang) │
│ (Bitmask 8-b) │ (int8_t 2's)  │ (int8_t 2's)  │ (int8_t 2's)  │ (int8_t 2's)  │
└───────────────┴───────────────┴───────────────┴───────────────┴───────────────┘
```

* **Byte 0 (Buttons)**: Mặt nạ bit thể hiện trạng thái các nút bấm (1 = Đang nhấn, 0 = Thả ra):
  * **Bit 0**: Nút chuột trái (`Left Button`).
  * **Bit 1**: Nút chuột phải (`Right Button`).
  * **Bit 2**: Nút chuột giữa (`Middle Button`).
  * **Bits [7:3]**: Các bit dự phòng mở rộng.
* **Byte 1 (Delta X)**: Độ dịch chuyển ngang của con trỏ chuột, biểu diễn dưới dạng số bù 2 có dấu `int8_t` (Dải giá trị từ $-127$ đến $+127$). Giá trị âm: di chuyển sang trái; Giá trị dương: di chuyển sang phải.
* **Byte 2 (Delta Y)**: Độ dịch chuyển dọc của con trỏ chuột (`int8_t`). Theo chuẩn HID máy tính: Giá trị âm: con trỏ di chuyển lên trên; Giá trị dương: con trỏ di chuyển xuống dưới.
* **Byte 3 (Wheel)**: Bước cuộn dọc của con lăn chuột (`int8_t`).
* **Byte 4 (Pan)**: Bước cuộn ngang màn hình (`int8_t`).

---
""")

    # -------------------------------------------------------------
    # PHẦN H
    # -------------------------------------------------------------
    md.append(r"""# PHẦN H — NGOẠI VI NÚT BẤM, ADC VÀ QUẢN LÝ NGUỒN PIN

## H.1. Nút bấm cơ khí và Quản lý chống rung phím (Edge-detected & Debounce)

* **Hiện tượng dội phím cơ học (Button Bouncing)**: Khi hai tiếp điểm kim loại bên trong nút nhấn cơ khí chạm nhau, do tính chất đàn hồi vật lý, chúng bật nhả liên tục trong khoảng thời gian $1\text{--}5\,\text{ms}$ tạo ra một chuỗi xung kích ảo trước khi ổn định hoàn toàn.
* **Cấu hình Active-Low**: Các chân GPIO25, 26, 27 được cấu hình chế độ ngõ vào có điện trở kéo lên nội bộ (`pinMode(pin, INPUT_PULLUP)`). Nút bấm nối một chân vào GPIO và chân còn lại nối mass GND. Khi nút được nhấn, chân bị kéo xuống mức $0\,\text{V}$ (mức LOW).
* **Phân biệt bắt cạnh và chống rung phần mềm**:
  * **Bắt cạnh (Edge Detection)**: Là phát hiện thời điểm chuyển trạng thái logic giữa hai chu kỳ quét (từ HIGH sang LOW khi nhấn). Bắt cạnh giúp phát hiện sự kiện tức thì nhưng không tự loại bỏ được rung nảy tiếp điểm cơ học.
  * **Chống rung phần mềm (Debounce)**: Là cơ chế lọc thời gian (khoảng $1\text{--}5\,\text{ms}$ hoặc $15\text{--}20\,\text{ms}$ là các giá trị tham khảo/đề xuất) để bỏ qua các dao động tiếp điểm thoáng qua.
  * **Trạng thái xử lý trong Firmware**:
    * Hiện tại: Firmware thực hiện nhận diện cạnh nhấn (Edge-detection) thông qua lưu giữ trạng thái nút ở chu kỳ trước (`CODE_IMPLEMENTED`).
    * Kế hoạch: Logic chống rung phím Software Debounce bằng `millis()` là hạng mục `PLANNED / NEEDS_IMPLEMENTATION`, sẽ được đo đạc và tinh chỉnh trên nút bấm thực tế.

## H.2. Mạch đo áp pin qua ADC1_CH6 (GPIO34)

* **Điện áp pin LiPo 1S**: Dao động từ $3.2\,\text{V}$ (cạn kiệt) đến $4.2\,\text{V}$ (khi sạc đầy).
* **Cầu phân áp điện trở**: Để đưa điện áp về ngưỡng an toàn của chân ADC ESP32 ($< 3.3\,\text{V}$), nhóm sử dụng 2 điện trở bằng nhau $R_1 = R_2 = 100\,\text{k}\Omega$:
  $$V_{\text{ADC}} = V_{\text{BAT}} \times \frac{R_2}{R_1 + R_2} = \frac{V_{\text{BAT}}}{2} \quad \Rightarrow \quad V_{\text{BAT}} = 2 \times V_{\text{ADC}}$$
  Khi pin sạc đầy $4.2\,\text{V}$, điện áp tại chân ADC là $2.1\,\text{V}$, nằm an toàn trong dải đo tuyến tính khi cấu hình suy hao $11\,\text{dB}$ (`ADC_ATTEN_DB_11`).
* **Trạng thái kỹ thuật**: Cầu phân áp đã được thiết kế trên sơ đồ nguyên lý mạch mang Carrier Board (`HARDWARE_DESIGNED`). Chân GPIO34 tuyệt đối tách biệt khỏi nguồn 5V VIN. Trong firmware V1, lệnh `analogRead(34)` chưa được gọi để ưu tiên kiểm thử ổn định giao tiếp I2C và pipeline chuyển động (`HARDWARE_DESIGNED / FIRMWARE_NOT_IMPLEMENTED`).

---
""")

    # -------------------------------------------------------------
    # PHẦN I
    # -------------------------------------------------------------
    md.append(r"""# PHẦN I — BẢNG ĐỐI CHIẾU CÁC QUYẾT ĐỊNH THIẾT KẾ (DESIGN TRADE-OFFS)

Khi giảng viên đặt câu hỏi: *"Tại sao nhóm lại làm cách A mà không làm cách B?"*, các thành viên sử dụng 7 đối chiếu kỹ thuật dưới đây theo chuẩn: **Ràng buộc $\rightarrow$ Đánh đổi kỹ thuật $\rightarrow$ Quyết định**:

### 1. ESP32 Classic vs STM32F4/F1
* **Ràng buộc**: Chuột bay cầm tay yêu cầu kết nối không dây BLE HID gọn nhẹ và thời lượng pin tốt.
* **Đánh đổi**: STM32 cần mua thêm module BLE ngoài (nRF52/HC-05), làm tăng diện tích PCB và khó cấu hình GATT.
* **Quyết định**: Chọn ESP32 Classic vì tích hợp sẵn phần cứng BLE v4.2 và CPU $240\,\text{MHz}$ lõi kép cực mạnh.

### 2. Giao tiếp I2C vs SPI
* **Ràng buộc**: Mạch mang Carrier Board 1 lớp tự gia công, ưu tiên số đường dây tối thiểu.
* **Đánh đổi**: SPI tốc độ cao nhưng tốn 4 dây (SCK, MOSI, MISO, CS), rất khó đi dây 1 lớp không bị cắt mass. I2C chỉ cần 2 dây (SDA, SCL), tốc độ Fast Mode $400\,\text{kHz}$ hoàn toàn thừa đáp ứng chu kỳ lấy mẫu chuột $100\,\text{Hz}$ (đọc burst 12 byte Accel & Gyro chỉ mất $\approx 0.38\,\text{ms}$, chiếm chưa tới $4\%$ chu kỳ $10\,\text{ms}$).
* **Quyết định**: Chọn giao tiếp I2C Fast Mode $400\,\text{kHz}$ cho phiên bản V1.

### 3. Tự viết driver thanh ghi mỏng vs Dùng thư viện trọn gói (SparkFun DMP)
* **Ràng buộc**: Báo cáo giữa kỳ yêu cầu giải thích tường minh cấu trúc thanh ghi và bitfield trước hội đồng.
* **Đánh đổi**: Thư viện SparkFun nạp firmware DMP nhị phân cồng kềnh (hơn 14 KB), biến cảm biến thành "hộp đen" và khó làm chủ chi tiết. Tự viết driver tốn công tra cứu datasheet nhưng kiểm soát chính xác 100% từng byte truyền và bộ nhớ chiếm dụng cực nhỏ.
* **Quyết định**: Tự viết driver thanh ghi mỏng `icm20948_driver` làm chủ toàn diện các thanh ghi cấu hình.

### 4. Dùng Gyroscope + Accel (6-axis Fusion) vs Dùng Accelerometer tích phân 2 lần
* **Ràng buộc**: Điều khiển vị trí con trỏ chuột trên màn hình 2D ổn định, không bị trôi tự do.
* **Đánh đổi**: Tích phân 2 lần gia tốc kế làm bùng nổ sai số theo hàm bình phương thời gian ($t^2$), con trỏ bay mất sau vài giây. Con quay Gyroscope đo trực tiếp vận tốc góc xoay cổ tay ($\omega$), nhân hệ số Gain ra pixel không cần tích phân.
* **Quyết định**: Tuyệt đối không dùng tích phân 2 lần gia tốc; sử dụng Gyroscope làm nguồn điều khiển chính, gia tốc kế neo Roll/Pitch qua bộ lọc bù Quaternion.

### 5. Vì sao không dùng Magnetometer (Từ kế) trong V1
* **Ràng buộc**: Môi trường văn phòng/phòng học chứa nhiều nguồn nhiễu từ trường (khung bàn sắt, loa máy tính, nguồn xung).
* **Đánh đổi**: Từ kế AK09916 cần thuật toán bù méo từ trường cứng/mềm phức tạp, nếu chưa hiệu chuẩn sẽ làm sai lệch hướng con trỏ chuột nghiêm trọng. Chuột máy tính chỉ cần điều khiển tương đối 2D.
* **Quyết định**: Tạm thời tắt từ kế ở V1 để tiết kiệm pin và tránh rung giật; bù trôi trục Yaw bằng cơ chế Clutch/Recenter.

### 6. Vì sao dùng 6-axis Complementary Quaternion thay vì Kalman Filter (EKF)
* **Ràng buộc**: Vòng lặp điều khiển $100\,\text{Hz}$ cần thực thi nhanh chóng, tránh quá tải CPU và tiết kiệm năng lượng.
* **Đánh đổi**: Extended Kalman Filter (EKF) đòi hỏi nhiều phép nhân ma trận hiệp phương sai phức tạp, tốn thời gian tính toán và tiêu tốn năng lượng pin. Bộ lọc bù Quaternion tính toán cực nhẹ mà vẫn triệt tiêu hoàn toàn hiện tượng Gimbal Lock.
* **Quyết định**: Sử dụng bộ lọc bù Quaternion 6 trục ($K = 2.0\,\text{s}^{-1}$, $\tau \approx 0.5\,\text{s}$).

### 7. Vì sao chọn GPIO34 (ADC1_CH6) để đo điện áp pin
* **Ràng buộc**: Đo chính xác điện áp pin LiPo mà không gây xung đột với module vô tuyến BLE.
* **Đánh đổi**: Bộ chuyển đổi SAR ADC2 bị khóa phần cứng khi Wi-Fi hoạt động. Chân GPIO34 thuộc khối SAR ADC1 hoàn toàn độc lập, đồng thời là chân Input-Only giúp bảo toàn các chân I/O đa năng.
* **Quyết định**: Chọn duy nhất chân GPIO34 (ADC1_CH6) cho mạch đo điện áp pin qua cầu phân áp $100\,\text{k}\Omega / 100\,\text{k}\Omega$.

---
""")

    # -------------------------------------------------------------
    # PHẦN J
    # -------------------------------------------------------------
    md.append(r"""# PHẦN J — CẨM NANG XỬ LÝ SỰ CỐ PHẦN CỨNG & PHẦN MỀM (TROUBLESHOOTING GUIDE)

Khi thực nghiệm mạch hoặc demo trước giảng viên, nếu gặp sự cố, thành viên bình tĩnh tra cứu 11 kịch bản xử lý lỗi sau:

| Mã lỗi / Hiện tượng | Nguyên nhân gốc rễ (Root Cause) | Quy trình kiểm tra & Khắc phục tức thì |
|---|---|---|
| **LỖI 1**: Đọc `WHO_AM_I` trả về `0x00` hoặc `0xFF` | Mất nguồn cảm biến, đứt đường I2C, cắm lỏng dây jumper hoặc cắm lệch hàng chân phải DevKit (chân TX0/RX0 nằm xen giữa GPIO22 và GPIO21) | 1. Dùng đồng hồ VOM đo điện áp tại chân VCC module (đủ $3.3\,\text{V}$).<br>2. Kiểm tra cắm đúng chân GPIO21 (SDA), GPIO22 (SCL), tránh cắm nhầm hàng chân TX0/RX0.<br>3. Kiểm tra tiếp xúc dây cắm jumper và trở kéo $10\,\text{k}\Omega$ onboard.<br>4. Nạp I2C scanner để dò lại địa chỉ $0\text{x}68$. |
| **LỖI 2**: Bus I2C bị treo cứng (Bus Lockup / SCL kẹt LOW) | Slave bị mất nguồn giữa chừng khi đang kéo chân SDA/SCL xuống LOW | Nạp hàm phục hồi bus I2C: Cấu hình SCL làm GPIO Output, phát thủ công 9 xung clock để Slave nhả đường SDA, sau đó phát điều kiện STOP. |
| **LỖI 3**: Nạp firmware báo lỗi "A fatal error occurred: Timed out waiting for packet header" | Chân GPIO0 không được kéo xuống mass lúc nạp, hoặc mạch nạp tự động lỗi | Nhấn giữ nút `BOOT` (GPIO0) trên ESP32 DevKit, bấm nhả nút `EN` (Reset), sau đó mới bấm nút Upload trên máy tính. |
| **LỖI 4**: Con trỏ chuột tự trôi liên tục khi đặt im trên bàn (Cursor Drift) | Chưa trừ sai số độ lệch tĩnh (Zero-Rate Bias) hoặc ngưỡng Dead-zone quá thấp | 1. Giữ chuột hoàn toàn bất động trong 2 giây đầu khi vừa khởi động để tính lại Bias.<br>2. Tăng ngưỡng Dead-zone từ $0.8^{\circ}/\text{s}$ lên $1.2^{\circ}/\text{s}$. |
| **LỖI 5**: Con trỏ chuột bị giật cục khi rê chậm (Jitter) | Dải đo toàn thang đặt quá lớn ($\pm 2000^{\circ}/\text{s}$) làm giảm độ nhạy | Kiểm tra thanh ghi `GYRO_CONFIG_1` (`0x01` Bank 2): Đảm bảo các bit `GYRO_FS_SEL` ghi giá trị `01` (dải $\pm 500^{\circ}/\text{s}$, độ nhạy $65.5\,\text{LSB}/(^{\circ}/\text{s})$) và bật DLPF. |
| **LỖI 6**: Nhấn nút chuột 1 lần nhưng máy tính nhận cú đúp (Double-click ảo) | Hiện tượng dội phím cơ học (Switch Bouncing) | Kích hoạt bộ lọc chống rung phần mềm: Bổ sung biến kiểm tra thời gian `millis() - last_press_time > 20ms`. |
| **LỖI 7**: Máy tính không tìm thấy thiết bị Bluetooth Air Mouse | Ngăn xếp BLE chưa khởi động, hoặc đang kẹt kết nối với máy tính khác | 1. Kiểm tra Serial Monitor xem có log "BLE Advertising started".<br>2. Quên thiết bị (Forget Device) trên máy tính cũ nếu đã từng kết nối trước đó. |
| **LỖI 8**: ESP32 bị sập nguồn liên tục khi bật Bluetooth (Brownout Reset) | Nguồn cấp USB hoặc nguồn pin không đủ dòng tức thời cho khối RF ($> 250\,\text{mA}$) | Bổ sung tụ hóa dung lượng $100\,\mu\text{F} \text{ đến } 470\,\mu\text{F}$ song song với tụ gốm $100\,\text{nF}$ ngay sát chân $3.3\,\text{V}$ và GND của ESP32. |
| **LỖI 9**: Xoay cổ tay sang ngang nhưng con trỏ chuột lại chạy dọc màn hình | Ánh xạ sai trục con quay hồi chuyển trong firmware | Đổi trục trong công thức: Đổi $\omega_z$ sang $\omega_y$ hoặc nhân thêm dấu âm $-1$ để đảo ngược chiều trục tọa độ. |
| **LỖI 10**: Cảm biến nóng ran bất thường | Cấp nhầm chân $5\,\text{V}$ vào module, hoặc cắm ngược cực nguồn | Ngắt nguồn lập tức! Kiểm tra chân cấp nguồn module WCMCU-20948 chỉ được nối chân 3V3 của ESP32, tuyệt đối không dùng chân 5V. |
| **LỖI 11**: Đọc điện áp pin ADC trả về giá trị 0 hoặc nhảy loạn xạ | Chân GPIO34 bị chạm chập, hoặc sai cấu hình suy hao `ADC_ATTEN_DB_11` | Kiểm tra cầu phân áp $100\,\text{k}\Omega / 100\,\text{k}\Omega$, đảm bảo điện áp tại chân GPIO34 nằm trong khoảng $1.6\text{--}2.1\,\text{V}$. |

---
""")

    # -------------------------------------------------------------
    # PHẦN K
    # -------------------------------------------------------------
    md.append(r"""# PHẦN K — BẢNG TỔNG HỢP RESEARCH GAPS CÒN LẠI (HẠNG MỤC CẦN KIỂM CHỨNG)

Báo cáo trung thực và minh bạch về các hạng mục nghiên cứu còn lại cần tiếp tục thực nghiệm trong giai đoạn 2 (Tuần 6 đến Cuối kỳ):

| STT | Hạng mục kỹ thuật | Trạng thái hiện tại (Tuần 5) | Kế hoạch thực nghiệm Giai đoạn 2 (Cuối kỳ) | Mức độ rủi ro |
|---|---|---|---|---|
| **GAP 1** | Đo kiểm thực tế bus I2C bằng Logic Analyzer | Mới kiểm tra logic trên firmware và mô hình thanh ghi giả lập host test (`MOCK_REGISTER_MODEL_TESTED / HARDWARE_READBACK_NOT_RUN`) | Bắt dạng sóng thực tế trên chân SDA/SCL để đo chính xác Rise Time, Fall Time và kiểm chứng xung ACK vật lý | Thấp |
| **GAP 2** | Kiểm chứng chống rung phím cơ học bằng phần mềm | Mới nhận diện cạnh nhấn (Edge-detection), chưa chạy debounce timer trên nút thật | Đo thời gian dội tiếp điểm của nút nhấn thực tế bằng máy hiện sóng, tinh chỉnh tham số debounce $15\text{--}20\,\text{ms}$ | Thấp |
| **GAP 3** | Đọc ADC đo điện áp pin trên phần cứng thật | Đã thiết kế cầu phân áp trên schematic, chưa gọi hàm đọc trong firmware | Lập trình hàm đọc `analogRead(34)` với hiệu chuẩn `esp_adc_cal`, ánh xạ đường cong xả pin LiPo | Trung bình |
| **GAP 4** | Gia công và hàn lắp bo mạch mang Carrier Board | Đang hoàn thiện bố cục cơ khí và layout PCB 1 lớp | Gia công bo mạch, hàn linh kiện, đo thông mạch và kiểm tra an toàn chạm chập trước khi cắm module | Cao |
| **GAP 5** | Tinh chỉnh thuật toán thích nghi hệ quy chiếu | Đã viết code và test toán học trên máy tính | Thử nghiệm người dùng thực tế vung tay ở các tư thế ngồi/đứng khác nhau để tinh chỉnh hệ số Gain $K$ | Trung bình |
| **GAP 6** | Tối ưu hóa dòng tiêu thụ và chế độ Deep Sleep | Hệ thống đang chạy ở chế độ bình thường liên tục | Lập trình tự động chuyển ESP32 vào chế độ Deep Sleep khi chuột không chuyển động quá 60 giây | Trung bình |

---
""")

    # -------------------------------------------------------------
    # PHẦN L — NGÂN HÀNG 36 CÂU HỎI VẤN ĐÁP
    # -------------------------------------------------------------
    md.append(r"""# PHẦN L — NGÂN HÀNG 36 CÂU HỎI VẤN ĐÁP BẢO VỆ GIỮA KỲ (Q&A DEFENSE BANK)

Toàn bộ 36 câu hỏi dưới đây được chuẩn hóa và phân chia theo 12 nhóm chủ đề kỹ thuật cốt lõi, trang bị đầy đủ câu trả lời trực diện (15–30 giây), giải thích chuyên sâu, từ khóa cốt lõi và nguồn tài liệu trích dẫn để cả 3 thành viên tự tin bảo vệ đề tài trước hội đồng:
""")

    qa_path = 'docs/MIDTERM_QA_BANK.md'
    if os.path.exists(qa_path):
        with open(qa_path, 'r', encoding='utf-8') as fp:
            qa_content = fp.read()
        nhom_start = qa_content.find("## NHÓM 1:")
        if nhom_start != -1:
            qa_body = qa_content[nhom_start:]
            md.append(qa_body)
        else:
            md.append(qa_content)

    # -------------------------------------------------------------
    # PHẦN M — CHEAT SHEET
    # -------------------------------------------------------------
    md.append(r"""
---

# PHẦN M — CHEAT SHEET 2 TRANG TÓM TẮT TRỌNG TÂM (IN 2 MẶT A4 TRƯỚC GIỜ BẢO VỆ)

Phần tóm lược ngắn gọn nhất toàn bộ thông số kỹ thuật cốt lõi của đề tài, thiết kế để 3 thành viên có thể in ra 2 mặt của một tờ giấy A4 để xem lại nhanh trong 5 phút trước khi bước vào phòng vấn đáp:

> [!NOTE]
> ### CHEAT SHEET — MẶT TRƯỚC: THÔNG SỐ VÀ THANH GHI CỐT LÕI
> 
> **1. BẢN CHẤT HỆ THỐNG:**
> * **Kiến trúc cốt lõi**: **Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion**.
> * **Relative Rate-Controlled Pointing Device**: Con trỏ di chuyển tỉ lệ thuận với vận tốc góc **XOAY cổ tay** ($\omega$).
> * Ngay cả khi bàn tay không tịnh tiến trong không gian, cổ tay xoay vẫn tạo ra $\omega$ và di chuyển chuột. Dừng xoay cổ tay ($\omega \approx 0$) $\rightarrow$ Con trỏ dừng ngay lập tức. **KHÔNG** định vị 3D tuyệt đối, **KHÔNG** dùng gia tốc kế tích phân 2 lần (sai số trôi bùng nổ theo $t^2$).
> 
> **2. PHẦN CỨNG & BỐ TRÍ CHÂN (CURRENT DESIGN / PROVISIONAL):**
> * **I2C SDA**: GPIO21  |  **I2C SCL**: GPIO22 (Fast Mode $\le 400\,\text{kHz}$, trở kéo $4.7\,\text{k}\Omega$ lên $3.3\,\text{V}$ và $10\,\text{k}\Omega$ lên $1.8\,\text{V}$).
> * **NÚT BẤM**: `BTN_LEFT` (GPIO25), `BTN_RIGHT` (GPIO26), `BTN_MODE` (GPIO27) — Cấu hình `INPUT_PULLUP` Active-Low.
> * **CHỈ THỊ**: `LED_STATUS` (GPIO32) qua trở hạn dòng $1.0\,\text{k}\Omega$.
> * **ĐO PIN**: `BAT_SENSE` (GPIO34 / ADC1_CH6) — Chân Input-Only, thuộc ADC1 tránh xung đột Wi-Fi, cầu phân áp $100\,\text{k}\Omega / 100\,\text{k}\Omega$. Chân ADC hoàn toàn tách biệt với nguồn 5V VIN. Trạng thái: `HARDWARE_DESIGNED / FIRMWARE_NOT_IMPLEMENTED`.
> * **CẤM DÙNG / TRÁNH NÚT BẤM**: GPIO6-11 (Flash nội cấm dùng); GPIO0, 2, 12, 15 (Strapping pins tránh nút bấm để loại trừ rủi ro boot failure).
> 
> **3. BA THANH GHI CỐT LÕI CỦA ICM-20948 (TDK DS-000189):**
> * **`PWR_MGMT_1` (User Bank 0, Địa chỉ `0x06`) = `0x01` (`0b00000001`):**
>   - Bit 7: `DEVICE_RESET = 0` (Bình thường)
>   - Bit 6: `SLEEP = 0` (Thoát chế độ ngủ mặc định, đánh thức chip)
>   - Bit 5: `LP_EN = 0` (Tắt chế độ tiết kiệm năng lượng, đo liên tục)
>   - Bit 4: `Reserved = 0` (Bit dành riêng)
>   - Bit 3: `TEMP_DIS = 0` (Bật cảm biến nhiệt độ nội)
>   - Bits [2:0]: `CLKSEL = 001` (Tự động chọn nguồn xung PLL tốt nhất, dự phòng dao động nội)
> * **`GYRO_CONFIG_1` (User Bank 2, Địa chỉ `0x01`) = `0x1B` (`0b00011011`):**
>   - Bits [7:6]: `Reserved = 00`
>   - Bits [5:3]: `GYRO_DLPFCFG = 011` (DLPF 51.2 Hz, Noise BW 73.3 Hz theo Table 16)
>   - Bits [2:1]: `GYRO_FS_SEL = 01` (Dải đo con quay hồi chuyển $\pm 500^{\circ}/\text{s}$)
>   - Bit 0: `GYRO_FCHOICE = 1` (Kích hoạt bộ lọc số DLPF)
> * **`ACCEL_CONFIG` (User Bank 2, Địa chỉ `0x14`) = `0x1B` (`0b00011011`):**
>   - Bits [5:3]: `ACCEL_DLPFCFG = 011` (DLPF 50.4 Hz, Noise BW 68.8 Hz theo Table 18 — Accelerator Configuration)
>   - Bits [2:1]: `ACCEL_FS_SEL = 01` (Dải đo gia tốc $\pm 4g$)
>   - Bit 0: `ACCEL_FCHOICE = 1` (Kích hoạt bộ lọc số DLPF gia tốc)
> * **Trạng thái kiểm chứng**: `MOCK_REGISTER_MODEL_TESTED / HARDWARE_READBACK_NOT_RUN` (kiểm thử trên mảng giả lập `s_mock_regs[4][256]`, chưa đọc lại từ chip vật lý).
> 
> **4. CƠ CHẾ CHUYỂN USER BANK:**
> * Thanh ghi `REG_BANK_SEL` tại địa chỉ `0x7F` (cố định trên cả 4 Bank).
> * Ghi `0x00` (Bank 0)  |  `0x10` (Bank 1)  |  `0x20` (Bank 2)  |  `0x30` (Bank 3).

> [!TIP]
> ### CHEAT SHEET — MẶT SAU: TOÁN HỌC, PIPELINE VÀ 5 CÂU HỎI BẮT BUỘC
> 
> **5. CÔNG THỨC TOÁN HỌC & ĐỘ NHẠY:**
> * Độ nhạy Gyroscope $\pm 500^{\circ}/\text{s}$: $\text{Sensitivity} = 65.5\,\text{LSB} / (^{\circ}/\text{s})$ ($32768 / 500$).
> * Độ nhạy Accelerometer $\pm 4g$: $\text{Sensitivity} = 8192\,\text{LSB} / g$ ($32768 / 4$).
> * Đổi Gyro sang vận tốc góc: $\omega = (\text{Raw} - \text{Bias}) / 65.5$ ($^{\circ}/\text{s}$).
> * Tần số ODR: $\text{ODR} = \frac{1125\,\text{Hz}}{1 + \text{DIV}} = \frac{1125}{1 + 10} \approx 102.27\,\text{Hz}$ ($\approx 9.78\,\text{ms}$).
> * Tính pixel: $\Delta X = \text{roundf}(K_x \cdot \omega_z), \quad \Delta Y = \text{roundf}(-K_y \cdot \omega_y)$ ($K_x = K_y = 2.2$).
> * Kẹp biên Clamping: $\max(-127, \min(127, \Delta X))$ (theo chuẩn HID `int8_t`).
> 
> **6. NĂM CÂU HỎI THẦY CHẮC CHẮN HỎI VÀ CÂU TRẢ LỜI NGẮN GỌN:**
> 1. *Tại sao không tích phân 2 lần gia tốc kế?*  
>    $\rightarrow$ Do sai số tĩnh bias tích lũy bùng nổ theo bình phương thời gian ($t^2$), con trỏ bay mất sau vài giây. Con quay đo trực tiếp vận tốc góc xoay nhân Gain ra pixel không cần tích phân.
> 2. *Thanh ghi `PWR_MGMT_1` ghi `0x01` để làm gì?*  
>    $\rightarrow$ Bit 6=0 để thoát chế độ Sleep (đánh thức chip) và Bits [2:0]=001 để tự động khóa xung vào bộ dao động PLL chất lượng cao.
> 3. *Thanh ghi `GYRO_CONFIG_1` ghi `0x1B` gồm những bit nào?*  
>    $\rightarrow$ Bit 0=1 bật DLPF; Bits [5:3]=011 chọn tần số cắt DLPF 51.2 Hz; Bits [2:1]=01 chọn dải đo $\pm 500^{\circ}/\text{s}$ (độ nhạy 65.5 LSB/(°/s)).
> 4. *Repeated START trong I2C là gì và tại sao dùng?*  
>    $\rightarrow$ Là điều kiện START phát lại khi đường SCL đang giữ quyền kiểm soát mà không phát STOP; giúp đảo chiều giao dịch từ Ghi địa chỉ thanh ghi sang Đọc dữ liệu an toàn mà không bị thiết bị khác chen ngang bus.
> 5. *Đề tài này có phải chuột 3D VR không?*  
>    $\rightarrow$ Không! Đây là thiết bị trỏ tương đối điều khiển theo tốc độ xoay cổ tay 2D (Relative Rate-Controlled Pointing Device), tối ưu cho thuyết trình và Smart TV.
""")

    # -------------------------------------------------------------
    # PHẦN N — BẢN ĐỒ DÀN Ý 10 SLIDE
    # -------------------------------------------------------------
    md.append(r"""
---

# PHẦN N — BẢN ĐỒ DÀN Ý CHUẨN BỊ SLIDE THUYẾT TRÌNH (10 SLIDES CHUẨN)

Nhóm không tạo file PowerPoint trong task này, nhưng chuẩn bị sẵn cấu trúc dàn ý 10 Slide thuyết trình chuẩn mực để các thành viên tự thiết kế slide sau đó:

| Số thứ tự Slide | Tiêu đề & Nội dung cốt lõi | Hình ảnh / Sơ đồ đề xuất | ĐIỀU CẤM KỴ TUYỆT ĐỐI |
|---|---|---|---|
| **Slide 1** | **Đặt vấn đề & Mục tiêu đề tài**<br>• Giới thiệu đề tài: Air Mouse BLE HID dùng ESP32 + ICM-20948.<br>• Nêu bật bản chất: Relative Rate-Controlled Pointing Device.<br>• Mục tiêu: Thuyết trình, Smart TV, hỗ trợ người khuyết tật vận động. | Hình ảnh mô phỏng thao tác vung cổ tay điều khiển con trỏ chuột. | **TUYỆT ĐỐI KHÔNG** ghi "định vị tuyệt đối 3D" hoặc hình ảnh kính thực tế ảo VR 6DOF. |
| **Slide 2** | **Sơ đồ kiến trúc toàn hệ thống**<br>• Dòng luồng dữ liệu từ Cổ tay $\rightarrow$ IMU $\rightarrow$ ESP32 $\rightarrow$ BLE HID $\rightarrow$ PC.<br>• Nêu rõ vai trò của từng khối linh kiện (12-byte burst read, 6-axis Complementary Quaternion). | Sơ đồ khối toàn hệ thống (Hình 1.1 / Hình A.1). | Không vẽ sơ đồ nguyên lý mạch quá chi tiết ở slide này. |
| **Slide 3** | **Thiết kế phần cứng & Phân bổ GPIO**<br>• Bảng phân loại ngoại vi ESP32 vs Thiết bị ngoài ICM-20948.<br>• Bảng chân GPIO (SDA 21, SCL 22, BTN 25/26/27, LED 32 trở $1.0\,\text{k}\Omega$, ADC 34).<br>• Giải thích lý do chọn GPIO34 (Input-only, ADC1_CH6). | Hình chụp bo mạch ESP32 DevKit 38-pin và module WCMCU-20948. | Không đưa các chân strapping pins vào danh sách sử dụng cho nút bấm. |
| **Slide 4** | **Giao tiếp I2C & Cơ chế Open-Drain**<br>• ESP32 Master, ICM-20948 Slave (Địa chỉ `0x68` AD0=0).<br>• Cực máng để hở Open-Drain và điện trở kéo pull-up.<br>• Chuỗi giao dịch đọc thanh ghi với Repeated START. | Sơ đồ chuỗi xung giao dịch I2C (Hình 4.1 / Hình C.1). | Không đi quá sâu vào thông số thời gian rise-time/fall-time. |
| **Slide 5** | **Cảm biến ICM-20948 & Kiến trúc User Bank**<br>• IMU 9-DOF, phiên bản V1 tập trung con quay hồi chuyển 3 trục và gia tốc kế 3 trục.<br>• Lý do chip phân chia thành 4 User Bank (không gian địa chỉ 512 byte [4 x 128], ~80-100 thanh ghi hoạt động).<br>• Cơ chế chuyển Bank qua thanh ghi đặc biệt `REG_BANK_SEL` (`0x7F`). | Sơ đồ 4 User Bank và thanh ghi `REG_BANK_SEL` (Hình 5.1 / Hình D.1). | Không nói rằng I2C chỉ có 7-bit register address. |
| **Slide 6** | **Phân tích các thanh ghi cốt lõi (Trọng tâm nhất)**<br>• `PWR_MGMT_1` (Bank 0, `0x06`) = `0x01` (Thoát Sleep, khóa xung PLL).<br>• `GYRO_CONFIG_1` (Bank 2, `0x01`) = `0x1B` (DLPF 51.2Hz, Dải đo $\pm 500^{\circ}/\text{s}$).<br>• `ACCEL_CONFIG` (Bank 2, `0x14`) = `0x1B` (DLPF 50.4Hz, Dải đo $\pm 4g$). | Sơ đồ trực quan 8-bit của các thanh ghi (Hình 6.1 và 6.2). | Không ghi sai vị trí bit `TEMP_DIS` (Bit 3) và `Reserved` (Bit 4). |
| **Slide 7** | **Pipeline xử lý dữ liệu từ Raw đến Con trỏ**<br>• Burst Read 12-byte $\rightarrow$ Đổi đơn vị vật lý (/65.5 và /8192) $\rightarrow$ Bù Bias tĩnh.<br>• Bộ lọc bù Quaternion 6 trục ($K=2.0\,\text{s}^{-1}$) $\rightarrow$ Adaptive Frame $\rightarrow$ Dead-zone $\rightarrow$ Gain & Clamping.<br>• Giải thích vì sao chọn Complementary Quaternion thay vì Kalman Filter. | Sơ đồ Pipeline xử lý tín hiệu (Hình 8.1 / Hình F.1). | Không đưa các ma trận hiệp phương sai phức tạp của Kalman. |
| **Slide 8** | **Danh mục lệnh và API điều khiển ngoại vi**<br>• Bảng đối chiếu lệnh: Input, Return Value, Hardware Effect.<br>• Phân định 2 nhóm thao tác: Ghi cấu hình vs Đọc dữ liệu.<br>• Vai trò HAL của `Wire.h` và driver mỏng `icm20948_driver`. | Bảng đối chiếu API rút gọn (Bảng 9.1 trong báo cáo). | Không copy-paste toàn bộ file mã nguồn C/C++ lên slide. |
| **Slide 9** | **Tiến độ thực nghiệm & Các mốc Demo giữa kỳ**<br>• Các mốc thử nghiệm chức năng (`WHO_AM_I`, `PWR_MGMT_1`, Burst 12B, Unit Test 10/10 PASS, PIO Build).<br>• Báo cáo trạng thái minh bạch: `CODE_IMPLEMENTED`, `MOCK_REGISTER_MODEL_TESTED`, `COMPILE_VERIFIED`, `NEEDS_HARDWARE_TEST`. | Bảng tiến độ Milestone hoặc video ngắn quay màn hình đọc Serial. | Không tuyên bố tính năng đã chạy thật trên mạch vật lý nếu chưa nạp thử nghiệm. |
| **Slide 10** | **Đánh giá kết quả & Kế hoạch giai đoạn 2**<br>• Tóm tắt kết quả nghiên cứu giữa kỳ Tuần 5.<br>• Kế hoạch cuối kỳ: Firmware bring-up mạch thật, hoàn thiện BLE HID, làm mạch in PCB.<br>• Lời cảm ơn và mời thầy đặt câu hỏi vấn đáp. | Lộ trình Gantt chart hoặc danh sách các đầu việc giai đoạn 2. | Không kết luận hời hợt hoặc đưa ra các mốc thời gian phi thực tế. |

---
""")

    # -------------------------------------------------------------
    # PHẦN O — GỢI Ý PHÂN CÔNG
    # -------------------------------------------------------------
    md.append(r"""# PHẦN O — GỢI Ý PHÂN CÔNG NHIỆM VỤ VÀ PHỐI HỢP 3 THÀNH VIÊN

Để việc chuẩn bị slide và ôn thi vấn đáp đạt hiệu quả cao nhất, nhóm đề xuất phương án phân công chuyên sâu theo thế mạnh từng người, nhưng vẫn đảm bảo khối kiến thức chung bắt buộc cả 3 cùng nắm vững:

> [!NOTE]
> ### PHÂN CÔNG CHUYÊN SÂU THEO THẾ MẠNH TỪNG THÀNH VIÊN
> 
> * **THÀNH VIÊN 1 (Chuyên trách Phần cứng & ESP32):**
>   - **Trách nhiệm thuyết trình**: Slide 1, Slide 2, Slide 3, Slide 10.
>   - **Chuyên môn bảo vệ**: Kiến trúc ESP32, quy tắc chân GPIO, strapping pins, ADC1_CH6, mạch phân áp pin LiPo, khối nguồn MT3608 và LDO 3.3V trên board DevKit (loại bỏ BSS138 và LDO 1.8V).
> * **THÀNH VIÊN 2 (Chuyên trách Giao tiếp I2C & Cảm biến ICM-20948):**
>   - **Trách nhiệm thuyết trình**: Slide 4, Slide 5, Slide 6.
>   - **Chuyên môn bảo vệ**: Giao thức I2C, Open-Drain, địa chỉ `0x68`, Repeated START, 4 User Bank, thanh ghi `REG_BANK_SEL` (`0x7F`), phân tích chi tiết từng bit của `PWR_MGMT_1`, `GYRO_CONFIG_1`, `ACCEL_CONFIG`.
> * **THÀNH VIÊN 3 (Chuyên trách Xử lý tín hiệu, BLE HID & Demo):**
>   - **Trách nhiệm thuyết trình**: Slide 7, Slide 8, Slide 9.
>   - **Chuyên môn bảo vệ**: Đổi đơn vị $65.5\,\text{LSB}/(^{\circ}/\text{s})$ và $8192\,\text{LSB}/g$, bù trừ Bias, vị trí Hardware DLPF, Bộ lọc bù Quaternion 6 trục, Dead-zone, ánh xạ trục, bản tin BLE HID Report, danh mục API Input/Output và demo thực nghiệm.

> [!IMPORTANT]
> ### KHỐI KIẾN THỨC BẮT BUỘC CẢ 3 THÀNH VIÊN ĐỀU PHẢI NẮM VỮNG
> 
> Dù được phân công phần nào, bất kỳ thành viên nào khi được giảng viên chỉ định đột xuất đều **PHẢI** trả lời trôi chảy 5 câu hỏi sau:
> 1. **Đề tài đang làm gì?** $\rightarrow$ Bản chất là thiết bị trỏ tương đối điều khiển theo tốc độ xoay cổ tay (Rate-Control), không tracking 3D, không VR controller.
> 2. **Dòng dữ liệu từ chuyển động xoay cổ tay đến con trỏ chuột trên màn hình đi qua các khối nào?** (10 bước tuần tự).
> 3. **Bus I2C là gì? Tại sao cần điện trở kéo pull-up? Địa chỉ cảm biến là bao nhiêu?**
> 4. **Thanh ghi `PWR_MGMT_1` ghi giá trị `0x01` để làm gì? `GYRO_CONFIG_1` ghi `0x1B` để làm gì? `ACCEL_CONFIG` ghi `0x1B` để làm gì?**
> 5. **Tại sao dùng con quay hồi chuyển Gyroscope mà không dùng gia tốc kế Accelerometer tích phân 2 lần?**

---
""")

    content = "".join(md)
    output_path = "deliverables/CAM_NANG_KIEN_THUC_AIR_MOUSE_MIDTERM.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Handbook Markdown updated and generated successfully at: {output_path}")

if __name__ == '__main__':
    generate_handbook_markdown()
