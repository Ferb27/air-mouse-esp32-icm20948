# BÁO CÁO ĐO ĐẠC TRÔI BIAS CON QUAY (GYRO BIAS DRIFT) TRÊN PHẦN CỨNG THẬT

- **Ngày thực hiện:** 2026-10-08 (Theo mốc tài liệu kế hoạch: 2026-10-04)
- **Đối tượng kiểm nghiệm:** Bo mạch Air Mouse (ESP32 Classic DevKit 38-pin + Breakout ICM-20948 WCMCU-20948)
- **Trạng thái xác thực:** `BENCH_VERIFIED` (chỉ áp dụng cho các giá trị đo được trên bo mạch này, cấp nguồn USB tại bàn thử nghiệm). BLE ghép nối với máy tính: `NOT_TESTED`.

---

## 1. Điều Kiện Đo Đạc

- **Bề mặt & tư thế:** Bo mạch được đặt cố định, phẳng trên mặt bàn làm việc, không di chuyển trong suốt thời gian đo.
- **Nguồn cấp:** Cấp nguồn 5V qua cổng Micro-USB từ máy tính xách tay (chưa sử dụng pin LiPo 1S và mạch sạc/nâng áp TP4056/MT3608).
- **Cổng kết nối:** ESP32 cắm vào cổng USB (COM3) của máy laptop từ xa, được điều khiển và thu thập log thông qua cầu nối mạng RFC2217 (`rfc2217://<LAPTOP_IP>:4000?ign_set_control`) qua giao diện Tailscale.
- **Nhiệt độ môi trường & thông gió:** Theo khai báo của người dùng tại thời điểm đo: nhiệt độ phòng ở mức bình thường, cảm nhận thoải mái không nóng; không bật quạt gió và không mở điều hòa nhiệt độ.
- **Lần đo A (Warm start - khởi động nóng):**
  - Board đã được cắm nguồn hoạt động liên tục trước đó.
  - Bắt đầu: `14:26:38` (2026-10-08)
  - Kết thúc: `14:38:42` (2026-10-08)
  - Tổng thời gian đo: 720 giây (~12 phút).
- **Thời gian làm nguội giữa 2 lần đo:**
  - Thời điểm rút cáp USB: `14:38:59`
  - Thời điểm cắm lại cáp USB: `14:46:28`
  - Tổng thời gian ngắt nguồn để cảm biến nguội tự nhiên: **~7.5 phút** (khoảng 449 giây).
- **Lần đo B (Cold start - khởi động nguội):**
  - Board được cắm điện lại sau 7.5 phút nghỉ và tiến hành hiệu chuẩn 2 giây ngay khi cấp điện.
  - Bắt đầu: `14:47:12` (2026-10-08)
  - Kết thúc: `14:59:16` (2026-10-08)
  - Tổng thời gian đo: 720 giây (~12 phút).

---

## 2. Danh Sách Tệp & Mã Băm Toàn Vẹn SHA-256 (64 Ký Tự)

Tất cả các tệp dữ liệu thô (raw log) và tệp kết quả phân tích được bảo toàn nguyên vẹn với mã băm SHA-256 chính xác:

| Tệp | SHA-256 Checksum | Mô tả |
| :--- | :--- | :--- |
| `raw_logs/bias_drift_2026-10-04_A_warm.log` | `ea8949d51c39425094b5f1b9880e2110d83012493133e5dd175e897c5190af4b` | Lần A khởi chạy đầu tiên, bị dừng sớm tại t=0s do lỏng dây I2C (`WHO_AM_I=0x00`). Lưu giữ nguyên vẹn không ghi đè. |
| `raw_logs/bias_drift_2026-10-04_A_warm_retry1.log` | `92f7ac4c63bbcf0d41eeb740230c7432871c87bf655da41eef35e2ed836285e3` | Lần A chạy lại thành công trọn vẹn 720 giây sau khi cắm chặt lại dây cảm biến. |
| `raw_logs/bias_drift_2026-10-04_B_cold.log` | `43c5ea4c9e7569889e8b3cc611afd2bc2b64c71aef5093a8ccd5992e1a4e919f` | Lần B (khởi động nguội sau 7.5 phút làm nguội), hoàn thành trọn vẹn 720 giây. |
| `raw_logs/main_firmware_boot_com3_2026-10-04.log` | `0744058e0848f0a36a38f6c77483e2efd0f59ad912f1d5f04941eb3e919fa9e7` | Log khởi động và chạy kiểm tra 20 giây của firmware chính thức sau khi nạp hoàn trả bo mạch. |
| `docs/bias_drift_analysis_2026-10-04_A_warm.txt` | `d22bbdf1d7066c4a4c62b2ff34b40b5707c77943a0585968aa41f89c7fdc65a1` | Kết xuất phân tích thống kê của `analyze_bias_drift.py` cho Lần A. |
| `docs/bias_drift_analysis_2026-10-04_B_cold.txt` | `16897e257b955a58cdbe4aa5c1eeef693e5f0e899a86bf0bee5f9438cb40fb6eb` | Kết xuất phân tích thống kê của `analyze_bias_drift.py` cho Lần B. |

---

## 3. Kết Quả Đo Lần A và Lần B

### 3.1. Kết Quả Lần A (Warm Start - file `raw_logs/bias_drift_2026-10-04_A_warm_retry1.log`)

Hiệu chuẩn ban đầu tại khởi động:
`[CAL] bias_x=-0.5473 bias_y=-1.4521 bias_z=+0.3484 dps polls=200 elapsed_ms=2199 temp=32.60`

#### Khối SUMMARY (Dán nguyên bản từ script phân tích):
```text
SUMMARY
die temperature: first 10 s avg 32.54 C -> last 10 s avg 32.74 C (delta +0.20 C)
rx(roll,no cursor)   first-30s avg -0.003 | last-60s avg -0.007 | change -0.003 dps | max |10s mean| 0.016 at t~703s | slope -0.0000 dps/min
ry(pitch->dY)        first-30s avg +0.003 | last-60s avg -0.021 | change -0.024 dps | max |10s mean| 0.029 at t~704s | slope -0.0019 dps/min
rz(yaw->dX)          first-30s avg -0.002 | last-60s avg -0.001 | change +0.001 dps | max |10s mean| 0.015 at t~647s | slope +0.0004 dps/min
noise (mean per-second std-dev): gx 0.104  gy 0.104  gz 0.090 dps (bench 2026-10-01: ~0.09)
windows (10 s mean) where max(|ry|,|rz|) >= 0.1: 0 of 711
windows (10 s mean) where max(|ry|,|rz|) >= 0.2: 0 of 711
windows (10 s mean) where max(|ry|,|rz|) >= 0.3: 0 of 711
largest max(|ry|,|rz|) of any 10 s mean: 0.029 dps
possible disturbance (any per-second std-dev > 0.25 dps, i.e. touch/vibration): 22 s, at t = [14, 30, 96, 228, 239, 252, 291, 325, 365, 439, 488, 489, 502, 508, 518] ...
```

#### Khối REAL PIPELINE (Dán nguyên bản từ script phân tích):
```text
REAL PIPELINE (production motion_process, clutch released): total |dX|+|dY| = 803 counts in 720 s; reported stationary 85.1% of samples
WORST CASE (fixed startup calibration, no auto-zero): stationary lock would hold 85.0% of samples
pipeline bias estimate: start (-0.547,-1.452,+0.348) -> end (-0.552,-1.476,+0.346) dps
```

#### Bảng Theo Từng Phút (Lần A):
```text
min | temp_end | rx      ry      rz     | max|10s-mean| rx   ry   rz  | cnt(sum) | stat%  | fixlock%
  1 |    32.69 | -0.003 +0.003 -0.001 | 0.008 0.009 0.008 |       61 |  79.5  |  79.5
  2 |    32.69 | -0.003 -0.001 -0.003 | 0.010 0.010 0.012 |       45 |  86.1  |  85.7
  3 |    32.50 | -0.002 +0.004 -0.005 | 0.012 0.012 0.011 |       19 |  89.1  |  89.1
  4 |    32.79 | -0.005 -0.001 -0.005 | 0.013 0.008 0.013 |       73 |  93.7  |  93.7
  5 |    32.50 | -0.005 -0.010 -0.001 | 0.013 0.015 0.013 |       96 |  81.9  |  81.3
  6 |    32.65 | -0.001 -0.009 -0.000 | 0.007 0.015 0.012 |       62 |  87.7  |  87.3
  7 |    32.69 | -0.004 -0.009 -0.006 | 0.012 0.015 0.011 |       42 |  93.4  |  93.1
  8 |    32.60 | -0.001 -0.011 -0.002 | 0.009 0.019 0.011 |       20 |  92.0  |  91.6
  9 |    32.79 | +0.001 -0.008 +0.004 | 0.008 0.019 0.015 |       73 |  90.2  |  91.1
 10 |    32.79 | -0.003 -0.013 -0.001 | 0.011 0.023 0.006 |      121 |  68.7  |  68.9
 11 |    32.65 | -0.002 -0.014 +0.002 | 0.010 0.020 0.015 |      175 |  65.2  |  65.6
 12 |    32.65 | -0.007 -0.021 -0.001 | 0.016 0.029 0.012 |       16 |  93.6  |  93.6
```

---

### 3.2. Kết Quả Lần B (Cold Start - file `raw_logs/bias_drift_2026-10-04_B_cold.log`)

Hiệu chuẩn ban đầu tại khởi động:
`[CAL] bias_x=-0.6039 bias_y=-1.4399 bias_z=+0.3633 dps polls=200 elapsed_ms=2199 temp=32.84`

#### Khối SUMMARY (Dán nguyên bản từ script phân tích):
```text
SUMMARY
die temperature: first 10 s avg 32.76 C -> last 10 s avg 32.87 C (delta +0.11 C)
rx(roll,no cursor)   first-30s avg -0.003 | last-60s avg -0.008 | change -0.005 dps | max |10s mean| 0.018 at t~699s | slope -0.0009 dps/min
ry(pitch->dY)        first-30s avg -0.006 | last-60s avg -0.044 | change -0.038 dps | max |10s mean| 0.054 at t~571s | slope -0.0036 dps/min
rz(yaw->dX)          first-30s avg +0.002 | last-60s avg +0.001 | change -0.002 dps | max |10s mean| 0.057 at t~347s | slope -0.0004 dps/min
noise (mean per-second std-dev): gx 0.110  gy 0.135  gz 0.093 dps (bench 2026-10-01: ~0.09)
windows (10 s mean) where max(|ry|,|rz|) >= 0.1: 0 of 702
windows (10 s mean) where max(|ry|,|rz|) >= 0.2: 0 of 702
windows (10 s mean) where max(|ry|,|rz|) >= 0.3: 0 of 702
largest max(|ry|,|rz|) of any 10 s mean: 0.057 dps
possible disturbance (any per-second std-dev > 0.25 dps, i.e. touch/vibration): 69 s, at t = [115, 117, 119, 120, 126, 127, 131, 132, 262, 268, 271, 276, 277, 281, 293] ...
```

#### Khối REAL PIPELINE (Dán nguyên bản từ script phân tích):
```text
REAL PIPELINE (production motion_process, clutch released): total |dX|+|dY| = 2428 counts in 711 s; reported stationary 81.1% of samples
WORST CASE (fixed startup calibration, no auto-zero): stationary lock would hold 80.2% of samples
pipeline bias estimate: start (-0.604,-1.440,+0.363) -> end (-0.614,-1.483,+0.365) dps
```

#### Bảng Theo Từng Phút (Lần B):
```text
min | temp_end | rx      ry      rz     | max|10s-mean| rx   ry   rz  | cnt(sum) | stat%  | fixlock%
  1 |    33.12 | -0.003 -0.005 +0.002 | 0.008 0.012 0.006 |        6 |  95.8  |  95.4
  2 |    33.03 | +0.000 -0.014 -0.003 | 0.016 0.019 0.009 |      141 |  91.3  |  91.3
  3 |    33.12 | +0.001 -0.017 +0.003 | 0.009 0.024 0.010 |      196 |  90.4  |  90.3
  4 |    32.79 | +0.002 -0.022 +0.006 | 0.010 0.029 0.013 |       32 |  89.1  |  89.4
  5 |    32.79 | +0.000 -0.011 +0.003 | 0.009 0.016 0.010 |      315 |  64.0  |  62.7
  6 |    32.69 | -0.003 -0.029 +0.006 | 0.010 0.037 0.057 |      555 |  57.4  |  56.2
  7 |    32.79 | -0.006 -0.029 -0.006 | 0.016 0.036 0.010 |       64 |  84.3  |  83.2
  8 |    32.65 | -0.006 -0.033 -0.003 | 0.013 0.040 0.011 |      146 |  87.6  |  86.6
  9 |    32.79 | -0.009 -0.041 +0.001 | 0.017 0.046 0.011 |       91 |  86.5  |  85.9
 10 |    33.03 | -0.007 -0.046 -0.005 | 0.013 0.054 0.012 |      132 |  80.7  |  78.3
 11 |    32.79 | -0.009 -0.039 -0.000 | 0.014 0.047 0.008 |      341 |  81.9  |  80.2
 12 |    32.79 | -0.007 -0.044 +0.000 | 0.018 0.050 0.007 |      409 |  60.9  |  59.1
```

---

## 4. So Sánh Lần A và Lần B

1. **Nhiệt độ die cảm biến:** Nhiệt độ die nội tại cảm biến ở Lần A (khởi động nóng) tăng từ mức trung bình 10 giây đầu $32.54^\circ\text{C}$ lên 10 giây cuối $32.74^\circ\text{C}$ ($\Delta = +0.20^\circ\text{C}$); ở Lần B (khởi động nguội sau 7.5 phút ngắt điện) tăng từ $32.76^\circ\text{C}$ lên $32.87^\circ\text{C}$ ($\Delta = +0.11^\circ\text{C}$).
2. **Độ dịch chuyển bias:** Độ trôi bias trên trục pitch ($g_y \to dY$) giữa 30 giây đầu và 60 giây cuối là $-0.024\text{ dps}$ ở Lần A và $-0.038\text{ dps}$ ở Lần B; trên trục yaw ($g_z \to dX$) là $+0.001\text{ dps}$ ở Lần A và $-0.002\text{ dps}$ ở Lần B.
3. **Đỉnh trôi trung bình 10 giây:** Giá trị cực đại của cửa sổ trôi 10 giây $\max(|r_y|, |r_z|)$ đạt $0.029\text{ dps}$ (ở giây thứ 704) tại Lần A, và đạt $0.057\text{ dps}$ (ở giây thứ 347) tại Lần B; cả hai lần đều ghi nhận $0\text{ / }711$ và $0\text{ / }702$ cửa sổ vượt ngưỡng $0.1\text{ dps}$.
4. **Xung tích lũy pipeline thực tế:** Tổng số xung chuột $|dX| + |dY|$ do pipeline thật sinh ra trong suốt thời gian nằm yên là $803\text{ counts}$ ở Lần A (tỷ lệ đứng yên $85.1\%$) và $2428\text{ counts}$ ở Lần B (tỷ lệ đứng yên $81.1\%$), chủ yếu tích tụ vào các thời điểm ghi nhận dao động cơ học ngoại vi trên mặt bàn (Lần B xuất hiện 69 giây có độ lệch chuẩn $> 0.25\text{ dps}$).

---

## 5. Đánh Giá Kỹ Thuật & Giới Hạn Đo Đạc

### 5.1. Đánh Giá Dựa Trên Thang Đo Mô Phỏng
- **Thang đối chiếu mô phỏng** (độ nhiễu $0.09\text{ dps}$, bias dư trên yaw, số count sinh ra trong 10 giây nằm yên theo `docs/FIRMWARE_CHANGELOG_2026-10-03.md` mục 6):
  - $0.1\text{ dps} \to 1\text{--}3\text{ counts}$
  - $0.2\text{ dps} \to 27\text{--}45\text{ counts}$
  - $0.3\text{ dps} \to 161\text{--}171\text{ counts}$
  - $0.5\text{ dps} \to \approx 415\text{ counts}$
- **Kết luận đánh giá theo quy chuẩn câu chữ cho phép:**
  > "Bias lệch tối đa **0.029 °/s** (Lần A) và **0.057 °/s** (Lần B) so với hiệu chuẩn, **nằm trong vùng chịu được của mô phỏng, trong lần đo này**."

### 5.2. Danh Sách Giới Hạn Bắt Buộc (4 Ý Bắt Buộc Theo Handoff)
1. **Chưa bật BLE khi đo:** Chương trình đo `firmware_bias_drift` không bật sóng Bluetooth Low Energy (BLE) để cô lập dữ liệu UART; firmware thật có bật BLE HID nên ESP32 sẽ phát nhiệt và tạo nhiễu gợn nguồn khác, độ trôi bias thực tế khi phát sóng có thể sẽ khác.
2. **Nguồn cấp:** Nguồn đo là cổng USB 5V máy tính, chưa phải là nguồn pin LiPo 1S kết hợp module sạc TP4056 và mạch nâng áp/ổn áp MT3608.
3. **Quy mô mẫu thử:** Phép đo được thực hiện trên **1 bo mạch**, gồm **2 lần đo** (1 warm, 1 cold), trong **cùng một ngày**, ở nhiệt độ phòng cụ thể như đã khai báo. **Không ngoại suy** cho các bo mạch khác hoặc các dải nhiệt độ môi trường khắc nghiệt khác.
4. **Chưa thử nghiệm trên tay người:** Bo mạch nằm cố định trên bàn phẳng; hiện tượng rung tự nhiên của bàn tay người khi cầm thiết bị trong không gian chưa được đưa vào phép đo này.

---

## 6. Khôi Phục Firmware Chính Thức & Xác Nhận Khởi Động

Sau khi hoàn tất thu thập dữ liệu đo trôi bias, bo mạch đã được nạp lại firmware chính thức (`firmware/`) mang bộ lọc đã tinh chỉnh ngày 03/10/2026.

### 6.1. Kết Quả Biên Dịch & Nạp Flash
- **Thời gian build:** 2.60 giây (`SUCCESS`)
- **Tài nguyên RAM:** `39,636 bytes` / `327,680 bytes` (chiếm 12.1%)
- **Tài nguyên Flash:** `1,159,037 bytes` / `1,310,720 bytes` (chiếm 88.4%)
- **Nạp chương trình:** Hoàn tất ghi 1,165,616 bytes flash qua RFC2217 trong 64.65 giây, hash xác thực đạt 100%, tự động hard reset qua chân RTS.

### 6.2. Log Khởi Động 20 Giây (`raw_logs/main_firmware_boot_com3_2026-10-04.log`)
Các dòng kiểm tra quan trọng trích xuất từ log:
```text
[INIT] Initializing ICM-20948 Sensor Bus (400 kHz)...
[DIAGNOSTICS] Register Readback Verification:
  -> WHO_AM_I         (Bank 0, 0x00) : 0xEA  [PASS]
  -> PWR_MGMT_1       (Bank 0, 0x06) : 0x01  [PASS] (CLKSEL=Auto-PLL, SLEEP=0)
  -> GYRO_CONFIG_1    (Bank 2, 0x01) : 0x1B  [PASS] (FS=500dps, DLPF=51.2Hz)
  -> ACCEL_CONFIG     (Bank 2, 0x14) : 0x1B  [PASS] (FS=4g, DLPF=50.4Hz [011])
  -> GYRO_SMPLRT_DIV  (Bank 2, 0x00) : 10     [PASS] (ODR ~ 102.27 Hz)
  -> ACCEL_SMPLRT_DIV (Bank 2, 0x10-11): 10  [PASS] (ODR ~ 102.27 Hz, synced)

[CALIBRATION] Commencing 2-second Startup Gyro Bias Calibration...
[CALIBRATION] Please leave the device completely STATIONARY on the table.
[CALIBRATION] Completed in 2200 ms with 200 successful polls (nominal ODR ~102.27 Hz).
[CALIBRATION] Zero-Rate Bias: X =  -0.60 dps | Y =  -1.49 dps | Z =  +0.38 dps
[BLE] Starting BLE HID Mouse Advertising as 'AirMouse-ESP32'...
[SYSTEM] Air Mouse System Ready. Entering 100 Hz Main Loop.
```

### 6.3. Trạng Thái Hoạt Động Khi Nằm Yên
Các dòng trạng thái chu kỳ 1 Hz khi bo mạch nằm yên trên bàn:
```text
[15:04:16.044] [STATUS] Rate: 92 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:17.047] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:18.045] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:19.046] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:20.044] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:21.046] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:22.045] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:23.047] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:24.044] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:25.045] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:26.046] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:27.048] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:28.045] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:29.045] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:30.045] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:31.044] [STATUS] Rate: 100 Hz | Stat: 0 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
[15:04:32.045] [STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.38
```
- **Hành vi con trỏ:** Toàn bộ các dòng log đều ghi nhận `dX: +0, dY: +0`, con trỏ chuột không phát sinh bất kỳ bước trôi ngoài ý muốn nào khi bo mạch nằm yên.
- **Trạng thái Stat:** Giá trị `Stat` dao động giữa `1` và `0` khi bo mạch nằm yên (phản ánh đặc tính phát hiện trạng thái đứng yên ở ngưỡng sàn nhiễu tự nhiên nhạy cảm).
- **Lưu ý BLE:** Ghép nối BLE với thiết bị máy tính thực tế vẫn ở trạng thái **`NOT_TESTED`**.

---

## 7. Các Hạng Mục Chưa Làm / Chờ Người Dùng Quyết Định

1. **Hạng mục C:** Cơ chế nhấn giữ nút Clutch (nút Air Mouse ON/OFF) trong thời gian dài để thực hiện tái hiệu chuẩn bias tức thời khi đang cầm trên tay mà không cần khởi động lại bo mạch.
2. **Hạng mục D:** Tinh chỉnh ngưỡng phát hiện trạng thái đứng yên (`STATIONARY_THRESH_DPS`) nếu quá trình sử dụng thực tế cầm tay đòi hỏi ngưỡng thích ứng khác.
3. **Đo đạc có BLE phát sóng:** Thực hiện bài đo trôi bias tương tự nhưng có bật BLE truyền dữ liệu liên tục để kiểm tra tác động nhiệt và nguồn của sóng vô tuyến ESP32.
4. **Đo đạc bằng pin LiPo:** Đo trôi bias khi cấp nguồn độc lập từ pin LiPo 1S qua mạch sạc TP4056 và module ổn áp.
5. **Đồng bộ tài liệu báo cáo:** Cập nhật các kết quả đo đạc thực tế này vào các tài liệu kiến trúc phần cứng và báo cáo giữa kỳ (chưa thực hiện trong phạm vi nhiệm vụ này).

---

## 8. Ghi Nhận Sai Lệch So Với Kế Hoạch Handoff Gốc

1. **Giao thức kết nối COM:** Do bo mạch được cắm vào máy tính xách tay của người dùng tại địa điểm từ xa, kết nối nối tiếp được thực hiện qua giao thức RFC2217 qua mạng riêng ảo Tailscale (`rfc2217://<LAPTOP_IP>:4000?ign_set_control`) thay vì mở cổng COM3 cục bộ trực tiếp trên máy chủ chạy agent. Tốc độ baud và cơ chế reset chân RTS đều hoạt động tương đương.
2. **Mã băm file công cụ đo:** Tệp `scripts/capture_serial.py` tại thời điểm bắt đầu phiên làm việc đã có mã băm SHA-256 bắt đầu bằng `c3675d7c86a9b2c4` (được tạo trước lúc 13:39:17 ngày 2026-10-08) thay vì `079fedcf5359168c` như ghi trong bảng kế hoạch của Claude. Toàn bộ mã nguồn tệp được giữ nguyên không chỉnh sửa.
3. **Lần đo A phải thực hiện lại (Retry 1):** Lần đo A ban đầu dừng sớm ở $t=0\text{s}$ do lỏng chân kết nối I2C khiến chip phản hồi `WHO_AM_I=0x00` (được lưu giữ nguyên vẹn tại `raw_logs/bias_drift_2026-10-04_A_warm.log`). Sau khi người dùng cắm lại dây phần cứng chắc chắn, lần chạy A hợp lệ được ghi vào `raw_logs/bias_drift_2026-10-04_A_warm_retry1.log` và hoàn thành đủ 720 giây.
