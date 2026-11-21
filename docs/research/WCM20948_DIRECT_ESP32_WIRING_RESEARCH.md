# Kiểm chứng khả năng nối trực tiếp module ICM-20948 10 chân với ESP32 3,3 V

> Ngày kiểm chứng: 2026-09-24  
> Ảnh phần cứng: `C:\Users\phamt\Downloads\PXL_20260924_161435862.jpg`  
> Phạm vi: module PCB đen 10 chân `VCC, GND, SCL, SDA, NCS, AD0, INT, FSY, ACL, ADA` trong ảnh; không suy rộng sang Adafruit, SparkFun, Pimoroni hoặc GY-ICM20948V2.

## Kết luận ngắn

**Không có đủ căn cứ để xem việc nối thẳng module trong ảnh vào I2C 3,3 V của ESP32 là thiết kế đúng chuẩn.** Dựa trên hình dạng PCB, module này có độ tương đồng cao với breakout ICM-20948 10 chân loại tối giản: chip QFN lộ thiên, tụ lọc và điện trở kéo lên, nhưng không thấy LDO 1,8 V hoặc mạch chuyển mức hai chiều. Nếu `VCC` của module nối chung VDD và VDDIO như loại breakout này thường làm, cấp 3,3 V vào `VCC` sẽ vượt giới hạn VDDIO của chính IC.

Việc một số người cấp 3,3 V và thấy module vẫn trả dữ liệu **có thể xảy ra**, nhưng chỉ chứng minh mẫu đó hoạt động tại thời điểm thử. Nó không chứng minh điện áp nằm trong đặc tả, không bảo đảm độ bền, sai số hoặc khả năng hoạt động giữa các lô bo.

## 1. Dữ kiện từ nguồn chính thức TDK

Theo [datasheet ICM-20948 Rev. 1.6 của TDK InvenSense](https://invensense.tdk.com/wp-content/uploads/2024/03/DS-000189-ICM-20948-v1.6.pdf):

- `VDD`: 1,71–3,6 V.
- `VDDIO`: 1,71–1,95 V.
- I2C hỗ trợ Standard Mode và Fast Mode đến 400 kHz.
- Địa chỉ I2C là `0x68` khi AD0 thấp và `0x69` khi AD0 cao.

Điểm dễ gây nhầm là **giới hạn 3,6 V chỉ áp dụng cho VDD**, không áp dụng cho VDDIO.

[Application Note AN-000146 của TDK về chuyển từ MPU-9250 sang ICM-20948](https://invensense.tdk.com/wp-content/uploads/2018/10/AN-000146-v2.0-TDK_Migration_MPU_9250toICM-20948.pdf) nói rõ:

- VDDIO của ICM-20948 chỉ đến 1,95 V.
- Điện áp I/O tối đa là `VDDIO + 0,5 V`.
- Điện áp cao hơn có thể làm chip hoạt động sai hoặc hỏng.
- Khi host dùng miền điện áp cao hơn, TDK đề xuất thiết kế lại nguồn hoặc thêm bộ chuyển mức.

Ở VDDIO lớn nhất 1,95 V, giới hạn I/O nêu trên là 2,45 V. Vì vậy mức kéo lên I2C 3,3 V không nằm trong điều kiện được TDK bảo đảm.

## 2. Nhận dạng module trong ảnh

Quan sát được trực tiếp:

- PCB đen, một hàng 10 chân đúng thứ tự `VCC ... ADA`.
- Kích thước và bố cục khớp nhóm module ICM-20948 10 chân khoảng 26,7 × 15,3 mm.
- Mặt linh kiện có chip ICM-20948 QFN ở giữa, hai linh kiện điện trở nhỏ gần SCL/SDA và ba tụ nhỏ ở phía còn lại.
- Không thấy IC LDO hoặc cặp MOSFET/IC chuyển mức chuyên dụng trên mặt bo được chụp.

Ảnh thương mại của [module có cùng bố cục tại Paradisetronic](https://paradisetronic.com/products/icm-20948-modul-mpu-9250-upgrade-3-achsen-accelerometer-gyroskop-und-magnetometer-9dof-i2c-spi) cho thấy mặt còn lại gần như chỉ có đường mạch và pad hàn; không có tầng nguồn/chuyển mức. [Một listing khác của cùng họ module](https://shop.wegmatt.com/products/icm-20948-imu-module-soldered-pins) cũng chỉ mô tả đây là breakout của IC, không công bố sơ đồ bảo vệ mức logic.

Giới hạn của nhận dạng ảnh:

- Không đọc được mã linh kiện và không có schematic chính thức của đúng lô bo người dùng đang giữ.
- Module có thể là bản sao khác đường mạch dù hình thức giống nhau.
- Vì vậy kết luận “không có chuyển mức” có độ tin cậy **trung bình–cao**, chưa phải xác nhận netlist 100%.

## 3. Vì sao có hướng dẫn cắm thẳng 3,3 V và vẫn chạy?

Các trường hợp thường bị trộn lẫn:

1. **Breakout khác loại:** Adafruit và SparkFun có LDO/chuyển mức trên bo nên được phép nối trực tiếp host 3,3 V hoặc 5 V theo hướng dẫn riêng của nhà sản xuất. Điều đó không áp dụng cho mọi bo mang chip ICM-20948.
2. **Seller sao chép thông số VDD của IC:** nhiều listing ghi “1,71–3,6 V” nhưng bỏ qua giới hạn VDDIO 1,95 V. Một số trang còn vừa dùng ảnh bo tối giản vừa tuyên bố tương thích hệ 3,3 V mà không cung cấp schematic.
3. **Chạy ngoài đặc tả:** IC có thể vẫn phản hồi khi bị quá áp; linh kiện không nhất thiết hỏng ngay ở lần cấp điện đầu tiên. Absolute maximum không phải ngưỡng vận hành khuyến nghị và việc sống sót không chứng minh độ tin cậy.
4. **I2C là open-drain:** SDA/SCL được kéo lên bằng điện trở. Điện áp thực tế phụ thuộc điện trở kéo lên trên module và pull-up của host. Hai sơ đồ nhìn giống nhau có thể tạo mức bus khác nhau.

Do đó, video hoặc bài thử “cắm thẳng và đọc được dữ liệu” là bằng chứng thực nghiệm cho đúng mẫu thử, nhưng yếu hơn datasheet và schematic khi quyết định thiết kế lâu dài.

## 4. Phương án nối được bảo đảm theo datasheet

Cho module tối giản được nhận dạng trong ảnh:

- Tạo nguồn 1,8 V ổn định cho `VCC`.
- Dùng bộ chuyển mức I2C hai chiều giữa ESP32 3,3 V và SDA/SCL phía module 1,8 V.
- ESP32 `GPIO21` → phía HV của kênh SDA; phía LV → `SDA` module.
- ESP32 `GPIO22` → phía HV của kênh SCL; phía LV → `SCL` module.
- Nối chung GND.
- `AD0` → GND để dùng địa chỉ `0x68`.
- `NCS` phải ở mức cao của miền VDDIO khi dùng I2C; không kéo chân này lên 3,3 V nếu module không có bảo vệ mức.
- `FSY` nối GND nếu không dùng, theo mô tả chân trong datasheet.
- `INT`, `ACL`, `ADA` có thể để chưa nối trong lần bring-up I2C đầu tiên.

## 5. Cách xác minh đúng bo trước khi quyết định bỏ mạch chuyển mức

Không cấp 3,3 V vào module để “thử xem có sống không”. Thực hiện khi bo tắt nguồn:

1. Chụp rõ cả hai mặt và đọc mã mọi IC phụ, nếu có.
2. Dùng thang thông mạch xác định chân `VCC` header có đi thẳng tới rail cấp chip/pull-up hay đi qua regulator.
3. Cấp nguồn giới hạn dòng 1,8 V vào `VCC`.
4. Đo điện áp nghỉ tại SDA và SCL. Nếu xấp xỉ 1,8 V, module chỉ đang kéo bus lên miền 1,8 V.
5. Chỉ kết luận hỗ trợ trực tiếp 3,3 V khi có schematic đúng mã module hoặc xác định được linh kiện LDO và chuyển mức trên bo cùng đường nối của chúng.

## 6. Ảnh hưởng tới tài liệu dự án

Baseline hiện tại trong `docs/AIR_MOUSE_HARDWARE_ARCHITECTURE.md` dùng nguồn 1,8 V và BSS138 là phương án bảo thủ nhưng phù hợp với datasheet TDK cho module tối giản. Tuy nhiên câu “cấp quá 2,5 V sẽ gây cháy ngay lập tức” trong tài liệu là khẳng định quá mức: nguồn chính thức chỉ nói điện áp vượt giới hạn có thể gây sai hoạt động hoặc hư hỏng; không bảo đảm hỏng ngay. Cần sửa cách diễn đạt trong một tác vụ tài liệu riêng.

## Mức độ chắc chắn

| Kết luận | Mức chắc chắn |
|---|---|
| IC ICM-20948 có VDDIO vận hành 1,71–1,95 V | Rất cao — datasheet TDK |
| I/O 3,3 V không nằm trong giới hạn TDK khi VDDIO là 1,8–1,95 V | Rất cao — datasheet/application note TDK |
| Module trong ảnh không có sẵn LDO và level shifter | Trung bình–cao — đối chiếu bố cục ảnh; chưa có schematic đúng lô |
| Một số mẫu có thể vẫn chạy khi cắm trực tiếp 3,3 V | Có thật về mặt thực nghiệm, nhưng không chứng minh độ an toàn hoặc độ bền |
| Khuyến nghị dùng 1,8 V + chuyển mức cho đúng module trong ảnh | Cao — lựa chọn duy nhất hiện có bằng chứng phù hợp datasheet |

---

## 7. Phụ lục Thực nghiệm Hardware Bring-up (Cập nhật ngày 2026-09-25)

> Trạng thái: `BENCH_VERIFIED_ON_OWNED_MODULE` / `DIRECT_3V3_FUNCTIONAL_CONFIRMED`  
> Tham chiếu báo cáo thực nghiệm: `docs/HARDWARE_BRINGUP_DIRECT_3V3_2026-09-25.md`  
> Tệp bằng chứng: `raw_logs/probe_i2c_result.log`, `raw_logs/main_firmware_boot.log`

Vào ngày 25/09/2026, nhóm đã tiến hành thử nghiệm kết nối trực tiếp module WCMCU-20948 cụ thể mà nhóm đang sở hữu với chân nguồn 3,3 V và chân GPIO21/22 của ESP32 DevKit 38-pin (COM8) mà không qua IC chuyển mức BSS138 hay LDO 1,8 V phụ.

### Kết quả đo đạc thực nghiệm:
1. **Bus I2C & Định danh**: Module phản hồi ACK tại địa chỉ `0x68`, chuyển bank 0 thành công, và thanh ghi `WHO_AM_I` đọc về chính xác giá trị `0xEA`.
2. **Độ ổn định bus ngắn hạn**: Đạt 100/100 lần đọc WHO_AM_I thành công ở 100 kHz và 100/100 lần đọc ở 400 kHz Fast-Mode trong phép thử ngắn hạn (0 NACK / 0 lỗi bus).
3. **Thu thập dữ liệu chuyển động**: Đọc burst 12 byte liên tục thành công, trục Z gia tốc thể hiện đúng trọng trường $1g$ ($\approx +16200 \text{ LSB}$ ở dải mặc định $\pm 2g$ của chương trình probe; firmware chính dùng $\pm 4g$ nên $1g \approx 8192\,\text{LSB}$) khi nằm yên.
4. **Firmware chính thức**: Đọc lại thành công toàn bộ các thanh ghi cấu hình vật lý (`PWR_MGMT_1=0x01`, `GYRO_CONFIG_1=0x1B`, `ACCEL_CONFIG=0x1B`, sample dividers=10), hoàn thành 200 mẫu hiệu chuẩn trôi tĩnh khởi động và duy trì vòng lặp 100 Hz.

### Ý nghĩa đối với dự án:
- Dự án chính thức chấp nhận phương án kết nối trực tiếp 3,3 V (`DIRECT_3V3_FUNCTIONAL_CONFIRMED`) làm baseline phần cứng cho mẫu thử nghiệm Air Mouse V1.
- Phân tích ở Mục 1 đến Mục 5 về giới hạn datasheet TDK InvenSense của chip trần vẫn được giữ nguyên như một tài liệu đối sánh kỹ thuật và cơ sở lý thuyết học thuật. Nhóm ghi nhận đây là kết quả thực nghiệm trên đúng linh kiện sở hữu, không khái quát hóa thành đặc tính kỹ thuật chung cho mọi loại breakout ICM-20948 trên thị trường.

