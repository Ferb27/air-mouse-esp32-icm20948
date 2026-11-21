# Kích thước module tham khảo

Trích mục module trong tài liệu cơ khí; tất cả **CẦN ĐO THỰC TẾ**. Không dùng bố cục PCB cũ thay perfboard V2.

2. **Kích thước các module cắm theo web reference**:
   - Module ESP32 Classic 38-pin: $55.0 \times 28.0\,\text{mm}$.
   - Module WCMCU-20948 (10 chân header): $26.7 \times 15.3\,\text{mm}$, pin pitch $2.54\,\text{mm}$ (`WEB_VERIFIED_DESIGN_REFERENCE`, footprint `PinSocket_1x10_P2.54mm_Vertical` + custom outline $26.7 \times 15.3\,\text{mm}$).
   - Module sạc TP4056 Type-C: $26.0 \times 17.0\,\text{mm}$.
   - Module tăng áp MT3608: $36.0 \times 17.0\,\text{mm}$.

Board 90×150 mm, pitch 2.54 mm. Vùng pin B21…Z37=60.96×40.64 mm gồm viền; pin chưa chọn. Pack tham khảo 523450 khoảng 50×34×5.2 mm, đo cả PCM/tab/dây. Mút 1–2 mm và Kapton không thay vùng cấm chân. Hai hàng ESP32 25.4 mm là giả định, phương án 22.86 mm chỉ sau đo.
