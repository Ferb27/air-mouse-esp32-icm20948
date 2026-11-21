# Hướng dẫn hàn Air Mouse trên board đục lỗ — V2

> Bản dành cho người hàn, 16/10/2026: đã đổi liên kết sang gói và đánh dấu phần mềm để chủ dự án làm. Bảng 43 dòng/tọa độ giữ nguyên. Xem [hình tổng hợp](hinh/00_TONG_HOP_HINH.html) và [kiểm tra bằng đồng hồ](09_KIEM_TRA_KHONG_FIRMWARE.md).

Ngày tạo: **15/10/2026**. Cập nhật V2: **16/10/2026**. Mọi phép đo và ô tick dưới đây do **người lắp thực hiện**; chưa có kết quả đo phần cứng của lần biên soạn.

## Nhật ký thay đổi V2

1. Một board chính **90×150 mm**, pitch **2.54 mm** [P2] §1; board 10×10 cm chỉ là tùy chọn thử trước.
2. Ba giai đoạn trên cùng board: logic USB → nguồn thay pin → cơ khí; dùng socket để rút module khi hàn tiếp.
3. Pin **1S có mạch bảo vệ, chưa xác định**; chuẩn bị giắc JST-PH 2.0 hai chân, ưu tiên dung lượng ≥1000 mAh [P2] §2.1.
4. Giữ TP4056 nguyên trạng, dòng sạc khoảng 1 A; phân tích nhánh pin nhỏ ở §3.9.2.
5. Bổ sung J5V tháo rời, nhãn **“5V — RÚT KHI CẮM USB”**.
6. Dịch ESP32 sang phải ba cột và IMU sang trái; dành vùng pin **60.96×40.64 mm**, tính từ lưới, gồm viền ≥2 mm [P2] §2.5.
7. Giữ nguyên GPIO/net; C2 song song nguồn; B- tách OUT-. Không sửa firmware/KiCad.
8. Thêm §3.13: điều kiện sẵn sàng, thử không pin, chuẩn J1, ngày pin về và vật tư thiếu.

⚠ Không nối tắt **B- với OUT-**; không đưa 5V vào GPIO34/IMU. Sai có thể mất bảo vệ pin hoặc hỏng linh kiện.

**Khi chạy pin thì cắm đầu nối 5V; khi cắm USB vào ESP32 thì RÚT đầu nối 5V. Không bao giờ cắm USB ESP32 lúc đầu nối 5V còn cắm.**

## Nguồn đã đọc, giả định và khác biệt cần biết

Ký hiệu [ ] trỏ nguồn; số mục thuộc tài liệu gốc, mã nguồn trỏ hằng/hàm.

| Mã | Tài liệu đã đọc | Dùng để làm gì |
|---|---|---|
| [P2] | [PROMPT_ANTI_SUA_HUONG_DAN_V2.md](08_NGUON_TRICH_DAN.md), §§0–5 | Yêu cầu V2, ưu tiên khi khác [P]/BOM cũ |
| [P] | [PROMPT_ANTI_HUONG_DAN_HAN_PERFBOARD.md](08_NGUON_TRICH_DAN.md), §§0–5 | Yêu cầu V1; phần khác V2 xem [P2] |
| [B] | [BOM_FINAL_perfboard_2026-10-14.csv](03_BOM_VAT_TU.csv), STT 1–18, 20–32 | Linh kiện cần hàn; thông số mua hàng chưa thay thế đo đạc |
| [N] | [SCHEMATIC_NETLIST.md](04_NOI_DAY_NETLIST.md), §§1–4 | Tên net, chân nối, tách âm pin và mass hệ thống |
| [F] | [pin_definitions.h](05_CHAN_GPIO.md), các khối I2C, Buttons, LED, Battery | GPIO, địa chỉ IMU |
| [A] | [AIR_MOUSE_HARDWARE_ARCHITECTURE.md](08_NGUON_TRICH_DAN.md), §§1.3, 4–6 | Baseline Direct 3.3V, khoảng cách và nguồn |
| [M] | [PCB_MECHANICAL_PLACEMENT.md](06_KICH_THUOC_MODULE.md), §§1–4, 6 | Tham khảo kích thước; không sao chép bố cục PCB sang perfboard |
| [H] | [HARDWARE_BRINGUP_DIRECT_3V3_2026-09-25.md](08_NGUON_TRICH_DAN.md), §§2–4 | Bằng chứng lịch sử trên đúng bộ ESP32 + IMU sở hữu |
| [W] | [Báo cáo tuần 5](08_NGUON_TRICH_DAN.md), §§3, 5–6 | Giới hạn BLE và đo pin |
| [O] | [air_mouse.docx](08_NGUON_TRICH_DAN.md), phần kiến trúc dự kiến | Tài liệu gốc thời ICM-20602/SPI; không dùng làm sơ đồ đấu dây hiện tại |
| [FW] | [mô tả phần mềm trong bản trích nguồn](08_NGUON_TRICH_DAN.md), `setup()`, `loop()`; [mô tả phần mềm trong bản trích nguồn](08_NGUON_TRICH_DAN.md), `imu_init()`; [mô tả phần mềm trong bản trích nguồn](08_NGUON_TRICH_DAN.md), `env:esp32dev` | Hành vi nút, LED, readback và lệnh build |
| [PR] | [mô tả phần mềm trong bản trích nguồn](08_NGUON_TRICH_DAN.md), `scanI2C()`, `setup()`; [mô tả phần mềm trong bản trích nguồn](08_NGUON_TRICH_DAN.md) | Quét địa chỉ và đọc WHO_AM_I bằng chương trình có sẵn |

Nguồn ngoài đã kiểm tra ngày 15/10/2026:

| Mã | Nguồn chính thức và vị trí | Giới hạn áp dụng |
|---|---|---|
| [E1] | Espressif, [DevKitC V4 User Guide](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html), Power Supply Options | Chỉ cấp một trong các đường USB, 5V, 3V3 |
| [E2] | Espressif, [ESP32_DevKitc_V4 schematic](https://dl.espressif.com/dl/schematics/esp32_devkitc_v4-sch.pdf), V4, 06/12/2017, trang 1, khối Power Supply, D3 BAT760-7 | Sơ đồ tham chiếu; chưa xác định hãng/revision bo thật |
| [E3] | Espressif, [Hardware Design Guidelines: placement for modules](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/pcb-layout-design.html#general-principles-of-pcb-layout-for-modules-positioning-a-module-on-a-base-board) | Ăng-ten ngoài mép bo; khoảng hở khuyến nghị ít nhất 15 mm |
| [T] | NanJing Top Power ASIC Corp., [TP4056 REV_2.3](https://toppwr.com/uploadfile/file/20240130/65b892bb04a3c.pdf), trang 2, 5, 7 | Sạc CC/CV, 4.2V; bảng RPROG 1.2 kΩ cho dòng điển hình 1 A; TEMP có thể bị vô hiệu hóa |
| [L] | Adafruit, [Charge Rate](https://learn.adafruit.com/adafruit-microlipo-and-minilipo-battery-chargers/charge-rate), tác giả lady ada, trang công bố 2014/cập nhật 2024 | Khuyến nghị chung tối đa khoảng 1C; không chứng nhận định mức cho một pack cụ thể |
| [S] | HAKKO, [Tip oxidation](https://www.hakko.com/english/support/maintenance/detail.php?seq=103); [HAKKO 375, Test criteria](https://www.hakko.com/english/products/hakko_375.html) | Quản lý nhiệt, oxy hóa đầu mỏ; hãng có thử SAC ở 350°C, không phải quy trình riêng cho bộ linh kiện này |
| [PIO] | PlatformIO, [run](https://docs.platformio.org/en/latest/core/userguide/cmd_run.html), [device monitor](https://docs.platformio.org/en/latest/core/userguide/device/cmd_monitor.html) | Đã đối chiếu cú pháp với `python -m platformio ... --help` tại máy này; Core 6.2.0 |

**Giả định:** perfboard có pad đồng rời; dùng đúng ESP32 Classic 38 chân và IMU từng thử trong [H]. Đổi IMU cần xác minh lại Direct 3.3V. Tọa độ là đề xuất, phải lắp khô. “Cắm là chạy” chỉ áp dụng cho pin đúng điện áp, cực, giắc, dòng và kích thước §3.13, không phải mọi pin 1S.

| Điểm khác hồ sơ cũ | Áp dụng V2 | Căn cứ |
|---|---|---|
| PCB 130×70 mm, hai board bắt buộc | Một perfboard 90×150 mm; board khác chỉ thử tùy chọn | [P2] §1 |
| BOM STT 17 còn tên pin cũ/dây trần; STT 1 còn nhắc đổi RPROG | Pin chưa chọn; ưu tiên 1S 3.7V PCM, JST-PH 2.0, ≥1000 mAh; giữ RPROG | [P2] §§0–2; giữ dòng CSV cũ theo yêu cầu, không đặt pin theo STT 17 cũ |
| Vùng pin nhỏ V1 | Vùng cấm 60.96×40.64 mm gồm viền, không chân/vít/dây | [P2] §2.5; tính lưới §3.5 |
| J2 và TP8–TP11 | Chỉ test 1×4 SCL/SDA/3V3/GND; đo nguồn tại pad module | [P] §2, [N] §2 |
| Socket 2×19, cap tròn | Hai cái 1×20 nguyên thanh, mỗi thanh thừa một lỗ; cap vuông thử trước | [B] STT 5–6, 13–14 |
| “Qua C2”, nút ON/OFF | C2 song song; GPIO27 hiện là clutch, SW1 ngắt nguồn | [N] §2 dòng 11–13, [FW] `loop()` |
| Có GPIO34 nên tưởng đã báo pin yếu | Giữ phân áp; firmware hiện chưa đọc ADC | [F], [W] §6, [FW] |

## 3.0. Tóm tắt một trang

Hoàn thiện board chính để chỉ còn chọn pin đúng quy cách, đo cực rồi cắm. Phát triển firmware ngoài phạm vi; chỉ dùng chương trình thử có sẵn để kiểm phần cứng, không sửa mã. **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.

| Giai đoạn trên board 90×150 mm | Việc làm | Điều kiện chuyển bước | Thời gian ước lượng |
|---|---|---|---|
| Chuẩn bị | Đo, lắp khô, tập hàn | Chốt lỗ/chiều chân/vùng pin | 45–90 phút |
| 1. Logic USB | ESP32, IMU, ba nút, R1/LED, test point | 0x68, nút/LED đạt hoặc ghi chưa thử | 2–4 giờ | **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
| 2. Nguồn thay pin | TP4056, SW1, boost, phân áp/tụ, J1/J5V | Đo không tải/có tải theo §3.13.2 | 2–3 giờ |
| 3. Cơ khí | Cách điện, gá, nắp nút, vùng pin | Không chân nhọn/đè pin | 30–60 phút |
| Ngày pin về | Kiểm pin, cực và §3.13.4 | Kiểm riêng pin thật/sạc | Chạy đầu 5 phút là mốc đề xuất [P2] §3.13.4; sạc chưa biết |

Thời gian hàn là **ước lượng**, không phải số đo. Board 10×10 cm không cần cho quy trình này.

```text
Pin / nguon thay pin (+) --> J1(+) --> B+   TP4056 OUT+ --> SW1 --> V_SYS --> MT3608 VIN+
Pin / nguon thay pin (-) --> J1(-) --> B-         OUT- --> GND ------------ MT3608 VIN-
 [khong noi tat B- voi OUT-]                          MT3608 VOUT- --> GND

MT3608 VOUT+ --> 5V --> J5V.1 duc <-> cai.1 --> ESP32 VIN/5V
                  |    J5V.2 duc <-> cai.2 --> ESP32 GND
                  |         ^ GND (khong phai cau noi tat 2 chan)
                  +--> C2(+) ; C2(-) --> GND
ESP32 3V3 --> IMU VCC,NCS ; GPIO21/22 --> SDA/SCL
V_SYS --> R2 -->+--> R3 --> GND
               | BAT_SENSE
               +--> C1 --> GND
               +--> GPIO34
```

Nguồn: [N] §§2–4, [F]; J5V thêm điểm ngắt tháo rời theo [P2] §2.2, không đổi net khi ghép đúng. GND ESP32 còn dây về mass chung như §3.7.

## 3.1. Dụng cụ và vật tư

| Mức | Cần có | Dùng để làm gì |
|---|---|---|
| Bắt buộc | Mỏ hàn, đế gác, đầu mỏ sạch | Gác an toàn; nên có chỉnh nhiệt |
| Bắt buộc | Thiếc lõi flux, flux điện tử | Sn63/Pb37 dễ hàn nhưng có chì; SAC không chì cũng dùng được; không axit hàn ống nước |
| Bắt buộc | Bơm hút hoặc dây hút thiếc | Sửa cầu/lỗ, không giật chân khi thiếc đông |
| Bắt buộc | Đồng hồ, que/kẹp cách điện, cầu chì A tốt | DC/ohm/diode/thông mạch; đọc đúng hướng dẫn model |
| Bắt buộc | Kìm cắt/tuốt 28AWG, nhíp, kính bảo hộ | Tránh cắt xước lõi và chân bắn vào mắt |
| Bắt buộc | Kẹp board, băng giấy, lúp/camera phóng đại | Giữ linh kiện, soi mối trước cấp nguồn |
| Bắt buộc | Thước kẹp/thước chia nhỏ, bút | Đo lỗ, linh kiện, nhãn cực/vùng pin |
| Bắt buộc | Co nhiệt, Kapton, mút EVA/PE, băng hai mặt, gá cách điện | Bọc chân và giữ module; mút 1–2 mm [P]/[M] §4 |
| Bắt buộc | Thông gió/hút khói | Tránh hít khói flux, không ăn uống khi hàn |
| Nên có khi sạc | Nhiệt kế đầu dò cách điện | Đo vỏ pin riêng với nhiệt IC |
| Cần để kiểm nguồn theo kịch bản | Nguồn bàn giới hạn dòng và dây thử J1, có thể mượn | Thử §3.13.2; nguồn chỉ cấp dòng không phải tải mô phỏng để thử sạc |
| Nên có | Cáp USB dữ liệu góc vuông, breadboard | Dễ tiếp cận cổng/thử module rời |

**Nhiệt khởi đầu đề xuất, phải thử pad dư:** khoảng 320–350°C với Sn63/Pb37, khoảng 350°C với SAC, đều là **ước lượng thực hành**, không phải giới hạn linh kiện. [S] hỗ trợ quản lý nhiệt và có thử SAC 350°C. Chọn mức thấp nhất vẫn làm ướt chân/pad nhanh; không tăng nhiệt để chữa đầu mỏ bẩn/thiếu flux. Mỏ không chỉnh nhiệt: tập trước, nhờ người có kinh nghiệm kiểm mối nếu chưa ướt đều.

## 3.2. An toàn

1. Dọn vật dễ cháy, bật hút khói, đặt đế mỏ chắc; đeo kính và rửa tay sau hàn, nhất là thiếc chì.
2. Rút pin, hai USB và nguồn thay pin trước khi hàn/đo ohm; đo DC xác nhận tụ xả, không chập tụ bằng tua vít.
3. Nếu phải xử lý dây pin: che kín một dây trước khi làm dây kia; chỉ nối vào dây pack sẵn, không hàn lên túi/tab cell/PCB bảo vệ.
4. Co nhiệt từng mối ngay, không thổi nóng vào túi pin. Giữ PCM, không bypass B-/OUT-.
5. Cắt/bọc lưới và drain DB9 thừa; nhặt râu kim loại trước cấp điện.
6. Chỉ cấp nguồn sau soi mối hàn và đo nguội §3.8; SW1 OFF trước ghép/rút J1/J5V.

⚠ Pin vẫn có điện khi SW1 OFF. Đầu dây/terminal trần chạm nhau có thể gây cháy; không chập/đâm thủng/ép túi pin.

⚠ Pin phồng/rách/mùi/rò/nóng bất thường: ngắt phía nguồn sạc nếu an toàn và dừng dùng. Không bóp/đâm/thử xả/sạc lại. Không cầm pin đang bốc khói; tránh xa, báo người xung quanh và lực lượng ứng cứu địa phương khi cần. Pin nguội ổn định đưa tới nơi thu gom phù hợp, không bỏ rác sinh hoạt.

## 3.3. Đo vật lý trước khi hàn

Điền số đo trước khi chốt lỗ. Thông số mua hàng [B]/[M] không thay linh kiện thực.

| Cần đo/xác nhận | Kết quả người lắp điền | Quyết định phụ thuộc |
|---|---|---|
| Board: số hàng/cột, pitch, khoảng tâm A1 tới hai mép; pad có nối dải không | ____; **CẦN ĐO THỰC TẾ** | Dùng được lưới §3.5 không |
| ESP32: hai hàng chân, pitch dọc, đủ 38 chân, thân nhô khỏi socket | ____ mm | Chọn U/AE hoặc U/AD, khe hở IMU |
| ESP32: hãng/revision, USB, nhãn VIN/3V3/GND/GPIO | ____ | Đấu theo chữ, không theo số đếm netlist |
| Chân cuối tới đầu và điểm bắt đầu vùng ăng-ten | ____ / ____ mm | Cả vùng ăng-ten nhô khỏi board |
| TP4056: thân, cổng, B+/B-/OUT+/OUT-, điểm gá | ____ | Đúng bản bảo vệ, lọt khung nguồn |
| MT3608: thân, pad, cuộn cảm/biến trở | ____ | Lọt khung, cách IMU, chỉnh được |
| IMU: thân, pitch, thứ tự chữ chân, hướng trục | ____ | Chiều socket C42…L42 |
| SW1: pitch, COM, cặp đóng mỗi vị trí | ____ | Gá mép, nối dây nếu khác lưới |
| Nút: bốn chân/hai nhóm thông; cap B3F vừa/kẹt/lỏng | ____ | Chốt lỗ thật, không ép chân |
| Vùng pin cả TOP/BOTTOM và khoảng cao tới vỏ | ____ mm | Pack cả PCM/tab/dây phải lọt |
| J1: kiểu ghép/cực tại mặt cắm; J5V: lực giữ/cực/dòng tiếp điểm | ____ | Chọn đầu pin và đánh dấu hướng |

Pin chưa có: để trống model/dung lượng/kích thước. Ưu tiên 1S 3.7V PCM, giắc cái JST-PH 2.0 hai chân, ≥1000 mAh [P2] §2.1. Pack tham chiếu 523450 khoảng 50×34×5.2 mm [M] §§1.2/4; kích thước cả PCM/đầu dây và dòng sạc/xả **CẦN XÁC NHẬN**.

⚠ Khoảng chân nút công bố 5.0×12.5 mm [B] STT 5 chưa trùng bội số 2.54 mm. Không vừa thì gá riêng và nối dây cách điện; ép chân có thể nứt nút/bong pad.

## 3.4. Kiểm tra và chuẩn bị module rời

### 3.4.1. Hàn header đực IMU

1. Đối chiếu mười chữ chân với §3.7; chưa khớp thì dừng.
2. Lấy mười chân từ dải đực 1×40 [B] STT 12; gá phần dài xuống breadboard **không điện**, phần ngắn xuyên module.
3. Hàn một đầu, để nguội và kiểm tra thẳng; làm chảy lại mối nếu cần chỉnh, không bẻ mối nguội.
4. Hàn đầu kia, kiểm tra rồi hàn các chân còn lại.
5. Rút sau nguội; soi khe chân, đo chân–pad đúng, không cầu thiếc.

### 3.4.2. Thử logic trên board chính, chỉ USB

**BƯỚC PHẦN MỀM — để chủ dự án làm:** quét I2C 0x68, WHO_AM_I 0xEA, nạp mã, kiểm chức năng nút/LED/ADC. Người hàn không cần cài công cụ hoặc nạp chương trình. Chưa thực hiện ghi CHƯA THỬ PHẦN MỀM.

Dùng [đường kiểm tra bằng đồng hồ](09_KIEM_TRA_KHONG_FIRMWARE.md). Không dựa vào LED/khởi động của chương trình chưa biết để kết luận dây đúng.

### 3.4.3. Chỉnh MT3608 trước khi nối ESP32

**Khi chạy pin thì cắm đầu nối 5V; khi cắm USB vào ESP32 thì RÚT đầu nối 5V.**

1. Rút J5V, USB ESP32 và USB TP4056; nhận pad bằng chữ module.
2. Ưu tiên nguồn bàn 3.7–4.2V qua J1, giới hạn ≤500 mA theo [P2] §3.13.2; xem đủ §3.13.2. Thử riêng boost có thể cấp cùng nguồn vào VIN+/VIN-, nhưng chưa kiểm chuỗi J1/TP4056/SW1.
3. Kẹp đồng hồ DC đỏ VOUT+, đen VOUT- khi nguồn tắt, rồi bật nguồn.
4. Vặn ít một và đọc chiều tăng/giảm; chiều vặn đúng module **CẦN XÁC NHẬN**, không cố qua chặn.
5. Chỉnh 5.0V, khoảng thiết kế 4.9–5.1V [A] §5.1, [N] §1; tắt/bật để đo lại.
6. Đo có tải theo §3.13.2. Nếu giới hạn dòng/sụt áp/reset thì dừng tìm nguyên nhân, không tăng quá 500 mA để hết reset.

⚠ Đầu ra chưa chỉnh có thể phá DevKit. Không nối ESP32 trước khi đo đúng; nhãn boost “2A” không bảo đảm dòng ra ở điều kiện pin này.

### 3.4.4. TP4056 nguyên trạng, thử sạc khi có pin

Giữ RPROG; dòng cài đặt **khoảng 1 A**, dòng thật phụ thuộc module/nhiệt/trạng thái pin [T]. Quy tắc chọn sơ bộ ≤1C [L]: 1 A là 1C ở 1000 mAh; pin nhỏ hơn vượt 1C (400 mAh là 2.5C, tính toán). Chọn nhánh §3.9.2, không coi dung lượng là chứng nhận an toàn.

1. Chưa có pin: nhận B+/B-/OUT+/OUT-, kiểm dây và thử **đường xả** bằng nguồn thay pin §3.13.2. Không cắm USB TP4056 khi nguồn thay pin còn nối J1; không dùng nguồn bàn chỉ cấp dòng làm pin để thử sạc.
2. Có pin: hoàn tất thử chạy §3.13.4; SW1 OFF, J5V rút, USB ESP32 rút để sạc riêng.
3. Đọc giới hạn pack nếu có, chọn nhánh giám sát §3.9.2; điều chưa biết ghi **CẦN XÁC NHẬN**, không coi là kết quả đạt hay chặn việc hàn.
4. Chưa cắm USB sạc: ngắt dây dương pin, chèn ampe kế `pin+ → que đỏ/cổng A có cầu chì → COM → B+`; pin− vẫn về B-. Chọn thang/cổng chịu dòng theo hướng dẫn đồng hồ.
5. Bọc/kẹp chắc, ưu tiên nhiệt kế cách điện trên vỏ pin rồi cấp USB 5V vào TP4056 [T]. Ghi dòng phía pin và theo dõi nhiệt suốt lần sạc.
6. Ngắt USB trước khi tháo đồng hồ A; chuyển que về cổng V, nối kín dây rồi đo DC B+–B-. Dòng USB không thay dòng pin.
7. Theo dõi dòng giảm/điện áp cuối. TP4056 danh định 4.2V, bảng VFLOAT 4.158–4.242V trong điều kiện [T] trang 5. Vượt giới hạn pin hoặc tăng bất thường thì ngắt; cực đại IC không phải giới hạn an toàn mọi pack.
8. Rút USB và ghi kết quả; đèn đầy không chứng minh đúng dòng/nhiệt.

⚠ Ampe kế chạm ngang hai cực pin gần như gây chập, có thể cháy/đứt cầu chì. Chỉ mắc nối tiếp, không đổi thang/rút que khi đang sạc.

## 3.5. Bố cục trên board

### 3.5.1. Lưới và điều kiện áp dụng

**Bố cục đề xuất, điều chỉnh sau khi đo thực tế.** Nhìn TOP: nút phía trước, ăng-ten hướng sau. Cột A…Z, AA…AG tăng trái→phải; hàng 1…57 tăng trước→sau. Lật BOTTOM bị đảo trái/phải: đánh dấu A1 và góc phụ trước khi lật, không đếm lại từ trái mặt hàn.

Board 90×150 mm, pitch 2.54 mm [P2] §1. Dựng hình với giả định **ước lượng** A1 cách hai mép 3 mm; phải đo lại. Tâm lỗ `x=3+(cột−1)×2.54`, `y=3+(hàng−1)×2.54` mm. A…AG có 33 cột, 1…57 có 57 hàng; khoảng tâm ngoài 81.28×142.24 mm (tính toán), chưa khẳng định board mua được đủ lỗ.

### 3.5.2. Ba giai đoạn trên cùng board

1. Hàn logic tại vị trí cuối, cấp USB kiểm thử; chưa nối TP4056/boost/pin. Chừa vùng pin/nguồn ngay từ đầu.
2. Rút USB và module khỏi socket; hàn nguồn, J1/J5V, R2/R3/C1/C2. Đo nguội, thử nguồn thay pin §3.13.2.
3. Rút mọi nguồn; gá/cách điện rồi đo lại. Board 10×10 cm chỉ thử tùy chọn, không phải chuyển linh kiện qua board khác.

### 3.5.3. Sơ đồ và tọa độ board chính

```text
TOP   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC AD AE AF AG
01    +------------------------------------------------------------------+
05    |             SW2 H5                SW4 R5              SW3 AB5    |
08    |                     het vung nut du kien                         |
09    | TP4056 A9..L17                                                   |
10    |                               MT3608 N10..AC17                   |
17    |                     het cum nguon phia truoc                     |
19    | R1 D19--H19    D1 K19/L19                       SW1 AA19..AG22   |
21    | +------------------- B21..Z37 -------------------+               |
22    | |        VUNG PIN BOTTOM / CAM CHAN HAN           |               |
25    | |                                                | R2 AA25/AA29 |
29    | |     KHONG DAY, VIT, PAD HAN NOI, CHAN THT        | R3 AA29/AA33 |
31    | |                                                | C1 AC29/AC31 |
34    | |                                                | J5V AC34/AD34|
35    | |                                                | C2 AE35/AG35 |
37    | +------------------------------------------------+               |
38    |                                         U38             AE38     | lo thua
39    |                                         | USB huong vao   |      |
41    | IMU than B41..M47                        |                 |      |
42    |   C42=============L42                   |     ESP32       |      |
47    |                                         |                 |      |
50    | TP B50 SCL                              |                 |      |
51    | TP B51 SDA                              |                 |      |
52    | TP B52 3V3                              |                 |      |
53    | TP B53 GND                              |                 |      |
57    +-----------------------------------------U57-------------AE57-----+
                                              ANTEN NGOAI MEP SAU
```

ASCII chỉ phân vùng; bảng chốt tọa độ neo, chưa phải chân thật của nút/module nguồn.

| Cụm | Lỗ/vùng đề xuất | Điều kiện trước hàn |
|---|---|---|
| SW2 trái / SW4 mode / SW3 phải | Tâm H5 / R5 / AB5; vùng dự kiến hàng 2…8 | Tim cách 25.4 mm (10 pitch); đo bốn chân/cap, ghi lỗ thật ____ |
| R1, D1 | R1 D19/H19; D1 A tại K19, K tại L19 | Đo giá trị/cực, nối dây theo §3.7 |
| TP4056 | Thân A9…L17, cổng hướng mép trái | Khung 27.94×20.32 mm tính từ lưới; thân tham chiếu 26×17 mm [M] §1.2; đo/gá thật |
| MT3608 | Thân N10…AC17, biến trở hướng lên | Khung 38.10×17.78 mm; thân tham chiếu 36×17 mm [M] §1.2; đo thật |
| SW1 | Gá mép phải AA19…AG22, chân nối dây | Khung 15.24×7.62 mm; thân/chân **CẦN ĐO THỰC TẾ**, không ép pitch |
| J1 | PH2.0 đực trên dây, gá mép trước/trái ngoài B21…Z37 | Nhãn +/− ở mặt cắm, không tì lên pin |
| G* | Điểm chia mass có bọc tại P39, giữa hai cụm module | Không nối vào B-; thử lắp để không chạm socket/thân module |
| R2 / R3 / C1 | R2 AA25/AA29; R3 AA29/AA33; C1 AC29/AC31 | AA29=BAT_SENSE; C1.1 AC29→AA29, C1.2 AC31→GND |
| J5V | Đực AC34 (+5V), AD34 (GND); cái trên dây VIN/GND | Không dùng shunt chập hai chân; bọc chân, đánh dấu chiều |
| C2 | AE35 (+), AG35 (−) | + phía nguồn J5V.1; − GND; song song trước điểm ngắt |
| IMU | Thân B41…M47; socket C42…L42 | Khung 27.94×15.24 mm; thân tham chiếu 26.7×15.3 mm [M] §1.2; đo độ tràn mép/gá chắc |
| ESP32 | Socket U38…U57 và AE38…AE57 | Dịch phải 3 cột từ R/AB. Cách 25.4 mm; nếu đo 22.86 mm đổi AE→AD. Dự kiến dùng hàng 39…57, thừa hàng 38 phía USB. **Người dùng đã ướm khô ESP32 lên lỗ board (16/10/2026): khớp lưới 25.4 mm**; ESP32 chỉ cắm vào socket, không hàn chết |
| Test point | B50 SCL, B51 SDA, B52 3V3, B53 GND | Header 1×4, TP1/TP2/TP3/TP4 [N] §2 |
| Vùng pin, cả hình chiếu hai mặt | Hình chữ nhật kín B21…Z37 | 60.96×40.64 mm từ 24×16 khoảng lỗ; không chân/dây/vít/pad hàn nổi |

**Vùng pin:** [P2] §2.5 yêu cầu tối thiểu 54×36 mm cộng viền 2 mm mỗi phía, tức **58×40 mm** (tính toán). Vùng chọn 60.96×40.64 mm đáp ứng; bỏ viền 2 mm còn 56.96×36.64 mm. Nên giới hạn cả pack/PCM/tab trong 54×36 mm để còn dư; pin tham chiếu 50×34×5.2 mm [M] cần đo cả phần bọc/PCB. “21×14 lỗ” không đủ: 21×14 tâm lỗ chỉ trải 50.80×33.02 mm. Bản này dùng **25 cột lỗ ×17 hàng lỗ**, không thu nhỏ vùng pin.

**Kiểm tra hình học, tính theo khung giả định:**

1. Với thân ESP32 nhô 1.3 mm ngoài hàng chân [P2] §2.3: mép trái `x_U−1.3=52.50 mm`; mép phải IMU tại M `33.48 mm`; khe dự kiến **19.02 mm**. Cột AE ở x=79.20 mm cho mép phải ESP32 khoảng 80.50 mm, còn trong board 90 mm. Lắp khô module thật, không dùng số này để ép lắp.
2. IMU bắt đầu hàng 41, boost hết hàng 17: khoảng dọc **60.96 mm**; nút hết hàng 8: **83.82 mm**. Vượt mục tiêu IMU–cuộn cảm >36 mm, IMU–nút >30 mm [P2] §2.5, [M] §3.2; đo lại nếu thân/chip/cuộn cảm tràn khung.
3. Vùng pin hết hàng 37, socket bắt đầu hàng 38; kiểm tra mép module/nhựa socket/đầu cáp không đè pin. Dây đi vòng hành lang bên phải, không ngang hình chiếu pin.
4. Chân cuối ESP32 hàng 57 ở y=145.24 mm, còn 4.76 mm tới mép 150 mm (tính toán). Đo tới **điểm bắt đầu vùng ăng-ten**. Chưa ra hẳn thì dịch/cắt mép perfboard trước khi lắp, làm sạch bụi; không cắt DevKit. Khoảng hở 15 mm quanh ăng-ten [E3], không dây/pin/vít.
5. USB hướng vào trong: thử cáp góc vuông/chiều cao đầu cắm; có thể nạp trước đóng vỏ nhưng chừa cách mở/rút module. SW1, J1/J5V phải tiếp cận được.
6. Không lọt linh kiện thật: đưa module nguồn ra gá mép trước, dời nút/LED hoặc tăng board sau đo; **giữ nguyên vùng pin**. Không chồng module nóng/chân nhọn lên pin.

Chiều IMU dự kiến C42 VCC, D42 GND, E42 SCL, F42 SDA, G42 NCS, H42 AD0, I42 INT, J42 FSY, K42 ACL, L42 ADA; chỉ áp dụng nếu chữ in khớp. Ghi tọa độ VIN/3V3/GND/GPIO ESP32 sau lắp khô ____; không suy nhãn từ hàng lỗ.

## 3.6. Thứ tự hàn từ thấp lên cao

Mỗi mối: cố định → ít flux → mỏ chạm chân/pad → thiếc vào chỗ tiếp xúc → rút thiếc → rút mỏ → giữ yên đến đông. Mối tốt ướt đều, không viên rời/cầu thiếc; không chì có thể kém bóng. Không ướt thì dừng, để nguội, làm sạch; không nung mãi.

### 3.6.1. Điện trở

- **Mục tiêu / linh kiện-lỗ:** R1 D19/H19 giai đoạn 1; thêm R2 AA25/AA29, R3 AA29/AA33 giai đoạn 2. [B] STT 8–9, [N] §2 dòng 8/33/36–39.
- **Thao tác:** (1) Đo rời. (2) Uốn chân không sát thân. (3) Gài, hàn từng chân. (4) Che đầu cắt khi cắt thừa.
- **Kiểm tra:** R1 1 kΩ, R2/R3 100 kΩ; dung sai 1% cộng sai số đồng hồ. AA29 là điểm chung cố ý.
- **Lỗi thường gặp:** nhầm 1k/100k, kéo cầu BAT_SENSE sang GND.

### 3.6.2. Tụ

- **Mục tiêu / linh kiện-lỗ:** giai đoạn 2 C1 AC29/AC31; C2 AE35(+)/AG35(−). [B] STT 10–11, [N] §2 dòng 12–13/38/40.
- **Thao tác:** (1) Nhận C1 không cực/vạch âm C2. (2) Đặt đúng. (3) Hàn, cắt chân, đánh dấu +.
- **Kiểm tra:** C1 giữa AA29–GND; C2 phía nguồn J5V.1–GND, không nối tiếp dây 5V.
- **Lỗi thường gặp:** tin chân dài đã cắt hoặc đảo C2.

⚠ C2 ngược cực có thể nóng/rò/vỡ.

### 3.6.3. LED

- **Mục tiêu / linh kiện-lỗ:** D1 K19(A)/L19(K), R1→A→K→GND; [N] §2 dòng 33–35, [F] `PIN_LED_STATUS`.
- **Thao tác:** (1) Diode test nhận A/K khi rời. (2) Hàn đúng chiều. (3) Đánh dấu K sau cắt.
- **Kiểm tra:** không cầu bỏ qua R1; LED dùng GPIO32, không nhầm LED DevKit.
- **Lỗi thường gặp:** đảo LED, suy Vf thật từ ước tính netlist.

### 3.6.4. Header/socket

- **Mục tiêu / linh kiện-lỗ:** hai cái ESP32 1×20, IMU 1×10, test 1×4 theo §3.5.3; [B] STT 12–14.
- **Nguyên tắc:** chỉ hàn **chân của socket (header cái) vào board**. ESP32 và IMU **chỉ cắm vào socket, KHÔNG hàn chân module vào socket hay vào board**. Mặt hàn là mặt dưới của board; không đưa mỏ hàn lên chân hay mặt linh kiện của module.
- **Thao tác:** (1) Cắm module **không điện** vào socket để canh hai hàng chân thẳng hàng (module chỉ dùng làm gá, không hàn). (2) Hàn giữ đầu mỗi thanh socket. (3) Để nguội, rút module. (4) Hàn chân còn lại của socket. (5) Đánh dấu test.
- **Kiểm tra:** không căng/lệch hàng; lỗ thừa 38 không đi dây; pad thông đúng ổ, không chập bên cạnh.
- **Lỗi thường gặp:** thiếc vào ổ cái; đảo IMU; lỗ thừa về phía ăng-ten.

### 3.6.5. Ba nút

- **Mục tiêu / linh kiện-lỗ:** SW2/SW4/SW3 theo tâm §3.5; ghi bốn lỗ thật. [N] §2 dòng 27–32, [F] Buttons.
- **Thao tác:** (1) Đo hai nhóm chân thông sẵn A/B. (2) A↔B thả hở/nhấn thông. (3) Thử cap. (4) Hàn/gá riêng nếu lệch pitch. (5) A→GPIO, B→GND; chân dư không cần dây riêng.
- **Kiểm tra:** đo nhấn/thả tại đầu dây; cap không giữ nút.
- **Lỗi thường gặp:** hai chân cùng nhóm làm luôn nhấn; đoán nhóm theo hướng.

### 3.6.6. SW1

- **Mục tiêu / linh kiện-lỗ:** gá AA19…AG22; OUT+→tiếp điểm ON, COM→V_SYS; [N] §2 dòng 5/7/8.
- **Thao tác:** (1) Đo COM/cặp đóng. (2) Ghi ON/OFF. (3) Hàn dây, bọc riêng. (4) Bọc NC. (5) Gá thân chịu lực.
- **Kiểm tra:** OFF hở OUT+–V_SYS, ON thông; không ngắt riêng mass.
- **Lỗi thường gặp:** hai chân ngoài không COM; NC chạm pad khác.

### 3.6.7. J1

- **Mục tiêu / linh kiện-lỗ:** PH2.0 đực [B] STT 3 trên dây, gá mép trước/trái. Pitch 2.0 mm khác 2.54 mm, không ép perfboard.
- **Thao tác:** (1) Hàn khi không pin. (2) J1 +→B+, −→B-. (3) Co nhiệt từng chân. (4) Gá, chừa chỗ rút. (5) Đo bằng dây thử PH2.0 cái theo §3.13.3.
- **Kiểm tra:** đúng cực tới B+/B-, không B-→OUT- ngoài module; nhãn ngay mặt ghép.
- **Lỗi thường gặp:** đảo do góc nhìn, nhét dây trần thay terminal, mối hàn chịu kéo.

### 3.6.8. J5V, module nguồn và dây

- **Mục tiêu / linh kiện-lỗ:** đực AC34/AD34, cái trên dây VIN/GND. Dải đực 1×40 còn dư [B] STT 12 đủ lấy hai chân. Socket ESP32/IMU dùng hết nên **thêm một dải cái 1×10**, BOM STT 21; không cắt socket đang dùng.
- **Thao tác:** (1) Tách hai chân đực liền nhau đầu dải, hàn AC34→VOUT+ và AD34→GND. (2) Dải cái bổ sung giữ ổ 1–2, cưa/cắt qua ổ 3 hy sinh ổ đó; đeo kính, sửa nhựa sắc và kiểm tiếp điểm, không bẻ như dải đực. (3) Cái 1→dây đỏ→VIN, cái 2→đen→GND, co nhiệt riêng. (4) Dán **“5V — RÚT KHI CẮM USB”**, dấu + hai nửa, thêm gá/chặn hướng tránh đảo. (5) Đo nguội rồi ghép khi không điện. (6) Gá nguồn trên đệm cách điện, hàn/đo/tick từng dây.
- **Kiểm tra:** đây là **cặp dây nguồn**, không dùng jumper shunt chập hai chân. Rút cái phải ngắt VOUT+–VIN; kiểm cực, lực giữ và dòng định mức tiếp điểm. Chưa biết thì **CẦN XÁC NHẬN**, không suy từ pitch.
- **Lỗi thường gặp:** đảo 5V/GND, dùng shunt gây chập, lõi hở/râu đồng, keo che lỗi.

DB9: tín hiệu một lõi; nguồn chập 2–3 lõi cùng dài, hàn đủ hai đầu, giữ dưới khoảng 10–15 cm [P] §2. Cắt/bọc lưới và drain thừa. Không kéo qua vùng pin/ăng-ten. Đầu cái/pad không chứa được bó dây thì dùng mối chuyển tiếp ngắn có co nhiệt ngoài vùng pin, không nhồi gây chập; kiểm đường nguồn dưới tải thật.

## 3.7. Bảng nối dây đầy đủ

**Quy ước:** `G*` là điểm chia mass bằng dây có bọc, ngoài vùng pin, nối gốc OUT- ở board chính. Giai đoạn 1 lấy GND ESP32 làm gốc; giai đoạn 2 nối gốc đó tới OUT-. Không có mặt phẳng mass tự động trên perfboard. G* đề xuất tại P39; đo lắp khô trước. Đoạn cùng pad không cần dây riêng nhưng vẫn đo/tick.

Nguồn mỗi dòng: [N] §2, số dòng cột cuối; GPIO thêm [F]. Bỏ J2/TP8–11 theo [P]. Màu **đề xuất**, thiếu màu thì dán nhãn: đỏ dương, đen mass; âm pin đen nhãn **CELL−/B−**, không trộn GND.

`P` = bó 2–3 lõi nguồn; `S` = một lõi; `pad` = nối bằng chân/điểm hàn chung. Chiều dài là **ước lượng cắt thử**, đơn vị cm. Đường nguồn P giữ dưới khoảng 10–15 cm [P] §2; tín hiệu phải vòng ngoài vùng pin nên có thể dài hơn. Đo đường đi thật, không nối căng. GND tới nút/LED chỉ mang dòng tín hiệu có thể dùng một lõi; đường hồi nguồn chính phải dùng P.

| STT | Net | Từ | Đến | Loại | Màu gợi ý | Dài ước lượng | Đã nối | Đã đo thông | Nguồn [N] §2 |
|---|---|---|---|---|---|---|---|---|---|
| 01 | VBAT | BAT1 dây + đã đo | J1 cực + qua đầu ghép | Dây pin sẵn/P phần nối dài | Đỏ | 3–6 | □ | □ | 1; [P] §2 |
| 02 | GND_BAT_CELL | BAT1 dây − đã đo | J1 cực − qua đầu ghép | Dây pin sẵn/P phần nối dài | Đen, nhãn CELL− | 3–6 | □ | □ | 2; [P] §2 |
| 03 | VBAT | J1 + | MOD1 B+ | P | Đỏ | 3–6 | □ | □ | 3 |
| 04 | GND_BAT_CELL | J1 − | MOD1 B- | P | Đen, nhãn B− | 3–6 | □ | □ | 4 |
| 05 | V_SW_IN | MOD1 OUT+ | SW1 tiếp điểm ON | P | Đỏ, nhãn OUT+ | 3–6 | □ | □ | 5 |
| 06 | GND | MOD1 OUT- | G* | P | Đen | 8–13 | □ | □ | 6 |
| 07 | V_SYS | SW1 COM | MOD2 VIN+ | P | Đỏ, nhãn SYS | 6–10 | □ | □ | 7 |
| 08 | V_SYS | SW1 COM | R2.1 | S | Đỏ, nhãn đo SYS | 4–8 | □ | □ | 8 |
| 09 | GND | G* | MOD2 VIN- | P | Đen | 9–14 | □ | □ | 9 |
| 10 | GND | G* | MOD2 VOUT- | P | Đen | 9–14 | □ | □ | 10 |
| 11 | 5V | MOD2 VOUT+ → J5V.1 đực AC34 | J5V.1 cái → U1 VIN/5V | P, qua cặp tiếp điểm | Đỏ, nhãn 5V | Tổng 7–12 | □ | □ | 11; [P2] §2.2 |
| 12 | 5V | Phía nguồn J5V.1, cùng VOUT+ | C2 + tại AE35 | P/pad | Đỏ | 1–3 | □ | □ | 12 |
| 13 | GND | C2 − | G* | P | Đen | 3–8 | □ | □ | 13 |
| 14 | 3V3 | U1 3V3 | U2 VCC (1) | P | Đỏ, nhãn 3V3 | 3–7 | □ | □ | 14; [F] I2C |
| 15 | 3V3 | U2 VCC cùng net U1 3V3 | U2 NCS (5) | S | Đỏ, nhãn NCS | 1–3 | □ | □ | 15 |
| 16 | 3V3 | U1 3V3 | TP3 | S | Đỏ, nhãn TP3 | 3–8 | □ | □ | 17 |
| 17 | IMU_SDA | U1 GPIO21 | U2 SDA (4) | S | Xanh lá | 7–12 | □ | □ | 18; [F] PIN_I2C_SDA |
| 18 | IMU_SDA | U2 SDA cùng net GPIO21 | TP2 | S | Xanh lá | 2–5 | □ | □ | 20 |
| 19 | IMU_SCL | U1 GPIO22 | U2 SCL (3) | S | Vàng | 7–12 | □ | □ | 21; [F] PIN_I2C_SCL |
| 20 | IMU_SCL | U2 SCL cùng net GPIO22 | TP1 | S | Vàng | 2–5 | □ | □ | 23 |
| 21 | GND | U2 GND (2) | G* | P | Đen | 4–8 | □ | □ | 24 |
| 22 | GND | U2 AD0 (6) | U2 GND cùng net G* | S | Đen, nhãn AD0 | 1–3 | □ | □ | 25 |
| 23 | GND | U2 FSY (8) | U2 GND cùng net G* | S | Đen, nhãn FSY | 1–3 | □ | □ | 26 |
| 24 | BTN_LEFT | U1 GPIO25 | SW2 nhóm A | S | Xanh dương | 17–22 | □ | □ | 27; [F] PIN_BTN_LEFT |
| 25 | GND | SW2 nhóm B | G* | S | Đen | 16–21 | □ | □ | 28 |
| 26 | BTN_RIGHT | U1 GPIO26 | SW3 nhóm A | S | Trắng | 13–18 | □ | □ | 29; [F] PIN_BTN_RIGHT |
| 27 | GND | SW3 nhóm B | G* | S | Đen | 11–16 | □ | □ | 30 |
| 28 | BTN_MODE | U1 GPIO27 | SW4 nhóm A | S | Tím | 15–20 | □ | □ | 31; [F] PIN_BTN_MODE |
| 29 | GND | SW4 nhóm B | G* | S | Đen | 14–19 | □ | □ | 32 |
| 30 | LED_STATUS | U1 GPIO32 | R1.1 (1 kΩ) | S | Cam | 15–20 | □ | □ | 33; [F] PIN_LED_STATUS |
| 31 | LED_ANODE | R1.2 | D1 anode A | S | Cam, nhãn A | 1–3 | □ | □ | 34 |
| 32 | GND | D1 cathode K | G* | S | Đen | 13–18 | □ | □ | 35 |
| 33 | BAT_SENSE | R2.2/R3.1 tại AA29 | U1 GPIO34 | S | Xám | 3–7 | □ | □ | 36; [F] PIN_BAT_SENSE |
| 34 | BAT_SENSE | R2.2 | R3.1 | pad | Nhãn SENSE | 0 | □ | □ | 37 |
| 35 | BAT_SENSE | R2.2/R3.1 | C1.1 | S | Xám | 1–2 | □ | □ | 38 |
| 36 | GND | R3.2 | G* | S | Đen | 2–6 | □ | □ | 39 |
| 37 | GND | C1.2 | G* | S | Đen | 2–6 | □ | □ | 40 |
| 38 | GND | U1 GND nhãn thật, tương ứng N chân 14 | G* | P | Đen | 3–8 | □ | □ | 41 |
| 39 | GND | U1 GND nhãn thật, tương ứng N chân 32 | G* | P | Đen | 3–8 | □ | □ | 42 |
| 40 | GND | U1 GND nhãn thật, tương ứng N chân 38 | G* | P | Đen | 3–8 | □ | □ | 43 |
| 41 | GND | TP4 | G* | S | Đen | 4–8 | □ | □ | 45 |
| 42 | GND | G* | J5V.2 đực AD34 | P | Đen | 2–5 | □ | □ | §3.1; [P2] §2.2 |
| 43 | GND | J5V.2 cái | U1 GND theo nhãn thật | P | Đen | 2–5 | □ | □ | §3.1; [P2] §2.2 |

Giai đoạn 1 nối dòng 14–32 và 38–41, lấy G* từ GND ESP32. Giai đoạn 2 thêm 01–13, 33–37, 42–43; chưa có pin thì dùng nguồn thay pin tại J1 theo §3.13.2 thay nhánh 01–02. USB ESP32 luôn yêu cầu rút cả đầu cái J5V.

Dòng 01–02 mô tả đường điện của pack đã có giắc, không yêu cầu hàn thêm dây pin.

Thứ tự IMU theo [N] §2/§4.2: **1 VCC; 2 GND; 3 SCL; 4 SDA; 5 NCS; 6 AD0; 7 INT; 8 FSY; 9 ACL; 10 ADA**. INT/ACL/ADA để hở, không cần dây; không nối chúng vào SCL/SDA. NCS không phải chân nguồn để cấp riêng cho IC trần.

⚠ Số thứ tự ESP32 trong [N] là quy ước bảng; chưa xác nhận giống cách đếm của bo thật. Đấu theo **chữ in trên bo** và GPIO trong [F], không chỉ đếm “chân 33”. GPIO34 chỉ nối BAT_SENSE giữa R2/R3, không nối 5V hoặc VBAT/V_SYS trực tiếp; sai có thể phá ADC.

## 3.8. Kiểm tra điện sau từng giai đoạn

### 3.8.1. Đo nguội: rút toàn bộ nguồn

Thực hiện sau từng cụm hàn, sau giai đoạn 1, sau giai đoạn 2, sau mọi sửa lỗi. Rút pin, nguồn thay pin và cả hai USB, chờ/đo xác nhận tụ xả; ưu tiên rút ESP32/IMU khỏi socket khi kiểm tra dây. Chập hai que để biết điện trở dây đo và tiếng beep chuẩn. Không đặt một ngưỡng ohm tùy ý cho mọi module.

| Cặp điểm | Kết quả cần có | Cách đọc/nguồn | Đạt |
|---|---|---|---|
| Hai đầu **từng dòng** §3.7 | Thông trực tiếp gần giá trị chập hai que | Không đo xuyên R1/R2/R3 rồi đòi beep; [N] §2 | □ |
| OUT-–G*, G*–VIN-/VOUT-/U1 GND/U2 GND/TP4 | Thông | Chỉ giai đoạn 2 có OUT-; [N] §3.1 | □ |
| 3V3–U2 VCC/NCS/TP3 | Thông | [N] §3.6, bỏ J2 | □ |
| GPIO21–SDA/TP2; GPIO22–SCL/TP1 | Thông đúng net, không đổi chéo | [N] §§3.8–3.9 | □ |
| SW1 OUT+–COM | OFF hở, ON thông | Đo công tắc tách khỏi nhánh khác nếu có đường vòng; [N] §§3.3–3.4 | □ |
| Hai nhóm SW2/3/4 | Thả hở, nhấn thông | [N] §§3.10–3.12; đo khi không có đường vòng module | □ |
| 5V–GND | Không chập trực tiếp | Tụ có thể làm beep thoáng; đo ổn định, đổi chiều, tách tải nếu nghi ngờ | □ |
| 3V3–GND | Không chập trực tiếp | Tách ESP32/IMU để phân biệt cầu thiếc với linh kiện trên module | □ |
| VBAT–GND | Không có cầu dây/thiếc chập | Pin phải tháo; module bảo vệ có thể ảnh hưởng số ohm | □ |
| VBAT–GND_BAT_CELL (B+–B-) | Không chập | Không đo ohm trên pin đang có điện | □ |
| 5V–3V3 | Không có nối tắt bằng dây/thiếc | Đo tách DevKit; LDO/diode trên bo có thể tạo đường dẫn một chiều | □ |
| GND_BAT_CELL–GND | **Không có dây/cầu thiếc nối ngoài module** | MOSFET bảo vệ đang dẫn có thể khiến đo như thông; beep không chứng minh đã đấu sai hoặc bảo vệ hoạt động | □ |
| BAT_SENSE–V_SYS / BAT_SENSE–GND | Qua R2 / R3, không thông trực tiếp | Khoảng 100 kΩ khi đo riêng nhánh đã cô lập; C1 có quá độ [B]/[N] | □ |
| INT/ACL/ADA, SW1 chân NC, lỗ socket thừa | Không có dây sang net khác | Kiểm tra bằng mắt và đo trên carrier khi module đã rút | □ |

⚠ Không cố kiểm tra bảo vệ bằng cách chập pin hoặc xả cạn. Đo ohm/beep qua MOSFET hay LDO không đủ để xác nhận mạch bảo vệ/cách ly nguồn.

### 3.8.2. Bảng điện áp

Đo DC. Trừ hàng điện áp pack, que đen vào **GND = OUT-** ở giai đoạn 2 hoặc GND ESP32 ở giai đoạn 1. Khoảng 3.0–4.2V là dải thiết kế của [N], không phải cam kết ngưỡng cắt của pack/DW01 cụ thể. Sai số dụng cụ phải cộng vào đánh giá.

| Điểm đo | Điều kiện | Mục tiêu/khoảng đối chiếu | Nguồn và giới hạn | Ghi đo |
|---|---|---|---|---|
| B+ so B- | Pack nối đúng, chưa sạc | Danh định 3.7V; dải thiết kế 3.0–4.2V | [P2] §2.1, [N] §1; pin thật còn đối chiếu quy cách | ____ |
| OUT+ so OUT- | Bảo vệ cho phép xuất điện | Gần điện áp pack; chênh lệch do bảo vệ/dây | [N] §§1, 4.4; dung sai chênh áp **CẦN ĐO THỰC TẾ** | ____ |
| V_SYS so GND | SW1 ON, chạy pin | 3.0–4.2V theo thiết kế, có sụt áp tải | [N] §1 net V_SYS | ____ |
| V_SYS so GND | OFF, không USB/nguồn ngoài | Gần 0V sau khi tụ xả | Suy luận từ [N] §2 dòng 7–8; đo dư do tụ/đường hồi không dùng để kết luận ngay | ____ |
| VOUT+ so VOUT- | Boost rời, rồi có tải | Mục tiêu 5.0V, 4.9–5.1V | [A] §5.1; chỉnh ở điều kiện dùng thật | ____ |
| VIN ESP32 so GND | Chạy từ boost, USB rút | 4.9–5.1V tại chân bo | [N] §1 net 5V; so với VOUT để phát hiện sụt dây | ____ |
| 3V3/TP3, U2 VCC | Chỉ một nguồn cho ESP32 | Mục tiêu 3.3V, khoảng thiết kế 3.25–3.35V | [N] §1 net 3V3; đây là tiêu chí dự án, không khẳng định mọi LDO đều có dung sai đó | ____ |
| BAT_SENSE, GPIO34 | V_SYS đang có nguồn | Khoảng 0.5×V_SYS; 1.5–2.1V danh định theo dải thiết kế | [N] §§1/3.7; R2/R3 1% [B] cho tỷ số 0.495–0.505 (tính toán), cộng sai số đo | ____ |
| SCL/SDA, TP1/TP2 | Bus nghỉ, có pull-up của đúng module | Gần 3V3 khi nghỉ; lúc truyền đồng hồ có thể chỉ số trung bình | [N] §§1/4.5; không đặt dung sai DC cho dữ liệu đang chạy | ____ |
| GPIO25/26/27 | Firmware bật INPUT_PULLUP | Thả gần 3V3, nhấn gần GND | [F], [FW] `setup()`; không chập trực tiếp chân 3V3 để thử nút | ____ |
| GPIO32→R1; D1 A/K | LED được firmware bật | GPIO cao gần 3V3; Vf của LED thật **CẦN ĐO THỰC TẾ** | [N] §2 dòng 33–35; giá trị Vf ước tính trong N không thay datasheet LED | ____ |
| B+ so B-, cuối sạc | Khi có pin thật, theo nhánh §3.9.2 | Danh định 4.2V; đối chiếu giới hạn pack và bảng VFLOAT của [T] | [T] trang 5; không dùng giá trị tối đa của charger làm giới hạn an toàn pin | ____ |

### 3.8.3. Trình tự bật nguồn an toàn

1. **Logic:** rút J5V, nguồn tại J1 và USB TP4056; đo nguội, cấp USB ESP32. Kiểm 3V3/probe 0x68/nút/LED bằng chương trình thử sẵn §3.4.2, không phát triển firmware mới. **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
2. **Thêm nguồn:** rút USB/module, hàn giai đoạn 2 rồi đo nguội toàn bộ. Thử không tải với J5V rút, nguồn thay pin §3.13.2; không USB TP4056.
3. **Boost:** chỉnh 5.0V (4.9–5.1V) tại VOUT; tắt nguồn rồi cắm J5V đúng để thử tải. Đo VIN/3V3/BAT_SENSE, không chỉ đo không tải.
4. **Cơ khí:** rút nguồn, gá xong đo lại; đủ checklist §3.13.1 mới gọi sẵn sàng.
5. **Pin thật:** theo §3.13.4; thử sạc riêng sau chạy pin, SW1 OFF, J5V rút, không USB ESP32. Chưa có pin thì sạc ghi CHƯA THỬ.

Giới hạn ≤500 mA là trần thử [P2] §3.13.2, không bảo đảm mọi tải ESP32 đủ dòng. Nếu giới hạn gây sụt áp/reset, không tăng tùy tiện; ghi phép thử tải chưa đạt và kiểm nguyên nhân. Ampe kế mắc nối tiếp khi nguồn tắt, đúng cổng/thang có cầu chì. Dòng phía pin khác phía 5V; đồng hồ thường không bắt xung BLE/gợn áp, có thể cần máy hiện sóng.

## 3.9. Rủi ro cần phân tích riêng

### 3.9.1. USB và boost cùng cấp 5V

**Khi chạy pin thì cắm đầu nối 5V; khi cắm USB vào ESP32 thì RÚT đầu nối 5V. Không bao giờ cắm USB ESP32 lúc J5V còn cắm.** J5V tại AC34/AD34, nhãn “5V — RÚT KHI CẮM USB”; SW1 OFF trước cắm/rút.

DevKitC V4 chính hãng có D3 BAT760-7 [E2], nhưng chưa biết bo thật dùng đúng sơ đồ; [E1] vẫn yêu cầu một nguồn. SW1 OFF chỉ ngắt đầu vào boost, chưa chứng minh đầu ra không nhận ngược USB. Tháo J5V là biện pháp mặc định. Không tự thêm một diode rồi kết luận mọi đường hồi đã cách ly.

⚠ USB ESP32 khi J5V còn ghép có thể đẩy dòng ngược về máy tính/boost. Đảo đầu cái hoặc dùng shunt chập hai chân J5V có thể gây ngắn mạch.

### 3.9.2. Dòng sạc khoảng 1 A và lựa chọn pin

Giữ TP4056 nguyên trạng, không sửa RPROG [P2] §1. Quy tắc chung [L] là dòng sạc ≤1C; `C-rate=I_sạc(mA)/dung_lượng(mAh)`:

| Dung lượng | Với 1 A, tính toán | Nhánh lựa chọn |
|---|---|---|
| ≥1000 mAh | ≤1C | Ưu tiên để dùng module nguyên trạng; vẫn kiểm đúng pin 1S sạc cuối 4.2V, PCM, dòng thật/nhiệt |
| <1000 mAh | >1C; 400 mAh→2.5C | Nhánh **chấp nhận rủi ro đã biết**, không gọi an toàn chỉ vì có giám sát |

**Không thể kết luận “≥1000 mAh thì không có vấn đề” chỉ từ dung lượng.** 1C là chọn sơ bộ, không thay định mức pack; dòng module có sai lệch [T]. Nếu biết pack không cho phép dòng đó, nên đổi pin/sạc phù hợp. Thông tin chưa có ghi **CẦN XÁC NHẬN**, không bịa giới hạn.

Nhánh pin nhỏ nếu bạn vẫn chọn thử:

1. Chấp nhận nguy cơ giảm tuổi thọ, nóng/phồng hoặc cháy do quá dòng nạp; PCM/DW01 không đặt dòng sạc phù hợp cho cell.
2. Để pin ngoài vỏ kín, trên bề mặt khó cháy, thoáng và xa module nóng; SW1 OFF, J5V rút, chỉ USB TP4056.
3. Ưu tiên nhiệt kế; theo dõi sát **5–10 phút đầu** (mốc đề xuất [P2] §2.1), rồi tiếp tục có người giám sát đến kết thúc; hết khoảng đầu không có nghĩa hết rủi ro.
4. Không có nhiệt kế: chỉ chạm nhẹ vỏ pin nguyên, không pad/IC. Tay không đo được °C hay mọi hư hỏng bên trong; không nhấc/cầm pin đang nóng/phồng/bốc khói.
5. Không sạc qua đêm, khi vắng người hoặc trong vỏ ép kín. Ngắt USB sạc ngay nếu nóng bất thường, phồng, có mùi, áp tăng bất thường hoặc dòng vượt giới hạn đã biết; xử lý §3.2.
6. Đo dòng pin/áp cuối theo §3.4.4; không lấy nhiệt độ chip làm giới hạn cell. TEMP có thể không đo nhiệt pin trên module hai dây [T].

Mua pin: **Li-ion/LiPo 1S 3.7V, sạc cuối 4.2V, có PCM, giắc cái JST-PH 2.0 hai chân, ưu tiên ≥1000 mAh**, cả pack/PCM/tab/dây lọt §3.5.3 và không ép vỏ. Không dùng pin khác hóa học/nhiều cell chỉ vì giắc vừa. Giám sát giúp nhận dấu hiệu, không làm dòng quá định mức trở thành phù hợp.

### 3.9.3. Pin yếu, sụt áp và thời lượng

Ước lượng `I_pin ≈ 5V×I_5V/(V_pin×hiệu_suất_boost)+dòng_tĩnh`. Pin yếu tăng dòng phía pin với cùng tải; dây/giắc/hai tầng bảo vệ có thể sụt áp/reset. Đo VIN/3V3 có tải, không coi boost “2A” là bảo đảm.

Pin chưa xác định nên **chưa ước lượng số giờ chạy**. Khi có pin, `thời_gian ≈ dung_lượng_Ah×điện_áp_danh_định×tỷ_lệ_năng_lượng_dùng_được×hiệu_suất/(5V×I_5V_trung_bình)`; tỷ lệ/dòng phải đo hoặc ghi giả định. Firmware chưa đọc ADC [FW]/[W] §6, chưa tự báo pin yếu. Không xả kiệt để thử bảo vệ/thời lượng.

### 3.9.4. Ăng-ten và IMU

- **Ăng-ten:** pad đồng cũng là kim loại. Cả vùng ăng-ten ngoài mép, khoảng hở 15 mm [E3], tránh dây/pin/vít/vỏ dẫn; thử sau đóng vỏ.
- **IMU:** gá chắc/đỡ board gần nút; cách nút >30 mm, cuộn cảm >36 mm [P2]/[M] §3.2. Tách dây nguồn khỏi I2C/BAT_SENSE; so sánh từng nguồn riêng nếu rung/reset.
- **Direct 3.3V:** [H] xác nhận chức năng ngắn hạn trên bộ sở hữu, không mọi breakout/tuổi thọ. Thay module cần xác minh lại.

## 3.10. Xử lý sự cố

| Triệu chứng | Nguyên nhân có thể | Cách kiểm tra | Cách khắc phục |
|---|---|---|---|
| Không lên nguồn | SW1 dùng sai COM, giắc đảo, bảo vệ ngắt, dây hở | Rút tải; đo lần lượt pin B+–B-, OUT+–OUT-, V_SYS, boost; không bypass B- | Sửa đúng dây sau cắt nguồn; pack 0V/chưa rõ bảo vệ thì dừng xác minh |
| ESP32 reset liên tục | 5V sụt, dây hồi nhỏ, giới hạn nguồn thấp, chập, nguồn tranh nhau | Thử riêng USB khi boost đã tháo; đo tại VIN/3V3 có tải, đọc log reset | Sửa đường nguồn/mối hàn, kiểm tra tải trước tăng giới hạn; C2 không thay nguồn đủ dòng |
| Không thấy IMU | SDA/SCL nhầm, socket lệch, NCS/AD0 sai, thiếu 3V3, lỏng dây | Probe theo §3.4; đọc chữ chân, đo bus nghỉ; 0x69 gợi ý AD0 sai | Tắt nguồn rồi sửa; không nhầm ACL/ADA; không tự cấp 5V để thử |
| WHO_AM_I sai dù có ACK | Nhầm thiết bị, bank sai, lỗi bus hoặc module khác | Probe chọn bank 0, kỳ vọng 0xEA [PR] | Kiểm tra module và dây; ACK một mình chưa đủ nhận dạng |
| Nút không ăn/luôn nhấn | Hai chân cùng nhóm, cap kẹt, hở mass, chưa BLE | Đo nguội nhấn/thả; đo GPIO đang INPUT_PULLUP; xem Clutch trong log | Chuyển sang hai nhóm đúng; sửa cap; click trái/phải cần kiểm tra bằng chương trình thử hoặc mức GPIO | **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
| LED không sáng | Ngược cực, R1 sai, GPIO sai, firmware dừng trước vòng lặp | Diode test khi ngắt nguồn; kiểm R1/GPIO32; đọc FATAL | Sửa chiều/dây; không bỏ điện trở để thử sáng |
| Sạc không vào | Cáp/nguồn không đúng, mạch bảo vệ, pin đầy, module sai | Kiểm tra đầu vào TP, cực pack, đo dòng đúng phía pin; đọc giới hạn pack | Không nối tắt bảo vệ hoặc ép dòng; xác minh module/pack; giữ SW1 OFF |
| MT3608 nóng | Chập đầu ra, tải quá sức, sai điện áp, dây kém, module lỗi | Tắt ngay, tháo tải, kiểm nguội; thử nguồn giới hạn dòng | Sửa nguyên nhân trước chạy tiếp; không vặn biến trở để chữa mọi lỗi |
| ADC đọc sai/không có số ADC | Firmware chưa đọc, nối sai điểm, tỷ số trở/hiệu chuẩn/nhiễu | Đồng hồ đo V_SYS và BAT_SENSE; kiểm R2/R3/C1; xem [FW] | Phần cứng phải đạt khoảng 1/2 V_SYS; bổ sung ADC/hiệu chuẩn là tác vụ riêng, không sửa firmware ở đây |
| Trỏ rung khi bấm/chạy pin | Board võng, IMU lỏng, nhiễu boost | So sánh trạng thái tĩnh, bấm nút và đổi nguồn đúng quy trình | Gá chắc, tách dây/vị trí nguồn; đo trước khi chỉnh bộ lọc |
| Nạp thất bại | Sai COM, monitor chiếm cổng, cáp chỉ sạc, chưa vào download | Đối chiếu `device list`, thoát monitor; xem hướng dẫn bo thật | Chọn đúng cổng/cáp; BOOT/EN theo bo; không erase flash như bước sửa mặc định |

## 3.11. Lắp cơ khí cuối cùng

1. Rút pin/hai USB/nguồn thay pin; nhặt đầu chân/râu đồng và soi lại mối.
2. Kiểm hình chiếu B21…Z37 trống ở cả hai mặt: không chân, dây, vít, pad hàn nổi. Kapton/xốp không hợp thức hóa chân nhọn.
3. Làm sạch flux theo chỉ dẫn, để khô; không dùng dung môi chưa biết tương thích.
4. Lót Kapton, mút EVA/PE 1–2 mm [P]/[M] §4, băng hai mặt phù hợp; chừa dây/PCM và độ cao vỏ. Pin chưa có thì chỉ chuẩn bị lớp lót.
5. Khi có pin, dán không ép túi/tab/PCB; không xiết dây rút hoặc đổ keo nóng lên pin. Không lọt thì đổi pack hoặc xếp lại, không thu vùng cấm.
6. Gá TP4056/boost/J1 trên đệm phi kim, đỡ lực cắm cáp; keo nến chỉ phụ trợ ở mép nguội, không bít chip/cuộn cảm/biến trở/cổng.
7. Giữ dây ngoài vùng pin/ăng-ten, bọc pad nguồn; chừa độ chùng để rút module/J5V.
8. Thử cap: hơi lỏng có thể đệm một lớp băng mỏng tháo được; không cùng trụ hoặc kẹt thì đổi cap/để nút trần. Không nhỏ keo vào khe nút.
9. Lắp vỏ khô, thử cáp/SW1/BOOT/EN; không để vỏ giữ nút hoặc đè pin.
10. Đo lại §3.8/§3.13 bằng từng nguồn riêng; người lắp tick đã đo, pin thật/sạc chưa có thì ghi chưa thử.

## 3.12. Phụ lục

### 3.12.1. Checklist in ra giấy

- [ ] Đã ghi lỗ thật, board pad rời; lắp khô không va chạm, ESP32 U/AE hoặc U/AD, IMU C42…L42.
- [ ] Hàn/soi/đo từng cụm theo §3.6; vùng B21…Z37 trống cả hai mặt.
- [ ] Từng dòng §3.7 và cặp đo nguội §3.8 đã kiểm.
- [ ] B-/OUT- không nối ngoài module; GPIO34 chỉ BAT_SENSE; NC hở.
- [ ] Thử bằng chương trình có sẵn hoặc ghi CHƯA THỬ; không phát triển firmware ở đây.
- [ ] Hoàn tất §3.13.1 và ghi giới hạn phép thử nguồn thay pin.
- [ ] Sạc/pin thật để CHƯA THỬ đến ngày có pin, không tick từ tài liệu.

Ngày ____; người kiểm ____; nguồn thử ____; mục thiếu ____.

### 3.12.2. Giá trị linh kiện và cách nhận biết

Giá trị mua hàng lấy từ [B] STT 7–11; kết nối từ [N] §2. Mã vạch/mã in dưới đây là quy ước đọc linh kiện, phải đo đối chiếu, không khẳng định lô hàng sẽ có đúng kiểu vạch này.

| Linh kiện | Giá trị | Mã thường gặp/cách nhận biết | Kiểm tra |
|---|---|---|---|
| R1 | 1 kΩ, 1/4W, 1% | 5 vạch: nâu–đen–đen–nâu–nâu; nếu 4 vạch 1%: nâu–đen–đỏ–nâu | Đo rời; dải danh định 990–1010 Ω từ 1%, cộng sai số đồng hồ |
| R2/R3 | 100 kΩ, 1/4W, 1% | 5 vạch: nâu–đen–đen–cam–nâu; nếu 4 vạch 1%: nâu–đen–vàng–nâu | Mỗi con 99–101 kΩ theo 1%, cộng sai số đo |
| C1 | 100 nF/50V | Mã 104 = 100000 pF = 100 nF; không phân cực | 104 không cho biết định mức 50V; đọc nhãn/túi mua hàng |
| C2 | 10 µF/50V | In 10µF, 50V; vạch dọc thường chỉ cực − | Xác nhận dấu âm, đo/soi lại khi chân đã cắt; không có mã màu điện trở |
| D1 | LED xanh 3 mm | A/K xác nhận bằng diode test; cạnh vát/chân chỉ là dấu hỗ trợ | Không nối trực tiếp GPIO bỏ qua R1 |

### 3.12.3. Thuật ngữ

| Từ | Nghĩa trong hướng dẫn |
|---|---|
| Perfboard pad rời | Board lỗ có từng vòng đồng độc lập; phải nối dây để tạo net |
| Net | Nhóm điểm nối điện chung, ví dụ 3V3; gần nhau trên board không có nghĩa đã cùng net |
| Socket/header | Ổ cái/chân đực giúp cắm rút module |
| Flux | Chất trợ hàn điện tử giúp bề mặt ướt thiếc |
| THT | Chân xuyên qua board; phần nhô có thể đâm thủng pin |
| Keepout | Vùng cấm đặt vật đã chỉ rõ; vùng pin cấm chân hàn/vít/dây, vùng ăng-ten cấm vật cản dẫn điện |
| Active-low/pull-up | Nhả được kéo lên, nhấn nối GND và đọc mức thấp |
| ADC/BAT_SENSE | Bộ đổi điện áp sang số/điểm giữa cầu phân áp; chưa có phép đọc trong firmware hiện tại |
| CC/CV | Sạc dòng không đổi rồi điện áp không đổi; không lấy dung lượng chia dòng để kết luận thời gian sạc chính xác |
| C-rate | Dòng quy đổi theo dung lượng: pin 400 mAh có 1C = 400 mA (tính toán); giới hạn thực theo nhà sản xuất |
| NC | Không nối; không tùy tiện nối xuống mass |
| Clutch | Giữ nút để khóa dịch chuyển con trỏ khi đổi tư thế tay; không phải ngắt nguồn |

### 3.12.4. Căn cứ và giới hạn xác minh

Logic giữ [N] §2/[F]; J5V chỉ thêm điểm ngắt. Hình học tính theo pitch, chưa đo linh kiện. [H] là bằng chứng lịch sử, không phải board mới. Chưa build/nạp/đo điện/nhiệt lần sửa này. Thử nguồn thay pin không chứng minh đã thử sạc, pin thật hay thời lượng.

### 3.12.5. Câu hỏi mở cần trả lời hoặc đo thực tế

1. Pin 1S PCM, dung lượng/dòng, cả pack/độ cao nào lọt vùng? Giắc cái PH2.0 có đúng cực J1 không?
2. TP4056 đủ pad bảo vệ, dòng thực/nhiệt sạc ra sao?
3. Hãng/revision ESP32, khoảng hàng/thân nhô và nhãn chân thật là gì?
4. Điểm bắt đầu ăng-ten có ngoài mép với socket U/AE hoặc U/AD không?
5. Board đủ A…AG, 1…57, pitch/khoảng mép như giả định không?
6. Nguồn/nút/cap/IMU lọt khung không? Khoảng IMU–boost/nút thực bao nhiêu?
7. J1 đo cực/gá chắc chưa? J5V AC34/AD34 và ổ cái bổ sung đúng chiều, định mức, đã thử ngắt VOUT+–VIN chưa?
8. Có nguồn thay pin/dây thử PH2.0/đồng hồ không? Thiếu thì đã ghi phép chưa thử chưa?
9. Vỏ/cáp có ép pin, cản SW1/J1/J5V không?
10. Người lắp sẽ ghi dòng sạc/sụt áp/thời lượng pin thật ở đâu? Không điền trước khi đo.

## 3.13. Trạng thái sẵn sàng để cắm pin

### 3.13.1. Định nghĩa sẵn sàng

Chỉ người lắp tick sau khi đo. “Sẵn sàng phần cứng” nghĩa là các phép dưới đây đạt trên **board chính với nguồn thay pin**, vẫn còn xác nhận pin thật/sạc ngày nhận pin. Không đồng nghĩa đã hoàn thành firmware hoặc pin bất kỳ cắm vào đều phù hợp.

- [ ] Board hàn xong đủ §3.7, mọi mối hàn đã soi; không râu đồng/pad bong/cầu thiếc.
- [ ] Không chập các cặp §3.8; B- không nối ngoài module sang OUT-.
- [ ] ESP32 nạp được chương trình thử có sẵn bằng USB, J5V đã rút khi nạp. **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
- [ ] IMU ACK 0x68, WHO_AM_I 0xEA [F]/[PR]; ghi log/ngày thử ____. **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
- [ ] Ba nút nhấn/thả đúng, LED GPIO32 bật/tắt đúng bằng chương trình thử; không coi đo thông dây là đã thử phần mềm. **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
- [ ] MT3608 chỉnh 5.0V, đo 4.9–5.1V không tải và tại VIN khi có tải [A] §5.1, [N] §1.
- [ ] Đã thử đường J1→TP4056 OUT→SW1→boost→J5V→ESP32 bằng nguồn thay pin, không chỉ cấp riêng vào boost; ghi V_J1 ____; giới hạn/dòng ____.
- [ ] Đo 3V3 trong 3.25–3.35V và BAT_SENSE khoảng 0.5×V_SYS [N] §1; ghi VIN ____; 3V3 ____; V_SYS ____; SENSE ____.
- [ ] J1 hàn dây B+/B-, nhãn cực ở mặt ghép, cố định ngoài vùng pin; dây thử cái đã đo đúng cực.
- [ ] J5V AC34/AD34 đúng cực/lực giữ; đã đo rút ra ngắt VOUT+–VIN trên carrier khi tháo module/nguồn; không có dây khác nối tắt điểm ngắt.
- [ ] Pin chưa nối, cả hai USB/nguồn thay pin đã rút, **SW1 OFF, J5V cắm đúng chiều** để cất chờ pin.
- [ ] Vùng B21…Z37 trống chân/dây/vít, đã lót Kapton + mút 1–2 mm [P]/[M]; mép vỏ/cáp không ép vào vùng pin.

**Kết quả người lắp ghi:** đủ tất cả ô → “Sẵn sàng chờ pin đúng quy cách”. Thiếu phép nguồn thay pin/chức năng → “Hàn xong, còn kiểm tra ____”; không ghi “chỉ còn cắm pin”. Kiểm thử sạc/pin thật/thời lượng luôn còn chờ, không giả tick.

### 3.13.2. Kiểm tra đường nguồn KHÔNG có pin

Thứ tự ưu tiên theo [P2] §3.13.2; mức 3.7–4.2V và trần 500 mA là điều kiện phép thử do yêu cầu V2 đặt ra, không phải định mức cho mọi pack.

| Lựa chọn | Điều kiện | Kiểm được / giới hạn |
|---|---|---|
| 1. Nguồn bàn giới hạn dòng | Đầu ra DC 3.7–4.2V, giới hạn ≤500 mA (hoặc thấp hơn nếu thiết bị/dây yêu cầu), dây thử PH2.0 cái đúng cực | Thử đường cấp và tải trong mức dòng đó; không mô phỏng nội trở/PCM/dung lượng pin thật |
| 2. Mượn pin 1S có PCM | Chủ sở hữu cho phép tháo/rút, pack nguyên, biết quy cách, đo DC/cực trước; chỉ thử, không sạc | Pack có thể cấp quá 500 mA; **PCM không phải giới hạn dòng 500 mA**. Muốn giữ cùng điều kiện thử phải có bộ hạn dòng riêng phù hợp; không có thì chưa đạt kịch bản nguồn giới hạn dòng, nên mượn nguồn bàn |
| 3. Không có hai nguồn trên | Chỉ USB ESP32, J5V rút | Kiểm logic/3V3, soi/đo thông nguội; chưa kiểm đường nguồn qua J1/boost có tải, sạc, sụt áp pin và thời lượng |

Chỉ USB 5V thì **chưa thể chỉnh/xác nhận boost ở đầu vào giả pin**. Phương án hoàn tất an toàn là mượn bộ nguồn DC đã kiểm 3.7–4.2V có giới hạn ≤500 mA, hoặc nhờ nơi bán/phòng thí nghiệm chỉnh boost rời bằng nguồn phù hợp. Chỉnh boost rời chưa thay thử cả đường J1. Không lấy chân 3V3 ESP32 nuôi boost, không nối 5V USB thẳng vào J1/B+/B-.

⚠ Rút cả USB TP4056 và USB ESP32 trong mọi bước nguồn thay pin qua J1. TP4056 có thể nạp dòng ngược vào nguồn bàn nếu cắm USB sạc, làm hỏng nguồn; **không thử sạc nguồn thay thế**. Không bypass B-/OUT- hoặc chập pin để kích bảo vệ.

| Bước | Một việc chính | Đo ở đâu / giá trị mong đợi | Lỗi và điều kiện dừng |
|---|---|---|---|
| 1 | Chuẩn bị nguồn rời, đầu ra chưa nối J1 | Đồng hồ tại đầu giắc thử: đúng +/−, 3.7–4.2V; nguồn đặt giới hạn ≤500 mA | Sai cực/áp, dây trần hoặc không giới hạn được → chưa nối |
| 2 | Kiểm carrier không điện, J5V rút, SW1 OFF | Các cặp §3.8 không chập; COM–OUT+ hở | Chập, công tắc không ngắt hoặc chưa rõ cực → sửa nguội |
| 3 | Tắt nguồn, ghép giắc thử J1 rồi bật nguồn với SW1 OFF | B+–B- 3.7–4.2V; OUT+–OUT- gần bằng đầu vào; V_SYS gần 0V sau tụ xả | OUT bằng 0, nguồn giới hạn dòng ngay, nóng/mùi → tắt, kiểm sơ đồ/đặc tính khởi động bảo vệ; không nối tắt MOSFET |
| 4 | Bật SW1 khi J5V vẫn rút, tải ESP32 tách | V_SYS gần OUT; VOUT+–VOUT- chỉnh 5.0V, trong 4.9–5.1V [N]/[A] | Áp tăng mất kiểm soát, không chỉnh được, nóng/giới hạn dòng → OFF |
| 5 | Tắt nguồn, xác nhận tụ xả rồi cắm module/J5V đúng | Trước ghép: đo DC gần 0V tại đường 5V; kiểm dấu + AC34→VIN | Còn áp, sai chiều hay đầu cái lỏng → chưa bật |
| 6 | Bật nguồn và SW1 để thử tải | B+/B-, OUT+/OUT-, V_SYS, VIN 4.9–5.1V, 3V3 3.25–3.35V, SENSE≈0.5×V_SYS [N] §1 | Áp ngoài khoảng, reset, dòng kẹt giới hạn, nóng/mùi → OFF; ghi chưa đạt tải |
| 7 | Theo dõi vận hành thử trong 5 phút | Ghi điện áp đầu/cuối, dòng nguồn, nhiệt; mốc 5 phút là đề xuất [P2] §3.13.4 | Không có chương trình thử thì chỉ xác nhận nguồn với tải hiện có; không suy ra đã thử chức năng/nhiệt mọi chế độ | **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
| 8 | Tắt/rút nguồn thay pin để cất chờ | Không điện bên carrier; SW1 OFF, J5V cắm đúng, J1 để trống cách điện | Điện còn từ nguồn khác → tìm/rút nguồn, không đo ohm khi có điện |

Nếu bảo vệ không xuất OUT với nguồn thay pin, ghi “chưa kiểm được chuỗi qua bảo vệ”. Xem hướng dẫn đúng module hoặc đổi nguồn thử phù hợp; không cắm USB sạc vào nguồn bàn để tìm cách kích. Đo không tải đúng chỉ kiểm một phần; tải thật vượt trần 500 mA hoặc nguồn bị sụt cần đánh giá riêng, chưa thể ghi sẵn sàng đầy đủ.

### 3.13.3. Hoàn thiện J1 để cắm là chạy

J1 là PH2.0 đực hai chân [B] STT 3, **hàn dây ra**, không ép pitch 2.0 mm vào perfboard 2.54 mm. Cực + đã dán→B+; cực −→B- của TP4056 [N] §2 dòng 1–4. Bọc hai chân riêng, gá ngoài vùng pin, nhãn đỏ/+ ngay mặt cắm; không coi “pin 1” theo góc nhìn ảnh bán hàng là đã biết cực.

1. Với J1 chưa nối nguồn, đo thông cực +→B+, cực −→B-; kiểm không có dây B-→OUT- ngoài module.
2. Dùng dây thử JST-PH 2.0 **cái** được thêm STT 31 để kiểm/mô phỏng pin; đo đúng cực giắc thử trước ghép. Nguồn thử phải tắt lúc ghép/rút.
3. Yêu cầu pin mua về có giắc cái JST-PH 2.0 hai chân khớp cơ khí; pack nguyên PCM, đúng điện áp/dòng/kích thước §3.9.2/§3.5.3.
4. **Luôn đo cực ở chính đầu cắm của pin trước khi ghép lần đầu**, không tin màu dây. Dùng đầu dò đủ nhỏ/cách điện hoặc dây ghép thử đã kiểm; không đưa hai đầu kim loại trần kề nhau dễ chập. Que đỏ tại hốc sẽ ghép J1+, đen tại hốc còn lại phải hiện điện áp dương.
5. Nếu đầu khác loại: chưa cắm, không nhét chân trần; chọn pack đúng đầu hoặc dây chuyển đủ định mức được đo cực từ đầu tới cuối. Chưa có dây đúng thì chưa đạt mục tiêu “cắm là chạy”.
6. Nếu cùng đầu nhưng đảo cực: ưu tiên **đổi hai dây phía J1 của carrier khi đã tháo toàn bộ nguồn/pin**, co nhiệt và dán nhãn lại; đo thông tới B+/B-, thử nguồn thay pin và đo cực pin lại. Việc này an toàn hơn đụng terminal đang có điện của pin; không đảo ký hiệu B+/B- trên module.
7. Nếu buộc đổi terminal phía pin, nên nhờ người có dụng cụ làm: bọc một terminal, tháo/di chuyển từng dây, cách điện ngay, tuyệt đối không để hai terminal trần cùng lúc; không cắt đồng thời cả hai dây, không hàn vào cell. Đo lại ở mặt cắm sau sửa. Nếu không giữ được cách điện từng dây thì dùng adapter/đổi pack.

⚠ Giắc JST vừa không bảo đảm cùng cực giữa các hãng. Ghép đảo có thể phá module, làm nóng dây hoặc cháy pin.

### 3.13.4. Ngày pin về — tối đa 12 bước

Mỗi bước do người lắp đo; cả hai USB ban đầu đều rút. Dải 3.0–4.2V từ [N] §1 là dải kiểm thiết kế, không thay giới hạn pack thật.

1. **Đo pin khi tách khỏi mạch:** DC tại giắc pin, khoảng 3.0–4.2V. Ngoài dải, 0V hoặc pack hỏng/phồng → dừng; không kích/bypass bảo vệ.
2. **Xác nhận cực tại mặt giắc:** que đỏ ở hốc ghép J1+, đen hốc J1− phải hiện điện áp dương bằng bước 1. Đảo/không rõ/giắc sai → dừng, xử lý §3.13.3.
3. **Đặt trạng thái trước ghép:** SW1 OFF, J5V cắm đúng +/−; với mạch không điện, đo SW1 hở OUT+–COM và kiểm không chập 5V–GND như §3.8. Còn nguồn khác hoặc không ngắt được → dừng.
4. **Ghép pin:** sau ghép đo B+–B- bằng pin bước 1, đúng dấu; lệch rõ, nóng/mùi hoặc tia lửa bất thường → ngắt nếu an toàn và dừng.
5. **Đo OUT+–OUT-:** gần bằng B+–B- khi chưa tải; đo V_SYS gần 0V sau tụ xả. OUT=0, áp sai dấu, sụt bất thường → dừng kiểm bảo vệ, không bypass.
6. **Bật SW1:** đo V_SYS so OUT- gần OUT, trong dải thiết kế 3.0–4.2V; sụt/reset/nóng → OFF và dừng. Không thử xả thêm pin yếu để đạt phép này.
7. **Đo VIN ESP32:** 4.9–5.1V [A] §5.1/[N] §1; ngoài khoảng/dao động rõ → OFF, không chỉnh bừa khi tải đang có lỗi.
8. **Đo 3V3 tại ESP32/TP3 và IMU VCC:** 3.25–3.35V theo tiêu chí [N] §1; sai/chạm que nguy hiểm → OFF, kiểm lại.
9. **Đo BAT_SENSE tại GPIO34:** khoảng 0.5×V_SYS; tỷ số 0.495–0.505 từ R2/R3 1% [B], cộng sai số đo. Sai tỷ số/tiến gần điện áp pin thô → OFF, không tiếp tục để bảo vệ ADC.
10. **Quan sát khởi động và nhiệt:** kiểm LED/hành vi chương trình thử đã biết; ưu tiên nhiệt kế đo TP4056, MT3608 và vỏ pin, ghi số thật. Chỉ chạm nhẹ phần vỏ còn nguyên/không dẫn điện khi không có nhiệt kế; tay không cho giá trị °C. Reset/nóng bất thường/phồng/mùi → OFF, không cắm USB để xem log khi J5V còn ghép. **BƯỚC PHẦN MỀM — để chủ dự án làm** nếu cần chạy/nạp/quét.
11. **Chạy đầu 5 phút có người theo dõi:** đo lại VIN/3V3/V_SYS và nhiệt đầu/cuối, ghi reset/sụt áp. Mốc 5 phút là đề xuất [P2] §3.13.4, chưa chứng minh thời lượng/độ bền; lỗi → OFF và dừng.
12. **Thử sạc riêng sau khi đọc §3.9.2:** SW1 OFF, J5V rút, USB ESP32 rút; đo dòng pin nối tiếp và B+–B- theo §3.4.4, hướng đến 4.2V danh định [T] trong giới hạn pack. Theo dõi sát 5–10 phút đầu và suốt lần sạc; nóng/phồng/mùi/áp hoặc dòng vượt mức đã biết → rút USB sạc và xử lý §3.2.

### 3.13.5. Vật tư để hoàn thành “chỉ thiếu pin”

“Có trong BOM” không có nghĩa đã mua/đang có. Kiểm kê trước, dùng lại hoặc mượn món phù hợp; không mua thêm LED/trở/tụ khi gói hiện tại còn đủ. Dòng CSV cũ giữ nguyên; các dòng mới nối **sau dòng tổng cũ**, giá để trống. Dòng tổng/công thức cũ chưa bao gồm phần bổ sung và không phải tổng dự toán V2.

| Món / số lượng cần | Đối chiếu BOM | Mức | Xử lý |
|---|---|---|---|
| Board chính 90×150 mm, một | STT 20 có nhưng còn tìm mua | Bắt buộc | Chỉ dùng đúng board chính đo được; 10×10 STT 15 tùy chọn |
| ESP32/IMU sở hữu, hai cái 1×20, cái IMU 1×10 | Module theo [H]; socket STT 13–14 | Bắt buộc | Hai cái 1×20 giữ nguyên; không cắt lấy J5V |
| Đực IMU 10 + test 4 + J5V 2 chân | STT 12 có hai dải 1×40, tổng 80 chân | Bắt buộc | Cần 16 chân, đủ, không mua thêm đực |
| Cái 1×10 bổ sung, một dải | Chưa có dư; thêm **21** | Bắt buộc | Giữ hai ổ cho đầu J5V, hy sinh ổ cạnh khi cắt |
| TP4056, MT3608, SW1, J1 đực | STT 1–4 | Bắt buộc | Kiểm đúng pad/giắc; không sửa RPROG |
| Ba nút/cap, LED, R1/R2/R3/C1/C2 | STT 5–11, gói nhiều chiếc | Bắt buộc | Có sẵn dự phòng theo gói; kiểm số thật, không thêm dòng dự phòng |
| DB9, Kapton, mút | STT 16/18 | Bắt buộc | Dùng đủ bó nguồn và lớp lót |
| Ống co nhiệt cách điện, một bộ cỡ vừa dây/giắc | Chưa có; thêm **22** | Bắt buộc | Bọc chân J1/J5V/mối nối riêng |
| Băng dán hai mặt phù hợp pin/đệm, một phần dùng | Chưa có; thêm **23** | Bắt buộc | Không xiết pin, không phủ mối đang cần đo |
| Gá phi kim + đệm cách điện, một bộ | Chưa có; thêm **24** | Bắt buộc | Đỡ cổng nguồn/chống kéo; keo nến có thể bổ trợ, không đổ lên pin/chip |
| Cáp USB dữ liệu đúng đầu ESP32, một | Chưa liệt kê; thêm **25** | Bắt buộc | Kiểm kiểu cổng thật; góc vuông chỉ nên có nếu đầu thẳng bị vướng |
| Cáp cấp USB Type-C TP4056, một | Chưa liệt kê; thêm **26** | Bắt buộc khi thử sạc | Có thể dùng chung nếu cùng kiểu/đúng công năng; kiểm kê trước mua |
| Thiếc điện tử có lõi flux, một phần dùng | Chưa liệt kê; thêm **27** | Bắt buộc | Chọn loại theo §3.1, không thêm giá chưa biết |
| Flux điện tử, một phần dùng | Chưa liệt kê; thêm **28** | Bắt buộc | Không axit hàn ống nước |
| Dây hút thiếc hoặc dụng cụ hút phù hợp | Chưa liệt kê; thêm **29** | Bắt buộc | Chọn một; có bơm hút thì không cần mua cả hai |
| Băng giấy giữ linh kiện, một phần dùng | Chưa liệt kê; thêm **30** | Bắt buộc cho quy trình gá | Không thay cách điện lâu dài ở nguồn bằng băng giấy |
| Dây thử PH2.0 cái hai chân, một | Chưa liệt kê; thêm **31** | Bắt buộc cho thử qua J1 | Đầu kia tới nguồn tắt, đo cực trước; không phải pin |
| Dụng cụ §3.1: mỏ/đế, đồng hồ, kìm, nhíp, thước, kính, kẹp, lúp; thông gió | Mỏ cơ bản đã có theo [P]; phần còn lại chưa liệt kê; thêm nhóm **32** để kiểm kê | Bắt buộc dùng/được mượn | Không mặc định mua cả bộ; chỉ bổ sung món thiếu, thông gió là điều kiện làm việc |
| Nhiệt kế đầu dò cách điện | Chưa có BOM | Nên có | Ưu tiên khi sạc; sờ tay không thay phép đo nhiệt |
| Nguồn bàn giới hạn dòng, đồng hồ/máy đo nâng cao | Chưa có BOM | Cần tiếp cận để kiểm nguồn theo kịch bản; ưu tiên mượn | Không bắt buộc mua nguồn; thiếu thì trạng thái kiểm nguồn còn mở |
| Keo nến/súng keo, cáp góc vuông, breadboard | Chưa có BOM | Nên có/tùy gá | Không thêm dòng bắt buộc khi gá/cáp hiện tại đã đáp ứng |
| Pin 1S PCM, JST-PH 2.0 cái, ưu tiên ≥1000 mAh | STT 17 cũ không còn là quyết định mua | Chỉ thiếu pin sau hoàn thiện | Chọn theo §3.9.2/§3.13.3; đo cả PCM/tab/cực trước ghép |
