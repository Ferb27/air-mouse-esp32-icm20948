# CẨM NANG VẤN ĐÁP BẢO VỆ GIỮA KỲ 1 TRANG (MIDTERM DEFENSE ONE-PAGE)
## DỰ ÁN: AIR MOUSE BLE HID (ESP32 + ICM-20948)

> **Môn học**: Hệ thống nhúng (Embedded Systems) — Báo cáo Giữa kỳ Tuần 5  
> **Kiến trúc**: Hybrid 9-Axis Air Mouse  
> **Quy tắc**: Câu trả lời cô đọng, đi thẳng vào trọng tâm, có cơ sở kỹ thuật thuyết phục, dễ thuộc cho cả 3 thành viên trong nhóm.  

---

### Q1. Đề tài của nhóm đang làm gì?
Nhóm làm chuột bay không dây **Hybrid 9-Axis Air Mouse BLE HID** dùng ESP32 và cảm biến ICM-20948. Gyroscope đo vận tốc góc cổ tay để di chuyển con trỏ tương đối (Relative Rate-Control). Accelerometer hỗ trợ chống trôi, nhận diện đứng yên và nhận dạng cử chỉ vung tịnh tiến ngắn (Back/Forward). Tích hợp cơ chế tái định tâm giúp đổi tư thế cầm tự do (kể cả chĩa lên trời).

### Q2. Những ngoại vi nào được sử dụng trong hệ thống?
- **Nội vi ESP32**: I2C0 Master ($400\,\text{kHz}$), GPIO Input (`GPIO25, 26, 27`), GPIO Output (`GPIO32`), SAR ADC1 (`GPIO34`), và khối phần cứng BLE v4.2.
- **Ngoại vi bên ngoài**: Cảm biến chuyển động 9 trục ICM-20948 trên module WCMCU-20948 (kết nối trực tiếp I2C mức $3.3\,\text{V}$, `BENCH_VERIFIED_ON_OWNED_MODULE`).

### Q3. Cảm biến ICM-20948 gồm những gì bên trong?
Gồm 3 khối cảm biến đóng gói dạng Multi-Chip Module (SiP): Gyroscope 3 trục, Accelerometer 3 trục và Magnetometer 3 trục (AK09916, đế silicon riêng của Asahi Kasei), kèm bộ chuyển đổi ADC 16-bit nội bộ. Tổng cộng là **9 trục cảm biến vật lý**, không phải vị trí XYZ và góc 3D trong phòng.

### Q4. Bus I2C dùng để làm gì trong mạch?
Dùng để truyền thông dữ liệu hai chiều giữa ESP32 (Master) và ICM-20948 (Slave, địa chỉ `0x68`) với tốc độ $400\,\text{kHz}$ qua 2 dây `SDA` (`GPIO21`) và `SCL` (`GPIO22`) nối trực tiếp ở mức $3.3\,\text{V}$ trên module WCMCU-20948 sở hữu, không cần mạch chuyển mức BSS138 hay LDO 1,8 V phụ.

### Q5. Thanh ghi `REG_BANK_SEL` là gì và tại sao bắt buộc phải dùng?
Là thanh ghi chuyển Bank nằm ở địa chỉ cố định `0x7F` trên mọi bank của ICM-20948. Do chip tổ chức thành 4 User Bank (Bank 0, 1, 2, 3) với không gian địa chỉ 512 byte (khoảng 80–100 thanh ghi hoạt động). Muốn truy cập thanh ghi ở Bank nào thì bắt buộc phải ghi số Bank tương ứng vào bits [5:4] của thanh ghi này trước.

### Q6. Thanh ghi `PWR_MGMT_1` bao nhiêu bit? Từng bit quan trọng làm gì?
Độ rộng 8-bit, nằm ở Bank 0, địa chỉ `0x06`. Nhóm ghi giá trị **`0x01`** (`0b00000001`):
- Bit 6 (`SLEEP = 0`): Đánh thức chip khỏi chế độ ngủ tiết kiệm điện mặc định.
- Bit 5 (`LP_EN = 0`): Tắt chế độ Low-Power để đo đạc liên tục hiệu năng cao.
- Bits [2:0] (`CLKSEL = 001`): Tự động chọn nguồn xung nhịp PLL tốt nhất (dự phòng dao động nội 20 MHz theo DS-000189 Table 16).

### Q7. Thanh ghi `GYRO_CONFIG_1` bao nhiêu bit? Giá trị `0x1B` nghĩa là gì?
Độ rộng 8-bit, nằm ở Bank 2, địa chỉ `0x01`. Nhóm ghi **`0x1B`** (`0b00011011`):
- Bit 0 (`GYRO_FCHOICE = 1`): Bật bộ lọc dải thông thấp phần cứng (Hardware DLPF).
- Bits [2:1] (`GYRO_FS_SEL = 01`): Chọn dải đo toàn thang $\pm 500^{\circ}/\text{s}$ (độ nhạy $65.5\,\text{LSB}/(^{\circ}/\text{s})$).
- Bits [5:3] (`GYRO_DLPFCFG = 011` tức số $3$): Cài đặt tần số cắt bộ lọc DLPF là $51.2\,\text{Hz}$, độ trễ $5.9\,\text{ms}$.

### Q8. Thanh ghi cấu hình khác thanh ghi dữ liệu thế nào?
- **Thanh ghi cấu hình (R/W)**: Dùng để thiết lập chế độ làm việc phần cứng (chọn dải đo, bộ lọc, clock, nguồn); thường chỉ ghi 1 lần lúc khởi động.
- **Thanh ghi dữ liệu (Read-Only)**: Chứa kết quả đo vật lý tức thời từ ADC 16-bit của cảm biến; liên tục thay đổi theo chuyển động tay người dùng.

### Q9. Các thanh ghi `GYRO_XOUT` và `ACCEL_XOUT` chứa dữ liệu gì?
Chứa giá trị số nguyên 16-bit có dấu dạng bù hai (High byte và Low byte). Ta đọc nối 2 byte lại thành `int16_t`:
- Chia $65.5$ để chuyển Gyro thô sang đơn vị vận tốc góc ($^{\circ}/\text{s}$).
- Chia $8192.0$ để chuyển Accel thô sang đơn vị gia tốc trọng trường ($g$).

### Q10. Thư viện `Wire.h` làm nhiệm vụ gì?
Là thư viện phần cứng (HAL) điều khiển ngoại vi I2C Master tích hợp sẵn của ESP32: tạo xung nhịp SCL, tạo điều kiện START/STOP, truyền nhận từng byte trên đường SDA và kiểm tra cờ ACK/NACK từ slave.

### Q11. Hai thao tác cơ bản của I2C: Read và Write khác nhau thế nào?
- **Ghi (Write)**: Master gửi địa chỉ Slave kèm bit $R/W = 0$, gửi tiếp địa chỉ thanh ghi cần ghi, rồi gửi byte dữ liệu cấu hình.
- **Đọc (Read)**: Master gửi địa chỉ Slave kèm bit $W=0$ và địa chỉ thanh ghi muốn đọc; sau đó phát xung REPEATED START, gửi lại địa chỉ Slave kèm bit $R/W = 1$, rồi đọc các byte dữ liệu Slave trả về.

### Q12. Tại sao nhóm dùng phong cách lập trình bán thanh ghi (Semi-Register)?
Để thể hiện bản chất kỹ thuật môn Hệ thống nhúng: hiểu rõ từng địa chỉ, từng bit cấu hình phần cứng của cảm biến. Nhóm dùng `Wire.h` làm cầu nối truyền nhận, tự viết các hàm mỏng `selectBank`, `writeReg`, `readReg` thay vì dùng thư viện đen che giấu hết thanh ghi.

### Q13. Chuột bị drift (tự trôi) thì hệ thống xử lý thế nào?
Xử lý bằng quy trình 4 tầng: (1) Lấy trung bình 200 lần polling lúc khởi động tĩnh (nominal delay $10\,\text{ms}$, thời gian danh định $\approx 2.0\,\text{s}$) để trừ sai số offset tĩnh (Bias); (2) Bật bộ lọc phần cứng DLPF $51.2\,\text{Hz}$ (Gyro) và $50.4\,\text{Hz}$ (Accel); (3) Bộ nhận diện đứng yên (kết hợp Gyro và Accel) tự động khóa ngõ ra $\Delta = 0$ khi tay dừng; (4) Vùng chết Dead-zone ($0.8^{\circ}/\text{s}$) cắt sạch rung tay sinh lý.

### Q14. Nếu cầm chuột chĩa thẳng lên trời thì sao?
Nhóm dùng gia tốc kế đo hướng vector trọng trường Trái Đất $\vec{g}$ chiếu vào thân cảm biến, tính toán Quaternion tham chiếu để xoay vận tốc góc đo được sang mặt phẳng điều khiển trực quan trước mắt người dùng. Do đó, dù chĩa lên trời hay cầm ngang, lắc tay sang hai bên con trỏ vẫn di chuyển ngang màn hình.

### Q15. Chuyển động tịnh tiến trong không gian được xử lý thế nào?
Nhóm **chỉ nhận dạng cử chỉ vung tịnh tiến ngắn (Translational Flick Gesture)** qua mẫu xung gia tốc (Vung nhanh sang trái $\rightarrow$ Back trang web; Vung nhanh sang phải $\rightarrow$ Forward trang web). Nhóm **tuyệt đối không tích phân gia tốc kế 2 lần để tìm vị trí XYZ**, vì sai số offset bị nhân với $t^2$ sẽ bùng nổ hàng mét chỉ sau vài giây.

### Q16. Tại sao chọn ICM-20948 thay vì MPU6050?
Nhóm chọn ICM-20948 vì các lý do kỹ thuật an toàn và phù hợp kiến trúc: (1) Cấu trúc User Bank Register (4 bank, 512 byte không gian địa chỉ); (2) Bộ lọc số phần cứng DLPF đa dải tần linh hoạt cho cả Gyroscope và Accelerometer; (3) Tích hợp sẵn la bàn 3 trục AK09916 tạo thành cụm 9-DOF hoàn chỉnh trong đóng gói SiP, sẵn sàng cho các thuật toán định hướng nâng cao sau này.

### Q17. Tại sao nối trực tiếp 3,3 V vào module WCMCU-20948 khi datasheet IC trần ghi VDDIO 1,8 V?
Nhóm chọn nối trực tiếp 3,3 V trên đúng module WCMCU-20948 mà nhóm đang sở hữu và đã kiểm chứng chức năng thực nghiệm bằng ACK 0x68, WHO_AM_I = 0xEA, register readback vật lý thành công và đọc luồng dữ liệu 12 byte thực tế. Đây là kết quả thực nghiệm trên bàn (bench-test) của mẫu module cụ thể nhằm tối giản bo mạch 1 lớp và loại bỏ tiếp xúc lỏng của mạch chuyển mức trung gian, không phải khẳng định chung cho mọi loại breakout ICM-20948 trên thị trường.
