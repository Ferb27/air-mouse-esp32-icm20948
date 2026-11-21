# Nguồn trích dẫn trong gói

Bản trích phục vụ lắp phần cứng. Ưu tiên hướng dẫn V2 và số đo thật; ký hiệu nguồn giữ để tra cứu.

- [P2]: V2 chốt board chính 90×150 mm, pin 1S PCM chưa chọn, giữ TP4056 khoảng 1 A, J5V tháo rời, vùng pin tối thiểu 58×40 mm gồm viền.
- [P]: ràng buộc V1 còn áp dụng: DB9, nguồn bó 2–3 lõi khoảng dưới 10–15 cm, Kapton/mút 1–2 mm, ba nút/cap cần thử, giữ socket.
- [B]: 03_BOM_VAT_TU.csv; dòng pin 17 là lịch sử, không phải quyết định mua hiện tại.
- [N]: 04_NOI_DAY_NETLIST.md; lắp theo 43 dòng mục 3.7 hướng dẫn perfboard.
- [F]: 05_CHAN_GPIO.md; [M]: 06_KICH_THUOC_MODULE.md.
- [O]: đề cương cũ dùng cảm biến khác, không dùng để đấu dây hiện tại; không cần đề cương để lắp.
- [FW]/[PR]: phần mềm do chủ dự án làm, không kèm mã/lệnh thực thi trong gói. Quét I2C/WHO_AM_I và hành vi nút/LED cần chương trình thử; việc hàn xong chưa chứng minh chức năng.

## Căn cứ kỹ thuật trích từ nguồn [A]/[H]/[W]

### 1.3 Module cảm biến WCMCU-20948 & Quyết định Kết nối Trực tiếp 3.3V [`BENCH_VERIFIED_ON_OWNED_MODULE`]
- **Thông số cơ khí đã khóa (Locked Mechanical Reference)**:
  - **Board outline**: $26.7\,\text{mm} \times 15.3\,\text{mm}$
  - **Header**: $1 \times 10$ chân cắm thẳng hàng, bước chân `PIN_PITCH = 2.54 mm`.
  - **Footprint reference**: `PinSocket_1x10_P2.54mm_Vertical` + custom board outline $26.7 \times 15.3\,\text{mm}$.
- **Thông số điện và kết quả thực nghiệm Bring-up (Hardware Bring-up Verification)**:
  - **Kết nối thực tế**: Module WCMCU-20948 nối trực tiếp vào ESP32 ở điện áp $3.3\,\text{V}$ (`VCC -> 3V3`, `GND -> GND`, `SCL -> GPIO22`, `SDA -> GPIO21`, `NCS -> 3V3`, `AD0 -> GND`, `FSY -> GND`).
  - **Trở kéo bus I2C**: Hai điện trở dán mã "103" ($10\,\text{k}\Omega$) tích hợp sẵn trên module WCMCU-20948 đóng vai trò trở kéo nội bộ cho SDA/SCL lên $3.3\,\text{V}$.
  - **Tốc độ I2C**: Vận hành thành công ở $400\,\text{kHz}$ (Fast-Mode).
  - **Kiểm chứng thực tế ((nguồn gốc; nội dung cần thiết đã trích trong gói))**:
    - Quét I2C phản hồi ACK tại địa chỉ `0x68`.
    - Chuyển bank 0 thành công, đọc thanh ghi định danh `WHO_AM_I` (`0x00`) trả về chính xác `0xEA`.
    - 100/100 lần đọc WHO_AM_I thành công trong phép thử ngắn hạn ở cả 100 kHz và 400 kHz (0 NACK / 0 lỗi bus).
    - Đọc dữ liệu burst 12 byte con quay và gia tốc kế thành công, trục Z ghi nhận trọng lực Trái Đất $\approx 1g$ khi đặt tĩnh.
    - Firmware chính đọc lại thanh ghi vật lý thành công (`PWR_MGMT_1=0x01`, `GYRO_CONFIG_1=0x1B`, `ACCEL_CONFIG=0x1B`), chạy hiệu chuẩn 200 mẫu và vòng lặp 100 Hz.
- **Ranh giới kỹ thuật với Datasheet IC trần**:
  - Datasheet TDK InvenSense DS-000189 quy định dải $V_{\text{DDIO}}$ của chip IC trần là $1.71\text{--}1.95\,\text{V}$. Dự án chấp nhận kết nối trực tiếp $3.3\,\text{V}$ như một quyết định thiết kế mẫu thử nghiệm (prototype baseline) đã được kiểm chứng chức năng thực tế trên đúng linh kiện sở hữu. Nhóm không biến điều này thành khẳng định chung cho mọi breakout ICM-20948 trên thị trường.
- **Cấu hình chân WCMCU-20948 cho chế độ I2C**:
  - `VCC`: Nối trực tiếp nguồn $3.3\,\text{V}$ từ ESP32 DevKit.
  - `GND`: Nối mass hệ thống.
  - `SCLK / SCL`: Nối trực tiếp `GPIO22` của ESP32.
  - `SDI / SDA`: Nối trực tiếp `GPIO21` của ESP32.
  - `NCS`: **Nối cứng lên $3.3\,\text{V}$** để vô hiệu hóa SPI và cố định hoạt động ở chế độ I2C.
  - `SDO / AD0`: **Nối cứng xuống `GND`** để chọn địa chỉ I2C cố định là **`0x68`**.
  - `FSY`: Nối xuống `GND`.
  - `ACL`, `ADA`: Để hở (`NC`), đây là bus I2C Master phụ của IMU, **tuyệt đối không nối vào bus I2C của ESP32**.
  - `INT`: Tín hiệu ngắt chưa sử dụng ở V1 (firmware sử dụng cơ chế polling 100 Hz).


### 5.1 Khối nguồn & Kiểm chứng thực tế [`DECIDED`]
- Kiến trúc nguồn: `LiPo 1S -> TP4056/protection -> switch -> boost 5V -> ESP32 5V/VIN -> ESP32 3V3 -> WCMCU VCC (Direct 3.3V)`.
- Cung cấp đường nguồn đầu vào ổn định; độ ổn định thực tế phải được kiểm chứng dưới các xung dòng phát BLE của ESP32.
- Bắt buộc đo và vi chỉnh điện áp MT3608 về đúng $5.0\,\text{V} \pm 0.1\,\text{V}$ trước khi cắm ESP32.


## 4. Ranh Giới Kỹ Thuật & Giới Hạn Kết Luận

1. **Phạm vi kết luận**:
   - Kết quả này xác nhận: **Hoạt động thành công trên đúng module WCMCU-20948 và ESP32 mà nhóm đang sở hữu.**
   - Đây là quyết định kỹ thuật ở cấp độ mẫu thử nghiệm (prototype baseline) nhằm đơn giản hóa mạch in 1 lớp, loại bỏ rủi ro tiếp xúc của các module trung gian.
2. **Quy định datasheet của IC trần**:
   - Datasheet của nhà sản xuất TDK InvenSense (DS-000189) quy định dải hoạt động của IC trần là $V_{DD} = 1.71\text{--}3.6\,\text{V}$ nhưng $V_{DDIO} = 1.71\text{--}1.95\,\text{V}$ (§3.4); giới hạn tuyệt đối của $V_{DDIO}$ là $2.5\,\text{V}$ (§3.7, Table 9).
   - Nhóm không xóa dữ kiện này và không khẳng định mọi module WCMCU-20948 trên thị trường đều chịu được 3,3 V. Tuy nhiên, trên bo mạch breakout thương phẩm WCMCU-20948 cụ thể của nhóm, không ghi nhận NACK hoặc lỗi bus trong phép thử ngắn hạn đã ghi log khi cấp nguồn 3,3 V trực tiếp từ ESP32.
3. **Ranh giới tuyên bố minh bạch (Scope of Claims)**:
   - Nhóm không đưa ra tuyên bố mang tính khẳng định tuyệt đối về độ an toàn điện trên mọi điều kiện biên, không tuyên bố mức điện áp 3,3 V này phù hợp với định mức danh định của riêng IC trần, và chưa thực hiện các phép thử stress-test để kết luận về tuổi thọ lâu dài của linh kiện.
   - Nhóm ghi nhận trạng thái kết nối Bluetooth HID tới máy tính là chưa kiểm thử (`BLE_CONNECTION_STATUS: NOT_TESTED`), không tuyên bố chuột đã ghép nối thành công.

---


## 6. CÔNG VIỆC CHƯA HOÀN THÀNH, HẠN CHẾ & VẤN ĐỀ TỒN TẠI

Nhóm thẳng thắn nhìn nhận các hạn chế và ranh giới kỹ thuật hiện tại của dự án tại mốc giữa kỳ Tuần 5:
1. **Kết nối BLE HID với máy tính ở trạng thái NOT_TESTED**: Mã nguồn firmware BLE HID đã biên dịch thành công và phát tín hiệu quảng bá `AirMouse-ESP32`, nhưng nhóm CHƯA thực hiện ghép nối thực tế với máy tính PC để đo độ trễ và kiểm tra độ ổn định chuột trên hệ điều hành. Trạng thái kết nối máy tính: `NOT_TESTED`. Tuyệt đối không tuyên bố con trỏ chuột đã hoạt động thực tế trên PC.
2. **Ranh giới điện áp 3.3V trực tiếp và datasheet raw IC**: Hoạt động thành công trên đúng module WCMCU-20948 và ESP32 mà nhóm đang sở hữu (`BENCH_VERIFIED_ON_OWNED_MODULE`). Tuy nhiên, datasheet gốc của IC ICM-20948 (TDK DS-000189) quy định dải điện áp I/O $V_{\text{DDIO}}$ tối đa là $1.95\,\text{V}$. Việc cấp 3.3V trực tiếp là độ lệch kỹ thuật trên module breakout thương phẩm cụ thể của nhóm và có rủi ro tiềm ẩn về độ bền lâu dài chưa được kiểm chứng qua các bài stress-test. Nhóm không suy rộng thành mức an toàn tối thượng hay áp dụng cho mọi điều kiện biên.
3. **Hồ sơ thiết kế KiCad ở trạng thái chờ đồng bộ**: Tuân thủ nghiêm ngặt quy tắc không can thiệp thủ công file cú pháp S-expression thô của KiCad khi chưa cập nhật qua KiCad MCP Server. Do đó, hồ sơ KiCad hiện tại vẫn còn khối BSS138 và AMS1117-1.8V (trạng thái: `KICAD_SYNC_STATUS: STALE / BLOCKED_PENDING_KICAD_MCP_UPDATE`), sẽ được đồng bộ chính thức ở giai đoạn tiếp theo.
4. **Chức năng đo điện áp pin chưa kích hoạt trong firmware**: Mạch phân áp 100k/100k đã thiết kế phần cứng hoàn chỉnh, nhưng firmware Tuần 5 chưa gọi hàm `analogRead(34)` trong vòng lặp chính để ưu tiên tối ưu hóa bus I2C và pipeline 100 Hz.
5. **Khối từ kế AK09916 chưa tham gia thuật toán dung hợp**: Thuật toán V1 hiện triển khai dung hợp 6 trục (Gyro + Accel). Chưa tích hợp từ kế AK09916 nên trục Yaw chưa có mốc hướng tuyệt đối, dựa vào tích phân con quay. Dù đã có dead-zone triệt tiêu trôi tĩnh, việc xoay liên tục trong thời gian dài vẫn tích lũy sai số trôi nhẹ.

---


