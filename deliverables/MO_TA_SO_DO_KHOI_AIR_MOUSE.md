# ĐẶC TẢ VÀ MÔ TẢ SƠ ĐỒ KHỐI HỆ THỐNG AIR MOUSE DIRECT 3.3V
## HƯỚNG DẪN THIẾT KẾ ĐỒ HỌA CHO THÀNH VIÊN VẼ HÌNH

> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Kiến trúc phần cứng**: V4.0.0 — Direct 3.3V Baseline (ESP32 DevKit 38-pin + WCMCU-20948)  
> **Mục đích tài liệu**: Cung cấp đặc tả kiến trúc bằng lời, sơ đồ khối dạng ký tự ASCII chuẩn hóa, và các chỉ dẫn bố cục đồ họa để thành viên phụ trách vẽ hình (sử dụng draw.io, Visio, Illustrator hoặc PowerPoint) tự tạo hình ảnh sơ đồ khối rõ đẹp, đạt chuẩn báo cáo học thuật mà không làm sai lệch bản chất kỹ thuật.  
> **Cam kết kỹ thuật**: Không vẽ mạch chuyển mức BSS138, không vẽ nguồn 1.8V, không tách từ kế AK09916 thành module rời bên ngoài, thể hiện đúng bản tin chuột BLE HID là 5 byte và trạng thái kết nối máy tính là `NOT_TESTED`.

---

## 1. Mô Tả Bằng Lời Từng Khối Chức Năng

Sơ đồ khối hệ thống Air Mouse được cấu thành từ 6 khối chức năng cốt lõi:

### 1.1 Khối Nguồn (Power Management Subsystem)
- **Cấu hình & Luồng năng lượng**:
  - Nguồn cấp khởi đầu từ một cell **Pin LiPo 1S** điện áp danh định $3.7\,\text{V}$ (dải làm việc $3.0\text{--}4.2\,\text{V}$, dung lượng $1000\,\text{mAh}$).
  - Cực Cell (+) nối vào chân `B+` của **Module sạc & bảo vệ TP4056**, cực Cell (-) nối vào chân `B-` của module. Cổng Type-C nhận nguồn 5V ngoài khi cắm sạc.
  - Cụm IC giám sát DW01A và Dual MOSFET FS8205A bảo vệ quá nạp ($> 4.2\,\text{V}$), quá xả ($< 2.4\,\text{V}$) và bảo vệ ngắn mạch đầu ra.
  - Ngõ `B-` không nối trực tiếp với `OUT-` hoặc system GND bên ngoài module để tránh bypass MOSFET bảo vệ.
  - Ngõ ra `OUT+` của TP4056 nối vào tiếp điểm ON của **Công tắc nguồn gạt (SW1)**. Chân COM của SW1 nối vào đường dương `V_SYS` cấp tới chân `VIN+` của MT3608. Tiếp điểm còn lại của SW1 để hở (NC).
  - Ngõ ra `OUT-` của TP4056 là điểm gốc của **System GND**, nối thông trực tiếp: `OUT- → system GND → MT3608 VIN-`. Không đưa OUT- qua công tắc.
  - **Module tăng áp DC-DC Boost MT3608** nâng điện áp dao động của pin lên mức điện áp cố định **$5,0\,\text{V}$** ổn định.
  - Mức nguồn $5,0\,\text{V}$ này được cấp vào chân `VIN` (hoặc `5V`) của bo ESP32 Classic DevKit 38-pin kèm tụ hóa bù nguồn $C_2 = 10\,\mu\text{F}$.
  - IC ổn áp tuyến tính (LDO onboard) gắn sẵn trên bo ESP32 DevKit hạ áp từ $5,0\,\text{V}$ xuống **$3,3\,\text{V}$** sạch để cấp nguồn nuôi cho chip vi điều khiển ESP32 và cấp trực tiếp cho chân `VCC` của module cảm biến WCMCU-20948.
  - *Lưu ý quan trọng*: Hệ thống đã loại bỏ hoàn toàn IC LDO AMS1117-1.8V và mạng nguồn 1V8.

### 1.2 Khối Cảm Biến Chuyển Động (Motion Sensing Subsystem)
- **Cấu hình phần cứng**:
  - Sử dụng module cảm biến thương phẩm **WCMCU-20948**, mang trên bo chip IMU 9 trục **InvenSense ICM-20948**.
  - Phần cứng cảm biến tích hợp sẵn: Con quay hồi chuyển 3 trục (Gyroscope), Gia tốc kế 3 trục (Accelerometer), và Từ kế 3 trục (Magnetometer AK09916 đóng gói chung bên trong SiP qua bus I2C phụ nội bộ).
- **Ranh giới thuật toán firmware hiện tại**:
  - Firmware giai đoạn giữa kỳ (Tuần 5) chỉ kích hoạt và thu thập dữ liệu từ **Gyroscope và Accelerometer** để triển khai thuật toán dung hợp tư thế **6 trục (6-Axis Fusion)** bằng bộ lọc bù Quaternion.
  - Khối từ kế AK09916 chưa được khởi tạo, đọc hoặc đưa vào thuật toán hiện tại. Do đó, **tuyệt đối không vẽ AK09916 như một khối module rời bên ngoài**.
- **Giao tiếp liên kết**:
  - Nối trực tiếp với ESP32 qua bus **I2C Fast-Mode tần số $400\,\text{kHz}$** (`GPIO21` là SDA, `GPIO22` là SCL).
  - Module sử dụng trở kéo $10\,\text{k}\Omega$ có sẵn trên bo mạch WCMCU-20948 kéo lên đường $3,3\,\text{V}$. Không sử dụng BSS138.
  - Chân `AD0` nối GND chọn địa chỉ I2C 7-bit là `0x68`. Chân `NCS` nối 3.3V để kích hoạt chế độ I2C.

### 1.3 Khối Xử Lý Trung Tâm (Central Processing Unit — MCU)
- **Phần cứng**: Vi điều khiển **ESP32 Classic DevKit 38-pin** (SoC ESP32-D0WD-V3 kiến trúc 32-bit Xtensa Dual-Core LX6 chạy ở tần số $240\,\text{MHz}$).
- **Quy trình xử lý chuyển động (Firmware Pipeline)**:
  1. Giao tiếp I2C Master đọc burst 12 byte dữ liệu thô (6 byte Accel + 6 byte Gyro) từ Bank 0 với chu kỳ định thời $10\,\text{ms}$ ($100\,\text{Hz}$).
  2. Ghép dữ liệu 16-bit bù 2 và quy đổi ra đơn vị vật lý ($g$ và $^{\circ}/\text{s}$).
  3. Bù trừ sai số trôi tĩnh (Zero-rate Bias Calibration) của con quay hồi chuyển.
  4. Ước lượng vector trọng trường và tư thế góc nghiêng 6 trục thông qua bộ lọc bù Quaternion ($K = 2.0\,\text{s}^{-1}$).
  5. Áp dụng cơ chế khung tham chiếu thích nghi (Adaptive Reference Frame) và vùng chết hai ngưỡng chuyển tiếp (Dead-zone $0.8^{\circ}/\text{s}$ và $1.4^{\circ}/\text{s}$) để chống rung tay sinh lý.
  6. Tính toán độ dời con trỏ chuột tương đối $(\Delta X, \Delta Y)$ theo nguyên lý Rate-Control kết hợp khống chế biên độ giới hạn $[-127, +127]$.

### 1.4 Khối Giao Tiếp Người Dùng (User Control Inputs)
- Gồm **3 nút bấm xúc giác cơ khí (Tactile Switches 12x12mm)** gắn kèm nắp chụp tròn $\varnothing 12\,\text{mm}$:
  - **Nút Chuột Trái (SW_LEFT)**: Nối chân `GPIO25`.
  - **Nút Chuột Phải (SW_RIGHT)**: Nối chân `GPIO26`.
  - **Nút Bật/Tắt Chuột Bay / Clutch (SW_MODE)**: Nối chân `GPIO27` (RTC GPIO).
- Cơ chế cấu hình chân: Toàn bộ 3 nút được cấu hình chế độ **`INPUT_PULLUP`** tích cực mức thấp (Active-Low). Khi chưa nhấn ở mức logic 1 ($3,3\,\text{V}$), khi người dùng nhấn nút sẽ nối chân thẳng xuống mass GND tạo mức logic 0 ($0\,\text{V}$).

### 1.5 Khối Đầu Ra Không Dây (Wireless Output Interface)
- Sử dụng bộ vô tuyến tích hợp của ESP32 phát giao thức **Bluetooth Low Energy (BLE)** theo cấu hình **HID over GATT (Human Interface Device Profile)**.
- **Định dạng bản tin**: Đóng gói báo cáo chuột tiêu chuẩn **HID Mouse Report 5 byte** theo thư viện ESP32-BLE-Mouse 0.3.1:
  - Byte 1: `Buttons Mask` (Bit 0: Left, Bit 1: Right, Bit 2: Middle).
  - Byte 2: `dX` (Độ dời chuột trục X có dấu, dải $-127$ đến $+127$).
  - Byte 3: `dY` (Độ dời chuột trục Y có dấu, dải $-127$ đến $+127$).
  - Byte 4: `Wheel` (Cuộn bánh xe trục đứng).
  - Byte 5: `hWheel / Pan` (Cuộn bánh xe trục ngang).
- **Ranh giới thực nghiệm**: Khối BLE hiện tại ở trạng thái **`NOT_TESTED`** trên máy tính thật (mã nguồn đã biên dịch thành công, đã khởi chạy lệnh phát sóng quảng bá `AirMouse-ESP32` nhưng chưa ghép nối đo kiểm với hệ điều hành máy tính PC). Tuyệt đối không vẽ hay tuyên bố con trỏ chuột đã điều khiển thực tế trên PC.

### 1.6 Khối Phụ Trợ (Auxiliary & Diagnostics)
- **Đèn LED chỉ thị (LED_STATUS)**: Đèn LED 3mm màu xanh lá nối từ chân `GPIO32` qua điện trở hạn dòng $R_1 = 1.0\,\text{k}\Omega$ xuống GND, báo hiệu các trạng thái: Khởi động, Hiệu chuẩn bias tĩnh, và Chế độ hoạt động.
- **Mạch phân áp đo pin (Battery Voltage Divider)**: Cầu phân áp $100\,\text{k}\Omega / 100\,\text{k}\Omega$ mắc từ `V_SYS` về GND, điểm giữa đưa vào chân **`GPIO34` (Kênh `ADC1_CH6`)** kèm tụ lọc $C_1 = 100\,\text{nF}$. Chức năng này ở trạng thái `HARDWARE_DESIGNED`, firmware Tuần 5 chưa gọi hàm `analogRead(34)`.

---

## 2. Sơ Đồ Khối Mức Hệ Thống Dạng ASCII (Rút Gọn 75 Cột)

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

---

## 3. Hướng Dẫn Chi Tiết Bố Cục Cho Người Vẽ Đồ Họa

Khi vẽ lại sơ đồ khối trên phần mềm chuyên dụng để chèn vào báo cáo Word/PDF và Slide bảo vệ, người thiết kế cần tuân thủ các nguyên tắc mỹ thuật và kỹ thuật sau:

### 3.1 Bố cục tổng thể (Luồng từ Trái sang Phải)
- **Cột bên trái**: Khối Nguồn (Pin LiPo $\to$ TP4056 $\to$ SW1 $\to$ MT3608). Vẽ các khối này thẳng hàng từ trên xuống dưới hoặc nằm trọn trong một khung viền nét đứt mang tên *"Khối Quản Lý Nguồn"*.
- **Vị trí trung tâm**: Khối xử lý trung tâm **ESP32 Classic DevKit**. Đây là khối lớn nhất, đóng vai trò hạt nhân kết nối tất cả các phân hệ.
- **Phía trên hoặc góc trên bên trái của ESP32**: Module cảm biến **WCMCU-20948**. Đường I2C nối giữa WCMCU và ESP32 phải là mũi tên hai chiều với nhãn rõ ràng: `I2C 400 kHz (SDA: GPIO21, SCL: GPIO22) Direct 3.3V`.
- **Phía dưới của ESP32**:
  - Cụm 3 nút bấm cơ khí (SW_LEFT, SW_RIGHT, SW_MODE) kèm chú thích `Active-Low, GPIO25/26/27`.
  - Mạch đèn LED chỉ thị (`GPIO32 $\to$ R1 1.0k $\to$ LED D1`).
  - Mạch phân áp đo pin (`V_SYS $\to$ R2 100k / R3 100k $\to$ GPIO34 / ADC1_CH6`).
- **Cột bên phải**: Khối Thiết bị đích (**Máy tính PC / Smart TV**). Giữa ESP32 và Máy tính là mũi tên không dây dạng sóng BLE kèm nhãn: `BLE HID Mouse Report (5 bytes), Chu kỳ 10ms`.
  - Bắt buộc ghi nhãn phụ dưới khối Máy tính: `Trạng thái: NOT_TESTED`.

### 3.2 Quy chuẩn màu sắc và kiểu đường nét (Visual Hierarchy)
- **Đường cấp nguồn (Power Traces)**: Sử dụng nét vẽ đậm, màu Đỏ hoặc Cam (VD: `VBAT`, `5V`, `3V3`). Mũi tên một chiều chỉ hướng truyền năng lượng.
- **Đường dữ liệu có dây (Data / Control Buses)**: Sử dụng nét liền màu Xanh dương đậm hoặc Đen. Bus I2C bắt buộc là mũi tên hai chiều.
- **Đường truyền không dây (Wireless Link)**: Sử dụng nét đứt khúc hoặc biểu tượng phát sóng kèm mũi tên màu Tím hoặc Xanh lam.
- **Màu nền các khối (Block Fill)**:
  - Khối nguồn: Màu vàng nhạt hoặc cam pastel (`#FFF3E0`).
  - Khối MCU ESP32: Màu xanh lam pastel (`#E1F5FE` hoặc `#E3F2FD`).
  - Khối cảm biến IMU: Màu xanh ngọc pastel (`#E0F2F1`).
  - Khối nút bấm & LED: Màu xám nhạt (`#F5F5F5`).
  - Khối thiết bị đích: Màu tím nhạt (`#EDE7F6`).

### 3.3 Những điều cấm kỵ khi vẽ sơ đồ khối
1. **Tuyệt đối không vẽ mạch chuyển mức logic BSS138** hay nguồn LDO 1.8V vào sơ đồ khối này.
2. **Tuyệt đối không vẽ chip từ kế AK09916 như một hộp rời bên ngoài**. Nếu muốn đề cập, chỉ ghi dòng chữ nhỏ bên trong khối WCMCU-20948: *"AK09916 (Chưa dùng trong V1)"*.
3. **Không ghi bản tin 4 byte**. Chuẩn báo cáo chuột của thư viện ESP32-BLE-Mouse 0.3.1 là **5 byte**.
4. **Không nhồi nhét quá nhiều chi tiết thanh ghi** (như `0x06`, `0x1B`, `0x7F`) vào sơ đồ khối mức hệ thống. Các chi tiết thanh ghi thuộc về sơ đồ thuật toán và bảng đối chiếu.
5. **Độ phân giải và cỡ chữ**: Toàn bộ chữ trong các khối hộp phải dùng font chữ không chân (Arial, Helvetica hoặc Roboto), cỡ chữ tối thiểu $9\text{--}10\,\text{pt}$ để khi đưa vào trang báo cáo A4 hoặc co về chiều ngang $15\text{--}16\,\text{cm}$ người đọc vẫn nhìn rõ từng từ.
