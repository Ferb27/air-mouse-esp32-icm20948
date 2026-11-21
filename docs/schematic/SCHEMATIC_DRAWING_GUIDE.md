# HƯỚNG DẪN VẼ SƠ ĐỒ NGUYÊN LÝ AIR MOUSE V1 (SCHEMATIC DRAWING GUIDE)

> **Dự án**: Chuột bay không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems) — Mốc Báo cáo Giữa kỳ Tuần 5  
> **Tài liệu**: Cẩm nang Hướng dẫn Bố cục và Trình tự Vẽ Sơ đồ Nguyên lý Chuẩn EDA  
> **Phiên bản**: V2.1.0 — Direct 3.3V (đã xóa bước vẽ LDO 1.8V/BSS138 và test point 1V8, 2026-10-01)  
> **Kiến trúc phần cứng**: `DIRECT_3V3_FUNCTIONAL_CONFIRMED` (Xác minh thực tế trực tiếp 3.3V sau Hardware Bring-up)  
> **Trạng thái đồng bộ KiCad**: `KICAD_SYNC_STATUS: STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE` (KiCad schematic `hardware/air_mouse.kicad_sch` vẫn giữ BSS138 và LDO 1.8V lịch sử, chờ cập nhật qua KiCad MCP Server)  
> **Mục tiêu sử dụng**: Cung cấp hướng dẫn trực quan, phân vùng bản vẽ (Canvas Layout Architecture), trình tự các bước vẽ mạch chi tiết, bảng quản lý miền nguồn, bảng xử lý chân bỏ trống (No Connect) và trang tra cứu nhanh (Quick Reference Sheet) cho kiến trúc nguyên mẫu trực tiếp 3.3V.

---

## 1. Kiến Trúc Bố Cục Bản Vẽ (Canvas Layout Architecture)

Để sơ đồ nguyên lý đạt tính mỹ thuật kỹ thuật cao, dễ theo dõi dòng tín hiệu (signal flow) từ trái sang phải và từ trên xuống dưới, khuyến nghị thiết lập trang vẽ khổ **A4 Landscape** và phân chia thành **4 Phân Vùng Chức Năng Cốt Lõi (4 Functional Zones)** (khối chuyển mức và LDO 1.8V đã loại bỏ):

### A. Bản Đồ Sơ Đồ Nguyên Lý Trực Quan Toàn Hệ Thống (Direct 3.3V System Visual)

```mermaid
graph LR
    subgraph S1["PHÂN VÙNG 1: NGUỒN & SẠC PIN"]
        BAT1["Pin LiPo 1S<br/>3.7V 1000mAh"] -->|VBAT| J1["Cọc JST-PH 2.0<br/>J1 (J_BAT)"]
        J1 -->|VBAT| MOD1["Module Sạc TP4056<br/>Pad B+ / B-"]
        MOD1 -->|V_SW_IN<br/>(OUT+)| SW1["Công tắc gạt SPDT<br/>SW1 (SS12D00)"]
        SW1 -->|V_SYS<br/>(Pin 2 COM)| MOD2["Module Tăng Áp<br/>MT3608 5V (2A)"]
        MOD2 -->|5V (VOUT+)| C2["Tụ Hóa 10µF 25V<br/>C2 (Lọc nguồn 5V)"]
    end

    subgraph S2["PHÂN VÙNG 2: VI ĐIỀU KHIỂN ESP32"]
        MOD2 -->|5V| ESP_VIN["ESP32 DevKit 38P<br/>Chân 19: VIN"]
        ESP_3V3["ESP32 DevKit 38P<br/>Chân 1: 3V3"]
        ESP_ADC["ESP32 DevKit 38P<br/>Chân 5: GPIO34"]
        ESP_LED["ESP32 DevKit 38P<br/>Chân 7: GPIO32"]
        ESP_BTN["ESP32 DevKit 38P<br/>Chân 9, 10, 11: GPIO25, 26, 27"]
        ESP_I2C["ESP32 DevKit 38P<br/>Chân 33: GPIO21 (SDA)<br/>Chân 36: GPIO22 (SCL)"]
    end

    subgraph S3["PHÂN VÙNG 3: CẢM BIẾN IMU TRỰC TIẾP 3.3V"]
        ESP_3V3 -->|3V3| U2["Cảm Biến 9-DOF IMU<br/>WCMCU-20948 (ICM-20948)<br/>VCC: 3.3V | NCS: 3.3V<br/>AD0: GND (0x68) | FSY: GND"]
        ESP_I2C <-->|IMU_SDA (GPIO21)<br/>IMU_SCL (GPIO22)| U2
    end

    subgraph S4["PHÂN VÙNG 4: NÚT BẤM, LED & CẦU ĐO PIN"]
        SW_L["Nút Trái SW2 (TC-1212T)"] -->|BTN_LEFT| ESP_BTN
        SW_R["Nút Phải SW3 (TC-1212T)"] -->|BTN_RIGHT| ESP_BTN
        SW_M["Nút Mode SW4 (TC-1212T)"] -->|BTN_MODE| ESP_BTN
        ESP_LED -->|LED_STATUS| R1["Trở R1 (1kΩ)"] --> D1["LED D1 (Green 3mm)"] --> GND_LED["GND"]
        SW1 -->|V_SYS| R2["Trở R2 (100kΩ)"] --> NODE_SENSE["BAT_SENSE<br/>(1.5V - 2.1V)"]
        NODE_SENSE --> R3["Trở R3 (100kΩ) || Tụ C1 (100nF)"] --> GND_DIV["GND"]
        NODE_SENSE -->|BAT_SENSE| ESP_ADC
    end

    subgraph S5["MỞ RỘNG & TEST POINTS"]
        ESP_I2C -.-> J2["Header I2C 1x4 (J2)<br/>3V3, GND, SDA, SCL"]
        TP_BANK["Test Points TP1-TP4 (1x4 Header: SCL, SDA, 3V3, GND)<br/>Test Points TP8-TP11 (PCB Pads: VBAT, VSYS, 5V, 3V3)"]
    end
```

---

### B. Hình Vẽ Sơ Đồ Nguyên Lý Chi Tiết Từng Phân Vùng Chức Năng

#### 1. Hình vẽ Khối Nguồn & Tăng Áp (Power & Charging Subsystem)

```text
               +-------------------------------------------------------------------------+
               | KHỐI NGUỒN & SẠC PIN (POWER SUBSYSTEM)                                  |
               |                                                                         |
  [BAT1]       |       [J1: JST-PH]             [MOD1: TP4056 TYPE-C MODULE]             |
+----------+   |      +------------+           +------------------------------+          |
| Pin LiPo | 1 | (VBAT)| 1        1 | (VBAT)   | Pad B+              Pad OUT+ | (V_SW_IN)|
| 1S 3.7V  |---+----->|            |---------->|                              |----+     |
|          | 2 | (BAT-)| 2        2 | (BAT-)   | Pad B-              Pad OUT- |    |     |
|          |---+----->|            |---------->|                                  |     |
+----------+   |      +------------+           +------------------------------+   |     |
               |                                              | (GND)             |     |
               |                                              v                   |     |
               |                                             GND                  |     |
               |                                                                  |     |
               |      [SW1: SS12D00 SPDT]              [MOD2: MT3608 BOOST]       v     |
               |     +--------------------+           +---------------------+   Chân 1  |
               |     | Chân 1 (V_SW_IN)   |<------------------------------------+       |
               |     | Chân 2 (V_SYS/COM) |----+ (V_SYS)                                |
               |     | Chân 3 (NC)        |    |                                        |
               |     +--------------------+    v                                        |
               |        ^                Pad VIN+        Pad VOUT+ (5V)                 |
               |        |                 +---------------------+                       |
               |       (X) No Connect     |  MT3608 STEP-UP 5V  |---------+ (Net 5V)    |
               |                          | Pad VIN-  Pad VOUT- |         |             |
               |                          +---------------------+         |             |
               |                                |           |             |   +---+ (+) |
               |                                v           v             +---|C2 |     |
               |                               GND         GND            |   |10u|     |
               |                                                          |   +---+ (-) |
               |                                                          |     |       |
               |                                                          v     v       |
               |                                                 ESP32 VIN     GND      |
               +-------------------------------------------------------------------------+
```

#### 2. Hình vẽ Khối Cảm Biến ICM-20948 Trực Tiếp 3.3V (WCMCU-20948 Direct 3.3V)

```text
               +------------------------------------------------------------------------------------+
               | KHỐI CẢM BIẾN IMU TRỰC TIẾP 3.3V (WCMCU-20948 DIRECT 3.3V I2C BUS)                |
               |                                                                                    |
               |                                            [U2: WCMCU-20948 (ICM-20948)]           |
               |                                           +------------------------------+         |
(ESP32 3V3) ---------------------------------------------->| Chân 1: VCC (3.3V)           |         |
(ESP32 GND) ---------------------------------------------->| Chân 2: GND                  |         |
(ESP32 GPIO22) ------------------------------------------->| Chân 3: SCL (I2C 400kHz)     |         |
(ESP32 GPIO21) ------------------------------------------->| Chân 4: SDA (I2C Data)       |         |
(ESP32 3V3) ---------------------------------------------->| Chân 5: NCS (Khóa I2C)       |         |
(ESP32 GND) ---------------------------------------------->| Chân 6: AD0 (Địa chỉ 0x68)   |         |
               |                                           | Chân 7: INT (Để hở / NC)     |         |
(ESP32 GND) ---------------------------------------------->| Chân 8: FSY (Nối mass)       |         |
               |                                           | Chân 9: ACL (CẤM NỐI - NC)   |         |
               |                                           | Chân 10: ADA (CẤM NỐI - NC)  |         |
               |                                           +------------------------------+         |
               | Ghi chú: Module đã có sẵn trở kéo 10k onboard trên SDA/SCL lên chân VCC (3.3V).    |
               +------------------------------------------------------------------------------------+
```

#### 3. Hình vẽ Sơ Đồ Chân Bo ESP32 DevKit 38-Pin

```text
               +-------------------------------------------------------------------------+
               | KHỐI VI ĐIỀU KHIỂN TRUNG TÂM (ESP32 DEVKIT V1 38-PIN)                  |
               |                                                                         |
               |                            +-----------------+                          |
               |                            |   PCB ANTENNA   |                          |
               |                            +-----------------+                          |
               |                     [HÀNG TRÁI]           [HÀNG PHẢI]                   |
               |    (Net 3V3) <------| 1: 3V3              38: GND   |------> (GND)      |
               |          (NC) (X)---| 2: EN               37: IO23  |---(X) (NC)        |
               |          (NC) (X)---| 3: VP/IO36          36: IO22  |<-----> IMU_SCL    |
               |          (NC) (X)---| 4: VN/IO39          35: TXD0  |---(X) (NC)        |
               |   (BAT_SENSE) ----->| 5: IO34 (ADC1_6)    34: RXD0  |---(X) (NC)        |
               |          (NC) (X)---| 6: IO35             33: IO21  |<-----> IMU_SDA    |
               |  (LED_STATUS) ----->| 7: IO32             32: GND   |------> (GND)      |
               |          (NC) (X)---| 8: IO33             31: IO19  |---(X) (NC)        |
               |    (BTN_LEFT) ----->| 9: IO25             30: IO18  |---(X) (NC)        |
               |   (BTN_RIGHT) ----->| 10: IO26            29: IO5   |---(X) (NC)        |
               |    (BTN_MODE) ----->| 11: IO27            28: IO17  |---(X) (NC)        |
               |          (NC) (X)---| 12: IO14            27: IO16  |---(X) (NC)        |
               |          (NC) (X)---| 13: IO12            26: IO4   |---(X) (NC)        |
               |         (GND) <-----| 14: GND             25: IO0   |---(X) (NC)        |
               |          (NC) (X)---| 15: IO13            24: IO2   |---(X) (NC)        |
               |    (FLASH CẤM) (X)--| 16: SD2             23: IO15  |---(X) (NC)        |
               |    (FLASH CẤM) (X)--| 17: SD3             22: SD1   |---(X) (FLASH CẤM) |
               |    (FLASH CẤM) (X)--| 18: CMD             21: SD0   |---(X) (FLASH CẤM) |
               |  (Từ MT3608 5V) --->| 19: 5V (VIN)        20: CLK   |---(X) (FLASH CẤM) |
               |                     +-------------------------------+                   |
               +-------------------------------------------------------------------------+
```

#### 4. Hình vẽ Khối Nút Bấm, LED & Cầu Phân Áp Đo Pin

```text
               +-------------------------------------------------------------------------+
               | KHỐI GIAO DIỆN NGƯỜI DÙNG & ĐO PIN (BUTTONS, LED & BATTERY SENSE)       |
               |                                                                         |
               |   [NÚT BẤM - ACTIVE-LOW]              [LED BÁO TRẠNG THÁI]              |
               |   (ESP32 IO25) --->+  SW2 (Left)      (ESP32 IO32)                      |
               |                    o--/ o---> GND          |                            |
               |                                            v                            |
               |   (ESP32 IO26) --->+  SW3 (Right)        +---+  R1 (1k 1/4W)            |
               |                    o--/ o---> GND        |   |                          |
               |                                          +---+                          |
               |   (ESP32 IO27) --->+  SW4 (Mode)           | (Net LED_ANODE)            |
               |                    o--/ o---> GND          v (Chân 2 Anode)             |
               |                                          +---+                          |
               |                                           \ /  D1 (LED Green 3mm)       |
               |   [CẦU PHÂN ÁP ĐO PIN 1:2]                ---                           |
               |   (Nguồn pin sau công tắc V_SYS)           | (Chân 1 Cathode)           |
               |               |                            v                            |
               |               v                           GND                           |
               |             +---+ R2 (100k 1%)                                          |
               |             |   |                                                       |
               |             +---+                                                       |
               |               |                                                         |
               |               +-----------------------> Đến Chân 5 ESP32 (GPIO34)       |
               |               | (Net BAT_SENSE: 1.5 - 2.1V)                             |
               |        +------+------+                                                  |
               |        |             |                                                  |
               |      +---+ R3      +---+ C1                                             |
               |      |   | 100k    |   | 100nF                                          |
               |      +---+ 1%      +---+ 50V                                            |
               |        |             |                                                  |
               |        v             v                                                  |
               |       GND           GND                                                 |
               +-------------------------------------------------------------------------+
```

#### 5. Hình vẽ Cổng I2C Mở Rộng & Bảng Điểm Đo Kiểm (Test Points)

```text
               +-------------------------------------------------------------------------+
               | KHỐI NGOẠI VI & TEST POINTS (EXPANSION & HARDWARE DEBUG)                |
               |                                                                         |
               |      [J2: I2C EXTENSION HEADER 1x4]       [BẢNG TEST POINTS DEBUG]      |
               |             +--------------+              Header 1x4:                   |
               |   Chân 1    | 3V3          |              (O) TP1:  IMU_SCL             |
               |   Chân 2    | GND          |              (O) TP2:  IMU_SDA             |
               |   Chân 3    | SDA (GPIO21) |              (O) TP3:  3V3                 |
               |   Chân 4    | SCL (GPIO22) |              (O) TP4:  GND                 |
               |             +--------------+              Pad đồng PCB:                 |
               |                                           (O) TP8:  VBAT                |
               |                                           (O) TP9:  V_SYS               |
               |                                           (O) TP10: 5V                  |
               |                                           (O) TP11: 3V3                 |
               |                                           (TP5–TP7 đã bỏ cùng khối 1V8) |
               +-------------------------------------------------------------------------+
```

---

### C. Nguyên tắc phối màu và quy ước nét vẽ:
1. **Đường dây điện thật (Explicit Manhattan Wires)**: Ưu tiên vẽ đường dây thẳng đứng hoặc nằm ngang, bẻ góc vuông $90^\circ$. Tránh đi dây chéo góc.
2. **Điểm giao cắt (Junctions)**: Mọi điểm nối ngã ba hoặc ngã tư bắt buộc phải có dấu chấm liên kết (Junction Dot). Hai dây cắt nhau không nối tuyệt đối không được có chấm.
3. **Nhãn mạng (Net Labels)**: Đặt nhãn mạng rõ ràng tại các đường bus chính (`5V`, `3V3`, `GND`, `BAT_SENSE`, `IMU_SDA`, `IMU_SCL`, v.v.) để vừa nhìn thấy dây nối vừa dễ tra cứu netlist.

---

## 2. Trình Tự Vẽ Sơ Đồ Nguyên Lý 10 Bước (10-Step Step-by-Step Drawing Sequence)

Để hoàn thiện bản vẽ nhanh chóng và không bỏ sót linh kiện, hãy thực hiện tuần tự theo 10 bước sau (hai bước vẽ LDO 1.8V và mạch chuyển mức BSS138 của bản cũ đã bị xóa vì kiến trúc Direct 3.3V không còn hai khối này):

### Bước 1: Thiết lập Khung Bản Vẽ và Khung Tiêu Đề (Title Block)
- Tạo trang schematic mới trên KiCad / EDA với kích thước chuẩn **A4 Landscape** ($297 \times 210\,\text{mm}$).
- Điền đầy đủ thông tin Khung tên (Title Block):
  - **Title**: `AIR MOUSE BLE HID - SYSTEM SCHEMATIC`
  - **Revision**: `v1.0.0`
  - **Company / Group**: `Embedded Systems Project Group - Air Mouse Team`
  - **Comment 1**: `ESP32 Classic + ICM-20948 (Rate-Control BLE Mouse)`
  - **Date**: `2026-03`

### Bước 2: Bố trí Khối Nguồn & Sạc Pin (Phân vùng 1 — Trái Ngoài)
- Đặt biểu tượng Pin `BAT1` và Cọc cắm 2 chân `J1` (`JST_PH_B2B-PH-K`). Nối cực dương pin vào chân 1 (`VBAT`), cực âm vào chân 2 (nhãn mạng `GND_BAT_CELL`, **không phải** `GND`).
- Đặt Module sạc `MOD1` (`TP4056`). Nối chân 1 `J1` vào pad `B+`, chân 2 `J1` vào pad `B-` (mạng `GND_BAT_CELL`). Chỉ pad `OUT-` mới nối xuống biểu tượng `GND`. **Tuyệt đối không** nối `B-` với `GND` hoặc `OUT-` bên ngoài module, vì sẽ bypass MOSFET bảo vệ FS8205A.
- Đặt Công tắc trượt `SW1` (`1P2T / SPDT`). Nối pad `OUT+` của `MOD1` vào chân 1 của `SW1` (nhãn mạng `V_SW_IN`).
- Chân 2 (Common) của `SW1` đặt nhãn mạng `V_SYS`. Chân 3 của `SW1` để hở và gắn cờ No Connect `X`.
- Đặt Module tăng áp `MOD2` (`MT3608`). Nối nhãn `V_SYS` vào pad `VIN+`. Nối pad `VIN-` và pad `VOUT-` xuống `GND`.
- Pad `VOUT+` của `MOD2` đặt nhãn mạng `5V`. Đặt tụ hóa `C2` ($10\,\mu\text{F}$) mắc song song giữa pad `VOUT+` ($+$) và `GND` ($-$).

### Bước 3: Đặt Bo Vi Điều Khiển Trung Tâm (Phân vùng 2 — Giữa Bản Vẽ)
- Đặt biểu tượng module 38 chân `U1` (`ESP32 DevKit V1 38-Pin` hoặc 2 hàng header 1x19 `J_ESP_L`, `J_ESP_R`).
- Nối đường nguồn `5V` từ ngõ ra `MOD2` thẳng vào chân 19 (`VIN`) của `U1`.
- Nối các chân mass: Chân 14, Chân 32, Chân 38 của `U1` xuống biểu tượng `GND`.
- Chân 1 (`3V3`) của `U1` đặt nhãn nguồn `3V3` để cấp cho các khối ngoại vi.

### Bước 4: Bố trí Module Cảm Biến Chuyển Động ICM-20948 (Phân vùng 3 — Bên Phải)
- Đặt biểu tượng module 10 chân `U2` (`WCMCU-20948`).
- Nối chân 1 (`VCC`) vào đường nguồn `3V3` (chân 1 của `U1`).
- Nối chân 2 (`GND`) xuống mass `GND`.
- **Cấu hình chân chế độ (Crucial)**:
  - Chân 5 (`NCS`): Nối cứng lên đường nguồn `3V3` (khóa chế độ giao tiếp I2C).
  - Chân 6 (`AD0`): Nối cứng xuống mass `GND` (cố định địa chỉ I2C 7-bit là `0x68`).
  - Chân 8 (`FSY`): Nối cứng xuống mass `GND` (khóa tính năng Frame Sync).
- Chân 7 (`INT`): Để hở và gắn cờ No Connect `X` (V1 đọc cảm biến bằng polling 100 Hz, chưa dùng ngắt).
- **Chân để hở bắt buộc**: Chân 9 (`ACL`) và Chân 10 (`ADA`) gắn cờ No Connect `X`. Tuyệt đối không nối vào bus I2C của MCU.

### Bước 5: Đi Dây Bus Giao Tiếp I2C Trực Tiếp 3.3V (Explicit Manhattan Wires)
- Từ chân 33 (`GPIO21`) của `U1`, vẽ dây nối thẳng sang chân 4 (`SDA`) của `U2`. Gắn nhãn mạng `IMU_SDA`.
- Từ chân 36 (`GPIO22`) của `U1`, vẽ dây nối thẳng sang chân 3 (`SCL`) của `U2`. Gắn nhãn mạng `IMU_SCL`.
- Không vẽ thêm trở kéo: module WCMCU-20948 đã có sẵn trở kéo $10\,\text{k}\Omega$ onboard lên `VCC` ($3.3\,\text{V}$).

### Bước 6: Bố trí Khối Nút Bấm Người Dùng (Phân vùng 4 — Dưới Phải)
- Đặt 3 nút nhấn xúc giác `SW2`, `SW3`, `SW4` (`TC-1212T`).
- Nối tiếp điểm 2 của cả 3 nút bấm xuống mass `GND`.
- Tiếp điểm 1 của `SW2` (Left Click): Vẽ dây nối vào chân 9 (`GPIO25`) của `U1`. Gắn nhãn `BTN_LEFT`.
- Tiếp điểm 1 của `SW3` (Right Click): Vẽ dây nối vào chân 10 (`GPIO26`) của `U1`. Gắn nhãn `BTN_RIGHT`.
- Tiếp điểm 1 của `SW4` (Mode Toggle): Vẽ dây nối vào chân 11 (`GPIO27`) của `U1`. Gắn nhãn `BTN_MODE`.

### Bước 7: Bố trí Khối Đèn LED Chỉ Thị Trạng Thái (Phân vùng 4)
- Đặt điện trở hạn dòng `R1` ($1.0\,\text{k}\Omega$) và Đèn LED 3mm `D1` (Green).
- Chân 1 của `R1`: Vẽ dây nối vào chân 7 (`GPIO32`) của `U1`. Gắn nhãn `LED_STATUS`.
- Chân 2 của `R1`: Nối trực tiếp vào cực Anode (chân 2) của `D1` (nhãn mạng `LED_ANODE`).
- Cực Cathode (chân 1 vát cạnh) của `D1`: Nối xuống mass chung `GND`.

### Bước 8: Bố trí Cầu Phân Áp Đo Điện Áp Pin (Phân vùng 4)
- Đặt điện trở trên `R2` ($100\,\text{k}\Omega$), điện trở dưới `R3` ($100\,\text{k}\Omega$) và Tụ gốm `C1` ($100\,\text{nF}$).
- Chân 1 của `R2`: Nối vào nguồn dương hệ thống `V_SYS` (sau công tắc `SW1`).
- Điểm nút nối giữa Chân 2 của `R2`, Chân 1 của `R3` và Chân 1 của `C1`: Đặt nhãn mạng `BAT_SENSE`.
- Từ nhãn `BAT_SENSE`, vẽ dây nối thẳng vào chân 5 (`GPIO34` / `ADC1_CH6`) của `U1`.
- Chân 2 của `R3` và Chân 2 của `C1`: Nối xuống mass chung `GND`.

### Bước 9: Bố trí Đầu Nối Mở Rộng và Các Điểm Đo Kiểm Debug (Phân vùng 5 — Góc Dưới Trái)
- Đặt cọc cắm 4 chân `J2` (`PinHeader_1x04_P2.54mm`):
  - Chân 1 nối vào mạng `3V3`.
  - Chân 2 nối vào `GND`.
  - Chân 3 nối vào mạng `IMU_SDA`.
  - Chân 4 nối vào mạng `IMU_SCL`.
- Đặt 8 điểm đo kiểm Test Point (giữ số hiệu theo `SCHEMATIC_NETLIST.md` V2; `TP5`–`TP7` của bản 1.8V đã bỏ):
  - Header 1x4: `TP1` nối `IMU_SCL`, `TP2` nối `IMU_SDA`, `TP3` nối `3V3`, `TP4` nối `GND`.
  - Pad đồng PCB: `TP8` nối `VBAT`, `TP9` nối `V_SYS`, `TP10` nối `5V`, `TP11` nối `3V3`.

### Bước 10: Đánh Dấu Cờ "No Connect" (NC) và Chạy Kiểm Tra Quy Tắc Điện Học (ERC)
- Đặt cờ No Connect (dấu chéo xanh `X`) lên toàn bộ các chân không sử dụng của ESP32 và các module theo danh sách ở Mục 4.
- Chạy công cụ **Electrical Rules Check (ERC)** trong KiCad / EDA.
- Đảm bảo đạt kết quả: **0 Errors, 0 Warnings** (hoặc chỉ có cảnh báo chấp nhận được về chân cấp nguồn đã được giải quyết bằng `PWR_FLAG`).

---

## 3. Bảng Quản Lý Miền Nguồn Hệ Thống (Power Domain Summary)

| Miền điện áp (Domain) | Điện áp danh định | Dải điện áp hoạt động | Nguồn cung cấp (Source) | Dòng đỉnh dự kiến (Peak Current) | Các linh kiện và IC tiêu thụ | Yêu cầu tụ lọc / ổn định |
| :---: | :---: | :---: | :--- | :---: | :--- | :--- |
| **`VBAT`** | $3.7\,\text{V}$ | $3.0\text{--}4.2\,\text{V}$ | Cell pin LiPo 1S qua cọc J1 | $1.5\,\text{A}$ (sạc / xả) | Module sạc TP4056 (Pad `B+`) | Tụ trên mạch bảo vệ pin |
| **`V_SYS`** | $3.7\,\text{V}$ | $3.0\text{--}4.2\,\text{V}$ | Sau công tắc gạt chính SW1 | $1.2\,\text{A}$ | Ngõ vào tăng áp MT3608 (`VIN+`), Cầu phân áp đo pin R2 | Tụ gốm tích hợp ngõ vào MT3608 |
| **`5V`** | $5.0\,\text{V}$ | $4.9\text{--}5.1\,\text{V}$ | Module tăng áp DC-DC MT3608 | $800\,\text{mA}$ | Chân `VIN` của bo ESP32 DevKit | Tụ hóa $C_2 = 10\,\mu\text{F}$ THT đặt sát chân VIN ESP32 |
| **`3V3`** | $3.3\,\text{V}$ | $3.25\text{--}3.35\,\text{V}$ | LDO 3.3V trên board DevKit | $150\,\text{mA}$ | Lõi SoC ESP32, Module cảm biến WCMCU-20948 (`VCC`, `NCS`), Cổng I2C ngoài J2 | Tụ gốm tích hợp onboard bo ESP32 |

---

## 4. Bảng Xử Lý Các Chân Không Sử Dụng (Unused / No-Connect Pins Table)

Để sơ đồ nguyên lý không bị cảnh báo chân hở (unconnected pin) khi chạy ERC trong KiCad, toàn bộ các chân dưới đây **BẮT BUỘC ĐƯỢC GẮN CỜ NO CONNECT (`X`)**:

| Linh kiện / Module | Ký hiệu chân (Pin Name) | Số thứ tự chân (Pin Num) | Lý do không sử dụng / Cấm kết nối | Hành động trên Schematic |
| :--- | :--- | :---: | :--- | :---: |
| **U1** (ESP32 DevKit) | `EN` | 2 | Đã có nút bấm EN và mạch RC reset onboard bo DevKit | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO36 (VP)` | 3 | Chân ADC input-only, không dùng trong V1 | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO39 (VN)` | 4 | Chân ADC input-only, không dùng trong V1 | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO35` | 6 | Chân ADC input-only, dự phòng | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO33` | 8 | Chân GPIO tự do, dự phòng mở rộng | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO14, GPIO12` | 12, 13 | Chân Strapping / JTAG, để trống tránh lỗi boot | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO13` | 15 | Chân GPIO tự do, dự phòng mở rộng | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `SD2, SD3, CMD` | 16, 17, 18 | **CHÂN FLASH NỘI BỘ — CẤM TUYỆT ĐỐI NỐI DÂY** | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `CLK, SD0, SD1` | 20, 21, 22 | **CHÂN FLASH NỘI BỘ — CẤM TUYỆT ĐỐI NỐI DÂY** | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO15, 2, 0` | 23, 24, 25 | Chân Strapping Pins cấu hình boot ROM | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO4, 16, 17` | 26, 27, 28 | Chân GPIO tự do / UART phụ | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO5, 18, 19` | 29, 30, 31 | Chân bus SPI nội bộ / GPIO tự do | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `RXD0, TXD0` | 34, 35 | Cổng nạp UART chính (đã nối chip USB-UART onboard) | Gắn cờ No Connect (`X`) |
| **U1** (ESP32 DevKit) | `GPIO23` | 37 | Chân GPIO tự do, dự phòng mở rộng | Gắn cờ No Connect (`X`) |
| **U2** (WCMCU-20948) | `ACL` (Aux SCL) | 9 | Bus I2C Master phụ — CẤM NỐI VÀO BUS CHÍNH CỦA MCU | Gắn cờ No Connect (`X`) |
| **U2** (WCMCU-20948) | `ADA` (Aux SDA) | 10 | Bus I2C Master phụ — CẤM NỐI VÀO BUS CHÍNH CỦA MCU | Gắn cờ No Connect (`X`) |
| **SW1** (Công tắc nguồn)| `Pin 3` (OFF Throw)| 3 | Tiếp điểm vị trí tắt không cần cấp điện | Gắn cờ No Connect (`X`) |
| **U2** (WCMCU-20948) | `INT` | 7 | Chưa dùng ngắt phần cứng (firmware polling 100 Hz) | Gắn cờ No Connect (`X`) |

---

## 5. Bảng Tra Cứu Nhanh 1 Trang Cho Kỹ Sư Vẽ Mạch (Pin-to-Pin Quick Reference Sheet)

Bảng tra cứu "Copy-Paste Ready" dưới đây tổng hợp cô đọng toàn bộ linh kiện chính (kiến trúc Direct 3.3V, không còn U3/U4/C3/C4), số chân và đích nối tương ứng:

```text
==============================================================================================
AIR MOUSE V1 — PIN-TO-PIN CONNECTION QUICK REFERENCE SHEET
==============================================================================================
[POWER SUBSYSTEM]
BAT1 (+)        --> J1 Pin 1 (VBAT)
BAT1 (-)        --> J1 Pin 2 (GND_BAT_CELL)
J1 Pin 1        --> MOD1 Pad B+ (VBAT)
J1 Pin 2        --> MOD1 Pad B- (GND_BAT_CELL — KHÔNG nối GND)
MOD1 Pad OUT+   --> SW1 Pin 1 (V_SW_IN)
MOD1 Pad OUT-   --> GND  (gốc của GND hệ thống)
SW1 Pin 2 (COM) --> MOD2 Pad VIN+ (V_SYS)  &  R2 Pin 1 (V_SYS)
SW1 Pin 3       --> NO CONNECT (X)
MOD2 Pad VIN-   --> GND
MOD2 Pad VOUT-  --> GND
MOD2 Pad VOUT+  --> U1 Pin 19 (5V)  &  C2 (+) (5V)
C2 (-)          --> GND

[MOTION SENSOR — WCMCU-20948, DIRECT 3.3V]
U2 Pin 1 (VCC)  --> U1 Pin 1 (3V3)
U2 Pin 2 (GND)  --> GND
U2 Pin 3 (SCL)  --> U1 Pin 36 (GPIO22)  (IMU_SCL)
U2 Pin 4 (SDA)  --> U1 Pin 33 (GPIO21)  (IMU_SDA)
U2 Pin 5 (NCS)  --> 3V3  (I2C Mode Lock)
U2 Pin 6 (AD0)  --> GND  (I2C Address = 0x68 Lock)
U2 Pin 7 (INT)  --> NO CONNECT (X)
U2 Pin 8 (FSY)  --> GND  (Frame Sync Disabled)
U2 Pin 9 (ACL)  --> NO CONNECT (X)
U2 Pin 10 (ADA) --> NO CONNECT (X)

[MCU SUBSYSTEM — ESP32 DEVKIT 38-PIN]
U1 Pin 1 (3V3)  --> U2 Pin 1 (VCC)  &  U2 Pin 5 (NCS)  &  J2 Pin 1 (3V3)  &  TP3  &  TP11
U1 Pin 5 (IO34) --> R2 Pin 2  &  R3 Pin 1  &  C1 Pin 1 (BAT_SENSE)
U1 Pin 7 (IO32) --> R1 Pin 1 (LED_STATUS)
U1 Pin 9 (IO25) --> SW2 Pin 1 (BTN_LEFT)
U1 Pin 10 (IO26)--> SW3 Pin 1 (BTN_RIGHT)
U1 Pin 11 (IO27)--> SW4 Pin 1 (BTN_MODE)
U1 Pin 14 (GND) --> GND
U1 Pin 19 (VIN) --> MOD2 Pad VOUT+ (5V)
U1 Pin 32 (GND) --> GND
U1 Pin 33 (IO21)--> U2 Pin 4 (SDA)  &  J2 Pin 3  &  TP2  (IMU_SDA)
U1 Pin 36 (IO22)--> U2 Pin 3 (SCL)  &  J2 Pin 4  &  TP1  (IMU_SCL)
U1 Pin 38 (GND) --> GND

[BUTTONS, LED & BATTERY SENSE]
SW2 Pin 2       --> GND
SW3 Pin 2       --> GND
SW4 Pin 2       --> GND
R1 Pin 2        --> D1 Pin 2 (Anode) (LED_ANODE)
D1 Pin 1 (Cath) --> GND
R2 Pin 1        --> SW1 Pin 2 (V_SYS)
R2 Pin 2        --> U1 Pin 5 (GPIO34)  &  R3 Pin 1  &  C1 Pin 1 (BAT_SENSE)
R3 Pin 2        --> GND
C1 Pin 2        --> GND

[I2C EXPANSION HEADER]
J2 Pin 1        --> 3V3
J2 Pin 2        --> GND
J2 Pin 3        --> IMU_SDA (U1 Pin 33)
J2 Pin 4        --> IMU_SCL (U1 Pin 36)

[TEST POINTS]
TP1 --> IMU_SCL   TP2 --> IMU_SDA   TP3 --> 3V3   TP4 --> GND      (Header 1x4)
TP8 --> VBAT      TP9 --> V_SYS     TP10 --> 5V   TP11 --> 3V3     (Pad đồng PCB)
==============================================================================================
```
