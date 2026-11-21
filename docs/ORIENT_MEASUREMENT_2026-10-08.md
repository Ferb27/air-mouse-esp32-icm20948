# BÁO CÁO ĐO ĐẠC ĐỊNH HƯỚNG TRỤC CẢM BIẾN (ORIENTATION MEASUREMENT) TRÊN PHẦN CỨNG THẬT

- **Ngày thực hiện:** 2026-10-08
- **Đối tượng kiểm nghiệm:** Cụm bo mạch Air Mouse (ESP32 Classic DevKit 38-pin + Breakout ICM-20948 WCMCU-20948 cắm trên breadboard).
- **Trạng thái:** `BENCH_VERIFIED` (chỉ áp dụng cho cách cầm và các giá trị đo được trên bo mạch này trong lần chạy này, cấp nguồn USB tại bàn thử nghiệm).

---

## 1. Điều Kiện Đo Đạc & Cách Cầm Bo Mạch

- **Cách người dùng cầm bo mạch (Nguyên văn mục 4):**
  - Cầm cả cụm (ESP32 + breadboard + cảm biến) như cầm điều khiển TV:
    - Đầu có cổng micro-USB / cáp hướng về phía người cầm (phía cổ tay). Đầu đối diện là MŨI, hướng về màn hình.
    - Mặt có linh kiện / chip hướng lên trời.
    - Tay cầm thoải mái, giữ cố định cách cầm này suốt cả lần đo (không xoay cụm trong tay giữa các cử động).
    - Bốn dây kết nối I2C (SDA, SCL), VCC và GND giữa ESP32 và module cảm biến được ấn chắc chắn trên breadboard.
- **Hiện tượng người dùng quan sát thực tế trước khi đo:**
  - "khi tôi đặt như này thì giữ nguyên chiều cao, và di sang trái thì nó đi sang phải, và ngược lại" (trục cao pitch bình thường, trục ngang yaw bị ngược chiều).
- **Thời gian thực hiện đợt đo hợp lệ (`orient_2026-10-08_retry1.log`):**
  - Bắt đầu ghi log: `16:28:24` (2026-10-08)
  - Hiệu chuẩn tĩnh ban đầu: `16:28:27` (`[CAL] bias_x=-1.9202 bias_y=-1.0210 bias_z=-0.1411 dps`, 200 mẫu).
  - Hoàn tất chuỗi cử động và dừng log: `16:35:50` (2026-10-08).
- **Ghi nhận quá trình đo:**
  - Lần đo đầu tiên `raw_logs/orient_2026-10-08.log` kéo dài 420 giây (7 phút) kết thúc ở động tác thứ 2 do thời gian hướng dẫn từng bước qua hội thoại. Tệp log đầu được lưu trữ toàn vẹn và thực hiện lại trọn vẹn 11 cử động trong `orient_2026-10-08_retry1.log` (1200 giây).
  - Tại cử động M3, người dùng có nhận xét "lúc trước tôi có làm ngẩng lên rồi á" vì nhầm lẫn với tư thế tĩnh H1, tuy nhiên dữ liệu cảm biến vẫn ghi nhận đầy đủ cử động ngẩng cổ tay tại mốc 16:32:34.

---

## 2. Danh Sách Tệp & Mã Băm SHA-256 (64 Ký Tự)

| Tệp | SHA-256 Checksum | Mô tả |
| :--- | :--- | :--- |
| `raw_logs/orient_2026-10-08.log` | `0c50ba00d5c8d9afe8c836256b7c1e1aa75bce08d56c29198c2b6f9d1ef302ae` | Log đo định hướng đợt 1 (420 giây). Lưu giữ nguyên vẹn không ghi đè. |
| `raw_logs/orient_2026-10-08_retry1.log` | `4cc3933a1c7591c461615dc786877fce7e856e9a87aee553320ecf328ad5f219` | Log đo định hướng đợt 2 hoàn thành đủ 11 cử động với 4430 dòng dữ liệu 100 ms. |
| `raw_logs/main_firmware_boot_2026-10-08_after_orient.log` | `c3e0a0f6c144a4e30a3f1449d81a9c66a416095537dd878f54b1735456ac6a54` | Log khởi động và chạy 20 giây của firmware chính sau khi nạp khôi phục bo mạch. |
| `docs/orient_phases_2026-10-08.csv` | `60ad52d2594cb230a886f472c34695cbe60edd9446f4c8474099e8c7f92fed48` | Bảng mốc thời gian bắt đầu và kết thúc của 11 cử động. |
| `docs/orient_analysis_2026-10-08.txt` | `40d76600ba9d1d8255dd7ea64add7fbd544791ca24107f2b40c8ebae5b36941f` | Kết xuất phân tích nguyên văn từ script `analyze_orient.py`. |

---

## 3. Bảng Số Liệu Nguyên Văn Từ `analyze_orient.py`

```text
log: raw_logs\orient_2026-10-08_retry1.log
cal: [16:28:27.981] [CAL] bias_x=-1.9202 bias_y=-1.0210 bias_z=-0.1411 dps polls=200
[O] lines parsed: 4430

phase | n | fail | mean ax ay az (g) | mean gx gy gz (dps) | turned about X Y Z (deg)
H0_phang | 40 | 0 | +0.014 -0.006 +0.989 | +1.38 -0.28 +0.40 | +5.5 -1.1 +1.6
H1_mui_len | 40 | 0 | -0.038 -0.293 +0.917 | +8.56 -0.89 -0.24 | +34.2 -3.5 -1.0
H2_mui_xuong | 40 | 0 | -0.029 +0.362 +0.884 | -6.96 -0.47 +2.73 | -27.9 -1.9 +10.9
H3_nghieng_phai | 40 | 0 | +0.663 -0.015 +0.699 | +1.88 +9.77 -0.68 | +7.5 +39.1 -2.7
H4_nghieng_trai | 40 | 0 | -0.518 -0.015 +0.745 | +1.23 -13.79 -0.75 | +4.9 -55.2 -3.0
M1_quay_phai | 30 | 0 | +0.071 +0.068 +0.980 | -1.71 -1.20 -22.62 | -5.1 -3.6 -67.9
M2_quay_trai | 30 | 0 | +0.127 +0.077 +0.973 | +6.45 -0.89 +29.24 | +19.4 -2.7 +87.7
M3_ngang_len | 30 | 0 | +0.036 -0.446 +0.849 | -10.98 -1.63 +2.08 | -32.9 -4.9 +6.2
M4_cui_xuong | 30 | 0 | +0.079 +0.427 +0.859 | +12.35 -1.58 -1.51 | +37.1 -4.7 -4.5
M5_lat_phai | 30 | 0 | +0.728 -0.008 +0.479 | +2.29 -23.90 +1.90 | +6.9 -71.7 +5.7
M6_lat_trai | 30 | 0 | -0.673 -0.030 +0.658 | -2.32 +17.88 +2.84 | -7.0 +53.7 +8.5
```

*Lưu ý kiểm tra kỹ thuật:* Tất cả 11 pha đều ghi nhận `fail = 0` (0 lỗi đọc I2C), số mẫu đủ 40 mẫu cho nhóm H (4.0s) và 30 mẫu cho nhóm M (3.0s).

---

## 4. Mô Tả Thuần Số Liệu Theo Hướng Dẫn (Không Kết Luận Thay Claude)

1. **H0_phang (Tư thế phẳng ngang):**
   - Trục Z có $|mean\ a| = 0.989\text{ g} \approx 1\text{ g}$, trong khi trục X đạt $+0.014\text{ g}$ và trục Y đạt $-0.006\text{ g}$.
   - Trục Z là trục đứng thẳng chịu gia trọng trường; dấu dương ($+0.989\text{ g}$) cho biết **đầu dương (+Z) của cảm biến hướng lên trời**.
2. **H1_mui_len (Ngẩng mũi 45°) so với H0:**
   - Trục Y có độ biến thiên lớn nhất: gia tốc $a_y$ giảm từ $-0.006\text{ g}$ xuống **$-0.293\text{ g}$** (chuyển sang âm). Gia tốc $a_z$ giảm từ $+0.989\text{ g}$ xuống $+0.917\text{ g}$.
   - Trục Y là trục phản ứng với chuyển động "tới - lui" (pitch dọc thân bo mạch). Khi mũi ngẩng lên, $a_y$ mang giá trị âm.
3. **H2_mui_xuong (Cúi mũi 45°) so với H0:**
   - Trục Y đảo chiều gia tốc: $a_y$ tăng từ $-0.006\text{ g}$ lên **$+0.362\text{ g}$** (chuyển sang dương). Gia tốc $a_z$ đạt $+0.884\text{ g}$.
   - Khi mũi cúi xuống, $a_y$ mang giá trị dương.
4. **H3_nghieng_phai (Nghiêng mép phải 45°) so với H0:**
   - Trục X có độ biến thiên lớn nhất: gia tốc $a_x$ tăng từ $+0.014\text{ g}$ lên **$+0.663\text{ g}$** (dương mạnh). Gia tốc $a_z$ giảm xuống $+0.699\text{ g}$, trong khi $a_y$ gần như không đổi ($-0.015\text{ g}$).
   - Trục X là trục phản ứng với chuyển động "trái - phải" (roll ngang thân bo mạch). Khi nghiêng sang phải, $a_x$ mang giá trị dương.
5. **H4_nghieng_trai (Nghiêng mép trái 45°) so với H0:**
   - Trục X đảo chiều gia tốc: $a_x$ giảm từ $+0.014\text{ g}$ xuống **$-0.518\text{ g}$** (âm mạnh). Gia tốc $a_z$ đạt $+0.745\text{ g}$.
   - Khi nghiêng sang trái, $a_x$ mang giá trị âm.
6. **M1 & M2 (Quay mũi sang Phải / Trái quanh trục Z):**
   - Trục Z là trục có độ lớn vận tốc góc và góc tích lũy lớn nhất:
     - **M1 (Quay phải):** Tích lũy góc quay quanh trục Z là **$-67.9^\circ$** (vận tốc góc trung bình $g_z = -22.62\text{ dps}$, âm).
     - **M2 (Quay trái):** Tích lũy góc quay quanh trục Z là **$+87.7^\circ$** (vận tốc góc trung bình $g_z = +29.24\text{ dps}$, dương).
   - Tương quan dấu: Khi xoay cổ tay đưa mũi sang PHẢI, con quay đo được $g_z < 0$; khi xoay cổ tay đưa mũi sang TRÁI, con quay đo được $g_z > 0$.
7. **M3 & M4 (Ngẩng mũi lên / Cúi mũi xuống quanh trục X):**
   - Trục X là trục có biến thiên góc quay chính:
     - **M3 (Ngẩng lên):** Tích lũy góc quay quanh trục X là **$-32.9^\circ$** (vận tốc góc trung bình $g_x = -10.98\text{ dps}$, âm).
     - **M4 (Cúi xuống):** Tích lũy góc quay quanh trục X là **$+37.1^\circ$** (vận tốc góc trung bình $g_x = +12.35\text{ dps}$, dương).
8. **M5 & M6 (Lật nghiêng Phải / Trái quanh trục Y):**
   - Trục Y là trục có biến thiên góc quay chính:
     - **M5 (Lật phải):** Tích lũy góc quay quanh trục Y là **$-71.7^\circ$** (vận tốc góc trung bình $g_y = -23.90\text{ dps}$, âm).
     - **M6 (Lật trái):** Tích lũy góc quay quanh trục Y là **$+53.7^\circ$** (vận tốc góc trung bình $g_y = +17.88\text{ dps}$, dương).
   - Đúng như người dùng nhận xét trực tiếp trong quá trình thử nghiệm ("lật phải trùng với nghiêng phải"), cử động lật nghiêng cổ tay tác động trực tiếp lên trục roll của cảm biến.

---

## 5. Nạp Lại Firmware Chính Thức & Xác Nhận Khởi Động

Thực hiện nạp lại bản firmware chính sẵn có (`firmware/`, bản gain = 0.3 đã build) để hoàn trả bo mạch về trạng thái hoạt động:

- **Kết quả nạp:**
  - Tổng số byte ghi: `1,165,968 bytes` (nén 731,566 bytes) vào địa chỉ `0x10000` trong 78.6 giây ở tốc độ 115200 baud.
  - Xác thực toàn vẹn: `Hash of data verified`, `Hard resetting via RTS pin`.
- **Log khởi động 20 giây (`raw_logs/main_firmware_boot_2026-10-08_after_orient.log`):**
  ```text
  [INIT] Initializing ICM-20948 Sensor Bus (400 kHz)...
  [DIAGNOSTICS] Register Readback Verification:
    -> WHO_AM_I         (Bank 0, 0x00) : 0xEA  [PASS]
    -> PWR_MGMT_1       (Bank 0, 0x06) : 0x01  [PASS]
    -> GYRO_CONFIG_1    (Bank 2, 0x01) : 0x1B  [PASS]
    -> ACCEL_CONFIG     (Bank 2, 0x14) : 0x1B  [PASS]
    -> GYRO_SMPLRT_DIV  (Bank 2, 0x00) : 10     [PASS]
    -> ACCEL_SMPLRT_DIV (Bank 2, 0x10-11): 10  [PASS]

  [CALIBRATION] Commencing 2-second Startup Gyro Bias Calibration...
  [CALIBRATION] Completed in 2200 ms with 200 successful polls (nominal ODR ~102.27 Hz).
  [CALIBRATION] Zero-Rate Bias: X =  -0.56 dps | Y =  -1.48 dps | Z =  +0.38 dps
  [BLE] Starting BLE HID Mouse Advertising as 'AirMouse-ESP32'...
  [SYSTEM] Air Mouse System Ready. Entering 100 Hz Main Loop.
  [  3951][I][BLEDevice.cpp:253] gapEventHandler(): ESP_GAP_BLE_AUTH_CMPL_EVT
  [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
  ```
- **Xác nhận trạng thái:**
  - Khởi tạo phần cứng hoàn hảo (`WHO_AM_I=0xEA`).
  - Ghi nhận sự kiện xác thực ghép nối BLE thành công (`ESP_GAP_BLE_AUTH_CMPL_EVT`).
  - Khi bo mạch nằm yên, hệ thống xuất chu kỳ 100 Hz với `dX: +0, dY: +0` ổn định.

---

## 6. Các Điều Chưa Làm / Chờ Người Dùng & Claude Quyết Định

1. **Sửa chiều trục hoặc ánh xạ trục:** Thuộc quyền quyết định kỹ thuật của Claude sau khi phân tích bảng số liệu mục 3 (đặc biệt là dấu của trục Z cho `dX` và việc hoán đổi trục giữa X và Y cho chuyển động ngẩng/cúi và lật nghiêng).
2. **Tiếp tục tinh chỉnh Gain:** Đánh giá lại mức gain (hiện tại đang là 0.3) sau khi chiều trục được đảo đúng.
3. **Phần cứng nút bấm:** Hàn/gắn nút Clutch tại GPIO27 và hàn cố định dây I2C để tránh rung lỏng tiếp xúc.

---

## 7. Sai Lệch So Với Kế Hoạch Handoff Gốc

1. **Thực hiện Retry 1 cho file log đo:** File log đo ban đầu `orient_2026-10-08.log` với thời gian đặt 420 giây (7 phút) kết thúc khi vừa xong động tác H1 do các khoảng trao đổi hướng dẫn từng bước với người dùng qua giao diện trò chuyện. Toàn bộ tệp đo đợt 1 được giữ nguyên và mở đợt log `orient_2026-10-08_retry1.log` (1200 giây) để hoàn thành trọn vẹn cả 11 động tác với chất lượng tín hiệu tối ưu (`fail = 0`).
2. **Cổng kết nối:** Sử dụng cầu mạng RFC2217 qua Tailscale (`rfc2217://<LAPTOP_IP>:4000?ign_set_control`) do bo mạch được cắm vào máy tính laptop từ xa của người dùng.
