# BẢNG NỐI DÂY CHÂN-ĐẾN-CHÂN AIR MOUSE DIRECT 3.3V
## TÀI LIỆU BÀN GIAO THIẾT KẾ SƠ ĐỒ NGUYÊN LÝ (SCHEMATIC SPECIFICATION)

> **Dự án**: Chuột không gian không dây (Air Mouse BLE HID)  
> **Phiên bản kiến trúc**: V4.0.0 — Direct 3.3V Baseline (Đã khóa)  
> **Mục đích tài liệu**: Tài liệu giao việc kỹ thuật chi tiết chân-đến-chân (Pin-to-Pin Wire List) cho thành viên phụ trách vẽ lại sơ đồ nguyên lý (Schematic) trên KiCad.  
> **Quy định ràng buộc**: Không khôi phục mạch chuyển mức BSS138, không dùng LDO 1.8V, không có mạng nguồn 1V8. Tuyệt đối không đoán số chân vật lý nếu chưa chắc chắn hướng nhìn bo mạch (ghi rõ `NEEDS_PHYSICAL_ORIENTATION_CHECK`).

---

## 1. Nguyên Tắc & Quy Ước Nhãn Chân

1. **Phân định rõ ba cấp độ định danh chân**:
   - **Tên chân in trên module (Silkscreen Label)**: Nhãn in thực tế trên bo breakout (VD: `VCC`, `GND`, `SCL`, `SDA`, `AD0`, `NCS`, `FSY`, `B+`, `B-`, `OUT+`, `OUT-`, `VIN+`, `VIN-`, `VOUT+`, `VOUT-`).
   - **Tên ngoại vi / GPIO của ESP32**: Định danh logic trong vi điều khiển và firmware (VD: `GPIO21`, `GPIO22`, `GPIO25`, `GPIO26`, `GPIO27`, `GPIO32`, `GPIO34 / ADC1_CH6`, `3V3`, `GND`, `VIN/5V`).
   - **Số thứ tự chân vật lý (Physical Pin Number)**: Thứ tự chân trên header cắm. Đối với ESP32 DevKit 38 chân, nếu chưa xác minh bằng thước đo và đối chiếu hướng cắm thực tế, ghi rõ `NEEDS_PHYSICAL_ORIENTATION_CHECK` để tránh lỗi đối xứng gương.
2. **Quy tắc Mass hệ thống (System GND) và phân tách B- / OUT- của TP4056**:
   - `B+` và `B-` là hai đầu phía cell pin.
   - `OUT+` và `OUT-` là hai đầu phía tải đã đi qua mạch bảo vệ (IC DW01A + Dual MOSFET FS8205A).
   - `B-` **không được nối tắt trực tiếp với `OUT-` hoặc system GND ở bên ngoài module**, vì làm như vậy sẽ nối tắt (bypass) MOSFET bảo vệ, vô hiệu hóa hoàn toàn cơ chế bảo vệ quá xả và bảo vệ ngắn mạch của pin.
   - **System GND bắt đầu từ chân `OUT-` của TP4056**. Chân `OUT-` nối thông trực tiếp: `OUT- → system GND → MT3608 VIN-`.
   - Các khối MT3608 VIN-, ESP32 GND, WCMCU GND, nút bấm, LED và mạch phân áp ADC dùng chung System GND này.
   - Chỉ sơ đồ nội bộ của module TP4056 quyết định quan hệ điện giữa B- và OUT-.
   - **Cảnh báo bắt buộc**: *Chỉ áp dụng sơ đồ này khi module vật lý thực sự có đủ B+, B-, OUT+, OUT-. Nếu module chỉ có B+/B- hoặc OUT+/OUT-, phải dừng lại và xác minh đúng biến thể trước khi đấu dây.*
3. **Quy tắc điện áp logic**:
   - Toàn bộ tín hiệu điều khiển và bus I2C hoạt động ở mức logic **3,3 V**.

---

## 2. Bảng Nối Dây Chi Tiết Toàn Hệ Thống

| STT | Khối chức năng | Linh kiện / Chân nguồn (Source) | Tên mạng (Net Name) | Linh kiện / Chân đích (Destination) | Điện áp danh định | Chức năng kỹ thuật | Ghi chú & Cảnh báo an toàn |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **A. KHỐI CẢM BIẾN WCMCU-20948 (ICM-20948)** | | | | | | | |
| 1 | Cảm biến IMU | ESP32 DevKit Chân `3V3` | `+3V3` | WCMCU-20948 Chân `VCC` | 3.3 V | Cấp nguồn hoạt động chính | Nối trực tiếp nguồn 3.3V từ LDO 3.3V trên board DevKit. Cấp 5V nằm ngoài baseline đã kiểm chứng và có nguy cơ làm hỏng module; tuyệt đối không thực hiện. |
| 2 | Cảm biến IMU | ESP32 DevKit Chân `GND` | `GND` | WCMCU-20948 Chân `GND` | 0 V | Nối mass chung hệ thống | Bắt buộc thông mạch với toàn bộ hệ thống System GND. |
| 3 | Cảm biến IMU | ESP32 `GPIO22` (Header phải) | `I2C_SCL` | WCMCU-20948 Chân `SCL` (SCLK) | 3.3 V | Xung nhịp I2C Master 400 kHz | Baseline đã hoạt động với hai trở 10 kΩ onboard của module. Không tự động lắp thêm pull-up. Nếu mở rộng bus hoặc thay đổi dây/PCB, phải đo mức HIGH và rise time rồi mới quyết định giá trị pull-up hiệu dụng. |
| 4 | Cảm biến IMU | ESP32 `GPIO21` (Header phải) | `I2C_SDA` | WCMCU-20948 Chân `SDA` (SDI) | 3.3 V | Đường dữ liệu nối tiếp I2C | Module đã có sẵn trở kéo 10 kΩ onboard lên VCC (3.3V). |
| 5 | Cảm biến IMU | ESP32 DevKit Chân `3V3` | `+3V3` | WCMCU-20948 Chân `NCS` | 3.3 V | Chọn giao thức giao tiếp I2C | NCS kéo lên HIGH (3.3V) để vô hiệu hóa SPI, kích hoạt giao tiếp I2C trên ICM-20948. |
| 6 | Cảm biến IMU | ESP32 DevKit Chân `GND` | `GND` | WCMCU-20948 Chân `AD0` (SDO) | 0 V | Cấu hình địa chỉ I2C Slave | AD0 nối GND chọn địa chỉ I2C 7-bit là `0x68` (Ghi: 0xD0, Đọc: 0xD1). |
| 7 | Cảm biến IMU | ESP32 DevKit Chân `GND` | `GND` | WCMCU-20948 Chân `FSY` | 0 V | Đồng bộ khung hình (Frame Sync) | Không sử dụng tính năng đồng bộ ngoài, nối GND để chống nhiễu trôi nổi. |
| 8 | Cảm biến IMU | WCMCU-20948 Chân `INT` | `NC_IMU_INT` | Không nối (No Connect - NC) | — | Ngắt phần cứng cảm biến | Chưa dùng trong firmware V1 (đang lấy mẫu định kỳ polling 100 Hz). Để hở chân. |
| 9 | Cảm biến IMU | WCMCU-20948 Chân `ACL` | `NC_IMU_ACL` | Không nối (No Connect - NC) | — | I2C Aux Master Clock | Chân clock I2C phụ của ICM-20948. **TUYỆT ĐỐI KHÔNG NỐI VÀO SCL CHÍNH**. |
| 10 | Cảm biến IMU | WCMCU-20948 Chân `ADA` | `NC_IMU_ADA` | Không nối (No Connect - NC) | — | I2C Aux Master Data | Chân data I2C phụ của ICM-20948. **TUYỆT ĐỐI KHÔNG NỐI VÀO SDA CHÍNH**. |
| **B. KHỐI BA NÚT NHẤN ĐIỀU KHIỂN (TACTILE SWITCHES)** | | | | | | | |
| 11 | Nút bấm | ESP32 `GPIO25` (`NEEDS_PHYSICAL_ORIENTATION_CHECK`) | `BTN_LEFT` | SW_LEFT (Nút Chuột Trái) Tiếp điểm A | 3.3 V / 0 V | Tín hiệu nút bấm Chuột Trái | Firmware cấu hình `INPUT_PULLUP`. Bình thường HIGH (3.3V), nhấn nối xuống LOW (0V). |
| 12 | Nút bấm | SW_LEFT Tiếp điểm B (Đối diện A) | `GND` | Hệ thống `GND` | 0 V | Nối mass tiếp điểm nút bấm | Xem chi tiết quy tắc đấu chân nút 4 chân ở Mục 3 bên dưới. |
| 13 | Nút bấm | ESP32 `GPIO26` (`NEEDS_PHYSICAL_ORIENTATION_CHECK`) | `BTN_RIGHT` | SW_RIGHT (Nút Chuột Phải) Tiếp điểm A | 3.3 V / 0 V | Tín hiệu nút bấm Chuột Phải | Firmware cấu hình `INPUT_PULLUP`. Bình thường HIGH (3.3V), nhấn nối xuống LOW (0V). |
| 14 | Nút bấm | SW_RIGHT Tiếp điểm B (Đối diện A) | `GND` | Hệ thống `GND` | 0 V | Nối mass tiếp điểm nút bấm | Tiếp điểm đối diện tiếp điểm A. |
| 15 | Nút bấm | ESP32 `GPIO27` (`NEEDS_PHYSICAL_ORIENTATION_CHECK`) | `BTN_MODE` | SW_MODE (Nút Air Mouse Mode / Clutch) Tiếp điểm A | 3.3 V / 0 V | Bật/tắt chuột bay hoặc đóng băng con trỏ | Firmware cấu hình `INPUT_PULLUP`. GPIO27 là RTC GPIO hỗ trợ đánh thức Sleep. |
| 16 | Nút bấm | SW_MODE Tiếp điểm B (Đối diện A) | `GND` | Hệ thống `GND` | 0 V | Nối mass tiếp điểm nút bấm | Tiếp điểm đối diện tiếp điểm A. |
| **C. KHỐI LED CHỈ THỊ TRẠNG THÁI (STATUS LED)** | | | | | | | |
| 17 | Đèn báo | ESP32 `GPIO32` (`NEEDS_PHYSICAL_ORIENTATION_CHECK`) | `LED_CTRL` | Điện trở R1 (1.0 kΩ, 1/4W) Đầu 1 | 3.3 V | Tín hiệu điều khiển LED | Dòng xuất mức cao tối đa $\approx 1.2\,\text{mA}$, bảo vệ an toàn cho cổng GPIO ESP32. |
| 18 | Đèn báo | Điện trở R1 (1.0 kΩ) Đầu 2 | `LED_ANODE` | LED D1 (3mm Green) Chân Anode (+) | $\approx 2.1\,\text{V}$ | Dòng phân cực thuận LED | Chân dài hơn của LED hoặc phía không có vát cạnh. |
| 19 | Đèn báo | LED D1 (3mm Green) Chân Cathode (-) | `GND` | Hệ thống `GND` | 0 V | Đường thoát dòng LED | Chân ngắn hơn hoặc phía có vát phẳng trên thân LED. |
| **D. KHỐI PHÂN ÁP ĐO ĐIỆN ÁP PIN (BATTERY SENSING)** | | | | | | | |
| 20 | Đo pin | Điểm sau công tắc nguồn `SW1` | `V_SYS` | Điện trở R2 (100 kΩ, 1%, 1/4W) Đầu 1 | $3.0\text{--}4.2\,\text{V}$ | Lấy mẫu điện áp nguồn pin | Nối sau công tắc để không tiêu hao dòng tự xả của pin khi tắt máy. |
| 21 | Đo pin | Điện trở R2 (100 kΩ) Đầu 2 | `BAT_SENSE` | Nút mạng đo áp `BAT_SENSE` | $1.5\text{--}2.1\,\text{V}$ | Nút phân áp trung gian ($1:1$) | Tỉ lệ chia áp: $V_{\text{sense}} = V_{\text{SYS}} \times \frac{100\text{k}}{100\text{k} + 100\text{k}} = 0.5 \times V_{\text{SYS}}$. |
| 22 | Đo pin | Nút mạng `BAT_SENSE` | `BAT_SENSE` | ESP32 `GPIO34` (Kênh `ADC1_CH6`) | $1.5\text{--}2.1\,\text{V}$ | Ngõ vào bộ chuyển đổi tương tự-số | **GPIO34 là chân Input-Only, thuộc ADC1**, không bị xung đột với Wi-Fi/BLE. Firmware hiện tại chưa kích hoạt `analogRead`. |
| 23 | Đo pin | Nút mạng `BAT_SENSE` | `BAT_SENSE` | Điện trở R3 (100 kΩ, 1%, 1/4W) Đầu 1 | $1.5\text{--}2.1\,\text{V}$ | Trở phân áp nhánh dưới | Ghép song song với tụ lọc C1. |
| 24 | Đo pin | Điện trở R3 (100 kΩ) Đầu 2 | `GND` | Hệ thống `GND` | 0 V | Nối mass cầu phân áp | Điểm tựa điện thế cho phép đo ADC. |
| 25 | Đo pin | Nút mạng `BAT_SENSE` | `BAT_SENSE` | Tụ gốm C1 (100 nF, 50V) Cực 1 | $1.5\text{--}2.1\,\text{V}$ | Lọc nhiễu tần số cao cho ADC | Tụ gốm nhiều lớp (MLCC) 104 lọc nhiễu chuyển mạch và xung nhọn. |
| 26 | Đo pin | Tụ gốm C1 (100 nF) Cực 2 | `GND` | Hệ thống `GND` | 0 V | Nối mass tụ lọc | Đặt càng gần chân GPIO34 của ESP32 càng tốt. |
| **E. KHỐI CHUỖI NGUỒN PIN & ĐIỀU PHỐI NĂNG LƯỢNG** | | | | | | | |
| 27 | Chuỗi nguồn | Pin LiPo 1S Dây Đỏ (Dương) | `VBAT_RAW` | Cọc cắm JST-PH 2.0mm Pin 1 (Dương) | $3.0\text{--}4.2\,\text{V}$ | Dẫn nguồn từ cell pin LiPo | Dây đỏ từ khối pin có mạch bảo vệ PCM. |
| 28 | Chuỗi nguồn | Pin LiPo 1S Dây Đen (Âm) | `GND_BAT` | Cọc cắm JST-PH 2.0mm Pin 2 (Âm) | 0 V | Đường về mass của pin LiPo | Dây đen từ khối pin. |
| 29 | Chuỗi nguồn | Cọc cắm JST-PH 2.0mm Pin 1 | `VBAT` | Module TP4056 Chân `B+` | $3.0\text{--}4.2\,\text{V}$ | Ngõ vào cell pin sạc/bảo vệ | Nối trực tiếp ngõ dương cell pin vào chân B+ của TP4056. |
| 30 | Chuỗi nguồn | Cọc cắm JST-PH 2.0mm Pin 2 | `GND_BAT_CELL` | Module TP4056 Chân `B-` | 0 V | Ngõ âm cell pin | Nối ngõ âm cell pin vào chân B- của TP4056 (phía trước IC bảo vệ DW01A/FS8205A). Tuyệt đối không nối tắt chân này sang OUT- hoặc system GND bên ngoài module để tránh bypass MOSFET bảo vệ. |
| 31 | Chuỗi nguồn | Module TP4056 Chân `OUT+` | `V_BAT_PROT` | Công tắc SW1 Tiếp điểm ON (xác định qua VOM) | $3.0\text{--}4.2\,\text{V}$ | Dương nguồn sau mạch bảo vệ | Điện áp pin đã qua mạch bảo vệ. Nối vào một tiếp điểm ON của công tắc gạt SW1. Không dựa vào số chân in, dùng VOM đo thông mạch xác định. |
| 32 | Chuỗi nguồn | Module TP4056 Chân `OUT-` | `GND` | Hệ thống `GND` chung | 0 V | Điểm khởi đầu System GND | Chân OUT- là gốc của System GND toàn mạch: OUT- → system GND → MT3608 VIN-. Không đưa OUT- qua công tắc. |
| 33 | Chuỗi nguồn | Công tắc SW1 Chân Chung (COM) | `V_SYS` | Module MT3608 Chân `VIN+` | $3.0\text{--}4.2\,\text{V}$ | Cấp nguồn vào mạch nâng áp DC-DC | Khi gạt SW1 sang ON, tiếp điểm ON nối sang COM cấp nguồn dương sang `V_SYS` vào MT3608 VIN+. Tiếp điểm còn lại của SW1 để hở (NC). |
| 34 | Chuỗi nguồn | Hệ thống `GND` | `GND` | Module MT3608 Chân `VIN-` | 0 V | Mass ngõ vào nâng áp | Nối System GND (bắt nguồn từ TP4056 OUT-). |
| 35 | Chuỗi nguồn | Module MT3608 Chân `VOUT+` | `+5V_BOOST` | Chân `VIN` (hoặc `5V`) của ESP32 DevKit | 5.0 V | Cấp nguồn 5V ổn định cho ESP32 | **Bắt buộc đo chỉnh biến trở MT3608 đạt đúng 5.0V trước khi cắm ESP32**. |
| 36 | Chuỗi nguồn | Module MT3608 Chân `VOUT-` | `GND` | Chân `GND` của ESP32 DevKit | 0 V | Mass ngõ ra nâng áp | Nối mass chung. |
| 37 | Chuỗi nguồn | Đường nguồn `+5V_BOOST` | `+5V_BOOST` | Tụ hóa C2 (10 µF, 16V hoặc 25V) Cực Dương (+) | 5.0 V | Tụ bù năng lượng và lọc nguồn | Đặt sát chân VIN của ESP32. Chú ý đúng cực tính tụ hóa. |
| 38 | Chuỗi nguồn | Cực Âm (-) Tụ hóa C2 | `GND` | Hệ thống `GND` | 0 V | Thoát mass tụ lọc | Vạch sọc trắng trên thân tụ là cực Âm. |
| **F. CÁC HEADER MỞ RỘNG VÀ ĐIỂM ĐO KIỂM (TEST POINTS)** | | | | | | | |
| 39 | Header mở rộng | Đường nguồn `+3V3` | `+3V3` | Header I2C ngoài J2 Pin 1 | 3.3 V | Cấp nguồn 3.3V cho thiết bị I2C phụ | Dự phòng cắm màn hình OLED hoặc que đo Logic Analyzer. |
| 40 | Header mở rộng | Hệ thống `GND` | `GND` | Header I2C ngoài J2 Pin 2 | 0 V | Mass header mở rộng | Mass chuẩn. |
| 41 | Header mở rộng | Mạng `I2C_SDA` (GPIO21) | `I2C_SDA` | Header I2C ngoài J2 Pin 3 | 3.3 V | Đường SDA mở rộng | Nối thông với chân SDA của ICM-20948. |
| 42 | Header mở rộng | Mạng `I2C_SCL` (GPIO22) | `I2C_SCL` | Header I2C ngoài J2 Pin 4 | 3.3 V | Đường SCL mở rộng | Nối thông với chân SCL của ICM-20948. |
| 43 | Điểm đo kiểm | Mạng `I2C_SCL` | `I2C_SCL` | Test Point `TP1` (Dải Header 1x4 Pin 1) | 3.3 V | Đo xung nhịp I2C bằng Oscilloscope | Điểm kẹp que đo kiểm tra tần số và sườn xung 400 kHz. |
| 44 | Điểm đo kiểm | Mạng `I2C_SDA` | `I2C_SDA` | Test Point `TP2` (Dải Header 1x4 Pin 2) | 3.3 V | Đo dữ liệu I2C bằng Logic Analyzer | Điểm kẹp que đo giải mã bản tin I2C và kiểm tra ACK. |
| 45 | Điểm đo kiểm | Đường nguồn `+3V3` | `+3V3` | Test Point `TP3` (Dải Header 1x4 Pin 3) | 3.3 V | Kiểm tra điện áp LDO 3.3V trên board DevKit | Kiểm tra độ sụt áp 3.3V khi ESP32 phát sóng vô tuyến. |
| 46 | Điểm đo kiểm | Hệ thống `GND` | `GND` | Test Point `TP4` (Dải Header 1x4 Pin 4) | 0 V | Kẹp mass que đo dụng cụ đo | Kẹp mass máy hiện sóng / máy phân tích logic. |
| 47 | Pad đo mở rộng | Nút `VBAT` | `VBAT` | Test Pad `TP8` (Pad đồng trần Ø1.5mm) | $3.0\text{--}4.2\,\text{V}$ | Đo điện áp trực tiếp tại cực pin | Dùng đồng hồ VOM kiểm tra tình trạng pin trước sạc. |
| 48 | Pad đo mở rộng | Nút `V_SYS` | `V_SYS` | Test Pad `TP9` (Pad đồng trần Ø1.5mm) | $3.0\text{--}4.2\,\text{V}$ | Đo điện áp sau công tắc gạt | Xác nhận công tắc nguồn đã đóng mạch tốt hay chưa. |
| 49 | Pad đo mở rộng | Nút `+5V_BOOST` | `+5V_BOOST` | Test Pad `TP10` (Pad đồng trần Ø1.5mm) | 5.0 V | Đo ngõ ra mạch boost MT3608 | Kiểm tra ngõ ra 5V có đúng danh định trước khi đóng điện. |
| 50 | Pad đo mở rộng | Nút `+3V3` | `+3V3` | Test Pad `TP11` (Pad đồng trần Ø1.5mm) | 3.3 V | Đo nguồn logic 3.3V độc lập | Điểm kiểm tra điện áp cấp cho cảm biến WCMCU-20948. |

---

## 3. Hướng Dẫn Kỹ Thuật Đấu Nối Cho Từng Khối Cụ Thể

### 3.1 Khối Nút Bấm Xúc Giác 4 Chân (Tactile Push Button 12x12mm)
- **Đặc điểm tiếp điểm cơ khí**: Nút nhấn xúc giác chuẩn $12 \times 12\,\text{mm}$ (hoặc $6 \times 6\,\text{mm}$) thường có 4 chân cắm xếp thành 2 cặp. Bên trong thân nút, **hai chân nằm cùng một phía hẹp đã được nối tắt với nhau bằng thanh kim loại dẫn điện cố định**.
- **Nguy cơ lỗi thường gặp**: Nếu đấu nhầm hai dây tín hiệu vào hai chân đã nối tắt ngầm bên trong, mạch sẽ bị kéo vĩnh viễn xuống GND (nút luôn ở trạng thái bị nhấn), khiến ESP32 không nhận biết được thao tác bấm.
- **Quy chuẩn đấu nối bắt buộc**:
  - Phải đấu tín hiệu GPIO vào một phía và dây GND vào **phía tiếp điểm đối diện** (qua khe hở cơ khí của nút).
  - Trước khi hàn lên bo mạch, người lắp ráp **bắt buộc phải dùng thang đo thông mạch (tiếng bip) trên đồng hồ vạn năng DMM** để kiểm tra: khi chưa bấm thì hai chân chọn phải hở mạch hoàn toàn; khi bấm nút thì đồng hồ mới kêu bip (thông mạch $< 1\,\Omega$).

### 3.2 Khối Nguồn Pin LiPo, Sạc TP4056 và Nâng Áp MT3608
- **Đấu nối công tắc nguồn SW1 trên đường dương nguồn**:
  - TP4056 `OUT+` → một tiếp điểm ON của `SW1`.
  - Chân `COM` của `SW1` → `V_SYS` → MT3608 `VIN+`.
  - Tiếp điểm còn lại của `SW1` để `NC` nếu dùng công tắc SPDT làm công tắc ON/OFF.
  - TP4056 `OUT-` → system GND → MT3608 `VIN-`.
  - **Không đưa OUT- qua công tắc**. Không ngắt đồng thời cả hai dây bằng công tắc SPDT một cực.
  - **Quy tắc xác định chân công tắc**: Không được dựa hoàn toàn vào số thứ tự chân 1/2/3 in trên thân công tắc vì mỗi biến thể có thể khác nhau. Người thi công bắt buộc dùng đồng hồ vạn năng DMM (thang đo thông mạch tiếng bip) để xác định chính xác chân COM và tiếp điểm ON trước khi hàn.
- **Quy trình đóng điện an toàn (Bring-up Sequence)**:
  1. Hàn dây từ giắc pin JST-PH vào chân `B+` và `B-` của module sạc TP4056. Tuyệt đối không nối tắt `B-` với `OUT-` hoặc System GND bên ngoài module.
  2. Nối `OUT+` của TP4056 vào một tiếp điểm ON của công tắc gạt `SW1`. Nối chân COM của `SW1` vào ngõ `VIN+` của MT3608. Nối trực tiếp `OUT-` của TP4056 vào System GND và chân `VIN-` của MT3608 (`OUT- → system GND → MT3608 VIN-`).
  3. **CHƯA ĐƯỢC NỐI NGÕ RA MT3608 VÀO ESP32**. Cắm pin LiPo vào, bật công tắc SW1 sang ON. Dùng tuốc-nơ-vít xoay biến trở tinh chỉnh trên module MT3608, đồng thời đo đồng hồ vạn năng tại hai chân `VOUT+` và `VOUT-` cho đến khi điện áp hiển thị **chính xác $5.00\,\text{V} \pm 0.05\,\text{V}$**.
  4. Tắt công tắc SW1, ngắt pin, sau đó mới hàn dây từ ngõ ra MT3608 vào chân `VIN` và `GND` của ESP32 DevKit cùng tụ hóa C2 (10 µF).
- **Cảnh báo cực tính pin**: Kiểm tra kỹ dây đỏ (+) và dây đen (-) của cọc pin JST-PH. Một số loại pin trên thị trường bị bấm ngược thứ tự chân tại đầu cos JST. Luôn đo kiểm cực tính bằng đồng hồ trước khi cắm giắc.
- **Cấm thao tác**: Tuyệt đối không vừa cắm sạc cổng Type-C trên module TP4056 vừa tiến hành hàn dây hoặc rút cắm linh kiện trên mạch khi chưa ngắt công tắc nguồn.

### 3.3 Khối Phân Áp Giám Sát Pin (ADC1_CH6 / GPIO34)
- Mạch gồm hai điện trở $100\,\text{k}\Omega$ mắc nối tiếp tạo hệ số suy hao $0.5$. Dòng tiêu hao qua cầu phân áp:
  $$I_{\text{divider}} = \frac{V_{\text{BAT}}}{R_2 + R_3} = \frac{4.2\,\text{V}}{200\,\text{k}\Omega} = 21\,\mu\text{A}$$
  Mức dòng này cực nhỏ, không gây sụt dung lượng pin đáng kể khi bật máy.
- Tụ $C_1$ ($100\,\text{nF}$) mắc song song với $R_3$ giúp ổn định điện áp ngõ vào bộ lấy mẫu SAR ADC của vi điều khiển ESP32, chống hiện tượng sụt áp tức thời do tụ lấy mẫu nội ($C_{\text{sample}} \approx 4\text{--}10\,\text{pF}$) nạp điện.
- **Trạng thái firmware**: Hàm `analogRead(34)` hiện tại **chưa được gọi** trong firmware Tuần 5 để ưu tiên chu kỳ quét 100 Hz của I2C và BLE.

---

## 4. Danh Mục Các Chân Tuyệt Đối Cấm Nối (Forbidden Connections)

Người vẽ schematic và người thi công mạch in phải tuân thủ nghiêm ngặt các rào cản kỹ thuật sau:

1. **TUYỆT ĐỐI KHÔNG NỐI `WCMCU ACL` VÀO ĐƯỜNG `SCL` CHÍNH**:
   - Chân `ACL` trên module WCMCU-20948 là chân xuất xung nhịp cho giao tiếp I2C Master phụ trợ (Auxiliary I2C Master) dùng để nối riêng với cảm biến bên ngoài (như từ kế hoặc áp kế phụ). Việc chập `ACL` vào đường `SCL` (GPIO22) sẽ gây xung đột bus (bus contention), phá hỏng giao tiếp I2C giữa ESP32 và cảm biến.
2. **TUYỆT ĐỐI KHÔNG NỐI `WCMCU ADA` VÀO ĐƯỜNG `SDA` CHÍNH**:
   - Chân `ADA` là đường dữ liệu của bus I2C phụ trợ. Không được nối vào đường `SDA` (GPIO21). Cả hai chân `ACL` và `ADA` phải để hở (`NC`).
3. **TUYỆT ĐỐI KHÔNG CẤP NGUỒN 5V VÀO CHÂN `VCC` CỦA WCMCU-20948**:
   - Chân `VCC` của module WCMCU-20948 chỉ được nối duy nhất vào rail nguồn **3,3 V** lấy từ chân `3V3` của ESP32 DevKit. Cấp 5V nằm ngoài baseline đã kiểm chứng và có nguy cơ làm hỏng module; tuyệt đối không thực hiện.
4. **TUYỆT ĐỐI KHÔNG NỐI CHÂN `GPIO34` TRỰC TIẾP VỚI CỰC PIN LIPO**:
   - Điện áp pin LiPo ($3.0\text{--}4.2\,\text{V}$) vượt quá ngưỡng điện áp cho phép cực đại của chân vi điều khiển ESP32 ($3.6\,\text{V}$). Chân `GPIO34` chỉ được nối vào điểm giữa của cầu phân áp `BAT_SENSE` (sau điện trở $R_2$).
5. **TUYỆT ĐỐI CẤM SỬ DỤNG CÁC CHÂN `GPIO6` ĐẾN `GPIO11` TRÊN ESP32**:
   - Các chân GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, GPIO11 được kết nối nội bộ trực tiếp với chip nhớ SPI Flash trên module ESP32. GPIO6–11 được dành cho SPI Flash trên ESP32-WROOM và không được sử dụng cho ngoại vi.
6. **TUYỆT ĐỐI KHÔNG ĐƯA BSS138 HOẶC MẠNG NGUỒN 1V8 TRỞ LẠI SCHEMATIC**:
   - Thiết kế V4.0.0 đã loại bỏ hoàn toàn khối chuyển mức BSS138 và IC hạ áp 1.8V. Không vẽ thêm bất kỳ footprint nào liên quan đến hai khối này để tránh sai lệch với baseline đã nghiệm thu trên bàn thực nghiệm.
