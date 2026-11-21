# DANH MỤC KHOẢNG TRỐNG NGHIÊN CỨU & QUYẾT ĐỊNH KỸ THUẬT HYBRID AIR MOUSE (RG-01 ĐẾN RG-13)
## DỰ ÁN: AIR MOUSE BLE HID (ESP32 + ICM-20948)

> **Dự án**: Chuột bay không gian không dây (Air Mouse BLE HID)  
> **Kiến trúc**: Hybrid 9-Axis Air Mouse  
> **Phiên bản**: V2.0.0 — Canonical Research Gap Matrix  
> **Tài liệu tham chiếu gốc**: TDK InvenSense DS-000189, Espressif ESP32 TRM, Bluetooth HOGP Spec.  

---

## 1. Bảng Tổng Hợp Trạng Thái 13 Khoảng Trống Kỹ Thuật (RG Matrix)

| Mã RG | Chủ đề nghiên cứu | Trạng thái kỹ thuật | Mức độ ưu tiên | Kết luận / Hướng xử lý chính thức |
| :---: | :--- | :---: | :---: | :--- |
| **RG-01** | Bù sai số độ lệch tĩnh Gyro (Zero-rate Bias) | `CODE IMPLEMENTED` | **P0** (Sống còn) | Lấy trung bình 200 lần polling ($10\,\text{ms}$ delay, $2.0\,\text{s}$) lúc khởi động tĩnh để trừ offset. |
| **RG-02** | Nhận diện trạng thái đứng yên (Stationary Detection) | `CODE IMPLEMENTED` | **P0** (Sống còn) | Điều kiện kết hợp: $\|\vec{\omega}\| < 1.2\,\text{dps}$ VÀ $|\|\vec{a}\| - 1.0g| < 0.08g$ trong $300\,\text{ms}$. |
| **RG-03** | Chuột hướng tùy ý / chĩa lên trời (Arbitrary Orientation) | `CODE IMPLEMENTED` | **P1** (Trọng tâm) | Nhận diện vector trọng lực, chiếu vận tốc góc sang mặt phẳng điều khiển tham chiếu. |
| **RG-04** | Thiết lập khung tọa độ tham chiếu (Reference Frame) | `CODE IMPLEMENTED` | **P1** (Trọng tâm) | Chụp lại Quaternion hướng trọng trường khi nhả nút `BTN_MODE` (Clutch Recenter). |
| **RG-05** | Thuật toán dung hợp cảm biến (Sensor Fusion Choice) | `VERIFIED` | **P1** | Chọn bộ lọc bù 6-trục (6-Axis Complementary / Tilt Filter). Đơn giản, tin cậy, không dùng EKF/DMP phức tạp đêm nay. |
| **RG-06** | Đánh giá giá trị thực tế của Từ kế (Magnetometer AK09916) | `PROJECT DECISION` | **P1 / OPTIONAL** | Tạm khóa ở P0; tránh nhiễu từ tính laptop/kim loại bàn học. Giải thích trung thực trước giảng viên. |
| **RG-07** | Nhận dạng cử chỉ vung tịnh tiến (Flick Gesture Recognition) | `CODE IMPLEMENTED` | **P0** | Máy trạng thái nhận dạng xung gia tốc 2 pha (Vung đi + Giật lại) trên trục ngang khi giữ `BTN_MODE`. |
| **RG-08** | Chống kích hoạt nhầm cử chỉ (False Gesture Rejection) | `CODE IMPLEMENTED` | **P0** | Đặt cửa sổ thời gian ($60\text{--}450\,\text{ms}$), ngưỡng gia tốc đối kháng, và thời gian trễ Cooldown $350\,\text{ms}$. |
| **RG-09** | Hỗ trợ nút Back/Forward trên giao thức BLE HID Mouse | `VERIFIED` | **P0** | Sử dụng HID Mouse Button 4 (Back) và Button 5 (Forward); fallback gửi tổ hợp phím Alt+Left/Right nếu cần. |
| **RG-10** | Đồng bộ nhịp ODR, DLPF và độ trễ báo cáo BLE | `VERIFIED` | **P0** | Cảm biến ODR $\approx 102.27\,\text{Hz}$ (DIV=10), DLPF $51.2\,\text{Hz}$, chu kỳ báo cáo BLE $\approx 10\text{--}15\,\text{ms}$. |
| **RG-11** | Bù trôi nhiệt độ (Temperature Effects) | `PROJECT DECISION` | **P1** | Không dùng bảng tra nhiệt phức tạp; giải quyết bằng Online Auto-Zero thích nghi khi đứng yên. |
| **RG-12** | Ánh xạ trục cảm biến sang tọa độ con trỏ màn hình | `VERIFIED` | **P0** | $\Delta X = +K_x \cdot \omega_{\text{yaw}}$, $\Delta Y = -K_y \cdot \omega_{\text{pitch}}$ (trục màn hình máy tính hướng xuống là $+Y$). |
| **RG-13** | Khớp nối trục vật lý PCB và vị trí hàn module WCMCU-20948 | `NEEDS HARDWARE TEST` | **P0** | Kiểm tra chiều cắm thực tế của module IMU trên socket cái của Carrier Board. |

---

## 2. Chi Tiết 13 Khoảng Trống Nghiên Cứu (Detailed RG Breakdowns)

### RG-01: Gyro Zero-Rate Bias & Drift Control
- **Câu hỏi**: Làm thế nào để loại bỏ sai số lệch tĩnh (zero-rate offset) của con quay hồi chuyển khiến chuột tự chạy?
- **Tầm quan trọng**: Sống còn. Nếu không bù offset, con trỏ chuột liên tục phi hết tốc lực vào góc màn hình máy tính.
- **Bằng chứng hiện tại**: TDK DS-000189 §3.1 quy định zero-rate output danh định ở $25^\circ\text{C}$ có thể lên tới $\pm 5\,\text{dps}$ ($\approx \pm 327\,\text{LSB}$ ở thang $\pm 500\,\text{dps}$).
- **Nguồn tài liệu**: TDK InvenSense ICM-20948 Datasheet DS-000189 v1.5 §3.1 Table 1.
- **Quyết định thiết kế**: Khi bật nguồn, giữ thiết bị bất động trong 2 giây đầu tiên, đọc 200 lần polling (chu kỳ danh định $10\,\text{ms}$) và tính trung bình cộng để lưu làm `gyro_bias_x, gyro_bias_y, gyro_bias_z`.
- **Trạng thái**: `CODE IMPLEMENTED`.
- **Kiểm nghiệm yêu cầu**: Bật nguồn khi đặt chuột trên bàn; quan sát Serial Monitor hiển thị 3 giá trị bias được trừ về 0.

### RG-02: Stationary Detection (Nhận diện trạng thái đứng yên)
- **Câu hỏi**: Làm sao để chuột biết người dùng đã dừng tay và cố định con trỏ chuột tuyệt đối?
- **Tầm quan trọng**: Sống còn. Ngăn chặn hiện tượng con trỏ chuột bị trôi vi mô (creep) do rung tay sinh lý ($1\text{--}3\,\text{Hz}$) hoặc làm tròn số nguyên.
- **Bằng chứng hiện tại**: Khi tay đặt cố định, $\|\vec{\omega}\| \approx 0$ và độ lớn vector gia tốc $\|\vec{a}\| \approx 1.0g$ (thuần túy là trọng lực Trái Đất).
- **Nguồn tài liệu**: STMicroelectronics AN4503, InvenSense MotionApps Guide.
- **Quyết định thiết kế**: Kết hợp đồng thời 2 điều kiện: $\|\vec{\omega}\| < 1.2\,\text{dps}$ VÀ $|\|\vec{a}\| - 1.0g| < 0.08g$. Nếu thỏa mãn liên tục trong 30 mẫu ($\ge 300\,\text{ms}$), kích hoạt cờ `is_stationary = true` và ép ngõ ra chuột $\Delta X = 0, \Delta Y = 0$.
- **Trạng thái**: `CODE IMPLEMENTED`.
- **Kiểm nghiệm yêu cầu**: Đặt chuột nằm yên trên bàn 30 giây; quan sát con trỏ không được di chuyển dù chỉ 1 pixel.

### RG-03: Arbitrary Orientation & Pointing Upward (Chuột chĩa lên trời)
- **Câu hỏi**: Khi người dùng ngả lưng tựa ghế và chĩa đầu chuột lên trời, hướng rê chuột có bị đảo lộn không?
- **Tầm quan trọng**: Rất cao. Giảng viên đã trực tiếp đặt câu hỏi này trên lớp. Nếu gán cứng trục ($dX = \omega_z, dY = -\omega_y$), khi chĩa lên trời trục $Z$ quay ngang, lắc ngang biến thành gật dọc.
- **Bằng chứng hiện tại**: Trọng lực Trái Đất $\vec{g}$ là vector mốc tuyệt đối luôn trỏ xuống đất, đo được qua gia tốc kế.
- **Nguồn tài liệu**: Farooq et al., "Attitude Estimation for Handheld Devices Using MEMS IMU", IEEE Sensors.
- **Quyết định thiết kế**: Sử dụng gia tốc kế đo hướng vector trọng trường cục bộ tại tư thế hiện tại, tính Quaternion xoay để biến đổi vận tốc góc từ hệ trục thân cảm biến sang mặt phẳng điều khiển ngang/dọc trực quan đối với mắt nhìn người dùng.
- **Trạng thái**: `CODE IMPLEMENTED`.
- **Kiểm nghiệm yêu cầu**: Bấm giữ `BTN_MODE`, chĩa chuột thẳng đứng lên trời, nhả nút; lắc cổ tay sang hai bên và xác nhận con trỏ chuột di chuyển ngang màn hình máy tính.

### RG-04: Reference Coordinate Frame & Clutch Recenter (Khung tham chiếu & Ly hợp)
- **Câu hỏi**: Người dùng làm thế nào để thay đổi tư thế cầm chuột thoải mái nhất mà không làm sai lệch con trỏ?
- **Tầm quan trọng**: Cao. Tạo trải nghiệm tự do tương tự chuột bay cao cấp (Gyration / Logitech MX Air).
- **Bằng chứng hiện tại**: Các thiết bị thương mại đều có phím ngắt chuột (Clutch Button) để nhấc tay và định vị lại góc điều khiển.
- **Nguồn tài liệu**: US Patent US7236156B2 ("Handheld pointing device with clutching mechanism").
- **Quyết định thiết kế**: Bấm giữ `BTN_MODE` (`GPIO27`) để khóa chuyển động chuột; khi người dùng nhả nút (nếu không có cử chỉ flick), hệ thống chụp lại hướng trọng trường làm tư thế tham chiếu mới.
- **Trạng thái**: `CODE IMPLEMENTED`.
- **Kiểm nghiệm yêu cầu**: Bấm giữ `BTN_MODE`, nghiêng chuột $45^\circ$, nhả nút; kiểm tra tính ổn định của hướng điều khiển.

### RG-05: Sensor Fusion Algorithm Comparison (So sánh giải thuật dung hợp cảm biến)
- **Câu hỏi**: Chọn thuật toán dung hợp cảm biến nào cho đề tài giữa kỳ?
- **Tầm quan trọng**: Tránh bẫy quá mức (Over-engineering).
- **Bằng chứng hiện tại**: 
  - *EKF (Extended Kalman Filter)*: Tốn bộ nhớ và CPU, phức tạp trong việc giải thích ma trận hiệp phương sai trước giảng viên, dễ mất hội tụ nếu khởi tạo sai.
  - *DMP (Digital Motion Processor nội của ICM-20948)*: Yêu cầu nạp firmware nhị phân độc quyền (proprietary binary blob $>14\,\text{KB}$) qua I2C, không thể hiện được phong cách lập trình semi-register, rủi ro lỗi nạp cao đêm nay.
  - *Madgwick / Mahony*: Tốt nhưng chủ yếu phục vụ định vị tuyệt đối 9-DOF.
  - *6-Axis Tilt / Gravity Complementary Filter*: Cực kỳ gọn nhẹ ($<50$ dòng code), chạy êm trên ESP32 ($<0.5\,\text{ms}$), trực quan, dễ bảo vệ thuyết phục trước giảng viên môn Hệ thống nhúng.
- **Nguồn tài liệu**: TDK DS-000189; Higgins, "Comparison of complementary and Kalman filtering".
- **Quyết định thiết kế**: Chọn **6-Axis Gravity Vector Extraction via Low-Pass Filter** làm giải pháp cốt lõi cho V2 P0/P1.
- **Trạng thái**: `VERIFIED` & `PROJECT DECISION`.
- **Kiểm nghiệm yêu cầu**: Chạy benchmark tính toán thời gian thực trên ESP32.

### RG-06: Magnetometer Indoors (Từ kế AK09916 trong nhà)
- **Câu hỏi**: Có nên kích hoạt và đọc từ kế 3 trục AK09916 trong buổi bảo vệ giữa kỳ ngày mai không?
- **Tầm quan trọng**: Cao. Tránh rủi ro trôi giật con trỏ chuột trước hội đồng.
- **Bằng chứng hiện tại**: Trong phòng thí nghiệm/phòng học có nhiều nhiễu từ trường cứng và mềm (khung sắt bàn học, nam châm loa laptop, nguồn xung màn hình). Nếu không được hiệu chuẩn bằng thuật toán Ellipsoid Fitting phức tạp, từ kế sẽ xuất dữ liệu méo mó, làm lệch hướng điều khiển.
- **Nguồn tài liệu**: InvenSense AN-000143 ("Hard and Soft Iron Calibration").
- **Quyết định thiết kế**: **KHÓA TỪ KẾ Ở MỨC P1 / OPTIONAL**. Trình bày trung thực: *"ICM-20948 là chip 9-DOF có sẵn từ kế để mở rộng trong tương lai; tuy nhiên trong phiên bản V1/V2 giữa kỳ, nhóm sử dụng 6 trục Gyro + Accel để đảm bảo độ tin cậy tuyệt đối trước môi trường nhiễu từ tính trong phòng học."*
- **Trạng thái**: `PROJECT DECISION`.
- **Kiểm nghiệm yêu cầu**: Phân tích mạch I2C Master nội trong bài báo cáo.

### RG-07: Translational Flick Gestures (Nhận dạng cử chỉ vung tịnh tiến)
- **Câu hỏi**: Làm thế nào để nhận diện cử chỉ vung chuột sang trái (Back) và vung sang phải (Forward)?
- **Tầm quan trọng**: Tính năng tạo điểm nhấn công nghệ cho đề tài (UX differentiator).
- **Bằng chứng hiện tại**: Cử chỉ vung tay có đặc trưng: Gia tốc tăng vọt theo một hướng, đạt đỉnh, sau đó xuất hiện gia tốc đối kháng để hãm tay lại trong khoảng thời gian $150\text{--}400\,\text{ms}$.
- **Nguồn tài liệu**: Wobbrock et al., "Gestures without libraries: Toolkits for gesture recognition", ACM UIST.
- **Quyết định thiết kế**: Triển khai máy trạng thái 5 bước: `IDLE` $\rightarrow$ `ARMED` (khi giữ `BTN_MODE`) $\rightarrow$ `PEAK_DETECTED` (khi $|a_y| > 1.2g$) $\rightarrow$ `RETURN_DETECTED` (gia tốc đảo chiều) $\rightarrow$ `VALID_GESTURE` (gửi lệnh HID).
- **Trạng thái**: `CODE IMPLEMENTED`.
- **Kiểm nghiệm yêu cầu**: Vung tay nhanh sang trái khi giữ nút Mode; xác nhận trình duyệt chuyển về trang trước (History Back).

### RG-08: False Gesture Rejection (Chống kích hoạt nhầm cử chỉ)
- **Câu hỏi**: Làm thế nào để phân biệt giữa việc người dùng xoay đổi tư thế cầm (Recenter) và việc vung tay thực hiện cử chỉ (Flick)?
- **Tầm quan trọng**: Ngăn ngừa trải nghiệm tồi tệ khi đổi tư thế cầm mà vô tình bị Back/Forward trang web.
- **Bằng chứng hiện tại**: Thao tác đổi tư thế cầm diễn ra êm và chậm ($|a| < 0.4g$), trong khi cử chỉ flick có gia tốc đỉnh rất lớn ($|a| > 1.2g$).
- **Quyết định thiết kế**: Thiết lập ngưỡng phân tách: Gia tốc vung tay phải vượt ngưỡng $1.2g$, có pha giật về ngược chiều rõ ràng trong vòng $400\,\text{ms}$. Nếu chuyển động êm dịu, cử chỉ bị bỏ qua và hệ thống chuyển sang chế độ Recenter. Thời gian trễ phục hồi (Cooldown) sau mỗi cử chỉ là $350\,\text{ms}$.
- **Trạng thái**: `CODE IMPLEMENTED`.
- **Kiểm nghiệm yêu cầu**: Xoay đổi tư thế cầm chuột thật chậm; xác nhận không có bất kỳ lệnh Back/Forward nào bị kích hoạt nhầm.

### RG-09: BLE HID Back/Forward Support
- **Câu hỏi**: Ngăn xếp BLE HID Mouse có hỗ trợ nút Back/Forward không?
- **Tầm quan trọng**: Quyết định mã lệnh gửi về máy tính.
- **Bằng chứng hiện tại**: Chuẩn USB HID Pointing Device Descriptor và thư viện `BleMouse` trên Arduino-ESP32 hỗ trợ 5 nút chuột tiêu chuẩn: Button 1 (Left), Button 2 (Right), Button 3 (Middle), Button 4 (Back), Button 5 (Forward).
- **Nguồn tài liệu**: USB-IF HID Usage Tables §12 (Generic Desktop Page) & Button Page; `BleMouse.h` source code.
- **Quyết định thiết kế**: Gọi hàm `bleMouse.click(MOUSE_BACK)` (tương đương `MOUSE_BUTTON4 = 0x08`) và `bleMouse.click(MOUSE_FORWARD)` (tương đương `MOUSE_BUTTON5 = 0x10`).
- **Trạng thái**: `VERIFIED`.
- **Kiểm nghiệm yêu cầu**: Mở trình duyệt web Chrome/Edge, thực hiện cử chỉ và xác nhận trang web chuyển Back/Forward.

### RG-10: Sample Rate (ODR), DLPF & BLE Latency Synchronization
- **Câu hỏi**: Tần số đọc cảm biến, tần số bộ lọc và tần số gửi bản tin BLE phối hợp như thế nào?
- **Tầm quan trọng**: Tránh nghẽn hàng đợi BLE hoặc méo tín hiệu do lấy mẫu sai nhịp.
- **Bằng chứng hiện tại**: Ngăn xếp BLE GATT có khoảng thời gian kết nối (Connection Interval) danh định từ $7.5\,\text{ms}$ đến $15\,\text{ms}$ đối với thiết bị chuột HID tốc độ cao.
- **Nguồn tài liệu**: Bluetooth Core Specification v4.2 §Vol 6 Part B §4.5.1; ICM-20948 DS-000189 §10.1.
- **Quyết định thiết kế**:
  - Tần số ngõ ra cảm biến ODR: $1125\,\text{Hz} / (1 + 10) \approx 102.27\,\text{Hz}$ (được định bởi `GYRO_SMPLRT_DIV = 10`).
  - Bộ lọc số phần cứng DLPF: $51.2\,\text{Hz}$ (thỏa mãn tiêu chuẩn định lý lấy mẫu Nyquist: $f_{\text{DLPF}} \approx \frac{1}{2} \text{ODR}$).
  - Chu kỳ vòng lặp chính của ESP32: $10\,\text{ms}$ ($100\,\text{Hz}$), gửi báo cáo BLE mỗi chu kỳ hoặc khi có sự thay đổi tọa độ.
- **Trạng thái**: `VERIFIED`.
- **Kiểm nghiệm yêu cầu**: Đo chu kỳ vòng lặp bằng hàm `micros()` trên ESP32.

### RG-11: Temperature Effects on Gyro Bias
- **Câu hỏi**: Nhiệt độ sinh ra từ chip ESP32 và module tăng áp có làm trôi con quay hồi chuyển theo thời gian không?
- **Tầm quan trọng**: Trung bình. ESP32 phát sóng BLE có thể nóng lên từ $25^\circ\text{C}$ lên $40^\circ\text{C}$ sau 15 phút.
- **Bằng chứng hiện tại**: Datasheet ICM-20948 ghi nhận hệ số trôi nhiệt của Gyro là $\pm 0.05\,\text{dps}/^\circ\text{C}$. Độ chênh nhiệt $15^\circ\text{C}$ tạo ra độ lệch $\approx 0.75\,\text{dps}$.
- **Nguồn tài liệu**: TDK DS-000189 §3.1 Table 1.
- **Quyết định thiết kế**: Ngưỡng vùng chết `DEADZONE_LOW = 0.8 dps` kết hợp bộ nhận diện đứng yên `Stationary Auto-Zero` thích nghi sẽ tự động triệt tiêu trôi dạt nhiệt này mà không cần xây dựng bảng bù nhiệt phức tạp.
- **Trạng thái**: `PROJECT DECISION`.
- **Kiểm nghiệm yêu cầu**: Để chuột chạy liên tục 20 phút, kiểm tra xem con trỏ có bắt đầu trôi hay không.

### RG-12: Coordinate Mapping & Sign Conventions
- **Câu hỏi**: Quy ước dấu và phép gán trục giữa con quay hồi chuyển và tọa độ màn hình máy tính được thiết lập như thế nào?
- **Tầm quan trọng**: Sống còn. Nếu nhầm dấu, rê chuột sang phải con trỏ sẽ bay sang trái, hoặc gật tay lên con trỏ lại cắm xuống dưới.
- **Bằng chứng hiện tại**: Màn hình đồ họa máy tính có gốc tọa độ $(0, 0)$ ở góc trên bên trái: chiều sang phải là $+X$, chiều đi xuống là $+Y$.
- **Quyết định thiết kế**:
  - Chuyển động lắc cổ tay sang PHẢI (Yaw Right) tạo $\omega_z > 0 \rightarrow \Delta X > 0$.
  - Chuyển động gật cổ tay LÊN TRÊN (Pitch Up) tạo $\omega_y > 0 \rightarrow$ con trỏ cần đi lên ($\Delta Y < 0$), do đó $\Delta Y = -K_y \cdot \omega_y$.
- **Trạng thái**: `VERIFIED`.
- **Kiểm nghiệm yêu cầu**: Test trực tiếp hướng rê chuột trên màn hình máy tính.

### RG-13: PCB Mounting & Module Header Orientation
- **Câu hỏi**: Vị trí hàn socket cái của module WCMCU-20948 trên Carrier Board có khớp với giả định trục không?
- **Tầm quan trọng**: Cần xác nhận khi cắm linh kiện thật.
- **Bằng chứng hiện tại**: Module WCMCU-20948 cắm vào hàng chân socket $1\times 10$ đặt ở phía đầu bo mạch, mặt linh kiện ngửa lên trên.
- **Quyết định thiết kế**: Định nghĩa các hằng số đổi trục trong file cấu hình phần mềm (`AXIS_SWAP_XY`, `INVERT_X`, `INVERT_Y`) để dễ dàng đảo chiều nếu cắm ngược mà không cần hàn lại mạch.
- **Trạng thái**: `NEEDS HARDWARE TEST`.
- **Kiểm nghiệm yêu cầu**: Kiểm tra nhãn in mũi tên $X, Y$ trên vỏ chip ICM-20948 đối chiếu với hướng tiến của Carrier Board.
