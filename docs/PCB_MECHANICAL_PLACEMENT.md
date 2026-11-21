# AIR MOUSE — QUY CHUẨN CƠ KHÍ & BỐ TRÍ LINH KIỆN (PCB MECHANICAL PLACEMENT)

> **Tài liệu Đặc tả Cơ khí & Layout Định vị (Mechanical & Placement Specification)**  
> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems)  
> **Phiên bản**: 1.6.0 — Direct 3.3V (đã bỏ BSS138 và LDO 1.8V, 2026-10-01)  
> **Trạng thái**: `READY_FOR_PROVISIONAL_I2C_SCHEMATIC`  
> **WCMCU Mechanical Blocker**: `RESOLVED`  
> **Chốt chặn kiểm tra còn lại (Remaining Gate)**: `PHYSICAL_SANITY_CHECK_ONLY`  
> **Phân loại trạng thái kỹ thuật**:
> - `DECIDED`: Quyết định kiến trúc & nguyên tắc cơ khí đã chốt.
> - `WEB_VERIFIED_DESIGN_REFERENCE`: Kích thước WCMCU-20948 đã khóa $26.7 \times 15.3\,\text{mm}$, bước chân $2.54\,\text{mm}$ theo chuẩn web HESTORE kết hợp đo đạc tương quan của user (~$26.8 \times 15.5\,\text{mm}$).
> - `PCB 130x70`: `PROVISIONALLY FITS`.
> - `BATTERY ZERO-THT`: `PASS IN CURRENT PLACEMENT MODEL`.
> - `FINAL`: `PENDING PHYSICAL VERIFICATION`.
> - `2-3 JUMPER`: `ESTIMATE ONLY until routing is actually performed`.

---

## 1. Kích Thước Mục Tiêu Bo Mạch V1 (PCB Target Size)

### 1.1 Thông số mục tiêu [`PROVISIONAL MECHANICAL TARGET`]
- **Chiều dài bo mạch ($L$)**: $\approx 130.0\,\text{mm}$ (dọc theo chiều dài bàn tay khi cầm dạng remote điều khiển không gian).
- **Chiều rộng bo mạch ($W$)**: $\approx 70.0\,\text{mm}$ (vừa vặn lòng bàn tay, đủ chỗ cho 3 nút bấm, module IMU và cổng I2C mở rộng).
- **Độ dày bo mạch ($T$)**: $1.6\,\text{mm}$ (chuẩn gia công FR4 hoặc phay CNC mạch 1 lớp tại phòng thí nghiệm).
- **Số lớp đồng**: **1 lớp đồng (Single-Layer — Bottom Copper Layer)**. Mặt TOP chỉ dùng làm jumper vượt dây.

### 1.2 Đánh giá kích thước V1 [`PCB 130x70: PROVISIONALLY FITS`]
1. **Bảo vệ pin LiPo**: Dành riêng vùng phẳng hoàn toàn ở mặt dưới ($54.0 \times 36.0\,\text{mm}$) không có chân hàn nhọn xuyên qua để dán pin.
2. **Kích thước các module cắm theo web reference**:
   - Module ESP32 Classic 38-pin: $55.0 \times 28.0\,\text{mm}$.
   - Module WCMCU-20948 (10 chân header): $26.7 \times 15.3\,\text{mm}$, pin pitch $2.54\,\text{mm}$ (`WEB_VERIFIED_DESIGN_REFERENCE`, footprint `PinSocket_1x10_P2.54mm_Vertical` + custom outline $26.7 \times 15.3\,\text{mm}$).
   - Module sạc TP4056 Type-C: $26.0 \times 17.0\,\text{mm}$.
   - Module tăng áp MT3608: $36.0 \times 17.0\,\text{mm}$.
3. **Khoảng cách công thái học của nút bấm**: 3 nút bấm có gắn nắp **Button Cap đường kính $12.0\,\text{mm}$** cần khoảng cách tim $\ge 15.3\,\text{mm}$ để ngón tay bấm tự nhiên mà không bị chạm mép nắp.
4. **Khả thi khi đi dây 1 lớp**: Bus I2C chỉ có 2 đường tín hiệu (`SDA, SCL`), giảm bớt 3 đường so với SPI, giúp việc đi dây trên PCB 1 lớp thông thoáng hơn rất nhiều.

---

## 2. Sơ Đồ Bố Trí Không Gian Hai Mặt (Top & Bottom Layout Diagrams)

### 2.1 Bố cục Mặt Trên (TOP SIDE — Tọa độ & Linh kiện)

```text
       0 mm               35 mm                     85 mm            130 mm
      ┌──────────────────────────────────────────────────────────────────┐ 0 mm
      │ [TP4056 CHARGER]  [SW1]  [MT3608 BOOST 5V]                       │
      │ 26 x 17 mm        SPDT   36 x 17 mm                              │
15 mm │ ◄── USB-C Edge                                                   │
      │                                   ┌─────────────────────────┐    │
      │   (BTN_L)    (BTN_M)    (BTN_R)   │  ESP32 DEVKIT 38-PIN    │    │
35 mm │   Left       Mode       Right     │  55.0 x 28.0 mm         │    │
      │   ● Cap12    ● Cap12    ● Cap12   │  Socket 2x19 Header     │    │
      │                                   │                         │    │
50 mm │      [LED_STATUS]                 │  Ăng-ten quay sát mép   │    │
      │      (GPIO32)     [WCMCU-20948]   └─────────────────────────┘    │
      │                   (Direct 3.3V)     ▲ ANTENNA CLEARANCE 15mm     │
      │ ─────── TEST POINTS (4 CHÂN / PADS DỌC MÉP DƯỚI) ─────────  [J_I2C]    │
      └──────────────────────────────────────────────────────────────────┘ 70 mm
        X = 10..25 mm      X = 40..65 mm            X = 72..127 mm
```

### 2.2 Bố cục Mặt Dưới (BOTTOM SIDE — Battery Keepout Zone)

```text
       0 mm               25 mm                     70 mm            130 mm
      ┌──────────────────────────────────────────────────────────────────┐ 0 mm
      │ (Khu vực hàn TP4056, MT3608 sát mép trên)                        │
      │                                                                  │
20 mm │                   ╔═════════════════════════════╗                │
      │                   ║    BATTERY KEEPOUT ZONE     ║                │
      │ (Chân hàn nút bấm ║    Cell LiPo 1S Dẹt 1000mAh ║ (Chân header   │
35 mm │  nằm tại          ║    Kích thước: 50 x 34 mm   ║  ESP32 bắt đầu │
      │  X = 10..22 mm    ║    Reserve:    54 x 36 mm   ║  từ X = 72 mm  │
      │  hoàn toàn ngoài  ║                             ║  hoàn toàn     │
55 mm │  vùng pin)        ║    KAPTON + FOAM 1.5mm      ║  ngoài pin)    │
      │                   ║    ZERO-THT IN MODEL        ║                │
      │                   ╚═════════════════════════════╝                │
      │ (Khu vực hàn Test Points & I2C sát mép dưới)                     │
      └──────────────────────────────────────────────────────────────────┘ 70 mm
```

> [!NOTE]
> **VÙNG PIN LIPO (BATTERY ZERO-THT: PASS IN CURRENT PLACEMENT MODEL, FINAL: PENDING PHYSICAL VERIFICATION):**  
> - Cell pin LiPo 523450 ($50 \times 34 \times 5.2\,\text{mm}$) đặt tại: $X = 22.0\text{--}72.0\,\text{mm}$, $Y = 20.0\text{--}56.0\,\text{mm}$ ở mặt đáy.
> - Cụm 3 nút bấm nằm ở $X = 10.0\text{--}20.0\,\text{mm}$ (ngoài vùng pin).
> - Socket ESP32 DevKit bắt đầu từ $X = 72.0\,\text{mm}$ lùi về sau (ngoài vùng pin).
> - Khối nguồn TP4056 và MT3608 nằm ở dải mép trên $Y = 2.0\text{--}18.0\,\text{mm}$ (ngoài vùng pin).
> - Module IMU WCMCU-20948 nằm ở mặt TOP của vùng giữa bo; các chân socket THT của chúng nếu cần sẽ được bố trí ở dải $Y = 56\text{--}68\,\text{mm}$ hoặc cắt cụt sát mặt bo và lót đệm Kapton + Foam 1.5mm.

---

## 3. Quy Chuẩn Chi Tiết Từng Phân Vùng Bố Trí (Placement Constraints)

### 3.1 Vùng điều khiển ngón tay (Front / User Control Area) [`DECIDED`]
- **Vị trí**: Phía đầu bo mạch ($X = 0\text{--}30\,\text{mm}$).
- **Thành phần**:
  - 3 nút bấm xúc giác 12x12mm (Model TC-1212T) trang bị **Button Cap tròn đường kính $\varnothing 12.0\,\text{mm}$**:
    - `SW_L` (Chuột Trái / OK): Tọa độ dự kiến $(X = 15\,\text{mm}, Y = 20\,\text{mm})$.
    - `SW_M` (Bật/Tắt Air Mouse): Tọa độ dự kiến $(X = 12\,\text{mm}, Y = 35\,\text{mm})$.
    - `SW_R` (Chuột Phải): Tọa độ dự kiến $(X = 15\,\text{mm}, Y = 50\,\text{mm})$.
- **Kiểm tra va chạm nắp nút (Cap Clearance Check)**:
  - Khoảng cách tim giữa `SW_L` và `SW_M`: $D_{center} \approx 15.3\,\text{mm}$.
  - Khe hở giữa 2 mép cap: $\text{Clearance} = 15.3 - 12.0 = 3.3\,\text{mm} > 3.0\,\text{mm}$.
  - **Kết luận**: Thỏa mãn tiêu chuẩn an toàn cơ khí. Hai nắp nút không chạm cọ vào nhau khi thao tác.
- **Đèn LED báo trạng thái (`D1`)**: Đặt tại $(X = 25\,\text{mm}, Y = 35\,\text{mm})$, điều khiển từ `GPIO32`, nằm giữa 3 nút bấm nhưng lùi về sau, không bị ngón tay che khi cầm thao tác.

### 3.2 Vùng cảm biến IMU WCMCU-20948 (Direct 3.3V Cluster)
- **Vị trí**: Mặt TOP, đặt tại $(X \approx 40\text{--}65\,\text{mm}, Y \approx 40\text{--}65\,\text{mm})$.
- **Kích thước & Footprint WCMCU-20948**:
  - Outline module: $26.7 \times 15.3\,\text{mm}$.
  - Socket cắm: `PinSocket_1x10_P2.54mm_Vertical` (10 chân thẳng hàng, bước chân $2.54\,\text{mm}$).
  - Trạng thái cơ khí: **`RESOLVED`** (`WEB_VERIFIED_DESIGN_REFERENCE`, đo đạc thước kẻ của user ~26.8x15.5mm đóng vai trò sanity check tương quan).
- **Bố cục nội bộ cụm cảm biến**:
  - Không còn module LDO 1.8V và module chuyển mức BSS138 (đã loại bỏ theo baseline Direct 3.3V, bring-up ngày 25/09/2026).
  - WCMCU-20948 nối thẳng `3V3`/`GND` và `SDA`/`SCL` (GPIO21/GPIO22) của ESP32; `NCS` nối `3V3`, `AD0` và `FSY` nối `GND`.
  - Đặt socket WCMCU-20948 sao cho đường I2C từ ESP32 tới module ngắn nhất có thể.
- **Cách ly nguồn xung MT3608**:
  - Module MT3608 nằm tại $X = 50\text{--}86\,\text{mm}$, $Y = 2\text{--}18\,\text{mm}$.
  - Khoảng cách không gian Euclidean giữa cuộn cảm MT3608 và chip ICM-20948 đạt $> 36\,\text{mm}$, giảm thiểu ghép cặp nhiễu điện từ trường.
- **Tránh rung chấn cơ học**: Cụm IMU nằm cách xa tiếp điểm nút bấm $> 30\,\text{mm}$.
- **Định hướng trục (Orientation)**: Socket 10 chân đặt song song với cạnh bo; mũi tên trục $X, Y$ thẳng hàng với hướng trỏ chuột.

### 3.3 Vùng vi điều khiển ESP32 (Antenna Placement Guideline theo chuẩn Espressif)
- **Vị trí**: Mặt TOP, đuôi bo mạch ($X = 72\text{--}127\,\text{mm}$, $Y = 21\text{--}49\,\text{mm}$).
- **Quy chuẩn bố trí ăng-ten**:
  - Đầu chứa ăng-ten PCB của ESP32 quay về phía sau bo mạch ($X \rightarrow 127\text{--}130\,\text{mm}$) hoặc nhô ra ngoài mép Carrier PCB (Antenna Overhang).
  - Khoảng không gian xung quanh và bên dưới ăng-ten ($15\,\text{mm}$) không phủ đồng, không đi dây tín hiệu, không có kim loại và tuyệt đối không có pin LiPo.
- **Cổng USB nạp code**: Quay ra mép đuôi hoặc mép hông, cắm cáp nạp firmware và debug Serial dễ dàng.

### 3.4 Vùng khối nguồn (Power Area Placement)
- **Vị trí**: Chạy dọc mép trên bo mạch ($Y = 2\text{--}19\,\text{mm}$).
- **Thứ tự bố trí**:
  `Cổng sạc Type-C TP4056 (X = 5..31mm)` $\rightarrow$ `Công tắc trượt SW1 (X = 35..45mm)` $\rightarrow$ `Module Boost MT3608 (X = 48..84mm)`.
- Cổng sạc Type-C nhô ra ngoài mép trái bo $\approx 1.2\,\text{mm}$.
- Biến trở MT3608 ngửa lên trên, dễ dàng căn chỉnh $5.0\,\text{V}$.
- **Cách ly nhiệt (Thermal Isolation)**: Khối nguồn nằm tách biệt ở dải biên, không xếp chồng lên thân pin LiPo.

---

## 4. Tiêu Chuẩn Bảo Vệ & Cách Ly Pin LiPo (Battery Safety & Insulation)

> [!CAUTION]
> **AN TOÀN PIN LIPO:**  
> Pin LiPo túi mềm rất dễ bị thủng nếu va chạm với các đầu chân hàn xuyên lỗ (THT leads) sắc nhọn ở mặt dưới mạch in 1 lớp. Bắt buộc tuân thủ kết cấu cách ly 3 tầng:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Mặt dưới bo mạch PCB (Bottom Copper — Không chân nhọn)    │
├─────────────────────────────────────────────────────────────┤
│ 2. Lớp băng keo cách điện chịu nhiệt Kapton (Polyimide Tape)│  -> Chống rách xước, chịu nhiệt >200°C
├─────────────────────────────────────────────────────────────┤
│ 3. Lớp xốp đệm cách điện mềm EVA/PE Foam dày 1.0 – 2.0 mm   │  -> Hấp thụ rung chấn, triệt tiêu lực tì đè
├─────────────────────────────────────────────────────────────┤
│ 4. Thân túi mềm pin LiPo 1S 1000mAh (Model 523450)          │  -> Cố định bằng băng keo pin hai mặt
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Đánh Giá Khả Năng Đi Dây 1 Lớp (Single-Layer Routability Assessment)

### 5.1 Phân tích các luồng tín hiệu I2C
1. **Luồng I2C Host (2 tín hiệu: SDA, SCL)**:
   - Chân `GPIO21 (SDA)` và `GPIO22 (SCL)` nằm ở **hàng chân bên phải (Right Header, pins 33 & 36)** của ESP32 DevKit.
   - $\rightarrow$ 2 đường I2C $3.3\,\text{V}$ (`IMU_SDA`, `IMU_SCL`) chạy thẳng song song từ ESP32 tới chân `SDI/SDA` và `SCLK/SCL` của WCMCU-20948 trên lớp Bottom, không có điểm giao cắt trong mô hình bố trí hiện tại (cần xác nhận lại khi route thật).
2. **Luồng Nút Nhấn (BTN_LEFT, BTN_RIGHT, BTN_MODE)**:
   - Các chân GPIO nút nhấn (`GPIO25`, `GPIO26`, `GPIO27`) tập trung ở **hàng chân bên trái (Left Header)**.
   - 3 đường tín hiệu chạy thẳng dọc hành lang bên trái tới các nút bấm.
3. **Luồng Nguồn Công Suất (`VBAT`, `V_SYS`, `5V`)**:
   - Chạy dọc theo mép trên cùng của bo mạch tới chân 19 (`5V/VIN`) của ESP32. Chiều rộng: $1.0\text{--}1.2\,\text{mm}$.
4. **Mặt phẳng Mass (Ground Pour)**:
   - Phủ mass toàn bộ diện tích trống ở lớp Bottom (trừ vùng ăng-ten ESP32).

### 5.2 Đánh giá các điểm giao cắt & Jumper
- **2–3 Jumper: ESTIMATE ONLY until routing is actually performed**.
  - *Jumper 1*: Đường cấp nguồn `3V3` từ chân 1 ESP32 vượt qua hàng tín hiệu sang nuôi WCMCU-20948 (`VCC`, `NCS`) và cổng I2C mở rộng.
  - *Jumper 2*: Đường tín hiệu đo pin `BAT_SENSE` từ cầu phân áp vượt qua đường nguồn phụ.
  - *Jumper 3 (Dự phòng)*: Đường tín hiệu LED trạng thái (`GPIO32`).
- **Kết luận định tuyến (Routability Verdict)**: **`PASS IN CURRENT MODEL`** — Nhờ giảm bus cảm biến từ 5 đường (SPI) xuống 2 đường (I2C), mức độ thông thoáng đi dây trên PCB 1 lớp tăng đáng kể.

---

## 6. Quy Trình Kiểm Tra Vật Lý Bắt Buộc Trước Khi Đặt Mạch (Before PCB Order — Mandatory Physical Check)

Trước khi chuyển sang bước xuất file Gerber và đặt gia công mạch in, người dùng bắt buộc phải dùng thước kẹp caliper đo trực tiếp các linh kiện thực tế và điền vào bảng kiểm tra:

| STT | Linh kiện cần đo | Thông số vật lý bắt buộc xác nhận | Giá trị đo thực tế (mm) | Trạng thái đối chiếu Footprint |
| :---: | :--- | :--- | :---: | :--- |
| **1** | **ESP32 DevKit 38-Pin** | - Khoảng cách 2 hàng chân cắm (Row Pitch)<br>- Chiều dài $\times$ Chiều rộng bo mạch<br>- Bước chân cắm (Pin Pitch) | `...... mm`<br>`...... mm`<br>`...... mm` | Chốt footprint $25.4\,\text{mm}$ hay $22.86\,\text{mm}$ |
| **2** | **WCMCU-20948** | - Chiều dài $\times$ Chiều rộng bo module: Chuẩn thiết kế $26.7 \times 15.3\,\text{mm}$<br>- Bước chân 10 header: Chuẩn thiết kế $2.54\,\text{mm}$<br>- Kiểm tra đối chiếu vật lý (Sanity check) | `26.7 mm`<br>`2.54 mm`<br>`Đã khớp (~26.8x15.5mm)` | `WEB_VERIFIED_DESIGN_REFERENCE` (`PHYSICAL_SANITY_CHECK_ONLY`). Blocker cơ khí: **`RESOLVED`**. |
| **3** | **Module TP4056** | - Chiều dài $\times$ Chiều rộng module sạc<br>- Vị trí 4 lỗ hàn góc (Pad Pitch)<br>- Độ nhô cổng sạc Type-C | `...... mm`<br>`...... mm`<br>`...... mm` | Khớp vị trí pad hàn và mép bo |
| **4** | **Module MT3608** | - Chiều dài $\times$ Chiều rộng module tăng áp<br>- Vị trí 4 pad hàn góc `VIN/VOUT`<br>- Chiều cao biến trở vi chỉnh | `...... mm`<br>`...... mm`<br>`...... mm` | Khớp vị trí pad hàn |
| **5** | **Tactile & Button Cap**| - Kích thước thân nút bấm ($12 \times 12$ hay $6 \times 6\,\text{mm}$)<br>- Đường kính ngoài nắp nút ($D_{cap}$)<br>- Kiểm tra độ khớp trục trụ và nắp | `...... mm`<br>`...... mm`<br>`Khớp/Lỏng` | Xác nhận khoảng cách tim nút $\ge D_{cap} + 3\,\text{mm}$ |
| **6** | **Pin LiPo 1S** | - Chiều dài $\times$ Rộng $\times$ Dày cell pin<br>- Chiều dài dây dẫn pin và đầu cắm JST-PH | `...... mm`<br>`...... mm` | Đảm bảo lọt trọn trong Battery Keepout Zone |
| **7** | **Công tắc nguồn** | - Bước chân công tắc trượt (Pin Pitch)<br>- Chiều cao cần gạt công tắc | `...... mm`<br>`...... mm` | Chốt lỗ hàn $2.54\,\text{mm}$ |
