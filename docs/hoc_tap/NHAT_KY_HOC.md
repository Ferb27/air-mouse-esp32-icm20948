## Bài 1 — Bức tranh tổng thể — 2026-10-01 14:02
**Kết quả kiểm tra:** 2.5/3 đúng (Câu 1 và 2 đúng ngay; Câu 3 ban đầu chỉ nêu trực giác nhiễu phóng đại nhưng chưa nhớ quan hệ bậc 2 $t^2$ và số đo thực nghiệm, sau khi hướng dẫn đã chốt chuẩn xác).

### Chỗ người học hiểu sai / vấp
- "vì trong đó có cả nhiễu mà khi tích phân 2 lần thì sẽ phóng đại nhiễu lên nhiều lần, sai số tĩnh (offset) nhỏ thì sai số vị trí sẽ tăng theo thời gian 𝑡 (tôi không biết, đoạn này bạn đã dạy tôi đâu)" → Chưa nắm rõ công thức động học $s = \frac{1}{2} a t^2$ dẫn đến sai số vị trí tăng theo bình phương thời gian, và chưa nhớ mốc số liệu offset 11.6 mg đo thật.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Thiết bị gửi tọa độ tuyệt đối hay độ dời tương đối? Tay đứng yên thì sao? → Đáp: Thiết bị chỉ gửi độ dời tương đối $dX, dY$ qua gói tin BLE HID 5 byte; khi tay đứng yên thì vận tốc góc $\omega = 0$ nên $dX = 0$, con trỏ đứng yên.
- Hỏi: Vì sao không tích phân gia tốc 2 lần để tìm vị trí con trỏ? → Đáp: Do sai số tĩnh offset tích phân 2 lần sẽ tăng bùng nổ theo bình phương thời gian ($s = \frac{1}{2} a t^2$). Với offset đo thật là 11.6 mg, con trỏ sẽ tự trôi lệch 5.7 cm sau 1 s và 5.7 m sau 10 s, nên bắt buộc dùng vận tốc góc từ Gyro nhân hệ số ra độ dời.

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Không có câu hỏi ngoài lề mới.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Kiến trúc giải thuật / Cảm biến | Bổ sung phân tích định lượng sai số trôi vị trí $s = \frac{1}{2} a t^2$ với offset đo thật 11.6 mg (5.7 cm sau 1 s, 5.7 m sau 10 s). | Thầy rất hay hỏi bẫy: "Cảm biến 6-DOF có cả gia tốc kế, sao không tích phân 2 lần ra vị trí con trỏ?" |


## Bài 2 — Mỗi ngoại vi dùng để làm gì — 2026-10-01 14:29
**Kết quả kiểm tra:** 3/3 đúng (Câu 1, Câu 2 nắm rất chắc; Câu 3 nhớ đúng bản chất I2C ít dây, tốc độ đủ nhanh và đoán đúng NCS nối VCC).

### Chỗ người học hiểu sai / vấp
- "ncs được nối gnd hay vcc gì đó tôi không nhớ (chắc là vcc)" → Còn hơi do dự về chân NCS; cần nhớ bản chất NCS là Chip Select tích cực mức thấp (active-low), muốn tắt SPI để ép sang chế độ I2C thì bắt buộc phải kéo lên mức cao 3.3 V.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Tín hiệu chuyển động đọc bằng ADC hay ngoại vi nào? ADC của ESP32 làm gì? → Đáp: Đọc số liệu số 16-bit qua bus I2C; ADC nằm trong chip ICM-20948 chứ không đi qua ADC của ESP32. Khối ADC của ESP32 chỉ dùng đo pin ở GPIO34 (hiện firmware chưa triển khai).
- Hỏi: Vì sao không dùng SPI? Chân NCS nối đi đâu? → Đáp: I2C tiết kiệm chân (chỉ dùng GPIO21 SDA, GPIO22 SCL); ở 400 kHz đọc burst 12 byte chỉ mất 438 µs (chiếm 4.4% chu kỳ 10 ms), bus rảnh >95% nên hoàn toàn đáp ứng tốt. Chân NCS nối 3.3 V để vô hiệu hóa SPI và khóa vào I2C.

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Không có câu hỏi phát sinh.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Bảng phân bổ ngoại vi / Khối giao tiếp | Bổ sung thời gian chiếm dụng bus: I2C 400 kHz mất 438 µs (4.4% chu kỳ 10 ms), bus rảnh 95.6%. | Thầy hỏi dồn "tại sao không chọn SPI có tốc độ hàng chục MHz", đưa con số này ra là bảo vệ thành công ngay lập tức. |


## Bài 3 — ADC và Mạch đo Pin — 2026-10-01 14:50
**Kết quả kiểm tra:** 2.5/3 đúng (Câu 1 hiểu rất sâu bản chất 16-bit có dấu và tự tính 65.5 chuẩn xác; Câu 2 nhớ dải an toàn nhưng cần nhắc lại phép tính chia đôi; Câu 3 sau khi được giải thích cơ chế bẫy đã nắm được bộ so sánh).

### Chỗ người học hiểu sai / vấp
- "chân GPIO34 của ESP32 sẽ nhận được điện áp bao nhiêu vôn (dưới 2.45 V)" → Nắm được điều kiện giới hạn kỹ thuật ($< 2.45\text{ V}$) nhưng ban đầu chưa tính ra con số cụ thể $4.2\text{ V} / 2 = 2.1\text{ V}$.
- "cái này bạn đã dạy đâu mà tôi biết" (Câu 3 về TP4056) → Dễ rơi vào bẫy ngộ nhận mọi chức năng quản lý điện áp đều cần đến vi điều khiển và ADC.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: LSB là gì, vì sao trong code chia 65.5? → Đáp: LSB là khoảng cách giữa 2 vạch đo liền kề của ADC (bước nhảy lượng tử hóa nhỏ nhất). Ở dải $\pm 500^\circ/\text{s}$, ADC 16-bit có dấu ($2^{15} = 32768$), độ nhạy là $32768 / 500 \approx 65.5\text{ LSB}/(^\circ/\text{s})$.
- Hỏi: Pin 4.2 V vào GPIO34 bao nhiêu vôn? TP4056 có dùng ADC không? → Đáp: Pin 4.2 V qua cầu phân áp $100\text{ k}\Omega / 100\text{ k}\Omega$ ra $2.1\text{ V}$ để nằm trong dải đo chính xác ($< 2.45\text{ V}$) và không cháy chân ESP32. TP4056 không dùng ADC mà dùng bộ so sánh (comparator) với điện áp chuẩn nội 4.2 V để ngắt sạc.

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Không có câu hỏi phát sinh ngoài tài liệu.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Khối nguồn & Pin / Mạch đo pin | Ghi rõ: TP4056 tự động quản lý sạc bằng bộ so sánh analog độc lập; cầu phân áp 100k/100k đưa 4.2 V về 2.1 V cho ADC1 GPIO34 của ESP32. | Tránh bẫy thầy hỏi: "ESP32 có điều khiển ngắt sạc của TP4056 qua ADC không?" |


## Bài 4 — Giao tiếp I2C — 2026-10-01 15:52
**Kết quả kiểm tra:** 2/3 đúng vòng đầu (Câu 1 dịch bit ra `0xD0` đúng ngay; Câu 2 nhầm sang chân NCS; Câu 3 chỉ nêu tiết kiệm thời gian; sau khi phân tích trực giác sâu người học đã nắm vững cả 3 câu).

### Chỗ người học hiểu sai / vấp
- "thì sẽ không thể kéo lên vcc để chuyển chế độ được" (Câu 2) → Nhầm lẫn chức năng của điện trở kéo pull-up trên bus I2C với việc kéo chân NCS lên VCC để khóa chế độ I2C.
- "tôi nghĩ là không cần stop rồi start đọc, đỡ tốn thời gian hơn" (Câu 3) → Chưa thấy được lý do kỹ thuật cốt lõi: giữ quyền làm chủ bus và bảo toàn con trỏ địa chỉ nội bộ của chip cảm biến.
- Chưa nắm bản chất tại sao xung clock SCL cần "mấp mô" và SDA "đổi trạng thái" → Cần ví dụ trực quan về nhịp đếm clock (SCL) và giá trị bit điện áp 0/1 (SDA).

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Tại sao địa chỉ là `0x68` mà khi ghi lại truyền `0xD0`? → Đáp: Chuẩn I2C truyền 7 bit địa chỉ dịch trái 1 bit ghép thêm bit R/W ở cuối (với lệnh Ghi, bit R/W = 0 nên `0x68 << 1 | 0 = 0xD0`).
- Hỏi: Nếu không có trở kéo thì bus I2C bị sao? → Đáp: Chân I2C là cực máng hở (open-drain) chỉ có thể kéo xuống GND chứ không tự đẩy lên 3.3 V. Không có trở kéo thì dây không thể lên mức 1, mất xung nhịp SCL và bit 1 trên SDA, bus bị treo hoàn toàn.
- Hỏi: Repeated START để làm gì? → Đáp: Để giữ quyền làm chủ bus không bị gián đoạn, và quan trọng nhất là ngăn cảm biến tự động reset con trỏ địa chỉ nội bộ về ô mặc định (`0x00`) sau cờ STOP, đảm bảo đọc đúng 12 byte bắt đầu từ ô `0x2D`.

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Hỏi: "SCL mấp mô và SDA đổi trạng thái có tác dụng gì?" → Đáp: Dữ liệu là chuỗi bit 0 và 1 (0 V = bit 0, 3.3 V = bit 1 trên SDA). SCL đóng vai trò tiếng đếm nhịp "Một - Hai - Ba", cứ mỗi nhịp xung của SCL thì bên nhận mới nhìn sang SDA để ghi lại bit dữ liệu tại thời điểm đó.
- Hỏi: "Mạch hiện tại chỉ có 1 ESP32 thì cái gì chen chân vào mà phải giữ quyền bus?" → Đáp: Có 2 lý do: (1) Nếu phát STOP, chip ICM-20948 có thể tự reset con trỏ địa chỉ nội bộ về ô `0x00` làm đọc sai dữ liệu; (2) Chuẩn thiết kế công nghiệp đảm bảo an toàn tuyệt đối nếu tương lai mở rộng hệ thống đa Master (Multi-Master).

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md` | Mục 5 (Giao tiếp I2C) | Bổ sung phân tích: Kể cả hệ Single-Master vẫn bắt buộc dùng Repeated START vì cơ chế reset con trỏ địa chỉ nội bộ (address pointer) của cảm biến MEMS khi gặp STOP. | Người học hỏi câu hỏi thực tế rất sắc sảo, thầy rất dễ hỏi vặn: "Mạch em chỉ có 1 ESP32 thì tranh chấp với ai mà cần Repeated START?". |


## Bài 5 — Thanh ghi ICM-20948 từng bit — 2026-10-02 00:52
**Kết quả kiểm tra:** 3/3 đúng sau khi được hướng dẫn từng bước (Đổi `0x1B` ra nhị phân `0001 1011` rất chuẩn; hiểu vì sao `0xFFFF` bị tràn thanh ghi 8-bit; phân biệt rõ tần số lấy mẫu và tần số lọc DLPF).

### Chỗ người học hiểu sai / vấp
- Ban đầu chưa hình dung được thanh ghi 8-bit và cách đổi từ số Hex sang nhị phân → Sau khi dùng ví dụ 8 công tắc trên tường chia làm 2 nửa (mỗi nửa 4 công tắc ứng với 1 ký tự Hex), người học đã tự đổi thành thạo `1 -> 0001`, `B -> 1011`.
- Chưa hiểu khái niệm "chia tần số" (Frequency Divider) → Đã giải thích bằng ví dụ đồng hồ đập nhịp 1125 lần/giây, bộ chia đếm đủ 11 nhịp ($1 + 10$) mới đo một lần, giúp giảm từ 1125 Hz xuống 102.27 Hz để chống ngập dữ liệu ESP32.
- Ban đầu chưa rõ tại sao dải đo mở rộng thì chuột chạy chậm đi → Đã nắm được: nấc `01` là $\pm 500^\circ/\text{s}$ (độ nhạy 65.5 LSB), nấc `11` là $\pm 2000^\circ/\text{s}$ (độ nhạy 16.4 LSB thô hơn 4 lần), code vẫn chia 65.5 nên con trỏ bị chậm đi 4 lần.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Ghi 0x1B vào GYRO_CONFIG_1 có ý nghĩa gì? → Đáp: `0x1B` là `0001 1011`, trong đó bit 0 = 1 là bật bộ lọc DLPF; bit [2:1] = `01` là chọn dải đo $\pm 500^\circ/\text{s}$; bit [5:3] = `011` là chọn tần số lọc 51.2 Hz.
- Hỏi: Ghi 0xFFFF vào GYRO_SMPLRT_DIV được không? → Đáp: Không, vì thanh ghi chỉ rộng 8-bit (chứa tối đa `0xFF` = 255), không thể ghi giá trị 16-bit `0xFFFF` vào được.
- Hỏi: DLPF 51.2 Hz có phải tần số lấy mẫu không? Số 51.2 Hz ở đâu ra? → Đáp: Không, đó là tần số cắt của bộ lọc để rây lọc rung lắc tay (tần số lấy mẫu là 102.27 Hz). Số 51.2 Hz tra từ bảng datasheet ứng với cụm bit `011`, được chọn để xấp xỉ một nửa tần số lấy mẫu theo định lý Nyquist ($102.27 / 2 \approx 51.14\text{ Hz}$).

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Hỏi: "Tại sao `01` là 500 còn `11` là 2000?" → Đáp: Do nhà sản xuất quy định sẵn 4 nấc dải đo ở 2 bit [2:1]: `00` là 250, `01` là 500, `10` là 1000, `11` là $2000^\circ/\text{s}$ (mỗi nấc tăng gấp đôi).
- Hỏi: "Chia tần số nghĩa là sao?" → Đáp: Đếm nhịp để giảm tốc độ lấy mẫu từ xung gốc 1125 Hz xuống 102.27 Hz qua công thức $1125 / (1 + \text{DIV})$, tránh làm ESP32 quá tải.
- Hỏi: "Con số 51.2 Hz từ đâu ra nếu thầy hỏi?" → Đáp: Tra trong bảng cấu hình DLPF của datasheet ICM-20948 (ứng với bit [5:3] = `011`), chọn giá trị này vì nó khớp với tiêu chuẩn Nyquist bằng 1/2 tần số lấy mẫu 102.27 Hz.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md` | Mục 3 / Thanh ghi ICM | Thêm bảng tra giải thích rõ nguồn gốc 51.2 Hz và liên hệ với định lý Nyquist ($f_{cutoff} \approx f_s / 2$). | Giúp sinh viên tự tin khi thầy hỏi vặn sâu về căn cứ chọn thông số lọc. |


## Bài 6 — GPIO, Nút bấm và Đèn LED — 2026-10-02 09:20
**Kết quả kiểm tra:** 3/3 đúng xuất sắc (Câu 1 giải thích rất chuẩn active-low; Câu 2 tránh bẫy hoàn hảo khi chỉ ra bit 0 của `GPIO_OUT1_REG`; Câu 3 chỉ ra đúng GPIO34 là input-only và thiếu pull-up nội).

### Chỗ người học hiểu sai / vấp
- Không có lỗi sai nào trong bài này, người học nắm bài cực kỳ nhanh và chuẩn xác.
- Lưu ý bẫy kèm theo cần nhớ: Hệ thống hiện tại **chưa có chống dội phím (chưa debounce)** cả ở phần cứng lẫn firmware; ESP32 không có thanh ghi tốc độ chân `OSPEEDR` như STM32 mà dùng `FUN_DRV` để chọn dòng lái.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Vì sao nhấn nút lại đọc về mức 0? → Đáp: Mạch dùng trở kéo lên nội (`INPUT_PULLUP`), thả nút chân ở mức 1 (3.3 V), khi nhấn nút thì chân bị chập thẳng xuống đất (GND) nên đọc về mức 0 (active-low).
- Hỏi: Bật LED GPIO32 thì ghi bit nào thanh ghi nào? → Đáp: Ghi vào bit 0 của thanh ghi `GPIO_OUT1_REG` (địa chỉ `0x3FF44010`), vì `GPIO_OUT_REG` chỉ chứa 32 bit cho GPIO0–31.
- Hỏi: GPIO34 có làm nút bấm được không? → Đáp: Được về mặt ngõ vào vì là chân input-only, nhưng không có điện trở kéo nội bộ nên bắt buộc phải hàn thêm điện trở kéo ngoài (pull-up/pull-down).

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Không có câu hỏi phát sinh ngoài tài liệu.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Sơ đồ nguyên lý / Nút bấm & LED | Ghi rõ chân GPIO32 nằm ở bit 0 của `GPIO_OUT1_REG`, dòng LED tính toán $(3.3\text{ V} - 2.1\text{ V}) / 1\text{ k}\Omega = 1.2\text{ mA}$, và nêu trung thực hệ thống chưa có chống dội phím (kế hoạch tuần sau). | Thầy chuyên soi thanh ghi vi điều khiển và hỏi về hiện tượng dội phím cơ học. |


## Bài 7 — Thuật toán xử lý chuyển động — 2026-10-03 00:12
**Kết quả kiểm tra:** 3/3 đúng sau khi được phân tích bản chất (Câu 1 tự tính 64.24 -> 64 chuẩn xác; Câu 2 hiểu sâu hiện tượng tràn bit dấu làm đảo chiều chuột; Câu 3 nắm rõ bản chất vector trọng lực không đổi khi quay góc Yaw).

### Chỗ người học hiểu sai / vấp
- Ban đầu băn khoăn về giới hạn 8-bit có dấu (-127 đến +127) của chuột BLE HID và cách cài đặt lệnh kẹp trần (clamp) trong code.
- Tính ra trường hợp vung tay nhanh ($200^\circ/\text{s} \to dX = 438$) và thắc mắc Bluetooth gửi đi kiểu gì nếu bị giới hạn 127 → Đã giải thích cơ chế bão hòa: kẹp cứng về 127 trước khi đóng gói, các chu kỳ 10 ms liên tiếp gửi 127 giúp chuột lướt nhanh mượt mà mà không nổ lỗi.
- Ban đầu chưa rõ tại sao gia tốc kế không sửa được góc Yaw → Đã làm rõ: trục xoay Yaw thẳng đứng song song với vector trọng lực $\vec{g}$, nên khi xoay ngang góc trọng lực không đổi, gia tốc kế hoàn toàn "mù" trước góc Yaw (muốn sửa phải có từ kế Magnetometer).

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Tính dX khi xoay 30 °/s (deadzone 0.8, gain 2.2)? → Đáp: $dX = \text{round}(2.2 \times (30 - 0.8)) = \text{round}(64.24) = 64$.
- Hỏi: Nếu tính ra dX = 200 mà không kẹp thì sao? → Đáp: Bắt buộc phải kẹp về 127; nếu không kẹp, ép sang kiểu số `int8_t` sẽ bị tràn bit dấu thành số âm ($-56$), khiến con trỏ chuột giật chạy thụt lùi ngược hướng tay vung.
- Hỏi: Gia tốc kế có sửa được góc trôi Yaw trong bộ lọc bù không? → Đáp: Không, vì góc xoay Yaw quay quanh trục thẳng đứng song song với vector trọng lực của Trái Đất, hình chiếu trọng lực không thay đổi nên gia tốc kế không thể nhận biết được chuyển động xoay ngang này.

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Hỏi: "Tại sao gói tin Bluetooth HID 8 bit lại có phạm vi -127 đến +127, và lệnh kẹp là làm thế nào?" → Đáp: Do chuẩn HID Mouse dùng 8-bit có dấu (`int8_t`), 1 bit dấu nên còn 7 bit độ lớn ($2^7 = 128$) và bản đặc tả quy định dải đối xứng $[-127, +127]$. Lệnh kẹp dùng câu lệnh điều kiện `if (dX > 127) dX = 127;` để giới hạn trần.
- Hỏi: "Nếu vung tay 200 độ/s tính ra dX = 438 thì làm sao Bluetooth gửi đi được khi giới hạn 127?" → Đáp: Khi tính ra 438, lệnh kẹp ép nó về đúng 127 trước khi đưa vào gói tin BLE. Ở các chu kỳ 10 ms tiếp theo, nếu tay vẫn quay nhanh thì tiếp tục gửi các gói 127, tạo ra hiệu ứng con trỏ lướt ở vận tốc bão hòa tối đa mà không bị tràn số.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Mục 2 (Kiến trúc giải thuật) | Minh họa rõ hiện tượng tràn số nguyên có dấu `int8_t` (200 thành -56) và sự cần thiết của lệnh kẹp `clamp(dX, -127, 127)`. | Thầy rất hay hỏi dồn dạng bài toán biên: "Nếu người dùng vẩy tay cực mạnh thì thuật toán xử lý thế nào, có bị tràn số không?". |


## Bài 8 — Định thời, UART và Bluetooth BLE — 2026-10-03 00:36
**Kết quả kiểm tra:** 3/3 đúng sau khi làm rõ (Phân biệt rõ 1 byte độ dời dX và gói HID hoàn chỉnh 5 byte; nắm chuẩn kỹ thuật polling `micros()`; tính chính xác 11 520 byte/s).

### Chỗ người học hiểu sai / vấp
- "ở phần ble tôi tưởng nó chỉ truyền 8 bit chứ" → Ban đầu nhầm lẫn giữa kiểu dữ liệu 8-bit (`int8_t`) của riêng giá trị $dX$ với độ dài của cả gói tin chuột. Sau khi giải thích bức thư 5 ngăn (nút bấm, dX, dY, wheel cuộn dọc, pan cuộn ngang), người học đã phân biệt rành rẽ.
- Cần ghi nhớ tính trung thực: Thầy hỏi về thử nghiệm thực tế chuột trên máy tính thì phải trả lời đúng hiện trạng: BLE ghép nối PC là **NOT_TESTED**, mới chỉ đo phát gói tin và test bench ngắn hạn.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Chu kỳ 10 ms tạo bằng ngắt timer hay cách nào? → Đáp: Bằng cách thăm dò so sánh thời gian qua hàm `micros()` trong vòng lặp `loop()`, không dùng ngắt timer phần cứng; đo thực tế đạt đúng 10 000 µs (100 Hz).
- Hỏi: UART 115200 baud khung 8N1 truyền bao nhiêu byte/giây? → Đáp: Khung 8N1 tốn 10 bit cho mỗi byte (1 start + 8 data + 1 stop), nên tốc độ tối đa là $115\,200 / 10 = 11\,520\text{ byte/s}$.
- Hỏi: Gói tin BLE chuột dài mấy byte? Kết nối PC đã hoàn hảo chưa? → Đáp: Dài 5 byte gồm [Nút, dX, dY, Wheel, Pan]. Hiện tại khâu ghép nối điều khiển chuột ổn định lâu dài trên máy tính thật đang ở trạng thái chưa kiểm thử toàn diện (NOT_TESTED).

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Hỏi: "Tại sao ở bài trước bảo BLE chuột là 8 bit mà giờ lại bảo 5 byte?" → Đáp: 8 bit (1 byte) chỉ là kích thước của riêng độ dời ngang $dX$ hoặc $dY$ (`int8_t`), còn cả gói tin chuột gửi đi phải chứa đủ 5 thông số (nút bấm, dX, dY, cuộn dọc, cuộn ngang) nên chiếm tổng cộng 5 byte (40 bit).

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Bảng trạng thái thực nghiệm / Kết luận | Ghi rõ cấu trúc gói tin 5 byte chuẩn HID Mouse và trung thực đánh dấu trạng thái "BLE Mouse with Host OS: NOT_TESTED". | Tránh bẫy thầy vặn "đã thử nghiệm chuột click và cuộn mượt mà trên Windows/Mac thật chưa". |


---

# TỔNG KẾT TIẾN TRÌNH & BÁO CÁO BÀN GIAO CHO CLAUDE
*(Người học yêu cầu bỏ qua phần thi thử Bài 9 để chuyển sang tổng hợp báo cáo hoàn chỉnh cho Agent tiếp theo)*

## 1. Đánh giá chung về người học
- **Khả năng tiếp thu:** Rất tốt khi được tiếp cận từ trực giác đời thường; có tư duy phản biện sắc sảo (chủ động thắc mắc về con trỏ nội I2C trong hệ Single-Master, bản chất 8-bit dX vs 5 byte HID report, hiện tượng bão hòa vung tay nhanh).
- **Kỹ năng tính toán:** Đã tự tay tính toán chuẩn xác các con số kỹ thuật:
  + Đổi `0x1B` ra nhị phân `0001 1011` và bóc tách nhóm bit.
  + Tính dải đo và LSB: $2^{15} / 500 = 65.5\text{ LSB}/(^\circ/\text{s})$; $2^{15} / 4 = 8192\text{ LSB/g}$.
  + Tính cầu phân áp pin: $4.2\text{ V} / 2 = 2.1\text{ V}$ (an toàn dưới ngưỡng $2.45\text{ V}$ của ADC ESP32).
  + Tính tốc độ I2C: $438\ \mu\text{s} / 10\,000\ \mu\text{s} \approx 4.4\%$ chu kỳ.
  + Tính độ dời chuột: $\omega = 30^\circ/\text{s} \to dX = \text{round}(2.2 \times (30 - 0.8)) = 64$.
  + Tính tốc độ UART: $115\,200 / 10 = 11\,520\text{ byte/s}$.

---

## 2. TOP 5 CÂU DỄ MẤT ĐIỂM NHẤT (XẾP THEO MỨC ĐỘ NGUY HIỂM)

### 🔴 Top 1: Bẫy "ADC dùng để làm gì? Tín hiệu ICM đọc bằng ADC à? TP4056 có ADC không?"
- **Nguy cơ:** Rất dễ nhầm cảm biến vào ADC của ESP32, hoặc ngộ nhận TP4056 gửi dữ liệu ADC về vi điều khiển.
- **Câu trả lời chuẩn:**
  1. ICM-20948 tự số hóa bằng ADC 16-bit nội bộ, ESP32 chỉ đọc dữ liệu số hoàn chỉnh qua bus I2C.
  2. ADC1 của ESP32 (GPIO34) chỉ dùng đo pin qua cầu chia $100\text{ k}\Omega / 100\text{ k}\Omega$ ($4.2\text{ V} \to 2.1\text{ V}$), firmware hiện tại **chưa làm (NOT_IMPLEMENTED)**.
  3. Mạch sạc TP4056 và bảo vệ DW01A **không có ADC**, chúng dùng bộ so sánh analog (comparator) với điện áp tham chiếu nội ($4.2\text{ V}$ và $2.4\text{ V} / 4.3\text{ V}$) để tự động đóng ngắt phần cứng.

### 🔴 Top 2: Bẫy thanh ghi GPIO: "Bật LED GPIO32 ở bit nào thanh ghi nào?"
- **Nguy cơ:** Bị phản xạ trả lời "bit 32 của `GPIO_OUT_REG`".
- **Câu trả lời chuẩn:** Thanh ghi `GPIO_OUT_REG` chỉ có 32 bit cho GPIO 0–31. Chân GPIO32 bắt buộc nằm ở **bit 0 của thanh ghi thứ hai `GPIO_OUT1_REG`** (địa chỉ `0x3FF44010`).

### 🟠 Top 3: Bẫy I2C: "Tại sao Single-Master vẫn bắt buộc dùng Repeated START?"
- **Nguy cơ:** Trả lời "để tiết kiệm thời gian" hoặc "chỉ có 1 vi điều khiển thì không cần".
- **Câu trả lời chuẩn:** Nếu phát STOP, chip ICM-20948 có thể tự động reset con trỏ địa chỉ thanh ghi nội bộ về mặc định (`0x00`), làm lệnh Đọc tiếp theo lấy sai dữ liệu. Dùng Repeated START (`Wire.endTransmission(false)`) giúp ghim chặt con trỏ tại ô `0x2D` để đọc liên tục 12 byte dữ liệu chuyển động.

### 🟠 Top 4: Bẫy thuật toán & Toán học: "Nếu dX tính ra 200 thì sao? Accel có sửa được góc Yaw không?"
- **Nguy cơ:** Quên khái niệm tràn số nguyên có dấu `int8_t` hoặc ngộ nhận trọng lực sửa được cả 3 trục.
- **Câu trả lời chuẩn:** 
  1. Gói tin HID dùng `int8_t` ($-127$ đến $+127$). Nếu $dX = 200$ mà không kẹp (clamp), ép kiểu sẽ bị tràn bit dấu thành số âm ($-56$), khiến chuột giật lùi ngược hướng tay vung.
  2. Gia tốc kế đo vector trọng lực $\vec{g}$ cắm thẳng đứng, nên khi xoay ngang Yaw quanh trục thẳng đứng, trọng lực không đổi hướng $\to$ gia tốc kế hoàn toàn "mù" trước góc Yaw (chỉ sửa được Roll và Pitch).

### 🟡 Top 5: Bẫy trạng thái thực nghiệm & Khung truyền
- **Nguy cơ:** Khai báo "đã thử nghiệm chuột mượt 100% trên PC" hoặc "gói tin chuột dài 4 byte / 8 bit".
- **Câu trả lời chuẩn:**
  1. Gói tin Bluetooth HID dài **5 byte** [Nút, dX, dY, Wheel, Pan].
  2. Trạng thái ghép nối chuột với máy tính hiện tại là **NOT_TESTED** (mới kiểm thử phát gói tin, chưa test dài hạn trên Host OS).
  3. Nhịp 10 ms tạo bằng polling thăm dò `micros()`, không dùng ngắt timer phần cứng.

---

## 3. BẢNG TỔNG HỢP ĐỀ XUẤT CLAUDE BỔ SUNG VÀO BÁO CÁO & KỊCH BẢN THUYẾT TRÌNH

| Tài liệu đích | Mục cần sửa | Nội dung đề xuất bổ sung | Lý do kỹ thuật |
| --- | --- | --- | --- |
| `BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx` | Kiến trúc giải thuật (Mục 2) | Bổ sung phân tích định lượng sai số trôi vị trí $s = \frac{1}{2} a t^2$ với offset đo thật 11.6 mg (trôi 5.7 cm sau 1 s, 5.7 m sau 10 s). | Bảo vệ lý do cốt lõi vì sao không tích phân gia tốc kế 2 lần mà dùng con quay hồi chuyển rate-control. |
| `BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx` | Khối giao tiếp I2C | Thêm thông số: Thời gian chiếm dụng bus I2C 400 kHz là $438\ \mu\text{s}$ (4.4% chu kỳ 10 ms), bus rảnh 95.6%. | Trả lời thuyết phục câu hỏi "tại sao không dùng SPI tốc độ cao". |
| `BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx` | Bảng thanh ghi & Ngoại vi | Nêu rõ địa chỉ bit 0 của `GPIO_OUT1_REG` cho GPIO32, và cơ chế bộ so sánh analog độc lập của TP4056 / DW01A. | Khóa chặt 2 bẫy thanh ghi và bẫy ADC thầy hay hỏi nhất. |
| `BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx` | Thuật toán chuyển động | Thêm công thức kẹp bão hòa `clamp(dX, -127, 127)` và ví dụ tràn số bù hai ($200 \to -56$). | Chứng minh thuật toán chặt chẽ, xử lý trọn vẹn các trường hợp biên (vung tay cực nhanh). |
| `preprare4T/KICH_BAN_THUYET_TRINH_BAO_CAO_GIUA_KY.md` | Lời thoại phần Demo / Kết quả | Cập nhật kịch bản nói trung thực: Nhịp 10 ms chạy bằng polling `micros()`; BLE HID đã phát gói 5 byte nhưng ghép nối PC dài hạn đang ở trạng thái NOT_TESTED. | Thầy đánh giá cực cao sự trung thực khoa học, tránh bị bẻ khi thầy yêu cầu cắm chuột demo tại chỗ. |


---

## Đính chính — Về cơ chế Repeated START (Sr) của ICM-20948 — 2026-10-03 00:58

### 1. Nội dung đính chính sai lệch cũ
- **Sai (trong các bài học trước):** "Nếu phát cờ STOP, chip ICM-20948 sẽ tự động reset con trỏ địa chỉ thanh ghi nội bộ về 0x00, làm sai dữ liệu đọc."
  → **Đính chính:** Datasheet InvenSense DS-000189 **hoàn toàn KHÔNG nói điều này**. Các dòng giải thích về "reset con trỏ về 0x00" trong nhật ký học cũ là **SAI VÀ KHÔNG ĐƯỢC PHÉP SỬ DỤNG** khi trả lời thầy hoặc viết báo cáo.

### 2. Bản chất kỹ thuật chuẩn xác theo Datasheet (DS-000189 §6.3–§6.4)
1. **Tuân thủ đúng trình tự quy định của nhà sản xuất:** Datasheet quy định bắt buộc chuỗi giao dịch đọc thanh ghi: `S (START) → AD+W → RA (Register Address) → Sr (Repeated START) → AD+R → DATA... → NACK → P (STOP)`. Trong firmware, lệnh `Wire.endTransmission(false)` chính là lệnh phát ra điều kiện `Sr` này.
2. **Nguyên lý chuẩn I2C:** Khi dùng `Sr` thay vì `STOP`, bus I2C **luôn duy trì ở trạng thái bận (BUSY)**. Trong hệ thống có nhiều Master, không một Master nào khác có thể chen ngang giành quyền điều khiển giữa pha "chỉ định địa chỉ thanh ghi" và pha "đọc dữ liệu".
3. **Phản biện khi thầy hỏi dồn Single-Master:** *"Hiện tại mạch em chỉ có 1 ESP32 thì chống ai cướp bus?"*
   → **Đáp:** Hiện tại hệ thống chỉ có 1 Master nên ưu thế chống tranh chấp bus chưa phát huy; tuy nhiên nhóm tuân thủ nghiêm ngặt 100% theo đúng trình tự chuẩn mà datasheet DS-000189 mục 6.3 quy định. Thao tác tách rời bằng STOP rồi phát START mới không được datasheet mô tả nên nhóm không áp dụng và không khẳng định tính ổn định.


## NC-1 — Đọc hiểu từng bảng của báo cáo nộp — 2026-10-03 09:37
**Kết quả kiểm tra:** 4/4 chủ đề lớn đạt yêu cầu (Wired-AND/Push-Pull; 4 User Bank & 0x7F; ADC1 SAR 11 dB & 2.45 V; Phân tầng C++ sang Assembly Xtensa và 5 bước thanh ghi ADC).

### Chỗ người học hiểu sai / vấp
- Ban đầu nhầm logic Wired-AND (nghĩ giữ mức 0 nếu tất cả ở 0) → Đã chỉnh lại: Wired-AND chỉ ở mức 1 khi TẤT CẢ cùng thả; chỉ 1 bên kéo đất là toàn bộ dây về 0.
- Ban đầu chưa rõ tại sao Push-Pull bị chập → Đã hiểu: 1 bên đẩy 3.3V, 1 bên kéo 0V tạo đường ngắn mạch (short circuit) làm cháy chân chip.
- Thắc mắc sâu về lý do suy hao 11 dB chỉ giới hạn chính xác từ 150 mV đến 2450 mV ($2.45\text{ V}$) → Đã nắm: lõi SAR ADC chỉ nhận tối đa 1.1 V (0 dB), mạch suy hao 11 dB bị méo bão hòa phi tuyến khi điện áp vượt 2.45 V.
- Thắc mắc về lỗi ghi đè Read-Modify-Write khi có ngắt chen ngang → Đã hiểu cơ chế nguyên tử (Atomic) của thanh ghi W1TS.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Wired-AND là gì? Vì sao Push-Pull chập? → Đáp: Wired-AND chỉ ở mức 1 khi tất cả cùng buông tay cho trở kéo, 1 bên kéo 0 là dây về 0. Chân Push-Pull có transistor nối VCC và GND, nếu 1 bên xuất 1 và 1 bên xuất 0 sẽ gây ngắn mạch 3.3V xuống GND làm cháy chân chip.
- Hỏi: 4 Bank để làm gì, đổi bằng thanh ghi nào? → Đáp: Để vượt qua giới hạn địa chỉ 7-bit (128 ô) của thanh ghi I2C. Chuyển Bank bằng thanh ghi `0x7F` (`REG_BANK_SEL`) có mặt ở cả 4 Bank.
- Hỏi: Vì sao đo pin bằng ADC1 GPIO34? Dải 11 dB là bao nhiêu? → Đáp: ADC2 bị driver Wi-Fi chiếm dụng; ADC1 độc lập. Mức suy hao 11 dB có dải tuyến tính chính xác từ 150 mV đến 2450 mV ($2.45\text{ V}$), đưa 2.8 V vào sẽ bị méo bão hòa ở mã 4095.
- Hỏi: 104 trong mã Assembly `movi a11, 104` là gì? → Đáp: Là $0\times 68$ đổi sang thập phân ($6 \times 16 + 8 = 104$), chính là địa chỉ I2C của ICM-20948 nạp vào thanh ghi tham số hàm `Wire.beginTransmission`.
- Hỏi: 5 bước phần cứng khi đọc SAR ADC1? → Đáp: (1) Cài 12-bit & suy hao 11 dB; (2) Chọn kênh 6 (GPIO34); (3) Bật bit START; (4) Chờ cờ DONE; (5) Đọc dữ liệu ra.

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Hỏi: "Tại sao suy hao 11 dB thì trần đo lại là 2.45 V chứ không phải 3.3 V hay 3.9 V?" → Đáp: Lõi ADC chỉ đo tối đa 1.1 V; bộ suy hao 11 dB nén tín hiệu ~3.55 lần ($1.1 \times 3.55 \approx 3.9\text{ V}$). Nhưng do transistor bị méo phi tuyến khi điện áp cao, Espressif chỉ cam kết độ chính xác trong dải 150–2450 mV; trên 2.45 V bị bão hòa.
- Hỏi: "Vì sao Read-Modify-Write lại nguy hiểm khi có ngắt, và W1TS giải quyết thế nào?" → Đáp: RMW cần 3 bước nên nếu ngắt chen giữa sẽ ghi đè trạng thái cũ làm mất thay đổi của ngắt. W1TS chỉ ghi số 1 vào chân cần bật, phần cứng tự kích hoạt nguyên tử trong 1 chu kỳ, không đụng tới các chân khác.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Bảng 4.1 / Bảng 4.2.1 | Ghi chú rõ nguồn gốc số 104 (`0x68`) trong đoạn Assembly Xtensa và ưu điểm atomic của W1TS. | Thầy rất thích hỏi xoáy vào chi tiết disassembly và cơ chế thanh ghi MMIO. |


## NC-2 — Từ mã C tới chương trình đang chạy (Bản đồ bộ nhớ & Khởi động) — 2026-10-03 10:08
**Kết quả kiểm tra:** 3/3 đạt yêu cầu (Phân biệt cấu trúc RAM .data vs .bss; hiểu bản chất tiền xử lý #define; nắm rõ chuỗi khởi động đa tầng của ESP32).

### Chỗ người học hiểu sai / vấp
- Thắc mắc sâu về việc tại sao `#define` không chiếm byte nào trong bảng biến dữ liệu → Đã làm rõ: `#define` là cơ chế Tìm & Thay thế tự động của bộ tiền xử lý (Preprocessor), số được nhúng thẳng vào lệnh CPU dạng giá trị tức thời (immediate value) trong mã máy, khác với biến hằng `const` phải nằm ở `.rodata`.
- Ban đầu cho rằng chỉ cần biết tổng DRAM, không cần phân biệt `.data` và `.bss` → Đã nhắc mẹo ghi nhớ cho môn học: **BSS = Bằng Số Số-không (Zero)**, biến khởi tạo khác 0 nằm ở `.data`.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: RAM 39 628 B và Flash 88.4% gồm những gì? → Đáp: RAM gồm `.dram0.data` ($23\,188\text{ B}$) và `.dram0.bss` ($16\,440\text{ B}$). Flash dùng tới $1.15\text{ MB}$ ($88.4\%$) do ngăn xếp Bluetooth (Bluedroid) và framework Arduino chiếm phần lớn trong `.flash.text`.
- Hỏi: Biến bias và biến bank nằm ở đâu? → Đáp: `s_bias_x = 0.0f` nằm ở `.bss` (xóa về 0 lúc boot, không tốn Flash); `s_current_bank = 0xFF` nằm ở `.data` (lưu giá trị trong Flash rồi chép sang RAM lúc boot).
- Hỏi: Vì sao #define không tốn bộ nhớ biến? → Đáp: Do bộ tiền xử lý thay thế thẳng giá trị vào câu lệnh mã máy lúc biên dịch, không cấp phát ô nhớ độc lập.
- Hỏi: Sau reset, ESP32 chạy gì đầu tiên? Địa chỉ 0x10000 là gì? → Đáp: Chạy ROM bootloader (tầng 1) nung sẵn trong chip, kiểm tra chân strapping GPIO0 để chọn chế độ boot/nạp. Sau đó nạp bootloader tầng 2 ở `0x1000`, đọc phân vùng ở `0x8000`, nạp app tại `0x10000`, khởi động FreeRTOS rồi mới tạo tác vụ gọi `setup()` và `loop()`.

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Không có câu hỏi phát sinh thêm.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `deliverables/BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.md` | Bảng phân bổ bộ nhớ / Phần mềm | Ghi rõ cấu trúc RAM gồm .data (23.1 KB) và .bss (16.4 KB), Flash 1.15 MB chủ yếu do BLE stack; nêu tóm tắt chuỗi boot 3 tầng của ESP32. | Trả lời trọn vẹn các câu hỏi chuẩn đầu ra của môn Hệ thống nhúng về bản đồ bộ nhớ. |

---

# BÁO CÁO TỔNG KẾT GIAI ĐOẠN 2 BÀN GIAO CHO CLAUDE
*(Thời điểm: 03/10/2026 — Ngày báo cáo giữa kỳ chính thức)*

### 1. Tiến độ và nội dung đã hoàn thành trong Giai đoạn 2
- **Mục 0: Đính chính triệt để quan điểm sai về Repeated START:**
  + Đã loại bỏ hoàn toàn nhận định sai "gặp STOP chip tự reset con trỏ về 0x00" (datasheet không ghi).
  + Đã chốt chặt bản chất: Tuân thủ đúng trình tự đọc chuẩn trong datasheet DS-000189 mục 6.3 (`S -> AD+W -> RA -> Sr -> AD+R -> DATA -> NACK -> P`); cơ chế `Sr` giữ bus luôn bận (BUSY) chống tranh chấp; phản biện thông minh khi chỉ có 1 Master.
- **Bài NC-1: Đọc hiểu chuyên sâu từng bảng của Báo cáo nộp (Tuần 5):**
  + *Bảng 4.1:* Bản chất logic Wired-AND của cực máng hở (Open-Drain), chống ngắn mạch cháy chip so với Push-Pull; cơ chế 4 User Bank vượt giới hạn địa chỉ 7-bit nhờ chìa khóa `0x7F` (`REG_BANK_SEL`); ADC1 GPIO34 độc lập với Wi-Fi (tránh xung đột ADC2); giới hạn tuyến tính 11 dB ($150\text{ mV} - 2450\text{ mV}$); phân tầng C++ sang Assembly Xtensa và ý nghĩa địa chỉ `104` chính là `0x68`.
  + *Bảng 4.2.1:* Vùng nhớ MMIO `0x3FF44000`, vai trò của từ khóa `volatile`; ưu điểm nguyên tử (Atomic) của thanh ghi `GPIO_OUT1_W1TS_REG` chống lỗi ghi đè Read-Modify-Write khi có ngắt chen giữa; bit 0 của `0x3FF44014` điều khiển LED GPIO32.
  + *Bảng 4.3 & Bảng 5.2:* Phân định API Cấu hình (setup) vs Runtime (loop 10 ms); 5 bước thanh ghi điều khiển phần cứng của SAR ADC1; tính minh bạch tuyệt đối giữa các mốc `BENCH PASS`, `HOST PASS` và `NOT_TESTED`.
- **Bài NC-2: Bản đồ bộ nhớ & Quá trình khởi động:**
  + Bóc tách chi tiết con số báo cáo: RAM $39\,628\text{ B}$ (`.dram0.data` $23\,188\text{ B}$ + `.dram0.bss` $16\,440\text{ B}$); Flash chiếm $88.4\%$ do thư viện BLE Bluedroid và Arduino framework.
  + Phân biệt biến `.data` (khởi tạo khác 0) và `.bss` (khởi tạo bằng 0); cơ chế Find & Replace của tiền xử lý `#define` (tốn 0 byte biến).
  + Chuỗi boot 3 tầng của ESP32 (ROM bootloader $\to$ GPIO0 $\to$ Bootloader tầng 2 ở `0x1000` $\to$ Partition table `0x8000` $\to$ App tại `0x10000` $\to$ FreeRTOS $\to$ `setup/loop`).

### 2. Trạng thái người học sẵn sàng cho buổi vấn đáp ngày 03/10
- Người học đã nắm vững toàn bộ các tầng câu hỏi từ trực giác, toán học, bản đồ thanh ghi, đến các câu hỏi hóc búa của giảng viên.
- Tư duy phản biện nhanh, tự tin bảo vệ các con số đo thực tế và hiểu rõ những điểm giới hạn trung thực của dự án (nút bấm/LED/đo pin chưa lắp trên breadboard, BLE trên PC chưa kiểm thử dài hạn).


---

## Đính chính 2 — Khóa phạm vi và chuẩn hóa phát ngôn kỹ thuật — 2026-10-03 10:20

1. **Ghép nối BLE với PC là `NOT_TESTED` = chưa thử lần nào:**
   - Nhật ký ghi "chưa test dài hạn" là SAI (hàm ý đã test ngắn hạn). 
   - Câu chuẩn xác: *"Firmware phát quảng bá `AirMouse-ESP32`, nhưng nhóm chưa ghép nối với máy tính."*

2. **Bỏ nhận định "Quên đổi bank thì gyro chạy ±250 °/s và tắt bộ lọc":**
   - Nội dung này không có trong báo cáo chi tiết và chưa kiểm chứng trong datasheet, tuyệt đối không sử dụng.
   - Chỉ nói đúng nội dung báo cáo: Bank 2 chứa thanh ghi cấu hình nên phải chọn bank (ghi thanh ghi `0x7F`) trước khi ghi cấu hình.

3. **Chuẩn hóa ngôn từ, loại bỏ tuyệt đối các từ phóng đại:**
   - Không dùng "tuân thủ 100 % trình tự datasheet", chỉ nói: **"làm đúng theo trình tự datasheet"**.
   - Bỏ hoàn toàn các cụm từ cảm tính / thổi phồng như "hoàn hảo", "xuất sắc 100 %".


---

## Bài mới 1 — Ràng buộc điện & Các IC nguồn — 2026-10-03 10:52
**Kết quả kiểm tra:** 3/3 đúng (Nắm rất vững vai trò MOSFET bảo vệ giữa B−/OUT−; hiểu chuẩn xác cơ chế bộ so sánh analog không có ADC của 3 IC nguồn; giải thích đúng bản chất trở kháng 50 kΩ và tụ 100 nF cho SAR ADC).

### Chỗ người học hiểu sai / vấp
- Không vấp. Người học đã nắm trúng bản chất vật lý của linh kiện ngoài.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Tách B− và OUT− trên TP4056 để làm gì? → Đáp: Cực âm cell pin vào B−, mass hệ thống lấy từ OUT−; giữa 2 chân là MOSFET bảo vệ FS8205A do DW01A điều khiển. Nếu nối tắt sẽ vô hiệu hóa chức năng bảo vệ quá xả (< 2.4 V) và ngắn mạch (Mục 3.2).
- Hỏi: TP4056, DW01A, MT3608 có ADC không? → Đáp: Cả 3 IC không có ADC, chúng dùng bộ so sánh analog với điện áp chuẩn nội để tự động ngắt/điều áp (Mục 4.1).
- Hỏi: Tụ 100 nF ở chân chia áp ADC ESP32 để làm gì? → Đáp: Cầu trở 100k/100k có trở kháng nguồn lớn (50 kΩ) làm tụ lấy mẫu bên trong ADC nạp không kịp; tụ 100 nF ngoài nạp sẵn điện tích cho ADC và lọc nhiễu cao tần (Mục 4.3.2).

### Câu hỏi người học tự hỏi mà tài liệu CHƯA có
- Đã kiểm tra file chi tiết: Cả 3 IC nguồn đều ĐÃ CÓ sẵn trong file (Mục 3.2 và Mục 4.1 có bảng thông số chi tiết). Không cần bổ sung thêm.

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx` | Khối nguồn | Nhấn mạnh việc chỉnh biến trở MT3608 về đúng 5.0 V trước khi nối ESP32. | Tránh nguy cơ cháy board DevKit do module boost cấp áp quá cao. |


---

## Bài mới 2 — Phần cứng I2C ESP32 & Chi phí phần mềm — 2026-10-03 11:03
**Kết quả kiểm tra:** Người học đã hiểu rõ qua ví dụ trực quan (Đếm 200 chu kỳ từ clock 80 MHz APB để tạo xung 400 kHz; phân biệt rạch ròi 343 µs chạy trên dây vs 100 µs chi phí phần mềm driver).

### Chỗ người học hiểu sai / vấp
- Ban đầu thấy công thức và thanh ghi hơi khó hình dung; sau khi dùng ví dụ máy gõ nhịp 80 triệu tích tắc và ví dụ bốc dỡ hàng của shipper, người học đã nắm vững hoàn toàn.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: 400 kHz tạo ra thế nào? → Đáp: Bộ đếm I2C chia từ xung ngoại vi 80 MHz APB, đếm 200 chu kỳ (100 chu kỳ mức thấp `SCL_LOW` và 100 chu kỳ mức cao `SCL_HIGH`) để tạo 1 nhịp SCL (Mục 5.3).
- Hỏi: Vì sao đo 438 µs mà lý thuyết 343 µs? → Đáp: 343 µs là thời gian tín hiệu chạy trên dây; ~100 µs dôi ra là chi phí phần mềm của driver (nạp lệnh, chờ ngắt, chép FIFO) (Mục 5.5).

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md` | Mục 5.5 | Giữ nguyên diễn giải chi phí phần mềm ~100 µs. | Rất trực quan và thuyết phục khi thầy hỏi về độ trễ thực tế. |


---

## Bài mới 3 — Chi tiết các bước thuật toán chuyển động — 2026-10-03 11:15
**Kết quả kiểm tra:** Người học đã hiểu sâu bản chất vật lý (Chiếu tư thế tham chiếu theo vector trọng lực; Auto-zero bias $\alpha = 0.002$ chống trôi nhiệt; Vùng chết 2 ngưỡng parabol 0.8–1.4 °/s giúp êm ái; Gain 2.2 và lệnh clamp kẹp trần chống tràn số đổi dấu).

### Chỗ người học hiểu sai / vấp
- Không vấp. Người học chủ động đặt câu hỏi đào sâu về bản chất toán học và hình học không gian của phép chiếu tư thế tham chiếu.

### Câu trả lời mẫu đã chốt (người học tự nói lại được)
- Hỏi: Chiếu tư thế tham chiếu để làm gì? → Đáp: Dùng vector trọng lực $\vec{g}$ làm trục dọc tuyệt đối của căn phòng. Khi người dùng cầm chuột nghiêng $45^\circ$ cho đỡ mỏi tay, lắc ngang cổ tay thì thuật toán vẫn chiếu đúng về phương ngang màn hình, chuột không bị bay chéo lên góc (Mục 9.1).
- Hỏi: Tại sao vùng chết cần 2 ngưỡng 0.8 và 1.4 °/s? → Đáp: Ngưỡng 0.8 dập tắt rung tay sinh học; khoảng đệm 0.8–1.4 dùng đường cong parabol tăng tốc mượt mà, tránh cảm giác bị giật khựng như khi dùng 1 ngưỡng cứng (Mục 9.1).
- Hỏi: Kẹp [-127, 127] để làm gì? → Đáp: Gói HID dùng `int8_t`. Nếu vung tay nhanh tính ra $dX > 127$ mà không kẹp thì tràn bit dấu thành số âm, chuột giật lùi ngược hướng tay vung (Mục 1.2).

### Đề xuất bổ sung tài liệu trình bày
| File | Mục | Bổ sung gì | Lý do |
| --- | --- | --- | --- |
| `BAO_CAO_CHI_TIET_KIEN_THUC_AIR_MOUSE.md` | Mục 9.1 | Giữ nguyên các ví dụ trực quan về góc cầm nghiêng 45° và bàn đạp ga parabol. | Giúp bảo vệ thuyết phục phần thuật toán khi thầy hỏi sâu. |


---

# TỔNG KẾT GIAI ĐOẠN 3 — BÁO CÁO BÀN GIAO CHO CLAUDE
*(Thời điểm: 03/10/2026 — Phiên ôn luyện bám sát báo cáo chi tiết)*

## 1. Đánh giá chung về người học
- **Tiếp thu bản chất:** Người học đã hiểu thấu đáo từ mô hình vật lý trực quan đến thuật toán toán học:
  + Bản chất 3 trục của gia tốc kế $(a_x, a_y, a_z)$ hoạt động như 3 chiếc lò xo đo độ giãn của vector trọng lực Trái Đất để nhận biết góc nghiêng.
  + Cơ chế bộ lọc bù chạy liên tục trong mọi chu kỳ 10 ms để sửa trôi cho Gyro với hệ số $K = 2\text{ s}^{-1}$ ($\tau = 0.5\text{ s}$), và ngắt không nghe Accel khi vung tay mạnh ($|a|$ ngoài khoảng $0.75\text{--}1.25\text{ g}$).
  + Phép chiếu tư thế tham chiếu: dùng vector trọng lực $\vec{g}$ làm trục dọc tuyệt đối của căn phòng để dù cầm nghiêng chuột $45^\circ$, lắc ngang thì con trỏ vẫn chạy ngang màn hình.
  + Cơ chế nút Clutch tương đương việc "nhấc chuột quang lên khỏi mặt bàn" và kích hoạt Tái định tâm (Recenter) khi thả tay.
  + Cơ chế nhận diện cử chỉ Flick 2 pha (tăng tốc $> 1.15\text{ g}$ rồi hãm ngược $> 0.35\text{ g}$ trong $60\text{--}450\text{ ms}$) để loại bỏ va chạm thụ động một chiều.
  + Phần cứng: đếm 200 chu kỳ clock APB 80 MHz để tạo xung I2C 400 kHz; giải mã bản chất 100 µs dôi ra khi đo thật là chi phí phần mềm của driver; bảo vệ pin qua MOSFET giữa B− và OUT−; và vai trò nạp sẵn điện tích của tụ 100 nF cho ADC.
- **Tư duy phản biện:** Đặt câu hỏi rất sắc bén: "Vector trọng lực chỉ xuống đất thì làm sao chip biết được hướng?" và "Bộ lọc bù chạy khi bấm Clutch hay chạy trong mọi trường hợp?". Cả hai câu hỏi đều đã được giải đáp thỏa đáng bằng trực quan vật lý.

---

## 2. TOP CÂU HỎI TRỌNG TÂM CẦN LƯU Ý KHI THẦY VẤN ĐÁP HÔM NAY

### 🔴 Câu 1: Bộ lọc bù hoạt động thế nào? Khi nào thì nó ngắt Accel? Accel có sửa được Yaw không?
- **Đáp:** Bộ lọc bù chạy liên tục mỗi 10 ms. Dùng Gyro quay tư thế tức thời và dùng Accel kéo từ từ sửa lỗi nghiêng với $K = 2\text{ s}^{-1}$ ($\tau = 0.5\text{ s}$). Khi gia tốc động vượt ngoài khoảng $[0.75\text{ g}, 1.25\text{ g}]$ (vung tay mạnh), bộ lọc ngắt nhánh Accel để chống méo tư thế. Gia tốc kế hoàn toàn KHÔNG sửa được góc Yaw vì vector trọng lực song song với trục xoay thẳng đứng (Mục 9.1).

### 🔴 Câu 2: Tại sao cầm nghiêng chuột 45° mà lắc ngang chuột vẫn bay ngang màn hình?
- **Đáp:** Nhờ bước "Chiếu theo tư thế tham chiếu". Thuật toán lấy vector trọng lực $\vec{g}$ (luôn cắm thẳng đứng xuống tâm Trái Đất) làm trục dọc tuyệt đối của phòng. Mọi vận tốc góc xoay của tay đều được chiếu lên mặt phẳng ngang vuông góc với trục dọc này, nên cầm nghiêng chuột vẫn bay đúng phương ngang màn hình (Mục 1.2, 9.1).

### 🟠 Câu 3: Nút Clutch để làm gì? Cử chỉ Flick vì sao phải có 2 pha?
- **Đáp:** Nút Clutch tương đương việc nhấc chuột quang lên khỏi bàn: khóa con trỏ ($dX = dY = 0$) để người dùng đưa tay về tư thế thoải mái; thả nút ra thì Tái định tâm (Recenter). Cử chỉ Flick cần 2 pha (vượt $1.15\text{ g}$ rồi hãm ngược $> 0.35\text{ g}$ trong $60\text{--}450\text{ ms}$) để phân biệt cú vẩy tay có chủ đích với va chạm thụ động một chiều (Mục 1.4, 9.2).

### 🟠 Câu 4: Vì sao tính lý thuyết đọc I2C mất 343 µs mà đo thật ra 438 µs?
- **Đáp:** 343 µs là thời gian 137 chu kỳ xung chạy trên dây ở 400 kHz. Gần 100 µs dôi ra là chi phí phần mềm của driver Wire (nạp mảng lệnh, chờ ngắt hoàn tất, sao chép dữ liệu từ FIFO ra biến) (Mục 5.5).

### 🟡 Câu 5: Tách chân B− và OUT− trên mạch sạc TP4056 để làm gì?
- **Đáp:** Nằm giữa B− (cực âm cell pin) và OUT− (mass hệ thống) là 2 MOSFET bảo vệ của chip FS8205A do DW01A điều khiển. Nếu nối tắt B− với OUT− sẽ vô hiệu hóa chức năng ngắt xả kiệt (< 2.4 V) và chống ngắn mạch (Mục 3.2).

---

## 3. ĐỀ XUẤT CHO CLAUDE BỔ SUNG VÀO KỊCH BẢN THUYẾT TRÌNH & BÁO CÁO

| Tài liệu đích | Mục | Nội dung đề xuất | Lý do kỹ thuật |
| --- | --- | --- | --- |
| `preprare4T/KICH_BAN_THUYET_TRINH_BAO_CAO_GIUA_KY.md` | Thuật toán chuyển động | Thêm giải thích hình ảnh: Cầm nghiêng $45^\circ$ nhờ chiếu trọng lực vẫn bay ngang; nút Clutch tương đương "nhấc chuột quang khỏi bàn". | Cách nói này cực kỳ cuốn hút, người nghe và ban giám khảo nắm bắt ngay lập tức. |
| `preprare4T/KICH_BAN_THUYET_TRINH_BAO_CAO_GIUA_KY.md` | Cử chỉ & Cảm biến | Nhấn mạnh điều kiện lọc Accel ($0.75\text{--}1.25\text{ g}$) và Flick 2 pha chống va đập nhầm. | Khẳng định thuật toán chặt chẽ, có tính đến rung nhiễu thực tế. |
| `BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.docx` | Bảng kết quả thực nghiệm | Giữ vững tính trung thực: BLE ghép nối PC là NOT_TESTED (chưa ghép nối lần nào), đo pin ADC1 là NOT_IMPLEMENTED. | Tuyệt đối trung thực khoa học, đúng theo Đính chính 2. |
