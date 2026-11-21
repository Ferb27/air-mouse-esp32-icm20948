# HƯỚNG DẪN: TRANG WEB CẤU HÌNH AIR MOUSE

Trang: `tools/config_page/air_mouse_config.html` (một file duy nhất, không cần cài gì, không cần mạng). Viết 2026-10-22.

**Trạng thái trung thực:** logic trang (đọc/đổi/áp dụng/lưu/mặc định/báo lỗi/sự kiện) đã chạy thử với **board giả lập** trong trình duyệt (`HOST_TESTED`). **Chưa thử với board thật qua Web Serial** (`NOT_TESTED` trên phần cứng): lý do là board đang cắm ở laptop, còn trang phải chạy trên máy cắm board.

## Dùng thử không cần board
Mở file bằng Chrome hoặc Edge, bấm **Chế độ thử**. Trang dùng một board giả lập (cùng khoảng giá trị và quy tắc từ chối như firmware) để bạn làm quen giao diện; mọi thay đổi chỉ ở trong trang.

## Dùng với board thật (trên máy cắm board USB)
1. **Tắt server RFC2217** đang giữ cổng COM (cửa sổ `esp_rfc2217_server`: `Ctrl+C`), vì một cổng chỉ một chương trình dùng. Khi đó mình (Claude) từ PC sẽ không nối được cầu; dùng xong nhớ bật lại.
2. Mở `air_mouse_config.html` bằng **Chrome hoặc Edge** (Firefox/Safari không hỗ trợ Web Serial).
3. Bấm **Kết nối board (USB)**, chọn cổng (Silicon Labs CP210x), bấm Connect.
4. Mở cổng có thể làm board khởi động lại (khoảng 3 giây, hiệu chuẩn); **để board nằm yên**. Trang tự hỏi `@GET` cho tới khi board trả lời, rồi hiện các giá trị hiện tại.
5. Kéo thanh trượt (ô vàng = đã đổi nhưng chưa áp dụng). **Áp dụng thử** gửi `@SET` (đổi ngay, chuột dùng thử luôn, chưa lưu). **Lưu vào board** ghi vào flash (tắt nguồn bật lại vẫn giữ). **Mặc định** về giá trị gốc của firmware; **Đo lại bias** gửi `@CAL` (board phải nằm yên).
6. Phần "Trạng thái trực tiếp" hiện `[STATUS]` mỗi giây và các sự kiện nút (nhấn/nhả, lắc nhanh, bật/tắt chế độ cuộn): dùng để kiểm khi thử.

Nếu Chrome báo "không hỗ trợ Web Serial" khi mở trực tiếp file: mở bằng máy chủ cục bộ (`python -m http.server 8000` trong thư mục `tools/config_page`, rồi vào `http://localhost:8000/air_mouse_config.html`); `localhost` luôn là bối cảnh an toàn. (Mình chưa kiểm trường hợp mở trực tiếp file trên Chrome thật.)

## Preset (bộ thông số đã lưu)
- Phần đầu trang: danh sách preset. Có sẵn **Mặc định của firmware**; bạn thêm bao nhiêu preset cũng được.
- **+ Lưu thông số hiện tại thành preset mới**: chụp các giá trị đang hiển thị trên trang (17 thông số) và đặt tên (tối đa 40 ký tự, không trùng tên).
- Chọn một preset rồi **Áp dụng preset này**: đưa giá trị vào trang và gửi `@SET` cho board (đổi ngay, **chưa lưu vào flash của board**; muốn giữ thì bấm "Lưu vào board"). Ô "khác trang hiện tại ở ..." cho biết áp dụng sẽ đổi những mục nào.
- Thẻ preset nào trùng với giá trị đang chạy trên board sẽ có nhãn xanh **đang dùng trên board**.
- **Cập nhật preset này** ghi đè bằng giá trị đang hiển thị; **Đổi tên**, **Xóa** (có hỏi lại).
- **Xuất file** tải về `air_mouse_presets.json`; **Nhập file** thêm preset từ file (không xóa cái đang có, trùng tên thì tự thêm "(2)"; mục sai khoảng hoặc khóa lạ bị bỏ). Dùng để mang preset từ PC sang laptop hoặc gửi cho bạn.
- **Preset nằm trong trình duyệt của máy đang mở trang** (bộ nhớ cục bộ), không nằm trong board: xóa dữ liệu duyệt web là mất, nên xuất file để giữ. Nếu trình duyệt không cho lưu lâu dài (chế độ riêng tư...), trang hiện dòng cảnh báo và preset chỉ giữ tới khi đóng trang.
- Trạng thái: `HOST_TESTED` với board giả lập (tạo, trùng tên, áp dụng, cập nhật, đổi tên, xóa, xuất, nhập có mục lỗi, dữ liệu hỏng, lưu/tải qua bộ nhớ giả). Lưu lâu dài thật trong Chrome **chưa kiểm** (trình duyệt của Claude không có bộ nhớ cục bộ).
- Chưa làm: lưu preset **trong board** (để cắm sang máy khác vẫn còn), việc đó cần thêm vào firmware.

## Nếu có sự cố
- "Không mở được cổng": chương trình khác đang giữ cổng (server RFC2217, Arduino IDE, PlatformIO monitor...). Tắt nó.
- "Board không trả lời @GET": rút cắm cáp; hoặc firmware chưa phải bản có cấu hình (cần bản `2026-10-22_scroll_ref` trở lên).
- Banner vàng "phiên bản cấu hình X, trang viết cho 4": firmware và trang không cùng đời.
- Board từ chối giá trị: trang tô đỏ ô đó và nói rõ; board không đổi gì (một lần `@SET` là tất cả hoặc không gì cả).

## Giao thức (cho người sửa trang hoặc firmware)
Dòng văn bản, mỗi lệnh một dòng, trả lời một dòng bắt đầu `@`: `@GET` / `@SET k=v ...` / `@SAVE` / `@DEFAULTS` / `@CAL`. Chi tiết và khoảng giá trị: `firmware/include/air_config.h`. Thêm cài đặt mới: thêm vào `FIELDS` trong trang **và** trong `air_config.*` (tăng `AIR_CONFIG_VERSION`, đổi `EXPECTED_VERSION` trong trang).

## Gán nút và đảo chiều (firmware cấu hình phiên bản 5)
- Mục **Gán nút**: chọn chức năng cho nút trái (GPIO25), phải (GPIO26) và Mode (GPIO27): không làm gì / chuột trái / phải / giữa / Back / Forward / Mode. Hai nút có thể cùng một chức năng. Đổi trái ↔ phải cho người thuận tay trái.
- **Đảo chiều ngang / dọc** nằm ở thẻ Con trỏ.
- Trang cảnh báo nếu không còn nút nào là Mode (mất khóa con trỏ, lắc nhanh, cuộn) hoặc không còn nút nào là chuột trái.
- Dòng sự kiện hiện "Nút trái: nhấn → chuột phải" (vật lý → chức năng); ở **Chế độ thử** có 3 nút giả lập nhấn để xem.
- Preset chứa luôn cách gán nút và đảo chiều (17 thông số).
- Trạng thái: logic trang `HOST_TESTED` với board giả lập; firmware `HOST_TESTED` (34 test) và build SUCCESS; **chưa nạp, chưa thử với board thật** (`NOT_TESTED`).

## Đưa trang lên mạng (Cloudflare, gói miễn phí) để mở bằng một địa chỉ web
- Thư mục chuẩn bị sẵn: `tools/config_page/dist/` gồm `index.html` (bản sao của trang, thêm `noindex` để công cụ tìm kiếm không lập chỉ mục) và `_headers` (không lưu đệm, tắt đoán kiểu nội dung). **Sau mỗi lần sửa trang phải chép lại** `air_mouse_config.html` thành `dist/index.html` rồi đăng lại.
- **Cloudflare Pages, Direct Upload:** trên bảng điều khiển Cloudflare vào *Workers & Pages* → *Create* → *Pages* → tải lên (upload) thư mục `dist` → đặt tên dự án (ví dụ `airmouse-config`) → được địa chỉ `https://<tên>.pages.dev`. Hoặc dùng dòng lệnh: `npx wrangler pages deploy tools/config_page/dist --project-name=airmouse-config` (cần Node và đăng nhập `wrangler login`).
- Gói miễn phí đủ dùng: trang tĩnh nên lượt truy cập tới tệp tĩnh miễn phí và không giới hạn; mỗi site tối đa 20 000 tệp, mỗi tệp tối đa 25 MiB (theo tài liệu Cloudflare đọc ngày 2026-10-23). Trang chỉ có 1–2 tệp, vài chục KB.
- Web Serial cần HTTPS (hoặc `localhost`); `pages.dev` có HTTPS sẵn. Người dùng vào địa chỉ bằng **Chrome/Edge trên máy tính, cắm cáp USB từ board**, bấm Kết nối. Trang chạy hoàn toàn trong trình duyệt của người dùng; dữ liệu cấu hình nằm ở board, **không gửi gì về máy chủ**.
- **Preset lưu theo từng địa chỉ web**: preset tạo khi mở file trên máy (`file://`) sẽ không thấy ở `pages.dev`; dùng Xuất file / Nhập file để chuyển.
- Mặc định ai có địa chỉ cũng mở được trang; nó chỉ có tác dụng với board của chính họ cắm vào máy họ. Muốn hạn chế thì dùng Cloudflare Access (cần cấu hình thêm), hoặc không đăng lên mạng.

### Đã đăng (2026-10-23)
- Địa chỉ: **https://airmouse-config.embedded-sys.workers.dev**. Đăng bằng `wrangler` thành một **Worker phục vụ tệp tĩnh** (tên `airmouse-config`) trong tài khoản Cloudflare của người dùng, **không phải dự án Pages**: `wrangler pages ...` hiện chuyển sang Workers và báo lỗi khi tạo dự án Pages, nên dùng cách Workers Static Assets mà Cloudflare khuyến nghị.
- Kiểm tra sau khi đăng (từ PC, bằng yêu cầu HTTP): trả 200, 49 489 byte, có tiêu đề "Air Mouse Config", có nút kết nối, có `noindex`, tiêu đề `Cache-Control: no-cache` và `X-Content-Type-Options: nosniff` đúng như `_headers`. Chứng chỉ HTTPS mất khoảng 90 giây để sẵn sàng. **Chưa thử Web Serial trên địa chỉ này với board thật.**
- Đăng lại sau khi sửa trang: chép `air_mouse_config.html` thành `tools/config_page/dist/index.html` rồi chạy `npx wrangler deploy tools/config_page/dist --name airmouse-config --compatibility-date 2026-10-19` (đã đăng nhập `wrangler` bằng OAuth trên PC này).
- **Thay đổi đã xảy ra trong tài khoản Cloudflare khi đăng:** wrangler tự đăng ký **tên miền phụ workers.dev của tài khoản là `embedded-sys`** (trước đó tài khoản chưa có), và tạo Worker `airmouse-config`. Wrangler được cấp quyền OAuth khá rộng (Workers, D1, KV, zone, SSL...); thu hồi bằng `npx wrangler logout` và trong cài đặt tài khoản Cloudflare.

### Địa chỉ ngắn trên pages.dev (2026-10-23)
- Địa chỉ chính: **https://airmouse-config.pages.dev**. Mình hỏi về `airmouse-config.workers.dev` nhưng địa chỉ Worker luôn có dạng `<tên-worker>.<tên-miền-phụ-tài-khoản>.workers.dev` (hai nhãn), nên không thể chỉ có một nhãn như vậy; dự án **Pages** thì có dạng một nhãn `<tên>.pages.dev`.
- Dự án Pages tạo bằng `wrangler pages project create airmouse-config --production-branch=main --force` (cần `--force` đúng một lần vì wrangler mặc định chuyển Pages sang Workers). Đăng: `npx wrangler pages deploy tools/config_page/dist --project-name=airmouse-config --branch=main --commit-dirty=true` (**không** dùng `--force` nữa).
- Kiểm sau khi đăng: HTTP 200, 49 489 byte, đúng tiêu đề, `noindex`, `Cache-Control: no-cache`, `nosniff`.
- Địa chỉ Worker cũ `https://airmouse-config.embedded-sys.workers.dev` vẫn mở được (cùng nội dung) cho tới khi xóa Worker `airmouse-config`. **Hai bản đăng độc lập**: sửa trang phải đăng lại cho từng bản đang dùng.

### Đã xóa Worker cũ (2026-10-23)
- Worker `airmouse-config` (bản đăng đầu tiên, địa chỉ `...embedded-sys.workers.dev`) **đã xóa** bằng `wrangler delete airmouse-config`. Địa chỉ đó giờ trả 404. Danh sách Worker trong tài khoản chỉ còn 2 Worker của dự án khác. **Chỉ còn một bản đăng: https://airmouse-config.pages.dev** (dự án Pages), đã kiểm trả 200.
- Tên miền phụ workers.dev của tài khoản (`embedded-sys`) **vẫn còn** (xóa Worker không xóa nó; chỉ đổi được tên trong bảng điều khiển).

### Chú thích thêm trên trang (2026-10-23, theo phản hồi người dùng đã thử với board thật)
- **Phản hồi:** thử trang với board thật, "rất ok" (`USER_FEEDBACK`, một người, một buổi); nút "Đọc lại" và các ô chọn khó hiểu với người chưa dùng. Chi tiết các bước đã thử mình không có (người dùng chỉ báo tổng quát).
- **Đã sửa:** mỗi nút ở thanh dưới và ở phần preset có **dòng chú thích hiển thị sẵn** dưới nút (nút "Đọc lại" đổi thành "Đọc lại từ board"); mỗi thanh trượt có hai nhãn đầu mút ("← chậm, chính xác" ... "nhanh, quét xa →"); mỗi ô bật/tắt hiện câu mô tả trạng thái hiện tại ("Bật: ... / Tắt: ..."); mỗi ô chọn (Tâm cuộn, ba nút) hiện đoạn mô tả của lựa chọn đang chọn; nhật ký thô có giải thích.
- **Màn hình hẹp (≤ 640 px):** thanh nút chỉ hiện nút, có dòng "ℹ Hiện giải thích các nút" để mở chú thích (tránh thanh nút che nội dung).
- Đã đăng lại lên https://airmouse-config.pages.dev (200, 54 406 byte, có chú thích mới). Logic trang không đổi; kiểm bằng board giả lập (áp dụng, gán nút, lật cờ, đổi tâm cuộn).
