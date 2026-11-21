# ĐÁP ỨNG TOÀN DIỆN YÊU CẦU KIỂM TRA BẢO VỆ GIỮA KỲ TUẦN 5 CỦA GIẢNG VIÊN
## MÔN HỌC: HỆ THỐNG NHÚNG (EMBEDDED SYSTEMS)
### DỰ ÁN: AIR MOUSE BLE HID (ESP32 CLASSIC + ICM-20948)

> **Môn học**: Hệ thống nhúng (Embedded Systems)  
> **Mốc kiểm tra**: Báo cáo Giữa kỳ Tuần 5 (Lý thuyết cơ sở & Kiến trúc hệ thống)  
> **Mục tiêu tài liệu**: Khớp nối chính xác $100\%$ từng câu hỏi ghi nhận từ lớp học của Giảng viên với câu trả lời kỹ thuật chuẩn xác, bảo vệ vững chắc bản chất đề tài.  

---

## 1. BẢNG KHỚP NỐI 5 CÂU HỎI TRỌNG TÂM CỦA GIẢNG VIÊN

```text
+-----------------------------------------------------------------------------------------------+
| CÂU HỎI GIẢNG VIÊN TRÊN LỚP        | CÂU TRẢ LỜI CHUẨN XÁC CỦA NHÓM ĐỀ TÀI                    |
+------------------------------------+----------------------------------------------------------+
| 1. "Đang làm gì?"                  | Xây dựng chuột bay Hybrid 9-Axis Air Mouse BLE HID:      |
|                                    | - Gyro đo xoay cổ tay điều khiển con trỏ tương đối.      |
|                                    | - Accel hỗ trợ chống trôi, đứng yên và cử chỉ flick.     |
|                                    | - Reference frame cho phép đổi tư thế cầm tùy ý.         |
+------------------------------------+----------------------------------------------------------+
| 2. "Để làm việc đó thì những       | Phân biệt rạch ròi 2 nhóm:                              |
|    ngoại vi nào sẽ được dùng?"     | - Ngoại vi nội ESP32: I2C0, GPIO In, GPIO Out, ADC1, BLE |
|                                    | - Thiết bị ngoại vi ngoài: Cảm biến 9-DOF ICM-20948.     |
+------------------------------------+----------------------------------------------------------+
| 3. "Thanh ghi cấu hình gồm bao     | Phân tích chi tiết 2 thanh ghi cấu hình trọng tâm:       |
|    nhiêu bit? Bit nào cấu hình gì?"| - PWR_MGMT_1 (8-bit, Bank 0 0x06, giá trị 0x01)          |
|                                    | - GYRO_CONFIG_1 (8-bit, Bank 2 0x01, giá trị 0x1B)       |
|                                    | (Bổ sung ACCEL_CONFIG 8-bit, Bank 2 0x14, giá trị 0x1B). |
+------------------------------------+----------------------------------------------------------+
| 4. "Thanh ghi cấu hình khác        | - Thanh ghi cấu hình (Configuration): Xác lập chế độ     |
|    thanh ghi dữ liệu thế nào?"     |   hoạt động (nguồn, clock, dải đo, bộ lọc DLPF).         |
|                                    | - Thanh ghi dữ liệu (Data/Output): Chứa kết quả đo tức  |
|                                    |   thời của cảm biến (raw ADC 16-bit của Gyro, Accel).    |
+------------------------------------+----------------------------------------------------------+
| 5. "Thư viện/code I/O, các thư viện| Chuẩn bị đầy đủ 2 cách hiểu câu hỏi của giảng viên:      |
|    có mấy loại lệnh (2)...?"       | - Diễn giải A (Giao tiếp I2C): 2 loại lệnh WRITE & READ. |
|                                    | - Diễn giải B (Giao tiếp GPIO): 2 loại lệnh INPUT & OUTPUT|
+-----------------------------------------------------------------------------------------------+
```

---

## 2. CÂU HỎI 1: "ĐANG LÀM GÌ?" (OFFICIAL PROJECT SCOPE)

### Câu trả lời chính thức của nhóm:
> *"Nhóm xây dựng thiết bị **Chuột bay không gian không dây (Hybrid 9-Axis Air Mouse)** sử dụng vi điều khiển ESP32 và cảm biến quán tính 9 trục ICM-20948.  
> 
> Chuyển động xoay của cổ tay người dùng được đo đạc tức thời bằng con quay hồi chuyển (Gyroscope) để điều khiển con trỏ chuột máy tính theo nguyên lý vận tốc tương đối (Relative Rate-Control) thông qua giao thức chuẩn Bluetooth Low Energy (BLE) HID.  
> 
> Hệ thống tích hợp thêm gia tốc kế (Accelerometer) nhằm 3 mục tiêu phụ trợ quan trọng: (1) Nhận diện trạng thái đứng yên để tự động bù trừ sai số trôi (Stationary Auto-Zero); (2) Nhận diện các cử chỉ vung tay tịnh tiến ngắn (Translational Flick Gestures) cho thao tác Back/Forward; và (3) Kết hợp ước lượng khung tọa độ tham chiếu (Reference Coordinate Frame) giúp người dùng thoải mái thay đổi tư thế cầm thiết bị trong không gian (kể cả chĩa thẳng lên trời) mà không làm mất tính trực quan của các hướng điều khiển."*

---

## 3. CÂU HỎI 2: "ĐỂ LÀM VIỆC ĐÓ THÌ NHỮNG NGOẠI VI NÀO ĐƯỢC DÙNG?"

Nhóm trình bày bảng phân định rạch ròi, tuyệt đối không liệt kê các ngoại vi không sử dụng:

### A. Ngoại vi nội tại bên trong chip vi điều khiển ESP32:
1. **Bộ điều khiển I2C (I2C0 Master Controller)**:
   - Sử dụng chân `GPIO21` (SDA) và `GPIO22` (SCL).
   - Tốc độ truyền thông: Fast-Mode $400\,\text{kHz}$.
   - Vai trò: Khởi tạo các giao dịch đọc/ghi thanh ghi cấu hình và đọc mảng dữ liệu đo từ cảm biến ICM-20948.
2. **Ngoại vi nhập xuất số GPIO (General Purpose Input/Output)**:
   - **GPIO Input (Chế độ ngõ vào số Active-Low có pull-up nội)**:
     - `GPIO25`: Nhận tín hiệu nút nhấn Chuột Trái (Left Click).
     - `GPIO26`: Nhận tín hiệu nút nhấn Chuột Phải (Right Click).
     - `GPIO27`: Nhận tín hiệu nút Chế độ / Ly hợp / Cử chỉ (BTN_MODE / Clutch / Gesture Arm).
   - **GPIO Output (Chế độ ngõ ra số đẩy kéo Push-Pull)**:
     - `GPIO32`: Điều khiển đèn LED trạng thái (qua điện trở hạn dòng $1\,\text{k}\Omega$).
3. **Bộ chuyển đổi Tương tự - Số (SAR ADC1 Controller)**:
   - Sử dụng kênh `ADC1_CH6` tại chân `GPIO34` (chân Input-Only).
   - Độ phân giải: 12-bit ($0\text{--}4095$), dải điện áp $0\text{--}3.3\,\text{V}$ (sử dụng độ suy giảm $11\,\text{dB}$).
   - Vai trò: Đo điện áp pin LiPo thông qua cầu phân áp $100\,\text{k}\Omega / 100\,\text{k}\Omega$ để giám sát dung lượng pin.
4. **Khối phần cứng vô tuyến Bluetooth Low Energy (2.4GHz BLE Subsystem)**:
   - Chuẩn: BLE v4.2 Human Interface Device over GATT (HOGP).
   - Vai trò: Đóng gói và phát các bản tin chuột tương đối (BLE HID Mouse Reports) về máy tính chủ.

### B. Thiết bị ngoại vi kết nối bên ngoài (External Peripheral Device):
- **Cảm biến chuyển động ICM-20948 (InvenSense / TDK)**:
  - Tích hợp bên trong gồm 3 khối vi cơ MEMS độc lập:
    1. **Gyroscope 3 trục**: Đo vận tốc góc quanh trục $X, Y, Z$ ($\pm 500^{\circ}/\text{s}$).
    2. **Accelerometer 3 trục**: Đo gia tốc dọc trục $X, Y, Z$ ($\pm 4g$).
    3. **Magnetometer 3 trục (AK09916)**: Đo từ trường 3 trục (được khóa an toàn ở P1 để tránh rủi ro nhiễu từ tính phòng học).
  - Tổng cộng: **9 trục cảm biến vật lý (Nine Sensor Axes)**.
  - *Lưu ý bảo vệ*: Không được nhầm lẫn giữa "9 trục cảm biến" với "đo vị trí tọa độ 3D và góc 3D trong phòng".

---

## 4. CÂU HỎI 3 & 4: PHÂN TÍCH THANH GHI CẤU HÌNH & THANH GHI DỮ LIỆU

### A. Sự khác biệt bản chất giữa Thanh ghi Cấu hình và Thanh ghi Dữ liệu

| Tiêu chí so sánh | Thanh ghi Cấu hình (Configuration Registers) | Thanh ghi Dữ liệu (Data / Output Registers) |
| :--- | :--- | :--- |
| **Mục đích sử dụng** | Thiết lập chế độ làm việc phần cứng, chọn nguồn clock, bật/tắt bộ lọc số (DLPF), chọn dải đo toàn thang (Full-Scale Range), quản lý nguồn tiết kiệm điện. | Chứa giá trị đo tức thời của môi trường/vật lý do bộ chuyển đổi ADC 16-bit nội cảm biến cập nhật liên tục. |
| **Quyền truy cập** | Đọc và Ghi (**Read / Write — R/W**). Mã nguồn chủ động ghi tham số khởi tạo vào đây. | Chỉ đọc (**Read-Only — R**). Phần cứng cảm biến tự ghi đè số liệu mới sau mỗi chu kỳ lấy mẫu (ODR). |
| **Tính biến thiên** | Thường được ghi một lần duy nhất lúc khởi động (Boot/Init) hoặc khi chuyển chế độ; giá trị giữ nguyên trong suốt phiên làm việc. | Thay đổi liên tục theo thời gian thực tương ứng với chuyển động của tay người dùng. |
| **Ví dụ trong ICM-20948** | `PWR_MGMT_1`, `GYRO_CONFIG_1`, `ACCEL_CONFIG`, `REG_BANK_SEL`. | `GYRO_XOUT_H/L`, `GYRO_YOUT_H/L`, `ACCEL_XOUT_H/L`. |

---

### B. Bảng Giải Mã Chi Tiết Từng Bit Thanh Ghi Cấu Hình Trọng Tâm

#### 1. Thanh ghi Quản lý Nguồn: `PWR_MGMT_1` (Bank 0, Địa chỉ `0x06`)
- **User Bank**: Bank 0.
- **Địa chỉ Hex**: `0x06`.
- **Độ rộng**: 8-bit.
- **Giá trị Reset mặc định**: `0x41` (`0b01000001` — Chip ở chế độ SLEEP).
- **Giá trị ghi cấu hình thực tế**: **`0x01`** (`0b00000001`).

| Bit | Tên trường (Bitfield) | Giá trị ghi | Chức năng chi tiết theo Datasheet TDK DS-000189 §8.2 | Căn cứ lựa chọn của Đề tài |
| :---: | :--- | :---: | :--- | :--- |
| **7** | `DEVICE_RESET` | `0` | `1`: Reset toàn bộ thanh ghi nội về giá trị mặc định.<br>`0`: Hoạt động bình thường. | Không reset chip trong lệnh cấu hình vận hành. |
| **6** | `SLEEP` | `0` | `1`: Đưa cảm biến vào chế độ ngủ tiết kiệm điện.<br>`0`: Đánh thức chip dậy hoạt động đầy đủ. | **Bắt buộc = 0** để đánh thức chip, nếu không chip hoàn toàn bất động trên bus I2C. |
| **5** | `LP_EN` | `0` | `1`: Bật chế độ tiêu thụ năng lượng thấp (Duty-cycled).<br>`0`: Chế độ hoạt động liên tục đầy đủ tính năng. | Giữ `0` để con quay hồi chuyển đo đạc liên tục với độ ồn thấp nhất. |
| **4** | `Reserved` | `0` | Bit dự trữ của nhà sản xuất, bắt buộc giữ mức 0. | Tuân thủ datasheet. |
| **3** | `TEMP_DIS` | `0` | `1`: Tắt cảm biến nhiệt độ nội.<br>`0`: Bật cảm biến nhiệt độ nội. | Giữ `0` để đọc nhiệt độ phục vụ theo dõi trôi dạt nhiệt nếu cần. |
| **[2:0]**| `CLKSEL[2:0]` | `001` | `000`: Dùng bộ dao động nội 20 MHz.<br>`001` đến `101`: Tự động chọn nguồn xung tốt nhất (Auto selects the best available clock source — PLL nếu sẵn sàng, ngược lại dùng dao động nội).<br>`111`: Dừng xung nhịp. | Chọn `001` để phần cứng khóa xung vào bộ tạo xung PLL của con quay hồi chuyển ổn định, giảm thiểu tối đa trôi tần số (dự phòng dao động nội 20 MHz theo DS-000189 Table 16). |

- **Hiệu ứng phần cứng (Hardware Effect)**: Đánh thức chip khỏi giấc ngủ, khởi động mạch dao động PLL nội, cho phép các khối MEMS và bộ chuyển đổi ADC hoạt động.
- **Kỳ vọng đọc lại (Readback Expectation)**: Đọc lại từ Bank 0 địa chỉ `0x06` trả về chính xác `0x01`.

---

#### 2. Thanh ghi Cấu hình Con quay hồi chuyển: `GYRO_CONFIG_1` (Bank 2, Địa chỉ `0x01`)
- **User Bank**: Bank 2.
- **Địa chỉ Hex**: `0x01`.
- **Độ rộng**: 8-bit.
- **Giá trị Reset mặc định**: `0x00`.
- **Giá trị ghi cấu hình thực tế**: **`0x1B`** (`0b00011011`).

| Bit | Tên trường (Bitfield) | Giá trị ghi | Chức năng chi tiết theo Datasheet TDK DS-000189 §10.2 Table 16 | Căn cứ lựa chọn của Đề tài |
| :---: | :--- | :---: | :--- | :--- |
| **[7:6]**| `Reserved` | `00` | Các bit dự trữ của hãng, luôn giữ 0. | Tuân thủ datasheet. |
| **[5:3]**| `GYRO_DLPFCFG[2:0]` | `011` ($3$) | Cấu hình tần số cắt bộ lọc số dải thông thấp (Hardware DLPF):<br>`000`: 196.6 Hz<br>`001`: 151.8 Hz<br>`010`: 119.5 Hz<br>**`011`: 51.2 Hz (NBW 73.3 Hz, Table 16)**<br>`100`: 23.9 Hz<br>`101`: 11.6 Hz<br>`110`: 5.7 Hz | Chọn `011` để tạo dải thông **$51.2\,\text{Hz}$**; giảm rung động cơ học và nhiễu ngẫu nhiên tần số cao (datasheet DS-000189 không công bố độ trễ cho cấu hình này). |
| **[2:1]**| `GYRO_FS_SEL[1:0]` | `01` ($1$) | Lựa chọn dải đo toàn thang con quay hồi chuyển:<br>`00`: $\pm 250^{\circ}/\text{s}$ (Độ nhạy 131 LSB/dps)<br>**`01`: $\pm 500^{\circ}/\text{s}$ (Độ nhạy 65.5 LSB/dps)**<br>`10`: $\pm 1000^{\circ}/\text{s}$ (Độ nhạy 32.8 LSB/dps)<br>`11`: $\pm 2000^{\circ}/\text{s}$ (Độ nhạy 16.4 LSB/dps) | Dải $\pm 500^{\circ}/\text{s}$ là dải tỷ lệ vàng cho chuột bay: chuyển động vung cổ tay thông thường đạt $100\text{--}300^{\circ}/\text{s}$; không bị bão hòa (clipping) khi vung nhanh, đồng thời độ phân giải đạt $65.5\,\text{LSB}/(^{\circ}/\text{s})$ rất sắc nét. |
| **0** | `GYRO_FCHOICE` | `1` | `0`: Bỏ qua bộ lọc DLPF (Bypass filter).<br>`1`: Kích hoạt bộ lọc số DLPF theo cài đặt bit [5:3]. | **Bắt buộc = 1** để kích hoạt bộ lọc số phần cứng $51.2\,\text{Hz}$. |

- **Giải mã nhị phân tổng thể**:
  $$\text{Binary} = \underbrace{00}_{\text{Reserved}} \; \underbrace{011}_{\text{DLPF}=51.2\text{Hz}} \; \underbrace{01}_{\text{FS}=\pm 500\text{dps}} \; \underbrace{1}_{\text{FCHOICE}=1} = \mathbf{0b00011011} = \mathbf{0x1B}$$
- **Hiệu ứng phần cứng (Hardware Effect)**: Kích hoạt mạch lọc số phần cứng nội suy bên trong chip, ghim độ nhạy Gyro ở mức $65.5\,\text{LSB}/(^{\circ}/\text{s})$.
- **Kỳ vọng đọc lại (Readback Expectation)**: Chuyển sang Bank 2, đọc địa chỉ `0x01` trả về chính xác `0x1B`.

---

#### 3. Thanh ghi Cấu hình Gia tốc kế: `ACCEL_CONFIG` (Bank 2, Địa chỉ `0x14`)
- **User Bank**: Bank 2.
- **Địa chỉ Hex**: `0x14`.
- **Độ rộng**: 8-bit.
- **Giá trị ghi cấu hình thực tế**: **`0x1B`** (`0b00011011`).
- **Giải mã bitfield**:
  - Bits [5:3] (`ACCEL_DLPFCFG`): `011` $\rightarrow$ Bộ lọc DLPF dải thông $\approx 50.4\,\text{Hz}$ (tra cứu TDK DS-000189 rev 1.6 Table 18 — Accelerator Configuration, 3 dB BW 50.4 Hz, Noise BW 68.8 Hz; lưu ý bit `010` là $111.4\,\text{Hz}$).
  - Bits [2:1] (`ACCEL_FS_SEL`): `01` $\rightarrow$ Dải đo toàn thang gia tốc $\pm 4g$ (Độ nhạy $8192\,\text{LSB}/g$).
  - Bit 0 (`ACCEL_FCHOICE`): `1` $\rightarrow$ Kích hoạt bộ lọc DLPF gia tốc.
- **Thanh ghi đồng bộ ODR**: `ACCEL_SMPLRT_DIV_1/2` (Bank 2, Địa chỉ `0x10`–`0x11`) cấu hình giá trị `10` ($1125 / (1 + 10) = 102.27\,\text{Hz}$): accel và gyro được cấu hình cùng nominal ODR ≈102.27 Hz; chưa chứng minh đồng pha hoặc freshness nếu chưa dùng data-ready/FIFO.
- **Ý nghĩa**: Giúp đo đạc vector trọng trường và nhận dạng cử chỉ vung tịnh tiến cực kỳ mượt mà, không bị méo tín hiệu.

---

### C. Bảng Phân Tích Thanh Ghi Dữ Liệu Ngõ Ra (Data Output Registers)

| Tên thanh ghi | User Bank | Địa chỉ | Độ rộng | Quyền | Ý nghĩa dữ liệu chứa bên trong |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `ACCEL_XOUT_H / L` | Bank 0 | `0x2D` / `0x2E` | 16-bit signed | Read-Only | Gia tốc thô trục X ($2\,\text{byte}$ bù hai, chia cho $8192$ ra đơn vị $g$). |
| `ACCEL_YOUT_H / L` | Bank 0 | `0x2F` / `0x30` | 16-bit signed | Read-Only | Gia tốc thô trục Y (dùng nhận dạng cử chỉ vung tịnh tiến Flick Trái/Phải). |
| `ACCEL_ZOUT_H / L` | Bank 0 | `0x31` / `0x32` | 16-bit signed | Read-Only | Gia tốc thô trục Z (kết hợp đo vector trọng trường tham chiếu). |
| `GYRO_XOUT_H / L`  | Bank 0 | `0x33` / `0x34` | 16-bit signed | Read-Only | Vận tốc góc thô trục X (Roll — xoay lật quanh trục dài chuột). |
| `GYRO_YOUT_H / L`  | Bank 0 | `0x35` / `0x36` | 16-bit signed | Read-Only | Vận tốc góc thô trục Y (Pitch — gật cổ tay lên/xuống $\rightarrow \Delta Y$). |
| `GYRO_ZOUT_H / L`  | Bank 0 | `0x37` / `0x38` | 16-bit signed | Read-Only | Vận tốc góc thô trục Z (Yaw — lắc cổ tay trái/phải $\rightarrow \Delta X$). |

---

## 5. CÂU HỎI 5: "THƯ VIỆN/CODE I/O CÓ MẤY LOẠI LỆNH (2)...?"

Tùy theo góc độ tiếp cận của Giảng viên khi đặt câu hỏi vấn đáp, nhóm chuẩn bị sẵn **CẢ HAI PHƯƠNG ÁN GIẢI THÍCH**:

### PHƯƠNG ÁN A: Giao thức Truyền thông Nối tiếp I2C (`Wire.h`)
Nếu thầy hỏi về 2 loại lệnh giao tiếp cơ bản của bus I2C, câu trả lời là: **LỆNH GHI (WRITE TRANSACTION)** và **LỆNH ĐỌC (READ TRANSACTION)**.

```text
GIAO DỊCH GHI (I2C WRITE):
Master: [START] -> [Device Addr + 0 (W)] -> [Register Addr] -> [Data Byte] -> [STOP]

GIAO DỊCH ĐỌC (I2C READ):
Master: [START] -> [Device Addr + 0 (W)] -> [Register Addr] 
        -> [REPEATED START] -> [Device Addr + 1 (R)] -> Nhận Data Byte -> [STOP]
```

1. **Lệnh Ghi (Write)**:
   - Dùng để gửi lệnh cấu hình vào thanh ghi của cảm biến (ví dụ chọn Bank, ghi `0x01` vào `PWR_MGMT_1`).
   - Chuỗi lệnh trong mã nguồn:
     ```cpp
     Wire.beginTransmission(0x68);
     Wire.write(regAddress);
     Wire.write(dataByte);
     Wire.endTransmission();
     ```
2. **Lệnh Đọc (Read)**:
   - Dùng để thu nhận dữ liệu từ cảm biến về vi điều khiển (ví dụ đọc `WHO_AM_I`, đọc 6 byte Gyro).
   - Chuỗi lệnh trong mã nguồn:
     ```cpp
     Wire.beginTransmission(0x68);
     Wire.write(startRegAddress);
     Wire.endTransmission(false); // Gửi Restart giữ bus
     Wire.requestFrom((uint8_t)0x68, (size_t)length);
     while(Wire.available()) {
         buffer[i++] = Wire.read();
     }
     ```

---

### PHƯƠNG ÁN B: Nhập/Xuất Đa Dụng GPIO (`Arduino HAL / ESP-IDF GPIO`)
Nếu thầy hỏi về 2 loại lệnh I/O phần cứng cơ bản của vi điều khiển, câu trả lời là: **LỆNH NGÕ VÀO (INPUT)** và **LỆNH NGÕ RA (OUTPUT)**.

1. **Lệnh Ngõ Vào (Input)**:
   - Cấu hình chân: `pinMode(pin, INPUT_PULLUP)`.
   - Lệnh thực thi: `digitalRead(pin)`.
   - Ứng dụng trong đề tài: Đọc mức logic của 3 nút bấm `GPIO25, 26, 27`. Khi người dùng nhả phím $\rightarrow$ đọc được mức `HIGH` ($3.3\,\text{V}$); khi nhấn phím chập mass $\rightarrow$ đọc được mức `LOW` ($0\,\text{V}$).
2. **Lệnh Ngõ Ra (Output)**:
   - Cấu hình chân: `pinMode(pin, OUTPUT)`.
   - Lệnh thực thi: `digitalWrite(pin, HIGH / LOW)`.
   - Ứng dụng trong đề tài: Điều khiển đèn LED trạng thái tại chân `GPIO32`. Ghi `HIGH` cấp điện thế $3.3\,\text{V}$ làm sáng LED; ghi `LOW` làm tắt LED.
