# FIRMWARE CHANGELOG — 2026-10-03

Trạng thái xác minh: **HOST_TESTED** (Đã kiểm chứng unit test và mô phỏng số liệu trên môi trường máy tính; chưa thử nghiệm trên tay người dùng thật; BLE ghép nối `NOT_TESTED`).

> **Cập nhật 2026-10-04 (Claude, việc A):** test N1 đã được sửa (bias dư đặt sai trục), thêm test N7 mô tả giới hạn bias dư, và **mục 5, 6, 8 viết lại** vì bản gốc nói quá nhẹ rủi ro. Firmware **không đổi**; bản gốc test + changelog ở `backups/2026-10-04_sua_test_N1/`. Chưa đo trên board (`NOT_TESTED`).

---

## 1. Tóm tắt thay đổi (4.1 – 4.4)

- **4.1 (Sub-count accumulator)**: Bổ sung bộ cộng dồn phần dư `s_rem_x`, `s_rem_y` ở bước 10 và reset khi clutch / stationary / init / recenter để bảo toàn chuyển động nhỏ dưới 1 count.
- **4.2 (Tightening filter)**: Thay thế vùng chết cắt cứng `apply_deadzone` bằng hàm thắt chặt bậc hai liên tục `apply_tightening(val, threshold)` với ngưỡng 1.4 °/s để phản hồi góc nhỏ mượt mà.
- **4.3 (Ngưỡng đứng yên chặt hơn)**: Thu hẹp ngưỡng phát hiện đứng yên `stat_gyro_thresh` từ 1.2 °/s xuống 0.4 °/s nhằm giải phóng chuyển động tay chậm trong dải [0.4, 1.2] °/s.
- **4.4 (Trì hoãn tự chỉnh bias tĩnh)**: Bổ sung bộ đếm `s_rest_counter` (yêu cầu `AUTO_ZERO_MIN_REST_SAMPLES = 150`), chỉ tự động cập nhật bias `auto_zero` sau khi thiết bị đứng yên liên tục ≥ 1.5 s.

---

## 2. Bảng so sánh trước/sau

Kịch bản đo thực tế: 50 mẫu nằm yên (không nhiễu) sau đó 100 mẫu quay đều quanh trục đứng với tốc độ góc $\omega \in \{0.3, 0.5, 1.0, 1.5, 5.0, 30.0\}\,^\circ/\text{s}$.
Biên dịch độc lập giữa bản sao lưu (`backups/2026-10-03_sua_loc_nhieu/`) và bản mới (`firmware/`):

| $\omega$ (°/s) | Tổng dX trước (Bản sao lưu) | Tổng dX sau (Bản mới) | Nhận xét chi tiết kết quả đo |
| :---: | :---: | :---: | :---|
| **0.3** | 0 | 0 | Dưới ngưỡng đứng yên 0.4 °/s; khóa con trỏ tĩnh đúng chủ đích triệt tiêu nhiễu nghỉ. **Chỉ đúng khi không có nhiễu.** Với nhiễu σ = 0.09 °/s/trục, ω = 0.3 °/s liên tục cho ≈ 161–171 count mỗi 10 s (tương đương bias dư 0.3, xem mục 6) |
| **0.5** | 0 | 39 | **Khắc phục triệt để lỗi nuốt chuyển động**: Trước đây bằng 0 (khóa đứng yên); nay phản hồi 39 counts nhờ tightening và sub-count accumulator |
| **1.0** | 0 | 157 | **Khắc phục triệt để lỗi nuốt chuyển động**: Trước đây bị khóa do $\omega < 1.2\,^\circ/\text{s}$; nay cho 157 counts chuyển động rõ rệt |
| **1.5** | 200 | 330 | Trước đây bị trừ mất 0.8 °/s do deadzone ($(1.5 - 0.8) \times 2.2 \times 100 \approx 200$); nay bảo toàn trọn vẹn $1.5 \times 2.2 \times 100 = 330$ counts |
| **5.0** | 900 | 1100 | Trước đây trừ 0.8 °/s ($(5.0 - 0.8) \times 2.2 \times 100 \approx 900$); nay phản hồi tuyến tính chuẩn xác $5.0 \times 2.2 \times 100 = 1100$ counts |
| **30.0** | 6400 | 6600 | Trước đây trừ 0.8 °/s ($(30.0 - 0.8) \times 2.2 \times 100 \approx 6400$); nay phản hồi tuyến tính chuẩn xác $30.0 \times 2.2 \times 100 = 6600$ counts |

---

## 3. Kết quả test

### 10 test cơ sở (test cũ)
- **Trước khi sửa**: 10/10 PASS
- **Sau khi sửa**: 10/10 PASS (không sửa, không làm yếu bất kỳ assert nào)
  1. `test_register_bitfields`: PASS
  2. `test_driver_semi_register`: PASS
  3. `test_stationary_detection`: PASS
  4. `test_deadzone_and_rotation`: PASS
  5. `test_clutch_and_recenter`: PASS
  6. `test_attitude_and_gravity_removal`: PASS
  7. `test_flick_gesture`: PASS
  8. `test_attitude_convergence_p1a`: PASS
  9. `test_dynamic_dt_and_timing`: PASS
  10. `test_motion_process_end_to_end_gestures_p1b`: PASS

### 7 test bổ sung N1 – N7
Các test chạy với hạt giống ngẫu nhiên cố định (`s_seed = 12345u`; N7 dùng 11/12/13), nhiễu Gauss $\sigma = 0.09\,^\circ/\text{s}$, gia tốc $0.988\,\text{g}$, bias cơ sở $(-0.54, -1.49, 0.32)\,^\circ/\text{s}$:

| Mã test | Tên kịch bản | Số đo thực tế | Ngưỡng đánh giá (ước lượng) | Kết quả |
| :---: | :---| :---: | :---: | :---: |
| **N1** | Nằm yên 1000 mẫu (10 s), bias dư 0.1 °/s trên **gy và gz** (hai trục điều khiển con trỏ) | Tổng $\|dX\| + \|dY\| = \mathbf{5}$, khóa đứng yên 87 % số mẫu | $\le 20$ | **PASS** |
| **N2** | Chậm 1.0 °/s (300 mẫu yên + 200 mẫu quay) | Tổng dX 200 mẫu = $\mathbf{315}$ (kỳ vọng $\approx 314$) | $[250, 380]$ | **PASS** |
| **N3** | Rất chậm 0.5 °/s (300 mẫu yên + 200 mẫu quay) | Tổng dX 200 mẫu = $\mathbf{80}$ (kỳ vọng $\approx 79$) | $[55, 110]$ | **PASS** |
| **N4** | Chống nuốt bởi bias (300 mẫu yên + 1000 mẫu quay 1.0 °/s) | first100 = 157, last100 = 162 (tỷ lệ $\mathbf{103.18\%}$) | $\ge 90\%$ | **PASS** |
| **N5** | Tốc độ cao (1 mẫu $\omega_z = 30.0\,^\circ/\text{s}$, không nhiễu) | $\text{delta\_x} = \mathbf{66}$ (kỳ vọng $66$) | $[65, 67]$ | **PASS** |
| **N6** | Bão hòa (1 mẫu $\omega_z = 70.0\,^\circ/\text{s}$) | $\text{delta\_x} = \mathbf{127}$ | $== 127$ | **PASS** |
| **N7** | **Giới hạn đã biết**: nằm yên 10 s, bias dư trên yaw 0.1 / 0.2 / 0.3 °/s, 3 hạt giống | 0.1: tối đa **3**; 0.2: tối đa **45**; 0.3: **161–171**, khóa đứng yên 0 %, 10 s cuối của 30 s vẫn ≥ **157** | $\le 20$ / $\le 100$ / $[100, 300]$ (+ khóa $\le 5\%$, không tự phục hồi) | **PASS** (mô tả giới hạn, **không phải** chứng nhận chất lượng) |

Tổng hợp toàn bộ test harness: **17/17 TESTS PASSED** (`HOST_TESTED`).

**Đính chính test N1 (2026-10-04).** Bản N1 ngày 2026-10-03 đặt bias dư 0.1 °/s ở **trục X (roll)**. Trục này không điều khiển con trỏ (chỉ `gz`→dX, `gy`→dY), nên kết quả "0 count" đúng nhưng không kiểm tra được gì. Lỗi nằm ở đặc tả handoff, không phải ở Anti. N1 mới đặt bias dư trên `gy` và `gz`. N7 là test mới và **cố ý mô tả hành vi hạn chế hiện tại**: nếu sau này chỉnh ngưỡng đứng yên hoặc thêm hiệu chuẩn lại thì N7 sẽ FAIL đúng chủ đích. Khi đó cập nhật cận và changelog, không nới lỏng âm thầm. (Đã kiểm tra: với bản firmware đột biến đặt `stat_gyro_thresh = 1.2`, N7 FAIL vì chỉ còn 4–5 count ở 0.3 °/s.)

---

## 4. Build Firmware (PlatformIO)

Lệnh thực thi: `python -m platformio run -d firmware`
Kết quả: **SUCCESS**
- **RAM**: 12.1% (đã dùng 39,636 bytes / 327,680 bytes)
- **Flash**: 88.4% (đã dùng 1,159,037 bytes / 1,310,720 bytes)
- **Target**: `esp32dev` (board: `esp32doit-devkit-v1`, framework: `arduino`, platform: `espressif32 @ 7.1.3`)

---

## 5. Hành vi đã thay đổi cần người dùng biết

- Ở tốc độ cao, con trỏ chuột di chuyển nhanh hơn một chút (ví dụ ở 30 °/s: xuất ra 66 counts thay vì 64 counts mỗi chu kỳ) do thuật toán tightening không còn trừ cố định 0.8 °/s như cơ chế deadzone cũ.
- Khóa đứng yên chỉ hoạt động khi **30 mẫu liên tiếp** (≈ 0.3 s) đều có $\sqrt{g_x^2+g_y^2+g_z^2} < 0.4\,^\circ/\text{s}$ sau khi trừ bias hiệu chuẩn. Mệnh đề "$\omega < 0.4\,^\circ/\text{s}$ bị khóa hoàn toàn" **chỉ đúng khi không có nhiễu và bias đúng bằng giá trị hiệu chuẩn**. Với nhiễu thật $\sigma = 0.09\,^\circ/\text{s}$/trục: bias đúng thì khóa 93–97 % số mẫu và 0 count; nhưng chỉ cần lệch 0.2–0.3 °/s thì chuỗi 30 mẫu liên tiếp hay gãy và khóa mất tác dụng (số đo ở mục 6). Một chuyển động thật chậm ≈ 0.3 °/s kéo dài cũng được pipeline nhìn như bias dư 0.3 và cho cùng kết quả (con trỏ chạy chậm chứ không đứng yên).
- Hệ quả thiết kế: bản mới đổi "chống trôi bằng cách khóa mạnh" lấy "cho phép chuyển động chậm"; cái giá là **nhạy với bias lệch** và **không tự phục hồi** khi lệch quá 0.2–0.3 °/s (mục 6).

---

## 6. Rủi ro còn lại

> **Bản ghi 2026-10-03 đã bị thay thế (nói quá nhẹ).** Nguyên văn đã ghi: "nếu bias lệch quá 0.4 °/s so với giá trị hiệu chuẩn thì không còn được coi là đứng yên, con trỏ sẽ trôi chậm (ví dụ bias dư 0.5 °/s trôi khoảng 39 đơn vị/s) và bias không tự sửa được". Sai ở chỗ: **ngưỡng rủi ro thật là 0.2–0.3 °/s chứ không phải 0.4**, vì nhiễu 0.09 °/s/trục làm gãy chuỗi 30 mẫu trước khi bias dư chạm 0.4. Con số "39 đơn vị/s" là kết quả không nhiễu ($0.5^2/1.4 \times 2.2 \times 100 \approx 39$); có nhiễu thì đo được ≈ 41–42/s.

**Rủi ro:** nếu bias gyro thật lệch khỏi giá trị hiệu chuẩn lúc khởi động **từ 0.2–0.3 °/s trở lên trên trục yaw hoặc pitch**, khóa đứng yên không còn bám được, con trỏ **tự trôi khi tay đứng yên**, và vì bias chỉ tự chỉnh khi đã đứng yên liên tục ≥ 1.5 s nên **không tự phục hồi**. Chỉ hiệu chuẩn lại (khởi động lại board khi đặt yên) mới sửa được. Bản firmware cũ (ngưỡng đứng yên 1.2 °/s, sao lưu ở `backups/2026-10-03_sua_loc_nhieu/`) không có rủi ro này: chạy lại cùng mô phỏng, mọi hàng trong bảng dưới đều cho 0 count. Cái giá của bản cũ là nuốt chuyển động chậm, đúng lo ngại của thầy.

Mô phỏng `HOST_TESTED`: nằm yên 10 s, nhiễu $\sigma = 0.09\,^\circ/\text{s}$/trục, bias dư đặt **trên trục điều khiển con trỏ**, tổng $|dX|+|dY|$ (đơn vị count HID tương đối), phạm vi 3 hạt giống:

| Bias dư trên yaw (°/s) | Tổng count / 10 s | % mẫu được khóa đứng yên | Đánh giá |
| :---: | :---: | :---: | :--- |
| 0.0 | 0 | 93–97 % | Bình thường |
| 0.1 | 1–3 | 90–97 % | Chấp nhận được (N1, N7) |
| **0.2** | **27–45** | 42–61 % | Vùng chuyển tiếp, bắt đầu thấy trôi |
| **0.3** | **161–171** (≈ 17/s) | 0 % | Vượt ngưỡng, không tự phục hồi (N7) |
| 0.4 | 271–281 | 0 % | Trôi rõ |
| 0.5 | 413–422 (≈ 42/s) | 0 % | Trôi rõ |
| 0.8 | 1 028–1 034 | 0 % | Trôi nặng |

Bias dư đồng thời trên pitch **và** yaw (mỗi trục `r`, một hạt giống): `r` = 0.1 → 2 count/10 s; 0.2 → 152; 0.3 → 309. Hai trục cộng lại nên ngưỡng thực tế còn thấp hơn so với một trục.

**Điều đã đo là tốt:** bias trôi **từ từ** (tăng tuyến tính từ 0 đến 0.3 / 0.6 / 1.0 °/s trong 120 s, nằm yên) cho **0 count**, khóa 99 % số mẫu, vì bias tự chỉnh kịp bám. Nguy cơ nằm ở **bước nhảy đột ngột** của bias, ví dụ hiệu chuẩn lúc board chưa ổn định nhiệt rồi sau đó nóng lên (datasheet ZRO ±0.05 °/s/°C). Phần này là **suy luận từ mô phỏng, chưa đo trên board** (`NOT_TESTED`); việc B trong handoff (đo trôi bias thật khoảng 10 phút) sẽ trả lời.

Cách khắc phục đã đề xuất, chưa làm: hiệu chuẩn lại bằng giữ Clutch ≥ 2 s (việc C); thử nâng ngưỡng đứng yên lên ≈ 0.5–0.6 °/s sau khi có số đo thật (việc D, đánh đổi: mất cử động dưới ≈ 0.5 °/s); kẹp bias ≤ 0.5 °/s so với lúc hiệu chuẩn. Chưa thử với tay người thật, BLE ghép nối `NOT_TESTED`.

---

## 7. Việc cho giai đoạn sau (chưa làm)

1. Nghiên cứu bộ lọc làm mượt thích ứng mềm (soft tiered smoothing) để giảm rung tay sinh lý.
2. Thiết lập cơ chế kẹp an toàn mức sai lệch bias $\le 0.5\,^\circ/\text{s}$ so với giá trị hiệu chuẩn ban đầu.
3. Thêm tính năng giữ nút Clutch kéo dài để kích hoạt hiệu chuẩn lại bias nhanh chóng.
4. Tinh chỉnh thực nghiệm các ngưỡng trên người dùng thực tế với kết nối BLE HID hoàn chỉnh.

---

## 8. Sai lệch so với handoff này

Bản 2026-10-03 ghi "Không có". Thực tế có hai điểm, đã sửa ngày 2026-10-04:

1. Test N1 theo đặc tả đặt bias dư ở trục X (roll), không điều khiển con trỏ → "0 count" vô nghĩa. Đã sửa sang `gy`/`gz` (mục 3).
2. Mục 5 và 6 nêu ngưỡng rủi ro 0.4 °/s; ngưỡng đo được là 0.2–0.3 °/s khi có nhiễu (mục 5, 6).

Việc 1 là lỗi của đặc tả, không phải của người thực hiện firmware.
