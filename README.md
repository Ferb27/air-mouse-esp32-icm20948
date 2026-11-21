# Air Mouse — chuột không gian BLE dùng ESP32 + ICM-20948

Đồ án môn **Hệ thống nhúng** (HCMUTE). Một chiếc chuột cầm trên tay: xoay cổ tay để di chuyển con trỏ, 3 nút bấm để click trái/phải và bật/tắt chế độ, kết nối máy tính qua **Bluetooth Low Energy (HID)**. Điểm cuối kỳ: **A+**.

## Phần cứng

| Thành phần | Chi tiết |
| --- | --- |
| MCU | ESP32 Classic DevKit 38 chân |
| Cảm biến | WCMCU-20948 (ICM-20948 9 trục), I2C 400 kHz, nối thẳng 3,3 V |
| Nút | GPIO25 = chuột trái, GPIO26 = chuột phải, GPIO27 = Mode |
| Nguồn | USB (bản pin LiPo + TP4056 mới ở mức thiết kế) |
| Lắp ráp | Breadboard (đã có hướng dẫn hàn perfboard) |

Sơ đồ nguyên lý và bảng nối dây: [`deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md`](deliverables/BANG_NOI_DAY_AIR_MOUSE_DIRECT_3V3.md), [`hardware/`](hardware/) (KiCad), [`docs/AIR_MOUSE_HARDWARE_ARCHITECTURE.md`](docs/AIR_MOUSE_HARDWARE_ARCHITECTURE.md).

Ảnh lắp ráp thực tế trên breadboard: [1](docs/images/breadboard/breadboard_1.jpg), [2](docs/images/breadboard/breadboard_2.jpg), [3](docs/images/breadboard/breadboard_3.jpg).

## Tính năng firmware

- Điều khiển con trỏ theo **tốc độ xoay** (gain 0,3), lọc ngưỡng 1,4 °/s, hiệu chuẩn bias có kiểm tra và tự đo lại.
- Chống click lệch (đệm 40 ms), chống dội nút (nhấn 5 ms / nhả 20 ms).
- Nút Mode: clutch (khóa con trỏ), cân lại, **lắc nhanh = Back/Forward**, **chạm rồi nhấn giữ = cuộn theo góc nghiêng**.
- Giám sát sức khỏe cảm biến và **tự phục hồi bus I2C**.
- Cài đặt lưu vào flash (NVS) qua giao thức dòng `@GET / @SET / @SAVE / @DEFAULTS / @CAL`; gán lại chức năng nút; đảo chiều X/Y.
- **Trang web cấu hình** (có preset): [`tools/config_page/`](tools/config_page/).

## Cấu trúc thư mục

| Thư mục | Nội dung |
| --- | --- |
| `firmware/` | Mã nguồn chính (PlatformIO + Arduino). Lõi thuần `src/` test được trên máy tính, lớp `app_*` gọi phần cứng |
| `firmware_bench/`, `firmware_bias_drift/`, `firmware_orient/`, `firmware_probe/` | Chương trình đo thực nghiệm (timing/nhiễu, trôi bias, hướng cảm biến, dò I2C) |
| `release/2026-10-23_chot/` | Bản firmware chốt (bin + script nạp + SHA-256) |
| `hardware/` | Dự án KiCad, netlist, xuất PDF/SVG |
| `docs/` | Kiến trúc, nhật ký thông số, kết quả đo, rà soát mã, hướng dẫn |
| `deliverables/` | Báo cáo, cẩm nang, hướng dẫn hàn perfboard |
| `raw_logs/` | Log thô từ board thật (bằng chứng cho các số liệu) |
| `scripts/` | Công cụ bắt log, phân tích, kiểm chứng trên máy tính |

Báo cáo giữa kỳ: [`BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.pdf`](BAO_CAO_GIUA_KY_AIR_MOUSE_WEEK5.pdf). Tài liệu kiến thức chi tiết nằm trong `deliverables/`.

## Build và test

```bash
# Build firmware
python -m platformio run -d firmware

# Nạp (board cắm USB, ví dụ COM3)
python -m platformio run -d firmware -t upload

# 35 test thuật toán trên máy tính (cần g++)
bash firmware/test/run_host_tests.sh
```

Có thể nạp bản đã build sẵn trong `release/2026-10-23_chot/` bằng `flash_local_115200.cmd COM3`.

## Mức độ bằng chứng (trung thực)

| Hạng mục | Mức |
| --- | --- |
| Thuật toán lõi: lọc, hiệu chuẩn, cử chỉ, cuộn, gán nút, cấu hình | Test trên máy tính (35 test) |
| Boot, hiệu chuẩn, lưu/đọc cài đặt, nút, 100 Hz | Đo trên board thật (`raw_logs/`) |
| Cảm giác dùng (cuộn theo góc, trang cấu hình) | Phản hồi người dùng, chưa đo định lượng |
| Chạy liên tục lâu, dòng điện, thời lượng pin | **Chưa đo** |

Hạn chế đã biết: breadboard làm cảm biến thỉnh thoảng mất trạng thái (có cơ chế tự phục hồi < 0,15 s); chưa có pin/sạc trong bản cắm thử; flash dùng 90 %.

## Giấy phép

Mã nguồn: [MIT](LICENSE).
