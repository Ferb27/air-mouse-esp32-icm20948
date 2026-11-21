# Mô tả hình bằng chữ — sinh cùng dữ liệu với SVG

Nguồn: tools/du_lieu_hinh.json; tọa độ theo hướng dẫn V2. Không phải số đo thực. Màu B− được vẽ tím để tách GND đen; dây thật đen nhãn B−. Màu không thay nhãn net.

## 01_top — TOP — bố cục board chính

[SVG](hinh/01_top.svg). Hướng nhìn: TOP.

### Nhãn hiển thị

- TOP — bố cục board chính
- TOP nhìn linh kiện.
- đề xuất, chưa đo thực tế
- 90 mm · cột theo TOP, giữ tên lỗ khi lật
- A
- B
- C
- D
- E
- F
- G
- H
- I
- J
- K
- L
- M
- N
- O
- P
- Q
- R
- S
- T
- U
- V
- W
- X
- Y
- Z
- AA
- AB
- AC
- AD
- AE
- AF
- AG
- 1
- 2
- 3
- 4
- 5
- 6
- 7
- 8
- 9
- 10
- 11
- 12
- 13
- 14
- 15
- 16
- 17
- 18
- 19
- 20
- 21
- 22
- 23
- 24
- 25
- 26
- 27
- 28
- 29
- 30
- 31
- 32
- 33
- 34
- 35
- 36
- 37
- 38
- 39
- 40
- 41
- 42
- 43
- 44
- 45
- 46
- 47
- 48
- 49
- 50
- 51
- 52
- 53
- 54
- 55
- 56
- 57
- CẤM CHÂN HÀN · B21…Z37
- Vùng pin 60.96×40.64 mm
- Không dây / vít / mối hàn nổi
- Pin chưa chọn · gồm viền ≥2 mm
- SW2
- H5
- SW4
- R5
- SW3
- AB5
- R1 D19/H19
- D1 K19/L19
- MOD1
- TP4056
- A9…L17
- USB-C
- MOD2
- MT3608
- N10…AC17
- SW1
- AA19…AG22
- J1
- gá rời
- R2
- AA25/AA29
- R3
- AA29/AA33
- C1
- AC29/AC31
- J5V
- AC34/AD34
- C2
- AE35/AG35
- U2
- IMU WCMCU-20948
- B41…M47
- ESP32
- thân mờ: tham khảo
- U38…U57
- AE38…AE57
- hoặc AD sau đo
- USB vào trong
- G* P39
- TP1 SCL B50
- TP2 SDA B51
- TP3 3V3 B52
- TP4 GND B53
- ĂNG-TEN NGOÀI MÉP
- độ nhô CẦN ĐO
- Lưới đúng tỉ lệ; A1 cách mép 3 mm là giả định. Không dùng làm mẫu khoan.
- Màu: vàng = nút/vùng pin; xanh = module; tím = giắc; xám = socket/test. Nét xám mảnh là chú thích. Ăng-ten nét
- đứt: yêu cầu vị trí, độ nhô chưa đo.
- Nguồn: V2 §3.5.3. Vùng pin không chân cả hai mặt; vùng ăng-ten không đồng/dây/kim loại.

### Linh kiện và lỗ theo TOP (BOTTOM giữ nguyên tên lỗ)

| Ref | Linh kiện | Tọa độ/đặt | Màu vùng | Nối với |
|---|---|---|---|---|
| SW2 | Nút trái | H5 | #fde6b3 | 24: BTN_LEFT; U1 GPIO25 → SW2 nhóm A<br>25: GND; SW2 nhóm B → G* |
| SW4 | Nút mode | R5 | #fde6b3 | 28: BTN_MODE; U1 GPIO27 → SW4 nhóm A<br>29: GND; SW4 nhóm B → G* |
| SW3 | Nút phải | AB5 | #fde6b3 | 26: BTN_RIGHT; U1 GPIO26 → SW3 nhóm A<br>27: GND; SW3 nhóm B → G* |
| R1 | 1 kΩ | D19/H19 | #f6d7b8 | 30: LED_STATUS; U1 GPIO32 → R1.1 (1 kΩ)<br>31: LED_ANODE; R1.2 → D1 anode A |
| D1 | LED xanh | K19/L19 | #bfe8c1 | 03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B-<br>05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>06: GND; MOD1 OUT- → G*<br>31: LED_ANODE; R1.2 → D1 anode A<br>32: GND; D1 cathode K → G* |
| MOD1 | TP4056 | A9…L17 | #bde4da | 03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B-<br>05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>06: GND; MOD1 OUT- → G* |
| MOD2 | MT3608 | N10…AC17 | #cfe0f9 | 07: V_SYS; SW1 COM → MOD2 VIN+<br>09: GND; G* → MOD2 VIN-<br>10: GND; G* → MOD2 VOUT-<br>11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V |
| SW1 | Công tắc nguồn | AA19…AG22 | #fde6b3 | 05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>07: V_SYS; SW1 COM → MOD2 VIN+<br>08: V_SYS; SW1 COM → R2.1 |
| J1 | Giắc pin PH2.0 | gá trên dây ngoài vùng pin; CẦN ĐO THỰC TẾ | #e2cef1 | 01: VBAT; BAT1 dây + đã đo → J1 cực + qua đầu ghép<br>02: GND_BAT_CELL; BAT1 dây − đã đo → J1 cực − qua đầu ghép<br>03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B- |
| R2 | 100 kΩ | AA25/AA29 | #f6d7b8 | 08: V_SYS; SW1 COM → R2.1<br>33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>34: BAT_SENSE; R2.2 → R3.1<br>35: BAT_SENSE; R2.2/R3.1 → C1.1 |
| R3 | 100 kΩ | AA29/AA33 | #f6d7b8 | 33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>34: BAT_SENSE; R2.2 → R3.1<br>35: BAT_SENSE; R2.2/R3.1 → C1.1<br>36: GND; R3.2 → G* |
| C1 | 100 nF | AC29/AC31 | #fbe2b8 | 35: BAT_SENSE; R2.2/R3.1 → C1.1<br>37: GND; C1.2 → G* |
| J5V | Đầu 5V tháo rời | AC34/AD34 | #e2cef1 | 11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V<br>12: 5V; Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35<br>42: GND; G* → J5V.2 đực AD34<br>43: GND; J5V.2 cái → U1 GND theo nhãn thật |
| C2 | 10 µF, có cực | AE35/AG35 | #fbe2b8 | 12: 5V; Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35<br>13: GND; C2 − → G* |
| U2 | IMU WCMCU-20948 | B41…M47; C42/D42/E42/F42/G42/H42/I42/J42/K42/L42 | #bfe8c1 | 14: 3V3; U1 3V3 → U2 VCC (1)<br>15: 3V3; U2 VCC cùng net U1 3V3 → U2 NCS (5)<br>17: IMU_SDA; U1 GPIO21 → U2 SDA (4)<br>18: IMU_SDA; U2 SDA cùng net GPIO21 → TP2<br>19: IMU_SCL; U1 GPIO22 → U2 SCL (3)<br>20: IMU_SCL; U2 SCL cùng net GPIO22 → TP1<br>21: GND; U2 GND (2) → G*<br>22: GND; U2 AD0 (6) → U2 GND cùng net G*<br>23: GND; U2 FSY (8) → U2 GND cùng net G* |
| U1 | ESP32 + 2 socket | U38…AE57 | #d3dbe5 | 11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V<br>14: 3V3; U1 3V3 → U2 VCC (1)<br>15: 3V3; U2 VCC cùng net U1 3V3 → U2 NCS (5)<br>16: 3V3; U1 3V3 → TP3<br>17: IMU_SDA; U1 GPIO21 → U2 SDA (4)<br>19: IMU_SCL; U1 GPIO22 → U2 SCL (3)<br>24: BTN_LEFT; U1 GPIO25 → SW2 nhóm A<br>26: BTN_RIGHT; U1 GPIO26 → SW3 nhóm A<br>28: BTN_MODE; U1 GPIO27 → SW4 nhóm A<br>30: LED_STATUS; U1 GPIO32 → R1.1 (1 kΩ)<br>33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>38: GND; U1 GND nhãn thật, tương ứng N chân 14 → G*<br>39: GND; U1 GND nhãn thật, tương ứng N chân 32 → G*<br>40: GND; U1 GND nhãn thật, tương ứng N chân 38 → G*<br>43: GND; J5V.2 cái → U1 GND theo nhãn thật |
| G* | Điểm chia mass | P39 | #cbd5e1 | 06: GND; MOD1 OUT- → G*<br>09: GND; G* → MOD2 VIN-<br>10: GND; G* → MOD2 VOUT-<br>13: GND; C2 − → G*<br>21: GND; U2 GND (2) → G*<br>22: GND; U2 AD0 (6) → U2 GND cùng net G*<br>23: GND; U2 FSY (8) → U2 GND cùng net G*<br>25: GND; SW2 nhóm B → G*<br>27: GND; SW3 nhóm B → G*<br>29: GND; SW4 nhóm B → G*<br>32: GND; D1 cathode K → G*<br>36: GND; R3.2 → G*<br>37: GND; C1.2 → G*<br>38: GND; U1 GND nhãn thật, tương ứng N chân 14 → G*<br>39: GND; U1 GND nhãn thật, tương ứng N chân 32 → G*<br>40: GND; U1 GND nhãn thật, tương ứng N chân 38 → G*<br>41: GND; TP4 → G*<br>42: GND; G* → J5V.2 đực AD34 |
| TP1 | SCL | B50 | #e0e7ef | 20: IMU_SCL; U2 SCL cùng net GPIO22 → TP1 |
| TP2 | SDA | B51 | #e0e7ef | 18: IMU_SDA; U2 SDA cùng net GPIO21 → TP2 |
| TP3 | 3V3 | B52 | #e0e7ef | 16: 3V3; U1 3V3 → TP3 |
| TP4 | GND | B53 | #e0e7ef | 41: GND; TP4 → G* |
| BAT1 | Pin 1S PCM, chưa chọn | gá trên dây ngoài vùng pin; CẦN ĐO THỰC TẾ | #e2cef1 | 01: VBAT; BAT1 dây + đã đo → J1 cực + qua đầu ghép<br>02: GND_BAT_CELL; BAT1 dây − đã đo → J1 cực − qua đầu ghép |

Vùng pin: B21…Z37; 60.96×40.64 mm, cả hình chiếu hai mặt không chân/dây/vít. Lưới A1 cách mép 3 mm là giả định. Dấu ăng-ten ngoài mép chỉ yêu cầu vị trí, độ nhô CẦN ĐO THỰC TẾ.

## 02_bottom — BOTTOM — mặt hàn đối xứng

[SVG](hinh/02_bottom.svg). Hướng nhìn: BOTTOM, đối xứng trái/phải so TOP.

### Nhãn hiển thị

- BOTTOM — mặt hàn đối xứng
- BOTTOM: trái/phải bị đảo so với TOP; chữ giữ chiều đọc.
- đề xuất, chưa đo thực tế
- 90 mm · cột theo TOP, giữ tên lỗ khi lật
- A
- B
- C
- D
- E
- F
- G
- H
- I
- J
- K
- L
- M
- N
- O
- P
- Q
- R
- S
- T
- U
- V
- W
- X
- Y
- Z
- AA
- AB
- AC
- AD
- AE
- AF
- AG
- 1
- 2
- 3
- 4
- 5
- 6
- 7
- 8
- 9
- 10
- 11
- 12
- 13
- 14
- 15
- 16
- 17
- 18
- 19
- 20
- 21
- 22
- 23
- 24
- 25
- 26
- 27
- 28
- 29
- 30
- 31
- 32
- 33
- 34
- 35
- 36
- 37
- 38
- 39
- 40
- 41
- 42
- 43
- 44
- 45
- 46
- 47
- 48
- 49
- 50
- 51
- 52
- 53
- 54
- 55
- 56
- 57
- CẤM CHÂN HÀN · B21…Z37
- Vùng pin 60.96×40.64 mm
- Không dây / vít / mối hàn nổi
- Pin chưa chọn · gồm viền ≥2 mm
- SW2
- H5
- SW4
- R5
- SW3
- AB5
- R1 D19/H19
- D1 K19/L19
- MOD1
- TP4056
- A9…L17
- USB-C
- MOD2
- MT3608
- N10…AC17
- SW1
- AA19…AG22
- J1
- gá rời
- R2
- AA25/AA29
- R3
- AA29/AA33
- C1
- AC29/AC31
- J5V
- AC34/AD34
- C2
- AE35/AG35
- U2
- IMU WCMCU-20948
- B41…M47
- ESP32
- thân mờ: tham khảo
- U38…U57
- AE38…AE57
- hoặc AD sau đo
- USB vào trong
- G* P39
- TP1 SCL B50
- TP2 SDA B51
- TP3 3V3 B52
- TP4 GND B53
- ĂNG-TEN NGOÀI MÉP
- độ nhô CẦN ĐO
- Lưới đúng tỉ lệ; A1 cách mép 3 mm là giả định. Không dùng làm mẫu khoan.
- Màu: vàng = nút/vùng pin; xanh = module; tím = giắc; xám = socket/test. Nét xám mảnh là chú thích. Ăng-ten nét
- đứt: yêu cầu vị trí, độ nhô chưa đo.
- Nguồn: V2 §3.5.3. Vùng pin không chân cả hai mặt; vùng ăng-ten không đồng/dây/kim loại.

### Linh kiện và lỗ theo TOP (BOTTOM giữ nguyên tên lỗ)

| Ref | Linh kiện | Tọa độ/đặt | Màu vùng | Nối với |
|---|---|---|---|---|
| SW2 | Nút trái | H5 | #fde6b3 | 24: BTN_LEFT; U1 GPIO25 → SW2 nhóm A<br>25: GND; SW2 nhóm B → G* |
| SW4 | Nút mode | R5 | #fde6b3 | 28: BTN_MODE; U1 GPIO27 → SW4 nhóm A<br>29: GND; SW4 nhóm B → G* |
| SW3 | Nút phải | AB5 | #fde6b3 | 26: BTN_RIGHT; U1 GPIO26 → SW3 nhóm A<br>27: GND; SW3 nhóm B → G* |
| R1 | 1 kΩ | D19/H19 | #f6d7b8 | 30: LED_STATUS; U1 GPIO32 → R1.1 (1 kΩ)<br>31: LED_ANODE; R1.2 → D1 anode A |
| D1 | LED xanh | K19/L19 | #bfe8c1 | 03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B-<br>05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>06: GND; MOD1 OUT- → G*<br>31: LED_ANODE; R1.2 → D1 anode A<br>32: GND; D1 cathode K → G* |
| MOD1 | TP4056 | A9…L17 | #bde4da | 03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B-<br>05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>06: GND; MOD1 OUT- → G* |
| MOD2 | MT3608 | N10…AC17 | #cfe0f9 | 07: V_SYS; SW1 COM → MOD2 VIN+<br>09: GND; G* → MOD2 VIN-<br>10: GND; G* → MOD2 VOUT-<br>11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V |
| SW1 | Công tắc nguồn | AA19…AG22 | #fde6b3 | 05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>07: V_SYS; SW1 COM → MOD2 VIN+<br>08: V_SYS; SW1 COM → R2.1 |
| J1 | Giắc pin PH2.0 | gá trên dây ngoài vùng pin; CẦN ĐO THỰC TẾ | #e2cef1 | 01: VBAT; BAT1 dây + đã đo → J1 cực + qua đầu ghép<br>02: GND_BAT_CELL; BAT1 dây − đã đo → J1 cực − qua đầu ghép<br>03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B- |
| R2 | 100 kΩ | AA25/AA29 | #f6d7b8 | 08: V_SYS; SW1 COM → R2.1<br>33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>34: BAT_SENSE; R2.2 → R3.1<br>35: BAT_SENSE; R2.2/R3.1 → C1.1 |
| R3 | 100 kΩ | AA29/AA33 | #f6d7b8 | 33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>34: BAT_SENSE; R2.2 → R3.1<br>35: BAT_SENSE; R2.2/R3.1 → C1.1<br>36: GND; R3.2 → G* |
| C1 | 100 nF | AC29/AC31 | #fbe2b8 | 35: BAT_SENSE; R2.2/R3.1 → C1.1<br>37: GND; C1.2 → G* |
| J5V | Đầu 5V tháo rời | AC34/AD34 | #e2cef1 | 11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V<br>12: 5V; Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35<br>42: GND; G* → J5V.2 đực AD34<br>43: GND; J5V.2 cái → U1 GND theo nhãn thật |
| C2 | 10 µF, có cực | AE35/AG35 | #fbe2b8 | 12: 5V; Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35<br>13: GND; C2 − → G* |
| U2 | IMU WCMCU-20948 | B41…M47; C42/D42/E42/F42/G42/H42/I42/J42/K42/L42 | #bfe8c1 | 14: 3V3; U1 3V3 → U2 VCC (1)<br>15: 3V3; U2 VCC cùng net U1 3V3 → U2 NCS (5)<br>17: IMU_SDA; U1 GPIO21 → U2 SDA (4)<br>18: IMU_SDA; U2 SDA cùng net GPIO21 → TP2<br>19: IMU_SCL; U1 GPIO22 → U2 SCL (3)<br>20: IMU_SCL; U2 SCL cùng net GPIO22 → TP1<br>21: GND; U2 GND (2) → G*<br>22: GND; U2 AD0 (6) → U2 GND cùng net G*<br>23: GND; U2 FSY (8) → U2 GND cùng net G* |
| U1 | ESP32 + 2 socket | U38…AE57 | #d3dbe5 | 11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V<br>14: 3V3; U1 3V3 → U2 VCC (1)<br>15: 3V3; U2 VCC cùng net U1 3V3 → U2 NCS (5)<br>16: 3V3; U1 3V3 → TP3<br>17: IMU_SDA; U1 GPIO21 → U2 SDA (4)<br>19: IMU_SCL; U1 GPIO22 → U2 SCL (3)<br>24: BTN_LEFT; U1 GPIO25 → SW2 nhóm A<br>26: BTN_RIGHT; U1 GPIO26 → SW3 nhóm A<br>28: BTN_MODE; U1 GPIO27 → SW4 nhóm A<br>30: LED_STATUS; U1 GPIO32 → R1.1 (1 kΩ)<br>33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>38: GND; U1 GND nhãn thật, tương ứng N chân 14 → G*<br>39: GND; U1 GND nhãn thật, tương ứng N chân 32 → G*<br>40: GND; U1 GND nhãn thật, tương ứng N chân 38 → G*<br>43: GND; J5V.2 cái → U1 GND theo nhãn thật |
| G* | Điểm chia mass | P39 | #cbd5e1 | 06: GND; MOD1 OUT- → G*<br>09: GND; G* → MOD2 VIN-<br>10: GND; G* → MOD2 VOUT-<br>13: GND; C2 − → G*<br>21: GND; U2 GND (2) → G*<br>22: GND; U2 AD0 (6) → U2 GND cùng net G*<br>23: GND; U2 FSY (8) → U2 GND cùng net G*<br>25: GND; SW2 nhóm B → G*<br>27: GND; SW3 nhóm B → G*<br>29: GND; SW4 nhóm B → G*<br>32: GND; D1 cathode K → G*<br>36: GND; R3.2 → G*<br>37: GND; C1.2 → G*<br>38: GND; U1 GND nhãn thật, tương ứng N chân 14 → G*<br>39: GND; U1 GND nhãn thật, tương ứng N chân 32 → G*<br>40: GND; U1 GND nhãn thật, tương ứng N chân 38 → G*<br>41: GND; TP4 → G*<br>42: GND; G* → J5V.2 đực AD34 |
| TP1 | SCL | B50 | #e0e7ef | 20: IMU_SCL; U2 SCL cùng net GPIO22 → TP1 |
| TP2 | SDA | B51 | #e0e7ef | 18: IMU_SDA; U2 SDA cùng net GPIO21 → TP2 |
| TP3 | 3V3 | B52 | #e0e7ef | 16: 3V3; U1 3V3 → TP3 |
| TP4 | GND | B53 | #e0e7ef | 41: GND; TP4 → G* |
| BAT1 | Pin 1S PCM, chưa chọn | gá trên dây ngoài vùng pin; CẦN ĐO THỰC TẾ | #e2cef1 | 01: VBAT; BAT1 dây + đã đo → J1 cực + qua đầu ghép<br>02: GND_BAT_CELL; BAT1 dây − đã đo → J1 cực − qua đầu ghép |

Vùng pin: B21…Z37; 60.96×40.64 mm, cả hình chiếu hai mặt không chân/dây/vít. Lưới A1 cách mép 3 mm là giả định. Dấu ăng-ten ngoài mép chỉ yêu cầu vị trí, độ nhô CẦN ĐO THỰC TẾ.

## 03_nguon — Sơ đồ khối nguồn

[SVG](hinh/03_nguon.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Sơ đồ khối nguồn
- Luồng điện, không theo tỉ lệ. Tím = CELL−; đen = GND hệ thống.
- đề xuất, chưa đo thực tế
- BAT1 · Pin 1S PCM, chưa chọn
- 1S PCM; chưa chọn pin
- J1 · Giắc pin PH2.0
- + → B+ ; − → B−
- MOD1 · TP4056
- B+/B−: phía cell
- OUT+/OUT−: phía hệ thống
- USB-C 5V chỉ khi sạc pin thật
- SW1 · Công tắc nguồn
- OUT+ → ON ; COM → V_SYS
- MOD2 · MT3608
- VIN+ = V_SYS ; VIN− = GND
- VOUT+ = 5V ; VOUT− = GND
- J5V · Đầu 5V tháo rời
- 1 = +5V ; 2 = GND
- tháo cả đầu cái khi dùng USB
- U1 · ESP32 + 2 socket
- VIN/5V từ J5V.1
- GND về hệ thống
- VBAT
- OUT+
- V_SYS
- 5V
- 5V qua J5V
- CELL−
- GND = OUT−
- ✗
- CẤM nối B− với OUT−/GND
- bên ngoài module
- USB-C vào TP4056
- R2 · 100 kΩ
- V_SYS → 100 kΩ
- BAT_SENSE → GPIO34
- R3 · 100 kΩ
- 100 kΩ → GND
- C1 100 nF // R3
- C1: BAT_SENSE ↔ GND
- U2 · IMU WCMCU-20948
- VCC/NCS ← ESP32 3V3
- 3V3
- C2 · 10 µF, có cực
- +5V ↔ GND; không nối tiếp
- Nguồn: V2 §3.0/3.7; C1/C2 mắc song song. Xem hình 04a/04b cho từng liên kết điện.

### Liên kết điện

- 01 | VBAT | BAT1 dây + đã đo → J1 cực + qua đầu ghép | màu hình #b91c1c; màu dây Đỏ
- 02 | GND_BAT_CELL | BAT1 dây − đã đo → J1 cực − qua đầu ghép | màu hình #7c3aed; màu dây Đen, nhãn CELL−
- 03 | VBAT | J1 + → MOD1 B+ | màu hình #b91c1c; màu dây Đỏ
- 04 | GND_BAT_CELL | J1 − → MOD1 B- | màu hình #7c3aed; màu dây Đen, nhãn B−
- 05 | V_SW_IN | MOD1 OUT+ → SW1 tiếp điểm ON | màu hình #dc2626; màu dây Đỏ, nhãn OUT+
- 06 | GND | MOD1 OUT- → G* | màu hình #20252b; màu dây Đen
- 07 | V_SYS | SW1 COM → MOD2 VIN+ | màu hình #e54b2c; màu dây Đỏ, nhãn SYS
- 08 | V_SYS | SW1 COM → R2.1 | màu hình #e54b2c; màu dây Đỏ, nhãn đo SYS
- 09 | GND | G* → MOD2 VIN- | màu hình #20252b; màu dây Đen
- 10 | GND | G* → MOD2 VOUT- | màu hình #20252b; màu dây Đen
- 11 | 5V | MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V | màu hình #ef4444; màu dây Đỏ, nhãn 5V
- 12 | 5V | Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35 | màu hình #ef4444; màu dây Đỏ
- 13 | GND | C2 − → G* | màu hình #20252b; màu dây Đen
- 14 | 3V3 | U1 3V3 → U2 VCC (1) | màu hình #a61b29; màu dây Đỏ, nhãn 3V3
- 15 | 3V3 | U2 VCC cùng net U1 3V3 → U2 NCS (5) | màu hình #a61b29; màu dây Đỏ, nhãn NCS
- 16 | 3V3 | U1 3V3 → TP3 | màu hình #a61b29; màu dây Đỏ, nhãn TP3
- 17 | IMU_SDA | U1 GPIO21 → U2 SDA (4) | màu hình #15803d; màu dây Xanh lá
- 18 | IMU_SDA | U2 SDA cùng net GPIO21 → TP2 | màu hình #15803d; màu dây Xanh lá
- 19 | IMU_SCL | U1 GPIO22 → U2 SCL (3) | màu hình #a17a00; màu dây Vàng
- 20 | IMU_SCL | U2 SCL cùng net GPIO22 → TP1 | màu hình #a17a00; màu dây Vàng
- 21 | GND | U2 GND (2) → G* | màu hình #20252b; màu dây Đen
- 22 | GND | U2 AD0 (6) → U2 GND cùng net G* | màu hình #20252b; màu dây Đen, nhãn AD0
- 23 | GND | U2 FSY (8) → U2 GND cùng net G* | màu hình #20252b; màu dây Đen, nhãn FSY
- 24 | BTN_LEFT | U1 GPIO25 → SW2 nhóm A | màu hình #2563eb; màu dây Xanh dương
- 25 | GND | SW2 nhóm B → G* | màu hình #20252b; màu dây Đen
- 26 | BTN_RIGHT | U1 GPIO26 → SW3 nhóm A | màu hình #778696; màu dây Trắng
- 27 | GND | SW3 nhóm B → G* | màu hình #20252b; màu dây Đen
- 28 | BTN_MODE | U1 GPIO27 → SW4 nhóm A | màu hình #9333ea; màu dây Tím
- 29 | GND | SW4 nhóm B → G* | màu hình #20252b; màu dây Đen
- 30 | LED_STATUS | U1 GPIO32 → R1.1 (1 kΩ) | màu hình #d97706; màu dây Cam
- 31 | LED_ANODE | R1.2 → D1 anode A | màu hình #b45309; màu dây Cam, nhãn A
- 32 | GND | D1 cathode K → G* | màu hình #20252b; màu dây Đen
- 33 | BAT_SENSE | R2.2/R3.1 tại AA29 → U1 GPIO34 | màu hình #64748b; màu dây Xám
- 34 | BAT_SENSE | R2.2 → R3.1 | màu hình #64748b; màu dây Nhãn SENSE
- 35 | BAT_SENSE | R2.2/R3.1 → C1.1 | màu hình #64748b; màu dây Xám
- 36 | GND | R3.2 → G* | màu hình #20252b; màu dây Đen
- 37 | GND | C1.2 → G* | màu hình #20252b; màu dây Đen
- 38 | GND | U1 GND nhãn thật, tương ứng N chân 14 → G* | màu hình #20252b; màu dây Đen
- 39 | GND | U1 GND nhãn thật, tương ứng N chân 32 → G* | màu hình #20252b; màu dây Đen
- 40 | GND | U1 GND nhãn thật, tương ứng N chân 38 → G* | màu hình #20252b; màu dây Đen
- 41 | GND | TP4 → G* | màu hình #20252b; màu dây Đen
- 42 | GND | G* → J5V.2 đực AD34 | màu hình #20252b; màu dây Đen
- 43 | GND | J5V.2 cái → U1 GND theo nhãn thật | màu hình #20252b; màu dây Đen

## 04a_day_nguon — Nối dây 01–13, 42–43: nguồn

[SVG](hinh/04a_day_nguon.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Nối dây 01–13, 42–43: nguồn
- Sơ đồ từng liên kết theo net; số dòng khớp bảng 3.7. Không phải đường đi vật lý.
- đề xuất, chưa đo thực tế
- 01
- VBAT
- BAT1 dây + đã đo
- J1 cực + qua giắc
- 02
- GND_BAT_CELL
- BAT1 dây − đã đo
- J1 cực − qua giắc
- 03
- J1 +
- MOD1 B+
- 04
- J1 −
- MOD1 B-
- 05
- V_SW_IN
- MOD1 OUT+
- SW1 tiếp điểm ON
- 06
- GND
- MOD1 OUT-
- G*
- 07
- V_SYS
- SW1 COM
- MOD2 VIN+
- 08
- R2.1
- 09
- MOD2 VIN-
- 10
- MOD2 VOUT-
- 11
- 5V
- MOD2 VOUT+ → J5V.1 đực AC34
- J5V.1 cái → U1 VIN/5V
- 12
- Phía nguồn J5V.1, cùng VOUT+
- C2 + tại AE35
- 13
- C2 −
- 42
- J5V.2 đực AD34
- 43
- J5V.2 cái
- U1 GND theo nhãn thật
- Màu dương: các sắc đỏ; GND: đen; B−/GND_BAT_CELL: tím trên hình để tách rõ (dây thật đen nhãn
- B−). SDA xanh lá, SCL vàng, nút xanh dương/trắng có viền/tím, LED cam, SENSE xám. Nhãn net
- luôn là căn cứ chính.
- Nguồn: V2 §3.7; P = bó 2–3 lõi; S = một lõi. Dây đi vòng vùng pin, không đi theo nét logic này.

### Liên kết điện

- 01 | VBAT | BAT1 dây + đã đo → J1 cực + qua đầu ghép | màu hình #b91c1c; màu dây Đỏ
- 02 | GND_BAT_CELL | BAT1 dây − đã đo → J1 cực − qua đầu ghép | màu hình #7c3aed; màu dây Đen, nhãn CELL−
- 03 | VBAT | J1 + → MOD1 B+ | màu hình #b91c1c; màu dây Đỏ
- 04 | GND_BAT_CELL | J1 − → MOD1 B- | màu hình #7c3aed; màu dây Đen, nhãn B−
- 05 | V_SW_IN | MOD1 OUT+ → SW1 tiếp điểm ON | màu hình #dc2626; màu dây Đỏ, nhãn OUT+
- 06 | GND | MOD1 OUT- → G* | màu hình #20252b; màu dây Đen
- 07 | V_SYS | SW1 COM → MOD2 VIN+ | màu hình #e54b2c; màu dây Đỏ, nhãn SYS
- 08 | V_SYS | SW1 COM → R2.1 | màu hình #e54b2c; màu dây Đỏ, nhãn đo SYS
- 09 | GND | G* → MOD2 VIN- | màu hình #20252b; màu dây Đen
- 10 | GND | G* → MOD2 VOUT- | màu hình #20252b; màu dây Đen
- 11 | 5V | MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V | màu hình #ef4444; màu dây Đỏ, nhãn 5V
- 12 | 5V | Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35 | màu hình #ef4444; màu dây Đỏ
- 13 | GND | C2 − → G* | màu hình #20252b; màu dây Đen
- 42 | GND | G* → J5V.2 đực AD34 | màu hình #20252b; màu dây Đen
- 43 | GND | J5V.2 cái → U1 GND theo nhãn thật | màu hình #20252b; màu dây Đen

## 04b_day_tin_hieu — Nối dây 14–41: tín hiệu và mass

[SVG](hinh/04b_day_tin_hieu.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Nối dây 14–41: tín hiệu và mass
- Sơ đồ từng liên kết theo net; số dòng khớp bảng 3.7. Không phải đường đi vật lý.
- đề xuất, chưa đo thực tế
- 14
- 3V3
- U1 3V3
- U2 VCC (1)
- 15
- U2 VCC cùng net U1 3V3
- U2 NCS (5)
- 16
- TP3
- 17
- IMU_SDA
- U1 GPIO21
- U2 SDA (4)
- 18
- U2 SDA cùng net GPIO21
- TP2
- 19
- IMU_SCL
- U1 GPIO22
- U2 SCL (3)
- 20
- U2 SCL cùng net GPIO22
- TP1
- 21
- GND
- U2 GND (2)
- G*
- 22
- U2 AD0 (6)
- U2 GND 
- 23
- U2 FSY (8)
- 24
- BTN_LEFT
- U1 GPIO25
- SW2 nhóm A
- 25
- SW2 nhóm B
- 26
- BTN_RIGHT
- U1 GPIO26
- SW3 nhóm A
- 27
- SW3 nhóm B
- 28
- BTN_MODE
- U1 GPIO27
- SW4 nhóm A
- 29
- SW4 nhóm B
- 30
- LED_STATUS
- U1 GPIO32
- R1.1 (1 kΩ)
- 31
- LED_ANODE
- R1.2
- D1 anode A
- 32
- D1 cathode K
- 33
- BAT_SENSE
- R2.2/R3.1 tại AA29
- U1 GPIO34
- 34
- R2.2
- R3.1
- 35
- R2.2/R3.1
- C1.1
- 36
- R3.2
- 37
- C1.2
- 38
- U1 GND N# 14
- 39
- U1 GND N# 32
- 40
- U1 GND N# 38
- 41
- TP4
- Màu dương: các sắc đỏ; GND: đen; B−/GND_BAT_CELL: tím trên hình để tách rõ (dây thật đen nhãn
- B−). SDA xanh lá, SCL vàng, nút xanh dương/trắng có viền/tím, LED cam, SENSE xám. Nhãn net
- luôn là căn cứ chính.
- Nguồn: V2 §3.7; P = bó 2–3 lõi; S = một lõi. Dây đi vòng vùng pin, không đi theo nét logic này.

### Liên kết điện

- 14 | 3V3 | U1 3V3 → U2 VCC (1) | màu hình #a61b29; màu dây Đỏ, nhãn 3V3
- 15 | 3V3 | U2 VCC cùng net U1 3V3 → U2 NCS (5) | màu hình #a61b29; màu dây Đỏ, nhãn NCS
- 16 | 3V3 | U1 3V3 → TP3 | màu hình #a61b29; màu dây Đỏ, nhãn TP3
- 17 | IMU_SDA | U1 GPIO21 → U2 SDA (4) | màu hình #15803d; màu dây Xanh lá
- 18 | IMU_SDA | U2 SDA cùng net GPIO21 → TP2 | màu hình #15803d; màu dây Xanh lá
- 19 | IMU_SCL | U1 GPIO22 → U2 SCL (3) | màu hình #a17a00; màu dây Vàng
- 20 | IMU_SCL | U2 SCL cùng net GPIO22 → TP1 | màu hình #a17a00; màu dây Vàng
- 21 | GND | U2 GND (2) → G* | màu hình #20252b; màu dây Đen
- 22 | GND | U2 AD0 (6) → U2 GND cùng net G* | màu hình #20252b; màu dây Đen, nhãn AD0
- 23 | GND | U2 FSY (8) → U2 GND cùng net G* | màu hình #20252b; màu dây Đen, nhãn FSY
- 24 | BTN_LEFT | U1 GPIO25 → SW2 nhóm A | màu hình #2563eb; màu dây Xanh dương
- 25 | GND | SW2 nhóm B → G* | màu hình #20252b; màu dây Đen
- 26 | BTN_RIGHT | U1 GPIO26 → SW3 nhóm A | màu hình #778696; màu dây Trắng
- 27 | GND | SW3 nhóm B → G* | màu hình #20252b; màu dây Đen
- 28 | BTN_MODE | U1 GPIO27 → SW4 nhóm A | màu hình #9333ea; màu dây Tím
- 29 | GND | SW4 nhóm B → G* | màu hình #20252b; màu dây Đen
- 30 | LED_STATUS | U1 GPIO32 → R1.1 (1 kΩ) | màu hình #d97706; màu dây Cam
- 31 | LED_ANODE | R1.2 → D1 anode A | màu hình #b45309; màu dây Cam, nhãn A
- 32 | GND | D1 cathode K → G* | màu hình #20252b; màu dây Đen
- 33 | BAT_SENSE | R2.2/R3.1 tại AA29 → U1 GPIO34 | màu hình #64748b; màu dây Xám
- 34 | BAT_SENSE | R2.2 → R3.1 | màu hình #64748b; màu dây Nhãn SENSE
- 35 | BAT_SENSE | R2.2/R3.1 → C1.1 | màu hình #64748b; màu dây Xám
- 36 | GND | R3.2 → G* | màu hình #20252b; màu dây Đen
- 37 | GND | C1.2 → G* | màu hình #20252b; màu dây Đen
- 38 | GND | U1 GND nhãn thật, tương ứng N chân 14 → G* | màu hình #20252b; màu dây Đen
- 39 | GND | U1 GND nhãn thật, tương ứng N chân 32 → G* | màu hình #20252b; màu dây Đen
- 40 | GND | U1 GND nhãn thật, tương ứng N chân 38 → G* | màu hình #20252b; màu dây Đen
- 41 | GND | TP4 → G* | màu hình #20252b; màu dây Đen

## 05_imu — IMU WCMCU-20948: 10 chân

[SVG](hinh/05_imu.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- IMU WCMCU-20948: 10 chân
- Số theo netlist; đối chiếu chữ in trên module. Chỉ cắm socket trên carrier.
- đề xuất, chưa đo thực tế
- 01  VCC
- C42
- 3V3
- 02  GND
- D42
- GND
- 03  SCL
- E42
- GPIO22
- 04  SDA
- F42
- GPIO21
- 05  NCS
- G42
- 06  AD0
- H42
- 07  INT
- I42
- ĐỂ HỞ
- 08  FSY
- J42
- 09  ACL
- K42
- 10  ADA
- L42
- VCC/NCS → 3V3; AD0/FSY → GND. INT/ACL/ADA để hở, không ghép bus phụ vào
- SDA/SCL. Định hướng trái/phải của module phải đo thực; C42…L42 chỉ áp dụng khi
- chữ in khớp.
- Nguồn: V2 §3.5.3/3.7 và netlist. 0x68 là địa chỉ chọn bởi AD0=GND, chưa phải kết quả quét mới.

## 06_gpio — ESP32: danh sách chân dùng

[SVG](hinh/06_gpio.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- ESP32: danh sách chân dùng
- Danh sách chân, KHÔNG suy vị trí vật lý từ bo 38 chân tương tự.
- đề xuất, chưa đo thực tế
- CHƯA ĐỦ CĂN CỨ vẽ vị trí chân ESP32. Đối chiếu chữ in trên đúng bo; số
- dưới đây chỉ theo netlist, không phải cách đếm lỗ carrier.
- Nhãn trên bo
- Số netlist
- Nối tới
- 3V3
- 1
- U2 VCC/NCS; TP3
- VIN/5V
- 19
- Từ J5V.1 cái
- GND
- 14, 32, 38
- G* và J5V.2 cái
- GPIO21
- 33
- IMU SDA, TP2
- GPIO22
- 36
- IMU SCL, TP1
- GPIO25
- 9
- SW2 nhóm A
- GPIO26
- 10
- SW3 nhóm A
- GPIO27
- 11
- SW4 nhóm A
- GPIO32
- 7
- R1.1 → D1 A
- GPIO34
- 5
- BAT_SENSE; không nối trực tiếp pin/5V
- GPIO34 chỉ BAT_SENSE, không 5V hay V_SYS trực tiếp. Socket U38…U57 và AE38…AE57 (hoặc
- AD sau đo); không tự gán GPIO theo hàng 38…57.
- Nguồn: bảng GPIO/netlist và V2 §3.7. Pin thật và khoảng hai hàng: CẦN ĐO THỰC TẾ.

## 07_nhan_biet — Nút, LED, điện trở và tụ

[SVG](hinh/07_nhan_biet.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Nút, LED, điện trở và tụ
- Sơ đồ nhận biết; không theo tỉ lệ. Hướng nhóm chân nút chỉ là logic, phải đo.
- đề xuất, chưa đo thực tế
- NÚT 4 CHÂN: đo hai nhóm A/B
- A → GPIO
- B → GND
- nhấn mới thông
- Cùng nhóm luôn thông. Khác nhóm: thả hở, nhấn
- thông. Không đo ohm khi có nguồn; không suy nhóm
- A/B từ góc nhìn hình.
- D1 · LED xanh
- A: chân dài nếu chưa cắt
- K: chân ngắn/vát; diode test
- GPIO32 → R1 → A; K → GND
- A
- K
- ĐIỆN TRỞ 1%, năm vạch (đo lại bằng đồng hồ)
- R1 · 1 kΩ
- nâu – đen – đen – nâu – nâu
- R2/R3 · 100 kΩ
- nâu – đen – đen – cam – nâu
- C1 · 100 nF
- 100 nF / mã 104
- Không phân cực; BAT_SENSE–GND
- C2 · 10 µF, có cực
- 10 µF; có vạch cực âm (−)
- +5V → (+), GND → (−)
- Vạch/độ dài chân chỉ hỗ trợ nhận biết. Chân đã cắt phải đo/đối chiếu nhãn. Đảo C2 có
- thể gây nóng/rò/vỡ; LED phải có R1.
- Nguồn: V2 §3.6/3.12.2, BOM. Không xem hình nhóm chân nút là footprint đã xác nhận.

## 08_thu_tu_han — Thứ tự hàn từ thấp lên cao

[SVG](hinh/08_thu_tu_han.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Thứ tự hàn từ thấp lên cao
- Tám bước; rút mọi nguồn và rút module khỏi socket khi hàn tiếp.
- đề xuất, chưa đo thực tế
- 1. Điện trở
- R1 D19/H19
- R2 AA25/AA29
- R3 AA29/AA33
- Hàn → soi → đo → mới tiếp
- 2. Tụ
- C1 AC29/AC31
- C2 AE35/AG35
- 3. LED
- D1 K19/L19
- 4. Socket / test
- U1 U38…AE57
- U2 B41…M47
- TP1 B50
- TP2 B51
- TP3 B52
- TP4 B53
- 5. Nút
- SW2 H5
- SW4 R5
- SW3 AB5
- 6. SW1
- SW1 AA19…AG22
- 7. J1 / J5V
- J1 gá rời
- J5V AC34/AD34
- 8. Dây nối / đo
- G* P39
- MOD1 A9…L17
- MOD2 N10…AC17
- Làm cụm logic trước trên cùng board; bước nguồn bổ sung sau. J1/J5V và module nguồn gá trên đệm cách
- điện. Mọi hình nhỏ dùng cùng tọa độ với hình TOP.
- Nguồn: V2 §3.6. Không hàn cố định ESP32/IMU vào carrier; chỉ cắm socket.

### Linh kiện và lỗ theo TOP (BOTTOM giữ nguyên tên lỗ)

| Ref | Linh kiện | Tọa độ/đặt | Màu vùng | Nối với |
|---|---|---|---|---|
| SW2 | Nút trái | H5 | #fde6b3 | 24: BTN_LEFT; U1 GPIO25 → SW2 nhóm A<br>25: GND; SW2 nhóm B → G* |
| SW4 | Nút mode | R5 | #fde6b3 | 28: BTN_MODE; U1 GPIO27 → SW4 nhóm A<br>29: GND; SW4 nhóm B → G* |
| SW3 | Nút phải | AB5 | #fde6b3 | 26: BTN_RIGHT; U1 GPIO26 → SW3 nhóm A<br>27: GND; SW3 nhóm B → G* |
| R1 | 1 kΩ | D19/H19 | #f6d7b8 | 30: LED_STATUS; U1 GPIO32 → R1.1 (1 kΩ)<br>31: LED_ANODE; R1.2 → D1 anode A |
| D1 | LED xanh | K19/L19 | #bfe8c1 | 03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B-<br>05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>06: GND; MOD1 OUT- → G*<br>31: LED_ANODE; R1.2 → D1 anode A<br>32: GND; D1 cathode K → G* |
| MOD1 | TP4056 | A9…L17 | #bde4da | 03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B-<br>05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>06: GND; MOD1 OUT- → G* |
| MOD2 | MT3608 | N10…AC17 | #cfe0f9 | 07: V_SYS; SW1 COM → MOD2 VIN+<br>09: GND; G* → MOD2 VIN-<br>10: GND; G* → MOD2 VOUT-<br>11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V |
| SW1 | Công tắc nguồn | AA19…AG22 | #fde6b3 | 05: V_SW_IN; MOD1 OUT+ → SW1 tiếp điểm ON<br>07: V_SYS; SW1 COM → MOD2 VIN+<br>08: V_SYS; SW1 COM → R2.1 |
| J1 | Giắc pin PH2.0 | gá trên dây ngoài vùng pin; CẦN ĐO THỰC TẾ | #e2cef1 | 01: VBAT; BAT1 dây + đã đo → J1 cực + qua đầu ghép<br>02: GND_BAT_CELL; BAT1 dây − đã đo → J1 cực − qua đầu ghép<br>03: VBAT; J1 + → MOD1 B+<br>04: GND_BAT_CELL; J1 − → MOD1 B- |
| R2 | 100 kΩ | AA25/AA29 | #f6d7b8 | 08: V_SYS; SW1 COM → R2.1<br>33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>34: BAT_SENSE; R2.2 → R3.1<br>35: BAT_SENSE; R2.2/R3.1 → C1.1 |
| R3 | 100 kΩ | AA29/AA33 | #f6d7b8 | 33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>34: BAT_SENSE; R2.2 → R3.1<br>35: BAT_SENSE; R2.2/R3.1 → C1.1<br>36: GND; R3.2 → G* |
| C1 | 100 nF | AC29/AC31 | #fbe2b8 | 35: BAT_SENSE; R2.2/R3.1 → C1.1<br>37: GND; C1.2 → G* |
| J5V | Đầu 5V tháo rời | AC34/AD34 | #e2cef1 | 11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V<br>12: 5V; Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35<br>42: GND; G* → J5V.2 đực AD34<br>43: GND; J5V.2 cái → U1 GND theo nhãn thật |
| C2 | 10 µF, có cực | AE35/AG35 | #fbe2b8 | 12: 5V; Phía nguồn J5V.1, cùng VOUT+ → C2 + tại AE35<br>13: GND; C2 − → G* |
| U2 | IMU WCMCU-20948 | B41…M47; C42/D42/E42/F42/G42/H42/I42/J42/K42/L42 | #bfe8c1 | 14: 3V3; U1 3V3 → U2 VCC (1)<br>15: 3V3; U2 VCC cùng net U1 3V3 → U2 NCS (5)<br>17: IMU_SDA; U1 GPIO21 → U2 SDA (4)<br>18: IMU_SDA; U2 SDA cùng net GPIO21 → TP2<br>19: IMU_SCL; U1 GPIO22 → U2 SCL (3)<br>20: IMU_SCL; U2 SCL cùng net GPIO22 → TP1<br>21: GND; U2 GND (2) → G*<br>22: GND; U2 AD0 (6) → U2 GND cùng net G*<br>23: GND; U2 FSY (8) → U2 GND cùng net G* |
| U1 | ESP32 + 2 socket | U38…AE57 | #d3dbe5 | 11: 5V; MOD2 VOUT+ → J5V.1 đực AC34 → J5V.1 cái → U1 VIN/5V<br>14: 3V3; U1 3V3 → U2 VCC (1)<br>15: 3V3; U2 VCC cùng net U1 3V3 → U2 NCS (5)<br>16: 3V3; U1 3V3 → TP3<br>17: IMU_SDA; U1 GPIO21 → U2 SDA (4)<br>19: IMU_SCL; U1 GPIO22 → U2 SCL (3)<br>24: BTN_LEFT; U1 GPIO25 → SW2 nhóm A<br>26: BTN_RIGHT; U1 GPIO26 → SW3 nhóm A<br>28: BTN_MODE; U1 GPIO27 → SW4 nhóm A<br>30: LED_STATUS; U1 GPIO32 → R1.1 (1 kΩ)<br>33: BAT_SENSE; R2.2/R3.1 tại AA29 → U1 GPIO34<br>38: GND; U1 GND nhãn thật, tương ứng N chân 14 → G*<br>39: GND; U1 GND nhãn thật, tương ứng N chân 32 → G*<br>40: GND; U1 GND nhãn thật, tương ứng N chân 38 → G*<br>43: GND; J5V.2 cái → U1 GND theo nhãn thật |
| G* | Điểm chia mass | P39 | #cbd5e1 | 06: GND; MOD1 OUT- → G*<br>09: GND; G* → MOD2 VIN-<br>10: GND; G* → MOD2 VOUT-<br>13: GND; C2 − → G*<br>21: GND; U2 GND (2) → G*<br>22: GND; U2 AD0 (6) → U2 GND cùng net G*<br>23: GND; U2 FSY (8) → U2 GND cùng net G*<br>25: GND; SW2 nhóm B → G*<br>27: GND; SW3 nhóm B → G*<br>29: GND; SW4 nhóm B → G*<br>32: GND; D1 cathode K → G*<br>36: GND; R3.2 → G*<br>37: GND; C1.2 → G*<br>38: GND; U1 GND nhãn thật, tương ứng N chân 14 → G*<br>39: GND; U1 GND nhãn thật, tương ứng N chân 32 → G*<br>40: GND; U1 GND nhãn thật, tương ứng N chân 38 → G*<br>41: GND; TP4 → G*<br>42: GND; G* → J5V.2 đực AD34 |
| TP1 | SCL | B50 | #e0e7ef | 20: IMU_SCL; U2 SCL cùng net GPIO22 → TP1 |
| TP2 | SDA | B51 | #e0e7ef | 18: IMU_SDA; U2 SDA cùng net GPIO21 → TP2 |
| TP3 | 3V3 | B52 | #e0e7ef | 16: 3V3; U1 3V3 → TP3 |
| TP4 | GND | B53 | #e0e7ef | 41: GND; TP4 → G* |
| BAT1 | Pin 1S PCM, chưa chọn | gá trên dây ngoài vùng pin; CẦN ĐO THỰC TẾ | #e2cef1 | 01: VBAT; BAT1 dây + đã đo → J1 cực + qua đầu ghép<br>02: GND_BAT_CELL; BAT1 dây − đã đo → J1 cực − qua đầu ghép |

Vùng pin: B21…Z37; 60.96×40.64 mm, cả hình chiếu hai mặt không chân/dây/vít. Lưới A1 cách mép 3 mm là giả định. Dấu ăng-ten ngoài mép chỉ yêu cầu vị trí, độ nhô CẦN ĐO THỰC TẾ.

## 09_diem_do — Điểm đo và giá trị đối chiếu

[SVG](hinh/09_diem_do.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Điểm đo và giá trị đối chiếu
- Sơ đồ điểm đo logic; que đen phải đúng điểm âm, không luôn lấy B− làm GND.
- đề xuất, chưa đo thực tế
- 1
- Pin/B+
- 3.0–4.2V; pin 1S đúng quy cách
- Que đen: B-
- 2
- Sau bảo vệ
- Gần điện áp pin; chênh áp CẦN ĐO THỰC TẾ
- Que đen: OUT-
- 3
- V_SYS
- SW1 ON: 3.0–4.2V; OFF: gần 0V sau tụ xả
- Que đen: OUT- / GND
- 4
- 5V tại VIN
- 4.9–5.1V, J5V cắm đúng, USB ESP32 rút
- Que đen: GND
- 5
- 3V3
- 3.25–3.35V; mục tiêu 3.3V
- 6
- BAT_SENSE
- ≈0.5×V_SYS; khoảng 1.5–2.1V danh định
- Điện áp dải thiết kế không chứng nhận mọi pin. Tắt nguồn trước đổi dây/đo ohm. ADC và I2C
- cần phần mềm, để chủ dự án làm.
- Nguồn: V2 bảng 3.8.2. Chưa có số đo phần cứng; ghi vào nhật ký, không tick từ hình.

## 10_j5v — Hai trạng thái J5V

[SVG](hinh/10_j5v.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Hai trạng thái J5V
- Quy tắc bắt buộc; J5V là cặp dây +5V/GND, không phải shunt chập hai chân.
- đề xuất, chưa đo thực tế
- CHẠY PIN
- ✓ Cắm J5V đúng chiều + / −
- ✓ RÚT USB ESP32 và USB sạc
- ✓ SW1 ON sau kiểm tra
- ✗ Không đồng thời USB ESP32
- J5V.1 = AC34 +5V; J5V.2 = AD34 GND
- CẮM USB ESP32
- ✓ SW1 OFF, RÚT J5V
- ✓ Chỉ cấp USB vào ESP32
- ✓ Bọc/cố định đầu tháo
- ✗ SW1 OFF một mình chưa đủ
- Tắt SW1 trước cắm/rút. Đầu cái 1 tới VIN, cái 2 tới GND. Cắm đảo có thể chập; đo
- cực và chặn hướng trước vận hành.
- Nguồn: V2 §3.6.8/3.9.1. Không suy có diode trên DevKit tham khảo thành bo thật được cấp hai nguồn.

## 11_ngay_pin_ve — Ngày pin về: 12 bước và điểm dừng

[SVG](hinh/11_ngay_pin_ve.svg). Hướng nhìn: Sơ đồ logic, không theo tỉ lệ vật lý.

### Nhãn hiển thị

- Ngày pin về: 12 bước và điểm dừng
- Chỉ khi có pin thật đúng quy cách. Không đạt phép đo → dừng, ngắt nếu an toàn.
- đề xuất, chưa đo thực tế
- 1
- Đo pin khi tách khỏi mạch
- DC tại giắc pin, khoảng 3.0–4.2V. Ngoài dải, 0V hoặc pack hỏng/phồng
- 2
- Xác nhận cực tại mặt giắc
- que đỏ ở hốc ghép J1+, đen hốc J1− phải hiện điện áp dương bằng bước 1. Đảo/không rõ/giắc sai
- 3
- Đặt trạng thái trước ghép
- SW1 OFF, J5V cắm đúng +/−; với mạch không điện, đo SW1 hở OUT+–COM và kiểm không chập 5V–GND như §3.8. Còn
- nguồn khác hoặc không ngắt được
- 4
- Ghép pin
- sau ghép đo B+–B- bằng pin bước 1, đúng dấu; lệch rõ, nóng/mùi hoặc tia lửa bất thường
- 5
- Đo OUT+–OUT-
- gần bằng B+–B- khi chưa tải; đo V_SYS gần 0V sau tụ xả. OUT=0, áp sai dấu, sụt bất thường
- 6
- Bật SW1
- đo V_SYS so OUT- gần OUT, trong dải thiết kế 3.0–4.2V; sụt/reset/nóng
- 7
- Đo VIN ESP32
- 4.9–5.1V [A] §5.1/[N] §1; ngoài khoảng/dao động rõ
- 8
- Đo 3V3 tại ESP32/TP3 và IMU VCC
- 3.25–3.35V theo tiêu chí [N] §1; sai/chạm que nguy hiểm
- 9
- Đo BAT_SENSE tại GPIO34
- khoảng 0.5×V_SYS; tỷ số 0.495–0.505 từ R2/R3 1% [B], cộng sai số đo. Sai tỷ số/tiến gần điện áp pin thô
- 10
- Quan sát khởi động và nhiệt
- kiểm LED/hành vi chương trình thử đã biết; ưu tiên nhiệt kế đo TP4056, MT3608 và vỏ pin, ghi số thật. Chỉ
- chạm nhẹ phần vỏ còn nguyên/không dẫn điện khi không có nhiệt…
- 11
- Chạy đầu 5 phút có người theo dõi
- đo lại VIN/3V3/V_SYS và nhiệt đầu/cuối, ghi reset/sụt áp. Mốc 5 phút là đề xuất [P2] §3.13.4, chưa chứng
- minh thời lượng/độ bền; lỗi
- 12
- Thử sạc riêng sau khi đọc §3.9.2
- SW1 OFF, J5V rút, USB ESP32 rút; đo dòng pin nối tiếp và B+–B- theo §3.4.4, hướng đến 4.2V danh định [T]
- trong giới hạn pack. Theo dõi sát 5–10 phút đầu và suốt lần sạc;…
- ✗ Sai cực/áp, sụt/reset, nóng/phồng/mùi → DỪNG. Mọi ngưỡng và đầy đủ 12 bước: V2 §3.13.4 và mô
- tả chữ đi kèm.
- Nguồn: V2 §3.13.4. Sạc riêng sau đọc rủi ro §3.9.2; không sạc nguồn bàn thay pin.

### Nguyên văn 12 bước từ dữ liệu V2

1. **Đo pin khi tách khỏi mạch:** DC tại giắc pin, khoảng 3.0–4.2V. Ngoài dải, 0V hoặc pack hỏng/phồng → dừng; không kích/bypass bảo vệ.
2. **Xác nhận cực tại mặt giắc:** que đỏ ở hốc ghép J1+, đen hốc J1− phải hiện điện áp dương bằng bước 1. Đảo/không rõ/giắc sai → dừng, xử lý §3.13.3.
3. **Đặt trạng thái trước ghép:** SW1 OFF, J5V cắm đúng +/−; với mạch không điện, đo SW1 hở OUT+–COM và kiểm không chập 5V–GND như §3.8. Còn nguồn khác hoặc không ngắt được → dừng.
4. **Ghép pin:** sau ghép đo B+–B- bằng pin bước 1, đúng dấu; lệch rõ, nóng/mùi hoặc tia lửa bất thường → ngắt nếu an toàn và dừng.
5. **Đo OUT+–OUT-:** gần bằng B+–B- khi chưa tải; đo V_SYS gần 0V sau tụ xả. OUT=0, áp sai dấu, sụt bất thường → dừng kiểm bảo vệ, không bypass.
6. **Bật SW1:** đo V_SYS so OUT- gần OUT, trong dải thiết kế 3.0–4.2V; sụt/reset/nóng → OFF và dừng. Không thử xả thêm pin yếu để đạt phép này.
7. **Đo VIN ESP32:** 4.9–5.1V [A] §5.1/[N] §1; ngoài khoảng/dao động rõ → OFF, không chỉnh bừa khi tải đang có lỗi.
8. **Đo 3V3 tại ESP32/TP3 và IMU VCC:** 3.25–3.35V theo tiêu chí [N] §1; sai/chạm que nguy hiểm → OFF, kiểm lại.
9. **Đo BAT_SENSE tại GPIO34:** khoảng 0.5×V_SYS; tỷ số 0.495–0.505 từ R2/R3 1% [B], cộng sai số đo. Sai tỷ số/tiến gần điện áp pin thô → OFF, không tiếp tục để bảo vệ ADC.
10. **Quan sát khởi động và nhiệt:** kiểm LED/hành vi chương trình thử đã biết; ưu tiên nhiệt kế đo TP4056, MT3608 và vỏ pin, ghi số thật. Chỉ chạm nhẹ phần vỏ còn nguyên/không dẫn điện khi không có nhiệt kế; tay không cho giá trị °C. Reset/nóng bất thường/phồng/mùi → OFF, không cắm USB để xem log khi J5V còn ghép.
11. **Chạy đầu 5 phút có người theo dõi:** đo lại VIN/3V3/V_SYS và nhiệt đầu/cuối, ghi reset/sụt áp. Mốc 5 phút là đề xuất [P2] §3.13.4, chưa chứng minh thời lượng/độ bền; lỗi → OFF và dừng.
12. **Thử sạc riêng sau khi đọc §3.9.2:** SW1 OFF, J5V rút, USB ESP32 rút; đo dòng pin nối tiếp và B+–B- theo §3.4.4, hướng đến 4.2V danh định [T] trong giới hạn pack. Theo dõi sát 5–10 phút đầu và suốt lần sạc; nóng/phồng/mùi/áp hoặc dòng vượt mức đã biết → rút USB sạc và xử lý §3.2.
