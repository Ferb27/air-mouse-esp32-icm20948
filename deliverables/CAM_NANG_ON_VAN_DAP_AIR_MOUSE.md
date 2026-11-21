MÔN HỌC: HỆ THỐNG NHÚNG

CẨM NANG ÔN VẤN ĐÁP

AIR MOUSE: CHUỘT BAY KHÔNG DÂY

ESP32 · ICM-20948 · BLE HID

Học đọc code, hiểu thuật toán, trả lời câu hỏi của thầy

Nội dung: cách đọc code C/C++ trong 30 phút · vòng lặp 10 ms · cảm biến và I²C · bias và hiệu chuẩn · lọc nhiễu (tightening) · quaternion · con trỏ · clutch · cử chỉ lắc · nút bấm · cuộn trang · lỗi I²C · Bluetooth HID · cài đặt · ngân hàng câu hỏi · bài tập tính tay

Tài liệu tự học cho buổi vấn đáp. Số liệu lấy từ mã nguồn bản firmware chốt và log trong thư mục dự án.

MỤC LỤC


# PHẦN 0. CÁCH DÙNG CẨM NANG NÀY


## 0.1. Mục tiêu

Cẩm nang này dành cho người chưa đọc được code nhưng cần trả lời vấn đáp về đề tài Air Mouse. Thầy thường hỏi bốn kiểu câu: (1) phần này làm gì; (2) vì sao làm như vậy chứ không làm cách khác; (3) con số này lấy từ đâu; (4) cái gì chưa làm hoặc chưa kiểm chứng. Cẩm nang được viết để bạn trả lời được cả bốn kiểu với từng chức năng.

Mỗi chủ đề trong cẩm nang đi theo cùng một thứ tự: hình dung đời thường → vấn đề cần giải → cách làm từng bước kèm con số → đọc code thật của dự án → vì sao chọn tham số → câu hỏi thầy có thể hỏi (kèm đáp án mẫu) → điều phải nói thật. Các hộp màu giúp nhận ra từng loại thông tin:

HÌNH DUNG: hộp xanh dương: hình ảnh đời thường để hiểu bản chất, đọc trước khi đọc số.

CẦN NHỚ: hộp xanh lá: ý và con số phải thuộc.

Hỏi: hộp vàng: câu hỏi thầy có thể hỏi.

Đáp: Phần trả lời mẫu viết bằng lời của bạn, ngắn gọn, đủ ý.

NÓI THẬT: hộp đỏ: chỗ chưa làm, chưa đo hoặc còn hạn chế. Thầy rất hay hỏi những chỗ này; nói thật luôn an toàn hơn nói quá.


## 0.2. Lộ trình học đề xuất (ba buổi)

| Buổi | Học phần nào | Cách kiểm tra bản thân |
|---|---|---|
| Buổi 1 | Phần 1 (đọc code C/C++), Phần 2 (bức tranh tổng thể), Phần 3 (cảm biến và I²C) | Tự vẽ lại sơ đồ một vòng 10 ms không nhìn sách; giải thích I²C trong 1 phút |
| Buổi 2 | Phần 4–9: bias, lọc nhiễu, tư thế quaternion, tính con trỏ, clutch, cử chỉ lắc | Làm bài tập tính tay ở Phần 18; giải thích “tightening” cho một người chưa học |
| Buổi 3 | Phần 10–15: nút bấm, cuộn, lỗi I²C, BLE, cấu hình; sau đó Phần 16–19 | Đọc to 20 câu hỏi ở Phần 17 và tự trả lời; nhờ người khác hỏi ngẫu nhiên |


## 0.3. Quy tắc trả lời vấn đáp

- Nói theo bốn bước: hình ảnh đời thường, cơ chế, con số, mức bằng chứng. Ví dụ: “Bộ lọc tightening giống như giảm dần âm lượng khi tín hiệu nhỏ chứ không tắt hẳn; nếu tốc độ dưới 1,4 °/s thì nhân với tỉ lệ ω/1,4; test cho 43 điểm ảnh ở 1 °/s; đây là kết quả trên máy tính (HOST_TESTED).”
- Dám nói “em chưa đo”: độ trễ BLE, dòng điện, thời lượng pin, chạy dài, nhiều người dùng đều chưa đo. Nói rõ chưa đo hợp lệ hơn nhiều so với đoán con số.
- Không dùng các từ tuyệt đối như “100 %”, “hoàn hảo”, “đã khắc phục triệt để”. Dùng “trong phép thử này”, “trên board của nhóm”, “một người thử”.
- Phân biệt ba thứ: thứ nhóm tự đo, thứ lấy từ datasheet/tài liệu, thứ chọn bằng suy luận hoặc thử. Khi thầy hỏi “con số này từ đâu”, nói đúng loại nào.
- Khi bị hỏi chỗ không biết: nói phần mình biết chắc, rồi nói “phần này em chưa nắm kỹ, em sẽ kiểm tra lại trong mã nguồn”. Đừng đoán.

## 0.4. Bốn mức bằng chứng cần nhớ

| Nhãn | Nghĩa | Ví dụ của dự án |
|---|---|---|
| HOST_TESTED | Chạy tự động trên máy tính, không có phần cứng | 35 bài test của lõi thuật toán |
| BENCH_VERIFIED | Đo trên board thật, có log | Phục hồi I²C 33 ms; hiệu chuẩn ACCEPTED; thử nghiệm 150 s |
| USER_FEEDBACK | Chính người thực hiện đề tài tự sử dụng và đánh giá chủ quan | Cuộn theo góc nghiêng giảm mỏi tay |
| NOT_TESTED | Đã viết, chưa thử trên phần cứng | Lắc Back/Forward với bản mới; đo dòng điện |


# PHẦN 1. ĐỌC CODE C/C++ TRONG 30 PHÚT

Bạn không cần biết lập trình để trả lời vấn đáp, nhưng cần đọc được vài dòng code khi thầy chỉ vào màn hình và hỏi “dòng này làm gì”. Phần này dạy đúng những thứ xuất hiện trong code của dự án, không dạy thừa.


## 1.1. Chương trình chạy trên ESP32 như thế nào

HÌNH DUNG: ESP32 giống một nhân viên làm theo tờ hướng dẫn. Hàm setup() là các việc làm đúng một lần khi vừa đến chỗ làm (mở máy, kiểm tra dụng cụ). Hàm loop() là danh sách việc làm đi làm lại mãi mãi: hết danh sách thì quay lại dòng đầu. Cả firmware Air Mouse chỉ là hai hàm này gọi các hàm khác.

Đoạn mã 1.1. Khung của firmware.ino

```
void setup() {
    app_boot();        // chạy 1 lần: mở serial, khởi tạo cảm biến, hiệu chuẩn, bật
      Bluetooth
}

void loop() {
    ...                // chạy lặp vô hạn; dự án đặt nhịp 100 lần/giây (mỗi 10 ms)
}
```


## 1.2. Biến và kiểu dữ liệu

Biến là cái hộp có tên để chứa một con số. Kiểu cho biết hộp chứa loại số nào và to bao nhiêu. Code của dự án dùng đúng các kiểu sau:

| Kiểu | Chứa gì | Ví dụ trong dự án và lý do dùng |
|---|---|---|
| float | Số thực (có phần lẻ), 4 byte | gain_x = 0.3f (chữ f báo đây là float); gia tốc 0,988 g; tốc độ xoay −1,52 °/s |
| int | Số nguyên thường | Biến đếm trong vòng for |
| bool | Chỉ true hoặc false | clutch_pressed (nút Mode có đang giữ không) |
| int8_t | Số nguyên 8 bit có dấu: −128…127 | delta_x, delta_y, wheel: gói chuột HID chỉ có 1 byte cho mỗi giá trị nên kẹp trong ±127 |
| uint8_t | Số nguyên 8 bit không dấu: 0…255 | Giá trị cờ như flick_enable (0/1), chỉ số hành động nút |
| uint16_t | Không dấu 16 bit: 0…65535 | Bộ đếm mẫu đứng yên s_rest_counter |
| int16_t | Có dấu 16 bit: −32768…32767 | Số đọc thô của cảm biến (cảm biến trả số 16 bit có dấu) |
| uint32_t | Không dấu 32 bit: 0…4,29 tỉ | Đồng hồ now_ms (mili-giây từ lúc bật nguồn); tràn sau khoảng 49,7 ngày |

CẦN NHỚ: int8_t nghĩa là “integer 8 bit”. Chữ u đầu (uint) nghĩa là unsigned, không có số âm. Số đứng sau là số bit: 8, 16, 32.


## 1.3. Các ký hiệu hay gặp

| Ký hiệu | Ý nghĩa | Ví dụ trong code |
|---|---|---|
| = | Gán (bỏ giá trị bên phải vào biến bên trái) | s_bias_x = bx; |
| ==  != | So sánh bằng, khác (trả về đúng/sai) | if (raw != d->last_raw) |
| <  >  <=  >= | So sánh lớn nhỏ | if (a >= threshold) |
| &&  //  ! | VÀ, HOẶC, PHỦ ĐỊNH | press = mode_down && !s->last_down; (đang nhấn VÀ lần trước không nhấn: nghĩa là vừa nhấn xuống) |
| +=  ++ | Cộng dồn; tăng 1 | s_rest_counter++; |
| % | Chia lấy phần dư | (head + 1) % PH_LEN (quay vòng chỉ số trong vòng đệm) |
| điều_kiện ? A : B | Nếu đúng lấy A, sai lấy B | return yaw_dps > 0 ? FLICK_LEFT : FLICK_RIGHT; |
| (int32_t)x | Ép kiểu: đổi x sang kiểu khác | (int32_t)roundf(fx) đổi số thực đã làm tròn sang số nguyên |
| // | Chú thích: máy bỏ qua, người đọc | Rất nhiều trong code của dự án, đọc để hiểu ý tác giả |
| fabsf sqrtf roundf asinf | Trị tuyệt đối, căn bậc hai, làm tròn, arcsin (cho số float) | sqrtf(ax*ax + ay*ay + az*az) là độ lớn vector gia tốc |


## 1.4. Cấu trúc điều khiển

Đoạn mã 1.2. Ba cấu trúc gặp nhiều nhất

```
if (điều_kiện) {            // nếu đúng thì làm khối này
    ...
} else {                    // không thì làm khối này
    ...
}

for (int i = 0; i < 6; ++i) {   // lặp 6 lần với i = 0,1,2,3,4,5
    ...
}

switch (state) {            // chọn nhánh theo giá trị của state
    case SM_IDLE:   ...  break;
    case SM_PRESS1: ...  break;
}
```

switch thay cho một chuỗi if dài khi phải rẽ nhánh theo trạng thái. Chữ break có nghĩa “xong nhánh này, nhảy ra ngoài”.


## 1.5. Hàm

Hàm là một đoạn việc có tên, có thể gọi nhiều lần. Dạng tổng quát: kiểu_trả_về tên_hàm(tham_số) { thân hàm }. Kiểu void nghĩa là hàm không trả gì.

Đoạn mã 1.3. Một hàm hoàn chỉnh của dự án

```
static float apply_tightening(float val, float threshold) {   // nhận 2 số, trả 1 số
      float
    float a = fabsf(val);                // a = trị tuyệt đối của val
    if (a >= threshold) return val;      // đủ lớn: trả nguyên giá trị
    return val * (a / threshold);        // nhỏ: thu nhỏ dần
}
```

HÌNH DUNG: Hàm giống một cái máy ép nước: bỏ quả vào (tham số), máy chạy, nước ép chảy ra (giá trị trả về). apply_tightening(1.0, 1.4) trả về 0,714.


## 1.6. Biến static: bộ nhớ của thuật toán

Một biến bình thường trong hàm sẽ mất sau mỗi lần hàm chạy xong. Biến static thì giữ giá trị từ lần gọi này sang lần gọi sau. Rất nhiều biến trong motion_pipeline.cpp là static (tên bắt đầu bằng s_) và chính chúng là “trí nhớ” của bộ lọc:

Đoạn mã 1.4. Biến static trong motion_pipeline.cpp

```
static float s_bias_x = 0.0f;       // bias con quay đã đo: nhớ mãi cho đến khi đo lại
static uint16_t s_rest_counter = 0; // đã đứng yên liên tục bao nhiêu mẫu
static quat_t s_q = {1,0,0,0};      // tư thế hiện tại của board (quaternion)
```

CẦN NHỚ: Khi thầy hỏi “thuật toán nhớ gì giữa hai lần đọc cảm biến”, trả lời: bias, bộ đếm đứng yên, quaternion tư thế, phần dư làm tròn, và các biến trạng thái nút. Tất cả là biến static.


## 1.7. Gói dữ liệu struct

struct gom nhiều biến thành một gói có tên. Gói đo của cảm biến:

Đoạn mã 1.5. struct imu_data_t

```
typedef struct {
    float ax, ay, az;     // gia tốc 3 trục, đơn vị g
    float gx, gy, gz;     // tốc độ xoay 3 trục, đơn vị độ/giây
} imu_data_t;

imu_data_t d;             // tạo một gói tên d
d.ax = 0.01f;             // dấu chấm: lấy thành phần của gói
ptr->ax                   // mũi tên: lấy thành phần khi có con trỏ tới gói
```


## 1.8. Con trỏ * và địa chỉ &

HÌNH DUNG: Mỗi biến nằm ở một “số nhà” trong bộ nhớ. Địa chỉ &x là số nhà của x. Con trỏ *p là tờ giấy ghi số nhà. Muốn nhờ hàm “ghi kết quả vào nhà của tôi”, bạn đưa cho hàm số nhà (con trỏ) thay vì đưa bản sao.

Đoạn mã 1.6. Truyền con trỏ

```
bool app_imu_read(imu_data_t* d) {        // d là con trỏ tới một gói imu_data_t
    if (!imu_readData(d)) return false;   // đọc và ghi thẳng vào gói của người gọi
    ...
    return true;
}

imu_data_t imu_data = {};
bool read_ok = app_imu_read(&imu_data);   // đưa địa chỉ của imu_data cho hàm
```

Nhờ cách này một hàm có thể “trả về” nhiều giá trị: ví dụ motion_getBias(&bx, &by, &bz) ghi ba số vào ba biến của người gọi. Từ khóa const đứng trước con trỏ (const air_config_t* cfg) nghĩa là hàm chỉ được đọc, không được sửa.


## 1.9. File .h, file .cpp, #define, #include

- File .h (header) là mục lục: liệt kê tên hàm và kiểu dữ liệu. File .cpp là nội dung thật. Muốn biết một mô-đun làm gì, đọc .h trước (có chú thích ở đầu), rồi mới đọc .cpp.
- #include "abc.h" nghĩa là “chèn mục lục abc.h vào đây”.
- #define SM_TAP_MAX_MS 250 đặt một hằng số có tên: mọi chỗ ghi SM_TAP_MAX_MS được thay bằng 250. Dùng để đổi thông số ở một nơi.
- Tên có tiền tố app_ là lớp ứng dụng (cần Arduino/ESP32). Tên không có tiền tố là lõi thuần, chạy được trên máy tính.

## 1.10. Hai mẹo mà code dự án dùng nhiều


### Mẹo 1. So sánh thời gian an toàn khi đồng hồ tràn

Đoạn mã 1.7. Tính khoảng thời gian

```
if ((uint32_t)(now_ms - s->t_ms) <= SM_TAP_MAX_MS) { ... }   // đã trôi qua ≤ 250 ms
      chưa?
```

Đồng hồ now_ms là số 32 bit nên đến khoảng 49,7 ngày thì quay về 0. Nếu viết now_ms < t0 + 250 thì sai khi đồng hồ quay vòng. Phép trừ số không dấu cho kết quả đúng cả khi đồng hồ tràn, vì vậy code luôn viết now - trước rồi mới so sánh. Đây là chi tiết hay gây ấn tượng nếu bạn giải thích được.


### Mẹo 2. “Cạnh nhấn” và “cạnh nhả”

Đoạn mã 1.8. Phát hiện cạnh

```
bool press   = mode_down && !s->last_down;   // trước đó không nhấn, bây giờ nhấn  →
      vừa nhấn xuống
bool release = !mode_down && s->last_down;   // trước đó nhấn, bây giờ không       →
      vừa nhả ra
```

Muốn biết nút vừa được nhấn, phải so trạng thái hiện tại với trạng thái của nhịp trước (biến last_down). Đây là cách mọi thao tác nhấn/nhả/nhấn đúp trong dự án được nhận ra.


## 1.11. Tự kiểm tra

- int8_t chứa được dải nào, và vì sao con trỏ chuột dùng nó?
- Biến static khác biến thường chỗ nào? Cho ví dụ trong dự án.
- a && !b nghĩa là gì bằng lời?
- Vì sao viết now - t0 thay vì now < t0 + X?
Đáp án: (1) −128 đến 127; gói HID chuột dành 1 byte cho mỗi trục; code kẹp ±127. (2) Biến static giữ giá trị giữa các lần gọi, ví dụ s_bias_x. (3) “a đúng và b sai”. (4) Để đúng cả khi đồng hồ 32 bit tràn sau 49,7 ngày.


# PHẦN 2. BỨC TRANH TỔNG THỂ: MỘT VÒNG 10 MS

HÌNH DUNG: Hãy tưởng tượng một nhân viên bảo vệ cứ mỗi 10 mili-giây (100 lần mỗi giây) đi qua đúng 12 trạm theo thứ tự: nhận lệnh, hỏi cảm biến, kiểm tra cảm biến còn khỏe không, đọc nút, quyết định con trỏ đi đâu, gửi tin cho máy tính, ghi sổ. Xong lại quay về trạm đầu. Mọi chức năng của Air Mouse là một trạm trên vòng đi này.


## 2.1. Mười hai trạm trong loop()

| # | Việc làm | Hàm/mô-đun | Kể ở phần |
|---|---|---|---|
| 1 | Đọc lệnh gõ từ máy tính qua cổng serial (@GET, @SET, c…) | app_serial_poll | Phần 14 |
| 2 | Chưa đủ 10 ms thì bỏ qua, đủ thì chạy tiếp | app_loop_due | 2.2 |
| 3 | Đọc 6 số từ cảm biến, xoay trục cho đúng hướng | app_imu_read | Phần 3 |
| 4 | Kiểm tra cảm biến còn sống không; hỏng thì phục hồi | app_imu_health_step | Phần 12 |
| 5 | Nằm yên trên bàn mà bias sai thì tự đo lại | app_imu_self_heal | Phần 4 |
| 6 | Đọc 3 nút, chống dội, gán chức năng | app_buttons_read, bm_apply | Phần 10 |
| 7 | Nhận ra “chạm-nhấn-giữ” để vào chế độ cuộn | app_scroll_update | Phần 11 |
| 8 | Tính độ dời con trỏ và cử chỉ lắc | motion_process | Phần 5–9 |
| 9 | Đảo chiều X/Y theo cài đặt; nếu đang cuộn đổi góc nghiêng thành con lăn | app_scroll_convert | Phần 11 |
| 10 | Bộ chặn click: xóa cú giật trước khi nhấn | app_buttons_filter_motion | Phần 10 |
| 11 | Gửi gói chuột Bluetooth | app_ble_dispatch | Phần 13 |
| 12 | Mỗi giây in một dòng [STATUS] | app_status_report | Phần 15 |


## 2.2. Vì sao đúng 100 Hz, và vì sao không dùng delay()

100 Hz là tốc độ cập nhật đủ mượt cho con trỏ (mắt người thấy mượt từ khoảng 60 Hz), vừa đủ cho bộ lọc tư thế, và vừa khít với cảm biến lấy mẫu 102,27 Hz. Con số này là quyết định thiết kế ban đầu của nhóm; không có nguồn ngoài quy định.

Hàm delay(10) sẽ làm ESP32 “đứng đợi” 10 ms, trong lúc đó không phục vụ được Bluetooth hay cổng serial. Thay vào đó dự án hỏi đồng hồ micros() mỗi lần loop() được gọi: “đã đủ 10 000 µs kể từ lần chạy trước chưa?”. Chưa đủ thì thoát ngay để còn việc khác.

Đoạn mã 2.1. Nhịp 100 Hz (app_timing.cpp)

```
bool app_loop_due(uint32_t* now_ms) {
    uint32_t now_us = micros();
    if (now_us - s_last_loop_us < APP_LOOP_PERIOD_US) {   // chưa đủ 10 000 µs
        return false;                                     // → loop() thoát ngay
    }
    s_last_loop_us = now_us;                              // đủ rồi: ghi lại mốc, cho
      chạy
    *now_ms = millis();
    return true;
}
```


## 2.3. Hai lớp của mã nguồn

- Lõi thuần: thuật toán, không gọi Arduino, chạy được và test được trên máy tính. Nhờ đó có 35 bài test tự động.
- Lớp ứng dụng (các file app_*) nối lõi với phần cứng (GPIO, I²C, Bluetooth, flash). Không test tự động được.
Hỏi: Vì sao nhóm tách mã thành hai lớp?

Đáp: Để kiểm thử thuật toán trên máy tính mà không cần board. Lõi thuần chỉ dùng C/C++ chuẩn nên biên dịch bằng g++; lớp app_ mới gọi Arduino. Nhờ vậy sửa thuật toán có thể chạy lại 35 bài test trong vài giây.

Hỏi: Điểm đặc biệt trong thiết kế vòng lặp là gì?

Đáp: Khi cảm biến tạm hỏng thì con trỏ ngừng di chuyển nhưng nút bấm, Bluetooth và log vẫn chạy. Bản cũ dừng cả vòng lặp khi cảm biến hỏng nên nút cũng không bấm được.


# PHẦN 3. CẢM BIẾN, I²C VÀ ĐỌC DỮ LIỆU


## 3.1. Cảm biến đo cái gì

HÌNH DUNG: Gia tốc kế giống cảm giác trọng lượng khi bạn ngồi trong thang máy: nằm yên trên bàn nó vẫn báo 1 g hướng lên (lực của mặt bàn đỡ chống lại trọng lực). Nó cho biết hướng “xuống” ở đâu. Con quay (gyroscope) giống đồng hồ đo tốc độ vòng quay: nó cho biết đang quay nhanh bao nhiêu độ mỗi giây quanh từng trục, không cho biết góc hiện tại.

| Cảm biến | Đơn vị | Dùng để làm gì trong dự án |
|---|---|---|
| Con quay 3 trục (gx, gy, gz) | độ/giây (°/s) | Nguồn chính điều khiển con trỏ: xoay nhanh thì con trỏ chạy nhanh; cử chỉ lắc |
| Gia tốc kế 3 trục (ax, ay, az) | g (1 g ≈ 9,8 m/s²) | Biết hướng trọng lực, tức độ nghiêng của board; phát hiện đứng yên; sửa trôi của con quay |
| Từ kế AK09916 (có trong chip) | — | Không dùng trong firmware hiện tại |


## 3.2. I²C: hai dây nói chuyện

HÌNH DUNG: I²C giống gọi điện thoại trong một khu phố chỉ có hai đường dây chung. Một dây là SCL (nhịp: tiếng “tích tắc” của người chủ trì cuộc gọi), một dây là SDA (nội dung nói). ESP32 là master (người gọi) và chỉ có cảm biến là slave (người nghe) ở “số nhà” 0x68. Master gọi số nhà, hỏi “thanh ghi số mấy?”, rồi slave đọc dữ liệu ra từng byte.

Một lần đọc 12 byte gồm các bước sau, tất cả do phần cứng I²C của ESP32 thực hiện:

- START: master kéo SDA xuống khi SCL đang cao, báo hiệu bắt đầu.
- Gửi địa chỉ 7 bit 0x68 kèm bit W (ghi). Cảm biến trả ACK (xác nhận) bằng cách kéo SDA xuống một xung. Không có ACK nghĩa là cảm biến không nghe thấy.
- Gửi số thanh ghi muốn đọc (0x2D, nơi bắt đầu dữ liệu gia tốc).
- Repeated START rồi gửi địa chỉ kèm bit R (đọc).
- Cảm biến gửi liên tiếp 12 byte; master ACK mỗi byte, byte cuối trả NACK để dừng.
- STOP: master thả SDA lên khi SCL đang cao.
CẦN NHỚ: Bus I²C: tốc độ 400 kHz (chế độ Fast), địa chỉ cảm biến 0x68 vì chân AD0 nối GND, dây SDA = GPIO21, SCL = GPIO22. Đọc 12 byte mất khoảng 438 µs (số đo của dự án), còn nhịp là 10 000 µs nên bus rảnh hơn 95 % thời gian.


### Trở kéo lên (pull-up)

Hai dây SDA và SCL là kiểu open-drain: thiết bị chỉ có thể kéo xuống 0, không tự đẩy lên 1. Mức 1 do điện trở kéo lên nối với 3,3 V tạo ra. Module WCMCU-20948 đã có sẵn điện trở 10 kΩ nên dự án không lắp thêm.


## 3.3. Thanh ghi và cấu hình cảm biến

Cảm biến có hàng trăm thanh ghi (ô nhớ nhỏ có địa chỉ). Ghi vào thanh ghi là ra lệnh, đọc thanh ghi là lấy dữ liệu. ICM-20948 chia thanh ghi làm 4 “bank” (ngăn kéo); muốn dùng ngăn nào phải ghi số ngăn vào thanh ghi 0x7F trước.

| Thanh ghi | Bank | Giá trị | Ý nghĩa |
|---|---|---|---|
| WHO_AM_I (0x00) | 0 | 0xEA | “Chứng minh thư” của chip: đọc ra 0xEA là đúng ICM-20948 |
| PWR_MGMT_1 (0x06) | 0 | 0x01 | Đánh thức chip (thoát chế độ ngủ), chọn xung nhịp tự động |
| GYRO_SMPLRT_DIV (0x00) | 2 | 10 | Tốc độ lấy mẫu = 1125 / (1 + 10) = 102,27 Hz |
| GYRO_CONFIG_1 (0x01) | 2 | 0x1B | Dải đo ±500 °/s, bộ lọc số 51,2 Hz |
| ACCEL_CONFIG (0x14) | 2 | 0x1B | Dải đo ±4 g, bộ lọc số 50,4 Hz |


### Số thô đổi ra đơn vị thật

Cảm biến trả số nguyên 16 bit có dấu (từ −32768 đến 32767). Dải đo càng rộng thì mỗi “nấc” càng thô. Vì 32768 nấc ứng với 500 °/s nên mỗi nấc là 500/32768 = 1/65,5 °/s, nghĩa là chia số thô cho 65,5 để ra °/s. Tương tự 32768 nấc ứng với 4 g nên chia cho 8192 để ra g.

ω [°/s] = số thô / 65,5        a [g] = số thô / 8192

Đoạn mã 3.1. Đọc và đổi đơn vị (icm20948_driver.cpp)

```
// Đọc 12 byte liên tiếp: 6 byte gia tốc rồi 6 byte con quay (mỗi giá trị 2 byte: byte
      cao trước)
uint8_t raw[12];
imu_readBurst(0, REG_ACCEL_XOUT_H, raw, 12);

int16_t raw_ax = (int16_t)(((uint16_t)raw[0] << 8) | raw[1]);   // ghép 2 byte thành
      số 16 bit
...
data->ax = (float)raw_ax / 8192.0f;      // ra đơn vị g
data->gx = (float)raw_gx / 65.5f;        // ra đơn vị độ/giây
```

Giải thích dòng ghép byte: raw[0] << 8 dịch byte cao sang trái 8 bit (nhân 256), rồi | raw[1] ghép byte thấp vào. Ví dụ byte cao 0x20 và byte thấp 0x00 cho 0x2000 = 8192, tức đúng 1 g.


### Vì sao đọc 12 byte một lần

Sáu giá trị nằm liền nhau trong bộ nhớ cảm biến nên đọc một lần liên tục (burst). Việc này nhanh hơn đọc 6 lần riêng và đảm bảo cả sáu giá trị thuộc cùng một thời điểm; nếu đọc rời, giữa các lần đọc cảm biến có thể cập nhật giá trị mới.


### Quy trình khởi tạo imu_init()

- Gọi Wire.end() rồi Wire.begin(SDA, SCL, 400000): khởi động lại bộ I²C của ESP32 ở 400 kHz; đặt thời gian chờ 10 ms.
- Đọc WHO_AM_I: không bằng 0xEA thì dừng và báo lỗi.
- Ghi PWR_MGMT_1 = 0x01 để đánh thức.
- Ghi cấu hình tốc độ lấy mẫu, dải đo, bộ lọc cho con quay và gia tốc kế.
- Đọc lại từng thanh ghi vừa ghi và so với giá trị mong muốn. Cả 7 giá trị khớp thì mới coi là khởi tạo thành công (init_success).

## 3.4. Xoay trục cho đúng hướng

Khi cầm như điều khiển TV (cáp USB về phía cổ tay, mũi hướng màn hình, mặt chip hướng lên), trục X của cảm biến chỉ sang trái và trục Y chỉ về phía sau; còn thuật toán muốn X hướng về phía trước và Y sang phải. Một phép hoán đổi áp cho cả gia tốc và con quay:

Đoạn mã 3.2. Xoay trục (app_imu.cpp)

```
d->ax = d->ay;   d->ay = -ax;      // x_mới = y_cũ ;  y_mới = - x_cũ
d->gx = d->gy;   d->gy = -gx;
```

CẦN NHỚ: Phép xoay trục được đo bằng 11 cử động chuẩn rồi phát lại dữ liệu qua thuật toán, không phải đoán. Trước khi sửa, quay phải làm con trỏ chạy sang trái (dX = −2036); sau khi sửa dX = +2036.


## 3.5. Hỏi đáp về cảm biến

Hỏi: Vì sao chọn dải ±500 °/s và ±4 g?

Đáp: Chọn từ đầu dự án theo suy luận: cổ tay xoay nhanh có thể vượt 250 °/s nên không dùng ±250; cử chỉ lắc cần đo gia tốc 1,15 g cộng 1 g trọng lực nên ±2 g dễ bị chạm trần. Em chưa có phép đo tốc độ xoay cổ tay lớn nhất nên đây là lập luận, chưa phải số đo.

Hỏi: Bộ lọc số 51,2 Hz trong cảm biến để làm gì?

Đáp: Là bộ lọc thông thấp của chính chip, cắt bớt nhiễu tần số cao trước khi lấy mẫu. Datasheet không công bố độ trễ của nó. Lý do chọn mức này có từ firmware ban đầu.

Hỏi: ESP32 chạy 240 MHz còn I²C chạy 400 kHz, có cần đồng bộ hai tốc độ không?

Đáp: Không cần. Xung SCL do bộ I²C phần cứng của ESP32 tự tạo ra bằng cách chia xung nhịp ngoại vi, không phụ thuộc CPU đang chạy nhanh hay chậm. CPU chỉ ra lệnh đọc 12 byte rồi chờ; việc đọc tốn khoảng 438 µs trong khi nhịp là 10 ms.

Hỏi: Vì sao I²C mà không dùng SPI?

Đáp: Module chỉ có sẵn giao diện I²C dễ đấu nối (hai dây) và tốc độ 400 kHz đã đủ: 12 byte mất khoảng 0,44 ms so với nhịp 10 ms. Chân NCS nối 3,3 V để chọn I²C (kéo NCS xuống sẽ chọn SPI).

Hỏi: WHO_AM_I dùng để làm gì?

Đáp: Kiểm tra chip trả lời đúng và đúng loại: đọc thanh ghi 0x00 phải ra 0xEA. Nếu đọc ra 0 hoặc giá trị khác thì dây nối sai, cảm biến chưa cấp nguồn hoặc nhầm chip.

Hỏi: Tốc độ lấy mẫu của cảm biến là 102,27 Hz, vòng lặp là 100 Hz, có lệch nhau không?

Đáp: Có lệch nhẹ: cảm biến nhanh hơn 2,27 %, nên khoảng mỗi 0,44 giây cảm biến có một mẫu mới mà vòng lặp chưa kịp đọc nên bỏ một mẫu. Ảnh hưởng không đáng kể và đã ghi trong hạn chế.

Hỏi: Vì sao phải xoay trục?

Đáp: Cảm biến gắn trên board theo một hướng, còn thuật toán giả định X là phía trước, Y là bên phải. Em đo bằng 11 cử động chuẩn thì thấy trục cảm biến lệch, nên hoán đổi X, Y và đảo dấu một trục trong app_imu_read.


# PHẦN 4. BIAS, HIỆU CHUẨN VÀ PHÁT HIỆN ĐỨNG YÊN


## 4.1. Bias là gì

HÌNH DUNG: Cái cân bị lệch số 0: chưa đặt gì lên mà kim đã chỉ 1,5 kg. Muốn cân đúng phải trừ đi 1,5 kg ở mọi lần cân. Con quay cũng vậy: nằm yên trên bàn mà nó vẫn báo xoay một ít. Con số lệch đó là bias (độ lệch không). Của board nhóm khoảng −1,5 / +0,5 / +0,4 °/s trên ba trục.

Nếu không trừ bias, con trỏ sẽ trôi dần dù tay không động. Nếu trừ sai (đo bias lúc đang cầm hoặc đang rung), con trỏ trôi liên tục và không tự hết. Đây là lỗi nhóm gặp thật ngày 08/10: bật nguồn lúc đang cầm, bias đo sai khoảng 3 °/s, bộ khóa đứng yên không bao giờ bật được.


## 4.2. Hiệu chuẩn lúc bật nguồn, có kiểm tra

Mỗi lần thử: lấy 200 mẫu cách nhau 10 ms (2 s), tính trung bình từng trục (đó là bias) và độ lệch chuẩn sd (đo mức “rung” của dữ liệu), đồng thời chia cửa sổ làm hai nửa để xem trung bình có dịch chuyển không. Kết quả được chấp nhận khi cả bốn điều kiện thỏa:

- Đọc thành công ít nhất 90 % số mẫu (≥ 180/200).
- Độ lớn gia tốc trung bình nằm trong 1 ± 0,15 g: cảm biến “chết” trả 0 g bị loại.
- sd mỗi trục nằm trong [0,005 ; 0,35] °/s: sd ≈ 0 nghĩa là cảm biến đóng băng; sd lớn nghĩa là đang bị rung hoặc cầm.
- Trung bình hai nửa cửa sổ lệch nhau không quá 0,25 °/s mỗi trục: nếu có thì board đang di chuyển trong lúc đo.
Không đạt thì thử lại, tối đa 5 lần. Cả 5 lần đều hỏng lúc bật nguồn thì vẫn dùng lần cuối nhưng in cảnh báo, và cơ chế tự đo lại (mục 4.4) sẽ sửa sau.

Đoạn mã 4.1. Điều kiện chấp nhận hiệu chuẩn (bias_checks.cpp)

```
bool motion_calibration_still(const float sd[3], const float mean_a[3], const float
      mean_b[3]) {
    for (int k = 0; k < 3; ++k) {                       // lặp qua 3 trục
        if (!(sd[k] >= 0.005f)) return false;           // sd quá nhỏ = cảm biến đóng
      băng
        if (!(sd[k] <= 0.35f))  return false;           // sd quá lớn = đang rung/cầm
        if (!(fabsf(mean_a[k] - mean_b[k]) <= 0.25f)) return false;  // trung bình hai
      nửa lệch nhau
    }
    return true;                                        // qua hết cả ba trục: chấp
      nhận
}
```

Đọc dòng if (!(sd[k] >= 0.005f)) return false;: “nếu không phải (sd lớn hơn hoặc bằng 0,005) thì trả về sai ngay”. Cách viết !(a >= b) thay vì a < b còn có tác dụng bắt cả trường hợp a là NaN (số không hợp lệ), vì mọi phép so sánh với NaN đều cho sai.

Dòng log thật của bản chốt: Attempt 1: 2200 ms, 200 polls, |a| = 0.989 g, sd = 0.08/0.08/0.09 dps, half-mean diff = 0.01/0.01/0.01 dps -> ACCEPTED, bias −1,52 / +0,53 / +0,38 °/s.


## 4.3. Phát hiện đứng yên và tự chỉnh bias chậm

Trong motion_process(), mỗi mẫu được so với hai điều kiện: (a) tốc độ xoay sau khi trừ bias nhỏ hơn 0,4 °/s và (b) độ lớn gia tốc lệch khỏi 1 g dưới 0,08 g. Hai điều kiện đúng liên tục 30 mẫu (≈ 0,3 s) thì board được coi là đứng yên: đầu ra bị khóa về 0 và phần dư làm tròn bị xóa. Nhờ vậy khi tay buông, con trỏ không thể trôi.

Khi đã đứng yên 150 mẫu liên tiếp (1,5 s), bias được chỉnh chậm theo sai số còn lại:

bias ← bias + 0,002 · (ω − bias)

Hệ số 0,002 rất nhỏ nên bias chỉ nhích rất chậm; thời gian chờ 1,5 s để chuyển động rất chậm của tay không bị “hút” thành bias (test N4: nửa sau của chuyển động còn 95 % so với nửa đầu).

CẦN NHỚ: Ngưỡng 0,4 °/s chọn theo nhiễu của con quay: độ lệch chuẩn đo được khoảng 0,09 °/s, nên 0,4 °/s ≈ 4σ. Đây là tự suy luận từ số đo của dự án, không có nguồn ngoài. Con số 1,5 s trùng thời gian nghỉ tối thiểu mà thư viện VQF dùng.


## 4.4. Tự đo lại khi nằm yên trên bề mặt

HÌNH DUNG: Người cầm giữ yên một cái ly: tay vẫn run rất nhẹ. Cái ly đặt trên bàn thì không run chút nào. Nhìn độ “run” của gia tốc kế là biết board đang nằm bàn hay đang trên tay.

Cứ mỗi cửa sổ 100 mẫu (1 s), hàm motion_surface_rest_bias_bad() kiểm tra các điều kiện: sd gyro ≤ 0,35 °/s; sd gia tốc kế ≤ 0,005 g mỗi trục; độ lớn gia tốc trong 1 ± 0,08 g; và trung bình gyro lệch khỏi bias đang dùng hơn 0,5 °/s. Ba cửa sổ liên tiếp đều thỏa thì firmware đo lại bias một lần (có kiểm tra như mục 4.2) và in [HEAL].

| Trạng thái | sd của gia tốc kế (đo thật) | Kết luận |
|---|---|---|
| Nằm trên bàn | ≈ 0,002 g | dưới ngưỡng 0,005 g: coi là nằm bàn |
| Tay giữ phẳng vững nhất | ≈ 0,010 g (trục X) | trên ngưỡng: không bị coi là nằm bàn |

Ngưỡng 0,005 g đặt giữa hai mức đó: đủ chặt để bàn tay giữ yên không bị coi là “nằm bàn” (nếu không, chuyển động chậm của tay bị nuốt, đúng điều thầy lo ở giữa kỳ), đủ lỏng để bàn có rung nhẹ vẫn nhận ra. Lúc đầu nhóm đặt 0,008 g, thấy gần mức 0,010 g của tay quá nên siết xuống 0,005 g.

Bằng chứng (14/10): bật nguồn khi đang lắc, bias sai +13,27 °/s; đặt xuống bàn khoảng 5 s sau có dòng [HEAL] Resting on a surface but bias is off ... recalibrating, bias về −1,48 / +0,57 / +0,35 °/s; 85 trong 87 dòng [STATUS] sau đó có Stat: 1 và không có chuyển động.

Hỏi: Vì sao phải kiểm tra điều kiện trước khi chấp nhận bias?

Đáp: Vì bias đo lúc đang cầm hoặc đang chạm sẽ sai và, do bộ khóa đứng yên cần mọi trục dưới 0,4 °/s, bias sai quá khoảng 1 °/s sẽ làm bộ khóa không bao giờ bật và bộ tự chỉnh bias (chỉ chạy khi đã khóa) cũng không chạy: con trỏ trôi mãi. Đây là lỗi thật nhóm đã gặp ngày 08/10 nên mới thêm kiểm tra.

Hỏi: Bias có trôi theo nhiệt độ không? Nhóm có đo không?

Đáp: Nhóm đo trôi bias hai lần, mỗi lần 12 phút: lệch tối đa 0,029 và 0,057 °/s, thấp hơn nhiều ngưỡng rủi ro 0,2–0,3 °/s. Nhưng chip chỉ ấm lên 0,1–0,2 °C và chưa có ca khởi động nguội thật sự, nên em không khẳng định gì về dải nhiệt độ rộng.

Hỏi: Vì sao ngưỡng sd gia tốc kế là 0,005 g?

Đáp: Lấy từ số đo: nằm bàn 0,002 g, tay giữ vững nhất 0,010 g. Ngưỡng đặt giữa hai mức để chỉ nhận ra bề mặt bàn mà không nuốt chuyển động chậm của tay.

NÓI THẬT: Có một “vùng xám” đã biết: bias dư khoảng 0,2–0,5 °/s làm bộ khóa đứng yên khó bật nhưng chưa đủ 0,5 °/s để cơ chế tự đo lại kích hoạt. Test N7 ghi lại: bias dư 0,3 °/s trên yaw gây trôi khoảng 21 điểm ảnh/10 s và không tự phục hồi. Nhóm đề xuất hạ ngưỡng 0,5 xuống khoảng 0,2 °/s nhưng chưa làm và chưa thử.


# PHẦN 5. LỌC NHIỄU: “TIGHTENING” VÀ CHỐNG TRÔI

Đây là phần thầy hỏi ở buổi giữa kỳ nên phải nắm thật chắc: “bộ lọc nhiễu có nuốt cả chuyển động nhỏ có chủ ý không?”


## 5.1. Hình dung: núm âm lượng

HÌNH DUNG: Bạn nghe nhạc có tiếng ù nhỏ. Cách thô là đặt “cổng tắt tiếng”: dưới một mức nào đó thì tắt hẳn. Tiếng ù hết, nhưng tiếng thì thầm có ích cũng mất. Cách tinh (tightening) là vặn nhỏ dần: tín hiệu càng yếu càng bị giảm nhiều, nhưng không bao giờ bị cắt thành 0. Chuyển động có chủ ý dù chậm vẫn còn lại một phần.


## 5.2. Bản cũ sai ở đâu

- Vùng chết cứng 0,8/1,4 °/s: mọi tốc độ nhỏ hơn bị ép về 0.
- Khóa đứng yên ở 1,2 °/s: chuyển động tay chậm hơn mức này bị coi là đứng yên.
- Làm tròn mỗi mẫu bỏ phần lẻ: một mẫu tính ra 0,3 điểm ảnh bị làm tròn thành 0 và mất.
Hậu quả: xoay 0,5 °/s và 1,0 °/s đều cho 0 điểm ảnh. Thầy lo đúng; nhóm sửa cả ba nguyên nhân.


## 5.3. Công thức tightening

f(ω) = ω                  nếu |ω| ≥ T

f(ω) = ω · |ω| / T        nếu |ω| < T          (T = 1,4 °/s)

Ý nghĩa: dưới ngưỡng, tốc độ bị nhân với tỉ lệ |ω|/T (tức nhỏ hơn 1). Càng gần 0 càng bị giảm nhiều (giảm theo bình phương); đúng ngưỡng thì bằng ω; trên ngưỡng giữ nguyên. Đường cong liên tục, không có bước nhảy.

| Tốc độ ω (°/s) | f(ω) (°/s) | Nhận xét |
|---|---|---|
| 0,2 | 0,029 | Rất nhỏ: gần như bị triệt (đây mới là nhiễu) |
| 0,5 | 0,179 | Giảm còn 36 %: vẫn còn tín hiệu |
| 1,0 | 0,714 | Giảm còn 71 % |
| 1,4 | 1,4 | Đúng ngưỡng: giữ nguyên |
| 3,0 | 3,0 | Trên ngưỡng: giữ nguyên |

Đoạn mã 5.1. Tightening (motion_pipeline.cpp)

```
static float apply_tightening(float val, float threshold) {
    float a = fabsf(val);                 // độ lớn, bỏ dấu
    if (a >= threshold) return val;       // đủ lớn: giữ nguyên (cả dấu)
    return val * (a / threshold);         // nhỏ: nhân với tỉ lệ a/T  (= dấu * a² / T)
}
```

Dòng cuối: val * (a / threshold). Vì val có dấu còn a luôn dương, kết quả giữ nguyên dấu của chuyển động (xoay trái vẫn ra âm, xoay phải ra dương).


### Tính tay để minh họa với test N2 và N3

Với gain 0,3 và xoay đều 1,0 °/s trong 2 giây (200 mẫu): f = 1,0 × 1,0 / 1,4 = 0,714 °/s; mỗi mẫu cho 0,3 × 0,714 = 0,214 điểm ảnh; 200 mẫu cho ≈ 43 điểm ảnh (test đo được 44). Với 0,5 °/s: f = 0,179; 0,3 × 0,179 × 200 ≈ 11 điểm ảnh (test đo được 11). Bản cũ cho 0 ở cả hai trường hợp.


## 5.4. Cộng dồn phần dư

HÌNH DUNG: Bạn phải trả tiền bằng tiền nguyên nhưng giá mỗi lần là 0,3 đồng. Nếu mỗi lần làm tròn thành 0 thì cả đời không trả được xu nào. Cách đúng: mỗi lần cất phần lẻ lại và cộng vào lần sau; đến khi đủ 1 đồng thì trả một đồng.

Đoạn mã 5.2. Cộng dồn phần dư (motion_pipeline.cpp)

```
float fx = -s_cfg.gain_x * omega_horizontal + s_rem_x;   // giá trị tính được + phần
      lẻ cất từ lần trước
int32_t dx = (int32_t)roundf(fx);                         // phần nguyên gửi đi
s_rem_x = fx - (float)dx;                                 // phần lẻ còn lại, cất cho
      lần sau
```

Chuyển động chậm cho 0,2 điểm ảnh mỗi mẫu thì sau 5 mẫu phần dư tích đủ để gửi đi 1 điểm ảnh: con trỏ di chuyển chậm nhưng đúng quãng đường. Phần dư bị xóa khi: bão hòa ±127, đang giữ clutch, đang đứng yên, vừa cân lại, và lúc khởi tạo.


## 5.5. Ba lớp chống trôi và chống nhiễu

| Lớp | Chống gì | Cách làm |
|---|---|---|
| 1. Hiệu chuẩn bias | Độ lệch cố định của con quay | Đo lúc bật nguồn, kiểm tra, tự đo lại khi nằm bàn |
| 2. Khóa đứng yên | Con trỏ “bò” khi tay buông | Gyro < 0,4 °/s và /a/ gần 1 g trong 30 mẫu thì khóa đầu ra về 0 |
| 3. Tightening | Nhiễu nhỏ của con quay (σ ≈ 0,09 °/s) mà vẫn giữ chuyển động chậm | Thu nhỏ dần dưới 1,4 °/s thay vì cắt |
| + Phần dư | Mất chuyển động chậm do làm tròn | Cộng dồn phần lẻ qua các mẫu |
| + Chặn click | Cú giật của cổ tay khi nhấn nút | Xóa 40 ms chuyển động trước lúc nhấn (Phần 10) |

NÓI THẬT: “Chống rung tay” (run sinh lý) nhóm chưa làm. Tightening và khóa đứng yên chỉ xử lý nhiễu của chính cảm biến và độ trôi, không phải bộ lọc run tay (run tay có tần số cỡ vài Hz và biên độ có thể lớn hơn nhiễu cảm biến nhiều). Hướng thử nghiệm đã nghiên cứu là bộ lọc kiểu 1€, mặc định tắt, ưu tiên thấp; muốn làm phải đo run tay bằng ghi dữ liệu thô trước.

Nếu thầy hỏi “chống rung như thế nào”, hãy trả lời: “chống trôi và lọc nhiễu cảm biến bằng ba lớp (hiệu chuẩn, khóa đứng yên, tightening); chống run tay thì em chưa làm”.

Hỏi: Vì sao ngưỡng tightening là 1,4 °/s?

Đáp: Đây là giá trị của vùng chết cũ được giữ lại; không có nguồn ngoài quy định và em chưa thử so sánh các giá trị T khác. Ý tưởng tightening lấy từ tài liệu về điều khiển bằng gyro (Gyro Wiki/JoyShockMapper); các tài liệu đó dùng ngưỡng lớn hơn nhiều, nhưng nhóm không lấy con số của họ.

Hỏi: Khác nhau giữa vùng chết và tightening là gì?

Đáp: Vùng chết cắt hẳn tín hiệu nhỏ về 0 nên không thể di chuyển chậm hơn ngưỡng. Tightening giảm dần theo bình phương: tín hiệu nhỏ bị giảm nhiều nhưng không bị mất, nên di chuyển chậm vẫn có. Test N2, N3: 1,0 °/s cho 44 điểm ảnh, 0,5 °/s cho 11, thay vì 0 như bản cũ.

Hỏi: Vì sao không dùng bộ lọc thông thấp hay Kalman để lọc nhiễu?

Đáp: Bộ lọc thông thấp làm con trỏ bị trễ và làm mượt luôn cả chuyển động thật. Tightening không thêm độ trễ vì chỉ biến đổi từng mẫu. Kalman cần mô hình nhiễu và tốn tính toán, không cần thiết khi nhiễu con quay chỉ 0,09 °/s. Nhóm chưa thử các bộ lọc này nên đây là lập luận chứ không phải so sánh bằng số đo.


# PHẦN 6. ƯỚC LƯỢNG TƯ THẾ BẰNG QUATERNION


## 6.1. Vì sao cần biết tư thế

Con trỏ điều khiển bằng tốc độ xoay quanh trục thẳng đứng thật (xoay ngang) và quanh trục ngang thật (gật). Nhưng con quay đo quanh các trục của board, và board có thể đang nghiêng hoặc chĩa lên. Muốn biết “thẳng đứng thật” đang ở đâu trong hệ của board, phải biết tư thế của board. Tư thế còn dùng để tính gia tốc tuyến tính (trừ trọng lực) cho cử chỉ, và góc nghiêng cho cuộn.


## 6.2. Hình dung: đi với mắt nhắm

HÌNH DUNG: Bạn nhắm mắt đi thẳng và đếm bước chân: lúc đầu đi rất chính xác nhưng càng đi lâu càng lệch (đó là con quay: chính xác ngắn hạn, nhưng cộng dồn thì trôi). Thỉnh thoảng bạn hé mắt nhìn đường chân trời: không bao giờ lệch nhưng hơi nhiễu khi xe rung (đó là gia tốc kế nhìn hướng trọng lực). Cách tốt nhất: tin bước chân trong ngắn hạn, và liếc nhìn chân trời để chỉnh nhẹ dần. Đó là bộ lọc bù (complementary filter).


## 6.3. Quaternion là gì (mức tối thiểu để vấn đáp)

Quaternion là bốn con số q = (q₀, q₁, q₂, q₃) có độ dài bằng 1, mô tả một phép quay trong không gian 3 chiều. Dùng nó thay cho ba góc (pitch, roll, yaw) vì ba góc có thể bị “khóa gimbal” (mất một bậc tự do khi chĩa thẳng lên) và công thức cập nhật phức tạp hơn. Bạn không cần nhớ công thức; chỉ cần nhớ: q_0 = 1, còn lại 0 nghĩa là chưa quay; mỗi nhịp cập nhật xong phải chia cho độ dài để q luôn có độ dài 1.


## 6.4. Bốn bước mỗi mẫu

- Dự đoán trọng lực: từ q tính ra hướng trọng lực mà board “nghĩ” là đang có, ký hiệu v_g (một vector 3 số).
- Sai số nghiêng: lấy hướng trọng lực đo được (gia tốc kế, chuẩn hóa độ dài 1), nhân có hướng với v_g: e = a × v_g. Tích có hướng của hai vector gần nhau cho một vector vuông góc, nhỏ nếu hai hướng gần trùng, lớn nếu lệch nhiều. Chỉ tính khi 0,75 g < |a| < 1,25 g: nếu tay đang giật mạnh, gia tốc kế không còn đo trọng lực nữa nên bỏ qua.
- Hiệu chỉnh tốc độ xoay: ω′ = ω + K · e, với K = 2 s⁻¹. Tức là cộng thêm một “lực kéo” nhẹ để đưa tư thế dự đoán về khớp với trọng lực đo.
- Tích phân và chuẩn hóa: q ← q + ½ · q ⊗ ω′ · dt, rồi chia q cho độ dài của nó. dt tính từ đồng hồ thật và kẹp trong [1 ms, 50 ms].
CẦN NHỚ: K = 2 s⁻¹ nghĩa là sai số nghiêng giảm dần với hằng số thời gian τ = 1/K = 0,5 s: sau 0,5 s sai số còn khoảng 37 %. K lớn thì bám trọng lực nhanh nhưng nhiễu hơn; K nhỏ thì mượt nhưng con quay trôi lâu hơn mới được sửa. Giá trị 2 là giá trị khởi điểm của dự án, ghi chú trong code là cần hiệu chỉnh theo phần cứng.

Đoạn mã 6.1. Lõi bộ lọc bù (motion_pipeline.cpp, rút gọn)

```
// e = a_đo × v_g   (không có thành phần dọc theo v_g, nên bộ lọc KHÔNG nhìn thấy yaw)
e_tilt_x = ay_n * vg_z - az_n * vg_y;
e_tilt_y = az_n * vg_x - ax_n * vg_z;
e_tilt_z = ax_n * vg_y - ay_n * vg_x;

const float tilt_correction_rate_s_inv = 2.0f;                   // K = 2 mỗi giây
float wx = (gx_c * RAD_PER_DEG) + (tilt_correction_rate_s_inv * e_tilt_x);   // ω' = ω
      + K·e

float dq0 = 0.5f * (-s_q.q1 * wx - s_q.q2 * wy - s_q.q3 * wz) * dt;   // đạo hàm
      quaternion × dt
s_q.q0 += dq0;  ...                                                    // cộng vào q,
      rồi chuẩn hóa
```

gx_c * RAD_PER_DEG đổi °/s sang radian/giây (nhân π/180) vì công thức quaternion dùng radian. Biến gx_c có hậu tố _c là “corrected”: tốc độ xoay đã trừ bias.


## 6.5. Kết quả của bộ lọc dùng vào đâu

- Hướng trọng lực trong hệ board (s_body_gravity): để biết nghiêng bao nhiêu độ (cho chế độ cuộn).
- Gia tốc tuyến tính = gia tốc đo − trọng lực: để nhận dạng cử chỉ giật.
- Tham chiếu “hướng lên” lúc cân lại: để chiếu tốc độ xoay thành ngang/dọc (Phần 7).
NÓI THẬT: Bộ lọc không quan sát được yaw (góc xoay quanh trục thẳng đứng): sai số e luôn vuông góc với v_g. Yaw chỉ có tích phân con quay, không có tham chiếu tuyệt đối. Muốn có phải dùng từ kế AK09916 (có trong chip nhưng chưa dùng). Với chuột điều khiển theo tốc độ xoay thì yaw tuyệt đối không cần thiết, nên đây là giới hạn chấp nhận được.

Hỏi: Bộ lọc của nhóm là Kalman hay Madgwick hay Mahony?

Đáp: Là bộ lọc bù chỉ có thành phần tỉ lệ (K·e), tương tự họ bộ lọc Mahony khi bỏ thành phần tích phân. Không phải Kalman: không có ma trận hiệp phương sai. Nhóm chọn vì đơn giản, ít tốn tính toán và đủ dùng cho điều khiển theo tốc độ xoay.

Hỏi: Vì sao dùng quaternion mà không dùng góc Euler?

Đáp: Euler có hiện tượng khóa gimbal khi chĩa lên/xuống và công thức cập nhật phức tạp; quaternion cập nhật đơn giản bằng phép nhân và không bị khóa. Air mouse có lúc chĩa lên (cầm như bút chỉ) nên tránh Euler là hợp lý.

Hỏi: Tại sao chỉ sửa nghiêng khi 0,75 g < |a| < 1,25 g?

Đáp: Gia tốc kế đo cả trọng lực lẫn gia tốc do tay giật. Khi độ lớn lệch xa 1 g tức là tay đang tăng tốc mạnh, phép đo hướng trọng lực không đáng tin nên bỏ qua bước sửa, chỉ dùng con quay.

Hỏi: dt thay đổi thì sao?

Đáp: dt được tính từ đồng hồ mili-giây thật giữa hai lần gọi và kẹp trong 1–50 ms, nên nếu vòng lặp chậm do phục hồi cảm biến thì tích phân vẫn đúng. Test 9 kiểm tính bất biến theo dt (5–50 ms).


# PHẦN 7. TÍNH ĐỘ DỜI CON TRỎ


## 7.1. Điều khiển theo tốc độ xoay

HÌNH DUNG: Con trỏ chạy như xe trên đường: xoay càng nhanh, con trỏ chạy càng nhanh; ngừng xoay thì con trỏ đứng. Không giống màn hình cảm ứng, nơi chạm đâu con trỏ ở đó. Chuột HID gửi độ dời tương đối (đã đi được bao nhiêu) chứ không gửi vị trí tuyệt đối, vì máy tính mới là nơi biết con trỏ đang ở đâu.


## 7.2. Từ tốc độ xoay thành độ dời

- Lấy tốc độ xoay ba trục đã trừ bias và qua tightening: (g′ₓ, g′ᵧ, g′_z).
- Chiếu lên hai trục điều khiển. Gọi r là vector “hướng lên” đã lưu lần cân lại gần nhất. Xoay ngang ω_h = g′ · r (xoay quanh trục thẳng đứng). Gật lên xuống ω_v = g′ · l, với l là trục ngang của board vuông góc với r.
- Nhân gain và cộng phần dư: fx = −gain_x · ω_h + rem_x ; fy = −gain_y · ω_v + rem_y.
- Làm tròn thành số nguyên dX, dY và cất phần lẻ làm rem cho lần sau.
- Kẹp trong ±127 (giới hạn 8 bit của gói HID).
Dấu trừ có hai lý do: xoay sang phải cho ω_h âm theo quy tắc bàn tay phải nên phải đảo để con trỏ sang phải; còn gật mũi lên cho ω_v dương nhưng gốc màn hình ở góc trên trái nên “lên” là Y giảm.

HÌNH DUNG: Chiếu giống như đo bóng của một que: que xoay trong không gian 3 chiều, nhưng ta chỉ quan tâm bóng của nó chiếu lên hai hướng “ngang” và “dọc” thật (theo trọng lực), chứ không theo thân board. Nhờ vậy cầm board nghiêng thì con trỏ vẫn đi đúng chiều.


## 7.3. Gain và đổi ra điểm ảnh

Vòng lặp chạy 100 lần/giây nên xoay 1° cho khoảng 100 × gain điểm ảnh. Gain 0,3 cho ≈ 30 điểm ảnh mỗi độ.

| Phép tính | Kết quả | Ý nghĩa |
|---|---|---|
| Gain 0,3: 1° xoay | 100 × 0,3 = 30 điểm ảnh | Mức nhạy hiện tại |
| Gain 0,3: quét màn 1920 điểm | 1920 / 30 ≈ 64° | Phải xoay khoảng 64° (dùng clutch để nhấc tay lấy thêm quãng) |
| Gain cũ 2,2: 1° xoay | 100 × 2,2 = 220 điểm ảnh | Quá nhạy |
| Gain 2,2: quét màn 1920 điểm | 1920 / 220 ≈ 9° | Chỉ 9° là hết màn: không thể điều khiển chính xác |
| Run tay 0,5° ở gain 2,2 | ≈ 110 điểm ảnh | Giải thích vì sao phải giảm gain |

Hỏi: Gain 0,3 lấy từ đâu?

Đáp: Gain cũ 2,2 quá nhạy (khoảng 220 điểm ảnh mỗi độ, chỉ 9° là quét hết màn 1920). Nhóm hạ xuống 0,3 (khoảng 30 điểm ảnh mỗi độ) theo tính toán, rồi điều chỉnh qua thử nghiệm. Chưa tối ưu qua nhiều người thử; người dùng chỉnh được từ 0,02 đến 3,0 qua trang cấu hình.

Hỏi: Vì sao kẹp ±127?

Đáp: Gói HID chuột dành 1 byte có dấu cho mỗi giá trị di chuyển nên tối đa 127. Tốc độ 127 điểm ảnh mỗi nhịp 10 ms tương ứng khoảng 12.700 điểm ảnh/giây, tức khoảng 423 °/s ở gain 0,3, nên bão hòa chỉ khi xoay rất nhanh (test N6: 450 °/s bị kẹp ở 127).

Hỏi: Vì sao dùng độ dời tương đối chứ không gửi vị trí tuyệt đối?

Đáp: Chuột HID tiêu chuẩn chỉ báo cáo dịch chuyển; vị trí con trỏ do hệ điều hành quản lý. Muốn gửi vị trí tuyệt đối phải dùng loại thiết bị khác (digitizer) và phải biết kích thước màn hình.


# PHẦN 8. NÚT MODE LÀM CLUTCH VÀ CÂN LẠI

HÌNH DUNG: Khi dùng chuột thường mà hết chỗ trên mặt bàn, bạn nhấc chuột lên, đặt lại giữa bàn rồi rê tiếp; con trỏ không chạy lúc nhấc. Giữ nút Mode trên Air Mouse là “nhấc chuột lên”: con trỏ đứng yên cho bạn xoay tay về tư thế thoải mái, thả nút ra là đặt chuột xuống rê tiếp.


## 8.1. Cơ chế

- Giữ Mode: clutch_pressed = true: đầu ra dX = dY = 0, phần dư xóa, các bộ nhận dạng cử chỉ lắc được kích hoạt.
- Thả Mode: nếu trong lúc giữ không có cử chỉ nào thì cân lại: lấy hướng trọng lực hiện tại (gia tốc qua bộ lọc thông thấp, hệ số 0,1) làm tham chiếu “hướng lên” r mới, kéo quaternion về khớp, đặt yaw tương đối về 0.
- Việc cân lại đợi 150 ms (cài đặt recenter_ms, 50–500) với con trỏ vẫn khóa, vì chính cú nhấn/thả nút làm tay rung; chờ tay ổn định rồi mới chụp tham chiếu.
Đoạn mã 8.1. Nhấn và thả clutch (motion_pipeline.cpp, rút gọn)

```
if (clutch_pressed && !s_last_clutch_state) {               // vừa NHẤN Mode
    s_gesture_occurred_in_clutch = false;                   // chưa có cử chỉ nào
    ...
} else if (!clutch_pressed && s_last_clutch_state) {        // vừa THẢ Mode
    if (!s_gesture_occurred_in_clutch) {                    // không có cử chỉ: cân
      lại
        s_recenter_pending = true;
        s_recenter_due_ms = now_ms + s_recenter_settle_ms;  // hẹn 150 ms sau
    }
}
```

CẦN NHỚ: Lưu ý: cân lại không đưa con trỏ về giữa màn hình (chuột chỉ gửi độ dời, không biết vị trí). Nó chỉ chọn lại “hướng lên” của thuật toán theo tư thế tay lúc đó.

Hỏi: Cân lại để làm gì?

Đáp: Để trục điều khiển luôn tính theo tư thế thoải mái hiện tại của tay. Nếu sau khi nhấc tay người dùng cầm nghiêng hơn hoặc chĩa lên, tham chiếu cũ sẽ làm hướng ngang/dọc bị lệch.

Hỏi: Vì sao đợi 150 ms rồi mới cân lại?

Đáp: Vì bấm/thả nút làm tay rung; nếu cân lại ngay thì chụp đúng tư thế đang rung, tham chiếu bị sai. 150 ms là giá trị chọn khi thử, chỉnh được 50–500 ms.

Hỏi: Sao khi có cử chỉ lắc thì không cân lại?

Đáp: Cú lắc làm board quay nhanh; tư thế sau cú lắc không phải tư thế thoải mái của tay nên không dùng làm tham chiếu mới.


# PHẦN 9. CỬ CHỈ LẮC TAY: BACK / FORWARD


## 9.1. Người dùng làm gì

Giữ nút Mode rồi lắc nhanh board sang trái thì máy tính nhận nút chuột thứ 4 (Back, quay lại trang trước); lắc nhanh sang phải nhận nút thứ 5 (Forward, đi tới). Hữu ích khi lật slide hoặc duyệt web. Cử chỉ chỉ hoạt động khi giữ Mode để lắc nhầm lúc điều khiển bình thường không kích hoạt.


## 9.2. Bộ nhận dạng chính: theo tốc độ xoay (yaw_flick)

HÌNH DUNG: Giống ngưỡng báo động: tốc độ xoay vượt 150 °/s thì reo chuông một lần. Sau khi reo, chuông bị khóa cho đến khi tốc độ xoay hạ xuống dưới 35 % ngưỡng (52,5 °/s), để một lần lắc không reo nhiều lần. Rồi thêm 600 ms “im lặng” để cú vẩy ngược tự nhiên của cổ tay không bị tính là lần lắc ngược chiều.

- Tính tốc độ quay quanh trục thẳng đứng thật: yaw_dps = g' · v_g (dương là quay trái).
- Nếu đang trong 600 ms sau một cử chỉ: bỏ qua.
- Nếu đang khóa: chỉ mở khóa khi |yaw| < 0,35 × ngưỡng.
- Nếu |yaw| ≥ ngưỡng (mặc định 150 °/s): khóa lại và phát sự kiện, dương → Back, âm → Forward.
Đoạn mã 9.1. Cử chỉ theo tốc độ xoay (yaw_flick.cpp)

```
gesture_event_t yf_update(yaw_flick_t* y, float yaw_dps, uint32_t now_ms) {
    if (!(y->thresh_dps > 0.0f)) return GESTURE_EVENT_NONE;                       //
      ngưỡng 0 = tắt
    if ((int32_t)(now_ms - y->block_until_ms) < 0) return GESTURE_EVENT_NONE;     //
      đang trong 600 ms im lặng
    float a = fabsf(yaw_dps);
    if (y->locked) {
        if (a < 0.35f * y->thresh_dps) y->locked = false;                         //
      hạ xuống dưới 35 %: mở khóa
        return GESTURE_EVENT_NONE;
    }
    if (a >= y->thresh_dps) {                                                     //
      vượt ngưỡng: BÁO
        y->locked = true;
        return yaw_dps > 0.0f ? GESTURE_EVENT_FLICK_LEFT : GESTURE_EVENT_FLICK_RIGHT;
    }
    return GESTURE_EVENT_NONE;
}
```


## 9.3. Bộ thứ hai: theo gia tốc ngang (gesture_detector)

Nhận dạng cú giật tịnh tiến hai pha: xung gia tốc ngang vượt 1,15 g, rồi xung ngược chiều vượt 0,35 g trong khoảng 60–450 ms; sau đó nghỉ 350 ms. Chuyển động xoay quá nhanh (trên 600 °/s) bị loại vì đó là xoay cổ tay chứ không phải giật. Chỉ hoạt động khi tư thế hợp lệ (nghiêng dọc trong ±45°, nghiêng ngang trong ±30°). Hai bộ chạy song song; bộ theo gia tốc xét trước, không bắt được gì thì mới xét bộ theo tốc độ xoay.


## 9.4. Gửi nút đúng cách

Firmware gửi press rồi release đúng nút Back hoặc Forward chứ không dùng hàm click() của thư viện: click() ghi đè toàn bộ trạng thái các nút rồi về 0, nên nếu đang giữ nút trái để kéo-thả thì cú lắc sẽ làm nhả mất nút đó.

Hỏi: Vì sao phải có khóa và 600 ms im lặng?

Đáp: Một cú lắc tạo ra tốc độ xoay vượt ngưỡng trong vài nhịp liên tiếp nên không khóa sẽ bắn nhiều sự kiện. Sau cú lắc, cổ tay vẩy ngược lại theo quán tính và tạo tốc độ ngược chiều; nếu không im lặng 600 ms thì cú vẩy này bị hiểu là cử chỉ ngược chiều.

Hỏi: Ngưỡng 150 °/s lấy từ đâu?

Đáp: Là giá trị mặc định đang dùng khi thử; log của firmware in ra đỉnh tốc độ xoay mỗi lần giữ Mode (hold peaks) để dễ chỉnh, và ngưỡng chỉnh được 40–600 °/s qua cài đặt flick_dps hoặc phím y/Y. Em chưa có thống kê để nói đây là giá trị tối ưu.

Hỏi: Tại sao có hai bộ nhận dạng?

Đáp: Hai bộ nhận dạng hai kiểu chuyển động khác nhau: bộ theo gia tốc bắt cú giật tịnh tiến hai pha, bộ theo tốc độ xoay bắt cú xoay cổ tay nhanh. Cả hai cùng chạy khi giữ Mode và bổ sung cho nhau. Về thứ tự phát triển cụ thể, em xem lại nhật ký thay đổi để nói chính xác.

NÓI THẬT: Cử chỉ Back/Forward với bản firmware chốt chưa được thử lại trên board (NOT_TESTED). Hai bộ nhận dạng đã được kiểm bằng test trên máy tính (test 7, 10 và N14); riêng phần nối vào Bluetooth đã sửa để dùng press/release nhưng chưa kiểm trên board.


# PHẦN 10. NÚT BẤM: CHỐNG DỘI, CHẶN CLICK, GÁN NÚT


## 10.1. Phần cứng của nút

Ba nút nhấn nối giữa chân GPIO và GND. Firmware bật điện trở kéo lên nội bộ của ESP32 (INPUT_PULLUP), nên khi không nhấn chân đọc được mức cao; nhấn nút nối chân xuống GND nên đọc được mức thấp. Vì thế trong code “đang nhấn” được viết là digitalRead(pin) == LOW.

HÌNH DUNG: Chân GPIO như một cái lò xo kéo cần gạt lên (điện trở kéo lên). Nhấn nút là dùng tay ấn cần gạt xuống đất. Không nhấn thì cần gạt lên; nhấn thì cần gạt xuống.

| Nút | Chân | Chức năng mặc định |
|---|---|---|
| SW2 | GPIO25 | Chuột trái (giữ để kéo-thả) |
| SW3 | GPIO26 | Chuột phải |
| SW4 | GPIO27 | Mode: clutch, cử chỉ lắc, chạm-nhấn-giữ để cuộn |


## 10.2. Chống dội (debounce)

HÌNH DUNG: Bấm chuông cửa: lò xo bên trong nảy qua nảy lại trong vài mili-giây, nên điện bị đóng ngắt liên tục chứ không đóng sạch một lần. Nếu máy đọc từng lần nảy, một lần bấm bị hiểu thành nhiều lần bấm. Chống dội là chỉ tin trạng thái mới khi nó giữ nguyên đủ lâu.

Mỗi nút có một bộ lọc nhớ ba thứ: trạng thái ổn định đã chấp nhận (stable), lần đọc thô trước (last_raw) và thời điểm tín hiệu thô đổi gần nhất (changed_ms). Mỗi lần đọc:

- Nếu tín hiệu thô khác lần trước: đặt lại đồng hồ (changed_ms = now). Đây là bước làm cho nảy không tích lũy được.
- Nếu tín hiệu thô đã khác trạng thái ổn định và giữ nguyên đủ hold_ms: chấp nhận, đổi stable.
Thời gian bất đối xứng: nhấn được chấp nhận sau 5 ms (để click phản hồi nhanh), nhả sau 20 ms (nút hay nảy lâu hơn lúc nhả).

Đoạn mã 10.1. Chống dội (button_debounce.cpp)

```
bool debounce_update(debounce_t* d, bool raw, uint32_t now_ms, uint32_t hold_ms) {
    if (raw != d->last_raw) {
        d->last_raw = raw;
        d->changed_ms = now_ms;                 // vừa đổi: bấm giờ lại (bounce)
    } else if (raw != d->stable && (uint32_t)(now_ms - d->changed_ms) >= hold_ms) {
        d->stable = raw;                        // giữ đủ lâu rồi: chấp nhận
    }
    return d->stable;
}
bool debounce_update2(debounce_t* d, bool raw, uint32_t now_ms, uint32_t press_ms,
      uint32_t release_ms) {
    return debounce_update(d, raw, now_ms, raw ? press_ms : release_ms);   // nhấn
      dùng 5 ms, nhả dùng 20 ms
}
```

CẦN NHỚ: Chi tiết tinh tế: vòng lặp chỉ đọc nút mỗi 10 ms. Nên một lần nhấn thật được chấp nhận ở lần đọc kế tiếp (khoảng 10 ms sau khi phát hiện, vì 10 ≥ 5), còn một lần nhả cần giữ ≥ 20 ms tức đến lần đọc thứ ba. Các giá trị 5 ms và 20 ms là ước lượng của nhóm; nhóm chưa đo thời gian dội thực tế của nút đang dùng.

Hỏi: Vì sao thời gian nhấn và nhả khác nhau?

Đáp: Nhấn cần phản hồi nhanh để click không bị trễ; nhả có thể chậm hơn vì nút thường dội lâu hơn lúc nhả và nhả chậm 20 ms không ảnh hưởng cảm giác. Em cũng nói thật là hai con số 5/20 ms là ước lượng, chưa đo thời gian dội của nút thật.

Hỏi: Nếu không có chống dội thì sao?

Đáp: Một lần nhấn có thể thành vài lần nhấn/nhả, gây nhấp đúp ngoài ý muốn hoặc làm hỏng thao tác kéo-thả và nhận dạng chạm-nhấn-giữ.


## 10.3. Bộ chặn click (click guard)

HÌNH DUNG: Lúc bạn nhấn nút, ngón tay đẩy cả board làm con trỏ lệch vài điểm ảnh ngay trước lúc nút đóng; click trượt khỏi mục tiêu. Giải pháp: cho con trỏ đi chậm hơn thực tế 40 ms (như xem truyền hình trực tiếp có độ trễ), và khi phát hiện nút nhấn thì xóa 40 ms cuối chưa kịp gửi: cú giật do nhấn chưa bao giờ đến máy tính.

- Mỗi nhịp, đầu vào (dX, dY) được đẩy vào cuối một hàng đợi 4 chỗ; mẫu cũ nhất ở đầu hàng được gửi đi. Nên mọi chuyển động trễ đúng 4 nhịp = 40 ms.
- Khi phát hiện cạnh nhấn: xóa sạch hàng đợi (bỏ 40 ms vừa qua).
- Trong 250 ms đầu sau khi nhấn, đầu vào bị ép về 0 (con trỏ đứng yên để click chính xác).
- Giữ quá 250 ms được coi là kéo-thả: con trỏ lại di chuyển bình thường.
Đoạn mã 10.2. Bộ chặn click (click_guard.cpp, rút gọn)

```
if (pressed && !g->pressed) {            // vừa nhấn: bỏ chuyển động đang chờ trong
      hàng đợi
    g->pressed = true;  g->press_ms = now_ms;  clear_queue(g);
} else if (!pressed && g->pressed) { g->pressed = false; }

bool frozen = g->pressed && (uint32_t)(now_ms - g->press_ms) < CG_DRAG_MS;   //
      CG_DRAG_MS = 250
int8_t in_x = frozen ? 0 : dx;           // đang trong 250 ms đầu: ép về 0
...
*out_dx = g->qx[0];                      // mẫu cũ nhất ra khỏi hàng đợi
... dịch hàng đợi rồi đẩy in_x / in_y vào cuối
```

NÓI THẬT: Cái giá là con trỏ trễ thêm 40 ms. Nhóm chưa đo độ trễ này trên toàn tuyến (cảm biến → Bluetooth → màn hình). Độ trễ chỉnh được 0–100 ms (click_guard_ms). Test N11 kiểm trên máy tính: trễ đúng số mẫu, xóa xung rung, khóa 250 ms, kéo-thả.

Hỏi: Vì sao khóa con trỏ 250 ms khi nhấn?

Đáp: Để click chính xác: lúc nhấn tay còn rung, giữ con trỏ đứng yên cho đến khi ngón tay ổn định. Nếu giữ lâu hơn 250 ms thì coi là muốn kéo-thả nên cho di chuyển lại.


## 10.4. Gán nút và đảo chiều

Ba nút vật lý không gắn cứng với trái/phải/Mode mà qua bảng gán button_map: mỗi nút có một hành động trong {không làm gì, trái, phải, giữa, Back, Forward, Mode}. bm_apply() đổi trạng thái ba nút vật lý thành sáu nút logic; nhiều nút cùng hành động thì hợp bằng OR. Ứng dụng: người thuận tay trái đổi chỗ trái/phải; gán nút giữa cho một nút bất kỳ. Ngoài ra có invert_x, invert_y để đảo chiều con trỏ.

Đoạn mã 10.3. Gán hành động cho nút nhấn (button_map.cpp, rút gọn)

```
static void add(logical_buttons_t* o, uint8_t act, bool down) {
    if (!down) return;                   // nút không nhấn thì không làm gì
    switch (act) {
        case AIR_BTN_LEFT:   o->left = true;  break;
        case AIR_BTN_RIGHT:  o->right = true; break;
        case AIR_BTN_MODE:   o->mode = true;  break;
        ...
    }
}
```

Hỏi: Gán nút để làm gì?

Đáp: Cho phép người dùng đổi chức năng nút mà không sửa code: ví dụ tay trái, hoặc muốn có nút giữa. Cài đặt btn_left, btn_right, btn_mode (0–6) lưu trong flash, chỉnh qua trang web.


# PHẦN 11. CUỘN TRANG


## 11.1. Người dùng làm gì

Chạm nút Mode (nhấn rồi nhả trong ≤ 250 ms), rồi nhấn lại trong ≤ 350 ms và giữ. Lần nhấn thứ hai chính là chế độ cuộn, kéo dài đến khi nhả nút. Trong lúc cuộn, nghiêng board (ngẩng mũi lên thì trang cuộn lên, cúi xuống thì cuộn xuống); nghiêng bao nhiêu thì cuộn nhanh bấy nhiêu; về tư thế ban đầu thì dừng. Con trỏ đứng yên. Giữ lần nhấn đầu quá 250 ms thì chỉ là clutch bình thường.

HÌNH DUNG: Giống thao tác “chạm-đúp-rồi-kéo” trên touchpad laptop. Nghiêng board giống bàn đạp ga: đạp càng sâu xe chạy càng nhanh, nhả hẳn thì dừng. Vì vậy chỉ cần nghiêng 10–15° là cuộn được trang dài bao nhiêu cũng được.


## 11.2. Nhận dạng thao tác chạm–nhấn–giữ

Firmware theo dõi một “trạng thái” và các mốc thời gian. Bốn trạng thái:

| Trạng thái | Ý nghĩa | Chuyển đi đâu |
|---|---|---|
| SM_IDLE | Nghỉ, chưa có gì | Nhấn Mode → PRESS1 (ghi giờ nhấn) |
| SM_PRESS1 | Đang giữ lần nhấn thứ nhất | Nhả trong ≤ 250 ms → WAIT2 (đó là một cú “chạm”); nhả sau > 250 ms → IDLE (chỉ là clutch) |
| SM_WAIT2 | Chờ lần nhấn thứ hai | Nhấn trong ≤ 350 ms → SCROLL; quá 350 ms không nhấn → IDLE |
| SM_SCROLL | Đang cuộn (còn giữ nút) | Nhả Mode → IDLE và hẹn cân lại tham chiếu |

Hình 11.1. Sơ đồ chuyển trạng thái của thao tác cuộn trên nút Mode

Đoạn mã 11.1. Hai trạng thái giữa (scroll_mode.cpp)

```
case SM_PRESS1:                              // lần nhấn thứ nhất
    if (release) {
        if ((uint32_t)(now_ms - s->t_ms) <= SM_TAP_MAX_MS)       // SM_TAP_MAX_MS =
      250
             { s->state = SM_WAIT2; s->t_ms = now_ms; }          // chạm ngắn: chờ lần
      hai
        else s->state = SM_IDLE;                                  // giữ lâu: chỉ là
      clutch
    }
    break;
case SM_WAIT2:                               // chờ lần nhấn thứ hai
    if (press) {
        if ((uint32_t)(now_ms - s->t_ms) <= SM_GAP_MAX_MS)       // SM_GAP_MAX_MS =
      350
             { s->state = SM_SCROLL; out.started = true; }       // vào chế độ cuộn
        ...
    } else if ((uint32_t)(now_ms - s->t_ms) > SM_GAP_MAX_MS) s->state = SM_IDLE;
    break;
```


## 11.3. Cuộn theo góc nghiêng (cần điều khiển)

tốc độ [nấc/s] = sens × ( |θ − θ_gốc| − dead )        (bằng 0 nếu |θ − θ_gốc| ≤ dead)

θ là góc nghiêng hiện tại, θ_gốc là tư thế gốc, sens = 2,0 nấc/s mỗi độ, dead = 2,5° là vùng chết quanh tư thế gốc (để tay run nhẹ không làm trang tự cuộn). Ví dụ: nghiêng 8° ⇒ (8 − 2,5) × 2 = 11 nấc/s; nghiêng 10° ⇒ 15 nấc/s. Mỗi nhịp 10 ms cho 0,11 nấc, nên phần lẻ được cộng dồn như ở độ dời con trỏ: khoảng 9 nhịp mới đủ 1 nấc để gửi.

Góc lấy từ hướng trọng lực của bộ lọc ở Phần 6: pitch = asin(−v_gx) (ngẩng mũi lên là dương), roll = asin(−v_gy). Roll chỉ dùng cho cuộn ngang khi bật hscroll.

Đoạn mã 11.2. Tốc độ cuộn và cộng dồn nấc (scroll_mode.cpp)

```
static float tilt_speed(float x, float dead, float sens) {
    if (x > dead)  return (x - dead) * sens;      // nghiêng qua vùng chết về một phía
    if (x < -dead) return (x + dead) * sens;      // phía ngược lại (kết quả âm)
    return 0.0f;                                  // trong vùng chết: không cuộn
}
static int8_t take_notches(float* rem, float add) {
    float v = *rem + add;                         // cộng phần lẻ cũ
    int n = (int)v;                               // chỉ lấy số nấc nguyên
    *rem = v - (float)n;                          // phần lẻ còn lại cất lại
    ...                                           // kẹp ±127
    return (int8_t)n;
}
```


## 11.4. Tư thế gốc: tư thế thoải mái trước khi nhấn đúp

Nhấn hai lần làm bàn tay rời khỏi tư thế cầm thoải mái, nên nếu lấy tư thế lúc nhấn lần hai làm gốc thì “điểm giữa” bị lệch. Vì vậy firmware giữ lịch sử tư thế 320 ms (vòng đệm 32 mẫu) và lấy tư thế gốc là trung bình trong khoảng 250 ms đến 150 ms trước lần nhấn đầu tiên. Giống tay cầm điều khiển TV: tư thế thoải mái là điểm giữa, nghiêng ra khỏi đó là cuộn.

| Tham số | Ý nghĩa |
|---|---|
| Lịch sử 320 ms (32 mẫu) | Nhớ tư thế gần đây để biết tư thế “trước khi nhấn” |
| Gốc = trung bình 250→150 ms trước lần nhấn đầu | Lấy tư thế thoải mái, tránh lúc ngón tay đang đè nút |
| ST_QUIET_MS = 100 ms | Sau lần nhấn thứ hai im lặng 100 ms (xung rung của ngón cái không gây cuộn) |
| ST_RAMP_MS = 200 ms | Rồi tốc độ tăng dần từ 0 đến đủ trong 200 ms, tránh cuộn bốc đột ngột |
| scroll_ref = 0 hoặc 1 | 0: gốc là tư thế trước khi nhấn đúp (mặc định); 1: tư thế lúc nhấn lần hai |

Khi nhả Mode: thoát chế độ cuộn và gọi motion_scheduleRecenter() như lúc thả clutch (đợi tay ổn định rồi cân lại). Trong lúc cuộn, con trỏ đứng yên vì firmware ép dX = dY = 0 và chỉ gửi wheel/hwheel.

Hỏi: Vì sao chuyển từ cuộn theo tốc độ xoay sang theo góc nghiêng?

Đáp: Bản đầu lấy tốc độ cuộn từ tốc độ xoay nhưng cổ tay chỉ nghiêng được trong biên độ hạn chế nên không cuộn nổi trang dài. Cuộn theo góc nghiêng: giữ nghiêng thì cuộn mãi, nên chỉ cần nghiêng 10–15°.

Hỏi: Vì sao dùng thao tác chạm-nhấn-giữ mà không dùng thêm một nút?

Đáp: Để giữ chỉ ba nút (phần cứng đơn giản). Nút Mode vừa là clutch, vừa là nút cuộn nhờ phân biệt bằng thời gian: giữ lâu là clutch, chạm rồi nhấn lại là cuộn.

Hỏi: Có cuộn kiểu chạm mép màn hình không?

Đáp: Không. Chuột HID chỉ báo độ dời nên firmware không biết con trỏ đang ở đâu trên màn hình, không phát hiện được “chạm mép”. Chỉ làm được các kiểu thuần firmware như cuộn theo góc nghiêng.

NÓI THẬT: Các hằng số 250 ms, 350 ms, 2,5°, 2,0 là giá trị chọn khi thử và chỉnh, chưa tối ưu bằng đo hay thử với nhiều người. Hiệu quả chủ quan: giảm mỏi tay so với bản cuộn theo tốc độ xoay (đánh giá của người thực hiện, chưa có số liệu).


# PHẦN 12. LỖI I²C: PHÁT HIỆN VÀ PHỤC HỒI


## 12.1. Hiện tượng

Trên breadboard, thỉnh thoảng cảm biến “mất trạng thái”: ngừng trả dữ liệu đúng, thường toàn số 0 như vừa bị reset. Log ngày 22/10 ghi hai lần như vậy trong 120 giây, một lần trùng đúng mili-giây với lúc nhấn nút (lỗi i2cWriteReadNonStop returned Error -1 cùng lúc [BTN] LEFT down). Nguyên nhân nghi ngờ nhất: dây breadboard tiếp xúc kém hoặc nguồn sụt thoáng qua khi rung. Đây là suy luận từ sự trùng thời điểm, chưa phải bằng chứng trực tiếp.


## 12.2. Bốn hạn chế của mã cũ

- Bộ giám sát chỉ chạy sau khi đọc thành công; nếu đọc lỗi liên tục thì không đếm, không phục hồi.
- Phải mất 50 mẫu (0,5 s) |a| < 0,5 g mới nhận ra cảm biến ngừng hoạt động; suốt thời gian đó mẫu toàn 0 đi vào thuật toán và con trỏ trôi.
- Wire.begin() gọi lần hai không khởi tạo lại bộ I²C của ESP32 (cần Wire.end() trước).
- Thời gian chờ I²C mặc định 50 ms, lớn hơn nhiều nhịp 10 ms.

## 12.3. Luật giám sát imu_health

| Dấu hiệu | Ngưỡng | Hành động |
|---|---|---|
| Đọc I²C lỗi | 3 lần liên tiếp | Mẫu bị bỏ ngay; đủ 3 lần thì phục hồi + khởi tạo lại |
| Gia tốc kế toàn 0 hoặc NaN/∞ | 3 mẫu liên tiếp (30 ms) | Như trên (mẫu 0 không bao giờ đi vào thuật toán) |
| 100 mẫu giống hệt nhau | 100 mẫu (1 s) | Phục hồi (lưới an toàn cũ) |
| /a/ < 0,5 g | 50 mẫu (0,5 s) | Phục hồi (lưới an toàn cũ) |
| Sau mỗi lần khởi tạo lại | 80 ms | Bỏ mẫu, không đếm (cảm biến đang khởi động) |
| Giãn cách giữa hai lần phục hồi | 300 ms; 3 s nếu lần trước thất bại | Cảm biến thật sự vắng thì không quay vòng liên tục |


## 12.4. Giải phóng bus I²C

HÌNH DUNG: Hai người nói chuyện điện thoại, một người đang nói dở một câu thì bị ngắt, không dám nói tiếp và cứ giữ im lặng (kéo SDA xuống thấp) chờ đối phương. Cách gỡ: người chủ trì gõ nhịp 9 lần (9 xung SCL) để người kia nói nốt phần dở, rồi nói “kết thúc” (STOP). Sau đó hai bên bắt đầu lại từ đầu.

Trong I²C, mỗi byte gồm 8 bit cộng 1 bit ACK, tổng 9 xung SCL. Nếu một thiết bị phụ “lạc” giữa một byte nó sẽ giữ SDA ở mức thấp cho đến khi nhận đủ xung; vì vậy phát tối đa 9 xung SCL là đủ cho nó nhả dây. Rồi tạo điều kiện STOP (SDA từ thấp lên cao khi SCL đang cao) để đưa bus về trạng thái rảnh.

Đoạn mã 12.1. Giải phóng bus (icm20948_driver.cpp)

```
bool imu_busRecover(void) {
    Wire.end();                                   // trả lại bộ I2C và hai chân cho vi
      điều khiển
    pinMode(PIN_I2C_SDA, INPUT_PULLUP);  pinMode(PIN_I2C_SCL, INPUT_PULLUP);
    for (int i = 0; i < 9 && digitalRead(PIN_I2C_SDA) == LOW; ++i) {   // SDA còn bị
      giữ thấp: gõ nhịp
        pinMode(PIN_I2C_SCL, OUTPUT); digitalWrite(PIN_I2C_SCL, LOW);
      delayMicroseconds(5);   // SCL xuống
        pinMode(PIN_I2C_SCL, INPUT_PULLUP);
      delayMicroseconds(5);   // SCL lên
    }
    // điều kiện STOP: SDA từ thấp lên cao khi SCL đang cao
    pinMode(PIN_I2C_SDA, OUTPUT); digitalWrite(PIN_I2C_SDA, LOW);
      delayMicroseconds(5);
    pinMode(PIN_I2C_SCL, INPUT_PULLUP); delayMicroseconds(5);
    pinMode(PIN_I2C_SDA, INPUT_PULLUP); delayMicroseconds(5);
    return digitalRead(PIN_I2C_SDA) == HIGH && digitalRead(PIN_I2C_SCL) == HIGH;   //
      cả hai dây đã lên cao?
}
```

Hình 12.1. Các bước phục hồi khi cảm biến mất trạng thái


## 12.5. Số liệu

Dòng thời gian từ log: lỗi đầu tiên ở 5588 ms, i2cInit ở 5620 ms: ≈ 32 ms phát hiện (ba nhịp), 33 ms khởi tạo lại, cộng 80 ms chờ khởi động: tổng khoảng 145 ms, tức dưới 0,15 s không có chuyển động. Bản cũ mất 0,5–3 s và trong suốt thời gian đó con trỏ trôi do mẫu sai. Hai phiên thử 120 s ghi tổng cộng 4 lần mất, tất cả được phục hồi.

NÓI THẬT: Số lần mất cảm biến không giảm: nguyên nhân gốc là phần cứng (breadboard), sửa này chỉ rút ngắn hậu quả. Muốn xử lý gốc cần hàn perfboard và thêm tụ 10–100 µF gần chân VCC của module.

Test N25 kiểm bộ luật trên máy tính: cảm biến khỏe không bao giờ bị loại; mẫu 0 bị bỏ ngay và khởi tạo lại ở mẫu thứ 3; rơi tự do ngắn (0,2 g trong 200 ms) không bị coi là lỗi; 100.000 mẫu có nhiễu ngắt quãng 1–2 mẫu không kích hoạt nhầm.

Hỏi: Vì sao phải gọi Wire.end() trước Wire.begin()?

Đáp: Gọi Wire.begin() lần hai không khởi tạo lại bộ ngoại vi I²C của ESP32 (log của bản cũ không có dòng khởi tạo lần hai). Wire.end() giải phóng bộ I²C để Wire.begin() sau đó khởi động thật sự.

Hỏi: Vì sao đặt thời gian chờ I²C là 10 ms?

Đáp: Đọc 12 byte mất khoảng 0,5 ms; thời gian chờ mặc định 50 ms dài hơn cả nhịp 10 ms, nên nếu bus lỗi thì cả vòng lặp bị chặn. Đặt 10 ms để lỗi được báo ngay trong một nhịp.

Hỏi: Vì sao coi “toàn số 0” là dấu hiệu hỏng?

Đáp: Cảm biến sống luôn đo được gia tốc khoảng 1 g (trọng lực), không thể bằng đúng (0, 0, 0). Sau khi mất nguồn thoáng qua, ICM-20948 reset về chế độ ngủ và trả toàn 0. Nên phát hiện sớm bằng ba mẫu 0 (30 ms) thay vì chờ 0,5 s.

Hỏi: Bias có bị mất sau khi khởi tạo lại không?

Đáp: Không: firmware giữ bias cũ (log ghi old bias kept), chỉ khởi tạo lại cảm biến. Nếu bias cũ sai thì cơ chế tự đo lại khi nằm yên sẽ sửa.


# PHẦN 13. BLUETOOTH HID


## 13.1. Ý tưởng

HÌNH DUNG: ESP32 như một quán cà phê mở cửa treo biển “AirMouse-ESP32” (quảng bá, advertising). Máy tính thấy biển, bước vào làm quen (ghép nối). Từ đó, mỗi khi có chuyển động ESP32 gửi một tờ giấy báo cáo 5 byte cho máy tính, máy tính hiểu ngay là chuột vì nó khai báo mình là thiết bị HID (Human Interface Device), như mọi chuột Bluetooth khác. Không cần cài driver.

BLE (Bluetooth Low Energy) là loại Bluetooth tiết kiệm điện. HID qua GATT là cách chuột/bàn phím BLE khai báo và gửi dữ liệu. Dự án dùng thư viện ESP32 BLE Mouse (T-vK, phiên bản 0.3.1) lo phần mô tả HID và gửi gói.


## 13.2. Gói báo cáo 5 byte

| Byte | Nội dung | Ghi chú |
|---|---|---|
| 0 | Nút | Mỗi bit một nút: trái, phải, giữa, Back, Forward |
| 1 | Độ dời X | Số nguyên 8 bit có dấu: −127…127 |
| 2 | Độ dời Y | Như trên |
| 3 | Con lăn dọc (wheel) | Số nấc cuộn |
| 4 | Con lăn ngang (hwheel) | Số nấc cuộn ngang |


## 13.3. Gửi nút theo cạnh

Đoạn mã 13.1. Gửi nút theo cạnh (app_ble.cpp)

```
static void sync_button(uint8_t code, bool want, bool* held) {
    if (want && !*held) bleMouse.press(code);        // vừa muốn nhấn mà chưa nhấn:
      gửi "nhấn"
    else if (!want && *held) bleMouse.release(code); // vừa muốn nhả mà đang nhấn: gửi
      "nhả"
    *held = want;
}
...
if (move_x != 0 || move_y != 0 || wheel != 0 || hwheel != 0) {
    bleMouse.move(move_x, move_y, wheel, hwheel);    // chỉ gửi khi có chuyển động
}
```

Chỉ gửi press một lần khi vừa nhấn và release một lần khi vừa nhả; máy tính tự hiểu “giữ nút” là khoảng giữa hai sự kiện đó, nhờ vậy kéo-thả hoạt động. Gói chuyển động chỉ gửi khi có số khác 0, để không làm đầy đường truyền.


## 13.4. Khi mất kết nối

Khi Bluetooth ngắt: không gửi gì; LED (nếu có) nháy chậm mỗi 0,5 s; và firmware nhả toàn bộ 5 bit nút của thư viện. Lý do: thư viện giữ bit nút trong biến riêng và đặt vào mọi gói, nên nếu mất kết nối lúc đang giữ nút thì nút bị duy trì ở trạng thái nhấn sau khi kết nối lại. Cơ chế này chỉ mới được kiểm tra bằng đọc mã và biên dịch (NOT_TESTED trên board).

Hỏi: Vì sao chọn BLE chứ không phải Wi-Fi, Bluetooth cổ điển hay cáp USB?

Đáp: BLE tiết kiệm điện (quan trọng khi dùng pin), có sẵn trên ESP32, và hệ điều hành hỗ trợ sẵn HID qua BLE nên không cần driver. Wi-Fi tốn điện và cần mạng. Cáp USB làm mất ý nghĩa “không dây”. Bluetooth cổ điển ESP32 có nhưng thư viện chuột BLE đơn giản hơn.

Hỏi: Độ trễ Bluetooth là bao nhiêu?

Đáp: Nhóm chưa đo. Theo hiểu biết chung, BLE gửi theo chu kỳ kết nối (connection interval) do máy tính quyết định, thường vài mili-giây đến vài chục mili-giây; số cụ thể của dự án chưa có.

Hỏi: Vì sao mỗi giá trị di chuyển chỉ 8 bit?

Đáp: Đó là định dạng của báo cáo chuột HID trong thư viện: 1 byte có dấu cho mỗi trục. Nên firmware kẹp ±127 mỗi nhịp; chỉ bão hòa khi xoay rất nhanh (trên khoảng 423 °/s ở gain 0,3), khi đó phần vượt bị bỏ.


# PHẦN 14. CÀI ĐẶT, LƯU FLASH VÀ TRANG WEB


## 14.1. Vì sao cần cài đặt chỉnh được

Mỗi người cầm khác nhau, ưa độ nhạy khác nhau, thuận tay khác nhau. Thay vì sửa code và nạp lại, firmware có 17 cài đặt chỉnh qua máy tính, lưu vào flash để còn nguyên sau khi tắt nguồn.


## 14.2. Giao thức dòng lệnh @

Máy tính gửi một dòng bắt đầu bằng @ qua cổng serial (115200 baud), board trả đúng một dòng bắt đầu bằng @:

| Lệnh | Tác dụng |
|---|---|
| @GET | Trả toàn bộ 17 giá trị trên một dòng (@CFG ver=5 gain_x=0.300 ...) |
| @SET gain_x=0.45 flick_dps=180 | Đặt giá trị, áp dụng ngay, chưa lưu; tất cả hoặc không gì: một giá trị sai thì không đổi gì |
| @SAVE | Ghi vào flash |
| @DEFAULTS | Về mặc định, chưa lưu |
| @CAL | Đo lại bias (board phải nằm yên) |

HÌNH DUNG: Giống ra lệnh bằng tin nhắn: gửi một dòng chữ, nhận lại một dòng trả lời. @SET giống thử đổi cài đặt trên màn hình xem trước; chỉ khi bấm @SAVE mới “lưu thật”.

Bộ phân tích được thiết kế để chống đầu vào không hợp lệ: không phân biệt hoa thường, từ chối giá trị rỗng, có ký tự thừa (“12.5”, “7x”), NaN, vô cực, khóa lạ và giá trị ngoài khoảng. Test N16–N19 kiểm, kể cả 60.000 dòng lệnh ngẫu nhiên không làm hỏng chương trình hay làm cấu hình sai khoảng.


## 14.3. Lưu vào flash (NVS)

Cài đặt được lưu bằng thư viện Preferences của ESP32 (bộ nhớ NVS trong flash): namespace airmouse, một khóa cfg chứa số phiên bản (hiện bằng 5) rồi toàn bộ 17 trường. Khi khởi động, firmware chỉ chấp nhận khối đã lưu nếu độ dài đúng bằng kích thước hiện tại, phiên bản khớp và mọi giá trị nằm trong khoảng; ngược lại dùng mặc định.

- Chỉ ghi flash khi nhận @SAVE và có thay đổi (flash có số lần ghi giới hạn).
- Khi nạp bản firmware đổi cấu trúc cài đặt, cài đặt cũ bị bỏ và board về mặc định. Log bản chốt ghi đúng như vậy: stored settings have another size (36, expected 40) -> defaults.

## 14.4. Trang web cấu hình

Trang một file HTML (https://airmouse-config.pages.dev/) dùng Web Serial API của Chrome/Edge để nói chuyện với board qua cáp USB bằng chính giao thức @: nút kết nối gửi @GET; “Áp dụng thử” gửi @SET; “Lưu vào board” gửi @SAVE; “Đo lại bias” gửi @CAL. Có thêm preset (bộ giá trị đặt sẵn), nhập/xuất file, chế độ thử không cần board, và phần giải thích từng tham số.

Hỏi: Vì sao @SET là “tất cả hoặc không gì”?

Đáp: Để cấu hình không bao giờ ở trạng thái nửa vời: nếu người dùng gửi nhiều giá trị mà một giá trị sai thì không giá trị nào được áp dụng, tránh trường hợp đổi một nửa gây hành vi lạ.

Hỏi: Vì sao lưu kèm số phiên bản?

Đáp: Nếu bản firmware sau thêm hoặc bớt cài đặt, khối cũ có cấu trúc khác; đọc nhầm sẽ cho giá trị rác. Số phiên bản và kích thước giúp phát hiện và quay về mặc định an toàn.


# PHẦN 15. KHỞI ĐỘNG VÀ CÁCH ĐỌC LOG


## 15.1. Trình tự khởi động

- Mở cổng serial 115200 baud; cấu hình ba nút (INPUT_PULLUP) và chân LED.
- Khởi tạo cảm biến (thử tối đa 5 lần, mỗi lần giải phóng bus I²C); in kết quả đọc lại thanh ghi. Cả 5 lần hỏng thì báo [FATAL].
- Cấu hình thuật toán và nạp cài đặt từ flash.
- Hiệu chuẩn bias (2 s mỗi lần, tối đa 5 lần).
- Bật BLE, quảng bá “AirMouse-ESP32”; vào vòng lặp 100 Hz.

## 15.2. Đọc dòng [STATUS]

Ví dụ 15.1. Một dòng [STATUS] thật

```
[STATUS] Rate: 100 Hz | Stat: 1 | Clutch: 0 | dX:   +0, dY:   +0 | BiasZ: +0.40 | Up:
      4s | Frz: 0 | Heal: 0 | Err: 0 | Rec: 0 | Rst: 1
```

| Trường | Cách đọc |
|---|---|
| Rate | Số vòng lặp mỗi giây. 100 là đúng; nếu thấp hơn có thể đang phục hồi |
| Stat | 1 = đứng yên (con trỏ đang bị khóa); 0 = đang chuyển động |
| Clutch | 1 = đang giữ nút Mode |
| dX, dY | Độ dời vừa gửi đi (kiểm tra con trỏ có đang bị trôi: nếu board nằm yên mà khác 0 là có vấn đề) |
| BiasZ | Bias hiện dùng của trục Z (°/s) |
| Frz, Heal | Số lần phục hồi cảm biến; số lần tự đo lại bias |
| Err, Rec | Số lần đọc I²C lỗi; số lần giải phóng bus |
| Rst | Lý do khởi động lại gần nhất (1 = bật nguồn) |

Các tiền tố log khác: [BTN] (nút nhấn), [MODE] (clutch), [SCROLL] (cuộn), [GESTURE] (cử chỉ), [IMU] (cảm biến), [HEAL] (tự đo lại bias), [CALIBRATION], [CONFIG].


# PHẦN 16. BẢNG SỐ CẦN THUỘC VÀ SƠ ĐỒ NHỚ NHANH


## 16.1. Số liệu theo nhóm

| Thông số | Giá trị | Ghi chú |
|---|---|---|
| Nhịp và cảm biến |  |  |
| Nhịp vòng lặp | 100 Hz (10 ms) | APP_LOOP_PERIOD_US = 10 000 |
| Tốc độ lấy mẫu cảm biến | 1125/(1+10) = 102,27 Hz | Chia tần số = 10 |
| Tốc độ I²C / địa chỉ | 400 kHz / 0x68 | AD0 nối GND; SDA = GPIO21, SCL = GPIO22 |
| Dải đo / độ nhạy | ±500 °/s (65,5 LSB) · ±4 g (8192 LSB) | Chia số thô cho 65,5 và 8192 |
| Thời gian đọc 12 byte | ≈ 438 µs | Đo ở 400 kHz; ở 100 kHz là 1471 µs |
| Nhiễu con quay σ | ≈ 0,09 °/s | Đo khi nằm yên |
| Bias và đứng yên |  |  |
| Hiệu chuẩn | 200 mẫu (2 s), tối đa 5 lần | sd ∈ [0,005 ; 0,35] °/s, hai nửa lệch ≤ 0,25 °/s, /a/ = 1 ± 0,15 g |
| Bias của board | ≈ −1,5 / +0,5 / +0,4 °/s | X / Y / Z |
| Khóa đứng yên | gyro < 0,4 °/s, //a/−1/ < 0,08 g, 30 mẫu | ≈ 0,3 s |
| Tự chỉnh bias | sau 150 mẫu (1,5 s) đứng yên, α = 0,002 |  |
| Tự đo lại khi nằm bàn | sd gia tốc ≤ 0,005 g; bias lệch > 0,5 °/s; 3 cửa sổ 1 s | Bàn 0,002 g · tay vững nhất 0,010 g |
| Trôi bias 12 phút (đo) | 0,029 và 0,057 °/s | Hai lần đo |
| Lọc và con trỏ |  |  |
| Tightening | T = 1,4 °/s | f = ω·/ω//T dưới ngưỡng |
| Gain | 0,3 ≈ 30 điểm ảnh/độ | Cũ 2,2 ≈ 220 điểm ảnh/độ |
| Bộ lọc bù | K = 2 s⁻¹ (τ = 0,5 s) | Sửa nghiêng khi 0,75 < /a/ < 1,25 g; dt kẹp 1–50 ms |
| Kẹp độ dời | ±127 | Giới hạn HID 8 bit |
| Nút và click |  |  |
| Chống dội | nhấn 5 ms / nhả 20 ms | Ước lượng, chưa đo |
| Bộ chặn click | trễ 40 ms; khóa 250 ms | Chỉnh 0–100 ms |
| Cân lại sau clutch | 150 ms | Chỉnh 50–500 ms |
| Cử chỉ |  |  |
| Lắc theo tốc độ xoay | 150 °/s (40–600) | Khóa đến < 35 % ngưỡng; im lặng 600 ms |
| Lắc theo gia tốc | 1,15 g → 0,35 g, 60–450 ms, nghỉ 350 ms | Loại nếu xoay > 600 °/s |
| Cuộn |  |  |
| Chạm / khoảng cách nhấn lại | ≤ 250 ms / ≤ 350 ms |  |
| Cuộn theo góc | 2,0 nấc/s mỗi độ; vùng chết 2,5° | Nghiêng 10° ⇒ 15 nấc/s |
| Lịch sử tư thế | 320 ms; gốc = trung bình 250→150 ms trước lần nhấn đầu | Im lặng 100 ms; tăng tốc 200 ms |
| Phục hồi I²C |  |  |
| Phát hiện | 3 lần lỗi hoặc 3 mẫu toàn 0 (30 ms) |  |
| Khởi tạo lại / chờ | ≈ 33 ms / 80 ms | Tổng < 0,15 s |
| Giãn cách phục hồi | 300 ms; 3 s nếu lần trước thất bại |  |
| Thời gian chờ I²C | 10 ms | Mặc định 50 ms |
| Hệ thống |  |  |
| Cài đặt | 17 khóa; phiên bản 5; NVS airmouse/cfg | Lưu khi @SAVE |
| Kiểm thử | 35 test trên máy tính | N1–N25 + 10 test cơ sở |
| Firmware chốt | 1.186.320 byte; Flash 90,0 %, RAM 12,4 % | SHA-256 bắt đầu 46B47DBC53252988 |
| Thử nghiệm trực tiếp | 150 s, Rate 100 Hz, Err: 0 | Cuộn 2 lần (17 s và 13 s) |


## 16.2. Ba sơ đồ cần vẽ được không nhìn tài liệu

Hình 16.1. Một nhịp 10 ms (12 trạm)

Hình 16.2. Đường đi của một mẫu cảm biến qua motion_process()

Hình 16.3. Sơ đồ khối hệ thống


# PHẦN 17. NGÂN HÀNG CÂU HỎI VẤN ĐÁP

Đọc to từng câu, tự trả lời, rồi đối chiếu. Câu có dấu (★) là câu thầy rất hay hỏi hoặc câu bẫy.


## A. Tổng quan và kiến trúc

Hỏi: Đề tài của nhóm làm gì? Tóm tắt trong 30 giây.

Đáp: Air Mouse là chuột bay không dây: cầm trong tay, xoay cổ tay để di chuyển con trỏ, có nút trái/phải, nút Mode để khóa con trỏ và để cuộn, lắc nhanh để Back/Forward. Phần cứng là ESP32 và cảm biến ICM-20948; giao tiếp với máy tính bằng Bluetooth HID nên không cần driver. Trọng tâm của em là firmware: lọc nhiễu, hiệu chuẩn, ước lượng tư thế, các thao tác, và cơ chế tự phục hồi khi cảm biến lỗi.

Hỏi: (★) Nhóm đã làm được gì và chưa làm được gì?

Đáp: Đã làm: đọc cảm biến 100 Hz, chuỗi xử lý chuyển động có hiệu chuẩn và lọc, đủ thao tác chuột (click, kéo-thả, clutch, Back/Forward, cuộn), BLE HID, cài đặt lưu flash và trang web cấu hình, tự phục hồi I²C, 35 test.

Chưa làm: pin LiPo, mạch sạc, đo pin, LED chưa lắp; chưa có PCB (làm trên breadboard); chưa đo độ trễ, dòng điện, độ bền chạy dài; chưa chống run tay; chưa thử với nhiều người.

Hỏi: Firmware chia thành mấy lớp, vì sao?

Đáp: Hai lớp: lõi thuần chứa thuật toán, không gọi Arduino, test được trên máy tính; lớp app_ nối với phần cứng. Mục đích là kiểm thử thuật toán bằng 35 bài test tự động.

Hỏi: Vì sao chạy 100 Hz mà không phải 50 hay 200 Hz?

Đáp: 100 Hz đủ mượt, đủ cho bộ lọc, gần bằng tốc độ lấy mẫu 102,27 Hz của cảm biến. Đây là quyết định thiết kế ban đầu; em chưa thử các tần số khác để so sánh.

Hỏi: Vì sao không dùng delay()?

Đáp: delay() làm ESP32 đứng chờ, không phục vụ được BLE và serial. Firmware hỏi micros() mỗi lần loop() được gọi và chỉ xử lý khi đủ 10 ms.

Hỏi: Điều gì xảy ra nếu cảm biến hỏng giữa lúc đang dùng?

Đáp: Mẫu hỏng bị bỏ ngay, ba lần liên tiếp thì giải phóng bus I²C và khởi tạo lại cảm biến trong khoảng 33 ms; trong lúc đó con trỏ không di chuyển nhưng nút, Bluetooth và log vẫn chạy. Tổng gián đoạn dưới 0,15 s.


## B. Thuật toán

Hỏi: (★) Bộ lọc nhiễu có nuốt chuyển động nhỏ không?

Đáp: Bản đầu thì có: vùng chết cứng và khóa 1,2 °/s làm 0,5 và 1,0 °/s cho 0 điểm ảnh. Nhóm sửa bằng tightening (thu nhỏ dần thay vì cắt), hạ ngưỡng khóa xuống 0,4 °/s và cộng dồn phần dư. Test cho 44 điểm ảnh ở 1,0 °/s và 11 ở 0,5 °/s. Giới hạn: chuyển động nhỏ hơn 0,4 °/s kéo dài vẫn có thể bị coi là đứng yên.

Hỏi: (★) Con trỏ bị trôi khi để yên thì xử lý thế nào?

Đáp: Ba lớp: trừ bias đo lúc khởi động (có kiểm tra), khóa đầu ra về 0 khi đứng yên 0,3 s, tự chỉnh bias chậm khi đã đứng yên 1,5 s; nếu bias sai mà board nằm trên bàn thì tự đo lại. Giới hạn đã biết: bias dư khoảng 0,3 °/s trên yaw vẫn gây trôi nhẹ (test N7: 21 điểm ảnh/10 s).

Hỏi: Giải thích bộ lọc bù cho người chưa học.

Đáp: Con quay chính xác ngắn hạn nhưng cộng dồn thì trôi; gia tốc kế không trôi nhưng nhiễu khi tay giật. Bộ lọc tin con quay ở ngắn hạn rồi mỗi nhịp kéo nhẹ tư thế về hướng trọng lực đo được, với hằng số thời gian 0,5 s.

Hỏi: Quaternion là gì, vì sao dùng?

Đáp: Bốn số có độ dài 1 mô tả một phép quay 3D; không bị khóa gimbal như góc Euler, và cập nhật chỉ cần phép nhân rồi chuẩn hóa.

Hỏi: Tại sao con trỏ điều khiển theo tốc độ xoay chứ không theo góc?

Đáp: Chuột HID gửi độ dời tương đối. Xoay càng nhanh con trỏ càng nhanh, ngừng xoay thì đứng yên, và cơ chế clutch cho phép nhấc tay về lại. Theo góc thì cần ánh xạ góc sang vị trí tuyệt đối và yaw không có tham chiếu.

Hỏi: Phép chiếu ω_h = g′·r nghĩa là gì?

Đáp: Lấy thành phần tốc độ xoay theo hướng “thẳng đứng thật” r (hướng lên đã lưu lần cân lại). Nhờ định nghĩa trục theo trọng lực thay vì theo thân board nên cầm board nghiêng thì con trỏ vẫn đi đúng chiều.

Hỏi: Phần dư để làm gì?

Đáp: Để chuyển động rất chậm không bị làm tròn về 0 mỗi mẫu: phần lẻ được cất và cộng vào mẫu sau, nên tổng quãng đường vẫn đúng.

Hỏi: Vì sao cân lại sau khi thả clutch?

Đáp: Để tham chiếu “hướng lên” khớp với tư thế thoải mái mới của tay; đợi 150 ms vì thao tác nhấn/thả làm tay rung.

Hỏi: (★) Chống rung tay nhóm làm thế nào?

Đáp: Nhóm chưa làm bộ lọc run tay. Phần đã làm là chống trôi và lọc nhiễu cảm biến (hiệu chuẩn, khóa đứng yên, tightening) và chống giật lúc nhấn (bộ chặn click 40 ms). Chống run tay là hướng phát triển (bộ lọc kiểu 1€, mặc định tắt), cần đo run tay trước.

Hỏi: Cử chỉ lắc hoạt động thế nào, tránh kích hoạt nhầm ra sao?

Đáp: Chỉ hoạt động khi giữ Mode. Tốc độ quay quanh trục thẳng đứng vượt 150 °/s thì phát sự kiện; sau đó khóa đến khi tốc độ hạ dưới 35 % ngưỡng và im lặng 600 ms để cú vẩy ngược không thành cử chỉ ngược chiều.

Hỏi: Cuộn trang hoạt động thế nào?

Đáp: Chạm Mode, nhấn lại trong 350 ms và giữ để vào chế độ cuộn; nghiêng board so với tư thế thoải mái trước khi nhấn đúp để đặt tốc độ cuộn: 2 nấc/s cho mỗi độ nghiêng ngoài vùng chết 2,5°; con trỏ đứng yên. Nhả nút thì thoát và cân lại.

Hỏi: Vì sao trong lúc chờ nhấn lần hai thì con trỏ vẫn khóa?

Đáp: Vì lần nhấn đầu đã là nhấn Mode, bản chất là clutch. Chỉ khi nhả quá 250 ms thì mới chỉ là clutch; chạm ngắn đi vào chờ lần hai. Con trỏ không di chuyển trong khi giữ Mode.

Hỏi: Quá trình thay đổi gain từ 2,2 xuống 0,3 diễn ra thế nào?

Đáp: Gain 2,2 tương ứng 220 điểm ảnh mỗi độ, chỉ 9° là quét hết màn 1920 và run tay 0,5° làm lệch khoảng 110 điểm. Nhóm hạ còn 0,3 (30 điểm ảnh/độ) theo tính toán rồi thử lại; người dùng chỉnh được qua trang cấu hình.


## C. Phần cứng, I²C và Bluetooth

Hỏi: I²C hoạt động thế nào? Vẽ một lần đọc.

Đáp: Master gửi START, địa chỉ 0x68 cộng bit ghi, số thanh ghi muốn đọc, repeated START, địa chỉ cộng bit đọc, rồi cảm biến gửi 12 byte (master ACK từng byte, NACK byte cuối), và STOP. Hai dây SDA/SCL kéo lên bằng điện trở 10 kΩ có sẵn trên module.

Hỏi: Vì sao đọc thanh ghi cấu hình lại sau khi ghi?

Đáp: Để chắc chắn lệnh ghi thật sự có hiệu lực: nếu dây lỏng thì lệnh ghi có thể mất mà không báo lỗi. Cả 7 giá trị đọc lại phải khớp thì mới coi khởi tạo thành công.

Hỏi: Pull-up để làm gì? Có tính giá trị không?

Đáp: SDA và SCL là open-drain: thiết bị chỉ kéo xuống 0; mức 1 do trở kéo lên tạo ra. Module WCMCU-20948 có sẵn 10 kΩ và baseline đã hoạt động với giá trị đó; nhóm không lắp thêm và chưa đo thời gian lên của tín hiệu.

Hỏi: (★) Module cấp 3,3 V trực tiếp có an toàn không?

Đáp: Datasheet gốc của chip ICM-20948 quy định chân I/O trong dải 1,71–1,95 V. Module WCMCU-20948 của nhóm chạy ổn ở 3,3 V trong các phép thử, nhưng đó chỉ là kiểm trên đúng module này và độ bền lâu dài chưa được thử; em không khẳng định an toàn cho mọi điều kiện.

Hỏi: Nút nhấn nối như thế nào? Vì sao nhấn là mức thấp?

Đáp: Mỗi nút nối giữa chân GPIO và GND; firmware bật điện trở kéo lên nội bộ nên bình thường chân ở mức cao, nhấn nối xuống GND nên đọc được mức thấp.

Hỏi: Nếu không có LED và đo pin thì code LED, đo pin có không?

Đáp: Code LED có (nháy khi chờ BLE, sáng khi đã kết nối, nháy khi hiệu chuẩn) nhưng chưa kiểm vì chưa lắp LED. Code đo pin thì chưa có: chân GPIO34 mới khai báo.

Hỏi: Làm sao máy tính biết thiết bị là chuột?

Đáp: Thư viện BLE khai báo thiết bị là HID chuột trong quá trình ghép nối, cùng định dạng gói báo cáo 5 byte (nút, X, Y, wheel, hwheel). Hệ điều hành đã có sẵn trình điều khiển HID nên không cần cài thêm.


## D. Cài đặt và kiểm thử

Hỏi: Cài đặt lưu ở đâu, mất khi tắt nguồn không?

Đáp: Lưu trong bộ nhớ NVS của flash, khóa cfg kèm số phiên bản; không mất khi tắt nguồn. Chỉ ghi khi nhận @SAVE và có thay đổi.

Hỏi: Kiểm thử bằng cách nào? 35 test là gì?

Đáp: Lõi thuật toán được biên dịch bằng g++ cùng cảm biến và đồng hồ giả lập: 10 test cơ sở (driver, đứng yên, xoay, clutch, tư thế, cử chỉ…) và N1–N25 (độ nhạy, hiệu chuẩn, chống dội, chặn click, lắc, cài đặt, cuộn, gán nút, sức khỏe cảm biến), gồm 60.000 dòng lệnh ngẫu nhiên và 100.000 mẫu nhiễu.

Hỏi: Test trên máy tính có chứng minh sản phẩm dùng tốt không?

Đáp: Không. Test chỉ chứng minh logic đúng với dữ liệu giả lập hoặc phát lại. Hành vi thật trên board được kiểm bằng log và thử nghiệm trực tiếp; và cảm giác dùng mới do một người đánh giá.

Hỏi: Đã thử trên board những gì?

Đáp: Bring-up I²C; đo thời gian và nhiễu; trôi bias 12 phút; đo hướng trục; hiệu chuẩn và tự đo lại; phục hồi I²C (4 lần/240 s); cài đặt NVS; thử nghiệm 150 s bản chốt (nút, cuộn hai lần, 100 Hz, không mất cảm biến).


## E. Câu bẫy: trả lời thật

Hỏi: (★) Độ trễ của chuột là bao nhiêu?

Đáp: Em chưa đo độ trễ đầu-cuối. Em biết các thành phần: chu kỳ 10 ms, bộ chặn click thêm 40 ms, và chu kỳ kết nối Bluetooth do máy tính quyết định; tổng chưa có số đo.

Hỏi: (★) Pin dùng được bao lâu?

Đáp: Chưa có số liệu: thiết bị đang chạy bằng USB, chưa lắp pin và chưa đo dòng điện. Ước tính từ tài liệu ESP32 ở chế độ modem-sleep khoảng 14–31 mA nhưng bản hiện tại chưa tối ưu nên có thể cao hơn nhiều.

Hỏi: (★) Chạy liên tục lâu có ổn không, có rò rỉ bộ nhớ không?

Đáp: Phiên dài nhất em thử khoảng 156 s; chưa chạy 30–60 phút và chưa có bộ đếm bộ nhớ trong log, nên em không kết luận về rò rỉ.

Hỏi: (★) Có thử với người khác không?

Đáp: Chưa. Các đánh giá cảm giác (độ nhạy, cuộn, mỏi tay) do chính người thực hiện đề tài tự đánh giá; các hằng số cảm giác chưa tối ưu qua nhiều người.

Hỏi: Vì sao không có PCB?

Đáp: Nhóm chọn lắp trên breadboard cho kịp tiến độ và dễ thay đổi; PCB cần chốt kích thước và sơ đồ nguyên lý. Breadboard là điểm yếu: tiếp xúc kém làm cảm biến mất trạng thái, nên firmware có cơ chế tự phục hồi.

Hỏi: Cái gì bạn tự đo, cái gì lấy từ tài liệu, cái gì chọn bằng suy luận?

Đáp: Tự đo: nhiễu con quay 0,09 °/s; thời gian I²C 438 µs; bias và trôi bias; hướng trục; sd gia tốc kế (0,002 / 0,010 g); thời gian phục hồi 33 ms.

Từ tài liệu: độ nhạy 65,5 LSB và 8192 LSB; công thức tốc độ lấy mẫu; địa chỉ 0x68, WHO_AM_I 0xEA; ý tưởng tightening; con số 1,5 s nghỉ.

Chọn bằng suy luận hoặc thử: gain 0,3; T = 1,4 °/s; K = 2; 5/20 ms; 40 ms; 150 ms; 150 °/s; 250/350 ms; 2,5° và 2,0 của cuộn.


# PHẦN 18. BÀI TẬP TÍNH TAY

Thầy có thể bảo “tính thử cho thầy xem”. Làm từng bài rồi xem đáp án ở cuối.

- Số thô của con quay đọc được là 3275. Tốc độ xoay là bao nhiêu °/s? Và số thô gia tốc 8192 là bao nhiêu g?
- Tốc độ lấy mẫu của cảm biến khi chia tần số là 10? Khi chia tần số là 4?
- Gain 0,3, tightening T = 1,4. Xoay đều 2,0 °/s trong 1 s (100 mẫu). Con trỏ đi bao nhiêu điểm ảnh? Rồi tính cho 0,7 °/s trong 1 s.
- Xoay đều 20 °/s trong 0,5 s với gain 0,3. Con trỏ đi bao nhiêu điểm ảnh? Tương ứng xoay bao nhiêu độ?
- Mỗi mẫu tính ra 0,25 điểm ảnh. Sau bao nhiêu mẫu thì gửi được điểm ảnh đầu tiên (phần dư cộng dồn, làm tròn tới số nguyên gần nhất)? Mỗi giây gửi bao nhiêu điểm ảnh?
- Cuộn: sens = 2,0, dead = 2,5°. Nghiêng 6° thì tốc độ bao nhiêu nấc/s? Trung bình bao nhiêu nhịp thì gửi một nấc?
- Phục hồi I²C: 3 nhịp phát hiện, khởi tạo lại 33 ms, bỏ mẫu 80 ms. Tổng thời gian gián đoạn là bao nhiêu?
- Lắc: ngưỡng 150 °/s. Tốc độ xoay đo lần lượt: 160, 170, 100, 60, 50, 180 °/s (cách nhau 10 ms, trong 600 ms im lặng ở sau cú đầu). Có mấy sự kiện được phát? Sau khi hết 600 ms thì tốc độ phải hạ xuống dưới bao nhiêu mới mở khóa?
- Hàng đợi chặn click 4 mẫu. Mẫu đo ở nhịp t được gửi ở nhịp nào? Nếu nhấn nút ở nhịp t, những mẫu nào bị bỏ?
- Đồng hồ uint32_t mili-giây tràn sau bao nhiêu ngày?
- Độ dời tối đa mỗi nhịp là 127 điểm ảnh. Ở gain 0,3, tốc độ xoay nào làm bão hòa?

## Đáp án

| Bài | Đáp án và cách tính |
|---|---|
| 1 | 3275 / 65,5 = 50 °/s. 8192 / 8192 = 1 g. |
| 2 | Chia 10: 1125/11 = 102,27 Hz. Chia 4: 1125/5 = 225 Hz. |
| 3 | 2,0 ≥ 1,4 nên giữ nguyên: 0,3 × 2,0 = 0,6/mẫu → 60 điểm ảnh. Với 0,7: f = 0,7×0,7/1,4 = 0,35; 0,3 × 0,35 = 0,105/mẫu → khoảng 10,5 điểm ảnh (nếu không lọc sẽ là 0,3 × 0,7 × 100 = 21 điểm ảnh; tightening giảm còn một nửa vì f/ω = ω/T = 0,7/1,4 = 0,5). |
| 4 | 20 °/s ≥ 1,4: 0,3 × 20 = 6/mẫu; 50 mẫu → 300 điểm ảnh. Quay 20 × 0,5 = 10° → 10 × 30 = 300 điểm ảnh. Hai cách ra cùng kết quả. |
| 5 | Mẫu 1: 0,25 → làm tròn 0 (dư 0,25). Mẫu 2: 0,5 → làm tròn 1 (theo roundf, 0,5 làm tròn lên 1), dư −0,5. Mẫu 3: −0,25 → 0 …. Trung bình 0,25 điểm ảnh/mẫu → 25 điểm ảnh/giây. Điểm ảnh đầu tiên được gửi ở mẫu thứ 2. |
| 6 | (6 − 2,5) × 2 = 7 nấc/s → 0,07 nấc/nhịp → trung bình 1/0,07 ≈ 14 nhịp mới đủ một nấc. |
| 7 | 3×10 ms + 33 ms + 80 ms = 143 ms ≈ 0,14 s, dưới 0,15 s. |
| 8 | 160 ≥ 150: phát sự kiện đầu tiên, khóa lại và bắt đầu 600 ms im lặng. Trong 600 ms đó bộ nhận dạng bỏ qua mọi mẫu (170, 100, 60, 50, 180), nên chỉ có 1 sự kiện. Sau khi hết 600 ms, bộ nhận dạng vẫn đang khóa và chỉ mở khóa khi tốc độ hạ dưới 0,35 × 150 = 52,5 °/s. |
| 9 | Mẫu nhịp t gửi ở nhịp t+4 (trễ 40 ms). Nhấn ở nhịp t: bỏ cả 4 mẫu đang nằm trong hàng đợi (40 ms cuối) và ép đầu vào về 0 trong 250 ms. |
| 10 | 2³² ms = 4.294.967.296 ms ÷ 86.400.000 ms/ngày ≈ 49,7 ngày. |
| 11 | 127 điểm ảnh/nhịp = 12.700 điểm/giây; 12.700 / 30 điểm mỗi độ ≈ 423 °/s (test N6 dùng 450 °/s). |


# PHẦN 19. NHỮNG ĐIỀU PHẢI NÓI THẬT VÀ CÂU TRẢ LỜI MẪU

Thầy chấm cao khi bạn biết rõ giới hạn của sản phẩm. Học thuộc bảng dưới.

| Chủ đề | Câu trả lời mẫu (nói thật, không hạ thấp, không phóng đại) |
|---|---|
| Thiếu pin, LED, đo pin | “Phần pin và đo pin nhóm chưa lắp; mạch hiện chạy bằng cổng USB. Code LED có nhưng chưa kiểm vì chưa có LED, code đo pin chưa viết.” |
| Không có PCB | “Nhóm làm trên breadboard. Điểm yếu là tiếp xúc: cảm biến thỉnh thoảng mất trạng thái, nên firmware tự phục hồi dưới 0,15 s; muốn khắc phục gốc cần hàn perfboard hoặc làm PCB.” |
| Cảm biến vẫn mất trạng thái | “Số lần mất không giảm; nguyên nhân gốc là phần cứng. Phần mềm chỉ rút ngắn hậu quả từ 0,5–3 s xuống dưới 0,15 s.” |
| Chống run tay | “Em chưa làm bộ lọc run tay. Em đã làm chống trôi và lọc nhiễu cảm biến.” |
| Độ trễ, dòng điện, độ bền | “Chưa đo. Em biết các thành phần của độ trễ nhưng chưa có tổng số đo.” |
| Người dùng thử | “Do chính em đánh giá nên là đánh giá chủ quan, chưa thử với nhiều người.” |
| Hằng số | “Các hằng số cảm giác như gain, 40 ms, 150 ms, 250/350 ms lấy từ thử nghiệm của em, chưa tối ưu bằng đo hay khảo sát.” |
| Bias dư 0,3 °/s | “Đây là giới hạn đã biết, ghi thành test N7. Giải pháp đề xuất là hạ ngưỡng tự đo lại từ 0,5 xuống khoảng 0,2 °/s nhưng em chưa làm và chưa thử.” |
| Cử chỉ lắc | “Hai bộ nhận dạng đã kiểm bằng test trên máy tính; với bản firmware chốt em chưa thử lại trên board.” |
| Yaw | “Bộ lọc không quan sát được yaw nên yaw chỉ là tích phân con quay. Điều này chấp nhận được vì chuột điều khiển theo tốc độ xoay.” |
| Điện áp 3,3 V cho module | “Chạy ổn trên module của nhóm, nhưng datasheet chip quy định chân I/O 1,71–1,95 V nên độ bền lâu dài chưa được kiểm chứng.” |
| Flash 90 % | “Còn khoảng 131 KB, thêm tính năng lớn sẽ khó; có thể giảm log hoặc đổi bảng phân vùng.” |
| Test không phủ lớp app_ | “Lớp app_ cần phần cứng nên chỉ kiểm bằng log và thử trên board, không có test tự động.” |


## Lời kết: ba ý chính nếu bị hỏi “em học được gì”

- Lỗi thật chỉ lộ khi thử trên thiết bị thật: độ nhạy quá lớn, trục lắp lệch, hiệu chuẩn sai khi bật nguồn lúc đang cầm. Mỗi lỗi được đo, tìm nguyên nhân, sửa và kiểm lại bằng log.
- Tách mã thành lõi thuần và lớp ứng dụng cho phép kiểm thử thuật toán tự động, giúp sửa mạnh tay mà không sợ làm hỏng chức năng cũ.
- Phần cứng lỏng lẻo phải được bù bằng phần mềm tự phục hồi, nhưng chỉ phần cứng tốt (hàn chắc, tụ lọc nguồn) mới giải quyết được nguyên nhân gốc.
