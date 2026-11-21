# NGHIÊN CỨU: CHỐNG RUNG TAY CHO CON TRỎ (remote TV / chuột bay làm thế nào)

> **Quyết định của người dùng (2026-10-22): hướng này chỉ là THỬ NGHIỆM, ưu tiên thấp.** Lý do: tay run thì chuột vẫn dùng bình thường, không phải lỗi chặn việc dùng. Nếu làm thì: mặc định **tắt** (`smooth_fc = 0`, hành vi y hệt hiện tại), làm sau các việc chính, đo run tay (`@REC`) trước khi chọn số, và không ảnh hưởng 33 test đang có.

> Viết 2026-10-22. Đây là **khảo sát và đề xuất**, chưa có dòng code nào (`NOT_TESTED`). Nguồn web đọc qua bản tóm tắt tự động ([B]); chỗ nào là con số ước lượng của mình thì ghi "ước lượng". Phản hồi người dùng: tay run nên con trỏ rung theo ở chế độ thường, vẫn dùng được; remote TV rung ít hơn nhiều (`USER_FEEDBACK`, một người, một buổi).

## 1. Hiện tại firmware lọc gì? (đọc từ `motion_pipeline.cpp`)

| Khâu | Tác dụng lên rung tay |
| --- | --- |
| Cảm biến: bộ lọc số trong chip, cắt 51.2 Hz | **Không** chặn run tay (run tay 4–12 Hz nằm dưới 51 Hz, đi qua nguyên vẹn) |
| Tightening (ngưỡng 1.4 °/s) | Chỉ giảm các chuyển động **rất chậm** (< 1.4 °/s). Run tay có tốc độ quay lớn hơn nhiều (xem dưới) nên **đi qua** |
| Khóa đứng yên (0.4 °/s trong 300 ms) | Chỉ khi tay gần như bất động. Tay run thì không bao giờ vào trạng thái này |
| Bộ chặn click 40 ms | Chỉ liên quan lúc nhấn nút |

Kết luận: **chưa có bộ lọc nào nhắm vào run tay.** Đây là lý do con trỏ rung theo (và cũng là điểm khác với câu hỏi thầy về "bộ lọc nuốt chuyển động nhỏ": tightening không nuốt chuyển động nhỏ do run, vì run quá nhanh).

## 2. Run tay "to" cỡ nào? (ước lượng, chưa đo)

- Run tay sinh lý có hai đỉnh quanh 2–4 Hz và 8–12 Hz; đỉnh 8–12 Hz tăng khi cố giữ chính xác (nghiên cứu gia tốc kế ngón tay). [B]
- Nếu góc rung là hình sin biên độ A (độ) tần số f (Hz) thì **tốc độ quay đỉnh = 2π·f·A**. Ví dụ A = 0.1° ở 10 Hz cho khoảng 6 °/s; A = 0.3° cho khoảng 19 °/s (**ước lượng**, biên độ thật của bạn chưa đo).
- Biên độ con trỏ trên màn hình = A × (số điểm trên mỗi độ) = A × (gain × 100). Với gain 0.3 (30 điểm/độ): A = 0.1° thì khoảng 3 điểm; A = 0.3° thì khoảng 9 điểm (ước lượng). Đủ thấy bằng mắt.
- So với ngưỡng tightening 1.4 °/s thì 6–19 °/s lớn gấp 4–13 lần, nên tightening không giúp gì.

## 3. Người ta làm thế nào

| Cách | Mô tả | Nguồn / mức tin |
| --- | --- | --- |
| **Hillcrest Labs (Freespace)**: nền công nghệ của Loop Pointer và được Logitech cấp phép cho chuột bay | Phân biệt chuyển động có chủ ý với run tay tự nhiên; **đo run riêng của từng người và khử động**, thay vì lọc cả dải để khỏi mất độ chính xác | Thông cáo/bài đánh giá năm 2009–2010 [B]. Chi tiết thuật toán **không công bố** trong kết quả tìm được |
| **Bộ lọc 1€ (Casiez, CHI 2012)** | Lọc thông thấp bậc 1 nhưng **tần số cắt tự thay đổi theo tốc độ**: chuyển động chậm thì lọc mạnh (hết rung), chuyển động nhanh thì lọc nhẹ (không trễ). Hai tham số: `fcmin` (tần số cắt tối thiểu, bắt đầu khoảng 1 Hz) và `beta` (độ tăng theo tốc độ, bắt đầu 0.001–0.0001). Cách chỉnh: `beta = 0`, chỉnh `fcmin` lúc giữ yên cho hết rung, rồi tăng `beta` cho hết trễ lúc di chuyển nhanh. Tác giả báo ít trễ hơn các bộ lọc khác ở cùng mức giảm rung | Trang tác giả + bài báo [B]; có thư viện Arduino chính thức |
| **IBM (bằng sáng chế US6561993)**: bộ lái thiết bị trỏ cho người run tay | Đo phổ tần số của người dùng (cho họ giữ yên trên mục tiêu nhỏ, bám theo mục tiêu), tính hệ số bộ lọc số, lưu thành hồ sơ. Coi < 2 Hz là cố ý, > 4 Hz là run | Bằng sáng chế [B], ví dụ cho run 5 Hz, **không phải** run sinh lý 8–12 Hz nên không áp dụng nguyên con số |
| **Làm mượt trong các công cụ gyro** (JoyShockMapper: `GYRO_SMOOTH_THRESHOLD`, `GYRO_SMOOTH_TIME`) | Làm mượt chỉ khi chuyển động nhỏ, tăng dần ngưỡng | README JoyShockMapper (đã đọc ở phần trước) [B] |

Đánh đổi chung: lọc mạnh hơn thì **trễ hơn**; một nghiên cứu năm 2009 về nhiệm vụ trỏ kết luận độ trễ ảnh hưởng hiệu suất nhiều hơn một chút rung nhỏ [B]. Bộ lọc 1€ và làm mượt theo ngưỡng sinh ra để giải đúng tình huống này: **chỉ lọc mạnh lúc chậm** (lúc đang nhắm), nhẹ lúc nhanh (lúc đang di chuyển).

## 4. Đề xuất cho Air Mouse

**Hướng chính: bộ lọc kiểu 1€ áp lên tốc độ quay của con quay hồi chuyển, trước bước tightening và nhân gain.**
- Tốc độ quay ω đã là "vận tốc", nên dùng chính độ lớn |ω| (đã lọc) làm "tốc độ" để chỉnh tần số cắt: `fc = fcmin + beta · |ω|`.
- Gợi ý khởi đầu, **để chỉnh theo tay bạn**: `fcmin` khoảng 2–3 Hz, `beta` khoảng 0.03–0.1 Hz mỗi °/s (**con số đoán**). Với bộ lọc bậc 1, `fcmin = 2 Hz` làm tín hiệu 10 Hz còn khoảng 20 % biên độ (tính từ công thức, khoảng −14 dB); trễ khoảng 80 ms ở tốc độ rất chậm, nhưng ở tốc độ nhanh (vd 60 °/s) tần số cắt tăng lên khoảng 5–8 Hz nên trễ giảm còn 20–30 ms.
- Hai cài đặt mới trong giao thức `@`: `smooth_fc` (0 = tắt) và `smooth_beta`, để bạn thử A/B ngay trên board bằng `@SET`, không cần nạp lại.
- Lõi thuần, thêm test trên máy tính: (1) tín hiệu 10 Hz giảm đúng mức dự kiến khi chậm; (2) quay có chủ ý đều không bị mất, độ trễ đo được nằm trong giới hạn; (3) tắt (`smooth_fc = 0`) thì kết quả **y hệt** hiện tại (hồi quy 33 test cũ).

**Việc nên làm TRƯỚC khi chọn số: đo run tay của bạn** (chuẩn nhất, giống bước đầu của IBM/Hillcrest). Hiện log chỉ có `[STATUS]` mỗi giây nên không thấy được run 4–12 Hz.
1. Thêm lệnh ghi thô `@REC <giây>`: in tốc độ quay 3 trục ở 100 Hz (khoảng 3 KB mỗi giây, vừa với 115200 baud).
2. Bạn cầm board như lúc dùng chuột thường, **cố giữ con trỏ trên một điểm** 10 giây.
3. Mình phân tích phổ tần số (FFT) bằng Python ngoài firmware: biết tay bạn run ở tần số nào, biên độ bao nhiêu (`BENCH_VERIFIED`), rồi **kiểm bộ lọc trên chính dữ liệu đó** trước khi nạp.
4. Chọn `fcmin`, `beta` từ số đo, nạp, bạn thử lại.

**Các hướng khác (để sau, nếu 1€ chưa đủ)**
- **Lọc chặn dải (notch) đúng tần số run của người dùng**: sát với cách Hillcrest/IBM, ít làm trễ hơn lọc thông thấp, nhưng phải đo riêng từng người và làm thêm một chế độ hiệu chỉnh. Tốn công hơn nhiều.
- **Làm mượt bằng trung bình trượt vài mẫu**: đơn giản nhưng lọc kém hơn và trễ cố định, không thích ứng theo tốc độ. Không ưu tiên.
- **Vùng chết lớn hơn / khóa đứng yên mạnh hơn**: **không hiệu quả** với run tay vì tay run không bao giờ "đứng yên" theo cảm biến.

## 5. Rủi ro và điều chưa biết

- Biên độ và tần số run thật của bạn **chưa đo**; mọi con số ở mục 2 và gợi ý `fcmin`, `beta` là ước lượng.
- Lọc có thể làm cảm giác con trỏ "nặng" hoặc trễ khi nhắm chậm; vì thế có `smooth_fc = 0` để so, và sẽ cần bạn cầm thử.
- Tác động lên các phần đã có: cử chỉ lắc nhanh dùng tốc độ quay (ngưỡng 150 °/s) nên cần giữ phát hiện cử chỉ trên tín hiệu **chưa lọc** hoặc kiểm lại ngưỡng; cuộn theo góc dùng ước lượng tư thế nên không bị ảnh hưởng. Phải có test cho cả hai.
- Flash đang 89.8 %; bộ lọc 1€ chỉ vài trăm byte.
- Hillcrest: thuật toán cụ thể không công bố; không nên nói là mình "làm giống Hillcrest", chỉ nói cùng ý tưởng (lọc theo tốc độ, tách chuyển động có chủ ý khỏi run).

## 6. Nguồn ([B]: đọc qua tóm tắt tự động)

- Hillcrest Labs Loop Pointer (khử run tay, đo run từng người): <https://hothardware.com/news/hillcrest-labs-introduces-inair-mouse-for-tv>, <https://newatlas.com/hillcrest-loop-mouse-tv-remote/12013/>
- Bộ lọc 1€: trang tác giả <https://gery.casiez.net/1euro/> (cách chỉnh), bài báo <https://hal.archives-ouvertes.fr/hal-00670496>, mã nguồn <https://github.com/casiez/OneEuroFilter>
- IBM, "Device driver system for minimizing adverse tremor effects during use of pointing devices": <https://patents.google.com/patent/US6561993>
- Đánh đổi rung và độ trễ khi trỏ (Pavlovych 2009): <https://vvise.iat.sfu.ca/pubs/pavlovych2009tradeoff>
- Run sinh lý 2–4 Hz và 8–12 Hz (gia tốc kế ngón tay): <https://research.bond.edu.au/en/publications/changes-in-the-dynamics-of-tremor-during-goal-directed-pointing/>
- Làm mượt gyro trong JoyShockMapper: <https://github.com/Electronicks/JoyShockMapper/blob/master/README.md>
