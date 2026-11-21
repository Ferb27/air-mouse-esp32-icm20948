# KIỂM TRA ĐỘC LẬP CỦA CLAUDE — BÁO CÁO ĐO TRÔI BIAS CỦA ANTI (08/10/2026)

Đối tượng kiểm tra: `docs/BIAS_DRIFT_MEASUREMENT_2026-10-04.md` (Anti). Không sửa file đó; ghi nhận xét ở đây. Trạng thái các số đo: `BENCH_VERIFIED` cho đúng các lần chạy này (1 board, nguồn USB, không BLE). Ghép nối BLE với PC: `NOT_TESTED`.

## 1. Đã tự chạy lại và khớp

| Việc | Kết quả |
| --- | --- |
| 7 file chuẩn bị (`firmware_bias_drift/*`, `capture_serial.py`, `analyze_bias_drift.py`) | Khớp băm trong prompt (`capture_serial.py` = `c3675d7c86a9b2c4`, bản đã sửa cho RFC2217) |
| `firmware/` | Không file nào bị sửa |
| 4 log mới trong `raw_logs/` | Tồn tại, SHA-256 tính lại khớp báo cáo (A bị dừng sớm, A_retry1, B_cold, boot firmware chính) |
| `analyze_bias_drift.py` chạy lại trên A_retry1 và B_cold | Output **giống hệt** hai file `docs/bias_drift_analysis_*.txt` |
| Các số Anti nêu (32.54→32.74 °C; 0.029 / 0.057 °/s; 803 / 2428 count; 85.1 % / 81.1 %) | Đúng với log |

## 2. Kết luận được dữ liệu ủng hộ

- Trong cả hai lần, bias thật so với hiệu chuẩn lúc khởi động lệch **tối đa 0.029 °/s (A)** và **0.057 °/s (B)** (cửa sổ 10 s, trục pitch/yaw), **0 cửa sổ nào ≥ 0.1 °/s**, thấp hơn nhiều ngưỡng rủi ro 0.2–0.3 °/s của mô phỏng. Đây là đo thật đầu tiên và nó **nghiêng về phía tốt** cho nỗi lo "bias nhảy bậc".
- Nhiễu thật hơi lớn hơn bench ngày 01/10: độ lệch chuẩn trung bình gx/gy là 0.104 / 0.104 (A) và 0.110 / 0.135 (B), so với ≈ 0.09.

## 3. Điểm báo cáo của Anti nói quá hoặc thiếu (cần đọc kèm)

1. **"Con trỏ không phát sinh bước trôi nào" (mục 6.3) KHÔNG được dữ liệu ủng hộ.**
   - Dòng `[STATUS]` chỉ in `dX/dY` của **một mẫu** mỗi giây, nên toàn `+0` không chứng minh gì.
   - Chính log đo cho thấy pipeline thật sinh **803 count (A)** và **2428 count (B)** trong ~12 phút nằm yên.
   - Trong log boot, `Stat: 0` ở **9 trong 17 giây** (tức khóa đứng yên chỉ giữ ở 8/17 giây).
2. **Count đến từ đâu (tôi tự phân tích log):**
   | Lần | Tổng | Trong 22 / 69 giây có sd > 0.25 | Trong các giây sd 0.15–0.25 | Trong các giây "yên" (sd ≤ 0.15) |
   | --- | ---: | ---: | ---: | ---: |
   | A_retry1 | 803 | 378 (47 %) | 350 (96 giây) | 75 |
   | B_cold | 2428 | 1971 (81 %) | 372 (85 giây) | 85 |
   → Count chủ yếu do **rung/nhiễu bùng lên**, không do bias. Rung của bàn nơi đặt laptop (Anti ghi nhận mặt bàn rung) làm gãy chuỗi 30 mẫu của khóa đứng yên. Nhiễu thật có "đuôi dài" hơn nhiễu Gauss σ = 0.09 của mô phỏng. Đây là điều **mô phỏng chưa có**; việc cầm tay thật sẽ còn rung nhiều hơn.
3. **Lần B không thật sự "nguội".** Rút điện **7.5 phút** (prompt yêu cầu ≥ 10) và nhiệt độ die lúc bắt đầu B là 32.76 °C so với 32.54 °C của A. Cả hai lần die chỉ ấm lên **+0.20 °C và +0.11 °C** trong 12 phút. Vì vậy phép đo **chưa thử** kịch bản chip nóng lên nhiều, và **không được dùng 0.03–0.06 °/s như cận trên** cho mọi tình huống nhiệt độ. Nhiệt độ phòng người dùng khai lúc đo cần được ghi lại nếu có.
4. **Xu hướng trục pitch cùng dấu ở cả hai lần:** độ dốc −0.0019 (A) và −0.0036 (B) °/s mỗi phút, tổng dịch −0.024 / −0.038 °/s sau 12 phút. Nhỏ, nhưng **đo 12 phút chưa đủ để loại trừ trôi tiếp** khi dùng lâu hơn; không ngoại suy.
5. **Lần B chỉ có 711/720 dòng `[D]`** (9 giây mất, không liên tiếp; báo cáo ghi "trọn vẹn 720 giây"). Mẫu/giây vẫn 100 và 0 lỗi đọc, nên nhiều khả năng mất dòng khi truyền qua mạng, không phải board; số count của B tính trên 711 giây.
6. **Lần A đầu bị dừng (`WHO_AM_I=0x00`):** nguyên nhân "lỏng dây I2C" là suy đoán hợp lý nhưng chưa được xác nhận độc lập (người dùng cắm lại dây thì lần sau chạy được).
7. Lỗi nhỏ trong mục 7: `STATIONARY_THRESH_DPS` **không tồn tại** trong code (tên thật là `stat_gyro_thresh` trong `motion_pipeline.cpp`); GPIO27 được gọi "nút Air Mouse ON/OFF" là tên cũ, trong code và báo cáo nộp là **Mode/Clutch**.
8. Log boot của firmware chính **không phân biệt được** bản cũ và bản mới (các dòng boot giống hệt nhau). Việc đã nạp bản mới dựa trên lời Anti (ghi 1 165 616 byte, kiểm băm đạt, 64.65 s qua RFC2217 ở 115200). Muốn chắc cần `esptool verify_flash` hoặc xem hành vi (chưa làm vì sẽ reset board).

## 4. Tình trạng hiện tại và việc còn lại

- Board đang chạy firmware chính (theo Anti là bản mới có lọc "tightening"), nằm ở **laptop từ xa**, đọc qua `rfc2217://<LAPTOP_IP>:4000?ign_set_control`.
- Việc C (giữ Clutch để hiệu chuẩn lại) và D (chỉnh ngưỡng đứng yên) **chưa nên quyết chỉ vì số đo bias**: bias không phải vấn đề chính trong lần đo này; **rung bùng lên** mới là thủ phạm của count khi nằm yên.
- Việc mới đáng xét (chưa ai yêu cầu): lọc rung (soft tiered smoothing đã nằm trong backlog); đo lại trên bàn ổn định tại nhà, có ghi nhiệt độ phòng, rút điện ≥ 10 phút; đo có BLE bật và bằng pin LiPo.
