# BẢNG ĐẶC TẢ LINH KIỆN SƠ ĐỒ NGUYÊN LÝ V1 (SCHEMATIC COMPONENT LIST)

> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems) — Mốc Báo cáo Giữa kỳ Tuần 5  
> **Tài liệu**: Đặc tả Toàn diện Danh mục Linh kiện cho Thiết kế Sơ đồ Nguyên lý (Schematic Specification)  
> **Phiên bản**: V2.0.0 — Direct 3.3V Reconciled & Audited Schematic Spec  
> **Trạng thái phê duyệt BOM**: `PROVISIONAL_PROCUREMENT_LIST` (Danh mục mua sắm tạm thời — Chưa đạt trạng thái sẵn sàng mua sắm)  
> **Kiến trúc phần cứng**: `DIRECT_3V3_FUNCTIONAL_CONFIRMED` (Loại bỏ BSS138 và LDO 1.8V sau Hardware Bring-up)  
> **Trạng thái đồng bộ KiCad**: `KICAD_SYNC_STATUS: STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE` (KiCad schematic `hardware/air_mouse.kicad_sch` vẫn giữ BSS138 và LDO 1.8V lịch sử, chờ cập nhật qua KiCad MCP Server)  
> **WCMCU Mechanical Blocker**: `RESOLVED` (Kích thước module $26.7 \times 15.3\,\text{mm}$, pitch $2.54\,\text{mm}$)  
> **Trạng thái giá**: `REFERENCE_PRICE / NEEDS_RECHECK` (Toàn bộ đơn giá là giá tham chiếu lịch sử, cần kiểm tra lại trước khi giải ngân)  
>
> **Quy ước nguồn chân lý (Source of Truth Hierarchy)**:
> 1. `docs/HARDWARE_BRINGUP_DIRECT_3V3_2026-09-25.md` (Báo cáo Bring-up thực tế)
> 2. `docs/AIR_MOUSE_HARDWARE_ARCHITECTURE.md` (Kiến trúc phần cứng V4.0.0)
> 3. `docs/BOM_V1.md` (BOM V2.0.0: 23 units, 20 lines, 153.000 VNĐ)
> 4. `docs/schematic/SCHEMATIC_COMPONENT_LIST.md`
> 5. Thiết kế Schematic hiện hành (`hardware/air_mouse.kicad_sch` — `STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE`)
>
> **Mục tiêu sử dụng**: Cung cấp toàn bộ thông số, ký hiệu linh kiện (Ref Des), mã linh kiện thực tế, chân tín hiệu sử dụng, miền điện áp và đối chiếu footprint để kỹ sư thiết kế hoàn thiện sơ đồ nguyên lý và chuẩn bị layout PCB mà không cần suy đoán kết nối.

---

## 1. Bảng Xung Đột Footprint KiCad Chưa Xử Lý (KiCad Footprint Mismatch Table)

> [!WARNING]
> **KICAD_FOOTPRINT_MISMATCH / NEEDS_DECISION**:
> Các sai lệch sau giữa Schematic/Netlist KiCad hiện hành (`hardware/air_mouse.kicad_sch`, `hardware/air_mouse.xml`) và danh mục linh kiện BOM vật lý **bắt buộc phải được giải quyết trước khi chuyển sang giai đoạn layout PCB**. Theo quy chuẩn an toàn, **không được sửa file KiCad trong tác vụ tài liệu này**.

| Ký hiệu linh kiện | Footprint hiện hành trong KiCad Schematic / Netlist | Variant thực tế trên BOM & Phần cứng dự kiến | Bản chất xung đột kỹ thuật | Trạng thái hiện tại | Hướng xử lý ở vòng Layout PCB |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **U1** | `Connector_PinSocket_2.54mm:PinSocket_2x19_P2.54mm_Vertical` | 2 hàng Female Header $1 \times 19$ chân thẳng $2.54\,\text{mm}$ cách nhau $25.4\,\text{mm}$ (hoặc $22.86\,\text{mm}$) | Footprint KiCad hiện là socket đôi $2 \times 19$ liền khối bước $2.54\,\text{mm}$ (row pitch $2.54\,\text{mm}$), **không đại diện đúng** hai hàng socket cái $1 \times 19$ đặt cách nhau $\approx 25.4\,\text{mm}$ của bo ESP32 DevKit 38 chân. | `KICAD_FOOTPRINT_MISMATCH / NEEDS_DECISION` | Thay thế bằng cụm 2 footprint `PinSocket_1x19_P2.54mm_Vertical` đặt song song, khóa khoảng cách sau khi đo thước kẹp trên bo thật. |
| **SW2, SW3, SW4** | `Button_Switch_THT:SW_PUSH_6mm` | Nút nhấn xúc giác Tactile Switch $12 \times 12\,\text{mm}$ (Model TC-1212T-7.3) | Footprint KiCad hiện là nút mini $6 \times 6\,\text{mm}$, trong khi BOM và bố cục cơ khí chọn loại $12 \times 12\,\text{mm}$ để lắp vừa nắp chụp Button Cap $\varnothing 12.0\,\text{mm}$. Bước chân thực tế là $5.0 \times 12.5\,\text{mm}$. | `KICAD_FOOTPRINT_MISMATCH / NEEDS_DECISION` | Thay đổi footprint trong KiCad sang `Button_Switch_THT:SW_PUSH_12mm` để khớp kích thước chân cắm $12 \times 12\,\text{mm}$. |
| **U3, U4, C3, C4** | `BSS138, SOT-223 (AMS1117-1.8V), C_1V8` | Đã loại bỏ hoàn toàn khỏi BOM vật lý V1 | KiCad cũ vẫn chứa U3 (BSS138), U4 (LDO 1.8V) và các tụ C3, C4. | `RESOLVED_BY_REMOVAL / PENDING_KICAD_SYNC` | Xóa các linh kiện này trên KiCad Schematic thông qua KiCad MCP Server ở pha cập nhật EDA kế tiếp. |

---

## 2. Bảng Danh Mục Linh Kiện Chi Tiết Theo Khối Chức Năng

*(Để tối ưu khả năng hiển thị và chống vỡ chữ khi in ấn tài liệu, mỗi khối chức năng được trình bày thành 2 bảng liên kết chặt chẽ theo Reference: Bảng A cho Đặc tả phần cứng & Footprint; Bảng B cho Chức năng, Sơ đồ chân & Kết nối tín hiệu).*

### Khối A: Khối Vi Điều Khiển Trung Tâm (MCU Subsystem)

#### Bảng A.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **U1** | Bo mạch vi điều khiển ESP32 | **NodeMCU-32S / ESP32 DevKit V1 38-Pin** | Module bo cắm (DevKit Board) | SoC ESP32-D0WDQ6, Dual-core 240MHz, 520KB SRAM, BLE v4.2 | 2 hàng `PinSocket_1x19_P2.54mm_Vertical` (Row pitch $25.4\,\text{mm}$) | 1 |
| **J_ESP_L** | Socket cắm bên trái ESP32 | Female Header 1x19 P2.54mm | Đầu nối rào cái (Connector) | 19 chân thẳng, dòng tải định mức 3A, pitch $2.54\,\text{mm}$ | `Connector_PinSocket_2.54mm:PinSocket_1x19_P2.54mm_Vertical` | 1 |
| **J_ESP_R** | Socket cắm bên phải ESP32 | Female Header 1x19 P2.54mm | Đầu nối rào cái (Connector) | 19 chân thẳng, dòng tải định mức 3A, pitch $2.54\,\text{mm}$ | `Connector_PinSocket_2.54mm:PinSocket_1x19_P2.54mm_Vertical` | 1 |

#### Bảng A.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **U1** | Bộ xử lý trung tâm, đọc I2C cảm biến, tính toán Rate-Control, phát BLE HID | VIN: $5.0\,\text{V}$; VDD: $3.3\,\text{V}$ | Chân 1 (3V3), 5 (GPIO34 BAT_SENSE), 7 (GPIO32 LED), 9 (GPIO25 BTN_LEFT), 10 (GPIO26 BTN_RIGHT), 11 (GPIO27 BTN_MODE), 14/32/38 (GND), 19 (5V VIN), 33 (GPIO21 SDA), 36 (GPIO22 SCL) | Chân 2 (EN), 3/4/6 (GPIO36/39/35), 8 (GPIO33), 12/13 (GPIO14/12), 15 (GPIO13), 16-18/20-22 (Flash nội CẤM NỐI), 23-25 (Strapping), 26-31 (GPIO4..19), 34/35 (RX0/TX0), 37 (GPIO23) | `OWNED` (`KICAD_FOOTPRINT_MISMATCH / NEEDS_DECISION`) | Cắm qua 2 hàng socket cái 1x19. **KiCad mismatch**: Netlist hiện dùng socket đôi $2 \times 19$ liền khối, cần tách thành 2 rào $1 \times 19$ cách nhau $25.4\,\text{mm}$ (đo thực tế). |
| **J_ESP_L** | Đế cắm hàng chân trái của ESP32 DevKit (Chân 1 đến 19) | $0\text{--}5.0\,\text{V}$ | Chân 1, 5, 7, 9, 10, 11, 14, 19 | Chân 2, 3, 4, 6, 8, 12, 13, 15, 16, 17, 18 | `BUY` | Cho phép tháo lắp bo ESP32 để nạp chương trình hoặc thay thế dễ dàng. |
| **J_ESP_R** | Đế cắm hàng chân phải của ESP32 DevKit (Chân 20 đến 38) | $0\text{--}3.3\,\text{V}$ | Chân 32, 33, 36, 38 | Chân 20 đến 31, 34, 35, 37 | `BUY` | Hàng chân đối diện của socket ESP32. |

---

### Khối B: Khối Cảm Biến Chuyển Động (Motion Sensor Subsystem)

#### Bảng B.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **U2** | Module cảm biến 9-DOF IMU | **WCMCU-20948 / ICM-20948-M Breakout** | Breakout Module (10-pin) | TDK ICM-20948 (3-axis Gyro + 3-axis Accel + AK09916 Mag). Chạy trực tiếp $3.3\,\text{V}$ (`DIRECT_3V3_FUNCTIONAL_CONFIRMED`), có sẵn trở kéo $10\,\text{k}\Omega$ SDA/SCL. | `Connector_PinSocket_2.54mm:PinSocket_1x10_P2.54mm_Vertical` kèm courtyard $26.7 \times 15.3\,\text{mm}$ | 1 |
| **J_IMU** | Socket cắm module IMU | Female Header 1x10 P2.54mm | Đầu nối rào cái (Connector) | 10 chân thẳng, bước chân $2.54\,\text{mm}$, dòng tải định mức 3A | `Connector_PinSocket_2.54mm:PinSocket_1x10_P2.54mm_Vertical` | 1 |

#### Bảng B.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **U2** | Đo vận tốc góc quay cổ tay (Gyroscope) quanh 3 trục phục vụ điều khiển con trỏ chuột tương đối | $V_{DD} = 3.3\,\text{V}$ (`DIRECT_3V3_FUNCTIONAL_CONFIRMED`) | Chân 1 (VCC $3.3\,\text{V}$), 2 (GND), 3 (SCL nối GPIO22), 4 (SDA nối GPIO21), 5 (NCS nối lên $3.3\,\text{V}$), 6 (AD0 nối GND chọn 0x68), 8 (FSY nối GND) | Chân 7 (INT), Chân 9 (ACL), 10 (ADA) để hở | `OWNED` — `BENCH_VERIFIED_ON_OWNED_MODULE` | **Bring-up Pass**: Cấp nguồn trực tiếp $3.3\,\text{V}$ từ ESP32 DevKit. Chân NCS nối $3.3\,\text{V}$ khóa I2C; AD0 nối GND chọn 0x68; FSY nối GND. Đã xác minh thực tế 100/100 chu kỳ đọc WHO_AM_I = 0xEA. |
| **J_IMU** | Đế cắm nhận module cảm biến WCMCU-20948 | $0\text{--}3.3\,\text{V}$ | Chân 1, 2, 3, 4, 5, 6, 8 | Chân 7 (`INT`), 9 (`ACL`), 10 (`ADA`) | `BUY` | Bảo vệ module cảm biến khỏi nhiệt độ mỏ hàn. |

---

### Khối C: Khối Chuyển Mức Logic I2C (Logic Level Shifter Subsystem — ĐÃ LOẠI BỎ)

> [!NOTE]
> **REMOVED_IN_DIRECT_3V3_BASELINE**: Khối chuyển mức logic MOSFET BSS138 (U3) đã được loại bỏ hoàn toàn khỏi kiến trúc phần cứng và BOM vật lý sau kết quả đo đạc bring-up thực tế. Module WCMCU-20948 giao tiếp trực tiếp I2C với ESP32 ở 3.3V (400 kHz). Tệp KiCad Schematic cũ giữ ký hiệu này ở trạng thái stale chờ đồng bộ qua KiCad MCP Server.

---

### Khối D: Khối Nguồn & Sạc Pin (Power & Charging Subsystem)

#### Bảng D.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **BAT1** | Pin sạc LiPo 1S | **LiPo 1S Pouch Cell 1000mAh (Model 523450)** | Nguồn năng lượng hóa học | $V_{nom} = 3.7\,\text{V}$, nạp đầy $4.2\,\text{V}$, ngắt xả $3.0\,\text{V}$, có mạch bảo vệ PCM | Khối pin dẹt $50.0 \times 34.0 \times 5.2\,\text{mm}$ (Bottom mount) | 1 |
| **J1** (`J_BAT`) | Cọc cắm nguồn pin LiPo | **JST-PH 2.0mm 2-pin Right-Angle / Straight THT** | Đầu nối có ngàm khóa (Connector) | Bước chân $2.0\,\text{mm}$, dòng định mức 2A | `Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical` | 1 |
| **MOD1** | Module sạc & bảo vệ pin Type-C | **TP4056 Type-C with Dual Protection (DW01A + FS8205A)** | Module nạp pin tuyến tính kèm bảo vệ | Dòng sạc $1.0\,\text{A}$, ngắt sạc $4.2\,\text{V}$, bảo vệ xả cạn $2.5\,\text{V}$, quá dòng $3\,\text{A}$ | Module 4 pad góc: `B+, B-, OUT+, OUT-` + cổng Type-C nhô mép | 1 |
| **SW1** | Công tắc nguồn gạt chính | **Slide Switch SPDT SS12D00 / SS12F15 (1P2T)** | Công tắc cơ khí (Switch) | Dòng định mức $0.5\,\text{A}$ $50\,\text{V DC}$, 3 chân cắm thẳng THT, pitch $2.54\,\text{mm}$ | `Button_Switch_THT:SW_Slide_1P2T_SS12D00G4` | 1 |
| **MOD2** | Module tăng áp DC-DC Boost 5V | **MT3608 2A Step-Up Boost Module (Blue PCB)** | Module nguồn xung tăng áp (Boost Converter) | $V_{in} = 2.0\text{--}24\,\text{V}$, $V_{out} = 5.0\,\text{V} \pm 2\%$, dòng ra tối đa $2\,\text{A}$, tần số $1.2\,\text{MHz}$ | Module 4 pad góc: `VIN+, VIN-, VOUT+, VOUT-` ($36 \times 17\,\text{mm}$) | 1 |
| *(U4 cũ)* | *(IC / Module hạ áp LDO 1.8V)* | *AMS1117-1.8V* | *Đã loại bỏ (REMOVED)* | *Không cần đường nguồn 1.8V riêng trong kiến trúc trực tiếp 3.3V* | *Loại bỏ khỏi BOM V1* | 0 |

#### Bảng D.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **BAT1** | Cung cấp toàn bộ năng lượng di động cho thiết bị Air Mouse | $3.0\text{--}4.2\,\text{V}$ | Cực dương ($+$): Dây đỏ nối `J1` chân 1; Cực âm ($-$): Dây đen nối `J1` chân 2 | Không có | `BUY` — `PROJECT DECISION` | Bố trí mặt đáy (Bottom), cách ly bằng đệm Kapton + Foam 1.5mm. |
| **J1** (`J_BAT`) | Kết nối an toàn có khóa chống cắm ngược cực pin LiPo | $3.0\text{--}4.2\,\text{V}$ | Chân 1 (VBAT nối pad B+ TP4056); Chân 2 (`GND_BAT_CELL` nối pad B- TP4056, không nối GND hệ thống) | Không có | `BUY` — `VERIFIED` | Ngàm khóa định hướng: Chân 1 nối dây đỏ ($V_{\text{BAT}}$), Chân 2 nối dây đen (cực âm cell). |
| **MOD1** | Quản lý sạc pin LiPo qua cổng Type-C và bảo vệ ngắn mạch/quá xả cho cell pin | Vào: $5.0\,\text{V}$ USB; Ra: $3.0\text{--}4.2\,\text{V}$ | Pad 1 (B+), Pad 2 (B-), Pad 3 (OUT+ nối V_SW_IN), Pad 4 (OUT- nối GND) | Không có | `BUY` — `PROJECT DECISION` | Module hoàn chỉnh gồm 4 pad hàn. Pad OUT+ là nguồn dương có bảo vệ xả cạn, đưa vào công tắc SW1. |
| **SW1** | Bật/Tắt toàn bộ nguồn cấp cho mạch nâng áp và vi điều khiển | $3.0\text{--}4.2\,\text{V}$ | Chân 1 (V_SW_IN nhận từ OUT+ TP4056); Chân 2 (Common: V_SYS cấp cho MT3608 và cầu đo pin) | Chân 3 để hở (`NC`) | `BUY` — `VERIFIED` | Ngắt toàn bộ tải khỏi pin khi tắt nguồn, cho phép sạc pin an toàn mà không bị nhiễu tải. |
| **MOD2** | Nâng điện áp pin ($3.0\text{--}4.2\,\text{V}$) lên mức ổn định $5.0\,\text{V}$ cấp cho chân VIN của bo ESP32 | Vào: $3.0\text{--}4.2\,\text{V}$; Ra: $5.0\,\text{V}$ danh định | Pad 1 (VIN+ nối V_SYS), Pad 2 (VIN- nối GND), Pad 3 (VOUT+ nối net 5V), Pad 4 (VOUT- nối GND) | Không có | `BUY` — `PROJECT DECISION` | Đo và vi chỉnh điện áp đúng $5.0\,\text{V} \pm 0.1\,\text{V}$ trước khi cắm bo ESP32. |
| *(U4 cũ)* | *(LDO 1.8V)* | *REMOVED* | *Không sử dụng* | *Toàn bộ chân* | `REMOVED` | Đã loại bỏ khỏi BOM V1. Không cần LDO 1.8V. |

---

### Khối E: Khối Nút Bấm Người Dùng (User Push Buttons)

#### Bảng E.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **SW2** (`SW_L`) | Nút bấm chuột trái (Left Click) | **Tactile Switch 12x12x7.3mm (TC-1212T) kèm Cap $\varnothing 12\text{mm}$** | Nút nhấn cơ học thường mở (SPST-NO) | $12\,\text{V DC}$ $50\,\text{mA}$, lực bấm $160\text{--}250\,\text{gf}$, tiếp điểm mạ bạc | `Button_Switch_THT:SW_PUSH_12mm` | 1 |
| **SW3** (`SW_R`) | Nút bấm chuột phải (Right Click) | **Tactile Switch 12x12x7.3mm (TC-1212T) kèm Cap $\varnothing 12\text{mm}$** | Nút nhấn cơ học thường mở (SPST-NO) | $12\,\text{V DC}$ $50\,\text{mA}$, lực bấm $160\text{--}250\,\text{gf}$, tiếp điểm mạ bạc | `Button_Switch_THT:SW_PUSH_12mm` | 1 |
| **SW4** (`SW_M`) | Nút chuyển chế độ / Bật tắt di trỏ | **Tactile Switch 12x12x7.3mm (TC-1212T) kèm Cap $\varnothing 12\text{mm}$** | Nút nhấn cơ học thường mở (SPST-NO) | $12\,\text{V DC}$ $50\,\text{mA}$, lực bấm $160\text{--}250\,\text{gf}$, tiếp điểm mạ bạc | `Button_Switch_THT:SW_PUSH_12mm` | 1 |
| **CAP_L, CAP_R, CAP_M** | Nắp chụp nút bấm tròn | **Button Cap tròn $\varnothing 12.0\,\text{mm}$ cho nút 12x12** | Phụ kiện cơ khí | Nhựa ABS đúc, ngàm tròn ôm khít trụ nhấn $\varnothing 3.8\,\text{mm}$ | Phụ kiện cơ khí gắn ngoài | 3 |

#### Bảng E.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **SW2** (`SW_L`) | Nút Click chuột trái (Left Click) và chọn mục (OK) | $3.3\,\text{V}$ logic (Active-Low) | Chân 1: Nối `BTN_LEFT` (`GPIO25`); Chân 2: Nối mass `GND` | Không có | `BUY` — `PROVISIONAL / KICAD_MISMATCH` | **KiCad mismatch**: Netlist hiện dùng `SW_PUSH_6mm`, cần đổi sang `SW_PUSH_12mm` (bước chân $5.0 \times 12.5\,\text{mm}$). Cấu hình Active-Low, pull-up nội bộ. |
| **SW3** (`SW_R`) | Nút Click chuột phải (Right Click / Context Menu) | $3.3\,\text{V}$ logic (Active-Low) | Chân 1: Nối `BTN_RIGHT` (`GPIO26`); Chân 2: Nối mass `GND` | Không có | `BUY` — `PROVISIONAL / KICAD_MISMATCH` | **KiCad mismatch**: Tương tự SW2, cấu hình Active-Low trên `GPIO26`. Cần đổi footprint sang 12mm. |
| **SW4** (`SW_M`) | Nút Bật/Tắt tính năng chuột bay (Air Mouse Enable / Mode Toggle) | $3.3\,\text{V}$ logic (Active-Low) | Chân 1: Nối `BTN_MODE` (`GPIO27`); Chân 2: Nối mass `GND` | Không có | `BUY` — `PROVISIONAL / KICAD_MISMATCH` | **KiCad mismatch**: Cấu hình Active-Low trên `GPIO27` (RTC GPIO). Cần đổi footprint sang 12mm. |
| **CAP_L..M** | Tăng diện tích tiếp xúc ngón tay cho 3 phím bấm | Không dùng điện | Gắn trên đỉnh switch SW2, SW3, SW4 | Không có | `BUY` — `WEB_VERIFIED` | Khe hở danh định mép cap $\approx 3.3\,\text{mm}$ theo khoảng cách tim $15.3\,\text{mm}$; cần đo và thử lắp vật lý thực tế. |

---

### Khối F: Khối Chỉ Thị Trạng Thái (Status Indication Subsystem)

#### Bảng F.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **D1** | Đèn LED báo trạng thái | **LED 3mm tròn khuếch tán (Màu Xanh lá / Green)** | Diode phát quang (LED) | Điện áp thuận $V_f \approx 2.0\text{--}2.2\,\text{V}$, dòng định mức $2\text{--}5\,\text{mA}$, bước chân $2.54\,\text{mm}$ | `LED_THT:LED_D3.0mm` | 1 |
| **R1** (`R_LED`) | Điện trở hạn dòng LED | **Điện trở màng kim loại 1kΩ 1/4W 1% THT** | Điện trở cố định (Resistor) | Trở kháng $1.0\,\text{k}\Omega$, công suất $0.25\,\text{W}$, sai số $1\%$ | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | 1 |

#### Bảng F.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **D1** | Hiển thị trạng thái hệ thống: Khởi động / Hiệu chuẩn tĩnh / Chờ kết nối BLE / Đã kết nối | $0\text{--}3.3\,\text{V}$ (Active-HIGH) | Chân 1 (Cathode / K): Nối mass `GND`; Chân 2 (Anode / A): Nối net `LED_ANODE` | Không có | `BUY` — `VERIFIED` | Điều khiển từ `GPIO32` (Push-Pull ngõ ra, loại bỏ xung đột strapping boot). Dòng qua LED $\approx 1.2\,\text{mA}$ với trở $1\,\text{k}\Omega$. |
| **R1** (`R_LED`) | Giới hạn dòng điện chạy qua LED D1 ở mức an toàn và tiết kiệm pin ($\approx 1.2\,\text{mA}$) | $0\text{--}3.3\,\text{V}$ | Chân 1: Nối nhãn mạng `LED_STATUS` (`GPIO32`); Chân 2: Nối nhãn mạng `LED_ANODE` (cực Anode của LED D1) | Không có | `BUY` — `PROJECT DECISION` | Chốt giá trị $1.0\,\text{k}\Omega$ để tiết kiệm pin. Có thể thay bằng $330\text{--}470\,\Omega$ nếu cần sáng ngoài trời. |

---

### Khối G: Khối Giám Sát Điện Áp Pin (Battery Voltage Sensing)

#### Bảng G.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **R2** (`R_BAT1`) | Điện trở cầu phân áp phía trên (R_TOP) | **Điện trở màng kim loại chính xác 100kΩ 1/4W 1% THT** | Điện trở chính xác (Resistor) | Trở kháng $100\,\text{k}\Omega$, sai số $1\%$, hệ số nhiệt thấp | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | 1 |
| **R3** (`R_BAT2`) | Điện trở cầu phân áp phía dưới (R_BOT) | **Điện trở màng kim loại chính xác 100kΩ 1/4W 1% THT** | Điện trở chính xác (Resistor) | Trở kháng $100\,\text{k}\Omega$, sai số $1\%$, hệ số nhiệt thấp | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | 1 |
| **C1** (`C_BAT`) | Tụ lọc chống nhiễu ADC đo pin | **Tụ gốm nhiều lớp 100nF (0.1µF) 50V THT** | Tụ điện gốm (Capacitor) | Điện dung $100\,\text{nF}$ ($0.1\,\mu\text{F}$), điện áp định mức $50\,\text{V}$, điện môi X7R/Y5V | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm` | 1 |

#### Bảng G.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **R2** (`R_BAT1`) | Cầu phân áp phía trên, nối từ nguồn dương pin sau công tắc (`V_SYS`) xuống nút đo | $3.0\text{--}4.2\,\text{V}$ | Chân 1: Nối nguồn dương hệ thống sau công tắc `V_SYS`; Chân 2: Nối nút đo nhãn mạng `BAT_SENSE` | Không có | `BUY` — `VERIFIED` | Nối sau công tắc gạt `SW1` (`V_SYS`) để khi tắt nguồn thiết bị sẽ ngắt hoàn toàn dòng rò qua cầu phân áp ($I_{leak} \approx 21\,\mu\text{A}$). |
| **R3** (`R_BAT2`) | Cầu phân áp phía dưới, chia đôi điện áp pin đưa về dải đo an toàn của ADC ($1.5\text{--}2.1\,\text{V}$) | $0\text{--}2.1\,\text{V}$ | Chân 1: Nối nút đo nhãn mạng `BAT_SENSE`; Chân 2: Nối mass `GND` | Không có | `BUY` — `VERIFIED` | Cặp điện trở đối xứng 100k/100k tạo hệ số chia $1:2$ ($V_{\text{sense}} = V_{\text{SYS}} / 2$). Tuyệt đối không nối đường $5\,\text{V}$ vào ngõ vào ADC. |
| **C1** (`C_BAT`) | Lọc nhiễu cao tần tại nút phân áp và cấp điện tích tức thời khi SAR ADC lấy mẫu | $0\text{--}2.1\,\text{V}$ | Chân 1: Nối nút đo nhãn mạng `BAT_SENSE`; Chân 2: Nối mass `GND` | Không có | `BUY` — `PROJECT DECISION` | Tạo bộ lọc thông thấp với tần số cắt $f_c \approx 31.8\,\text{Hz}$, triệt tiêu gợn sóng đóng cắt của MT3608 và nhiễu sóng phát BLE. |

---

### Khối H: Tụ Ổn Định Nguồn & Giải Ngẫu (Decoupling & Bulk Capacitors)

#### Bảng H.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **C2** | Tụ ổn định nguồn 5V | **Tụ hóa nhôm 10µF 25V THT** (hoặc $47\mu\text{F}$) | Tụ hóa có phân cực (Electrolytic Cap) | Điện dung $10\,\mu\text{F}$, điện áp $25\,\text{V}$, bước chân $2.0\,\text{mm}$ | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | 1 |
| *(C3 cũ)* | *(Tụ ổn định ngõ ra LDO 1.8V)* | *Tụ hóa 10µF* | *Đã loại bỏ (REMOVED)* | *Không còn dùng rail 1.8V* | *Loại bỏ khỏi BOM V1* | 0 |
| *(C4 cũ)* | *(Tụ giải ngẫu cao tần 1.8V)* | *Tụ gốm 100nF* | *Đã loại bỏ (REMOVED)* | *Không còn dùng rail 1.8V* | *Loại bỏ khỏi BOM V1* | 0 |

#### Bảng H.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **C2** | Ổn định đường nguồn $5\,\text{V}$ ngõ ra MT3608 trước khi cấp vào chân VIN của ESP32 | $5.0\,\text{V}$ | Chân 1 ($+$): Nối đường nguồn `5V`; Chân 2 ($-$): Nối mass `GND` | Không có | `BUY` — `PROJECT DECISION` | Đặt sát chân VIN bo ESP32 để gánh xung dòng đỉnh khi khối vô tuyến BLE phát sóng. |
| *(C3, C4)* | *(Lọc nguồn 1.8V)* | *REMOVED* | *Không sử dụng* | *Toàn bộ chân* | `REMOVED` | Đã loại bỏ do không còn LDO 1.8V. |

---

### Khối I: Đầu Nối Mở Rộng Ngoại Vi (Expansion Connectors)

#### Bảng I.1: Đặc tả phần cứng & Footprint đề xuất
| Ký hiệu (Ref) | Tên linh kiện / Module | Mã linh kiện cụ thể (Exact Part) | Loại linh kiện | Giá trị / Thông số kỹ thuật | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **J2** (`J_I2C`) | Cổng mở rộng ngoại vi I2C 3.3V | **Male Pin Header 1x4 chân thẳng P2.54mm** | Đầu nối cọc đực (Connector) | 4 chân thẳng, dòng tải 3A, bước chân $2.54\,\text{mm}$ | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` | 1 |

#### Bảng I.2: Chức năng & Sơ đồ chân kết nối tín hiệu
| Ký hiệu (Ref) | Vai trò chức năng trong hệ thống | Điện áp làm việc | Các chân sử dụng | Các chân không dùng (NC) | Trạng thái (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| **J2** (`J_I2C`) | Cổng mở rộng bus I2C mức $3.3\,\text{V}$ để cắm thêm cảm biến hoặc màn hình OLED $3.3\,\text{V}$ | $0\text{--}3.3\,\text{V}$ | Chân 1: `3V3`; Chân 2: `GND`; Chân 3: `IMU_SDA` (`GPIO21`); Chân 4: `IMU_SCL` (`GPIO22`) | Không có | `BUY` — `OPTIONAL FOR EXTENSION` | Đấu nối song song trực tiếp với bus I2C của ESP32. |

---

### Khối J: Điểm Đo Kiểm Debug (Test Points) & Vật Liệu An Toàn

#### Bảng J.1: Thông số kỹ thuật & Vị trí trên mạch in
| Ký hiệu (Ref) | Tên điểm đo (Net Test Point) | Tên tín hiệu kết nối | Loại điểm đo | Điện áp danh định | Footprint đề xuất | SL |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: |
| **TP1** | TP_IMU_SCL | `IMU_SCL` (GPIO22) | Dải Header 1x4 chân thẳng | $3.3\,\text{V}$ | Header 1x04 P2.54mm (hoặc Pad D2.0mm) | 1 cụm (4 chân) |
| **TP2** | TP_IMU_SDA | `IMU_SDA` (GPIO21) | Dải Header 1x4 chân thẳng | $3.3\,\text{V}$ | Header 1x04 P2.54mm (hoặc Pad D2.0mm) | — |
| **TP3** | TP_3V3 | `3V3` | Dải Header 1x4 chân thẳng | $3.3\,\text{V}$ | Header 1x04 P2.54mm (hoặc Pad D2.0mm) | — |
| **TP4** | TP_GND | `GND` | Dải Header 1x4 chân thẳng | $0\,\text{V}$ | Header 1x04 P2.54mm (hoặc Pad D2.0mm) | — |
| **TP8** | TP_VBAT | `VBAT` | Pad đồng tròn trên PCB | $3.0\text{--}4.2\,\text{V}$ | `TestPoint:TestPoint_Pad_D2.0mm` | 1 |
| **TP9** | TP_VSYS | `V_SYS` | Pad đồng tròn trên PCB | $3.0\text{--}4.2\,\text{V}$ | `TestPoint:TestPoint_Pad_D2.0mm` | 1 |
| **TP10**| TP_5V | `5V` | Pad đồng tròn trên PCB | $5.0\,\text{V}$ | `TestPoint:TestPoint_Pad_D2.0mm` | 1 |
| **TP11**| TP_3V3_AUX | `3V3` | Pad đồng tròn trên PCB | $3.3\,\text{V}$ | `TestPoint:TestPoint_Pad_D2.0mm` | 1 |
| **INS1** | Vật liệu cách điện & đệm pin | Băng keo Kapton + Mút xốp EVA/PE dày 1.5mm | Đệm cách điện cơ khí | Nhiệt độ $> 200^\circ\text{C}$ | Tấm lót $54 \times 36\,\text{mm}$ mặt đáy | 1 bộ |

#### Bảng J.2: Ý nghĩa đo kiểm, Phân loại mua sắm & Giá trị dự toán
| Ký hiệu (Ref) | Ý nghĩa kiểm tra đo đạc | Trạng thái (Status) | Phân loại BOM | Đơn giá tham chiếu | Thành tiền (VNĐ) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **TP1–TP4** | Cụm 4 điểm đo I2C và nguồn cốt lõi (`SCL, SDA, 3V3, GND`) cắm Logic Analyzer | `BUY` (Core TP1–TP4) | `BUY` | 1.000đ / dải | **1.000đ** *(Tính chung dải header 1x4)* |
| **TP8** | Đo điện áp trực tiếp tại cell pin LiPo (trước công tắc) | `OPTIONAL` | `OPTIONAL` | 0đ | **0đ** *(Tích hợp PCB)* |
| **TP9** | Đo điện áp nguồn dương hệ thống sau công tắc gạt chính | `OPTIONAL` | `OPTIONAL` | 0đ | **0đ** *(Tích hợp PCB)* |
| **TP10**| Đo kiểm tra điện áp ra của MT3608 (bắt buộc trước khi cắm ESP32) | `OPTIONAL` | `OPTIONAL` | 0đ | **0đ** *(Tích hợp PCB)* |
| **TP11**| Đo kiểm tra đường nguồn $3.3\,\text{V}$ từ LDO 3.3V trên board DevKit | `OPTIONAL` | `OPTIONAL` | 0đ | **0đ** *(Tích hợp PCB)* |
| **INS1** | Đệm 3 tầng cách ly an toàn bảo vệ túi pin LiPo khỏi cọ xát với chân hàn THT | `BUY` | `BUY` | 25.000đ | **25.000đ** |

---

## 3. Tổng Hợp Thống Kê Số Lượng & Đối Chiếu Dự Toán Chi Phí

### 3.1 Kiểm toán số lượng linh kiện (Component Count Audit)
Thống kê chính xác và phân biệt rõ hai khái niệm:
- **`BUY_PHYSICAL_UNITS: 23` (23 đơn vị vật lý cần mua mới)**:
  - 15 linh kiện điện hoạt động: `MOD1, MOD2, BAT1, J1, SW1, SW2, SW3, SW4, D1, R1, R2, R3, C1, C2, J2` (15 đơn vị)
  - 3 socket cắm module trung gian: `J_ESP_L, J_ESP_R` (2 cái), `J_IMU` (1 cái) (3 đơn vị)
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

### 3.2 Bảng phân tích chi phí theo nhóm danh mục (Cost Recalculation Table)

| Phân nhóm danh mục linh kiện | Trạng thái mua sắm | Số lượng vật phẩm | Chi tiết các dòng cấu thành | Giá trị / Thành tiền (VNĐ) | Tỉ trọng chi phí (%) | Ghi chú kiểm toán chi phí |
| :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| **Linh kiện cốt lõi đã có sẵn** | `OWNED` | 2 linh kiện | `U1` (90.000đ) + `U2` (140.000đ) | 230.000 VNĐ | 0.00% *(Không chi trả)* | Đã có sẵn bo ESP32 DevKit và module WCMCU-20948. |
| **Khối Nguồn & Sạc Pin** | `BUY` | 5 vật phẩm | BAT1 (65.000) + MOD2 (15.000) + MOD1 (12.000) + SW1 (3.000) + J1 (2.500) | 97.500 VNĐ | 63.73% | Pin LiPo 1000mAh, mạch tăng áp 5V, mạch sạc Type-C, công tắc, cọc JST-PH. |
| **Khối Phím Bấm & Chỉ Thị Trạng Thái** | `BUY` | 6 vật phẩm | 3 switch SW2-SW4 (9.000) + LED D1 (1.000) + Trở R1 (500) + Cổng J2 (1.000) | 11.500 VNĐ | 7.52% | 3 phím nhấn tactile 12x12, 1 LED xanh lá 3mm, 1 trở hạn dòng 1kΩ, 1 header 1x4 mở rộng. |
| **Khối Thụ Động Đo Pin & Lọc Nguồn 5V** | `BUY` | 4 vật phẩm | 2 trở R2-R3 (1.000) + Tụ C1 (500) + Tụ C2 (1.000) | 2.500 VNĐ | 1.63% | 2 trở phân áp 100kΩ, 1 tụ lọc ADC 100nF, 1 tụ hóa 10µF (5V). |
| **Khối Socket Cắm Module** | `BUY` | 3 vật phẩm | 2 socket ESP32 1x19 (7.000) + 1 socket IMU 1x10 (2.500) | 9.500 VNĐ | 6.21% | 2 hàng rào cái 1x19, 1 hàng rào cái 1x10. |
| **Khối Test Points Cốt Lõi (1x4 Header)**| `BUY` | 1 vật phẩm | 1 dải header đực 1x4 `TP1–TP4` (SCL, SDA, 3V3, GND) | 1.000 VNĐ | 0.65% | Phục vụ kẹp đo Logic Analyzer trong phòng lab. |
| **Khối Phụ Kiện Cơ Khí & An Toàn Pin** | `BUY` | 4 vật phẩm | 3 Button Cap tròn 12mm (6.000) + 1 Bộ cách điện Kapton & EVA (25.000) | 31.000 VNĐ | 20.26% | 3 nắp chụp nút bấm tròn 12mm và bộ vật liệu lót đệm an toàn giảm chấn cho pin LiPo. |
| **Khối Test Points Đo Nguồn Mở Rộng** | `OPTIONAL` | 4 pad đồng | TP8 (VBAT) + TP9 (VSYS) + TP10 (5V) + TP11 (3V3) | 0 VNĐ | 0.00% | Bố trí pad đồng hàn trực tiếp trên mạch in PCB, không phát sinh chi phí mua ngoài. |
| **TỔNG CHI PHÍ THỰC TẾ PHẢI MUA MỚI** | **`BUY`** | **23 vật phẩm (20 dòng)** | **97.500 + 11.500 + 2.500 + 9.500 + 1.000 + 31.000** | **153.000 VNĐ** | **100.00%** | **Tổng chi phí dự toán mua mới cần chuẩn bị giải ngân.** |

### 3.3 Kiểm toán từng dòng linh kiện mua mới (Line-by-Line Math Verification)
$$\text{TOTAL\_BUY} = 12.000 + 15.000 + 65.000 + 2.500 + 3.000 + 9.000 + 1.000 + 500 + 500 + 500 + 500 + 1.000 + 1.000 + 7.000 + 2.500 + 1.000 + 6.000 + 25.000 = 153.000\,\text{VNĐ}$$

- **Đối chiếu với BOM cũ V1.5.0 (173.000 VNĐ)**:
  - Chi phí giảm trừ:
    - Loại bỏ U3 (BSS138): $-10.000\,\text{VNĐ}$
    - Loại bỏ U4 (LDO 1.8V): $-8.000\,\text{VNĐ}$
    - Loại bỏ C3 (Tụ hóa 10µF 1.8V): $-1.000\,\text{VNĐ}$
    - Loại bỏ C4 (Tụ gốm 100nF 1.8V): $-500\,\text{VNĐ}$
    - Điều chỉnh cụm Test Points từ 1x7 (1.500 VNĐ) xuống 1x4 (1.000 VNĐ): $-500\,\text{VNĐ}$
  - Tổng giảm trừ: $10.000 + 8.000 + 1.000 + 500 + 500 = 20.000\,\text{VNĐ}$.
  - Dự toán mới: $173.000 - 20.000 = 153.000\,\text{VNĐ}$.
- Toàn bộ đơn giá mang tính chất tham chiếu (`REFERENCE_PRICE / NEEDS_RECHECK`), cần đối chiếu với báo giá thời gian thực của nhà phân phối trước khi giải ngân.
- Trạng thái phê duyệt danh mục là `PROVISIONAL_PROCUREMENT_LIST` (danh mục tạm thời, chưa sẵn sàng giải ngân) khi các xung đột footprint chưa được giải quyết dứt điểm trên layout PCB.
