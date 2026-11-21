# BẢNG DỰ TOÁN & ĐẶC TẢ LINH KIỆN V1 (BILL OF MATERIALS - BOM V1)

> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems)  
> **Phiên bản BOM**: V2.0.0 — Direct 3.3V Reconciled & Audited BOM  
> **Trạng thái phê duyệt BOM**: `PROVISIONAL_PROCUREMENT_LIST` (Danh mục mua sắm tạm thời — Chưa đạt trạng thái sẵn sàng mua sắm)  
> **Kiến trúc phần cứng**: `DIRECT_3V3_FUNCTIONAL_CONFIRMED` (Loại bỏ BSS138 và LDO 1.8V sau Hardware Bring-up)  
> **WCMCU Mechanical Blocker**: `RESOLVED` (Kích thước module $26.7 \times 15.3\,\text{mm}$, pitch $2.54\,\text{mm}$)  
> **Trạng thái giá**: `REFERENCE_PRICE / NEEDS_RECHECK` (Toàn bộ đơn giá là giá tham chiếu lịch sử, cần kiểm tra lại trước khi giải ngân)  
>
> **Quy ước nguồn chân lý (Source of Truth Hierarchy)**:
> 1. `docs/HARDWARE_BRINGUP_DIRECT_3V3_2026-09-25.md` (Báo cáo Bring-up thực tế)
> 2. `docs/AIR_MOUSE_HARDWARE_ARCHITECTURE.md` (Kiến trúc phần cứng V4.0.0)
> 3. `docs/PCB_MECHANICAL_PLACEMENT.md` (Bố cục cơ khí & an toàn pin)
> 4. `docs/BOM_V1.md`
> 5. Thiết kế Schematic hiện hành (`hardware/air_mouse.kicad_sch` — `STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE`)
>
> **Quy ước trạng thái mua sắm (Procurement Status)**:
> - `OWNED`: Người dùng đã có sẵn linh kiện thực tế (Chi phí mua thêm = 0 VNĐ).
> - `BUY`: Linh kiện bắt buộc phải mua mới theo variant dự kiến cho V1.
> - `OPTIONAL`: Linh kiện mở rộng / điểm đo kiểm phụ, không bắt buộc cho hoạt động cốt lõi V1.
> - `DNP` (Do Not Populate) / `REMOVED`: Linh kiện không lắp hoặc đã loại bỏ khỏi thiết kế V1.

---

## 1. Bảng Xung Đột Footprint KiCad Chưa Xử Lý (KiCad Footprint Mismatch Table)

> [!WARNING]
> **KICAD_FOOTPRINT_MISMATCH / NEEDS_DECISION**:
> Các sai lệch sau giữa Schematic/Netlist KiCad hiện hành (`hardware/air_mouse.kicad_sch`, `hardware/air_mouse.xml`) và danh mục BOM vật lý **bắt buộc phải được giải quyết trước khi chuyển sang giai đoạn layout PCB**. Theo quy chuẩn an toàn, **không được sửa file KiCad trong tác vụ tài liệu này**.

| Ký hiệu linh kiện | Footprint hiện hành trong KiCad Schematic / Netlist | Variant thực tế trên BOM & Phần cứng dự kiến | Bản chất xung đột kỹ thuật | Trạng thái hiện tại | Hướng xử lý ở vòng Layout PCB |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **U1** | `Connector_PinSocket_2.54mm:PinSocket_2x19_P2.54mm_Vertical` | 2 hàng Female Header $1 \times 19$ chân thẳng $2.54\,\text{mm}$ cách nhau $25.4\,\text{mm}$ (hoặc $22.86\,\text{mm}$) | Footprint KiCad hiện là socket đôi $2 \times 19$ liền khối bước $2.54\,\text{mm}$ (row pitch $2.54\,\text{mm}$), **không đại diện đúng** hai hàng socket cái $1 \times 19$ đặt cách nhau $\approx 25.4\,\text{mm}$ của bo ESP32 DevKit 38 chân. | `KICAD_FOOTPRINT_MISMATCH / NEEDS_DECISION` | Thay thế bằng cụm 2 footprint `PinSocket_1x19_P2.54mm_Vertical` đặt song song, khóa khoảng cách sau khi đo thước kẹp trên bo thật. |
| **SW2, SW3, SW4** | `Button_Switch_THT:SW_PUSH_6mm` | Nút nhấn xúc giác Tactile Switch $12 \times 12\,\text{mm}$ (Model TC-1212T-7.3) | Footprint KiCad hiện là nút mini $6 \times 6\,\text{mm}$, trong khi BOM và bố cục cơ khí chọn loại $12 \times 12\,\text{mm}$ để lắp vừa nắp chụp Button Cap $\varnothing 12.0\,\text{mm}$. Bước chân thực tế là $5.0 \times 12.5\,\text{mm}$. | `KICAD_FOOTPRINT_MISMATCH / NEEDS_DECISION` | Thay đổi footprint trong KiCad sang `Button_Switch_THT:SW_PUSH_12mm` để khớp kích thước chân cắm $12 \times 12\,\text{mm}$. |
| **U3, U4, C3, C4** | `BSS138, SOT-223 (AMS1117-1.8V), C_1V8` | Đã loại bỏ hoàn toàn khỏi BOM vật lý V1 | KiCad cũ vẫn chứa U3 (BSS138), U4 (LDO 1.8V) và các tụ C3, C4. | `RESOLVED_BY_REMOVAL / PENDING_KICAD_SYNC` | Xóa các linh kiện này trên KiCad Schematic thông qua KiCad MCP Server ở pha cập nhật EDA kế tiếp. |

---

## 2. Bảng Đối Chiếu Toàn Diện Linh Kiện (Inventory Reconciliation Table)

| Reference (Schematic / BOM) | Tên linh kiện / Module | Số lượng | Có trong BOM cũ | Trạng thái cuối | Hành động | Ghi chú đồng bộ & Rà soát kỹ thuật |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **U1** | Bo vi điều khiển ESP32 DevKit 38-Pin | 1 | Có | `OWNED` | `UPDATE` | Đã có sẵn bo mạch. Cắm 2 hàng female header 1x19 pitch 2.54mm. Row pitch cần đo thước kẹp trên bo thật. |
| **U2** | Module cảm biến 9-DOF WCMCU-20948 | 1 | Có | `OWNED` | `UPDATE` | Đã có sẵn module. Cấp nguồn trực tiếp 3.3V từ ESP32 (`DIRECT_3V3_FUNCTIONAL_CONFIRMED`). Hai trở 10k onboard kéo bus I2C. |
| **U3** ↔ `U_SHIFTER` | Module chuyển mức logic I2C BSS138 | 0 | Có (`U3`) | `REMOVED` | `REMOVE` | **Đã loại bỏ khỏi BOM V1**. Module WCMCU-20948 nối trực tiếp GPIO21/22 ở 3.3V qua kết quả thực nghiệm Bring-up. |
| **U4** ↔ `U_REG18` | Module / IC hạ áp LDO AMS1117-1.8V | 0 | Có (`U4`) | `REMOVED` | `REMOVE` | **Đã loại bỏ khỏi BOM V1**. Không cần rail nguồn 1.8V riêng biệt. |
| **MOD1** | Module sạc & bảo vệ pin TP4056 Type-C | 1 | Có | `BUY` | `KEEP` | Tích hợp cổng Type-C và IC bảo vệ DW01A + FS8205A. Đặt sát mép bo. |
| **MOD2** | Module tăng áp DC-DC Boost MT3608 5V | 1 | Có | `BUY` | `KEEP` | Nâng điện áp pin ($3.0\text{--}4.2\,\text{V}$) lên ổn định $5.0\,\text{V}$ cấp cho chân VIN của ESP32 DevKit. |
| **BAT1** | Pin LiPo 1S 3.7V 1000mAh (Model 523450) | 1 | Có | `BUY` | `KEEP` | Đặt tại mặt đáy (BOTTOM), khu vực Battery Keepout. Có PCM bảo vệ. Kèm đệm 3 lớp Kapton + Foam EVA. |
| **J1** ↔ `J_BAT` | Cọc cắm nguồn pin JST-PH 2.0mm 2-pin | 1 | Có | `BUY` | `UPDATE` | Ngàm khóa chống ngược cực pin. Chân 1: VBAT (Đỏ), Chân 2: GND (Đen). |
| **SW1** | Công tắc nguồn trượt chính SPDT SS12D00 | 1 | Có | `BUY` | `KEEP` | Đặt tại mép bo mạch. Ngắt đường dương giữa `OUT+` của TP4056 và `VIN+` của MT3608. |
| **SW2** ↔ `SW_L` | Nút nhấn xúc giác Chuột Trái (12x12mm) | 1 | Có | `BUY` | `UPDATE` | Nối `GPIO25` (Active-Low). Lắp Button Cap Ø12mm. |
| **SW3** ↔ `SW_R` | Nút nhấn xúc giác Chuột Phải (12x12mm) | 1 | Có | `BUY` | `UPDATE` | Nối `GPIO26` (Active-Low). Lắp Button Cap Ø12mm. |
| **SW4** ↔ `SW_M` | Nút nhấn Bật/Tắt chuột bay (12x12mm) | 1 | Có | `BUY` | `UPDATE` | Nối `GPIO27` (Active-Low, RTC GPIO). Lắp Button Cap Ø12mm. |
| **CAP_L, CAP_R, CAP_M** | Nắp chụp nút bấm tròn $\varnothing 12\,\text{mm}$ | 3 | Có | `BUY` | `KEEP` | Phụ kiện cơ khí gắn lên 3 nút bấm 12x12. Khe hở mép cap $\ge 3.3\,\text{mm}$. |
| **D1** | Đèn LED báo trạng thái 3mm Xanh lá | 1 | Có | `BUY` | `UPDATE` | LED Xanh lá (Green), $V_f \approx 2.0\text{--}2.2\,\text{V}$, dòng $\approx 1.2\,\text{mA}$ với trở $1.0\,\text{k}\Omega$. Điều khiển từ `GPIO32`. |
| **R1** ↔ `R_LED` | Điện trở hạn dòng LED 1kΩ 1/4W 1% THT | 1 | Có | `BUY` | `UPDATE` | Nối giữa `GPIO32` và Anode LED D1. |
| **R2** ↔ `R_BAT1` | Điện trở cầu phân áp trên 100kΩ 1/4W 1% | 1 | Có | `BUY` | `UPDATE` | Nối từ `V_SYS` (sau công tắc) xuống chân `BAT_SENSE`. |
| **R3** ↔ `R_BAT2` | Điện trở cầu phân áp dưới 100kΩ 1/4W 1% | 1 | Có | `BUY` | `UPDATE` | Nối từ `BAT_SENSE` xuống `GND`. Tạo tỉ lệ chia áp $1:1$. |
| **C1** ↔ `C_BAT` | Tụ gốm 100nF 50V THT lọc ADC đo pin | 1 | Có | `BUY` | `UPDATE` | Mắc song song R3 xuống GND để lọc nhiễu ADC ($f_c \approx 31.8\,\text{Hz}$). |
| **C2** ↔ `C_5V` / `C_IN` | Tụ hóa nhôm 10µF 25V THT ổn định 5V | 1 | Có | `BUY` | `UPDATE` | Lọc nguồn $5.0\,\text{V}$ ngõ ra MT3608 trước khi cấp vào chân VIN của ESP32. |
| **C3** ↔ `C_1V8_BULK` | Tụ hóa nhôm 10µF ổn định 1.8V | 0 | Có | `REMOVED` | `REMOVE` | **Đã loại bỏ khỏi BOM V1** do không còn dùng LDO 1.8V. |
| **C4** ↔ `C_1V8_BYPASS` | Tụ gốm 100nF bypass 1.8V | 0 | Có | `REMOVED` | `REMOVE` | **Đã loại bỏ khỏi BOM V1** do không còn dùng LDO 1.8V. |
| **J2** ↔ `J_I2C` | Header đực 1x4 chân thẳng P2.54mm mở rộng | 1 | Có | `BUY` | `UPDATE` | 4 chân: `3V3, GND, SDA, SCL` mở rộng module I2C ngoài. |
| **J_ESP_L, J_ESP_R** | 2 hàng Female Header 1x19 P2.54mm | 2 | Có | `BUY` | `KEEP` | 2 rào cái cắm bo ESP32 DevKit 38 chân. Không hàn chết chip. |
| **J_IMU** | 1 hàng Female Header 1x10 P2.54mm | 1 | Có | `BUY` | `KEEP` | 1 rào cái cắm module WCMCU-20948 10 chân. |
| **TP1–TP4** | Cụm 4 Test Point I2C & Tín hiệu cốt lõi | 1 dải (4 chân) | Thay cụm TP1–7 | `BUY` | `UPDATE` | **4 Test Point cốt lõi**: `SCL, SDA, 3V3, GND`. Dùng 1 dải header đực 1x4 P2.54mm cắm que đo Logic Analyzer. |
| **TP8–TP11** | Cụm 4 Test Point kiểm tra đường nguồn | 4 pad | Có | `OPTIONAL` | `KEEP` | **4 Test Point tùy chọn đo nguồn**: `TP_VBAT, TP_VSYS, TP_5V, TP_3V3`. Thiết kế pad đồng $\varnothing 1.5\text{--}2.0\,\text{mm}$ trên PCB (0 VNĐ). |
| **INS1** | Vật liệu cách điện & đệm pin LiPo | 1 bộ | Có | `BUY` | `KEEP` | Băng dính Kapton + Mút xốp EVA/PE dày 1.5mm đảm bảo an toàn pin LiPo. |

---

## 3. Bảng Chi Tiết Định Danh Linh Kiện BOM V1

### Nhóm 1: Linh kiện đã có sẵn (`OWNED` — Chi phí mua thêm: 0 VNĐ)

| Ref / Group | Tên linh kiện / Module | Variant chính thức | SL | Trạng thái mua hàng | Thông số kỹ thuật bắt buộc | Footprint | Đơn giá tham chiếu | Thành tiền (VNĐ) |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| **U1** | Bo vi điều khiển ESP32 Classic | **ESP32 DevKit V1 38-Pin** | 1 | `OWNED` | SoC ESP32-D0WD-V3, 240MHz, 520KB SRAM, BLE v4.2. $V_{in} = 5\,\text{V}$ (VIN), $V_{logic} = 3.3\,\text{V}$. | 2 hàng 19 chân pitch $2.54\,\text{mm}$. | 90.000đ | **0đ** *(Đã có)* |
| **U2** | Module cảm biến IMU 9-DOF | **WCMCU-20948 (10-pin)** | 1 | `OWNED` | Cảm biến 3-axis Accel + 3-axis Gyro + AK09916 Mag. Chạy trực tiếp $3.3\,\text{V}$ (`DIRECT_3V3_FUNCTIONAL_CONFIRMED`), I2C Fast-Mode $\le 400\,\text{kHz}$. Trở kéo onboard $10\,\text{k}\Omega$ trên SDA/SCL. | $26.7 \times 15.3\,\text{mm}$, 1 hàng 10 chân pitch $2.54\,\text{mm}$. | 140.000đ | **0đ** *(Đã có)* |

---

### Nhóm 2: Linh kiện điện cốt lõi bắt buộc mua (`BUY — Core Electrical Components`)

| Ref / Group | Tên linh kiện / Module | Variant dự kiến | SL | Trạng thái | Thông số kỹ thuật | Footprint | Đơn giá tham chiếu | Thành tiền (VNĐ) |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| **MOD1** | Module sạc & bảo vệ pin LiPo Type-C | **TP4056 Type-C with Protection** | 1 | `BUY` | $V_{in} = 5\,\text{V}$ (Type-C), ngắt $4.2\,\text{V}$, $I_{chg} = 1\,\text{A}$, ngắt xả $2.5\,\text{V}$, bảo vệ quá dòng $3\,\text{A}$. | $26.0 \times 17.0\,\text{mm}$. 4 pad: `B+, B-, OUT+, OUT-`. | 12.000đ | **12.000đ** |
| **MOD2** | Module tăng áp DC-DC Boost 5V | **MT3608 2A Step-Up Module** | 1 | `BUY` | $V_{in} = 2.0\text{--}24\,\text{V}$, $V_{out} = 5.0\,\text{V} \pm 2\%$, dòng cực đại $2\,\text{A}$, tần số $1.2\,\text{MHz}$. | $36.0 \times 17.0\,\text{mm}$. 4 pad: `VIN+, VIN-, VOUT+, VOUT-`. | 15.000đ | **15.000đ** |
| **BAT1** | Pin sạc LiPo 1S dẹt (Pouch) | **LiPo 1S 3.7V 1000mAh Model 523450** | 1 | `BUY` | $V_{nom} = 3.7\,\text{V}$, sạc đầy $4.2\,\text{V}$, cắt xả $3.0\,\text{V}$, dung lượng $1000\,\text{mAh}$, có mạch PCM tích hợp. | $50.0 \times 34.0 \times 5.2\,\text{mm}$, đầu cắm JST-PH 2.0. | 65.000đ | **65.000đ** |
| **J1** (`J_BAT`) | Cọc cắm nguồn pin LiPo | **JST-PH 2.0mm 2-pin THT** | 1 | `BUY` | Bước chân $2.0\,\text{mm}$, dòng định mức $2\,\text{A}$, có ngàm khóa chống ngược cực. | $6.0 \times 5.0\,\text{mm}$, 2 chân THT (`JST_PH_B2B-PH-K`). | 2.500đ | **2.500đ** |
| **SW1** | Công tắc nguồn trượt chính | **Slide Switch SPDT SS12D00** | 1 | `BUY` | $0.5\,\text{A}$ $50\,\text{V DC}$, 1 cực 2 vị trí (1P2T), 3 chân THT pitch $2.54\,\text{mm}$. | Thân $8.5 \times 4.0\,\text{mm}$, cần gạt cao $4\text{--}5\,\text{mm}$. | 3.000đ | **3.000đ** |
| **SW2** (`SW_L`) | Nút nhấn xúc giác Chuột Trái | **Tactile Switch 12x12x7.3mm (TC-1212T)** | 1 | `BUY` | Tiếp điểm thường mở (SPST-NO), $12\,\text{V DC}$ $50\,\text{mA}$, lực nhấn $160\text{--}250\,\text{gf}$. | Thân $12 \times 12\,\text{mm}$, 4 chân THT pitch $5.0 \times 12.5\,\text{mm}$. | 3.000đ | **3.000đ** |
| **SW3** (`SW_R`) | Nút nhấn xúc giác Chuột Phải | **Tactile Switch 12x12x7.3mm (TC-1212T)** | 1 | `BUY` | Tiếp điểm thường mở (SPST-NO), $12\,\text{V DC}$ $50\,\text{mA}$, lực nhấn $160\text{--}250\,\text{gf}$. | Thân $12 \times 12\,\text{mm}$, 4 chân THT pitch $5.0 \times 12.5\,\text{mm}$. | 3.000đ | **3.000đ** |
| **SW4** (`SW_M`) | Nút nhấn Bật/Tắt chuột bay | **Tactile Switch 12x12x7.3mm (TC-1212T)** | 1 | `BUY` | Tiếp điểm thường mở (SPST-NO), $12\,\text{V DC}$ $50\,\text{mA}$, lực nhấn $160\text{--}250\,\text{gf}$. | Thân $12 \times 12\,\text{mm}$, 4 chân THT pitch $5.0 \times 12.5\,\text{mm}$. | 3.000đ | **3.000đ** |
| **D1** | Đèn LED báo trạng thái | **LED 3mm tròn khuếch tán Xanh lá** | 1 | `BUY` | $V_f \approx 2.0\text{--}2.2\,\text{V}$, dòng định mức $2\text{--}5\,\text{mA}$, bước chân $2.54\,\text{mm}$. | $\varnothing 3.0\,\text{mm}$, chân cắm thẳng THT (`LED_D3.0mm`). | 1.000đ | **1.000đ** |
| **R1** (`R_LED`) | Điện trở hạn dòng LED | **Điện trở màng kim loại 1kΩ 1/4W 1% THT** | 1 | `BUY` | Trở kháng $1.0\,\text{k}\Omega$, công suất $0.25\,\text{W}$, sai số $1\%$. Dòng LED $\approx 1.2\,\text{mA}$. | Trục axial $6.0 \times 2.3\,\text{mm}$, uốn $10.16\,\text{mm}$. | 500đ | **500đ** |
| **R2** (`R_BAT1`) | Điện trở cầu phân áp trên | **Điện trở màng kim loại 100kΩ 1/4W 1% THT** | 1 | `BUY` | Trở kháng $100\,\text{k}\Omega$, sai số $1\%$, công suất $0.25\,\text{W}$. Nối sau công tắc `V_SYS`. | Trục axial $6.0 \times 2.3\,\text{mm}$, uốn $10.16\,\text{mm}$. | 500đ | **500đ** |
| **R3** (`R_BAT2`) | Điện trở cầu phân áp dưới | **Điện trở màng kim loại 100kΩ 1/4W 1% THT** | 1 | `BUY` | Trở kháng $100\,\text{k}\Omega$, sai số $1\%$, công suất $0.25\,\text{W}$. Nối mass `GND`. | Trục axial $6.0 \times 2.3\,\text{mm}$, uốn $10.16\,\text{mm}$. | 500đ | **500đ** |
| **C1** (`C_BAT`) | Tụ lọc chống nhiễu ADC đo pin | **Tụ gốm nhiều lớp 100nF 50V THT** | 1 | `BUY` | Điện dung $100\,\text{nF}$, điện áp $50\,\text{V}$, lọc thông thấp $f_c \approx 31.8\,\text{Hz}$. | Bước chân $2.54\,\text{mm}$ (`C_Disc_D5.0mm_P2.50mm`). | 500đ | **500đ** |
| **C2** (`C_5V`) | Tụ ổn định đường nguồn 5V | **Tụ hóa nhôm 10µF 25V THT** | 1 | `BUY` | Điện dung $10\,\mu\text{F}$, điện áp $25\,\text{V}$, ESR thấp, lọc ngõ ra 5V MT3608. | $\varnothing 5.0 \times 11.0\,\text{mm}$, bước chân $2.0\,\text{mm}$. | 1.000đ | **1.000đ** |
| **J2** (`J_I2C`) | Cổng mở rộng ngoại vi I2C 3.3V | **Male Pin Header 1x4 chân thẳng P2.54mm** | 1 | `BUY` | 4 chân thẳng: `3V3, GND, SDA, SCL`, dòng định mức $3\,\text{A}$. | Dài $10.16\,\text{mm}$, pitch $2.54\,\text{mm}$. | 1.000đ | **1.000đ** |

---

### Nhóm 3: Đầu nối & Socket cắm module (`BUY — Sockets & Connectors`)

| Ref / Group | Tên linh kiện / Module | Variant chính thức | SL | Trạng thái | Thông số kỹ thuật | Footprint | Đơn giá | Thành tiền |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| **J_ESP_L, J_ESP_R** | Socket cắm module ESP32 DevKit | **Female Header 1x19 chân thẳng P2.54mm** | 2 | `BUY` | 2 rào cái 1x19 chân thẳng, dòng $3\,\text{A}$, điện trở tiếp xúc $< 20\,\text{m}\Omega$. | Dài $48.7\,\text{mm}$, cao $8.5\,\text{mm}$. | 3.500đ | **7.000đ** *(2 cái)* |
| **J_IMU** | Socket cắm module WCMCU-20948 | **Female Header 1x10 chân thẳng P2.54mm** | 1 | `BUY` | 1 rào cái 1x10 chân thẳng, bước chân $2.54\,\text{mm}$, dòng tải $3\,\text{A}$. | Dài $25.9\,\text{mm}$, cao $8.5\,\text{mm}$. | 2.500đ | **2.500đ** |

---

### Nhóm 4: Test Points đo kiểm (`Test Points`)

| Ref / Group | Tên điểm đo / Tín hiệu kết nối | Dạng phần cứng | SL | Trạng thái | Vai trò chức năng & Tín hiệu | Footprint | Đơn giá | Thành tiền |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| **TP1–TP4** | **Cụm 4 Test Point I2C & Tín hiệu cốt lõi** | **Male Pin Header 1x4 chân thẳng P2.54mm** | 1 dải | `BUY` | **4 điểm đo cốt lõi**: `SCL` (GPIO22), `SDA` (GPIO21), `3V3` (VCC), `GND` (Mass). Cắm kẹp que Logic Analyzer. | Header 1x04 P2.54mm (hoặc 4 pad đồng $\varnothing 2.0\,\text{mm}$) | 1.000đ | **1.000đ** |
| **TP8–TP11** | **Cụm 4 Test Point đo nguồn hệ thống** | **Pad đồng tròn $\varnothing 1.5\text{--}2.0\,\text{mm}$ trên PCB** | 4 pad | `OPTIONAL` | **4 điểm đo nguồn**: `TP_VBAT, TP_VSYS, TP_5V, TP_3V3`. Phục vụ kiểm tra VOM trước khi đóng tải. | Pad đồng hàn PCB | 0đ | **0đ** *(PCB pad)* |

---

### Nhóm 5: Phụ kiện cơ khí & Vật liệu an toàn pin (`BUY — Mechanical & Safety`)

| Ref / Group | Tên phụ kiện / Vật liệu | Variant chính thức | SL | Trạng thái | Thông số kỹ thuật | Kích thước | Đơn giá | Thành tiền |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: |
| **CAP_L, CAP_R, CAP_M** | Nắp chụp nút bấm tròn (Button Cap) | **Button Cap tròn $\varnothing 12.0\,\text{mm}$ cho nút 12x12** | 3 | `BUY` | Nhựa ABS đúc, ngàm tròn ôm khít trụ nhấn $\varnothing 3.8\,\text{mm}$. | $\varnothing 12.0\,\text{mm}$, cao $5.7\,\text{mm}$. | 2.000đ | **6.000đ** *(3 cái)* |
| **INS1** | Vật liệu cách điện & đệm pin LiPo | **Băng keo Kapton chịu nhiệt + Mút xốp EVA dày 1.5mm** | 1 bộ | `BUY` | Màng Polyimide chịu nhiệt $> 200^\circ\text{C}$, cách điện $> 5\,\text{kV}$. Mút EVA đàn hồi giảm chấn. | Tấm cắt lót $\approx 54.0 \times 36.0\,\text{mm}$. | 25.000đ | **25.000đ** |

---

### Nhóm 6: Linh kiện loại bỏ (`REMOVED / DNP`)

| Ký hiệu | Tên linh kiện / Module | Lý do loại bỏ khỏi BOM V1 | Quyết định kỹ thuật |
| :--- | :--- | :--- | :--- |
| **U3** (`U_SHIFTER`) | Module chuyển mức I2C BSS138 | **Đã loại bỏ**. Module WCMCU-20948 đã xác minh thực nghiệm hoạt động trực tiếp 3.3V với ESP32. | `DIRECT_3V3_CONFIRMED` |
| **U4** (`U_REG18`) | IC / Module hạ áp LDO 1.8V AMS1117-1.8V | **Đã loại bỏ**. Toàn bộ hệ thống dùng chung rail 3.3V, không cần rail 1.8V phụ. | `DIRECT_3V3_CONFIRMED` |
| **C3** (`C_1V8_BULK`) | Tụ hóa nhôm 10µF ổn định 1.8V | **Đã loại bỏ** do loại bỏ LDO 1.8V. | `DIRECT_3V3_CONFIRMED` |
| **C4** (`C_1V8_BYPASS`)| Tụ gốm 100nF dập nhiễu 1.8V | **Đã loại bỏ** do loại bỏ LDO 1.8V. | `DIRECT_3V3_CONFIRMED` |
| **TXB0104** | IC chuyển mức logic SPI tốc độ cao | Đã loại bỏ. Kiến trúc chuyển sang I2C Fast-Mode. | `PROJECT DECISION` |
| **AK09916 rời** | Module từ kế rời ngoài | Không dùng. Từ kế AK09916 đã tích hợp sẵn bên trong ICM-20948. | `PROJECT DECISION` |

---

## 4. Tổng Kết Dự Toán Chi Phí & Bảng Kiểm Toán Số Lượng (BOM Audit Table)

### 4.1 Kiểm toán số lượng linh kiện cần mua (Component Count Audit)
- **`BUY_PHYSICAL_UNITS: 23` (23 đơn vị vật lý cần mua mới)**:
  - 15 linh kiện điện hoạt động: `MOD1, MOD2, BAT1, J1, SW1, SW2, SW3, SW4, D1, R1, R2, R3, C1, C2, J2` (15 đơn vị)
  - 3 socket cắm module: `J_ESP_L, J_ESP_R` (2 cái), `J_IMU` (1 cái) (3 đơn vị)
  - 1 dải pin header đực 1x4 làm test points: `TP1–TP4` (1 đơn vị)
  - 3 nắp chụp nút bấm tròn: `CAP_L, CAP_R, CAP_M` (3 đơn vị)
  - 1 bộ vật liệu lót cách ly an toàn pin: `INS1` (1 đơn vị)
  - *Tổng cộng*: $15 + 3 + 1 + 3 + 1 = 23\,\text{đơn vị vật lý}$.
- **`BUY_BOM_LINES: 20` (20 dòng mua hàng sau khi loại bỏ 4 dòng cũ U3, U4, C3, C4)**:
  - Nhóm 2 (Linh kiện điện cốt lõi): 15 dòng
  - Nhóm 3 (Socket cắm module): 2 dòng (`J_ESP_L, J_ESP_R` gộp 1 dòng SL 2; `J_IMU` 1 dòng SL 1)
  - Nhóm 4 (Test points cốt lõi): 1 dòng (`TP1–TP4` 1 dòng SL 1 dải 1x4)
  - Nhóm 5 (Phụ kiện cơ khí & an toàn): 2 dòng (`CAP_L..M` gộp 1 dòng SL 3; `INS1` 1 dòng SL 1 bộ)
  - *Tổng cộng*: $15 + 2 + 1 + 2 = 20\,\text{dòng mua hàng}$.

### 4.2 Bảng phân tích chi phí theo nhóm danh mục (Cost Recalculation Table)

| Phân nhóm danh mục linh kiện | Trạng thái mua sắm | Số lượng vật phẩm | Chi tiết các dòng cấu thành | Giá trị / Thành tiền (VNĐ) | Tỉ trọng (%) |
| :--- | :---: | :---: | :--- | :---: | :---: |
| **Linh kiện cốt lõi đã có sẵn** | `OWNED` | 2 linh kiện | `U1` (90.000đ) + `U2` (140.000đ) | 230.000 VNĐ | 0.00% *(Không chi)* |
| **Khối Nguồn & Sạc Pin** | `BUY` | 5 vật phẩm | BAT1 (65.000) + MOD2 (15.000) + MOD1 (12.000) + SW1 (3.000) + J1 (2.500) | 97.500 VNĐ | 63.73% |
| **Khối Phím Bấm & Chỉ Thị Trạng Thái** | `BUY` | 6 vật phẩm | 3 switch SW2-SW4 (9.000) + LED D1 (1.000) + Trở R1 (500) + Cổng J2 (1.000) | 11.500 VNĐ | 7.52% |
| **Khối Thụ Động Đo Pin & Lọc Nguồn 5V** | `BUY` | 4 vật phẩm | 2 trở R2-R3 (1.000) + Tụ C1 (500) + Tụ C2 (1.000) | 2.500 VNĐ | 1.63% |
| **Khối Socket Cắm Module** | `BUY` | 3 vật phẩm | 2 socket ESP32 1x19 (7.000) + 1 socket IMU 1x10 (2.500) | 9.500 VNĐ | 6.21% |
| **Khối Test Points Cốt Lõi (1x4 Header)**| `BUY` | 1 vật phẩm | 1 dải header đực 1x4 `TP1–TP4` (SCL, SDA, 3V3, GND) | 1.000 VNĐ | 0.65% |
| **Khối Phụ Kiện Cơ Khí & An Toàn Pin** | `BUY` | 4 vật phẩm | 3 Button Cap tròn 12mm (6.000) + 1 Bộ cách điện Kapton & EVA (25.000) | 31.000 VNĐ | 20.26% |
| **Khối Test Points Đo Nguồn Mở Rộng** | `OPTIONAL` | 4 pad đồng | TP8 (VBAT) + TP9 (VSYS) + TP10 (5V) + TP11 (3V3) | 0 VNĐ | 0.00% |
| **TỔNG CHI PHÍ DỰ TOÁN MUA MỚI** | **`BUY`** | **23 vật phẩm (20 dòng)** | **97.500 + 11.500 + 2.500 + 9.500 + 1.000 + 31.000** | **153.000 VNĐ** | **100.00%** |

### 4.3 Kiểm toán từng dòng linh kiện mua mới (Line-by-Line Math Verification)
$$\text{TOTAL\_BUY} = 12.000 + 15.000 + 65.000 + 2.500 + 3.000 + 9.000 + 1.000 + 500 + 500 + 500 + 500 + 1.000 + 1.000 + 7.000 + 2.500 + 1.000 + 6.000 + 25.000 = 153.000\,\text{VNĐ}$$

- **Chi tiết các khoản giảm trừ khi chuyển sang Direct 3.3V (loại bỏ BSS138 & LDO 1.8V)**:
  - Chi phí giảm trừ:
    - Loại bỏ U3 (BSS138): $-10.000\,\text{VNĐ}$
    - Loại bỏ U4 (LDO 1.8V): $-8.000\,\text{VNĐ}$
    - Loại bỏ C3 (Tụ hóa 10µF 1.8V): $-1.000\,\text{VNĐ}$
    - Loại bỏ C4 (Tụ gốm 100nF 1.8V): $-500\,\text{VNĐ}$
    - Điều chỉnh cụm Test Points từ 1x7 xuống 1x4: $-500\,\text{VNĐ}$
  - Tổng giảm trừ: $10.000 + 8.000 + 1.000 + 500 + 500 = 20.000\,\text{VNĐ}$.
  - Dự toán mua mới cuối cùng: $153.000\,\text{VNĐ}$ (23 vật phẩm, 20 dòng mua hàng).
- *(Ghi chú kiểm toán tùy chọn)*: Nếu cụm Test Points đo kiểm sử dụng trực tiếp pad đồng trên mạch in (0 VNĐ), chi phí mua mới sẽ là $152.000\,\text{VNĐ}$ (22 đơn vị vật lý, 19 dòng mua hàng). Dự án chọn phương án 1x4 header ($153.000\,\text{VNĐ}$) để tạo cọc cắm que đo Logic Analyzer chắc chắn trong phòng thí nghiệm.