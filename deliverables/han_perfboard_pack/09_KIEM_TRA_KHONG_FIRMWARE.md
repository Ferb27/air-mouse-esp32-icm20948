# Kiểm tra không cần firmware

Nguồn: mục 3.6–3.8 và 3.13 hướng dẫn V2; điện áp/giá trị không thay đổi. Chỉ kiểm đường điện và phần tử rời; quét 0x68/WHO_AM_I, nạp mã, chức năng chuột và báo pin là **BƯỚC PHẦN MỀM — để chủ dự án làm**.

## 1. Soi và đo nguội

1. Rút pin, nguồn thay pin và hai USB; đo DC xác nhận tụ xả.
2. Rút ESP32/IMU khỏi socket, soi từng khe pad; đo từng dòng mục 3.7 và cặp cấm mục 3.8.1.
3. Đo nút rời hoặc cô lập nhánh: hai chân cùng nhóm luôn thông, A↔B thả hở/nhấn thông; không suy nhóm từ hướng nhìn chân.
4. Đo R1 rời khoảng 1 kΩ, R2/R3 mỗi con 100 kΩ, dung sai 1% cộng sai số đồng hồ.

## 2. Nguồn 3V3 khi chỉ USB ESP32

1. J5V rút, J1 trống, USB TP4056 rút; cắm ESP32 đúng socket khi không điện.
2. Cắm USB ESP32, đo DC đỏ 3V3/TP3, đen GND: tiêu chí 3.25–3.35V (mục tiêu 3.3V) theo bảng 3.8.2.
3. Tắt/rút nguồn trước khi cắm IMU; đối chiếu đúng VCC/GND/NCS/AD0/FSY. Có 3V3 chưa chứng minh bus I2C hoặc độ bền Direct 3.3V.

## 3. Thử LED + R1, tách khỏi GPIO32

Chỉ áp dụng khi đã xác nhận đúng D1 LED xanh 3 mm và R1 1 kΩ theo BOM, nhận đúng A/K bằng diode test. Netlist cho Vf tham khảo 2.0–2.2V: với 3.3V, `I=(3.3−Vf)/1000 ≈ 1.1–1.3 mA`. Đây là ước lượng, Vf thật cần đo; kể cả lấy Vf=0, 3.35V/990Ω≈3.4 mA là chặn trên của nhánh R1 đã xác nhận, không phải thông số định mức của LED bất kỳ.

1. Rút toàn bộ nguồn; **rút ESP32 khỏi carrier** để chân GPIO32 của module không còn dính R1.1. Không chập 3V3 vào GPIO32 của module đang cắm.
2. Giữ D1 K→GND carrier và R1.2→D1 A đúng bảng, J5V rút; xác nhận R1 không bị cầu nối bỏ qua.
3. Đặt ESP32 riêng trên đệm cách điện. Khi chưa USB, nối GND ESP32→G* carrier và một dây thử 3V3 ESP32→R1.1; không nối chân 3V3 vào VIN hoặc đưa 5V vào nhánh.
4. Cấp duy nhất USB cho ESP32 rời, đo nguồn trong 3.25–3.35V; quan sát LED ngắn để xác nhận chiều/mối nối. Nóng, dòng bất thường, không rõ R1/D1 hoặc dây → ngắt, không tăng áp/bỏ R1.
5. Rút USB, tháo hai dây thử, cắm lại module đúng socket khi không điện; kiểm net GPIO32→R1.1 nguyên như bảng.

⚠ Chỉ diode test cũng có thể không đủ áp để làm LED sáng; không sáng chưa chứng minh LED hỏng. Không dùng 5V hoặc nối trực tiếp LED để thử.

## 4. Boost và toàn đường nguồn không pin

Làm đúng mục 3.13.2: nguồn thay pin 3.7–4.2V, giới hạn ≤500 mA, cả hai USB rút. Chỉnh không tải 5.0V trước ghép J5V; sau đó đo VIN 4.9–5.1V, 3V3 3.25–3.35V và BAT_SENSE≈0.5×V_SYS có tải. Không có nguồn phù hợp thì ghi CHƯA THỬ, không lấy USB 5V cắm J1.

**Cách ghi trạng thái:** “Đã kiểm điện bằng đồng hồ; phần mềm chưa thử” khi chỉ hoàn tất các phép trên. Không tick các ô nạp/I2C/chức năng trong mục 3.13.1 thay chủ dự án. Pin thật, sạc và thời lượng vẫn chưa kiểm trước ngày pin về.
