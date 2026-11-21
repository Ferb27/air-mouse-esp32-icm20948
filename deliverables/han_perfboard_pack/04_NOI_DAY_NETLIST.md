# Danh sách net và bảng nối dây nguồn

Trích net và bảng pin-to-pin. Nguồn còn J2/TP8–TP11 cũ; chúng KHÔNG lắp trên perfboard. J5V là điểm ngắt thêm V2. Lắp theo **43 dòng mục 3.7 của hướng dẫn**. C1 gốm không phân cực dù bảng nguồn dùng cách gọi cực. Số chân netlist chưa thay nhãn bo thật.

## 1. Bảng Định Nghĩa Danh Mục Mạng Hệ Thống (System Net Definitions)

Hệ thống mạch Air Mouse V1 trong kiến trúc nguyên mẫu vật lý trực tiếp 3.3V bao gồm chính xác **15 mạng điện độc nhất (15 Unique Nets)** (đã loại bỏ 4 mạng thuộc khối 1.8V và Level Shifter; bản V2.1.0 tách riêng mạng `GND_BAT_CELL` của cực âm cell pin):

| STT | Tên mạng (Net Name) | Phân loại mạng (Net Class) | Điện áp danh định | Dải điện áp cho phép | Miền nguồn / Điểm gốc (Source) | Vai trò chức năng & Ghi chú quan trọng |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| 1 | **`GND`** | Power / Ground | $0\,\text{V}$ | Chuẩn $0\,\text{V}$ quy chiếu | Pad `OUT-` của TP4056 / Common Ground | **Mặt phẳng mass chung toàn hệ thống**, gốc tại pad `OUT-` (sau MOSFET bảo vệ). Các module (ESP32, WCMCU-20948, TP4056 qua `OUT-`, MT3608) và nút bấm, LED, tụ điện đều quy về chung mạng này. **Không** bao gồm cực âm cell pin và pad `B-` (xem mạng 15). |
| 2 | **`VBAT`** | Power / Battery | $3.7\,\text{V}$ | $3.0\text{--}4.2\,\text{V}$ | Cell pin LiPo 1S qua cọc cắm J1 | Nguồn thô từ cell pin LiPo cấp vào ngõ vào sạc và bảo vệ pin (Pad `B+` của Module TP4056). |
| 3 | **`V_SW_IN`** | Power / Unswitched | $3.7\,\text{V}$ | $3.0\text{--}4.2\,\text{V}$ | Pad `OUT+` của Module TP4056 | Nguồn dương sau mạch bảo vệ xả cạn (DW01A + FS8205A), đưa trực tiếp vào chân 1 của công tắc nguồn chính SW1. |
| 4 | **`V_SYS`** | Power / Switched System | $3.7\,\text{V}$ | $3.0\text{--}4.2\,\text{V}$ | Chân Common (Pin 2) của công tắc SW1 | Nguồn dương hệ thống sau công tắc gạt. Cấp cho ngõ vào tăng áp MT3608 (`VIN+`) và đỉnh cầu phân áp đo pin R2. Khi tắt SW1, toàn bộ hệ thống sau nó mất nguồn. |
| 5 | **`5V`** | Power / Boosted | $5.0\,\text{V}$ | $4.9\text{--}5.1\,\text{V}$ | Pad `VOUT+` của Module MT3608 | Nguồn $5.0\,\text{V}$ sau tăng áp DC-DC Boost, cấp trực tiếp vào chân VIN của ESP32 DevKit và nạp năng lượng cho tụ ổn định C2. **CẤM NỐI VÀO ADC HOẶC CẢM BIẾN**. |
| 6 | **`3V3`** | Power / MCU Logic | $3.3\,\text{V}$ | $3.25\text{--}3.35\,\text{V}$ | Chân 1 (3V3) của ESP32 DevKit | Nguồn $3.3\,\text{V}$ từ LDO 3.3V trên board DevKit, cấp nuôi module WCMCU-20948 (chân VCC, NCS), cổng mở rộng I2C J2 và test point TP3. |
| 7 | **`BAT_SENSE`** | Analog Sense | $1.85\,\text{V}$ | $1.50\text{--}2.10\,\text{V}$ | Điểm giữa cầu phân áp R2/R3 | Điện áp sau khi chia đôi từ $V_{\text{SYS}}$ ($V_{\text{sense}} = V_{\text{SYS}} / 2$), đưa vào chân GPIO34 (`ADC1_CH6`) của ESP32 để đo dung lượng pin còn lại. |
| 8 | **`IMU_SDA`** | I2C Open-Drain | $3.3\,\text{V}$ | $0\text{--}3.3\,\text{V}$ | ESP32 GPIO21 / WCMCU SDA | Đường truyền dữ liệu I2C $3.3\,\text{V}$ trực tiếp giữa vi điều khiển ESP32 và cảm biến ICM-20948 (`BENCH_VERIFIED_ON_OWNED_MODULE`). Kéo lên 3.3V bởi trở 10k onboard module. |
| 9 | **`IMU_SCL`** | I2C Open-Drain | $3.3\,\text{V}$ | $0\text{--}3.3\,\text{V}$ | ESP32 GPIO22 / WCMCU SCL | Đường xung clock I2C $3.3\,\text{V}$ trực tiếp giữa vi điều khiển ESP32 và cảm biến ICM-20948 (400 kHz Fast-Mode). Kéo lên 3.3V bởi trở 10k onboard module. |
| 10 | **`BTN_LEFT`** | Digital Input (Active-Low) | $3.3\,\text{V}$ | $0\text{--}3.3\,\text{V}$ | Nút nhấn SW2 / ESP32 GPIO25 | Tín hiệu nút bấm chuột trái (Left Click). Trạng thái nghỉ nhả phím kéo lên $3.3\,\text{V}$ bằng trở kéo nội `INPUT_PULLUP`; khi nhấn phím nối chập về mass ($0\,\text{V}$). |
| 11 | **`BTN_RIGHT`** | Digital Input (Active-Low) | $3.3\,\text{V}$ | $0\text{--}3.3\,\text{V}$ | Nút nhấn SW3 / ESP32 GPIO26 | Tín hiệu nút bấm chuột phải (Right Click). Trạng thái nghỉ kéo lên $3.3\,\text{V}$ (`INPUT_PULLUP`); khi nhấn phím nối chập về mass ($0\,\text{V}$). |
| 12 | **`BTN_MODE`** | Digital Input (Active-Low) | $3.3\,\text{V}$ | $0\text{--}3.3\,\text{V}$ | Nút nhấn SW4 / ESP32 GPIO27 | Tín hiệu nút chuyển chế độ Air Mouse ON/OFF. Trạng thái nghỉ kéo lên $3.3\,\text{V}$ (`INPUT_PULLUP`); khi nhấn phím nối chập về mass ($0\,\text{V}$). |
| 13 | **`LED_STATUS`**| Digital Output (Push-Pull) | $3.3\,\text{V}$ | $0\text{--}3.3\,\text{V}$ | Chân GPIO32 của ESP32 | Tín hiệu điều khiển đèn LED chỉ thị trạng thái từ ESP32, đưa vào chân 1 của điện trở hạn dòng R1 ($1\,\text{k}\Omega$). Mức cao ($3.3\,\text{V}$) bật sáng LED. |
| 14 | **`LED_ANODE`** | Analog/Current Loop | $2.1\,\text{V}$ | $0\text{--}2.2\,\text{V}$ | Chân 2 của điện trở R1 | Mạng trung gian sau điện trở R1 đưa vào cực Anode (chân 2) của đèn LED D1. Khi LED sáng, điện áp tại đây ghim ở mức $V_f \approx 2.0\text{--}2.2\,\text{V}$. |
| 15 | **`GND_BAT_CELL`** | Power / Battery Return | $0\,\text{V}$ (cực âm cell) | Chỉ nối cell ↔ `B-` | Cực âm cell pin LiPo qua cọc J1 | Đường trở về của cell vào pad `B-`; dòng đi qua MOSFET bảo vệ FS8205A bên trong module rồi mới ra `OUT-`. **CẤM nối mạng này vào `GND` hệ thống hoặc `OUT-` bên ngoài module** — làm vậy sẽ nối tắt (bypass) MOSFET, mất bảo vệ quá xả và ngắn mạch. Tên mạng khớp (nguồn gốc; nội dung cần thiết đã trích trong gói) (dòng 30). |

### Danh mục 4 mạng đã loại bỏ trong kiến trúc trực tiếp 3.3V (`REMOVED_NETS`):
1. **`1V8`**: Đã loại bỏ do không còn LDO 1.8V AMS1117-1.8V và tụ lọc C3, C4.
2. **`IMU_SDA_1V8`**: Đã hợp nhất vào mạng `IMU_SDA` do không còn qua MOSFET BSS138.
3. **`IMU_SCL_1V8`**: Đã hợp nhất vào mạng `IMU_SCL` do không còn qua MOSFET BSS138.
4. **`IMU_INT_1V8`**: Chân INT cảm biến ICM-20948 để hở (chưa sử dụng ngắt phần cứng trong V1).

---

## 2. Bảng Nối Dây Chi Tiết Pin-to-Pin (Complete Pin-to-Pin Netlist Table)

Bảng dưới đây liệt kê chi tiết từng liên kết nối dây từ chân xuất phát (`FROM`) đến chân đích (`TO`) tương ứng trên sơ đồ nguyên lý phần cứng nguyên mẫu trực tiếp 3.3V:

| STT | FROM (RefDes) | Chân xuất phát (Pin) | Tên mạng (Net Name) | TO (RefDes) | Chân đích (Pin) | Miền điện áp | Ghi chú kỹ thuật & Chức năng |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| 1 | **BAT1** | Pin 1 (+) | **`VBAT`** | **J1** (J_BAT) | Pin 1 (1) | $3.0\text{--}4.2\,\text{V}$ | Cực dương pin LiPo nối vào chân 1 cọc cắm JST-PH 2.0mm |
| 2 | **BAT1** | Pin 2 (-) | **`GND_BAT_CELL`** | **J1** (J_BAT) | Pin 2 (2) | Cực âm cell | Cực âm pin LiPo nối vào chân 2 cọc cắm JST-PH 2.0mm (**không** nối vào `GND` hệ thống) |
| 3 | **J1** (J_BAT) | Pin 1 (1) | **`VBAT`** | **MOD1** (TP4056)| Pad 1 (`B+`) | $3.0\text{--}4.2\,\text{V}$ | Đường sạc và nhận nguồn từ pin đưa vào Pad B+ của TP4056 |
| 4 | **J1** (J_BAT) | Pin 2 (2) | **`GND_BAT_CELL`** | **MOD1** (TP4056)| Pad 2 (`B-`) | Cực âm cell | Cực âm cell đưa vào Pad B- (phía trước MOSFET bảo vệ). Pad B- chỉ nối với J1, không nối `GND`/`OUT-` bên ngoài module |
| 5 | **MOD1** (TP4056)| Pad 3 (`OUT+`) | **`V_SW_IN`** | **SW1** | Pin 1 (1) | $3.0\text{--}4.2\,\text{V}$ | Ngõ ra dương có bảo vệ ngắt cạn đưa vào tiếp điểm 1 công tắc |
| 6 | **MOD1** (TP4056)| Pad 4 (`OUT-`) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Ngõ ra âm bảo vệ của TP4056 nối vào mass chung hệ thống |
| 7 | **SW1** | Pin 2 (Common) | **`V_SYS`** | **MOD2** (MT3608)| Pad 1 (`VIN+`)| $3.0\text{--}4.2\,\text{V}$ | Cực chung công tắc gạt cấp nguồn dương cho mạch tăng áp |
| 8 | **SW1** | Pin 2 (Common) | **`V_SYS`** | **R2** (R_TOP) | Pin 1 (1) | $3.0\text{--}4.2\,\text{V}$ | Cực chung công tắc cấp điện áp pin cho đỉnh cầu phân áp đo pin |
| 9 | **MOD2** (MT3608)| Pad 2 (`VIN-`) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Ngõ vào âm của mạch tăng áp nối mass |
| 10 | **MOD2** (MT3608)| Pad 4 (`VOUT-`)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Ngõ ra âm của mạch tăng áp nối mass chung |
| 11 | **MOD2** (MT3608)| Pad 3 (`VOUT+`)| **`5V`** | **U1** (ESP32) | Chân 19 (`VIN`)| $5.0\,\text{V}$ | Nguồn tăng áp $5.0\,\text{V}$ cấp nuôi bo vi điều khiển ESP32 |
| 12 | **MOD2** (MT3608)| Pad 3 (`VOUT+`)| **`5V`** | **C2** | Pin 1 (+) | $5.0\,\text{V}$ | Tụ hóa $10\,\mu\text{F}$ ổn định nguồn ngõ vào $5.0\,\text{V}$ ESP32 |
| 13 | **C2** | Pin 2 (-) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Cực âm tụ hóa C2 nối mass |
| 14 | **U1** (ESP32) | Chân 1 (`3V3`)| **`3V3`** | **U2** (IMU) | Chân 1 (`VCC`) | $3.3\,\text{V}$ | Nguồn $3.3\,\text{V}$ ESP32 cấp nuôi trực tiếp cho module WCMCU-20948 |
| 15 | **U1** (ESP32) | Chân 1 (`3V3`)| **`3V3`** | **U2** (IMU) | Chân 5 (`NCS`) | $3.3\,\text{V}$ | Kéo chân NCS lên $3.3\,\text{V}$ để cố định chế độ giao tiếp I2C |
| 16 | **U1** (ESP32) | Chân 1 (`3V3`)| **`3V3`** | **J2** (J_I2C) | Pin 1 (`3V3`) | $3.3\,\text{V}$ | Nguồn $3.3\,\text{V}$ đưa ra header cắm mở rộng I2C ngoài |
| 17 | **U1** (ESP32) | Chân 1 (`3V3`)| **`3V3`** | **TP3** | Pin 1 (`3V3`) | $3.3\,\text{V}$ | Điểm đo nguồn $3.3\,\text{V}$ trên header test point 1x4 |
| 18 | **U1** (ESP32) | Chân 33 (`GPIO21`)| **`IMU_SDA`** | **U2** (IMU) | Chân 4 (`SDA`) | $3.3\,\text{V}$ | Dây dữ liệu I2C nối trực tiếp ESP32 với module cảm biến (`BENCH_VERIFIED`) |
| 19 | **U1** (ESP32) | Chân 33 (`GPIO21`)| **`IMU_SDA`** | **J2** (J_I2C) | Pin 3 (`SDA`) | $3.3\,\text{V}$ | Đường dữ liệu I2C nối song song ra cọc cắm mở rộng ngoài J2 |
| 20 | **U1** (ESP32) | Chân 33 (`GPIO21`)| **`IMU_SDA`** | **TP2** | Pin 1 (`SDA`) | $3.3\,\text{V}$ | Điểm đo dữ liệu I2C trên header test point 1x4 |
| 21 | **U1** (ESP32) | Chân 36 (`GPIO22`)| **`IMU_SCL`** | **U2** (IMU) | Chân 3 (`SCL`) | $3.3\,\text{V}$ | Dây xung clock I2C nối trực tiếp ESP32 với module cảm biến (400 kHz) |
| 22 | **U1** (ESP32) | Chân 36 (`GPIO22`)| **`IMU_SCL`** | **J2** (J_I2C) | Pin 4 (`SCL`) | $3.3\,\text{V}$ | Đường xung clock I2C nối song song ra cọc cắm mở rộng ngoài J2 |
| 23 | **U1** (ESP32) | Chân 36 (`GPIO22`)| **`IMU_SCL`** | **TP1** | Pin 1 (`SCL`) | $3.3\,\text{V}$ | Điểm đo xung clock I2C trên header test point 1x4 |
| 24 | **U2** (IMU) | Chân 2 (`GND`)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân nguồn âm module cảm biến WCMCU-20948 |
| 25 | **U2** (IMU) | Chân 6 (`AD0`)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Nối chân AD0 về mass để cố định địa chỉ I2C 7-bit là `0x68` |
| 26 | **U2** (IMU) | Chân 8 (`FSY`)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Nối chân Frame Sync về mass (không sử dụng đồng bộ ngoài) |
| 27 | **U1** (ESP32) | Chân 9 (`GPIO25`)| **`BTN_LEFT`** | **SW2** (SW_L) | Pin 1 (1) | $3.3\,\text{V}$ | Chân GPIO25 nhận tín hiệu nhấn nút chuột trái (Left Click) |
| 28 | **SW2** (SW_L) | Pin 2 (2) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân tiếp điểm đối diện của nút bấm chuột trái nối mass |
| 29 | **U1** (ESP32) | Chân 10 (`GPIO26`)| **`BTN_RIGHT`**| **SW3** (SW_R) | Pin 1 (1) | $3.3\,\text{V}$ | Chân GPIO26 nhận tín hiệu nhấn nút chuột phải (Right Click) |
| 30 | **SW3** (SW_R) | Pin 2 (2) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân tiếp điểm đối diện của nút bấm chuột phải nối mass |
| 31 | **U1** (ESP32) | Chân 11 (`GPIO27`)| **`BTN_MODE`** | **SW4** (SW_M) | Pin 1 (1) | $3.3\,\text{V}$ | Chân GPIO27 nhận tín hiệu nút chuyển chế độ Air Mouse ON/OFF |
| 32 | **SW4** (SW_M) | Pin 2 (2) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân tiếp điểm đối diện của nút chuyển chế độ nối mass |
| 33 | **U1** (ESP32) | Chân 7 (`GPIO32`)| **`LED_STATUS`**| **R1** (R_LED) | Pin 1 (1) | $3.3\,\text{V}$ | Chân GPIO32 điều khiển ngõ ra logic đưa vào điện trở R1 ($1\,\text{k}\Omega$) |
| 34 | **R1** (R_LED) | Pin 2 (2) | **`LED_ANODE`**| **D1** (LED) | Chân 2 (Anode) | $2.1\,\text{V}$ | Ngõ ra sau điện trở đưa vào cực dương (Anode) đèn LED D1 |
| 35 | **D1** (LED) | Chân 1 (Cathode)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Cực âm (Cathode vát cạnh) của đèn LED nối mass chung |
| 36 | **R2** (R_TOP) | Pin 2 (2) | **`BAT_SENSE`**| **U1** (ESP32) | Chân 5 (`GPIO34`)| $1.5\text{--}2.1\,\text{V}$ | Điểm giữa cầu phân áp đưa vào chân ngõ vào ADC1_CH6 của ESP32 |
| 37 | **R2** (R_TOP) | Pin 2 (2) | **`BAT_SENSE`**| **R3** (R_BOT) | Pin 1 (1) | $1.5\text{--}2.1\,\text{V}$ | Nối điểm giữa cầu phân áp với đầu trên của điện trở R3 ($100\,\text{k}\Omega$) |
| 38 | **R2** (R_TOP) | Pin 2 (2) | **`BAT_SENSE`**| **C1** (C_BAT) | Pin 1 (1) | $1.5\text{--}2.1\,\text{V}$ | Nối điểm giữa cầu phân áp với cực dương tụ lọc chống nhiễu ADC |
| 39 | **R3** (R_BOT) | Pin 2 (2) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Đầu dưới của điện trở cầu phân áp R3 nối mass chung |
| 40 | **C1** (C_BAT) | Pin 2 (2) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Cực âm tụ lọc chống nhiễu ADC C1 nối mass chung |
| 41 | **U1** (ESP32) | Chân 14 (`GND`)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân mass hàng trái của bo vi điều khiển ESP32 |
| 42 | **U1** (ESP32) | Chân 32 (`GND`)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân mass giữa hàng phải của bo vi điều khiển ESP32 |
| 43 | **U1** (ESP32) | Chân 38 (`GND`)| **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân mass cuối hàng phải của bo vi điều khiển ESP32 |
| 44 | **J2** (J_I2C) | Pin 2 (`GND`) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Chân mass cọc cắm mở rộng I2C nối mass chung |
| 45 | **TP4** | Pin 1 (`GND`) | **`GND`** | **Mặt phẳng mass**| `GND` | $0\,\text{V}$ | Điểm mass trên header test point 1x4 |
| 46 | **TP8** | Pin 1 (1) | **`VBAT`** | **Đo kiểm** | Đồng hồ vạn năng| $3.0\text{--}4.2\,\text{V}$ | Điểm đo điện áp trực tiếp cell pin LiPo (pad đồng PCB) |
| 47 | **TP9** | Pin 1 (1) | **`V_SYS`** | **Đo kiểm** | Đồng hồ vạn năng| $3.0\text{--}4.2\,\text{V}$ | Điểm đo nguồn hệ thống sau công tắc gạt SW1 (pad đồng PCB) |
| 48 | **TP10**| Pin 1 (1) | **`5V`** | **Đo kiểm** | Đồng hồ vạn năng| $5.0\,\text{V}$ | Điểm đo nguồn ngõ ra tăng áp $5.0\,\text{V}$ MT3608 (pad đồng PCB) |
| 49 | **TP11**| Pin 1 (1) | **`3V3`** | **Đo kiểm** | Đồng hồ vạn năng| $3.3\,\text{V}$ | Điểm đo nguồn $3.3\,\text{V}$ từ LDO 3.3V trên board DevKit (pad đồng PCB) |

---


## Ranh giới cần giữ

 Các Ranh Giới Kỹ Thuật Bắt Buộc (Critical Electrical Boundaries)

Để bảo vệ phần cứng không bị cháy nổ hoặc suy hao tín hiệu trong quá trình vẽ sơ đồ nguyên lý, kỹ sư bắt buộc phải ghi nhớ các quy tắc ranh giới sau:

1. **Ranh giới Tuyệt đối giữa Nguồn $5\,\text{V}$ và Chân ADC (GPIO34)**:
   - Đường nguồn $5.0\,\text{V}$ ngõ ra MT3608 **CHỈ ĐƯỢC PHÉP** nối vào chân `VIN` của ESP32 và cực dương của tụ hóa `C2`.
   - Chân `GPIO34` (`ADC1_CH6`) **CHỈ ĐƯỢC PHÉP** nối vào điểm giữa của cầu phân áp `R2`/`R3` (`BAT_SENSE`, dải điện áp $1.5\text{--}2.1\,\text{V}$).
   - **CẤM TUYỆT ĐỐI** vẽ dây nối tắt từ đường $5\,\text{V}$ hoặc đường $V_{\text{SYS}}$ trực tiếp vào bất kỳ chân ADC nào của ESP32.

2. **Cách ly Tuyệt đối Chân I2C Phụ (Auxiliary I2C) của ICM-20948**:
   - Chân 9 (`ACL` - Aux SCL Master) và Chân 10 (`ADA` - Aux SDA Master) của module WCMCU-20948 là bus I2C phụ dùng để chip ICM-20948 tự động đọc la bàn ngoài hoặc cảm biến phụ.
   - Hai chân này **BẮT BUỘC ĐỂ HỞ (No Connect - NC)** trên sơ đồ nguyên lý.
   - **CẤM TUYỆT ĐỐI** nối `ACL, ADA` vào bus I2C chính (`GPIO21, GPIO22`) của ESP32, vì sẽ gây xung đột đa chủ (Multi-master collision) làm tê liệt toàn bộ bus I2C.

3. **Phân Định 4 Miền Điện Áp Nguồn Trong Thiết Kế Trực Tiếp 3.3V**:
   - Miền 1: $V_{\text{BAT}}$ ($3.0\text{--}4.2\,\text{V}$) — Chỉ tồn tại giữa pin LiPo và module sạc TP4056.
   - Miền 2: $V_{\text{SYS}}$ ($3.0\text{--}4.2\,\text{V}$) — Nguồn sau công tắc SW1 cấp cho MT3608 và cầu phân áp.
   - Miền 3: $5.0\,\text{V}$ — Nguồn công suất nâng áp cấp cho vi điều khiển ESP32.
   - Miền 4: $3.3\,\text{V}$ — Nguồn logic MCU và nguồn nuôi trực tiếp module cảm biến WCMCU-20948.
   *(Miền 1.8V đã loại bỏ khỏi thiết kế phần cứng sau khi xác minh Bring-up thành công).*

4. **Phân Tách `B-` và `OUT-` Của Module TP4056 (An Toàn Pin)**:
   - Cực âm cell pin chỉ đi qua J1 vào pad `B-` (mạng `GND_BAT_CELL`). `GND` hệ thống lấy từ pad `OUT-`.
   - Giữa `B-` và `OUT-` là MOSFET kép FS8205A do DW01A điều khiển. Nối tắt `B-` với `OUT-`/`GND` bên ngoài module sẽ vô hiệu hóa bảo vệ quá xả và ngắn mạch.
   - Trên KiCad: không đặt ký hiệu `GND` lên pad `B-`, và không cho vùng đổ đồng `GND` chạm pad `B-`.
   - Đo `TP8` (`VBAT`) so với `GND` hệ thống sẽ gồm cả sụt áp trên MOSFET bảo vệ (nhỏ, nhưng không bằng 0); muốn đo đúng điện áp cell thì đo giữa `B+` và `B-`.

5. **Ranh Giới Thực Nghiệm Module WCMCU-20948 Trực Tiếp 3.3V**:
   - Module WCMCU-20948 tích hợp sẵn 2 trở kéo $10\,\text{k}\Omega$ trên đường SDA/SCL lên chân VCC. Khi cấp VCC = 3.3V, bus I2C hoạt động ở mức logic 3.3V tương thích hoàn toàn với ESP32.
   - Kết quả thử nghiệm bring-up vật lý: `BENCH_VERIFIED_ON_OWNED_MODULE`, 100/100 chu kỳ đọc `WHO_AM_I = 0xEA` thành công ở 400 kHz Fast-Mode.
   - Giới hạn: Đây là kết quả đã được xác minh trên đúng module và bo ESP32 của nhóm; sinh viên lưu ý đối chiếu với lý thuyết datasheet raw IC ICM-20948 ($V_{\text{DDIO}} \le 1.95\,\text{V}$) khi trả lời hội đồng phản biện.
