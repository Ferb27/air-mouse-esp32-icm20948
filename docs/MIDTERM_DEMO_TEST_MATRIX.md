# MA TRẬN KIỂM CHỨNG & ĐO ĐẠC THỰC NGHIỆM GIỮA KỲ (MIDTERM DEMO TEST MATRIX)
## DỰ ÁN: AIR MOUSE BLE HID (ESP32 + ICM-20948)

> **Môn học**: Hệ thống nhúng (Embedded Systems) — Báo cáo Giữa kỳ Tuần 5  
> **Kiến trúc**: Hybrid 9-Axis Air Mouse  
> **Quy tắc ghi nhận**: Tuyệt đối trung thực kỹ thuật. Nếu chưa cắm phần cứng thật, ghi rõ `NEEDS HARDWARE TEST` hoặc `SIMULATION VERIFIED`; tuyệt đối **KHÔNG TỰ BỊA KẾT QUẢ PASS**.  

---

## 1. Bảng Ma Trận 10 Bài Đo Kiểm Nghiệm (Hardware & Interaction Verification)

| Mã Test | Tên bài kiểm tra | Thao tác thực hiện | Kết quả kỳ vọng (Expected) | Kết quả thực tế (Actual) | Đánh giá (Status) | Ghi chú kỹ thuật |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **TEST 1** | Độ ổn định tĩnh & Chống trôi (Stationary Anti-Drift) | Đặt thiết bị nằm yên trên mặt bàn phẳng trong $30\,\text{s}$ sau khi khởi động. | Con trỏ chuột không dịch chuyển dù chỉ $1\,\text{pixel}$ trên màn hình máy tính ($\Delta X = 0, \Delta Y = 0$). | Thuật toán đã mô phỏng đạt 0 creep; cần đo đạc thực nghiệm khi cắm bo mạch thật. | `NEEDS HARDWARE TEST` | Kiểm chứng hiệu quả của Startup Bias Calibration + Stationary Auto-Zero. |
| **TEST 2** | Độ nhạy xoay có chủ đích (Deliberate Small Rotation) | Lắc nhẹ cổ tay sang phải và gật nhẹ lên trên với vận tốc góc $>2^{\circ}/\text{s}$. | Con trỏ chuột lập tức dịch chuyển mượt mà sang phải và lên trên tương ứng với chuyển động tay. | Đã kiểm chứng công thức ánh xạ và vùng chết trên testbench C++; cần nạp board thật. | `NEEDS HARDWARE TEST` | Kiểm chứng vượt qua ngưỡng Dead-zone ($0.8^{\circ}/\text{s}$) và độ nhạy con trỏ. |
| **TEST 3** | Dừng chuyển động tức thời (Motion Stop & Settle) | Đang rê chuột nhanh thì đột ngột dừng cổ tay lại giữa không trung. | Con trỏ chuột dừng lại ngay lập tức, không bị văng trớn hay dao động giật cục. | Đã kiểm chứng phản hồi bộ lọc DLPF $51.2\,\text{Hz}$ trễ thấp ($5.9\,\text{ms}$). | `NEEDS HARDWARE TEST` | Chứng minh ưu điểm của Rate-Control so với các giải pháp tích phân góc Euler. |
| **TEST 4** | Khóa ly hợp đóng băng con trỏ (Clutch Freeze) | Nhấn và giữ nút `BTN_MODE` (`GPIO27`) trong khi vẫn tiếp tục vung cổ tay. | Con trỏ chuột hoàn toàn đóng băng tại chỗ, không gửi bất kỳ bản tin $\Delta X, \Delta Y$ nào. | Logic phần mềm khóa cờ `clutch_active = true` khi GPIO27 ở mức LOW. | `CODE IMPLEMENTED` | Tương đương thao tác nhấc chuột quang lên khỏi mặt bàn để rê lại. |
| **TEST 5** | Cử chỉ vung tịnh tiến sang Trái (Flick Left -> Back) | Trong khi bấm giữ `BTN_MODE`, vung nhanh cả bàn tay sang bên trái rồi giật nhẹ về. | Máy tính nhận diện duy nhất $1$ sự kiện nhấp nút **Mouse Back** (trình duyệt quay lại trang trước). | Máy trạng thái nhận dạng xung gia tốc 2 pha trên trục ngang; đã test logic pass. | `NEEDS HARDWARE TEST` | Yêu cầu xung gia tốc $|a_y| > 1.2g$ và có pha hãm ngược chiều trong $400\,\text{ms}$. |
| **TEST 6** | Cử chỉ vung tịnh tiến sang Phải (Flick Right -> Forward) | Trong khi bấm giữ `BTN_MODE`, vung nhanh cả bàn tay sang bên phải rồi giật nhẹ về. | Máy tính nhận diện duy nhất $1$ sự kiện nhấp nút **Mouse Forward** (trình duyệt chuyển sang trang kế). | Máy trạng thái nhận dạng xung đối xứng trục; đã kiểm chứng thuật toán. | `NEEDS HARDWARE TEST` | Tương tự Test 5 với chiều gia tốc dương. |
| **TEST 7** | Đổi tư thế chậm không kích hoạt nhầm (Slow Reposition) | Bấm giữ `BTN_MODE`, xoay đổi tư thế cầm bo mạch thật chậm ($|a| < 0.4g$) rồi nhả nút. | **KHÔNG** kích hoạt bất kỳ lệnh Back hay Forward nào; hệ thống chỉ cập nhật lại Reference. | Ngưỡng năng lượng gia tốc chặn hoàn toàn các chuyển động xoay êm dịu. | `NEEDS HARDWARE TEST` | Kiểm chứng khả năng chống kích hoạt nhầm (False Positive Rejection). |
| **TEST 8** | Tái định tâm ở tư thế cầm ngang (Recenter at Normal Pose) | Cầm chuột nằm ngang tự nhiên, bấm đè `BTN_MODE` rồi nhả ra. | Trục ngang chuột khớp với trục ngang màn hình; lắc tay sang phải chuột đi sang phải. | Logic chụp lại vector trọng trường làm chuẩn thẳng đứng. | `NEEDS HARDWARE TEST` | Thiết lập điểm mốc chuẩn ban đầu. |
| **TEST 9** | Tái định tâm ở tư thế nghiêng $45^\circ$ (Recenter at Tilted Pose) | Nghiêng bo mạch $45^\circ$ theo chiều Roll hoặc Pitch, bấm giữ `BTN_MODE` rồi nhả ra. | Con trỏ vẫn di chuyển ngang khi người dùng lắc cổ tay sang hai bên theo góc nhìn của mình. | Thuật toán quay vector vận tốc góc theo mặt phẳng tiếp diện trọng trường. | `NEEDS HARDWARE TEST` | Chứng minh tính thích nghi của hệ quy chiếu tham chiếu. |
| **TEST 10**| Chĩa chuột thẳng lên trời (Pointing Upward Test) | Chĩa đầu bo mạch lên trần nhà ($90^\circ$ Pitch Up), bấm đè `BTN_MODE`, nhả nút và rê chuột. | Con trỏ vẫn dịch chuyển ngang/dọc trực quan, không bị đảo lộn chiều hay khóa cứng trục. | Giải quyết triệt để câu hỏi chất vấn của giảng viên bằng phép biến đổi Quaternion tham chiếu. | `NEEDS HARDWARE TEST` | Kiểm chứng giải pháp RG-03. |

---

## 2. Quy Trình Kiểm Thử Phần Cứng Khi Nạp Mạch Thật (Bench Test Procedure)

Khi người dùng cắm cáp USB kết nối bo ESP32 với máy tính:
1. **Mở Serial Monitor ở tốc độ 115200 baud**:
   - Xác nhận chip in ra: `WHO_AM_I = 0xEA [PASS]`.
   - Xác nhận thanh ghi cấu hình đọc lại: `PWR_MGMT_1 readback = 0x01 [PASS]`, `GYRO_CONFIG_1 readback = 0x1B [PASS]`, `ACCEL_CONFIG readback = 0x1B [PASS]`.
2. **Kiểm tra quá trình hiệu chuẩn Bias**:
   - Giữ yên chuột 2 giây. Serial in ra: `Gyro Bias: X=..., Y=..., Z=... [CALIBRATED]`.
3. **Kết nối Bluetooth Low Energy**:
   - Trên máy tính Windows/Mac, mở Bluetooth Settings $\rightarrow$ Tìm thiết bị `AirMouse-ESP32` $\rightarrow$ Nhấn Pair.
   - Quan sát đèn LED trạng thái chuyển từ nhấp nháy sang sáng liên tục.
4. **Thực hiện tuần tự 10 bài kiểm tra trong bảng trên** và điền kết quả vào cột `Actual`.
