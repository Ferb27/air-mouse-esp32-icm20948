# CHIẾN LƯỢC KIỂM SOÁT VÀ TRIỆT TIÊU TRÔI CON TRỎ CHUỘT (DRIFT CONTROL STRATEGY)
## DỰ ÁN: AIR MOUSE BLE HID (ESP32 + ICM-20948)

> **Dự án**: Chuột bay không gian không dây (Air Mouse BLE HID)  
> **Kiến trúc**: Hybrid 9-Axis Air Mouse  
> **Mục tiêu**: Trả lời câu hỏi trọng tâm của giảng viên: *"Làm thế nào để chuột không bị tự trôi (drifting) khi cầm trên tay hoặc đặt trên bàn?"*  
> **Phiên bản**: V1.0.0 — Canonical Anti-Drift Strategy Specification  

---

## 1. Phân Loại Bản Chất Các Thành Phần Gây Trôi (Decomposition of Drift)

Để bảo vệ thuyết phục trước hội đồng chấm, nhóm tách bạch 6 nguyên nhân vật lý khác nhau gây ra hiện tượng lệch con trỏ:

| Ký hiệu | Thành phần gây sai số | Nguồn gốc vật lý | Tác động lên con trỏ chuột | Phương pháp triệt tiêu trong Dự án |
| :---: | :--- | :--- | :--- | :--- |
| **A** | **Zero-Rate Bias (Offset tĩnh)** | Sai số chế tạo vi cơ MEMS bên trong cấu trúc silicon của ICM-20948. Khi đứng yên tuyệt đối, giá trị đọc thô vẫn khác 0 (ví dụ $+15\text{--}40\,\text{LSB}$). | Con trỏ chuột tự chạy tuyến tính liên tục về một hướng cố định ngay cả khi đặt cố định trên bàn. | **Startup Bias Calibration**: Lấy trung bình 200 lần polling lúc khởi động tĩnh (nominal delay $10\,\text{ms}$, thời gian danh định $\approx 2.0\,\text{s}$) để trừ offset: $\omega_{\text{unbiased}} = \omega_{\text{raw}} - \text{Bias}_0$. |
| **B** | **High-Frequency Noise (Nhiễu tần số cao)** | Nhiễu nhiệt cơ học (Brownian motion) và nhiễu mạch khuếch đại analog nội của chip. | Con trỏ rung giật vi mô (jitter), nét di chuột bị răng cưa, khó bấm trúng icon nhỏ. | **Hardware DLPF (51.2 Hz)** cấu hình trong `GYRO_CONFIG_1` kết hợp phần mềm **Exponential Moving Average (EMA)**: $\omega_{\text{filt}} = \alpha \omega_k + (1-\alpha) \omega_{k-1}$. |
| **C** | **Temperature Drift (Trôi nhiệt)** | Nhiệt độ tự phát nóng của chip khi hoạt động làm biến dạng cấu trúc MEMS, khiến Bias thay đổi chậm theo thời gian ($\approx 0.05\,\text{dps}/^\circ\text{C}$). | Sau 5–10 phút sử dụng, con trỏ bắt đầu trôi chậm trở lại dù lúc bật nguồn đã hiệu chuẩn tĩnh. | **Online Stationary Auto-Zero**: Khi phát hiện thiết bị đứng yên trong phiên làm việc, tự động cập nhật lại giá trị Bias từ từ bằng bộ lọc thích nghi IIR. |
| **D** | **Physiological Hand Tremor (Rung tay sinh lý)** | Rung động không chủ ý tự nhiên của bàn tay con người ($8\text{--}12\,\text{Hz}$ hoặc rung cơ bản $1\text{--}3\,\text{Hz}$). | Con trỏ lắc lư khi người dùng cố định vị để nhấp chuột. | **Dead-Zone & Hysteresis (Vùng chết & Trễ)**: Nếu $|\omega_{\text{unbiased}}| < \omega_{\text{deadzone}}$ thì gán $\omega = 0$. Vùng chết cắt bỏ hoàn toàn rung động sinh lý. |
| **E** | **Cursor Creep (Trôi tích lũy bước rời rạc)** | Do làm tròn số nguyên khi chuyển đổi từ float sang `int8_t` ($-127$ đến $+127$) trong báo cáo BLE HID Mouse. | Tích lũy phần dư nhỏ qua từng chu kỳ $10\,\text{ms}$ khiến chuột thỉnh thoảng nhích 1 pixel. | **Residual Accumulator (Bộ tích lũy phần dư)**: Giữ lại phần thập phân lẻ chưa gửi để cộng dồn vào chu kỳ tiếp theo thay vì làm tròn cắt cụt (truncation). |
| **F** | **Orientation / Tilt Drift (Trôi góc nghiêng tham chiếu)** | Sự sai lệch góc nghiêng khi xoay thiết bị trong không gian. | Chiều xoay chuột ngang bị biến thành chuyển động xiên chéo. | **Accelerometer Gravity Vector**: Dùng trọng trường làm mốc tuyệt đối để chuẩn hóa mặt phẳng tham chiếu (Reference Coordinate Frame). |

---

## 2. Đường Ống Xử Lý Tín Hiệu Chống Trôi (Anti-Drift Pipeline)

```text
[ DỮ LIỆU THÔ ICM-20948 ]
  - Gyro X, Y, Z (Bank 0, 0x33-0x38)
  - Accel X, Y, Z (Bank 0, 0x2D-0x32)
            │
            ▼
[ BƯỚC 1: BỘ LỌC PHẦN CỨNG DLPF ]
  - Gyro DLPF: 51.2 Hz (GYRO_CONFIG_1 = 0x1B, ODR 102.27 Hz qua GYRO_SMPLRT_DIV = 10)
  - Accel DLPF: 50.4 Hz (ACCEL_CONFIG = 0x1B, ODR 102.27 Hz qua ACCEL_SMPLRT_DIV = 10)
            │
            ▼
[ BƯỚC 2: ĐỔI ĐƠN VỊ VẬT LÝ ]
  - ω = raw_gyro / 65.5  (dps)
  - a = raw_accel / 8192.0  (g)
            │
            ▼
[ BƯỚC 3: BỘ PHÁT HIỆN ĐỨNG YÊN (STATIONARY DETECTOR) ]
  - Điều kiện: (||ω|| < Thresh_Gyro) AND (| ||a|| - 1.0g | < Thresh_Accel)
  - Đạt điều kiện liên tục trong N_window chu kỳ (≥ 300 ms)?
       ├── ĐÚNG ──> [ BẬT CỜ STATIONARY ] ──> Cập nhật Auto-Zero Bias thích nghi
       │                                  ──> Khóa cứng ngõ ra: Delta = 0 (Anti-Creep)
       └── SAI  ──> [ THIẾT BỊ ĐANG DI CHUYỂN ]
            │
            ▼
[ BƯỚC 4: BÙ SAI SỐ TĨNH (BIAS COMPENSATION) ]
  - ω_comp = ω - Bias_current
            │
            ▼
[ BƯỚC 5: XỬ LÝ VÙNG CHẾT & TRỄ (DEAD-ZONE & HYSTERESIS) ]
  - Nếu |ω_comp| < Deadzone_Low  ──> ω_clean = 0
  - Nếu |ω_comp| > Deadzone_High ──> ω_clean = sgn(ω_comp) * (|ω_comp| - Deadzone_Low)
            │
            ▼
[ BƯỚC 6: BIẾN ĐỔI HỆ QUY CHIẾU THAM CHIẾU (REFERENCE FRAME TRANSFORM) ]
  - Chiếu ω_clean từ trục cảm biến sang mặt phẳng điều khiển màn hình theo Quaternion tham chiếu
            │
            ▼
[ BƯỚC 7: ÁNH XẠ ĐỘ NHẠY & CLAMPING SANG BLE HID DELTA ]
  - dX = clamp(K_sens * ω_screen_x, -127, +127)
  - dY = clamp(K_sens * ω_screen_y, -127, +127)
            │
            ▼
[ GỬI BẢN TIN BLE HID MOUSE REPORT ]
```

---

## 3. Thuật Toán Nhận Diện Đứng Yên (Stationary Detection Algorithm)

Bộ nhận diện đứng yên (Stationary Detector) kết hợp dữ liệu đồng thời từ **cả Gyroscope và Accelerometer**:

### Công thức kiểm tra:
1. **Chuẩn độ lớn vận tốc góc (Gyro Norm)**:
   $$\|\vec{\omega}\| = \sqrt{\omega_x^2 + \omega_y^2 + \omega_z^2}$$
   Điều kiện: $\|\vec{\omega}\| < \Omega_{\text{stat\_thresh}}$

2. **Độ lệch độ lớn gia tốc so với trọng lực $1g$ (Accel Deviation)**:
   $$\|\vec{a}\| = \sqrt{a_x^2 + a_y^2 + a_z^2}$$
   Điều kiện: $\left| \|\vec{a}\| - 1.0\,\text{g} \right| < A_{\text{stat\_thresh}}$

3. **Cửa sổ thời gian xác nhận (Time Confirmation Window)**:
   Cả hai điều kiện trên phải được thỏa mãn liên tục trong $M$ mẫu lấy mẫu liên tiếp ($t_{\text{window}} = M \times \Delta t \ge 300\,\text{ms}$).

### Bảng tham số khởi tạo (Parameters Table):

| Tham số | Giá trị khởi tạo thử nghiệm | Đơn vị | Trạng thái kỹ thuật | Ý nghĩa & Căn cứ xác định |
| :--- | :---: | :---: | :---: | :--- |
| `GYRO_STAT_THRESH` | $1.2$ | $^{\circ}/\text{s}$ | `NEEDS HARDWARE TUNING` | Ngưỡng chặn vận tốc góc khi tay đặt yên hoặc cố định trên bàn. |
| `ACCEL_STAT_THRESH` | $0.08$ | $g$ | `NEEDS HARDWARE TUNING` | Sai lệch gia tốc trọng trường tối đa cho phép khi không có rung động cơ học ngoài. |
| `STAT_WINDOW_COUNT` | $30$ | samples | `NEEDS HARDWARE TUNING` | Tại tốc độ $100\,\text{Hz}$, $30$ mẫu tương đương $300\,\text{ms}$ để xác nhận trạng thái bất động. |
| `DEADZONE_LOW` | $0.8$ | $^{\circ}/\text{s}$ | `NEEDS HARDWARE TUNING` | Cắt bỏ hoàn toàn rung động sinh lý của ngón tay người dùng. |
| `DEADZONE_HIGH` | $1.4$ | $^{\circ}/\text{s}$ | `NEEDS HARDWARE TUNING` | Ngưỡng trễ hysteresis giúp việc rê chuột khi bắt đầu chuyển động mượt mà, không bị giật khấc. |
| `AUTO_ZERO_ALPHA` | $0.002$ | - | `NEEDS HARDWARE TUNING` | Hệ số học chậm cho bộ lọc thích nghi bias: $\text{Bias} \leftarrow (1-\alpha)\text{Bias} + \alpha \omega_{\text{raw}}$. |

---

## 4. Tại Sao ICM-20948 Không Tự Động "Hết Trôi" Nếu Thiếu Phần Mềm?

> [!WARNING]
> **CẢNH BÁO VỀ LUẬN ĐIỂM BẢO VỆ ĐỒ ÁN**:
> Sinh viên tuyệt đối **KHÔNG ĐƯỢC NÓI**: *"Vì ICM-20948 đắt tiền hơn hoặc tốt hơn MPU-6050 nên nó không bị trôi"*.

### Căn cứ khoa học từ Datasheet TDK DS-000189:
1. Độ trôi nhiệt độ của Gyroscope ICM-20948 danh định là $\pm 0.05\,\text{dps}/^{\circ}\text{C}$ (typical).
2. Sai số zero-rate output danh định ở $25^{\circ}\text{C}$ lên tới $\pm 5\,\text{dps}$ (trên toàn thang $\pm 250\text{--}500\,\text{dps}$).
3. Nếu không có phần mềm hiệu chuẩn startup bias ($5\,\text{dps} \times 65.5 = 327\,\text{LSB}$), con trỏ chuột máy tính sẽ **ngay lập tức tự phi hết tốc lực sang góc màn hình**!
4. Khả năng chống trôi của Air Mouse đến từ **KIẾN TRÚC PHẦN MỀM ĐA TẦNG (Multi-stage Anti-Drift Architecture)**:
   - Hiệu chuẩn tĩnh lúc khởi động (Startup Calibration).
   - Bộ lọc dải thông thấp phần cứng (Hardware DLPF).
   - Bộ nhận diện đứng yên (Stationary Detector) kết hợp cả Gyro và Accel.
   - Vùng chết phi tuyến (Nonlinear Dead-zone with Hysteresis).
   - Khóa ly hợp tái định tâm (`BTN_MODE` Clutch).
