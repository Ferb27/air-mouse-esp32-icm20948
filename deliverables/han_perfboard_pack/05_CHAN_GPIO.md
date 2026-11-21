# Chân GPIO dùng trong mạch

Nguồn: định nghĩa GPIO và netlist trích trong gói; không phải sơ đồ chân vật lý. **CẦN ĐO THỰC TẾ** nhãn đúng ESP32 Classic 38 chân.

| Nhãn | Số theo netlist | Nối tới |
|---|---|---|
| 3V3 | 1 | U2 VCC/NCS; TP3 |
| VIN/5V | 19 | Từ J5V.1 cái |
| GND | 14, 32, 38 | G* và J5V.2 cái |
| GPIO21 | 33 | IMU SDA, TP2 |
| GPIO22 | 36 | IMU SCL, TP1 |
| GPIO25 | 9 | SW2 nhóm A |
| GPIO26 | 10 | SW3 nhóm A |
| GPIO27 | 11 | SW4 nhóm A |
| GPIO32 | 7 | R1.1 → D1 A |
| GPIO34 | 5 | BAT_SENSE; không nối trực tiếp pin/5V |

IMU 0x68 khi AD0=GND; GPIO34 input-only chỉ BAT_SENSE. Chân không dùng để hở.
