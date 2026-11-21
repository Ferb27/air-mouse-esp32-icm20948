# HỆ QUY CHIẾU KHÔNG GIAN VÀ PHÉP BIẾN ĐỔI TỌA ĐỘ (SENSOR COORDINATE FRAMES)
## DỰ ÁN: AIR MOUSE BLE HID (ESP32 + ICM-20948)

> **Dự án**: Chuột bay không gian không dây (Air Mouse BLE HID)  
> **Kiến trúc**: Hybrid 9-Axis Air Mouse  
> **Mục tiêu**: Định nghĩa tường minh các hệ trục tọa độ, giải quyết bài toán: *"Thiết bị bị chĩa lên trời hoặc nghiêng tự do thì chuột có hoạt động đúng trực quan không?"*  
> **Phiên bản**: V1.0.0 — Canonical Coordinate Transformation Specification  

---

## 1. Định Nghĩa 4 Hệ Quy Chiếu Trong Hệ Thống (Four Reference Frames)

```text
       [1. Sensor Body Frame]
                 │
                 ▼ (Gắn cơ khí trên Carrier Board)
         [2. PCB Hand Frame]
                 │
                 ▼ (Tư thế cầm nắm & Tái định tâm gần nhất)
      [3. Reference Control Frame]
                 │
                 ▼ (Phép chiếu tương quan lên màn hình)
       [4. Screen Pixel Frame]
```

### 1. Hệ trục thân cảm biến (Sensor Body Frame — $S$):
Được khắc trên mặt lưng chip ICM-20948 và in trên lớp Silkscreen của module WCMCU-20948:
- **$+X_s$**: Hướng dọc theo chiều dài bo cảm biến (hướng về phía hàng chân cắm).
- **$+Y_s$**: Hướng sang cạnh ngang của bo cảm biến (theo quy tắc bàn tay phải).
- **$+Z_s$**: Hướng vuông góc thẳng đứng lên trời, vuông góc với bề mặt chip MEMS.

### 2. Hệ trục bo mạch chuột & bàn tay người dùng (PCB Hand Frame — $B$):
Khi người dùng cầm bo chuột Air Mouse trên tay theo phương chuẩn:
- **Trục Tiến (Forward / Roll)**: Dọc theo sống lưng bo mạch, ăng-ten ESP32 hướng về phía màn hình máy tính ($+X_b$).
- **Trục Ngang (Right / Pitch)**: Hướng sang bên phải của bàn tay người dùng ($+Y_b$).
- **Trục Dọc (Down / Yaw)**: Hướng thẳng xuống mặt đất khi bo mạch đặt nằm ngang song song mặt bàn ($+Z_b$).

### 3. Hệ trục tham chiếu điều khiển (Reference Control Frame — $R$):
Là hệ trục ảo được "chụp lại" (Snapshotted) tại thời điểm người dùng hoàn tất thao tác bấm giữ và nhả nút `BTN_MODE` (Clutch / Recenter):
- Trục trọng trường cục bộ $\vec{g}$ được lấy làm trục thẳng đứng chuẩn ($Z_r$).
- Trục ngang màn hình ($X_r$) và trục dọc màn hình ($Y_r$) được tạo lập vuông góc với $Z_r$.

### 4. Hệ trục tọa độ con trỏ màn hình máy tính (Screen Frame — $D$):
Chuẩn tọa độ chuột đồ họa hệ điều hành máy tính (Windows / macOS / Linux):
- **$+X_{\text{screen}}$**: Dịch chuyển con trỏ sang **PHẢI** (Right: $\Delta X > 0$).
- **$-X_{\text{screen}}$**: Dịch chuyển con trỏ sang **TRÁI** (Left: $\Delta X < 0$).
- **$+Y_{\text{screen}}$**: Dịch chuyển con trỏ đi **XUỐNG** (Down: $\Delta Y > 0$).
- **$-Y_{\text{screen}}$**: Dịch chuyển con trỏ đi **LÊN** (Up: $\Delta Y < 0$).

---

## 2. Bài Toán Thiết Bị Chĩa Lên Trời (Device Pointing Upward Problem)

### A. Hiện tượng lỗi trên chuột thông thường (Fixed-Axis Flaw)
Hầu hết các dự án chuột bay mã nguồn mở cơ bản gán cứng trục:
$$\Delta X = K_x \cdot \omega_{z,\text{body}}$$
$$\Delta Y = -K_y \cdot \omega_{y,\text{body}}$$

Khi thiết bị đặt nằm ngang, quy tắc này hoạt động tốt:
- Lắc cổ tay sang trái/phải tạo $\omega_z \rightarrow$ chuột di chuyển ngang.
- Gật cổ tay lên/xuống tạo $\omega_y \rightarrow$ chuột di chuyển dọc.

**Tuy nhiên, khi người dùng ngả lưng tựa ghế và chĩa đầu chuột lên trời ($90^\circ$ Pitch Up)**:
- Trục $Z_{\text{body}}$ lúc này đã quay ngang thành trục nằm ngang trong phòng.
- Trục $X_{\text{body}}$ chĩa thẳng đứng lên trần nhà.
- Việc lắc cổ tay sang hai bên bây giờ thực chất là xoay quanh trục $Y_{\text{body}}$, nhưng phần mềm vẫn đọc trục $Z_{\text{body}}$ khiến con trỏ **hoàn toàn đứng yên hoặc chạy lộn xộn theo trục dọc**, gây ức chế tột độ cho người dùng.

---

## 3. Giải Pháp Phép Biến Đổi Hệ Quy Chiếu Thích Nghi (Adaptive Reference Transform)

Để khắc phục hiện tượng trên, hệ thống triển khai giải pháp biến đổi vận tốc góc thông qua **Quaternion Tham Chiếu (Reference Quaternion)**:

### Bước 1: Ước lượng vector trọng lực hiện tại (Gravity Vector Estimation)
Từ số liệu gia tốc kế 3 trục đã qua bộ lọc thông thấp (LPF):
$$\vec{a}_{\text{norm}} = \frac{\vec{a}}{\|\vec{a}\|}$$
Trong trạng thái gần tĩnh (Quasi-static), $\vec{a}_{\text{norm}}$ chỉ thuần túy là vector đơn vị của trọng lực Trái Đất chiếu vào hệ trục thân cảm biến:
$$\vec{g}_{\text{body}} \approx \vec{a}_{\text{norm}}$$

### Bước 2: Xác lập Quaternion Tham Chiếu khi người dùng nhả nút `BTN_MODE`
Khi người dùng bấm đè `BTN_MODE`, xoay chuột đến bất kỳ tư thế nào (kể cả chĩa lên trời) rồi nhả nút:
1. Hệ thống ghi nhận hướng trọng trường tại tư thế đó: $\vec{g}_{\text{ref}} = \vec{g}_{\text{body}}$.
2. Xác định Quaternion xoay $q_{\text{align}}$ đưa vector trọng trường thân cảm biến về trục thẳng đứng chuẩn:
   $$q_{\text{align}} = \text{QuaternionFromVectors}(\vec{g}_{\text{body}}, [0, 0, 1]^T)$$

### Bước 3: Chiếu vận tốc góc đo được sang mặt phẳng trực quan của người dùng
Ở mỗi chu kỳ lấy mẫu tiếp theo, vector vận tốc góc đo được trong thân cảm biến $\vec{\omega}_{\text{body}} = [\omega_x, \omega_y, \omega_z]$ được quay sang hệ quy chiếu tham chiếu:
$$\vec{\omega}_{\text{ref}} = q_{\text{align}} \otimes \begin{bmatrix} 0 \\ \vec{\omega}_{\text{body}} \end{bmatrix} \otimes q_{\text{align}}^{-1}$$

Sau đó, hai thành phần tương ứng với mặt phẳng vuông góc với mắt nhìn được đưa vào điều khiển chuột:
$$\Delta X = K_x \cdot \omega_{\text{ref}, z}$$
$$\Delta Y = -K_y \cdot \omega_{\text{ref}, y}$$

### Bước 4: Chế độ Fallback Đơn Giản (P0 Simplified Planar Projection)
Nếu tài nguyên tính toán hoặc thời gian chạy thực nghiệm đêm nay cần ưu tiên độ ổn định cao nhất, thuật toán sử dụng phép chiếu ma trận trực giao cục bộ (Local Tangent Plane Projection):
- Trục dọc con trỏ = vận tốc góc quanh trục vuông góc với mặt phẳng tạo bởi thân chuột và vector trọng trường.
- Trục ngang con trỏ = vận tốc góc quanh vector trọng trường cục bộ.
- Phép tính này hoàn toàn không chứa điểm kỳ dị (Gimbal Lock) của góc Euler và chỉ cần các phép nhân vô hướng/vector đơn giản.
