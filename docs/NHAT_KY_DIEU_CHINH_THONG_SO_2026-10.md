# NHẬT KÝ ĐIỀU CHỈNH THÔNG SỐ VÀ KIỂM THỬ (03/10 – 14/10/2026)

> Dùng để báo cáo thầy về **quá trình làm sau giữa kỳ**: đã đổi gì, vì sao, đo bằng cách nào, kết quả ra sao, và còn thiếu gì. Mọi con số dưới đây lấy từ log/test đã lưu trong dự án (cột "Bằng chứng"). Nhãn trạng thái: `HOST_TESTED` = chạy trên máy tính, `BENCH_VERIFIED` = đo trên board thật, `USER_FEEDBACK` = ý kiến người dùng khi cầm thử, `NOT_TESTED` = chưa thử.

## 1. Tóm tắt một đoạn (nói với thầy)

Sau giữa kỳ thầy hỏi bộ lọc nhiễu có "nuốt" chuyển động nhỏ không. Em kiểm tra thì đúng một phần, nên em **sửa bộ lọc** (bỏ vùng chết cứng, thu hẹp ngưỡng đứng yên) và **đo thật** trên board để kiểm chứng thay vì chỉ tin mô phỏng. Khi cầm thử bằng tay thì phát hiện thêm ba lỗi mà mô phỏng không thấy: **độ nhạy quá lớn (~10 lần)**, **trục cảm biến lắp lệch so với giả định của phần mềm (chiều ngang bị ngược, chiều dọc bị điều khiển bằng nghiêng cổ tay)**, và **hiệu chuẩn lúc bật nguồn bị sai nếu đang cầm board, làm con trỏ trôi**. Mỗi lỗi em đo, tìm nguyên nhân, sửa, rồi kiểm lại bằng log. Hiện người dùng cầm thử thấy điều khiển tốt (một buổi thử, `USER_FEEDBACK`).

## 2. Dòng thời gian: vấn đề → đo → sửa → kiểm chứng

| Ngày | Vấn đề / câu hỏi | Cách tìm nguyên nhân | Thay đổi | Kiểm chứng |
| --- | --- | --- | --- | --- |
| 03/10 | Thầy: bộ lọc có nuốt chuyển động nhỏ, chậm không? | Đọc code: 3 nguyên nhân thật (vùng chết cứng 0.8/1.4 °/s; khóa đứng yên ở 1.2 °/s; làm tròn mỗi mẫu bỏ phần dư) | Bỏ vùng chết, dùng "tightening"; khóa đứng yên 1.2 → 0.4 °/s; cộng dồn phần dư; chỉ tự chỉnh bias sau khi yên ≥ 1.5 s | `HOST_TESTED`: 0.5 °/s trước 0 count, sau 39 count/100 mẫu; 1.0 °/s: 0 → 157 (gain cũ 2.2) |
| 04/10 | Bản mới có nhạy với bias lệch không? Test N1 cũ đặt sai trục | Chạy mô phỏng có nhiễu thật (σ = 0.09 °/s) với bias dư trên trục điều khiển con trỏ | Sửa test N1 (đặt bias dư ở gy/gz, không phải gx); thêm N7 mô tả giới hạn; sửa changelog (ngưỡng rủi ro thật 0.2–0.3 °/s, không phải 0.4) | `HOST_TESTED`: 0.1 °/s → 1–3 count/10 s; 0.2 → 27–45; 0.3 → 161–171 (gain 2.2) |
| 04–08/10 | Bias thật của board có trôi vượt ngưỡng đó không? | Chương trình đo riêng, chạy **pipeline thật** trên dữ liệu thật 12 phút, hai lần (A: đang cắm điện; B: rút điện 7.5 phút) | Không đổi firmware | `BENCH_VERIFIED`: bias lệch tối đa 0.029 (A) và 0.057 (B) °/s, thấp hơn nhiều ngưỡng rủi ro; nhưng count nằm yên 803/2428 chủ yếu do **rung bàn**, và die chỉ ấm +0.1–0.2 °C |
| 08/10 | Người dùng thử: quá nhạy, không điều khiển được | Tính từ code: gain 2.2 × 100 Hz = ~220 count/độ; 1920 pixel chỉ cần ~9° | **gain 2.2 → 0.3** (~30 count/độ); thêm lệnh chỉnh lúc chạy `+` / `-` | `HOST_TESTED`; người dùng thấy "tốt hơn nhưng chưa ổn" |
| 08/10 | Vẫn không điều khiển được; không biết cầm hướng nào | **Đo hướng trục**: cầm kiểu điều khiển TV, làm 11 cử động chuẩn (ngẩng/cúi/nghiêng/quay phải/quay trái…), ghi gia tốc kế + con quay 10 lần/giây | Ánh xạ trục + đảo dấu chiều ngang (mục 4) | `BENCH_VERIFIED` + **phát lại dữ liệu thật** qua pipeline cũ/mới (bảng mục 4); người dùng xác nhận 4 hướng đúng |
| 08/10 | Con trỏ trôi sang trái | Log: hiệu chuẩn lúc khởi động đo sai ~1 °/s vì đang cầm board; khóa đứng yên không bao giờ bật (`Stat: 0` 174/174 giây) | **Hiệu chuẩn có kiểm tra** + lệnh `c` đo lại | `BENCH_VERIFIED` 10/10–14/10 (bảng mục 5) |
| 14/10 | Cầm lắc lúc bật nguồn vẫn dùng bias sai | Thấy ở ca thử B ngày 10/10 | **Tự đo lại khi nằm yên trên bề mặt** | `BENCH_VERIFIED` 14/10: tự khỏi sau ~5 s đặt xuống (mục 6) |

## 3. Bảng thông số đã đổi (trước / sau / lý do)

| Thông số | Trước | Sau | Lý do ngắn gọn | Nguồn / bằng chứng |
| --- | --- | --- | --- | --- |
| Vùng chết `apply_deadzone` | 0.8 / 1.4 °/s (cắt về 0) | **Bỏ**; thay bằng `apply_tightening`, ngưỡng **1.4 °/s** (dưới ngưỡng thì đầu ra = ω·\|ω\|/1.4) | Vùng chết cứng nuốt chuyển động chậm; tightening thu nhỏ dần chứ không cắt về 0 (Gyro Wiki/JoyShockMapper) | `docs/FIRMWARE_CHANGELOG_2026-10-03.md` |
| Ngưỡng khóa đứng yên `stat_gyro_thresh` | 1.2 °/s | **0.4 °/s** | 1.2 °/s khóa luôn cả chuyển động tay chậm | như trên |
| Cửa sổ khóa `stat_window_count` | 30 mẫu (~0.3 s) | giữ **30** | — | — |
| Tự chỉnh bias `auto_zero_alpha` | 0.002 (cả khi vừa yên) | giữ **0.002**, nhưng **chỉ sau khi yên liên tục ≥ 150 mẫu (1.5 s)** (`AUTO_ZERO_MIN_REST_SAMPLES`) | Bias không bị "hút" chuyển động chậm; tham khảo VQF/VSCView (rest ≥ 1.5–8 s) | changelog 03/10 |
| Cộng dồn phần dư làm tròn | không có | `s_rem_x`, `s_rem_y` | Chuyển động chậm cho < 0.5 count mỗi mẫu bị làm tròn về 0 | changelog 03/10 |
| **Gain** (`gain_x`, `gain_y`) | **2.2** (~220 count/độ) | **0.3** (~30 count/độ) | Quá nhạy: 1920 px chỉ cần ~9° xoay, run tay 0.5° = ~110 px | tính từ code; test N2–N7 đổi thang ×0.136 |
| Ánh xạ trục (`firmware.ino`) | giả định X = trục tới-lui, Y = ngang | **x_p = y_s, y_p = −x_s, z_p = z_s** (áp cho cả gia tốc kế và con quay, trước cả hiệu chuẩn) | Đo: cầm kiểu điều khiển TV, cảm biến +X = trái, +Y = sau (về cổ tay), +Z = lên | `docs/ORIENT_MEASUREMENT_2026-10-08.md`, `raw_logs/orient_2026-10-08_retry1.log` |
| Dấu chiều ngang (`motion_pipeline.cpp`) | `fx = +gain·ω_up` | `fx = −gain·ω_up` | Quay phải làm `gz` âm (quy tắc bàn tay phải), nên cần đảo để con trỏ sang phải | bảng phát lại mục 4 |
| Hiệu chuẩn bias lúc bật nguồn | 1 lần, 200 mẫu / 2 s, nhận hết | **Kiểm tra**: tối đa **5 lần**; chấp nhận khi **mọi trục sd ≤ 0.35 °/s và hai nửa cửa sổ lệch nhau ≤ 0.25 °/s**; hàm `motion_calibration_still` | Đang cầm/chạm board thì bias sai và không tự sửa được (ngưỡng khóa 0.4 °/s) | `docs/CALIBRATION_FIX_TEST_2026-10-10.md` |
| Lệnh `c` (serial) | không có | Đo lại bias; **không áp dụng** nếu cửa sổ bị từ chối (giữ bias cũ) | Có cách cứu khi bias sai | log 10/10 ca C |
| **Tự đo lại khi nằm yên trên bề mặt** | không có | Cửa sổ 1 s (100 mẫu), 3 cửa sổ liên tiếp thỏa: **gyro sd ≤ 0.35 °/s, gia tốc kế sd ≤ 0.005 g mỗi trục, \|a\| trong 1 ± 0.08 g, bias lệch > 0.5 °/s** → đo lại 1 lần có kiểm tra; hàm `motion_surface_rest_bias_bad` | Cứu ca "cầm lắc lúc bật nguồn" mà không cần serial | log 14/10 |

### Vì sao 0.005 g? (cách chọn ngưỡng "nằm yên trên bàn")
Muốn phân biệt **board nằm trên bàn** (cần đo lại bias) với **tay cầm giữ yên** (chuyển động chậm của tay không được "nuốt", đúng lo ngại của thầy). Em dùng dữ liệu thật đã đo: gia tốc kế **trên bàn** dao động ~0.002 g (độ lệch chuẩn của mẫu thô; ngay cả trung bình 100 ms chỉ 0.0007 g), còn **cầm tay giữ phẳng vững nhất** vẫn 0.010 g ở trục X (log đo hướng 08/10). Ngưỡng ban đầu em đặt 0.008 g, thấy khe hở quá hẹp với 0.010 g của tay, nên **siết xuống 0.005 g** (gấp 2.5 lần mức bàn). Cần thêm: ít nhất 3 giây liên tiếp, bias lệch > 0.5 °/s (lệch nhỏ hơn để bộ tự chỉnh chậm 0.002 lo).

## 4. Đo hướng trục: cách làm và bằng chứng

**Cách cầm chuẩn:** như điều khiển TV, cáp USB về phía cổ tay, mũi về phía màn hình, mặt chip hướng lên.

**Đo:** chương trình `firmware_orient` in 10 lần/giây gia tốc (g) và vận tốc góc đã trừ bias (°/s); 11 cử động, mỗi cử động ghi giờ; `scripts/host_verify/analyze_orient.py` tính trung bình gia tốc và góc đã xoay quanh từng trục (tích phân gyro).

**Suy ra:** nằm phẳng `az = +0.99 g` → Z hướng lên; ngẩng mũi lên: `ay < 0` và quay âm quanh X; nghiêng phải: `ax > 0` và quay âm quanh Y → **+X = trái, +Y = sau, +Z = lên** (hệ tọa độ thuận tay phải). Quay mũi sang phải: `gz` = −22.6 °/s trung bình, quay −67.9°.

**Phát lại dữ liệu thật qua pipeline (gain 0.3), tổng count |dX|, |dY|:**

| Cử động | Trước sửa (trải nghiệm thật) | Sau sửa |
| --- | --- | --- |
| Quay phải | dX = **−2036** (sang trái ✗) | dX = **+2036** (sang phải ✓) |
| Quay trái | dX = +2631 ✗ | dX = **−2631** ✓ |
| Ngẩng mũi lên | dY = +145 (gần như không phản hồi) | dY = **−990** (con trỏ lên ✓) |
| Cúi mũi xuống | dY = +137 | dY = **+1111** (xuống ✓) |
| Nghiêng cổ tay phải | dY = **+2151** (nghiêng điều khiển chiều dọc ✗) | dY = +208 (gần như bỏ qua ✓) |
| Nghiêng cổ tay trái | dY = −1609 | dY = −209 |

(45° quay phải ≈ 2036 count ≈ 30 count/độ, khớp gain 0.3.) Lưu ý: các pha "giữ" H1–H4 lẫn cả đoạn nâng/hạ nên không dùng để kết luận, chỉ dùng pha chuyển động M1–M6.

## 5. Sự cố "trôi sang trái" và cách sửa hiệu chuẩn

**Hiện tượng (08/10):** con trỏ tự trôi sang trái khi board đứng yên. **Log:** lúc khởi động người dùng đang cầm board nên bias đo ra là +1.44 / +0.69 / −0.66 °/s, lệch cỡ 3 °/s so với lúc nằm yên (khoảng −0.6 / −1.5 / +0.36); `Stat: 0` ở **174/174 giây**, `BiasZ` đứng im −0.66. **Nguyên nhân gốc:** bias dư ~1 °/s lớn hơn ngưỡng khóa 0.4 °/s nên không bao giờ khóa được, và vì chỉ tự chỉnh bias khi đang khóa nên **không tự phục hồi**. Đây đúng là rủi ro mô phỏng 04/10 đã cảnh báo, nay xảy ra thật.

**Kiểm chứng sau sửa (10/10, `raw_logs/calib_fix_*`):**
- Nằm yên: `Attempt 1: sd = 0.19/0.09/0.09 °/s … ACCEPTED`, bias cuối (trục pipeline) ≈ X −1.3, Y +0.56, Z +0.33.
- Cầm lắc mạnh lúc bật nguồn (sd > 100 °/s): cả 5 lần `REJECTED`, board dùng lần cuối với cảnh báo; bias sai X −6.35 → trôi liên tục (cố ý giữ làm bằng chứng cho ca "xấu nhất").
- Lệnh `c` khi nằm yên: `ACCEPTED`, `Stat: 1`, hết trôi.

## 6. Tự phục hồi (14/10): bằng chứng cuối

Board khởi động khi anh/chị lắc liên tục: 4–5 lần hiệu chuẩn `REJECTED`, bias sai áp dụng (**X = +13.27 °/s**); 27 giây `Stat: 0` (22 dòng có `dX/dY` khác 0 do đang lắc). Đặt xuống bàn lúc ~21:20:39: sau ~5 giây có `[HEAL] Resting on a surface but bias is off by -14.76 dps → recalibrating`, `ACCEPTED`, bias về **−1.48 / +0.57 / +0.35**. Từ đó **87 dòng `[STATUS]`: 85 dòng `Stat: 1`, 0 dòng `dX/dY` khác 0**. Log: `raw_logs/heal_fw_2026-10-14_B_shake_then_rest.log` (SHA-256 `aee32958…cf77d`). Ca nằm yên (`heal_fw_…_A_still.log`): `Attempt 1 ACCEPTED`, 36/37 dòng `Stat: 1`, 0 lỗi I2C.

## 7. Các bài kiểm thử đã làm (liệt kê để báo cáo)

| Loại | Bài | Mục đích | Kết quả |
| --- | --- | --- | --- |
| Máy tính (`HOST_TESTED`, 19 test PASS) | 10 test cơ sở (thanh ghi, driver, đứng yên, deadzone/xoay, clutch, thái độ, cử chỉ flick, hội tụ, dt, cử chỉ đầu-cuối) | Không phá chức năng cũ | PASS |
| | N1 đứng yên + bias dư 0.1 °/s trên gy+gz | Không trôi khi bias lệch nhỏ | ≤ 3 count/10 s (gain 0.3) |
| | N2, N3 xoay chậm 1.0 / 0.5 °/s | **Không nuốt chuyển động chậm** (câu hỏi của thầy) | 43 và 11 count/200 mẫu, khớp kỳ vọng 43 và 11 (tính từ gain 0.3) |
| | N4 chống bias hút chuyển động | Tự chỉnh bias không nuốt chuyển động | cuối/đầu = 95–105 % |
| | N5 tốc độ cao, N6 bão hòa | Hệ số và kẹp ±127 | 9 count (30 °/s), 127 (450 °/s) |
| | N7 giới hạn bias dư 0.1/0.2/0.3 °/s | Mô tả giới hạn đã biết | 0 / ≤ 5 / 21 count/10 s |
| | N8 kiểm tra hiệu chuẩn | Chấp nhận nằm yên, từ chối cầm/lắc/NaN | PASS |
| | N9 điều kiện tự phục hồi | Chỉ kích hoạt khi nằm bàn + bias sai | PASS |
| Đo trên board (`BENCH_VERIFIED`) | Đo thời gian I2C, nhiễu tĩnh, nhiệt (01/10) | Số liệu nền | I2C 438 µs/12 byte ở 400 kHz; nhiễu gyro σ ≈ 0.09 °/s; |A| = 0.988 g |
| | Đo trôi bias 12 phút × 2 lần (04–08/10) | Rủi ro bias lệch | tối đa 0.029 / 0.057 °/s |
| | Đo hướng trục (08/10) | Xác định cách cầm | mục 4 |
| | Kiểm tra hiệu chuẩn 3 ca (10/10), tự phục hồi (14/10) | Sửa lỗi trôi | mục 5, 6 |
| Cầm thử (`USER_FEEDBACK`) | Người dùng thử với laptop làm máy chủ Bluetooth | Cảm giác điều khiển | "rất ổn" (một buổi) |

## 8. Câu hỏi thầy có thể hỏi và cách trả lời trung thực

1. **"Bộ lọc nhiễu có nuốt chuyển động nhỏ không?"** Bản cũ có (vùng chết 0.8/1.4 và khóa 1.2 °/s khiến 0.5 và 1.0 °/s cho 0 count). Em sửa (tightening, khóa 0.4 °/s, cộng dồn phần dư) và kiểm bằng test N2/N3/N4: 1.0 và 0.5 °/s đều cho count, không bị bias hút. Giới hạn: dưới khoảng 0.4 °/s liên tục vẫn có thể bị khóa.
2. **"Sao đổi gain?"** Gain 2.2 ứng với ~220 count/độ nên quá nhạy (1920 px chỉ ~9°); 0.3 ứng với ~30 count/độ. Con số 0.3 là điểm khởi đầu theo lập luận, rồi người dùng cầm thử thấy ổn; chưa tối ưu bằng nhiều người thử.
3. **"Sao lúc đầu điều khiển ngược?"** Phần mềm giả định trục ngang là Y, nhưng cầm theo kiểu điều khiển TV thì trục ngang là X; chiều ngang còn bị ngược dấu. Em đo 11 cử động để xác định hướng thật, sửa bằng ánh xạ trục và đảo dấu, kiểm bằng phát lại dữ liệu đo thật.
4. **"Sao có tự đo lại bias?"** Bias gyro lệch > ~1 °/s lớn hơn ngưỡng khóa 0.4 °/s thì không tự sửa được. Hiệu chuẩn kiểm tra độ yên; nếu vẫn sai thì tự đo lại khi board nằm trên bề mặt (gia tốc kế rất ổn định, khác hẳn tay cầm).
5. **"Nguồn điện?"** Có lúc board báo `Brownout detector was triggered` khi bật BLE (11 lần trong một log ngày 10/10) và nạp firmware hay đứt giữa chừng; nghi do cáp/cổng USB nhưng **chưa chứng minh**. Chưa thử pin LiPo + mạch nâng áp.

## 9. Giới hạn và việc chưa làm (nói thẳng với thầy)

- Kết quả cầm thử là **một người, một buổi**, ghép với **laptop**. Ghép nối BLE với **PC** vẫn `NOT_TESTED`.
- Chưa đo độ trễ BLE, chưa lắp nút (Clutch GPIO27, click GPIO25/26), chưa có mạch đo pin.
- Dây I2C trên breadboard hay lỏng (nhiều đợt lỗi `i2cWriteReadNonStop`); cần hàn hoặc đầu nối chắc.
- Gain chỉnh lúc chạy (`+`/`-`) **không lưu**; mặc định 0.3.
- Ngưỡng hiệu chuẩn (0.35 °/s, 0.25 °/s) và tự phục hồi (0.005 g, 0.5 °/s, 3 s) lấy từ dữ liệu của **một board, vài buổi**; chưa kiểm với nhiều bàn/tay khác nhau.
- Đo bias chưa có BLE bật và chưa có ca khởi động nguội thật sự (die chỉ ấm +0.1–0.2 °C).
- Báo cáo giữa kỳ đã nộp **không cập nhật**; báo cáo chi tiết, cẩm nang, kịch bản vẫn mô tả thuật toán/gain cũ.

## 10. Nơi chứa bằng chứng

- Mã: `firmware/` (bản build cuối: `firmware.bin` SHA-256 `3428a52c…a70685`, thư mục nạp `release/2026-10-14_firmware_flash/`). Trước mỗi đợt sửa có bản sao lưu ở `backups/2026-10-03_*`, `2026-10-04_*`, `2026-10-08_*`, `2026-10-14_*`.
- Test: `firmware/test/test_motion_pipeline.cpp` (19 test).
- Log và báo cáo: `raw_logs/` (bias_drift_*, orient_*, handtest_*, calib_fix_*, heal_fw_*), `docs/FIRMWARE_CHANGELOG_2026-10-03.md`, `BIAS_DRIFT_MEASUREMENT_2026-10-04.md` + `BIAS_DRIFT_KIEM_TRA_CLAUDE_2026-10-08.md`, `ORIENT_MEASUREMENT_2026-10-08.md`, `HANDTEST_2026-10-08.md`, `CALIBRATION_FIX_TEST_2026-10-10.md`.
- Công cụ: `firmware_bias_drift/`, `firmware_orient/`, `scripts/capture_serial.py`, `scripts/gain_tuner.py`, `scripts/host_verify/analyze_*.py`.

## 11. Sự cố ghi nhận 17/10/2026: con trỏ trôi nhẹ rồi tự hết (CHƯA SỬA, có đề xuất)

- **Hiện tượng (người dùng báo, `USER_FEEDBACK`):** khi đang dùng, con trỏ **trôi nhẹ xuống và lệch phải**, sau đó **tự hết**. Không có log tại thời điểm đó (lúc kiểm tra bằng log 40 giây khi board nằm yên: `Stat: 1` 35/37 giây, 0 dòng `dX/dY` khác 0, bias +0.37 ổn định; `raw_logs/drift_check_2026-10-17_1.log`). Chưa biết lúc trôi board đang nằm bàn hay cầm tay.
- **Giả thuyết (suy luận từ mô phỏng, CHƯA chứng minh):** bias lệch nhẹ khoảng **0.2–0.5 °/s** rơi vào "vùng chết" giữa hai cơ chế tự sửa: (1) khóa đứng yên cần 30 mẫu liên tiếp dưới 0.4 °/s trên cả 3 trục nên bias dư ≥ ~0.2–0.3 °/s làm chuỗi đứt; (2) tự đo lại `[HEAL]` chỉ kích hoạt khi bias lệch **> 0.5 °/s**. Với gain 0.3: 0.3 °/s ≈ 2 pixel/giây (N7: 21 count/10 s), 0.5 °/s ≈ 4 pixel/giây, khớp mô tả "nhẹ". Các khả năng khác chưa loại: run tay lúc cầm, bàn rung, bias đổi theo nhiệt sau khi cắm điện.
- **Đề xuất (đã được người dùng cho hoãn, làm sau):** hạ ngưỡng bias của `motion_surface_rest_bias_bad` từ **0.5 xuống ~0.2 °/s**. Điều kiện nằm trên bề mặt (gia tốc kế sd ≤ 0.005 g trong ≥ 3 s, gyro sd ≤ 0.35 °/s) giữ nguyên nên không nuốt chuyển động tay; trung bình 100 mẫu chỉ nhiễu ~0.01 °/s nên 0.2 °/s còn xa nhiễu. Cần: sửa 1 hằng số, thêm/đổi test N9, nạp lại, rồi kiểm chứng bằng log. Kèm ghi log dài (30–60 phút) để bắt lần trôi sau và xem `Stat`, `BiasZ`, `dX/dY` đúng thời điểm.
- **Trạng thái:** `NOT_TESTED` (đề xuất), ngưỡng hiện tại vẫn 0.5 °/s.

## 12. Nút bấm trái/phải (17/10/2026)

- Dây: GPIO25 = trái (SW2), GPIO26 = phải (SW3), GPIO27 = Mode/Clutch (SW4), mỗi nút nối GND (kéo lên nội bộ, nhấn = mức thấp).
- Thay đổi: **chống dội 20 ms** cho cả 3 nút (`firmware/src/button_debounce.cpp`, test N10, `HOST_TESTED`); nhấn/nhả trái/phải gửi `press`/`release` (giữ để kéo-thả); mất kết nối khi đang giữ nút thì quên trạng thái để không kẹt; log `[BTN] LEFT/RIGHT down/up` (kèm `(BLE not connected)` khi chưa kết nối). Nút Mode giữ nguyên hành vi Clutch (giữ = khóa con trỏ), chỉ thêm chống dội.
- Chưa làm: đóng băng con trỏ ~100–150 ms sau khi nhấn (cổ tay hay giật lúc bấm), mở rộng nút Mode (nhấn giữ lâu = đo lại bias).
- Trạng thái: nạp lên board 17/10 (`firmware.bin` SHA-256 `3b486683…b1fa`); bấm thử thật `NOT_TESTED` tại thời điểm viết.

## 13. Nguồn tham khảo

> Mục này ghi **các nguồn ngoài mà session nghiên cứu (Claude) thật sự đã mở**, mức độ đã đọc, và nói thẳng những quyết định **không có nguồn ngoài**. Viết ngày 17/10/2026. Không kiểm lại nội dung mục 1–12 và không sửa chúng. Ngày truy cập tính theo mốc ngày của session (không có đồng hồ chính xác). Không có trích dẫn nguyên văn; mọi ý đều tóm tắt bằng lời của người viết.
>
> **Mức độ đọc:** **[A]** đã đọc bản gốc (tải hoặc mở nguyên tài liệu, trích văn bản); **[B]** chỉ đọc qua bản tóm tắt tự động của công cụ web (một mô hình nhỏ tóm tắt trang, có thể sai số liệu); **[C]** chỉ biết qua kết quả tìm kiếm (tiêu đề, đoạn trích), chưa mở.

### 13.1 Bảng nguồn

**Nhóm 1. Lọc nhiễu, đứng yên, hiệu chuẩn bias (tìm trên web) — 9 nguồn, đều [B]**

| # | Nguồn (tên, tác giả/tổ chức) | URL | Ngày truy cập | Mức | Ý chính |
| --- | --- | --- | --- | --- | --- |
| 1 | Gyro Wiki, bài "Good Gyro Controls Part 1: The Gyro is a Mouse" (trang của Jibb Smart; tác giả từng bài chưa xác minh) | http://gyrowiki.jibbsmart.com/blog:good-gyro-controls-part-1:the-gyro-is-a-mouse | 2026-10-03 | [B] | Khuyên không đặt ngưỡng cắt cứng cho chuyển động nhỏ vì sẽ không thể di chuyển chậm hơn ngưỡng; thay bằng "tightening" (đầu vào nhỏ bị thu nhỏ dần về 0 chứ không bị cắt). Làm mượt chỉ nên áp cho chuyển động nhỏ. Hiệu chuẩn bằng cách lấy trung bình nhiều mẫu |
| 2 | Gyro Wiki, bài "Tight and Smooth: Soft Tiered Smoothing" | http://gyrowiki.jibbsmart.com/blog:tight-and-smooth:soft-tiered-smoothing | 2026-10-03 | [B] | Làm mượt theo bậc mềm: chuyển động nhỏ đi qua bộ làm mượt, chuyển động lớn đi thẳng, hai ngưỡng nối bằng nội suy tuyến tính để không bị nhảy; tổng quãng đường được giữ nguyên. **Chưa áp dụng** vào dự án (ý tưởng cho giai đoạn sau) |
| 3 | JoyShockMapper, README (kho Electronicks; kho gốc của JibbSmart có trong kết quả tìm kiếm nhưng không mở) | https://github.com/Electronicks/JoyShockMapper/blob/master/README.md | 2026-10-03 | [B] | Liệt kê các tùy chọn xử lý nhiễu gyro: ngưỡng cutoff, cutoff recovery, ngưỡng và thời gian làm mượt. Tài liệu cảnh báo cutoff cứng làm mất khả năng theo dõi chậm |
| 4 | Bằng sáng chế US8786549B2 "Gyro mouse de-drift and hand jitter reduction" (chủ sở hữu, tác giả chưa xác minh) | https://patents.google.com/patent/US8786549 | 2026-10-03 | [B] (mở hai lần, công thức tóm tắt nhất quán) | Tính xác suất "đang cố ý đứng yên" từ phương sai, trung bình và vận tốc ước lượng; dùng xác suất đó điều chỉnh liên tục việc bù trôi và giảm rung, không có ngưỡng cứng. **Dự án không dùng thuật toán này** (dùng ngưỡng cứng 0.4 °/s) |
| 5 | VQF, mã nguồn C++ `vqf.hpp` (phần mô tả tham số); tài khoản GitHub dlaidig, chưa xác minh tên tác giả | https://raw.githubusercontent.com/dlaidig/vqf/main/vqf/cpp/vqf.hpp (kho: https://github.com/dlaidig/vqf — không mở trang chủ) | 2026-10-03 | [B] | Nhận diện "nghỉ" cần gyro dưới một ngưỡng cỡ vài °/s và gia tốc ổn định trong cỡ 1.5 s; ước lượng bias cập nhật chậm (thời gian quên cỡ 100 s) và bị kẹp ở cỡ 2 °/s. Số liệu chi tiết xem 13.3 |
| 6 | VSCView, pull request #8 "Gyro drift compensation via zero-motion auto-calibration" (người gửi PR: WombatFromHell theo kết quả tìm kiếm; kho Nielk1/VSCView) | https://github.com/Nielk1/VSCView/pull/8/files | 2026-10-03 | [B] | Chỉ cập nhật bias sau khi yên liên tục khoảng 8 s (bộ lọc EMA, Z-score, dò đỉnh); một cú động làm đếm lại từ đầu |
| 7 | ESP32C3_AirMouse (rohith-saravana) | https://github.com/rohith-saravana/ESP32C3_AirMouse | 2026-10-03 | [B] | Dự án sở thích: hiệu chuẩn lúc khởi động, vùng chết cố định, giới hạn mức di chuyển mỗi lần cập nhật. README nói phải chỉnh tay các hằng số và hiệu chuẩn lại khi trôi kéo dài; không nêu giá trị mặc định |
| 8 | esp32-air-mouse (AGIQdev-Aditya) | https://github.com/AGIQdev-Aditya/esp32-air-mouse | 2026-10-03 | [B] | Dự án sở thích: giữ nút khi đặt board lên bàn để hiệu chuẩn lại khi con trỏ trôi. README không nêu số mẫu hay ngưỡng |
| 9 | "空中鼠标算法原理讨论" (FerventDesert, blog cnblogs) | https://www.cnblogs.com/buptzym/p/4807692.html | 2026-10-03 | [B] | Nêu bài toán của chuột không gian (gyro rẻ có đầu ra tĩnh, cần làm mượt và oversampling) nhưng chỉ nói hiệu chuẩn lúc xuất xưởng; không có giải pháp động, không có số liệu |

**Nhóm 2. Datasheet và tài liệu kỹ thuật — 7 nguồn, đều [A]**

| # | Nguồn (tên, tác giả/tổ chức) | URL | Ngày truy cập | Mức | Dùng cho việc gì |
| --- | --- | --- | --- | --- | --- |
| 10 | TDK InvenSense, ICM-20948 Datasheet DS-000189 **rev 1.3** (bản sao do SparkFun lưu) | https://cdn.sparkfun.com/assets/7/f/e/c/d/DS-000189-ICM-20948-v1.3.pdf | 2026-10-01 | [A] | Độ nhạy gyro ±500 °/s = 65.5 LSB/(°/s) và accel ±4 g = 8192 LSB/g; ADC 16 bit; nhiễu, ZRO, zero-g; công thức nhiệt độ die; dải nguồn VDD/VDDIO; bảng DLPF (Table 16, 18); trình tự đọc I2C (mục 6.3) và chọn bank; chip hỗ trợ I2C tới 400 kHz. **Không dùng** cho quy ước hệ trục/chiều quay: session này không đọc phần đó |
| 11 | Espressif, ESP32 Series Datasheet **v5.3** | https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf | 2026-10-01 | [A] | ADC (sai số DNL/INL, dải đo theo mức suy hao, lệch ±6 % giữa các chip), điện trở kéo nội khoảng 45 kΩ, dòng nguồn/chìm tối đa của chân (dùng để giải thích nút bấm và LED). **Không đọc** phần nguồn cấp của chip |
| 12 | Espressif, ESP32 Technical Reference Manual **v5.8** | https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf | 2026-10-01 | [A], nhưng chỉ tra theo từ khóa, không đọc hết tài liệu | Thanh ghi GPIO (OUT1/ENABLE1, IO_MUX), bộ điều khiển I2C (chu kỳ SCL, `I2C_CTR_REG`, mã lệnh), thanh ghi SAR ADC1 |
| 13 | TP4056 datasheet (hãng ghi trong tài liệu: chưa xác minh lại) | https://dlnmh9ip6v2uc.cloudfront.net/datasheets/Prototyping/TP4056.pdf | 2026-10-01 | [A] | Điện áp nạp 4.2 V, ngưỡng trickle 2.9 V, công thức dòng sạc theo R_PROG (chương nguồn của báo cáo chi tiết) |
| 14 | DW01A datasheet (tài liệu lưu trên ic-fortune.com) | https://www.ic-fortune.com/upload/Download/DW01A-DS-10_EN.pdf | 2026-10-01 | [A] | Ngưỡng bảo vệ quá nạp, quá xả, quá dòng (chương nguồn) |
| 15 | MT3608 datasheet (Aerosemi; bản do Olimex lưu) | https://www.olimex.com/Products/Breadboarding/BB-PWR-3608/resources/MT3608.pdf | 2026-10-01 | [A] | Điện áp chuẩn FB 0.6 V, tần số đóng cắt 1.2 MHz (chương nguồn) |
| 16 | Thư viện ESP32 BLE Mouse v0.3.1 (T-vK), mã nguồn `BleMouse.cpp` đã cài trong `firmware/.pio/libdeps/` | https://github.com/T-vK/ESP32-BLE-Mouse | 2026-10-17 (mở file trong máy) | [A], chỉ mở file `BleMouse.cpp` | Gói HID chuột gồm 5 byte: nút, x, y, wheel, hWheel; hàm gửi đóng gói mảng 5 byte rồi `notify` |

**Nhóm 3. Chỉ biết qua kết quả tìm kiếm (chưa mở) — 14 nguồn, đều [C], truy cập 2026-10-03**

| # | Nguồn | URL | Ghi chú |
| --- | --- | --- | --- |
| C1 | Gyro Wiki, "7 Building Blocks for Better Controls" | http://gyrowiki.jibbsmart.com/blog:7-building-blocks-for-better-controls | Cùng chủ đề điều khiển bằng gyro |
| C2 | Gyro Wiki, "Good Gyro Controls Part 2: The Flick Stick" | https://gyrowiki.jibbsmart.com/blog:good-gyro-controls-part-2:the-flick-stick | Chủ đề khác (quay nhanh), không dùng |
| C3 | mygamepadtester.com, "Gyro Aiming Explained" | https://mygamepadtester.com/blogs/gyro-aiming-explained | Blog thương mại; đoạn trích tìm kiếm nêu ngưỡng làm mượt cỡ 1–3 °/s, **không xác minh, không dùng** |
| C4 | Diễn đàn reWASD, "Mouse output unusable due to stutter/jitter" | https://forum.rewasd.com/forum/rewasd/technical-questions-aa/228286-mouse-output-unusable-due-to-stutter-jitter | Thảo luận người dùng |
| C5 | "Steam Input Essentials" (bryanrumsey.wordpress.com) | https://bryanrumsey.wordpress.com/2019/02/25/steam-input-essentials-eps-7-mouse-joystick/ | Blog |
| C6 | Bằng sáng chế 20120229385 (patents.justia.com) | https://patents.justia.com/patent/20120229385 | Cùng chủ đề với nguồn 4; không mở, không khẳng định cùng họ sáng chế |
| C7 | aksherap1/Air-Mouse-Project | https://github.com/aksherap1/Air-Mouse-Project | Dự án sở thích ESP32 + MPU-6050 |
| C8 | Tamizharasu558/AirMouse | https://github.com/Tamizharasu558/AirMouse | Dự án sở thích |
| C9 | pybricks/support, issue #933 "Gyro bias calibration ideas" | https://github.com/pybricks/support/issues/933 | Thảo luận hiệu chuẩn bias |
| C10 | sts-calibration.com, "Gyro Calibration Guide" | https://sts-calibration.com/gyro-calibration-guide-fix-drift/ | Hướng dẫn chung |
| C11 | CSDN, "空鼠遥控姿态解算" | https://blog.csdn.net/weixin_42596565/article/details/118281260 | Chỉ thấy tiêu đề |
| C12 | CSDN, "空中鼠标算法详解与优化" | https://blog.csdn.net/weixin_34290390/article/details/85753884 | Mở lỗi HTTP 521; chỉ thấy tiêu đề |
| C13 | CSDN, "空中鼠标算法原理讨论" | https://blog.csdn.net/weixin_33816300/article/details/90660181 | Mở lỗi HTTP 521. Tiêu đề giống nguồn 9 (cnblogs) nên có thể là bản chép lại, chưa so sánh nội dung |
| C14 | CSDN, bài giới thiệu thuật toán VQF | https://blog.csdn.net/weixin_53470752/article/details/147542317 | Chỉ thấy tiêu đề |

### 13.2 Quyết định kỹ thuật → nguồn

Cột cuối trả lời thẳng: quyết định đó có nguồn ngoài hay do **tự suy luận / tự đo**. Các số đo và log của chính dự án (không phải nguồn ngoài) nằm ở mục 10 của nhật ký này.

| Thông số / quyết định | Giá trị | Nguồn ngoài (nếu có) | Hay là: tự suy luận / tự đo |
| --- | --- | --- | --- |
| Bỏ vùng chết cứng, dùng tightening | Ngưỡng T = **1.4 °/s**; dưới T thì đầu ra = ω·\|ω\|/T | **Ý tưởng** "tightening": Gyro Wiki Part 1 (nguồn 1) và cảnh báo về cutoff cứng của JoyShockMapper (nguồn 3), đều [B] | **Giá trị 1.4 °/s không có nguồn ngoài**: là số cũ `gyro_deadzone_high` được giữ lại. Gyro Wiki chỉ nêu ví dụ ngưỡng lớn hơn nhiều (cỡ 5 °/s, [B]). Không có bằng chứng đã thử giá trị T khác |
| Ngưỡng khóa đứng yên `stat_gyro_thresh` | **0.4 °/s**; cửa sổ 30 mẫu giữ nguyên | Không có nguồn ngoài. VQF dùng ngưỡng "nghỉ" lớn hơn nhiều (cỡ 2 °/s, [B]), chỉ để so sánh, không phải căn cứ | **Tự suy luận từ số đo nhiễu** σ ≈ 0.09 °/s (`bench_2026-10-01_icm20948_timing_noise_run2.log`, `BENCH_VERIFIED`), tức khoảng 4σ. Kiểm bằng mô phỏng 04/10: ngưỡng này nhạy với bias dư 0.2–0.3 °/s (`HOST_TESTED`, xem mục 2 và 11) |
| Chờ yên ≥ 1.5 s mới tự chỉnh bias | **150 mẫu** ở 100 Hz (`AUTO_ZERO_MIN_REST_SAMPLES`); `auto_zero_alpha` giữ 0.002 | **Tham khảo** VQF (thời gian nghỉ tối thiểu cỡ 1.5 s, [B]); VSCView cỡ 8 s ([B]) không theo | Con số 1.5 s **trùng giá trị của VQF khi được chọn**; chưa kiểm 1.5 s có tối ưu cho board này không. `auto_zero_alpha` 0.002 có sẵn trong code gốc, không nguồn ngoài. Đo trôi bias 12 phút chỉ cho thấy trôi nhỏ: 0.029 và 0.057 °/s (`BENCH_VERIFIED`) |
| Cộng dồn phần dư làm tròn | `s_rem_x`, `s_rem_y`; xóa khi bão hòa ±127, khi Clutch, khi đứng yên, khi recenter và khi init | **Không có nguồn ngoài** | **Tự suy luận từ code**: làm tròn mỗi mẫu cho 0 khi kết quả < 0.5 count nên mất chuyển động chậm. Gyro Wiki có nguyên tắc bảo toàn quãng đường nhưng nói về làm mượt, không phải làm tròn, nên không dùng làm nguồn. Kiểm bằng test N2, N3 (`HOST_TESTED`) |
| Gain | **0.3** (count mỗi mẫu 10 ms trên mỗi °/s) ≈ 30 count/độ (gain × 100 Hz); trước đó 2.2 ≈ 220 count/độ | **Không có nguồn ngoài** | **Tự tính từ code** (nhật ký mục 3), rồi người dùng cầm thử: lúc đầu "tốt hơn nhưng chưa ổn", sau đó "rất ổn" (`USER_FEEDBACK`, một người, một buổi). Session này không tham gia chọn 0.3 |
| Ánh xạ trục và đảo dấu chiều ngang | x_p = y_s, y_p = −x_s, z_p = z_s; fx = −gain·ω_up | **Không có nguồn ngoài mà session này đọc**. Session này chưa đọc phần quy ước hệ trục của datasheet ICM-20948 | **Tự đo** (11 cử động chuẩn, sau đó phát lại dữ liệu thật qua pipeline; `BENCH_VERIFIED` và `HOST_TESTED` theo nhật ký mục 3, 4). Do session khác thực hiện; session này chỉ đọc kết quả trong nhật ký, chưa tự kiểm lại |
| Hiệu chuẩn có kiểm tra | Tối đa **5 lần**; chấp nhận khi mọi trục sd ≤ **0.35 °/s** và hai nửa cửa sổ lệch ≤ **0.25 °/s** | Nhật ký không dẫn nguồn ngoài cho các ngưỡng này | **Tự đo/tự suy luận từ log của một board** (nhật ký mục 5, 9). Session này không tham gia và không biết cách chọn riêng từng ngưỡng |
| Tự đo lại khi nằm yên trên bề mặt | 3 cửa sổ 1 s liên tiếp: gyro sd ≤ 0.35 °/s, gia tốc kế sd ≤ **0.005 g** mỗi trục, \|a\| trong 1 ± 0.08 g, bias lệch > **0.5 °/s** | Không có nguồn ngoài. Ý tưởng chung "tự hiệu chuẩn khi nghỉ" cũng có ở VQF và VSCView ([B]) nhưng **không có bằng chứng** ngưỡng của dự án lấy từ đó (không rõ session thiết kế có tham khảo hay không) | **Tự đo**: bàn ≈ 0.002 g, tay giữ phẳng vững nhất ≈ 0.010 g, siết ngưỡng 0.008 → 0.005 g (nhật ký mục 3). Ngưỡng bias 0.5 °/s chưa chứng minh tối ưu; mục 11 đề xuất hạ xuống ~0.2 (`NOT_TESTED`) |
| Chống dội nút | **20 ms** (3 nút) | **Không có nguồn ngoài** | Con số 20 ms Claude đề xuất ở báo cáo chi tiết (mục 7.3) như **ước lượng**, chưa đo thời gian dội của nút thật. Việc cài đặt (`button_debounce.cpp`, test N10, `HOST_TESTED`) do session khác; không rõ họ có dựa nguồn nào. Bấm thử thật `NOT_TESTED` tại thời điểm viết nhật ký |
| Tần số lấy mẫu | Vòng lặp 100 Hz (10 ms); ODR cảm biến = 1125/(1+10) = 102.27 Hz | Công thức ODR: DS-000189 [A]. Lý do chọn 100 Hz: không có nguồn ngoài | Quyết định thiết kế ban đầu của nhóm (có trước các session này). **Tự đo**: chu kỳ đúng 10 000 µs trên 500 chu kỳ (`BENCH_VERIFIED`, 01/10) |
| Tốc độ I2C | **400 kHz**; đọc 12 byte mất 438 µs (400 kHz) và 1471 µs (100 kHz), 0 lỗi / 2000 lần | DS-000189 [A]: chip hỗ trợ I2C tới 400 kHz; trình tự đọc ở mục 6.3 | Thời gian là **tự đo** (`BENCH_VERIFIED`, 01/10). Lý do chọn 400 kHz (giảm thời gian chiếm bus) là suy luận, không nguồn ngoài. Nhật ký mục 9: dây breadboard lỏng gây lỗi I2C nhiều đợt về sau |
| Phạm vi đo | Gyro **±500 °/s**, accel **±4 g** (`GYRO_CONFIG_1` = `ACCEL_CONFIG` = 0x1B); 65.5 LSB/(°/s) và 8192 LSB/g | Độ nhạy: DS-000189 [A] | Việc chọn dải có từ firmware ban đầu. Lý do trong báo cáo chi tiết (cổ tay có thể vượt 250 °/s; Flick cần 1.15 g cộng 1 g trọng lực) là **suy luận của Claude, chưa có phép đo tốc độ xoay cổ tay lớn nhất**; dữ liệu 08/10 chỉ cho trung bình ≈ 22.6 °/s khi quay mũi sang phải (nhật ký mục 4) |
| Bộ lọc thông thấp phần cứng (DLPF) | Gyro 51.2 Hz (NBW 73.3 Hz); accel 50.4 Hz (NBW 68.8 Hz) | DS-000189 Table 16, 18 [A]; datasheet **không công bố độ trễ** | Chọn mức 011 có từ firmware ban đầu; lý do "triệt rung tay sinh lý" không có nguồn ngoài |
| Gói HID | 5 byte: nút, dX, dY, wheel, hWheel | `BleMouse.cpp` v0.3.1 [A] | Kẹp dX, dY ở ±127 là quyết định của firmware; session này chưa mở lại phần kiểu dữ liệu từng trường trong thư viện |

### 13.3 Cảnh báo độ tin cậy

- **Chỉ có hai nguồn ngoài thật sự ảnh hưởng đến quyết định thiết kế:** ý tưởng tightening (nguồn 1 và 3, [B]) và con số 1.5 s (VQF, [B]). **Mọi quyết định còn lại là tự suy luận hoặc tự đo.** Các nhãn `HOST_TESTED`, `BENCH_VERIFIED` ở 13.2 lấy từ nhật ký; cầm thử mới có một người, một buổi.
- **Chín nguồn nhóm 1 chỉ [B], và 14 nguồn nhóm 3 chỉ [C].** Công cụ đọc web dùng một mô hình nhỏ để tóm tắt trang nên có thể sai số liệu. Trước khi đưa vào báo cáo chính thức hoặc trích dẫn, phải đọc lại bản gốc các số sau:
  - JoyShockMapper: mặc định cutoff 0.0 °/s và thời gian làm mượt 0.125 s.
  - Soft Tiered Smoothing: trung bình 16 mẫu, ngưỡng thứ hai bằng 2 lần ngưỡng thứ nhất, công thức trọng số trực tiếp.
  - Gyro Wiki Part 1: ngưỡng ví dụ cỡ 5 °/s; công thức tightening.
  - Bằng sáng chế US8786549: công thức p(n); các σ (1, 0.3, 3 °/s); độ dài cửa sổ (hai lần đọc đều nhắc 30 mẫu và 500 mẫu, chưa phân biệt rõ đại lượng nào dùng cửa sổ nào); chu kỳ cập nhật bias.
  - VQF: thời gian nghỉ tối thiểu 1.5 s, ngưỡng gyro 2.0 °/s, ngưỡng gia tốc 0.5 m/s², thời gian quên bias 100 s, kẹp bias 2.0 °/s (kèm đơn vị).
  - VSCView PR #8: khoảng 8 s (≈ 533 mẫu ở ≈ 66.7 khung hình/giây, tức tốc độ của họ, không phải 100 Hz), ngưỡng 0.22.
- **[A] không có nghĩa tuyệt đối:** văn bản datasheet được trích bằng công cụ nên bảng có thể lệch cột. Số quan trọng cần đối chiếu PDF trước khi trích dẫn. Datasheet ICM-20948 là **rev 1.3** (bản sao SparkFun), không phải bản mới nhất của TDK (đường dẫn rev 1.6 không tải được dưới dạng PDF).
- **Những điều đã nói ở nơi khác (chủ yếu trong báo cáo chi tiết) dựa trên hiểu biết chung, session này chưa tra nguồn:** (a) giới hạn 300 ns thời gian lên của I2C Fast-mode (mục 3.2); (b) connection interval BLE trong khoảng 7.5 ms đến 4 s (mục 10); (c) nhận định "TRM ghi 11 dB là lỗi đánh máy, ESP-IDF gọi mức này là ADC_ATTEN_DB_11" (mục 4.3.1): đã thấy TRM ghi như vậy, nhưng việc đó là lỗi đánh máy là suy đoán. Session này cũng chưa đọc đặc tả Bluetooth HID hay USB HID Usage Tables.
- **Sai khác so với danh sách nguồn trong yêu cầu ghi nhật ký:** (1) "giữ nút để hiệu chuẩn lại" chỉ đúng với esp32-air-mouse (nguồn 8); ESP32C3_AirMouse (nguồn 7) là hiệu chuẩn lúc khởi động. Con số "300 mẫu" gắn với dự án đó chỉ xuất hiện trong đoạn tóm tắt tìm kiếm, README không xác nhận, nên không dùng. (2) Với ESP32 session này không đọc phần nguồn cấp của datasheet. (3) Quy ước hệ trục của ICM-20948 chưa đọc.

### 13.4 Nguồn không đọc được, và giới hạn của lần tìm

- **Reddit:** không đọc được. Tìm web giới hạn miền reddit.com báo lỗi miền không truy cập được; tải trang old.reddit.com báo không thể tải. **Không có dữ liệu Reddit nào trong dự án**, dù người dùng đã yêu cầu tìm.
- **CSDN:** hai bài (C12, C13) trả lỗi HTTP 521, chỉ thấy tiêu đề qua tìm kiếm.
- **VQF:** trang tham số trên vqf.readthedocs.io trả HTTP 404; đã chuyển sang đọc tệp `vqf.hpp` (nguồn 5).
- **Datasheet ICM-20948 bản TDK rev 1.6:** đường dẫn `invensense.tdk.com/wp-content/uploads/2024/03/DS-000189-ICM-20948-v1.6.pdf` trả về trang web điều hướng, không phải PDF; dùng bản sao rev 1.3 của SparkFun (nguồn 10).
- **Tìm tiếng Trung:** chỉ vài truy vấn, công cụ tìm web giới hạn trong phạm vi Hoa Kỳ nên kết quả tiếng Trung có thể thiếu. Có kết quả từ Zhihu và 立创开源广场 nhưng không liên quan trực tiếp, không mở. **Chưa tìm thấy bài tiếng Trung nào giải đúng bài toán "bộ lọc nuốt chuyển động nhỏ"**; điều đó không có nghĩa là không tồn tại.

## 13. CẬP NHẬT 17/10/2026 (tối): nguyên nhân thật của lần trôi là CẢM BIẾN ĐƠ, không phải "vùng chết" (cải chính mục 11)

- **Quan sát trực tiếp** (mở cổng với DTR/RTS tắt trước khi mở nên board KHÔNG reset, `raw_logs/drift_live_2026-10-17_noreset.log`): board nằm trên bàn, con trỏ đang trôi xuống và lệch phải nhẹ; **`Stat: 0` ở cả 35/35 giây**, `BiasZ` đứng im +0.37.
- **Lệnh `c` khi nằm yên** (`..._recal_cmd.log`): hiệu chuẩn báo **`sd = 0.00/0.00/0.00 dps` và bias = +0.00/+0.00/+0.00**. Cảm biến sống luôn có nhiễu ~0.09 °/s nên độ rung đúng bằng 0 nghĩa là **cảm biến trả về toàn số 0 (đơ)** trong khi ESP32 vẫn chạy.
- **Reset board** (`..._after_reset.log`): cảm biến sống lại ngay (`sd = 0.09/0.08/0.09`, bias −1.29 / +0.57 / +0.40, `Stat: 1`).
- **Cơ chế gây trôi:** gyro = 0 nhưng bias đã lưu ≈ (−1.22, +0.49, +0.37) nên phần dư không đổi ~1.3 °/s; tính theo dấu và ánh xạ trục thì phần dư đó đẩy con trỏ **xuống và sang phải nhẹ**, khớp mô tả. Khóa đứng yên không bật vì gia tốc kế cũng 0 (|a| không ≈ 1 g). Hiệu chuẩn lại còn bị lừa vì sd = 0 vẫn lọt qua kiểm tra "nằm yên".
- **Nguyên nhân khiến cảm biến đơ: CHƯA BIẾT.** Nghi ngờ (chưa chứng minh): nguồn 3.3 V chập chờn hoặc nhiễu điện làm ICM-20948 mất cấu hình (vừa gắn thêm dây nút ngay cạnh), dây I2C lỏng. Không thấy lỗi `i2cWriteReadNonStop` (bus vẫn ACK, chỉ dữ liệu bằng 0).
- **Cải chính mục 11:** giả thuyết "bias lệch 0.2–0.5 °/s rơi vào vùng chết" **chưa có bằng chứng và không cần thiết để giải thích sự cố này**. Đề xuất hạ ngưỡng 0.5 → 0.2 °/s vẫn là ý tưởng cho sau, nhưng không phải thủ phạm của lần này.
- **Sửa (HOST_TESTED, chưa nạp tại thời điểm viết):** (1) hiệu chuẩn **từ chối cửa sổ có sd < 0.005 °/s** (cảm biến đơ) và đòi **|a| = 1 ± 0.15 g**; log in thêm `|a|`; (2) **watchdog cảm biến đơ**: |a| < 0.5 g trong 0.5 s hoặc 100 mẫu giống hệt nhau liên tiếp → `[IMU] Sensor frozen/dead … re-initialising`, gọi lại `imu_init()` rồi đo lại bias (giữ bias cũ nếu board không yên), giới hạn 1 lần/3 s. Test N8 thêm ca "đơ" (20/20 PASS). Bản gốc `backups/2026-10-17_cam_bien_do/`.
- Việc cần theo dõi sau khi nạp: dòng `[IMU] Sensor frozen/dead` xuất hiện bao lâu một lần và vào lúc nào (bấm nút? cắm cáp?), để tìm nguyên nhân gốc.

## 14. BẰNG CHỨNG TRỰC TIẾP về sự cố "dùng giữa chừng thì không nhận" (17/10/2026, bản chó canh đầu tiên)

Log live `raw_logs/watch_live_2026-10-17.log` (SHA-256 `83e4d1e0…4744`, bắt không reset) vô tình ghi trúng sự cố, khi người dùng đang cầm dùng (board chạy được ~6.4 phút):
1. **06:21:55.565**: **11 lần đọc I2C liên tiếp lỗi** (`i2cWriteReadNonStop returned Error -1`, 110 ms), rồi cảm biến trả về **toàn số 0** (|a| = 0.000 g). Tức sự cố bắt đầu từ **lỗi bus I2C**, không chỉ cảm biến đơ.
2. **06:21:56** chó canh phát hiện, `imu_init = PASS`, nhưng cảm biến **vẫn chết** (các lần đo bias sau đó vẫn |a| = 0.000 g, sd = 0.00).
3. Bản cũ lúc đó **chặn ~11 giây** vì gọi đo lại bias 5 lần (lần đầu bị từ chối vì người dùng đang cử động: sd = 31 °/s; bốn lần sau vì cảm biến chết). Chuột đứng yên suốt thời gian này.
4. **06:22:07** chó canh khởi tạo lại lần hai → `imu_init = PASS` và **lần này sống lại**: `|a| = 0.985 g`, bias −1.36 / +0.51 / +0.40 `ACCEPTED`. Tổng thời gian mất tín hiệu **~15 giây** (06:21:55 → 06:22:10), tự hồi phục không cần reset board.
- **Kết luận:** (a) chó canh **không gây** lỗi, nó giúp board **tự hồi phục** (trước đây phải reset); (b) nhưng bản đầu **kéo dài thời gian mất tín hiệu** vì chặn 11 s đo lại bias; (c) cần thêm: lần khởi tạo đầu tiên không hồi phục cảm biến, lần hai (sau ~12 s) mới được. **Nguyên nhân gốc vẫn là phần cứng** (bus I2C bị lỗi rồi cảm biến mất trạng thái): nghi dây SDA/SCL/VCC/GND lỏng hoặc nguồn 3.3 V chập chờn, chưa chứng minh.
- **Sửa:** bỏ đo lại bias sau khi khởi tạo lại (giữ bias cũ), tiếp tục thử khởi tạo lại mỗi 3 s; thêm vào `[STATUS]` các trường `Up` (giây từ lúc bật), `Frz` (số lần chó canh chạy), `Heal`, `Rst` (lý do reset của chip) để đọc log bất cứ lúc nào cũng biết chuyện gì đã xảy ra. Nạp 17/10 (`firmware.bin` SHA-256 `0427790b…9b84`). Chưa kiểm chứng bản mới với sự cố thật (`NOT_TESTED`).
- **Việc nên làm:** kiểm tra/hàn lại dây I2C và nguồn cảm biến; thêm tụ lọc (ví dụ 10–100 µF gần chân VCC của module, nếu chưa có); đây mới là cách giảm số lần xảy ra.

## 15. Click bị trượt vì tay rung lúc ấn nút (17/10/2026) và bộ chặn click

- **Vấn đề (người dùng báo):** ấn chuột trái để chọn thì tay rung làm con trỏ trượt khỏi mục tiêu nên không click được. **Nguyên nhân (suy luận, chưa có số đo):** ngón cái ấn nút làm cả cụm board giật nhẹ; code cũ vẫn gửi chuyển động liên tục kể cả khi đang giữ nút, và chống dội 20 ms làm lệnh nhấn đến trễ; Windows chỉ tính là click nếu nhấn và nhả trên cùng một đối tượng.
- **Sửa (HOST_TESTED, 22/22 test; `click_guard.h/.cpp`, `button_debounce` bất đối xứng):** (1) **bộ đệm nhìn trước 40 ms** (4 mẫu): chuyển động bị giữ lại 40 ms, khi phát hiện nhấn thì **xóa** phần chuyển động ngay trước đó (cú giật lúc ấn); (2) **đóng băng con trỏ khi giữ nút < 250 ms**, giữ lâu hơn coi là kéo-thả và con trỏ chạy lại; (3) **nhận nhấn sau 5 ms, nhả sau 20 ms** (trước: 20 ms cả hai). Chỉnh bộ đệm lúc chạy qua serial: `>` tăng 10 ms, `<` giảm 10 ms (0–100 ms).
- **Đánh đổi:** độ trễ con trỏ tăng thêm 40 ms (đổi lại click chính xác hơn); kéo-thả bị chậm 250 ms lúc bắt đầu. Các số 40 ms / 250 ms / 5 ms là điểm khởi đầu, **chưa tinh chỉnh trên tay**.
- Trạng thái: build xong, thư mục nạp `release/2026-10-17_click_guard/`; chưa nạp tại thời điểm viết (`NOT_TESTED` trên tay).

## 16. Nút Mode: giữ = khóa con trỏ, nhả = cân lại vị trí (17/10/2026)

- **Yêu cầu (người dùng):** nút Mode (GPIO27): ấn vào là **cân lại vị trí**; phần "dí nút rồi gạt nhanh sang trái/phải" (cử chỉ Back/Forward) **để sau**.
- **Hành vi cũ:** giữ nút = khóa con trỏ và mở chế độ cử chỉ; nhả = cân lại ngay (trừ khi có cử chỉ). Hai điểm chưa hợp: (1) trong lúc giữ, một cú vuốt ngang có thể kích hoạt Back/Forward ngoài ý muốn; (2) cân lại đúng lúc nhả nút sẽ lấy hướng trọng lực khi ngón cái đang nhả, dễ dính cú giật của chính cái nhấn (cùng cơ chế với lỗi click trượt ở mục 15, **suy luận, chưa đo**).
- **Sửa (HOST_TESTED, 23/23 test, test mới N13):** (1) giữ Mode vẫn **khóa con trỏ**; (2) nhả Mode → **chờ 150 ms** (con trỏ vẫn khóa) rồi mới **cân lại** (đặt hướng "lên" tham chiếu bằng tư thế hiện tại, đưa góc quay ngang về 0); (3) **tắt cử chỉ** (`motion_setGesturesEnabled(false)` trong `firmware.ino`; mã cử chỉ giữ nguyên, mặc định trong thư viện vẫn bật để các test cũ không đổi); (4) log `[MODE] down` / `[MODE] up` / `[MODE] Recentered`; (5) cờ `recentered` mới trong `mouse_output_t`.
- **Ý nghĩa của "cân lại" với điều khiển theo tốc độ xoay:** chuột bay này không có vị trí tuyệt đối. Cân lại chỉ đổi **hệ quy chiếu**: hướng "lên" và trục quay ngang/dọc được lấy theo tư thế hiện tại của tay, nên khi anh/chị đổi cách cầm (ví dụ ngẩng cổ tay) thì quay cổ tay vẫn cho đúng ngang/dọc. Nó **không** đưa con trỏ về giữa màn hình.
- Chưa làm (theo lời người dùng): giữ nút + gạt nhanh trái/phải (Back/Forward); đo lại bias bằng giữ nút lâu; điều chỉnh số 150 ms trên tay.
- Trạng thái: build xong, thư mục nạp `release/2026-10-17_mode_button/`; `NOT_TESTED` trên tay.

## 17. Giữ Mode + lắc nhanh trái/phải = Back / Forward (17/10/2026)

- **Yêu cầu (người dùng):** giữ nút Mode rồi **lắc trái nhanh = lùi trang (Back)**, **lắc phải nhanh = tiến trang (Forward)**.
- **Có sẵn từ trước (đã tắt ở mục 16):** bộ phát hiện cú giật **tịnh tiến** bằng gia tốc ngang (đỉnh 1.15 g rồi gia tốc ngược lại 0.35 g trong 60–450 ms), chưa từng chỉnh trên tay. Vấn đề: lắc nhanh bằng **cổ tay** chủ yếu là chuyển động **xoay** quanh trục đứng, nên gia tốc ngang ở cảm biến thường không đạt 1.15 g (suy luận, chưa đo).
- **Thêm mới (HOST_TESTED, 24/24 test, test mới N14):** bộ phát hiện theo **tốc độ xoay ngang**: khi giữ Mode, tốc độ quay quanh trục đứng vượt **150 °/s** thì phát cử chỉ ngay, quay **trái** (+) = FLICK_LEFT = Back, quay **phải** (−) = FLICK_RIGHT = Forward. Sau khi phát, khóa tới khi tốc độ xuống dưới 35 % ngưỡng và **bỏ qua 600 ms** để cú quay về không kích hoạt cử chỉ ngược. Quay chậm (chỉnh tư thế, 60 °/s) không kích hoạt. Có cử chỉ thì **không cân lại** khi nhả. Bộ phát hiện cũ (gia tốc) vẫn chạy song song.
- **Chỉnh lúc chạy qua serial:** `y` = nhạy hơn (−20 °/s), `Y` = bớt nhạy (+20 °/s), giới hạn 40–600 °/s.
- **Log phục vụ chỉnh ngưỡng bằng số thật:** mỗi lần nhả Mode in `[MODE] hold peaks: turn = ... °/s (+ trái, ngưỡng ...), lateral accel = ... g`, và khi kích hoạt in `[FLICK] LEFT (Back)` / `RIGHT (Forward)`.
- **Giới hạn nói thẳng:** ngưỡng **150 °/s là số ước lượng**, **chưa có dữ liệu cú lắc nhanh thật** của người dùng (dữ liệu đo hướng ngày 08/10 chỉ có chuyển động chậm 20–30 °/s). Nếu giữ Mode để chỉnh tư thế mà quay nhanh hơn 150 °/s thì có thể kích hoạt nhầm. Trạng thái: `NOT_TESTED` trên tay; thư mục nạp `release/2026-10-17_flick/`.

### 17b. Kết quả đo thật của cử chỉ lắc nhanh (17/10/2026, `raw_logs/flick_test_2026-10-17_1.log`, SHA-256 `c7ee39b9…062e`, 150 giây, người dùng tự thử `BENCH_VERIFIED` phần số liệu)

- **33 lần giữ Mode**, trong đó **19 lần có cử chỉ** (tổng **16 Back (trái) + 14 Forward (phải)**), 14 lần không.
- **Tốc độ quay lớn nhất trong lần giữ có cử chỉ: 227–534 °/s** (trung vị khoảng 410). **Trong lần giữ không có cử chỉ: ≤ 97 °/s**, trừ một lần 276 °/s rơi vào khoảng chặn 600 ms ngay sau cử chỉ trước (đúng thiết kế: bỏ qua cú quay về). Hai nhóm **tách rời hoàn toàn** quanh ngưỡng **150 °/s** (trung bình nhân của 97 và 227 ≈ 148), nên giữ 150 °/s là hợp lý theo số đo thật. Ước lượng 150 °/s ban đầu nằm đúng chỗ, nhưng đây chỉ là **một người, một buổi**.
- Dấu đúng như thiết kế: quay trái = +, quay phải = −. Cử chỉ tạo `MOUSE_BACK` / `MOUSE_FORWARD`; việc trình duyệt có lùi/tiến thật hay không chưa được người dùng xác nhận tại thời điểm viết.
- **Nhiều cử chỉ trong một lần giữ:** 4 lần giữ có nhiều hơn một cử chỉ (ví dụ `RRRRL`, `LLRRLL`) khi người dùng lắc liên tục trong lúc giữ; mỗi cú quay đủ nhanh cách nhau > 600 ms đều tính. Có thể thêm quy tắc "một cử chỉ cho mỗi lần giữ" nếu muốn tránh kích hoạt nhầm bởi cú quay về chậm (chưa làm).
- **Nút trái đã hoạt động lại** sau khi người dùng tráo dây (5 lần `[BTN] LEFT down/up` ghi nhận); nguyên nhân từng là dây, không phải phần mềm.
- **Cảnh báo phần cứng quan trọng:** trong 150 giây lắc mạnh, cảm biến **đơ 17 lần** (`Frz: 16–17`, một lần `imu_init = FAIL`), mỗi lần lỗi I2C rồi tự hồi phục sau 0.5–3 s nhờ chó canh. **Lắc nhanh làm dây I2C trên breadboard chập chờn**; muốn dùng cử chỉ ổn định phải **hàn hoặc cố định chắc dây SDA, SCL, VCC, GND** của module cảm biến (dây ngắn, có giảm xóc, không để dây tự do).

## 18. Tách mã nguồn thành nhiều file (17/10/2026)

- **Yêu cầu (người dùng):** tách code ra nhiều file `.c/.h/.cpp` cho gọn nhưng vẫn liên kết với nhau.
- **Làm:** `firmware.ino` (429 dòng) → ~60 dòng điều phối + 9 mô-đun ứng dụng `app_*` (boot, imu, imu_guard, buttons, motion, ble, serial_cmd, status, timing) + `app_config.h` (mọi hằng số chỉnh được); `motion_pipeline.cpp` (534 → 490 dòng) tách thêm `yaw_flick` và `bias_checks`. Chi tiết, sơ đồ, bảng "muốn sửa X mở file nào": `docs/CAU_TRUC_MA_NGUON.md`. Sao lưu: `backups/2026-10-17_tach_file/`.
- **Nguyên tắc:** hai lớp, lõi thuần (test được trên máy tính, không gọi Arduino) và lớp `app_*` (gọi Arduino/BLE). Chỉ chuyển code, **giữ nguyên chuỗi log và hành vi**.
- **Kiểm chứng:** build PlatformIO SUCCESS, không cảnh báo (Flash 1 166 193 B, RAM 39 868 B); 24/24 test máy tính PASS (script mới `firmware/test/run_host_tests.sh|.ps1`). **Lớp `app_*` không có test tự động; chưa nạp lên board** (`NOT_TESTED` trên phần cứng).
