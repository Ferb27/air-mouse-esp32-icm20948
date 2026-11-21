# ĐẶC TẢ KIẾN TRÚC HYBRID 9-AXIS AIR MOUSE (V2.0)
## DỰ ÁN: CHUỘT BAY KHÔNG GIAN BLE HID (ESP32 + ICM-20948)

> **Dự án**: Chuột bay không gian không dây (Air Mouse BLE HID)  
> **Môn học**: Hệ thống nhúng (Embedded Systems) — Báo cáo Giữa kỳ Tuần 5  
> **Kiến trúc chính thức**: `HYBRID 9-AXIS AIR MOUSE`  
> **Phiên bản**: V2.0.0 — Canonical Hybrid Architecture Specification  
> **Ngày cập nhật**: 2026-09-18  

---

## 1. Tuyên Ngôn Kiến Trúc Cốt Lõi (Core Principles)

Kiến trúc **HYBRID 9-AXIS AIR MOUSE** giải quyết toàn diện bài toán điều khiển tự nhiên, khắc phục hiện tượng trôi (drift) và cho phép người dùng thay đổi tư thế cầm tự do (kể cả hướng lên trần nhà) mà vẫn giữ nguyên hướng điều khiển trực quan:

1. **Bản chất con trỏ**: Con trỏ chuột trên máy tính **DUY TRÌ TUYỆT ĐỐI NGUYÊN LÝ RELATIVE RATE-CONTROL** (chuột điều khiển theo vận tốc tương đối qua giao thức chuẩn BLE HID Mouse).
2. **Vai trò Con quay hồi chuyển (Gyroscope)**: Là nguồn cảm biến điều khiển con trỏ chính yếu và tức thời (độ trễ thấp, phản ứng nhanh theo vận tốc góc $\omega_x, \omega_y, \omega_z$).
3. **Vai trò Gia tốc kế (Accelerometer)**: Đóng vai trò phụ trợ thông minh (Support Auxiliary Function), phục vụ 3 mục đích:
   - **Nhận diện trạng thái đứng yên (Stationary Detection)** để tự động khóa trôi và cập nhật bù sai số tĩnh (Auto-Zero Bias Correction).
   - **Xác định vector trọng trường ($\vec{g}$)** để ước lượng khung định hướng tham chiếu (Reference Coordinate Frame).
   - **Nhận diện cử chỉ vung tịnh tiến ngắn (Translational Flick Gestures)**: Vung sang trái $\rightarrow$ Back, vung sang phải $\rightarrow$ Forward.
4. **Ước lượng định hướng (Orientation Estimation)**: Chỉ dùng làm **HÀM HỖ TRỢ NỘI BỘ (Internal Support Function)** để thiết lập hệ tọa độ tham chiếu thích nghi; **TUYỆT ĐỐI KHÔNG BIẾN THIẾT BỊ THÀNH 3DoF ABSOLUTE ORIENTATION POINTER** (không chiếu góc Euler tuyệt đối lên tọa độ pixel màn hình).
5. **Cơ chế Ly hợp / Tái định tâm (Clutch & Recenter Interaction)**: Cho phép người dùng bấm giữ nút `BTN_MODE` để "ngắt ly hợp" (đóng băng con trỏ), tự do đổi tư thế cổ tay hoặc xoay bo mạch sang góc cầm mới (ví dụ cầm ngang, nghiêng $45^\circ$, hoặc chĩa thẳng đứng lên trời), sau đó nhả nút để xác lập mặt phẳng điều khiển trực quan mới.
6. **Nhận diện cử chỉ tịnh tiến (Short Temporal Gesture Recognition)**: Phân tích xung gia tốc có chu kỳ (Vung đi + Giật về); **TUYỆT ĐỐI KHÔNG TÍCH PHÂN GIA TỐC KẾ 2 LẦN ĐỂ TÍNH TỌA ĐỘ VỊ TRÍ $X, Y, Z$ TRONG PHÒNG**.

---

## 2. Phân Định Rạch Ròi: Xoay (Rotation) vs Tịnh Tiến (Translation) vs Vị Trí Thực (True Position)

Để bảo vệ thuyết phục trước hội đồng chấm thi, tài liệu phân định bản chất vật lý của 3 khái niệm:

| Khái niệm | Cảm biến đo | Bản chất vật lý | Ứng dụng trong Đề tài | Giới hạn & Lý do kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **Điều khiển Xoay (Rotational Control)** | **Gyroscope (MEMS)** | Vận tốc góc ($\omega$ tính bằng $^{\circ}/\text{s}$) | Di chuyển con trỏ chuột tương đối $(\Delta X, \Delta Y)$ | Không tích phân ra góc màn hình; chỉ nhân gain độ nhạy trực tiếp: $\Delta X = K_x \cdot \omega_z$, $\Delta Y = K_y \cdot \omega_y$. Dừng xoay là con trỏ dừng. |
| **Cử chỉ Tịnh tiến (Translational Gesture)** | **Accelerometer (MEMS)** | Xung gia tốc tức thời ($a$ tính bằng $\text{m}/\text{s}^2$ hoặc $g$) | Nhận diện sự kiện phím tắt trình duyệt: **Back** (Flick Trái) và **Forward** (Flick Phải) | **Không đo quãng đường di chuyển**. Chỉ nhận dạng hình thái mẫu tín hiệu gia tốc theo thời gian (Temporal Waveform: Gia tốc đỉnh $\rightarrow$ Gia tốc hãm ngược chiều $\rightarrow$ Đứng yên). |
| **Vị trí Thực 3D (True XYZ Room Position)** | Gia tốc kế (Tích phân 2 lần) | Tọa độ không gian $(X, Y, Z)$ trong phòng | **KHÔNG TRIỂN KHAI (OUT OF SCOPE)** | **CẤM TUYỆT ĐỐI**. Do sai số trôi bias $\epsilon$ của gia tốc kế bị tích phân 2 lần bùng nổ theo bình phương thời gian: $s(t) = s_0 + v_0 t + \frac{1}{2} \epsilon t^2$. Chỉ sau 2-3 giây, sai số lên đến hàng mét, phá hủy hoàn toàn khả năng điều khiển. |

---

## 3. Trải Nghiệm Người Dùng (Target User Experience & Interaction State Machine)

Hệ thống tái sử dụng nút nhấn `BTN_MODE` (`GPIO27`) hiện có trên phần cứng để tạo trải nghiệm "Clutch-to-Reposition & Flick":

```text
               +-------------------------------------------------------------+
               |                  CHẾ ĐỘ BÌNH THƯỜNG (NORMAL)                 |
               | - Vận tốc góc Gyro -> Di chuyển con trỏ chuột tương đối     |
               | - Accelerometer giám sát trạng thái đứng yên để Auto-Zero   |
               +-------------------------------------------------------------+
                                              |
                                              | Bấm đè nút BTN_MODE (Press & Hold)
                                              v
               +-------------------------------------------------------------+
               |              TRẠNG THÁI LY HỢP (CLUTCH_ACTIVE)              |
               | - Đóng băng hoàn toàn con trỏ chuột (Delta = 0)             |
               | - Bắt đầu bộ đệm phân tích cử chỉ gia tốc (Gesture Buffer)  |
               +-------------------------------------------------------------+
                                      /                               \
         Phát hiện xung gia tốc      /                                 \ Không có xung flick mạnh
         (Flick Trái / Flick Phải)  /                                   \ Thiết bị ổn định ở tư thế mới
                                   v                                     v
+-----------------------------------------------+   +-----------------------------------------------+
|         XỬ LÝ CỬ CHỈ (GESTURE DETECTED)       |   |       TÁI ĐỊNH TÂM (RECENTER REFERENCE)       |
| - Vung trái + giật lại: Gửi HID Mouse Back   |   | - Lấy vector trọng trường hiện tại làm chuẩn  |
| - Vung phải + giật lại: Gửi HID Mouse Forward |   | - Thiết lập hệ quy chiếu điều khiển mới       |
| - Đánh dấu đã phát cử chỉ (Suppress Recenter) |   | - Chuẩn bị đón tư thế cầm mới (ví dụ ngửa lên)|
+-----------------------------------------------+   +-----------------------------------------------+
                                   \                                     /
                                    \                                   /
                                     v                                 v
                                    Nhả nút BTN_MODE (Button Released)
                                              |
                                              v
               +-------------------------------------------------------------+
               |              TRỞ VỀ BÌNH THƯỜNG (RESUME NORMAL)             |
               | - Tiếp tục rê chuột tự nhiên trên hệ quy chiếu vừa cập nhật |
               +-------------------------------------------------------------+
```

### Chi tiết 3 tương tác người dùng:

1. **Rê chuột thông thường (Normal Track)**:
   - Cổ tay nghiêng lắc nhẹ $\rightarrow$ con trỏ di chuyển tương ứng trên màn hình.
   - Khi tay dừng lại trên mặt bàn hoặc dừng giữa không trung $\rightarrow$ bộ phát hiện đứng yên kích hoạt, ép dX/dY về 0 khi bộ phát hiện đứng yên xác nhận đủ tin cậy; không bảo đảm loại bỏ mọi dạng drift.

2. **Ngắt ly hợp để đổi tư thế cầm (Clutch & Recenter)**:
   - Người dùng đang cầm ngang, cảm thấy mỏi cổ tay hoặc muốn tựa tay lên ghế và chĩa chuột lên trần nhà ($+Z$ hướng thiên):
   - Bấm giữ `BTN_MODE` $\rightarrow$ chuột đứng yên.
   - Xoay tay tự nhiên đến tư thế thoải mái nhất.
   - Nhả `BTN_MODE` $\rightarrow$ thuật toán tự động lấy hướng trọng trường mới làm trục dọc tham chiếu. Kể từ lúc này, xoay cổ tay sang trái/phải vẫn làm con trỏ di chuyển ngang, gật cổ tay lên/xuống vẫn làm con trỏ di chuyển dọc trên màn hình máy tính!

3. **Cử chỉ tịnh tiến lướt web (Flick Gesture: Back / Forward)**:
   - Trong khi đang đè `BTN_MODE`:
     - Vung nhanh cả bàn tay sang bên trái và giật nhẹ lại $\rightarrow$ máy tính nhận lệnh **Browser Back** (hoặc Mouse Button 4).
     - Vung nhanh cả bàn tay sang bên phải và giật nhẹ lại $\rightarrow$ máy tính nhận lệnh **Browser Forward** (hoặc Mouse Button 5).
   - Khi một cử chỉ hợp lệ được kích hoạt, hệ thống kích hoạt thời gian trễ chống dội (Cooldown $\approx 350\,\text{ms}$) và bỏ qua thao tác Recenter để không làm lệch hệ quy chiếu.

---

## 4. Hệ Quy Chiếu & Phép Biến Đổi Tọa Độ Tham Chiếu (Reference Frame Transformation)

### A. Vấn đề khi thiết bị chĩa lên trời (Pointing Upward Problem)
Khi thiết bị được chĩa thẳng đứng lên trời, trục $+X$ hoặc $+Y$ của cảm biến bị xoay $90^\circ$ so với phương ngang của màn hình máy tính. Nếu dùng phép gán trục cố định ($dX = \omega_z, dY = -\omega_y$), việc xoay cổ tay sang hai bên sẽ vô tình kích hoạt trục sai, làm con trỏ chạy chéo hoặc chạy dọc, gây ức chế cho người dùng.

### B. Giải pháp Quaternion Tham Chiếu
Hệ thống duy trì một Quaternion định hướng $q = [q_w, q_x, q_y, q_z]$ biểu diễn tư thế hiện tại của cảm biến so với trọng trường Trái Đất (Gravity Frame):
1. **Lúc khởi động hoặc khi Recenter**: Lưu tư thế hiện tại làm Quaternion tham chiếu $q_{\text{ref}}$.
2. **Khi vận hành**: Quaternion tương đối giữa tư thế hiện tại và tư thế tham chiếu được xác định:
   $$q_{\text{rel}} = q_{\text{ref}}^{-1} \otimes q_{\text{current}}$$
3. **Chiếu vận tốc góc vào mặt phẳng điều khiển màn hình**:
   Vận tốc góc đo được trong hệ trục thân cảm biến $\vec{\omega}_{\text{body}} = [\omega_x, \omega_y, \omega_z]$ được quay sang hệ quy chiếu tham chiếu:
   $$\vec{\omega}_{\text{control}} = q_{\text{rel}} \otimes \vec{\omega}_{\text{body}} \otimes q_{\text{rel}}^{-1}$$
4. **Ánh xạ con trỏ**:
   $$\Delta X = K_x \cdot \omega_{\text{control}, \text{yaw}}$$
   $$\Delta Y = K_y \cdot \omega_{\text{control}, \text{pitch}}$$

> [!TIP]
> Phép biến đổi này giúp con trỏ luôn tuân theo chuyển động tương đối của bàn tay đối với mắt nhìn của người dùng, bất kể bo mạch đang được cầm nằm ngang, dốc nghiêng hay chĩa lên trần nhà.

---

## 5. Bản Đồ Phân Bổ Ngoại Vi & Cảm Biến (Peripheral Allocation)

| Phần cứng | Khối chức năng | Phân loại | Cấu hình & Vai trò |
| :--- | :--- | :--- | :--- |
| **ESP32** | I2C Controller 0 | Nội vi MCU | Master mode, $400\,\text{kHz}$, kết nối `GPIO21` (SDA) và `GPIO22` (SCL) qua Level Shifter $1.8\,\text{V}$. |
| **ESP32** | GPIO Input | Nội vi MCU | `GPIO25` (Left Click), `GPIO26` (Right Click), `GPIO27` (Mode / Clutch / Recenter / Gesture Arm). |
| **ESP32** | GPIO Output | Nội vi MCU | `GPIO32` điều khiển LED trạng thái (Khởi động, kết nối BLE, hiệu chuẩn tĩnh). |
| **ESP32** | SAR ADC1 | Nội vi MCU | `ADC1_CH6` (`GPIO34`) đo điện áp pin chia đôi qua cầu trở 100k/100k. |
| **ESP32** | BLE HID Stack | Nội vi MCU | Giao thức chuột BLE HID tiêu chuẩn (Buttons, dX, dY, Wheel). |
| **ICM-20948** | 3-axis Gyroscope | Ngoại vi cảm biến | Đo vận tốc góc $\pm 500^{\circ}/\text{s}$, DLPF $51.2\,\text{Hz}$, đọc Burst 6 byte từ Bank 0 `0x33`. |
| **ICM-20948** | 3-axis Accelerometer | Ngoại vi cảm biến | Đo gia tốc $\pm 4g$, DLPF $\approx 50.4\,\text{Hz}$, đọc Burst 6 byte từ Bank 0 `0x2D`. |
| **ICM-20948** | 3-axis Magnetometer | Ngoại vi cảm biến | **P1 / OPTIONAL**. Khóa an toàn ở P0 để tránh rủi ro nhiễu từ tính phòng học. |

---

## 6. Cam Kết Tác Động Phần Cứng (Schematic Impact)

> [!NOTE]
> **HOÀN TOÀN KHÔNG YÊU CẦU THAY ĐỔI PHẦN CỨNG HAY SƠ ĐỒ NGUYÊN LÝ**:
> Toàn bộ logic của kiến trúc Hybrid 9-Axis Air Mouse (nhận diện đứng yên, cử chỉ tịnh tiến Back/Forward, ly hợp và tái định tâm góc nhìn) đều khai thác trực tiếp trên phần cứng đã được thiết kế hoàn chỉnh:
> - Cảm biến ICM-20948 đã nối đủ bus I2C để đọc cả Gyroscope và Accelerometer.
> - Nút `BTN_MODE` (`GPIO27`) đã được nối sẵn vào ESP32.
> - Các chân nguồn, LED, cầu phân áp pin giữ nguyên $100\%$.
