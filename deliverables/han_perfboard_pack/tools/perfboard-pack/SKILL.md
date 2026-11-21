---
name: perfboard-pack
description: Tái sinh và kiểm tra gói hướng dẫn hàn perfboard Air Mouse tự chứa, dùng bảng dữ liệu chung cho SVG và mô tả chữ, rồi đóng ZIP đã đối chiếu nội dung.
---

Áp dụng khi cập nhật chính gói này hoặc tạo gói tương tự từ hướng dẫn đã được duyệt. Không dùng hình đề xuất để suy ra số đo phần cứng.

1. Đối chiếu hướng dẫn hiện hành với [bảng dữ liệu](../du_lieu_hinh.json); cập nhật dữ liệu trước. Giữ nguyên nguồn gốc từng dòng dây và bảng tọa độ để phép kiểm phát hiện khác biệt.
2. Từ thư mục gốc gói, chạy `python tools/sinh_hinh.py`. [Bộ sinh](../sinh_hinh.py) tạo SVG, HTML inline và mô tả chữ từ cùng dữ liệu; có thử âm bằng tọa độ R1 sai. BOTTOM đảo trục x, giữ tên lỗ TOP; cả đầu nối gá rời cũng phải đổi phía.
3. Nếu máy đã có Playwright và trình duyệt, chạy `node tools/xuat_png.cjs <duong-dan-trinh-duyet> <duong-dan-module-playwright>`. Không cài thêm để xuất PNG. Xuất lại PNG sau mỗi thay đổi SVG; ảnh cũ không chứng minh bản mới đúng.
4. Soi TOP/BOTTOM, sơ đồ nguồn và chữ nhỏ. Phép thử LED bằng 3V3 phải tách khỏi dây GPIO32 cố định; mô tả rõ tháo ESP32 khỏi carrier để tránh cấp ngược GPIO. B- của pin và OUT-/GND là hai mạng khác nhau bên ngoài TP4056.
5. Chạy `python tools/kiem_tra_goi.py`. [Bộ kiểm](../kiem_tra_goi.py) đối chiếu 43 dòng/15 net, tọa độ, liên kết trong gói, đối xứng, PNG, quyền riêng tư; tạo manifest và ZIP, đọc giải nén từng tệp để so byte. Xem [kết quả](../KET_QUA_KIEM_TRA.md) trước khi báo hoàn tất.

Chỉ loại đường dẫn máy thật khi làm bản sao; không dùng biểu thức nhận nhầm `https://` thành ổ đĩa rồi cắt URL. Không sao chép phần mềm/bí mật hay tuyên bố đã thử phần cứng chỉ từ phép kiểm tài liệu. Khi tái sử dụng cho mạch khác, thay tiêu chí 43 dòng/15 net và căn cứ nguồn tương ứng, không giữ số đếm máy móc.
