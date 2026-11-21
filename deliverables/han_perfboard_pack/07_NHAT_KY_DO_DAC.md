# Nhật ký đo — người lắp điền

Ngày ____; người đo ____; bo/module ____; đồng hồ/model/thang/cổng ____; nguồn đang nối ____; ảnh TOP/BOTTOM ____.

## 1. Số đo vật lý

| Cần đo theo mục 3.3 | Giá trị thực / ảnh | Quyết định / chưa rõ |
|---|---|---|
| Board: hàng/cột, pitch, khoảng mép A1, pad rời | ____ | ____ |
| ESP32: hai hàng chân, thân, nhãn hãng/revision/VIN/3V3/GND/GPIO | ____ | ____ |
| Chân cuối tới đầu và điểm bắt đầu ăng-ten | ____ | ____ |
| TP4056: thân/pad/cổng | ____ | ____ |
| MT3608: thân/pad/cuộn cảm/biến trở | ____ | ____ |
| IMU: mười chữ chân/chiều trục | ____ | ____ |
| SS12D00: pitch, COM, cặp ON/OFF | ____ | ____ |
| SW2/SW3/SW4: bốn chân, nhóm A/B, cap | ____ | ____ |
| J1/J5V: đầu ghép, cực, lực giữ/dòng tiếp điểm | ____ | ____ |
| Vùng pin/vỏ, cả pack/PCM/tab/dây | ____ | ____ |
| Pin: áp và cực tại giắc, dung lượng/dòng sạc nếu biết | ____ | ____ |

## 2. Đo nguội — rút mọi nguồn, xác nhận tụ xả

| Cặp/nhánh | Thang/giá trị | Kết luận người đo |
|---|---|---|
| Hai đầu **từng dòng** §3.7 | ____ | CHƯA ĐO |
| OUT-–G*, G*–VIN-/VOUT-/U1 GND/U2 GND/TP4 | ____ | CHƯA ĐO |
| 3V3–U2 VCC/NCS/TP3 | ____ | CHƯA ĐO |
| GPIO21–SDA/TP2; GPIO22–SCL/TP1 | ____ | CHƯA ĐO |
| SW1 OUT+–COM | ____ | CHƯA ĐO |
| Hai nhóm SW2/3/4 | ____ | CHƯA ĐO |
| 5V–GND | ____ | CHƯA ĐO |
| 3V3–GND | ____ | CHƯA ĐO |
| VBAT–GND | ____ | CHƯA ĐO |
| VBAT–GND_BAT_CELL (B+–B-) | ____ | CHƯA ĐO |
| 5V–3V3 | ____ | CHƯA ĐO |
| GND_BAT_CELL–GND | ____ | CHƯA ĐO |
| BAT_SENSE–V_SYS / BAT_SENSE–GND | ____ | CHƯA ĐO |
| INT/ACL/ADA, SW1 chân NC, lỗ socket thừa | ____ | CHƯA ĐO |

J5V rút: ngắt VOUT+–VIN trên carrier khi module/nguồn đã tách; kết quả ____; ảnh ____.

## 3. Điện áp theo bảng 3.8.2

| Điểm / điều kiện | Mục tiêu | Đo thực / điểm âm | Kết luận |
|---|---|---|---|
| B+ so B- / Pack nối đúng, chưa sạc | Danh định 3.7V; dải thiết kế 3.0–4.2V | ____ / ____ | CHƯA ĐO |
| OUT+ so OUT- / Bảo vệ cho phép xuất điện | Gần điện áp pack; chênh lệch do bảo vệ/dây | ____ / ____ | CHƯA ĐO |
| V_SYS so GND / SW1 ON, chạy pin | 3.0–4.2V theo thiết kế, có sụt áp tải | ____ / ____ | CHƯA ĐO |
| V_SYS so GND / OFF, không USB/nguồn ngoài | Gần 0V sau khi tụ xả | ____ / ____ | CHƯA ĐO |
| VOUT+ so VOUT- / Boost rời, rồi có tải | Mục tiêu 5.0V, 4.9–5.1V | ____ / ____ | CHƯA ĐO |
| VIN ESP32 so GND / Chạy từ boost, USB rút | 4.9–5.1V tại chân bo | ____ / ____ | CHƯA ĐO |
| 3V3/TP3, U2 VCC / Chỉ một nguồn cho ESP32 | Mục tiêu 3.3V, khoảng thiết kế 3.25–3.35V | ____ / ____ | CHƯA ĐO |
| BAT_SENSE, GPIO34 / V_SYS đang có nguồn | Khoảng 0.5×V_SYS; 1.5–2.1V danh định theo dải thiết kế | ____ / ____ | CHƯA ĐO |
| SCL/SDA, TP1/TP2 / Bus nghỉ, có pull-up của đúng module | Gần 3V3 khi nghỉ; lúc truyền đồng hồ có thể chỉ số trung bình | ____ / ____ | CHƯA ĐO |
| GPIO25/26/27 / Firmware bật INPUT_PULLUP | Thả gần 3V3, nhấn gần GND | ____ / ____ | CHƯA ĐO |
| GPIO32→R1; D1 A/K / LED được firmware bật | GPIO cao gần 3V3; Vf của LED thật **CẦN ĐO THỰC TẾ** | ____ / ____ | CHƯA ĐO |
| B+ so B-, cuối sạc / Khi có pin thật, theo nhánh §3.9.2 | Danh định 4.2V; đối chiếu giới hạn pack và bảng VFLOAT của [T] | ____ / ____ | CHƯA ĐO |

## 4. Checklist từng giai đoạn

- [ ] Logic: soi/đo nguội, 3V3, nút/LED đo độc lập.
- [ ] Nguồn: thử J1/bảo vệ/SW1/boost/J5V/phân áp đúng chuỗi, có tải.
- [ ] Cơ khí: vùng pin trống, Kapton/mút, gá/cap/ăng-ten đạt số đo.
- [ ] Chủ dự án đã nạp/quét I2C/chức năng; log/ngày ____; chưa thì giữ trống.
- [ ] Có pin thật, đã đo cực/thử ngày pin về; chưa có thì giữ trống.
- [ ] Sạc: dòng/nhiệt/áp cuối ghi thật; chưa thử giữ trống.

## 5. Vấn đề gặp / ảnh đính kèm

| Bước / triệu chứng | Nguồn đang nối | Ảnh và số đo | Xử lý / cần hỏi |
|---|---|---|---|
| ____ | ____ | ____ | ____ |

Ghi CHƯA ĐO hoặc CẦN ĐO THỰC TẾ khi thiếu; không điền số giả hay coi tài liệu là kết quả kiểm.
