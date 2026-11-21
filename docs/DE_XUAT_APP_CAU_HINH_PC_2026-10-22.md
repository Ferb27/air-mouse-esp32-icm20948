# ĐỀ XUẤT: APP TRÊN PC ĐỂ CHỈNH ĐỘ NHẠY VÀ GÁN CHỨC NĂNG NÚT

> Viết 2026-10-22 theo gợi ý của bạn người dùng ("đặt mình vào vị trí người dùng"). **Đây là đề xuất và khảo sát, chưa có dòng code nào** (`NOT_TESTED`). Nguồn web đọc qua bản tóm tắt tự động ([B]), chưa đọc bản gốc; chỗ nào là suy luận thì ghi rõ.

## 1. Đặt mình vào vị trí người dùng: hiện tại thiếu gì?

Người dùng mua chuột về, cắm vào, ghép Bluetooth, dùng. Họ không biết serial, không biết gõ `+` vào cửa sổ log. Đối chiếu với code hiện tại:

| # | Người dùng muốn | Hiện tại (đọc từ code) | Mức |
| --- | --- | --- | --- |
| 1 | Chỉnh độ nhạy bằng thanh trượt, **tắt nguồn bật lại vẫn nhớ** | Chỉ chỉnh được bằng lệnh `+`/`-` qua serial; **không lưu**, reset là về gain 0.3 (`app_serial_cmd.cpp`, `motion_pipeline.cpp`) | Thiếu nặng |
| 2 | Chỉnh riêng ngang/dọc, đảo chiều | Có `gx`, `gy` trong code nhưng lệnh `+`/`-` đổi cả hai cùng lúc; đảo dấu cố định trong pipeline | Thiếu |
| 3 | **Cuộn trang** | `bleMouse.move(move_x, move_y, 0)`: tham số cuộn luôn bằng 0. **Chưa có cuộn** (`app_ble.cpp:52`) | Thiếu nặng (chuột mà không cuộn được) |
| 4 | Gán lại nút (vd GPIO26 thành chuột giữa, Mode thành cuộn) | Cố định: GPIO25 = trái, 26 = phải, 27 = Mode | Thiếu |
| 5 | Chọn thuận tay trái/phải (đổi trái-phải) | Không có | Thiếu nhỏ |
| 6 | Chỉnh độ nhạy lắc nhanh, độ trễ chống click | Có lệnh `y Y < >`, **không lưu** | Thiếu |
| 7 | Xem pin, trạng thái kết nối | LED GPIO32 và đo pin GPIO34 chưa có code | Ngoài phạm vi app |
| 8 | Đặt lại mặc định / lưu nhiều cấu hình (game, trình chiếu) | Không có | Để sau |

Hai việc nên làm trước vì người dùng chạm vào ngay: **(1) lưu cấu hình** và **(3) cuộn trang**. App đẹp mà không lưu được cấu hình thì vô nghĩa.

## 2. Sản phẩm tương tự làm gì (để chọn cái đáng làm)

- **JoyShockMapper** (điều khiển bằng gyro cho tay cầm) cho chỉnh được: độ nhạy (`GYRO_SENS`, hai giá trị = riêng X/Y), độ nhạy theo tốc độ (`MIN/MAX_GYRO_SENS` kèm ngưỡng), cutoff, làm mượt (`GYRO_SMOOTH_*`), đảo chiều (`GYRO_INVERT`, `GYRO_INV_X/Y`), nút bật/tắt gyro (`GYRO_ON`/`GYRO_OFF`, tương ứng nút Mode của mình), gán từng nút, độ nhạy cuộn (`SCROLL_SENS`). Cấu hình là file văn bản. [B]
- **VIA/Vial** (bàn phím QMK): web app dùng WebHID, đổi phím **không cần nạp lại firmware**; thay đổi lưu trong bộ nhớ của bàn phím nên cắm sang máy khác vẫn giữ. [B] Đây là mô hình nên học: *firmware lưu cấu hình, app chỉ là giao diện để sửa*.
- **Phần mềm chuột Logitech/Razer** (chung): nhiều mức DPI bấm nút chuyển, nút DPI tạm thời giảm độ nhạy, profile lưu theo bộ nút + DPI. [B]
- Không tìm được tài liệu phần mềm của chuột bay/air mouse thương mại (Gyration, Logitech cũ): chỗ này **chưa có nguồn**, không suy diễn.

Rút ra: tập chỉnh hợp lý cho chuột bay là **độ nhạy X/Y, đảo chiều, ngưỡng lắc, chống click, gán nút, cuộn**. Làm mượt/gia tốc/profile để sau.

## 3. Danh sách thông số đề xuất cho app

Giá trị mặc định lấy từ code hiện tại.

| Thông số | Mặc định | Khoảng | Lưu ở | Ghi chú |
| --- | --- | --- | --- | --- |
| `gain_x`, `gain_y` | 0.3 | 0.02–3.0 | NVS | Hiện đã có `motion_setGain(gx, gy)`; hiển thị thêm "≈ điểm/độ" (= gain × 100) |
| `invert_x`, `invert_y` | 0, 0 | 0/1 | NVS | Cần thêm cờ vào pipeline |
| `flick_dps` | 150 | 40–600 | NVS | Đã có `app_flick_adjust` |
| `flick_enable` | 1 | 0/1 | NVS | Pipeline đã cho tắt cử chỉ |
| `click_guard_ms` | 40 | 0–100 | NVS | Đã có `app_buttons_adjust_lookahead` |
| `recenter_ms` | 150 | 50–500 | NVS | Hằng `APP_RECENTER_SETTLE_MS` |
| `btn_left`, `btn_right`, `btn_mode` | L, R, Mode | xem mục 4 | NVS | Mới |
| `scroll_sens` | (chọn sau khi đo) | | NVS | Mới, cần tính năng cuộn |
| `swap_lr` | 0 | 0/1 | NVS | Mới, tiện cho người thuận tay trái |

Hiệu chuẩn bias (`c`) vẫn là nút bấm trong app ("Đo lại khi đặt trên bàn"); bias **không lưu** vì phụ thuộc nhiệt độ, mỗi lần bật đo lại.

## 4. Gán nút: làm được những gì

Thư viện hiện dùng (`ESP32 BLE Mouse` 0.3.1, t-vk) gửi được: nút trái, phải, giữa, Back, Forward và con lăn. **Không gửi được phím bàn phím** (Ctrl+C, Alt+Tab...); muốn thế phải đổi sang thư viện kết hợp chuột + phím hoặc tự khai báo HID report, rủi ro cao hơn, để sau.

Danh sách hành động cho mỗi nút (đề xuất):

| Hành động | Ý nghĩa | Làm được ngay? |
| --- | --- | --- |
| Left / Right / Middle | Chuột trái/phải/giữa | Có (Middle chưa dùng trong code nhưng thư viện có) |
| Back / Forward | Lùi/tiến trang | Có (đang dùng cho lắc nhanh) |
| Clutch (giữ = khóa con trỏ) | Hành vi nút Mode hiện nay | Có |
| Scroll (giữ + nghiêng = cuộn) | Giữ nút thì chuyển chuyển động dọc thành cuộn | Cần làm thêm |
| Precision (giữ = giảm nhạy ×0.3) | Giống nút DPI-shift | Cần làm thêm, đơn giản |
| DPI cycle | Nhấn đổi qua 3 mức nhạy | Cần làm thêm |
| Disabled | Không làm gì | Có |

Mode (GPIO27) đang gộp ba việc (Clutch, cân lại, cử chỉ lắc). Nếu cho gán lại nút Mode phải tách rõ: "hành động của nút" và "cử chỉ lắc khi giữ Mode". Đề xuất giữ **cử chỉ gắn với nút nào được gán `Clutch`** để không phá logic đã test.

## 5. Chọn kiến trúc: app nói chuyện với board bằng cách nào?

| Hướng | Cách hoạt động | Ưu | Nhược |
| --- | --- | --- | --- |
| **A. Trang web dùng Web Serial** (một file HTML, mở bằng Chrome/Edge) | Cắm USB, bấm "Kết nối", trang đọc/ghi cấu hình bằng dòng văn bản qua cổng COM | Không cài gì; dùng ngay cổng USB đang có; không đổi stack BLE; phần web đưa vào báo cáo dễ | Phải cắm cáp khi chỉnh; chỉ Chrome/Edge (Web Serial cần Chromium ≥ 89) [B] |
| **B. Web Bluetooth + dịch vụ GATT riêng** | Chỉnh không dây qua BLE | Không cần cáp; giống chuột thương mại | Thư viện `ESP32 BLE Mouse` không để thêm dịch vụ dễ dàng (cần sửa thư viện hoặc đổi sang NimBLE); flash đã 89 %; Web Bluetooth chặn dịch vụ HID chuẩn nhưng có vẻ cho dịch vụ riêng [B, chưa kiểm]; cách Windows xử lý thiết bị đã ghép HID **chưa có nguồn**; Firefox/Safari không hỗ trợ [B] |
| **C. App Windows riêng (Python + pyserial, hoặc Electron)** | Giao thức như A, nhưng là chương trình cài | Mở cổng COM kiểm soát được DTR/RTS; không phụ thuộc Chrome | Phải cài; viết GUI tốn công hơn trang web |
| **D. Board tự phát Wi-Fi + trang cấu hình** | Kết nối điện thoại/PC vào Wi-Fi của board | Không cần cáp | Flash 89 %, Wi-Fi + BLE cùng chạy làm RAM/nhiễu thêm; **không khuyên** |

**Đề xuất: làm A trước**, thiết kế giao thức đủ đơn giản để sau này đổi sang B hoặc C mà không viết lại firmware (mục 6). Lý do: rẻ nhất, dùng đúng phần cứng đang có, và học theo VIA (firmware giữ cấu hình, app chỉ là giao diện). B là mục tiêu "sản phẩm thật" nhưng nên ghi vào mục hướng phát triển, vì khối lượng và rủi ro lớn hơn.

Hai lưu ý thực tế:
- Khi board đang cắm ở laptop (cầu RFC2217), **trang Web Serial phải mở bằng Chrome trên laptop**, không dùng được từ PC qua mạng. Phát triển giao thức vẫn làm được ở PC với `capture_serial.py`.
- Mở cổng từ trình duyệt có thể làm board **reset** (cầu RFC2217 luôn reset; cổng cục bộ phụ thuộc DTR/RTS). Đây là suy luận từ kinh nghiệm bench, **chưa thử với Web Serial**. App nên báo "board khởi động lại, đặt yên 3 giây" sau khi kết nối.

## 6. Giao thức đề xuất (dòng văn bản, không cần thư viện JSON)

Log hiện tại và `[STATUS]` vẫn chạy. Dòng giao thức mở đầu bằng `@` để trang dễ lọc:

```
PC  -> board:  @GET                       board -> PC:  @CFG gain_x=0.300 gain_y=0.300 flick_dps=150 ...
PC  -> board:  @SET gain_x=0.45            board -> PC:  @OK gain_x=0.450        (áp dụng ngay, chưa lưu)
PC  -> board:  @SAVE                       board -> PC:  @OK saved
PC  -> board:  @DEFAULTS                   board -> PC:  @OK defaults
PC  -> board:  @CAL                        board -> PC:  @OK calibrated  (hoặc @ERR not-still)
sai khóa / ngoài khoảng:                   board -> PC:  @ERR range gain_x
```

Nguyên tắc: board **kiểm khoảng và từ chối** giá trị sai (không tin trang web); cấu hình áp dụng ngay để người dùng thử rồi mới `@SAVE`; ghi NVS qua `Preferences` (chỉ khi `@SAVE`, tránh mòn flash); lưu kèm số phiên bản cấu hình, sai phiên bản thì dùng mặc định.

## 7. Kế hoạch từng bước (mỗi bước nạp và kiểm riêng)

| Bước | Việc | Cách kiểm |
| --- | --- | --- |
| P0 | Tách **cấu hình thành một struct** + bộ phân tích dòng `@...` thành **lõi thuần** (không gọi Arduino) | Thêm test trên máy tính (N15...: khoảng giá trị, từ chối khóa sai, phiên bản) |
| P1 | Lớp `app_config_store`: đọc/ghi NVS, nạp lúc khởi động, lệnh `@GET/@SET/@SAVE/@DEFAULTS` | Nạp, tắt/bật nguồn, xem log có giữ giá trị không (`BENCH_VERIFIED`) |
| P2 | Cuộn trang (nút giữ + nghiêng) + gán nút | Thử trên trình duyệt thật (`USER_FEEDBACK`) |
| P3 | Trang web Web Serial: thanh trượt, danh sách gán nút, nút "Đo lại", "Lưu", "Mặc định", đồ thị tốc độ thời gian thực từ `[STATUS]` | Thử với người dùng thật |
| P4 | Tài liệu và đưa vào báo cáo; (tùy chọn) hướng B BLE | |

Ngân sách tài nguyên: Flash đang 89.0 % (còn khoảng 144 KB); `Preferences` có sẵn trong framework, thêm cỡ vài chục KB là cùng (ước lượng, chưa build). Nên build sau P1 để biết con số thật.

### Trạng thái thực hiện (cập nhật 2026-10-22)

- **P0 đã code, `HOST_TESTED`:** `firmware/src/air_config.cpp` + `include/air_config.h` (6 thông số: `gain_x`, `gain_y`, `flick_dps`, `flick_enable`, `click_guard_ms`, `recenter_ms`; lệnh `@GET/@SET/@SAVE/@DEFAULTS/@CAL`); test N15–N19, cả bộ **29/29 PASS**, gồm 60 000 dòng ngẫu nhiên không làm hỏng cấu hình.
- **P1 đã code, build SUCCESS** (Flash 89.5 %, RAM 12.3 %): `app_config_store.cpp` (NVS), dòng `@...` trong `app_serial_cmd.cpp`, nạp cài đặt lúc khởi động trong `app_boot.cpp`.
- **P1 đã nạp và thử trên board (`BENCH_VERIFIED`, một lần chạy)**, bản `release/2026-10-22_config_nvs/` (`firmware.bin` SHA-256 bắt đầu `c114a794987c0887`), log `raw_logs/config_nvs_test_2026-10-22.log`: lần boot đầu báo "nothing stored yet -> defaults"; `@SET gain_x=0.45 gain_y=0.45 flick_dps=180` rồi `@SAVE`; sau reset board tải lại đúng các giá trị đó; 9 dòng sai đều bị từ chối và không đổi gì; dòng `@` dang dở bị bỏ sau 2 s (`@ERR timeout`) và lệnh `?` hoạt động lại; lệnh `+` cũ được `@GET` thấy (0.45 → 0.54); `@DEFAULTS` + `@SAVE` rồi reset giữ được mặc định; `@CAL` trả `OK calibrated`. Board đang lưu **giá trị mặc định**.
- **Chưa kiểm:** `recenter_ms` và `flick_enable` không có hàm đọc ngược nên chưa chứng minh được là đã áp vào chuyển động thật; chưa thử con trỏ thật với gain 0.45 (`USER_FEEDBACK`); chưa thử mất điện giữa lúc `@SAVE`.
- **P2a (cuộn trang):** nhấn đúp Mode rồi giữ lần hai (cách C). Bản đầu cuộn theo **tốc độ xoay** (con trỏ nghiêng bao nhiêu thì cuộn bấy nhiêu); người dùng cầm thử báo: nghiêng xuống có giới hạn nên không cuộn được dài. **Đã đổi sang cuộn theo góc (hướng A, kiểu cần điều khiển):** góc nghiêng so với tư thế lúc nhấn quyết định tốc độ, giữ nghiêng thì cuộn mãi, về tư thế gốc thì dừng. Khóa cài đặt: `scroll_enable`, `scroll_sens` (1.0 nấc/giây trên mỗi độ vượt vùng chết, **giá trị đoán**), `scroll_dead` (4°, **giá trị đoán**), `scroll_invert`, `hscroll` (lăn cổ tay sang trái/phải để cuộn ngang, mặc định tắt); `AIR_CONFIG_VERSION` = 3. Test N20–N22, cả bộ **32/32 PASS** (`HOST_TESTED`). Build SUCCESS (Flash 89.7 %). **Chưa nạp, chưa thử tay** (`NOT_TESTED` trên phần cứng). Hướng "cuộn khi con trỏ chạm mép màn hình" (kiểu điều khiển TV) **không làm được thuần firmware** vì chuột không biết vị trí con trỏ trên màn hình; xem lý do ở trao đổi 2026-10-22.
- **P2a, vòng 3 (người dùng báo):** cuộn theo góc đã dễ dùng hơn (hạ vùng chết 4° → 2.5° và độ nhạy 1.0 → 2.0 cho đỡ mỏi cổ tay, `USER_FEEDBACK`: "đã đỡ mỏi tay"); nhưng khi nhấn đúp Mode thì tay lệch khỏi tư thế thoải mái nên tư thế gốc (lấy lúc nhấn) bị sai, cuộn không ổn. **Đã đổi: tư thế gốc là tư thế thoải mái trước khi nhấn đúp** (`scroll_ref=0` mặc định; `scroll_ref=1` quay về cách cũ để so sánh), có 100 ms yên lặng và tăng tốc dần 200 ms để không bị nhảy. Mặc định mới `scroll_sens=2.0`, `scroll_dead=2.5`; `AIR_CONFIG_VERSION` = 4. Test N20–N23, cả bộ **33/33 PASS** (`HOST_TESTED`); build SUCCESS (Flash 89.8 %). **Chưa nạp, chưa thử tay** với cách mới.
- **P2b (gán nút + đảo chiều X/Y) đã code:** `button_map.*`, 5 khóa mới `btn_left`, `btn_right`, `btn_mode`, `invert_x`, `invert_y`; `AIR_CONFIG_VERSION` = 5; nhật ký nút đổi thành `[BTN] LEFT down -> MIDDLE`. Test N24, cả bộ **34/34 PASS** (`HOST_TESTED`); build SUCCESS (Flash 89.9 %, RAM 12.4 %). **Chưa nạp, chưa thử tay** (`NOT_TESTED`). Trang web đã có mục Gán nút và đảo chiều (thử với board giả lập).
- Khoảng cho phép đã chốt trong code: `recenter_ms` 50–500, `click_guard_ms` 0–100 (làm tròn về bội của 10).

## 8. Rủi ro và điều chưa biết

- Web Serial và Web Bluetooth đều **chỉ Chrome/Edge** [B]. Nếu thầy chấm bằng máy khác trình duyệt thì cần hướng C.
- Chưa thử Web Serial trên Windows với board này (có reset khi mở không, tốc độ có ổn không).
- Lưu cấu hình ghi NVS: nếu mất điện giữa chừng, `Preferences` an toàn ở mức khóa-giá-trị nhưng phải có giá trị mặc định dự phòng.
- Sửa pipeline (đảo chiều, precision, scroll) có thể động tới 24 test; mỗi thay đổi phải thêm test và chạy lại cả bộ.
- Cuộn trang cần quyết định kiểu cuộn (tốc độ theo độ nghiêng hay từng nấc), nên thử trên tay trước.

## 9. Nguồn (mức [B]: đọc qua tóm tắt tự động)

- JoyShockMapper README: <https://github.com/Electronicks/JoyShockMapper/blob/master/README.md> (tên thiết lập gyro, X/Y riêng, cuộn, nút bật/tắt gyro)
- VIA technical / usage: <https://docs.keeb.io/via-technical>, <https://docs.keeb.io/via> (WebHID, lưu cấu hình trong bàn phím)
- Web Serial: ESP32 Device Manager <https://github.com/csiiiv/esp32-device-manager> (ví dụ trang cấu hình qua Web Serial, chỉ tham khảo); Preferences/NVS <https://zbotic.in/esp32-preferences-library-non-volatile-storage-nvs-guide/>
- Web Bluetooth chặn dịch vụ HID: thảo luận W3C <https://lists.w3.org/Archives/Public/public-web-bluetooth-log/2018Apr/0040.html>; trình duyệt hỗ trợ: <https://caniuse.com/web-bluetooth>
