# NGÂN HÀNG CÂU HỎI VẤN ĐÁP BẢO VỆ GIỮA KỲ (MIDTERM Q&A BANK)
## DỰ ÁN: AIR MOUSE BLE HID (ESP32 + ICM-20948)

> **Môn học**: Hệ thống nhúng (Embedded Systems)  
> **Phiên bản**: V1.0.0 — Official Defense Preparation Bank  
> **Cấu trúc**: 36 câu hỏi chuyên sâu phân bổ qua 12 nhóm chủ đề kỹ thuật cốt lõi.  
> **Định dạng mỗi câu**: `CÂU HỎI` $\rightarrow$ `TRẢ LỜI NGẮN (Trực diện)` $\rightarrow$ `GIẢI THÍCH CHUYÊN SÂU (Bảo vệ luận điểm)` $\rightarrow$ `NGUỒN BẰNG CHỨNG (Source Citation)`.  

---

## NHÓM 1: KHÁI NIỆM & BẢN CHẤT ĐỀ TÀI (PROJECT CONCEPT)

### Câu 1: Đề tài của nhóm về mặt kỹ thuật là loại thiết bị trỏ (pointing device) gì?
- **Trả lời ngắn**: Đây là thiết bị chuột bay **Hybrid Air Mouse sử dụng ICM-20948 9-DOF hardware, hiện triển khai 6-axis gyro–accelerometer fusion**, điều khiển con trỏ theo vận tốc xoay tương đối (Relative Rate-Control) bằng Gyroscope, đồng thời bổ sung Accelerometer qua bộ lọc bù Quaternion 6 trục ($K=2.0\,\text{s}^{-1}$) để nhận diện đứng yên chống trôi, nhận dạng cử chỉ vung tịnh tiến ngắn (Flick Back/Forward) và tự động bù góc nghiêng Roll/Pitch duy trì trực giao hệ quy chiếu điều khiển.
- **Giải thích chuyên sâu**: Air Mouse điều khiển con trỏ bằng chuyển động **XOAY của cổ tay (Rotational Motion)**, không phải bằng sự dịch chuyển tịnh tiến của bàn tay. Ngay cả khi tâm bàn tay đứng yên trong không gian, việc xoay cổ tay vẫn tạo ra vận tốc góc ($\omega$) và làm con trỏ di chuyển tương đối $(\Delta X, \Delta Y)$. Phần cứng ICM-20948 tích hợp sẵn từ kế AK09916 bên trong package (9-DOF hardware), nhưng firmware V1 hiện tại chỉ kích hoạt 6 trục (Gyro + Accel). Trục Yaw là tương đối và có trôi chậm chưa có la bàn tham chiếu tuyệt đối, nhưng được bù đắp hoàn hảo bằng cơ chế Clutch/Recenter. Accelerometer đóng vai trò phụ trợ thông minh: phát hiện trạng thái đứng yên để tự động bù sai số trôi tĩnh (Stationary Auto-Zero), nhận diện cử chỉ vung tịnh tiến ngắn (Flick Gestures), và ước lượng vector trọng trường để thiết lập hệ quy chiếu tham chiếu thích nghi (Adaptive Reference Frame) giúp con trỏ không bị méo hướng khi cổ tay nghiêng. Đề tài tuyệt đối không tích phân 2 lần gia tốc kế để tìm vị trí XYZ và không biến thành thiết bị trỏ tuyệt đối 3DoF.
- **Nguồn chứng minh**: *InvenSense MotionApps Architecture Guide, USB HID Pointing Device Class Definition, & TDK DS-000189*.

### Câu 2: Tại sao không dùng gia tốc kế (Accelerometer) tích phân 2 lần để tính vị trí con trỏ?
- **Trả lời ngắn**: Do hiện tượng bùng nổ sai số trôi (Drift Explosion) tỷ lệ với bình phương thời gian ($t^2$) khi tích phân tín hiệu nhiễu và độ lệch tĩnh (bias) của cảm biến MEMS.
- **Giải thích chuyên sâu**: Gia tốc đo được luôn chứa sai số offset $\epsilon$. Tích phân lần 1 ra vận tốc $v(t) = v_0 + \epsilon \cdot t$. Tích phân lần 2 ra quãng đường $s(t) = s_0 + v_0 t + \frac{1}{2} \epsilon t^2$. Chỉ sau vài giây, sai số vị trí sẽ lên tới hàng mét, khiến con trỏ chuột bay mất khỏi màn hình ngay cả khi thiết bị đặt bất động.
- **Nguồn chứng minh**: *Oliver J. Woodman (University of Cambridge), "An introduction to inertial navigation", Technical Report No. 696*.

### Câu 3: Con quay hồi chuyển (Gyroscope) đóng vai trò gì và tại sao phù hợp nhất cho Air Mouse?
- **Trả lời ngắn**: Con quay hồi chuyển đo trực tiếp vận tốc góc xoay quanh 3 trục ($\omega_x, \omega_y, \omega_z$ tính bằng $^{\circ}/\text{s}$), phản ánh trực tiếp ý định xoay cổ tay của người dùng mà không cần tích phân.
- **Giải thích chuyên sâu**: Khi người dùng muốn rê chuột sang phải, họ vung cổ tay sang phải tạo ra vận tốc góc $\omega_z > 0$. Vi điều khiển chỉ cần nhân giá trị này với một hệ số khuếch đại (gain) để tạo ra $\Delta X$, con trỏ lập tức dịch chuyển. Khi tay dừng vung, $\omega_z = 0$, con trỏ dừng lại ngay lập tức, đem lại cảm giác điều khiển tự nhiên và chính xác.
- **Nguồn chứng minh**: *TDK InvenSense ICM-20948 Datasheet §3.1*.

---

## NHÓM 2: VI ĐIỀU KHIỂN ESP32 (MCU ARCHITECTURE)

### Câu 4: Vì sao nhóm chọn ESP32 Classic mà không chọn STM32 hay vi điều khiển khác?
- **Trả lời ngắn**: ESP32 Classic tích hợp sẵn phần cứng thu phát Bluetooth Low Energy (BLE v4.2) trên cùng một chip, có xung nhịp mạnh ($240\,\text{MHz}$ dual-core), giá rẻ và phổ biến rộng rãi.
- **Giải thích chuyên sâu**: Nếu dùng STM32F4/F1, nhóm bắt buộc phải thiết kế thêm mạch ngoài gắn module Bluetooth (như HC-05 chạy Bluetooth Classic cũ hoặc nRF52/CC2541), làm tăng độ phức tạp mạch in, chi phí và khó khăn trong việc thiết lập chuẩn BLE HID. ESP32 xử lý đồng thời ngăn xếp BLE và giải thuật đọc cảm biến mượt mà nhờ 2 nhân Xtensa LX6 riêng biệt.
- **Nguồn chứng minh**: *Espressif ESP32 Series Datasheet §1 (Overview)*.

### Câu 5: ESP32 có những chân Strapping Pins nào và nhóm xử lý ra sao để tránh lỗi khởi động?
- **Trả lời ngắn**: Các chân GPIO0, GPIO2, GPIO15, GPIO12 là strapping pins quyết định chế độ boot; nhóm **không sử dụng** các chân này cho nút bấm hay cảm biến trên mạch mang V1.
- **Giải thích chuyên sâu**: Ví dụ, GPIO0 phải ở mức HIGH lúc cấp nguồn để ESP32 boot vào Flash nội. Nếu nối nút bấm vào GPIO0 mà người dùng vô tình giữ nút khi bật nguồn, ESP32 sẽ rơi vào chế độ nạp Firmware (Download Boot) và treo hệ thống. Nhóm đã bố trí nút bấm sang các chân an toàn (không thuộc nhóm strapping pins): GPIO25, GPIO26, GPIO27.
- **Nguồn chứng minh**: *Espressif Hardware Design Guidelines §2.4 (Strapping Pins)*.

---

## NHÓM 3: GIAO THỨC TRUYỀN THÔNG I2C (I2C PERIPHERAL)

### Câu 6: Giao tiếp I2C hoạt động theo nguyên lý master/slave như thế nào trong mạch?
- **Trả lời ngắn**: ESP32 đóng vai trò I2C Master (tạo xung nhịp SCL), cảm biến ICM-20948 đóng vai trò I2C Slave (địa chỉ `0x68`); dữ liệu truyền nối tiếp hai chiều trên đường SDA đồng bộ theo SCL.
- **Giải thích chuyên sâu**: Mọi giao dịch đều do ESP32 khởi xướng bằng điều kiện START (SDA kéo LOW khi SCL đang HIGH), gửi byte địa chỉ 7-bit kèm bit R/W (`0` = Ghi, `1` = Đọc), chờ xung ACK từ ICM-20948, truyền dữ liệu từng byte và kết thúc bằng điều kiện STOP.
- **Nguồn chứng minh**: *NXP I2C-bus specification and user manual UM10204 §3.1*.

### Câu 7: Tại sao đường truyền I2C bắt buộc phải có điện trở kéo lên nguồn (Pull-up Resistors)?
- **Trả lời ngắn**: Vì các chân I2C hoạt động ở chế độ cực máng để hở (Open-Drain), chỉ có thể chủ động kéo đường dây xuống GND (mức 0), không thể tự đưa lên mức 1.
- **Giải thích chuyên sâu**: Cấu trúc Open-Drain cho phép nhiều thiết bị nối chung đường dây mà không xảy ra ngắn mạch khi hai bên phát ngược mức logic (Wired-AND). Điện trở kéo lên nguồn đảm bảo khi không có thiết bị nào kéo xuống 0, đường dây tự động trở về mức HIGH logic. Nếu thiếu trở kéo, đường bus sẽ bị trôi lơ lửng (floating) và giao tiếp không thể diễn ra.
- **Nguồn chứng minh**: *NXP UM10204 §3.1.1*.

### Câu 8: Nếu I2C Master gửi địa chỉ mà cảm biến không phản hồi (NACK) thì mã nguồn xử lý thế nào?
- **Trả lời ngắn**: Hàm `Wire.endTransmission()` sẽ trả về mã lỗi khác `0` (ví dụ mã `2` = NACK nhận địa chỉ); chương trình phát hiện lỗi, hủy giao dịch và cảnh báo trạng thái.
- **Giải thích chuyên sâu**: Thay vì để chương trình bị treo (infinite wait), driver mỏng của nhóm kiểm tra giá trị trả về của `Wire.endTransmission()`. Nếu gặp NACK, driver thử lại tối đa 3 lần (timeout/retry policy). Nếu vẫn thất bại, hệ thống nhấp nháy LED đỏ báo lỗi phần cứng và không gửi bản tin rác lên BLE.
- **Nguồn chứng minh**: *Arduino Wire Library Reference & ESP32 Arduino Core Wire.cpp*.

---

## NHÓM 4: CẢM BIẾN CHUYỂN ĐỘNG ICM-20948

### Câu 9: Cảm biến ICM-20948 khác gì so với dòng MPU6050 cũ thường dùng trong đồ án?
- **Trả lời ngắn**: ICM-20948 là cụm cảm biến 9-DOF của TDK InvenSense (tích hợp thêm từ kế 3 trục AK09916), hỗ trợ chuẩn điện áp logic $1.8\,\text{V}$ hiện đại, sử dụng kiến trúc 4 User Bank (512 byte không gian địa chỉ) và tích hợp sẵn bộ xử lý chuyển động số DMP.
- **Giải thích chuyên sâu**: MPU-6050 là cảm biến 6-DOF thuần túy thế hệ cũ dùng logic $3.3\,\text{V}$. ICM-20948 thuộc dòng 9-DOF đóng gói SiP, hỗ trợ bộ lọc số DLPF đa dải tần linh hoạt cho cả Accel và Gyro, dải tần lấy mẫu điều chỉnh qua các bộ chia `SMPLRT_DIV`, và sẵn sàng cho việc mở rộng thuật toán định hướng 9 trục trong tương lai.
- **Nguồn chứng minh**: *TDK InvenSense ICM-20948 Datasheet DS-000189 rev 1.6*.

### Câu 10: ICM-20948 có từ kế (Magnetometer AK09916), tại sao nhóm không dùng trong V1?
- **Trả lời ngắn**: Vì chuột máy tính chỉ cần điều khiển tương đối; môi trường làm việc có nhiều từ trường nhiễu (khung sắt, loa laptop) làm từ kế bị méo và tốn thời gian xử lý không cần thiết.
- **Giải thích chuyên sâu**: Từ kế chỉ cần thiết khi cần định hướng la bàn tuyệt đối hướng Bắc (Yaw absolute orientation). Việc hiệu chuẩn từ trường cứng/mềm (Hard/Soft iron calibration) rất phức tạp và nếu không chuẩn sẽ gây giật con trỏ chuột. Tắt từ kế giúp giảm tải bus I2C và kéo dài thời lượng pin.
- **Nguồn chứng minh**: *InvenSense Application Note AN-000143 (Compass Calibration)*.

---

## NHÓM 5: THANH GHI & BITFIELD CỦA ICM-20948 (CHỌN LỌC CHUYÊN SÂU)

### Câu 11: Cơ chế User Bank Switching của ICM-20948 là gì và thanh ghi nào điều khiển?
- **Trả lời ngắn**: ICM-20948 tổ chức bản đồ thanh ghi thành 4 User Bank (Bank 0, 1, 2, 3) với không gian địa chỉ 512 byte (mỗi bank 128 byte, trong đó có khoảng 80–100 thanh ghi hoạt động); chuyển bank bằng cách ghi vào thanh ghi `REG_BANK_SEL` tại địa chỉ cố định `0x7F`.
- **Giải thích chuyên sâu**: Do số lượng thanh ghi cấu hình cần thiết để điều khiển cảm biến 9 trục vượt quá không gian địa chỉ 1 byte tiêu chuẩn trực tiếp (0x00–0x7F), chip chia hệ thống thanh ghi thành 4 Bank độc lập. Thanh ghi `REG_BANK_SEL` (`0x7F`) xuất hiện cố định ở mọi bank. Bits [5:4] của thanh ghi này quyết định bank được chọn: `0x00` = Bank 0 (dữ liệu chính, nguồn, WHO_AM_I, bộ đệm dữ liệu cảm biến ngoài), `0x10` = Bank 1 (hiệu chuẩn offset bias), `0x20` = Bank 2 (cấu hình DLPF, dải đo Gyro/Accel), `0x30` = Bank 3 (cấu hình I2C Master nội bộ). Cùng một địa chỉ thanh ghi có thể mang chức năng khác nhau tùy bank được chọn; muốn truy cập thanh ghi ở bank nào, bắt buộc phải chọn bank đó trước.
- **Nguồn chứng minh**: *TDK InvenSense ICM-20948 Datasheet, Register Map and Descriptions DS-000189 v1.3/v1.5 §10.1 & §13.1*.

### Câu 12: Phân tích thanh ghi `PWR_MGMT_1`: địa chỉ, giá trị cấu hình thực tế và ý nghĩa từng bit?
- **Trả lời ngắn**: Nằm ở Bank 0, địa chỉ `0x06`, độ rộng 8-bit. Giá trị vận hành là `0x01` (`0b00000001`) để đánh thức chip và khóa nguồn xung nhịp ổn định.
- **Giải thích chuyên sâu**:
  - Bit 7 (`DEVICE_RESET` = `0`): Không reset chip (`1` = Reset toàn bộ thanh ghi nội về mặc định).
  - Bit 6 (`SLEEP` = `0`): Đánh thức chip khỏi chế độ ngủ tiết kiệm điện mặc định sau khi cấp nguồn (`1` = Sleep).
  - Bit 5 (`LP_EN` = `0`): Tắt chế độ Low-Power để cảm biến đo liên tục hiệu năng cao (`0` = Duty-cycled mode disabled).
  - Bit 4 (`Reserved` = `0`): Bit dành riêng của hãng, luôn giữ mức 0.
  - Bit 3 (`TEMP_DIS` = `0`): Bật cảm biến nhiệt độ nội (`0` = Enable, `1` = Disable).
  - Bits [2:0] (`CLKSEL[2:0]` = `001`): Tự động chọn nguồn xung nhịp tốt nhất (Auto selects the best available clock source — PLL if ready, else internal 20 MHz oscillator).
- **Nguồn chứng minh**: *TDK InvenSense ICM-20948 Datasheet, Register Map and Descriptions DS-000189 v1.3/v1.5 §10.2 Table 16 (PWR_MGMT_1)*.

### Câu 13: Giá trị `0x1B` của thanh ghi `GYRO_CONFIG_1` thực chất bao gồm những bit nào?
- **Trả lời ngắn**: `0x1B` là biểu diễn Hex của chuỗi nhị phân `0b00011011` tại Bank 2, địa chỉ `0x01`.
- **Giải thích chuyên sâu**:
  - Bits [7:6] = `00`: Dự trữ.
  - Bits [5:3] (`GYRO_DLPFCFG` = `011` tức số thập phân $3$): Cài đặt tần số cắt của bộ lọc dải thông thấp số $3\text{dB Bandwidth} \approx 51.2\,\text{Hz}$, độ trễ $5.9\,\text{ms}$.
  - Bits [2:1] (`GYRO_FS_SEL` = `01` tức số thập phân $1$): Cài đặt dải đo toàn thang con quay hồi chuyển $\pm 500^{\circ}/\text{s}$.
  - Bit 0 (`GYRO_FCHOICE` = `1`): Kích hoạt bộ lọc số DLPF.
- **Nguồn chứng minh**: *TDK InvenSense ICM-20948 Datasheet, Register Map and Descriptions DS-000189 v1.3/v1.5 §14.2 (GYRO_CONFIG_1)*.

---

## NHÓM 6: DỮ LIỆU THÔ & CHUYỂN ĐỔI ĐƠN VỊ (DATA & CONVERSION)

### Câu 14: Thanh ghi I2C chỉ có 8-bit, làm sao đọc được dữ liệu cảm biến 16-bit?
- **Trả lời ngắn**: Cảm biến chia dữ liệu 16-bit thành 2 thanh ghi 8-bit liên tiếp: High Byte và Low Byte; vi điều khiển đọc 2 byte này rồi ghép bit theo quy tắc bù 2 (2's complement).
- **Giải thích chuyên sâu**: Ví dụ trục X của Gyro gồm `GYRO_XOUT_H` (`0x33`) và `GYRO_XOUT_L` (`0x34`). Khi đọc bằng Burst Read:  
  `int16_t raw_x = (int16_t)((buffer[0] << 8) | buffer[1]);`  
  Kiểu dữ liệu `int16_t` có dấu tự động diễn giải bit dấu (MSB) thành giá trị âm/dương chuẩn xác.
- **Nguồn chứng minh**: *ICM-20948 Datasheet §4.16*.

### Câu 15: Tại sao dải đo $\pm 500^{\circ}/\text{s}$ lại có hệ số độ nhạy là $65.5\,\text{LSB}/(^{\circ}/\text{s})$?
- **Trả lời ngắn**: Vì ADC của con quay hồi chuyển có độ phân giải 16-bit có dấu, dải giá trị từ $-32768$ đến $+32767$ đại diện cho $-500^{\circ}/\text{s}$ đến $+500^{\circ}/\text{s}$.
- **Giải thích chuyên sâu**:  
  $$\text{Sensitivity} = \frac{32768\,\text{LSB}}{500^{\circ}/\text{s}} = 65.536\,\text{LSB}/(^{\circ}/\text{s}) \approx 65.5\,\text{LSB}/(^{\circ}/\text{s})$$  
  Muốn đổi giá trị thô ra tốc độ góc: $\omega = (\text{Raw} - \text{Bias}) / 65.5$. Nếu đổi dải đo sang $\pm 2000^{\circ}/\text{s}$, độ nhạy sẽ giảm 4 lần xuống còn $16.4\,\text{LSB}/(^{\circ}/\text{s})$.
- **Nguồn chứng minh**: *ICM-20948 Datasheet §3.1 Table 1*.

---

## NHÓM 7: XỬ LÝ TÍN HIỆU & HIỆU CHUẨN (SIGNAL PROCESSING)

### Câu 16: Khi cảm biến đặt đứng yên trên bàn, vì sao giá trị Gyro đọc về không bằng 0?
- **Trả lời ngắn**: Do sai số độ lệch tĩnh (Zero-rate offset hay Gyro Bias) sinh ra từ dung sai cơ khí chế tạo MEMS và ứng suất nhiệt vi mô trên đế silicon.
- **Giải thích chuyên sâu**: Mọi cảm biến MEMS đều có một điện áp phân cực dư dù không có chuyển động cơ học. Nếu không bù trừ, giá trị này sẽ bị hệ thống hiểu nhầm là tay đang quay liên tục, làm con trỏ chuột tự động bò (drifting) trên màn hình.
- **Nguồn chứng minh**: *InvenSense MEMS Gyroscope Zero-Rate Output Application Note*.

### Câu 17: Quy trình hiệu chuẩn (Calibration) của nhóm diễn ra như thế nào?
- **Trả lời ngắn**: Trong khoảng 2.0 giây đầu sau khi bật nguồn, thiết bị được giữ nằm yên; ESP32 đọc $N=200$ mẫu (chu kỳ $10\,\text{ms}$, đồng bộ với cảm biến ODR $102.27\,\text{Hz}$ tránh trùng lặp mẫu), tính giá trị trung bình cộng của từng trục để lưu làm `bias_x, bias_y, bias_z`.
- **Giải thích chuyên sâu**: Mọi lần đo sau đó sẽ lấy: $\text{Raw\_Calibrated} = \text{Raw} - \text{Bias}$. Quá trình này bù trừ phần lớn sai số offset tĩnh tại nhiệt độ khởi động của cảm biến. Trong quá trình vận hành lâu dài, nếu nhiệt độ môi trường thay đổi lớn, có thể cần cập nhật bias động hoặc thực hiện lại thao tác hiệu chuẩn.
- **Nguồn chứng minh**: *TDK InvenSense Software Calibration Techniques*.

### Câu 18: Vùng chết (Dead-zone) là gì và khác gì so với bộ lọc thông thấp (Low-pass filter)?
- **Trả lời ngắn**: Bộ lọc thông thấp làm mịn dao động tần số cao; Vùng chết ép các chuyển động vận tốc siêu nhỏ (nhiễu rung tay) về chính xác bằng 0.
- **Giải thích chuyên sâu**: Tay người khi cố giữ yên vẫn có độ rung sinh lý biên độ nhỏ ($0.2\text{--}0.5^{\circ}/\text{s}$). Bộ lọc thông thấp chỉ làm mượt rung động này nhưng không triệt tiêu được nó. Dead-zone dùng hai ngưỡng: dưới 0.8 °/s đầu ra bằng 0; từ 0.8 đến 1.4 °/s là vùng chuyển tiếp tuyến tính; trên 1.4 °/s áp dụng phần vận tốc vượt ngưỡng thấp. Giá trị 1.2 °/s là ngưỡng Gyro độc lập dùng để nhận diện trạng thái đứng yên (giúp con trỏ chuột không bị dịch chuyển ngoài ý muốn khi người dùng dừng tay để bấm click chuột). Đề xuất tinh chỉnh các ngưỡng này trong tương lai cần kiểm chứng theo cảm giác rê chuột thực tế.
- **Nguồn chứng minh**: *MacKenzie, I. S., "Fitts' law as a research and design tool in human-computer interaction"*.

---

## NHÓM 8: NGOẠI VI GPIO & NÚT BẤM (GPIO & BUTTONS)

### Câu 19: Các nút bấm trên chuột được cấu hình Active-High hay Active-Low? Tại sao?
- **Trả lời ngắn**: Cấu hình Active-Low sử dụng điện trở kéo lên nội bộ (`INPUT_PULLUP`); khi nhấn nút chân GPIO bị nối xuống GND (mức `LOW`).
- **Giải thích chuyên sâu**: Cấu hình Active-Low an toàn và phổ biến nhất trong hệ thống nhúng vì không phải dẫn đường nguồn dương ($3.3\,\text{V}$) chạy vòng quanh các nút bấm cơ khí, giảm thiểu rủi ro chập nguồn xuống vỏ hoặc mass.
- **Nguồn chứng minh**: *Jack Ganssle, "A Guide to Debouncing", Ganssle Group*.

### Câu 20: Hiện tượng dội phím (Button Bouncing) là gì và nhóm khử rung bằng cách nào?
- **Trả lời ngắn**: Khi lá kim loại của nút nhấn cơ học chạm nhau, chúng bị đàn hồi và bật nhả liên tục trong vài mili-giây gây ra chuỗi xung kích ảo; nhóm dùng giải thuật khử rung phần mềm (Software Debounce) với ngưỡng khởi tạo $15\text{--}20\,\text{ms}$ (cần kiểm chứng với nút bấm thực tế).
- **Giải thích chuyên sâu**: Khi phát hiện cạnh xuống (Falling Edge), chương trình ghi nhận mốc thời gian `millis()`. Nếu trạng thái tiếp tục giữ LOW sau $20\,\text{ms}$, sự kiện click chuột mới được chính thức xác nhận và gửi bản tin BLE, ngăn chặn hiện tượng double-click ngoài ý muốn.
- **Nguồn chứng minh**: *Jack Ganssle, "A Guide to Debouncing"*.

---

## NHÓM 9: NGOẠI VI ADC & GIÁM SÁT PIN (ADC & BATTERY SENSE)

### Câu 21: Vì sao chân đo pin `BAT_SENSE` lại chọn `GPIO34` mà không chọn chân ADC khác?
- **Trả lời ngắn**: GPIO34 thuộc khối ADC1 (kênh ADC1_CH6). Khối ADC2 bị xung đột phần cứng với driver Wi-Fi trên ESP32; sử dụng ADC1_CH6 trên GPIO34 giúp tránh xung đột tài nguyên nếu sau này cần dùng Wi-Fi, đồng thời tận dụng hiệu quả chân chỉ có tính năng ngõ vào (Input-Only) của ESP32.
- **Giải thích chuyên sâu**: Trên ESP32, khối ADC2 (gồm các chân GPIO0, 2, 4, 12-15, 25-27) dùng chung bộ SAR ADC với bộ điều khiển Wi-Fi. Khi Wi-Fi driver kích hoạt, việc gọi `analogRead()` trên ADC2 sẽ bị chặn hoặc trả về lỗi `ESP_ERR_INVALID_STATE`. Mặc dù giao thức BLE không trực tiếp khóa ADC2 như Wi-Fi, nhưng việc chọn ADC1 (GPIO32-39) là quy chuẩn thiết kế an toàn nhất trên ESP32 nhằm tránh mọi xung đột tài nguyên SAR ADC tiềm ẩn. Đặc biệt, GPIO34 là kênh `ADC1_CH6` và là chân Input-Only (không có điện trở kéo nội và không có bộ đệm ngõ ra), giúp giải phóng các chân GPIO đa dụng hai chiều cho nút bấm và giao tiếp bus.
- **Nguồn chứng minh**: *Espressif ESP32 Technical Reference Manual §28.3 (SAR ADC) & ESP-IDF Programming Guide (ADC Limitations)*.

### Câu 22: Có thể nối trực tiếp cực dương pin LiPo vào chân ADC của ESP32 không? Tại sao?
- **Trả lời ngắn**: Không được nối trực tiếp; điện áp pin LiPo đầy lên tới $4.2\,\text{V}$, vượt quá điện áp ngõ vào cực đại an toàn của ESP32 ($3.6\,\text{V}$) và sẽ làm hỏng chân vi điều khiển.
- **Giải thích chuyên sâu**: Nhóm sử dụng cầu phân áp gồm 2 điện trở bằng nhau ($100\,\text{k}\Omega / 100\,\text{k}\Omega$) để chia đôi điện áp: $V_{\text{ADC}} = V_{\text{BAT}} \times \frac{100}{100+100} = \frac{V_{\text{BAT}}}{2}$. Điện áp tối đa vào chân ADC là $4.2\,\text{V} / 2 = 2.1\,\text{V}$, nằm an toàn trong dải đo tuyến tính của ADC1 khi bật suy hao $11\,\text{dB}$.
- **Nguồn chứng minh**: *Espressif ESP32 Datasheet §4.1 (Absolute Maximum Ratings)*.

---

## NHÓM 10: BLUETOOTH LOW ENERGY HID (BLE SUBSYSTEM)

### Câu 23: BLE HID là gì và tại sao máy tính nhận diện được Air Mouse mà không cần driver riêng?
- **Trả lời ngắn**: BLE HID (Human Interface Device over GATT Profile - HOGP) là tiêu chuẩn quốc tế của Bluetooth SIG; mọi hệ điều hành hiện đại đều tích hợp sẵn Generic HID Driver tuân theo tiêu chuẩn này.
- **Giải thích chuyên sâu**: Khi kết nối, ESP32 gửi bản đặc tả báo cáo (HID Report Descriptor) mô tả thiết bị là một chuột chuẩn có 3 nút bấm và 2 trục dịch chuyển $(X, Y)$. Máy tính giải mã bản tin này bằng driver chuột mặc định của hệ thống.
- **Nguồn chứng minh**: *Bluetooth SIG, "Human Interface Device (HID) Profile Specification" v1.1.1*.

### Câu 24: Một bản tin báo cáo chuyển động chuột (Mouse Report) gửi qua BLE gồm những byte nào?
- **Trả lời ngắn**: Cấu trúc bản tin phụ thuộc vào bản đặc tả báo cáo (HID Report Descriptor) được khai báo. Bản tin chuột tối thiểu gồm 3 byte [Buttons, dX, dY]; bản tin có con cuộn/pan gồm 4 đến 5 byte (ví dụ thư viện `T-vK/ESP32-BLE-Mouse` sử dụng bản tin 5-byte).
- **Giải thích chuyên sâu**:
  Trong tiêu chuẩn USB/BLE HID, định dạng báo cáo được quy định linh hoạt qua Report Descriptor đăng ký với máy chủ:
  - Byte 0 (Buttons): Bitmask trạng thái nút bấm (Bit 0 = Nút Trái, Bit 1 = Nút Phải, Bit 2 = Nút Giữa; 1 = Nhấn, 0 = Nhả).
  - Byte 1 ($\Delta X$): Độ dịch chuyển tương đối trục X. Trong descriptor chuẩn, đây là số nguyên có dấu 8-bit (`int8_t`, phạm vi $-127$ đến $+127$).
  - Byte 2 ($\Delta Y$): Độ dịch chuyển tương đối trục Y (`int8_t`, phạm vi $-127$ đến $+127$).
  - Byte 3 (Wheel): Cuộn dọc (Vertical scroll, tùy chọn).
  - Byte 4 (hWheel): Cuộn ngang (Horizontal pan, tùy chọn).
  Lưu ý: Giới hạn $\pm 127$ áp dụng khi trường $\Delta X, \Delta Y$ được định nghĩa là kiểu 8-bit có dấu `int8_t` trong descriptor; firmware cần thực hiện clamping (chặn trên/dưới) để tránh tràn số trước khi đóng gói báo cáo.
- **Nguồn chứng minh**: *USB Implementations Forum, Device Class Definition for HID v1.11 §B.2 (Standard Mouse Report) & T-vK/ESP32-BLE-Mouse HID Report Descriptor*.

---

## NHÓM 11: KỊCH BẢN SỰ CỐ & DEBUG PHẦN CỨNG (FAILURE SCENARIOS)

### Câu 25: Nếu BLE đột ngột bị mất kết nối (Disconnect) thì con trỏ chuột và ESP32 xử lý thế nào?
- **Trả lời ngắn**: ESP32 dừng gửi dữ liệu lên BLE để tránh tràn bộ đệm hàng đợi, chuyển đèn LED trạng thái sang nhấp nháy tìm kiếm và phát lại gói tin quảng bá (Advertising).
- **Giải thích chuyên sâu**: Máy tính chủ khi không nhận được gói tin BLE HID sẽ tự động giữ nguyên vị trí con trỏ chuột tại điểm dừng cuối cùng. Phía ESP32, hàm `bleMouse.isConnected()` trả về `false`, mã nguồn sẽ bỏ qua bước đóng gói báo cáo và chuyển sang trạng thái chờ kết nối lại (Auto-reconnect).
- **Nguồn chứng minh**: *Bluetooth Core Specification v4.2 Vol 3 Part C (GAP Connection Management)*.

### Câu 26: Nếu nạp code mà Serial Monitor báo `WHO_AM_I = 0x00` hoặc `0xFF` thì lỗi ở đâu?
- **Trả lời ngắn**: Đây là các gợi ý chẩn đoán (diagnostic clues) cho thấy giao tiếp đọc thanh ghi I2C không thành công: có thể do mất nguồn cấp 3.3V, lỏng dây jumper SDA/SCL, sai chân cắm trên DevKit, sai địa chỉ hoặc bus bị treo.
- **Giải thích chuyên sâu**:
  - Giá trị `WHO_AM_I = 0xEA` chỉ chứng minh rằng tại thời điểm kiểm tra, giao tiếp đọc thanh ghi I2C với đúng ID thành công; nó không tự chứng minh chất lượng tín hiệu ở mọi tốc độ hay phần cứng hoàn toàn không có lỗi.
  - Trả về `0xFF`: Gợi ý đường SDA đang ở trạng thái thả nổi kéo lên mức HIGH mà không có phản hồi từ Slave (ví dụ hở mạch SDA/SCL, cảm biến mất nguồn VDD 3.3V, hoặc sai địa chỉ thiết bị).
  - Trả về `0x00`: Gợi ý đường SDA đang bị kéo giữ ở mức LOW (chạm chập mass GND, cắm nhầm chân vào hàng UART TX0/RX0, hoặc IC cảm biến bị treo trạng thái reset).
- **Nguồn chứng minh**: *I2C Bus Troubleshooting Guide & Oscilloscope Waveform Analysis*.

---

## NHÓM 12: ĐÁNH ĐỔI THIẾT KẾ (DESIGN TRADE-OFFS)

### Câu 27: Tại sao nhóm chọn giao tiếp I2C mà không chọn SPI cho phiên bản V1?
- **Trả lời ngắn**: I2C chỉ cần 2 dây tín hiệu (SDA, SCL), tiết kiệm chân vi điều khiển, dễ đấu nối trên mạch in 1 lớp và tốc độ $400\,\text{kHz}$ đáp ứng tốt chu kỳ lấy mẫu chuột $100\,\text{Hz}$.
- **Giải thích chuyên sâu**: SPI cần 4 dây (MOSI, MISO, SCK, CS), đi dây trên mạch in 1 lớp rất dễ bị cắt ngang đường và phải dùng nhiều cầu nối (jumper). Với tần số báo cáo chuột $100\,\text{Hz}$ ($10\,\text{ms}$ một lần), đọc burst 12 byte (Accel + Gyro) từ `0x2D` đến `0x38` qua I2C $400\,\text{kHz}$ chỉ mất khoảng $\approx 0.38\,\text{ms}$ (chiếm chưa tới $4\%$ chu kỳ $10\,\text{ms}$), hoàn toàn không gây nghẽn bus mà vẫn đảm bảo lấy đồng thời cả gia tốc và vận tốc góc trong cùng một giao dịch.
- **Nguồn chứng minh**: *Air Mouse Hardware Architecture Spec V3.5 §1.3*.

### Câu 28: Vì sao nhóm tự viết driver thanh ghi mỏng mà không dùng thư viện có sẵn của hãng?
- **Trả lời ngắn**: Giúp nhóm làm chủ hoàn toàn hoạt động của chip, hiểu rõ từng thanh ghi và bitfield để giải thích trước giảng viên, đồng thời tiết kiệm tài nguyên Flash/RAM do loại bỏ mã nguồn DMP không sử dụng.
- **Giải thích chuyên sâu**: Các thư viện hoàn chỉnh (như SparkFun ICM-20948) có dung lượng rất lớn vì chứa toàn bộ firmware DMP (Digital Motion Processor) vài chục kilobyte để tính toán Quaternion. Đối với chuột tương đối, việc dùng thư viện lớn là dư thừa và biến sinh viên thành người dùng "hộp đen" (black box) không giải thích được bản chất thanh ghi.
- **Nguồn chứng minh**: *Midterm Week 5 Baseline Document §5*.

### Câu 29: Nếu xoay bo mạch hoặc đổi hướng cầm 90 độ thì ánh xạ trục Gyro sang con trỏ chuột thay đổi thế nào?
- **Trả lời ngắn**: Cần hoán đổi trục (Axis Swapping) và đảo dấu (Sign Inversion) trong ma trận xoay phần mềm, ví dụ $\Delta X = -K_y \cdot \omega_y$ và $\Delta Y = K_x \cdot \omega_x$.
- **Giải thích chuyên sâu**: Cảm biến đo chuyển động theo hệ tọa độ gắn trên thân chip (Body Frame). Màn hình máy tính hiển thị theo hệ tọa độ cố định (Screen Frame). Khi thay đổi hướng lắp chip trên PCB, chỉ cần thay đổi phép ánh xạ trong hàm xử lý chuyển động: $\begin{bmatrix} \Delta X \\ \Delta Y \end{bmatrix} = \mathbf{R} \begin{bmatrix} \omega_x \\ \omega_y \\ \omega_z \end{bmatrix}$, trong đó $\mathbf{R}$ là ma trận hoán vị hướng $2 \times 3$.
- **Nguồn chứng minh**: *Coordinate Systems and Transformations in Navigation (Farrell, 2008)*.

### Câu 30: Tần số lấy mẫu (Sample Rate) và chu kỳ gửi bản tin BLE ảnh hưởng thế nào đến độ mượt và độ trễ của chuột?
- **Trả lời ngắn**: Chu kỳ gửi bản tin tối ưu là $10\,\text{ms}$ (tương ứng tần số báo cáo $100\,\text{Hz}$), mang lại độ trễ đủ nhỏ cho mắt người không nhận thấy khựng giật, đồng thời không làm quá tải băng thông BLE.
- **Giải thích chuyên sâu**: Mắt người bắt đầu cảm nhận độ mượt ở tần số quét màn hình $\ge 60\,\text{Hz}$. Chuột máy tính văn phòng chuẩn thường gửi báo cáo ở $100\text{--}125\,\text{Hz}$. Nếu gửi quá chậm ($<30\,\text{Hz}$), con trỏ sẽ bị giật cục (stuttering). Nếu gửi quá nhanh ($>500\,\text{Hz}$), ngăn xếp BLE trên ESP32 sẽ bị nghẽn bộ đệm và tiêu tốn nhiều năng lượng vô ích.
- **Nguồn chứng minh**: *Human-Computer Interaction: Pointing Performance and Display Refresh Rates (ISO 9241-9)*.

### Câu 31: Mối liên hệ giữa tần số cắt bộ lọc DLPF ($51.2\,\text{Hz}$) và tần số lấy mẫu ($100\,\text{Hz}$) theo định lý Nyquist là gì?
- **Trả lời ngắn**: Định lý Nyquist-Shannon yêu cầu tần số lấy mẫu $f_s$ phải lớn hơn ít nhất 2 lần tần số thành phần cao nhất của tín hiệu ($f_{\max} < f_s / 2$). Với ODR $\approx 102.27\,\text{Hz}$ ($f_N \approx 51.1\,\text{Hz}$), bộ lọc DLPF phần cứng băng thông $3\text{dB} \approx 51.2\,\text{Hz}$ giúp suy giảm đáng kể hiện tượng chồng phổ (Aliasing), tuy nhiên không triệt tiêu hoàn toàn do đặc tuyến lọc có độ dốc suy hao hữu hạn.
- **Giải thích chuyên sâu**:
  Hệ thống bao gồm 4 miền thời gian/tần số riêng biệt cần phân biệt rõ:
  1. *Đường lấy mẫu sơ cấp nội bộ cảm biến*: Tín hiệu cơ học qua bộ lọc tương tự sơ cấp trước ADC nội (~1.1 kHz).
  2. *Tốc độ xuất dữ liệu của Gyro (ODR)*: Cấu hình qua `GYRO_SMPLRT_DIV = 10` cho ra $f_{\text{ODR}} = 1125 / (1 + 10) \approx 102.27\,\text{Hz}$. Tần số Nyquist tương ứng là $f_N = f_{\text{ODR}} / 2 \approx 51.1\,\text{Hz}$.
  3. *Chu kỳ vòng lặp Firmware*: Đọc dữ liệu định kỳ qua I2C mỗi $10\,\text{ms}$ ($100\,\text{Hz}$).
  4. *Chu kỳ gửi gói tin BLE HID (Connection Interval)*: Gửi báo cáo định kỳ $10\text{--}15\,\text{ms}$ lên máy tính chủ.

  Vì bộ lọc DLPF phần cứng cấu hình `GYRO_DLPFCFG = 3` có $3\text{dB Bandwidth} \approx 51.2\,\text{Hz}$ và Noise Bandwidth $\approx 73.3\,\text{Hz}$, tín hiệu ở lân cận tần số Nyquist ($51.1\,\text{Hz}$) chỉ bị suy giảm khoảng $3\,\text{dB}$, do đó một phần năng lượng nhiễu tần số cao vẫn có thể gập phổ vào băng thông đo. Nhóm xác định 2 phương án đánh đổi kỹ thuật khi thử nghiệm firmware:
  - *Phương án A*: Giữ DLPF $51.2\,\text{Hz}$ và tăng Gyro ODR lên cao hơn ($\approx 200\,\text{Hz}$ hoặc $1.1\,\text{kHz}$) để đưa tần số Nyquist lên trên $100\,\text{Hz}$, tạo biên an toàn chống chồng phổ rộng hơn.
  - *Phương án B*: Giữ Gyro ODR ở mức $\approx 100\,\text{Hz}$ và chuyển cấu hình DLPF sang tần số cắt thấp hơn (ví dụ $23.9\,\text{Hz}$ hoặc $11.6\,\text{Hz}$) để độ suy hao tại mốc Nyquist $50\,\text{Hz}$ đạt mức cao hơn, đánh đổi lại độ trễ pha tăng nhẹ.
- **Nguồn chứng minh**: *TDK InvenSense ICM-20948 Datasheet, Register Map and Descriptions DS-000189 §14.2 & Oppenheim & Schafer, "Discrete-Time Signal Processing"*.

### Câu 32: Khi nào thì giải thuật dung hợp cảm biến Complementary Filter hoặc Kalman Filter mới thực sự cần thiết?
- **Trả lời ngắn**: Bộ lọc bù Complementary Quaternion 6 trục ($K=2.0\,\text{s}^{-1}$) đã được triển khai trong firmware để ước lượng tư thế Roll/Pitch và thích nghi hệ quy chiếu cầm tay; tuy nhiên nhóm chủ động KHÔNG triển khai Kalman Filter (EKF) vì độ phức tạp ma trận không cần thiết và gây trễ tính toán.
- **Giải thích chuyên sâu**: Gia tốc kế đo được vector trọng trường $1g$, qua hàm lượng giác tính được góc Roll và Pitch tuyệt đối nhưng rất nhạy cảm với rung động tức thời. Gyroscope đo góc mượt mà nhưng bị trôi tích lũy khi tích phân theo thời gian. Firmware của nhóm đã triển khai thuật toán **6-axis Complementary Quaternion Filter** (`CODE_IMPLEMENTED + HOST_TESTED`): dùng quaternion để biểu diễn tư thế không bị khóa góc Gimbal Lock, bù nghiêng với hệ số tốc độ $K = 2.0\,\text{s}^{-1}$ ($\tau \approx 0.5\,\text{s}$), tự động điều chỉnh hệ quy chiếu tham chiếu (Adaptive Reference Frame) và hỗ trợ cơ chế Clutch/Recenter. Nhóm chủ động không triển khai thuật toán Kalman Filter (EKF) vì đòi hỏi nhân nghịch đảo ma trận $4\times 4$ hoặc $7\times 7$ liên tục trong mỗi chu kỳ lấy mẫu, làm tăng độ trễ tính toán không cần thiết cho một thiết bị trỏ tốc độ cao đòi hỏi đáp ứng tức thời.
- **Nguồn chứng minh**: *Welch & Bishop, "An Introduction to the Kalman Filter", UNC Chapel Hill & Madgwick, "An efficient orientation filter for inertial and inertial/magnetic sensor arrays"*.

### Câu 33: Vì sao nhóm sử dụng thư viện `Wire.h` của Arduino Core thay vì lập trình thanh ghi trực tiếp của I2C Controller trên ESP32?
- **Trả lời ngắn**: `Wire.h` là thư viện trừu tượng hóa chuẩn (HAL) đã được Espressif tối ưu hóa ngắt phần cứng, quản lý buffer FIFO và xử lý lỗi I2C State Machine an toàn; nhóm tập trung giải thích thanh ghi của cảm biến ICM-20948 là mục tiêu cốt lõi của đồ án.
- **Giải thích chuyên sâu**: Giao thức I2C trên ESP32 bao gồm hệ thống thanh ghi cấu hình chân phức tạp (GPIO Matrix, Clock Div, Command FIFO, Timeout). Thao tác trực tiếp thanh ghi nội ESP32 làm mã nguồn cồng kềnh hàng trăm dòng mà không đem lại giá trị học thuật thêm, trong khi việc tự viết driver thanh ghi cho thiết bị ngoại vi ICM-20948 đã thể hiện đầy đủ năng lực giao tiếp phần cứng nhúng.
- **Nguồn chứng minh**: *Espressif ESP32 Technical Reference Manual §11 (I2C Controller)*.

### Câu 34: Tại sao module WCMCU-20948 nối trực tiếp 3,3 V khi datasheet IC trần ghi VDDIO tối đa 1,95 V?
- **Trả lời ngắn**: Nhóm chọn nối trực tiếp 3,3 V trên đúng module WCMCU-20948 mà nhóm đang sở hữu và đã kiểm chứng chức năng thực nghiệm bằng ACK 0x68, WHO_AM_I = 0xEA, register readback vật lý thành công và đọc luồng dữ liệu 12 byte thực tế. Đây là kết quả thực nghiệm trên bàn (bench-test) của module cụ thể, không phải khẳng định chung cho mọi breakout ICM-20948.
- **Giải thích chuyên sâu**: Datasheet TDK InvenSense DS-000189 quy định VDDIO của IC trần là 1.71–1.95 V. Tuy nhiên, trên bo mạch breakout thương phẩm WCMCU-20948 cụ thể của nhóm, việc kết nối trực tiếp vào rail 3.3V của ESP32 đã hoạt động ổn định trong các bài test 100 lần đọc ở cả 100 kHz và 400 kHz Fast-Mode. Quyết định loại bỏ BSS138 và LDO 1.8V giúp đơn giản hóa mạch in 1 lớp, loại trừ các mối tiếp xúc chập chờn của module phụ và hạ thấp chi phí phần cứng. Nhóm giữ nguyên phân tích datasheet như một tài liệu đối sánh học thuật và ghi nhận ranh giới thực nghiệm rõ ràng.
- **Nguồn chứng minh**: *TDK InvenSense DS-000189 §3.4 (dải hoạt động VDD 1.71–3.6 V, VDDIO 1.71–1.95 V) & §3.7 (giới hạn tuyệt đối VDDIO 2.5 V) & Báo cáo thực nghiệm docs/HARDWARE_BRINGUP_DIRECT_3V3_2026-09-25.md*.

### Câu 35: Dung lượng và dòng phóng của pin LiPo 1S ảnh hưởng ra sao đến thời lượng vận hành của ESP32?
- **Trả lời ngắn**: ESP32 khi bật BLE tiêu thụ dòng điện trung bình khoảng $50\text{--}80\,\text{mA}$; pin LiPo 1S dung lượng $500\,\text{mAh}$ có thể duy trì hoạt động liên tục từ $6\text{--}8\,\text{giờ}$.
- **Giải thích chuyên sâu**: Khi gửi gói tin BLE định kỳ $10\,\text{ms}$, modem vô tuyến phát sóng trong vài trăm micro-giây với dòng đỉnh $\approx 130\,\text{mA}$, sau đó trở về trạng thái nghỉ tiêu thụ thấp. Mạch nâng áp MT3608 có hiệu suất khoảng $85\text{--}90\%$, chuyển đổi điện áp pin $3.7\,\text{V}$ lên $5\,\text{V}$ cấp vào chân VIN của ESP32 DevKit, đảm bảo hệ thống vận hành ổn định suốt chu kỳ xả của pin ($4.2\,\text{V} \rightarrow 3.2\,\text{V}$).
- **Nguồn chứng minh**: *Espressif ESP32 Power Consumption Analysis (User Guide §RF Current)*.

### Câu 36: Trong cấu hình BLE HID, sự khác nhau giữa chu kỳ quảng bá (Advertising Interval) và chu kỳ kết nối (Connection Interval) là gì?
- **Trả lời ngắn**: Advertising Interval dùng khi chuột chưa kết nối để máy tính quét thấy thiết bị; Connection Interval là chu kỳ gửi nhận gói tin định kỳ sau khi chuột và máy tính đã thiết lập kết nối thành công.
- **Giải thích chuyên sâu**:
  - *Advertising Interval* đặt khoảng $50\text{--}100\,\text{ms}$ để máy tính nhanh chóng dò thấy Air Mouse mà không tốn pin.
  - *Connection Interval* quyết định tốc độ phản hồi của chuột: Bluetooth SIG quy định khoảng thời gian kết nối cho thiết bị HID từ $7.5\,\text{ms}$ đến $15\,\text{ms}$ để đảm bảo độ trễ thấp và di chuyển con trỏ mượt mà.
- **Nguồn chứng minh**: *Bluetooth SIG Core Specification v4.2 Vol 6 Part B (Link Layer Specification)*.

