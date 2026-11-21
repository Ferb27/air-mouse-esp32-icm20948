import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('deliverables/assets', exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def create_system_block_diagram():
    fig, ax = plt.subplots(figsize=(11.2, 6.4), dpi=250)
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 6.4)
    ax.axis('off')

    c_mcu = '#EBF3FA'
    c_mcu_border = '#1F4E79'
    c_imu = '#FFF2CC'
    c_imu_border = '#D6B656'
    c_pwr = '#F8CECC'
    c_pwr_border = '#B85450'
    c_pc = '#E1D5E7'
    c_pc_border = '#9673A6'
    c_btn = '#D5E8D4'
    c_btn_border = '#82B366'
    c_tp = '#E8F5E9'
    c_tp_border = '#4CAF50'

    ax.text(5.6, 6.18, 'SƠ ĐỒ KHỐI KIẾN TRÚC HỆ THỐNG AIR MOUSE BLE HID (DIRECT 3.3V BASELINE)', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1F4E79')

    # ESP32 Box
    mcu_box = patches.FancyBboxPatch((3.8, 1.45), 4.3, 4.4, boxstyle='round,pad=0.1', 
                                     facecolor=c_mcu, edgecolor=c_mcu_border, linewidth=1.5)
    ax.add_patch(mcu_box)
    ax.text(5.95, 5.6, 'VI ĐIỀU KHIỂN ESP32 CLASSIC (DevKit 38-pin)', 
            ha='center', va='center', fontsize=10, fontweight='bold', color=c_mcu_border)

    ax.add_patch(patches.Rectangle((4.0, 4.5), 3.9, 0.75, facecolor='white', edgecolor=c_mcu_border, linewidth=1))
    ax.text(5.95, 4.95, 'I2C Controller (Master Mode - Fast Mode ≤ 400 kHz)', ha='center', va='center', fontsize=8.5, fontweight='bold')
    ax.text(5.95, 4.7, 'SDA (GPIO21)  |  SCL (GPIO22) nối trực tiếp cảm biến', ha='center', va='center', fontsize=8, color='#333333')

    ax.add_patch(patches.Rectangle((4.0, 3.4), 3.9, 0.95, facecolor='white', edgecolor=c_mcu_border, linewidth=1))
    ax.text(5.95, 4.1, 'Firmware Motion Engine (6-axis Gyro-Accel Fusion)', ha='center', va='center', fontsize=8.5, fontweight='bold')
    ax.text(5.95, 3.85, 'Burst Read 12B → Bù Bias → Quat 6 trục (K=2.0) → Adaptive Frame', ha='center', va='center', fontsize=7.2, color='#333333')
    ax.text(5.95, 3.6, 'Dead-zone → Rate-Control (dX, dY) | Lateral Flick | BLE Mouse Report', ha='center', va='center', fontsize=7.2, color='#333333')

    ax.add_patch(patches.Rectangle((4.0, 2.3), 3.9, 0.95, facecolor='white', edgecolor=c_mcu_border, linewidth=1))
    ax.text(5.95, 3.0, 'GPIO & ADC1 Subsystem (Độc lập Wi-Fi/BLE)', ha='center', va='center', fontsize=8.5, fontweight='bold')
    ax.text(5.95, 2.75, 'Nút bấm Active-Low: BTN_LEFT (25), BTN_RIGHT (26), BTN_MODE (27)', ha='center', va='center', fontsize=7, color='#333333')
    ax.text(5.95, 2.55, 'Chỉ thị: LED_STATUS (GPIO32)  |  Đo pin: BAT_SENSE (GPIO34 / ADC1_CH6)', ha='center', va='center', fontsize=7, color='#333333')
    ax.text(5.95, 2.38, 'Chân VIN: 5V (từ MT3608)  |  Chân 3V3: Cấp nguồn trực tiếp cho IMU', ha='center', va='center', fontsize=6.8, color='#990000')

    ax.add_patch(patches.Rectangle((4.0, 1.6), 3.9, 0.55, facecolor='white', edgecolor=c_mcu_border, linewidth=1))
    ax.text(5.95, 1.88, 'BLE Subsystem (HID over GATT Profile - HOGP v1.1.1)', ha='center', va='center', fontsize=8.5, fontweight='bold')

    # IMU Box (Direct 3.3V, WCMCU-20948)
    imu_box = patches.FancyBboxPatch((0.4, 3.75), 2.3, 2.1, boxstyle='round,pad=0.08', 
                                     facecolor=c_imu, edgecolor=c_imu_border, linewidth=1.3)
    ax.add_patch(imu_box)
    ax.text(1.55, 5.65, 'CẢM BIẾN IMU 9-DOF', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#B45F06')
    ax.text(1.55, 5.4, 'WCMCU-20948 (ICM-20948)', ha='center', va='center', fontsize=8, fontweight='bold')
    ax.text(1.55, 4.65, '• Gyro 3 trục (±500 °/s)\n• Accel 3 trục (±4g)\n• Hardware DLPF (51.2 Hz)\n• Miền nguồn: VCC = 3.3V (Trực tiếp)\n• Trở kéo onboard: 10kΩ trên SDA/SCL\n• Địa chỉ I2C: 0x68 (AD0 nối GND)\n• Bring-up Pass: WHO_AM_I = 0xEA', 
            ha='center', va='center', fontsize=6.8, color='#333333')

    # Test Points Box (TP1-TP4)
    tp_box = patches.FancyBboxPatch((2.85, 3.9), 0.8, 1.25, boxstyle='round,pad=0.05', 
                                    facecolor=c_tp, edgecolor=c_tp_border, linewidth=1.1)
    ax.add_patch(tp_box)
    ax.text(3.25, 4.95, 'TEST\nPOINTS', ha='center', va='center', fontsize=7.0, fontweight='bold', color='#2E7D32')
    ax.text(3.25, 4.35, 'TP1: SCL\nTP2: SDA\nTP3: 3V3\nTP4: GND\n(Dải 1x4)', ha='center', va='center', fontsize=6.0, color='#333333')

    # Buttons Box
    btn_box = patches.FancyBboxPatch((0.4, 1.8), 2.3, 1.7, boxstyle='round,pad=0.08', 
                                     facecolor=c_btn, edgecolor=c_btn_border, linewidth=1.3)
    ax.add_patch(btn_box)
    ax.text(1.55, 3.25, '3 NÚT NHẤN TACTILE', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#274E13')
    ax.text(1.55, 2.55, '• Left Click  (GPIO25)\n• Right Click (GPIO26)\n• Mode/Air (GPIO27)\nCấu hình Active-Low\nĐiện trở kéo lên nội pull-up\nKhử rung phần mềm 15-20 ms', 
            ha='center', va='center', fontsize=7.0, color='#333333')

    # Power & Battery Divider Box (SEPARATED CLEARLY)
    pwr_box = patches.FancyBboxPatch((0.4, 0.22), 7.7, 1.05, boxstyle='round,pad=0.08', 
                                     facecolor=c_pwr, edgecolor=c_pwr_border, linewidth=1.3)
    ax.add_patch(pwr_box)
    ax.text(4.25, 1.08, 'KHỐI NGUỒN PIN VÀ ĐO ĐIỆN ÁP (KIẾN TRÚC TRỰC TIẾP 3.3V — ĐÃ LOẠI BỎ BSS138 & LDO 1.8V)', 
            ha='center', va='center', fontsize=8.2, fontweight='bold', color='#990000')
    ax.text(4.25, 0.76, '• POWER PATH: Pin LiPo 1S (3.7V) → Sạc TP4056 → Công tắc SW1 → MT3608 Boost 5V cấp chân VIN của ESP32 DevKit.\n  LDO 3.3V trên board DevKit cấp 3.3V nuôi trực tiếp module WCMCU-20948 (đã đo kiểm và xác nhận hoạt động trên phần cứng thật).', 
            ha='center', va='center', fontsize=6.8, color='#333333')
    ax.text(4.25, 0.44, '• BATTERY SENSE PATH: Cực dương Pin VBAT sau công tắc V_SYS (3.0–4.2V) → Cầu phân áp (100kΩ / 100kΩ) → BAT_SENSE (1.5–2.1V)\n  gửi về chân GPIO34 (ADC1_CH6). LƯU Ý: Chân ADC KHÔNG nhận nguồn 5V VIN trực tiếp!', 
            ha='center', va='center', fontsize=6.8, fontweight='bold', color='#B85450')

    # PC Host Box
    pc_box = patches.FancyBboxPatch((8.9, 2.3), 2.1, 2.8, boxstyle='round,pad=0.08', 
                                    facecolor=c_pc, edgecolor=c_pc_border, linewidth=1.3)
    ax.add_patch(pc_box)
    ax.text(9.95, 4.85, 'MÁY TÍNH CHỦ (HOST)', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#4C1130')
    ax.text(9.95, 4.55, 'Windows / macOS / Linux', ha='center', va='center', fontsize=7.5)
    ax.text(9.95, 3.95, '• BLE Central Role\n• Driver Generic HID\n  (Không cần driver ngoài)\n• Nhận báo cáo chuột:\n  - Buttons bitmask\n  - ΔX, ΔY con trỏ', 
            ha='center', va='center', fontsize=7.2, color='#333333')
    ax.text(9.95, 2.85, 'CON TRỎ CHUỘT\nDI CHUYỂN THEO TỐC ĐỘ\nXOAY CỔ TAY', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#4C1130')

    # Annotations
    ax.annotate('Xoay cổ tay\n(Yaw / Pitch)', xy=(0.4, 4.8), xytext=(-0.55, 4.8),
                arrowprops=dict(facecolor='#333333', arrowstyle='->', lw=1.2),
                ha='center', va='center', fontsize=7.5, fontweight='bold')

    # Direct I2C Connection Arrow
    ax.annotate('', xy=(3.8, 5.3), xytext=(2.7, 5.3),
                arrowprops=dict(facecolor='#1F4E79', edgecolor='#1F4E79', arrowstyle='<->', lw=1.8))
    ax.text(3.25, 5.48, 'BUS I2C 3.3V\n(400 kHz)', ha='center', va='bottom', fontsize=6.8, fontweight='bold', color='#1F4E79')

    # Buttons Arrow
    ax.annotate('', xy=(3.8, 2.65), xytext=(2.7, 2.65),
                arrowprops=dict(facecolor='#274E13', arrowstyle='->', lw=1.2))
    ax.text(3.25, 2.85, 'GPIOs', ha='center', va='center', fontsize=7.5, color='#274E13')

    # SEPARATE ARROWS FOR POWER AND BAT_SENSE:
    # 1. Power arrow (5V VIN)
    ax.annotate('', xy=(4.6, 1.45), xytext=(4.6, 1.27),
                arrowprops=dict(facecolor='#990000', edgecolor='#990000', arrowstyle='->', lw=1.5))
    ax.text(4.6, 1.36, 'Nguồn 5V (vào chân VIN)', ha='right', va='center', fontsize=6.8, fontweight='bold', color='#990000')

    # 2. Battery sense arrow (VBAT divider -> GPIO34)
    ax.annotate('', xy=(7.3, 2.3), xytext=(7.3, 1.27),
                arrowprops=dict(facecolor='#D79B00', edgecolor='#D79B00', arrowstyle='->', lw=1.5, linestyle='--'))
    ax.text(7.4, 1.75, 'BAT_SENSE (1.5-2.1V)\nvào GPIO34 / ADC1_CH6\n(qua cầu phân áp, KHÔNG nối 5V)', ha='left', va='center', fontsize=6.5, fontweight='bold', color='#B45F06')

    # Wireless BLE arrow
    ax.annotate('', xy=(8.9, 3.75), xytext=(8.1, 3.75),
                arrowprops=dict(facecolor='#9673A6', arrowstyle='->', lw=1.8, linestyle='--'))
    ax.text(8.5, 4.05, 'SÓNG BLE 2.4GHz', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#4C1130')
    ax.text(8.5, 3.45, 'Bản tin chuột\nHID Report', ha='center', va='center', fontsize=7, color='#4C1130')

    plt.tight_layout()
    plt.savefig('deliverables/assets/fig_system_block_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_i2c_transaction_diagram():
    fig, ax = plt.subplots(figsize=(10, 2.6), dpi=250)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.6)
    ax.axis('off')

    ax.text(5.0, 2.4, 'SƠ ĐỒ GIAO THỨC ĐỌC THANH GHI QUA I2C VỚI REPEATED START', 
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1F4E79')

    boxes = [
        ('S', 'START', 0.1, 0.6, '#D5E8D4', '#274E13', 'M'),
        ('Slave Addr + W\n0x68 + 0 (0xD0)', 'Địa chỉ Slave + Ghi', 0.7, 1.6, '#DAE8FC', '#1F4E79', 'M'),
        ('ACK', 'Xác nhận', 2.3, 0.6, '#FFE6CC', '#D79B00', 'S'),
        ('Register Addr\n(Ví dụ: 0x06)', 'Địa chỉ thanh ghi', 2.9, 1.6, '#DAE8FC', '#1F4E79', 'M'),
        ('ACK', 'Xác nhận', 4.5, 0.6, '#FFE6CC', '#D79B00', 'S'),
        ('Sr', 'REPEATED\nSTART', 5.1, 0.8, '#D5E8D4', '#274E13', 'M'),
        ('Slave Addr + R\n0x68 + 1 (0xD1)', 'Địa chỉ Slave + Đọc', 5.9, 1.6, '#DAE8FC', '#1F4E79', 'M'),
        ('ACK', 'Xác nhận', 7.5, 0.6, '#FFE6CC', '#D79B00', 'S'),
        ('Data Byte\n(Dữ liệu đọc về)', 'Giá trị thanh ghi', 8.1, 1.2, '#FFF2CC', '#B45F06', 'S'),
        ('NACK', 'Hết đọc', 9.3, 0.45, '#F8CECC', '#B85450', 'M'),
        ('P', 'STOP', 9.8, 0.4, '#E1D5E7', '#9673A6', 'M')
    ]

    for title, desc, x, w, fc, ec, role in boxes:
        rect = patches.Rectangle((x, 0.7), w-0.03, 1.1, facecolor=fc, edgecolor=ec, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + (w-0.03)/2, 1.25, title, ha='center', va='center', fontsize=6.8, fontweight='bold', color=ec)
        ax.text(x + (w-0.03)/2, 0.45, f'[{role}]', ha='center', va='center', fontsize=6.5, fontweight='bold', color='#555555')

    ax.text(5.0, 0.15, 'Chú thích: [M] = Do I2C Master (ESP32) phát  |  [S] = Do I2C Slave (ICM-20948) phản hồi', 
            ha='center', va='center', fontsize=7.5, style='italic', color='#444444')

    plt.tight_layout()
    plt.savefig('deliverables/assets/fig_i2c_transaction.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_bank_switching_diagram():
    fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=250)
    ax.set_xlim(0, 9.2)
    ax.set_ylim(0, 4.0)
    ax.axis('off')

    ax.text(4.6, 3.75, 'CƠ CHẾ PHÂN CHIA VÀ CHUYỂN USER BANK TRÊN CHIP ICM-20948 (TDK DS-000189)', 
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1F4E79')

    sel_box = patches.FancyBboxPatch((0.4, 0.9), 2.6, 2.3, boxstyle='round,pad=0.08', 
                                     facecolor='#DAE8FC', edgecolor='#1F4E79', linewidth=1.4)
    ax.add_patch(sel_box)
    ax.text(1.7, 2.9, 'REG_BANK_SEL', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1F4E79')
    ax.text(1.7, 2.55, 'Địa chỉ: 0x7F', ha='center', va='center', fontsize=8.5, fontweight='bold')
    ax.text(1.7, 2.25, 'Cố định trên cả 4 Bank', ha='center', va='center', fontsize=7.5, style='italic')
    ax.text(1.7, 1.5, 'Ghi Bits [5:4]:\n• 00: Bank 0 (0x00)\n• 01: Bank 1 (0x10)\n• 10: Bank 2 (0x20)\n• 11: Bank 3 (0x30)', 
            ha='center', va='center', fontsize=7.2, color='#222222')

    banks = [
        ('USER BANK 0 (0x00)', 'PWR_MGMT_1 (0x06), WHO_AM_I (0x00 = 0xEA)\nGYRO_XOUT, ACCEL_XOUT (0x2D-0x38)\nEXT_SLV_SENS_DATA_00..23 (Đệm dữ liệu cảm biến ngoài)', 2.65, '#D5E8D4', '#274E13'),
        ('USER BANK 1 (0x10)', 'Self-Test, Offset Bias Calibration registers\nCấu hình cơ sở thời gian (Time-base) của cảm biến', 1.85, '#F5F5F5', '#666666'),
        ('USER BANK 2 (0x20)', 'GYRO_CONFIG_1 (0x01 = 0x1B), GYRO_SMPLRT_DIV (0x00 = 10)\nACCEL_CONFIG (0x14 = 0x1B), ACCEL_SMPLRT_DIV (0x10-11 = 10)', 1.05, '#FFF2CC', '#B45F06'),
        ('USER BANK 3 (0x30)', 'Cấu hình & Điều khiển I2C Master nội bộ\n(I2C_MST_CTRL, I2C_SLVx_ADDR, I2C_SLVx_REG, I2C_SLVx_CTRL)', 0.25, '#F5F5F5', '#666666')
    ]

    for title, desc, y, fc, ec in banks:
        box = patches.FancyBboxPatch((3.9, y), 5.0, 0.68, boxstyle='round,pad=0.05', 
                                     facecolor=fc, edgecolor=ec, linewidth=1.2)
        ax.add_patch(box)
        ax.text(4.1, y + 0.48, title, ha='left', va='center', fontsize=8, fontweight='bold', color=ec)
        ax.text(4.1, y + 0.22, desc, ha='left', va='center', fontsize=6.8, color='#333333')

        ax.annotate('', xy=(3.9, y + 0.34), xytext=(3.0, 2.0),
                    arrowprops=dict(facecolor=ec, edgecolor=ec, arrowstyle='->', lw=1.0))

    plt.tight_layout()
    plt.savefig('deliverables/assets/fig_bank_switching.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_motion_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 3.6), dpi=250)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 3.6)
    ax.axis('off')

    ax.text(5.75, 3.35, 'PIPELINE XỬ LÝ CHUYỂN ĐỘNG: PHÂN ĐỊNH HARDWARE DLPF VÀ FIRMWARE ENGINE', 
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1F4E79')

    # Domain 1 Background: ICM-20948 Hardware
    dom1_bg = patches.FancyBboxPatch((0.2, 0.65), 4.7, 2.4, boxstyle='round,pad=0.08',
                                    facecolor='#FFF9E6', edgecolor='#D6B656', linewidth=1.2, linestyle=':')
    ax.add_patch(dom1_bg)
    ax.text(2.55, 2.85, 'KHỐI PHẦN CỨNG NỘI BỘ CẢM BIẾN ICM-20948', ha='center', va='center',
            fontsize=8, fontweight='bold', color='#B45F06')

    # Domain 2 Background: ESP32 Firmware
    dom2_bg = patches.FancyBboxPatch((5.1, 0.65), 6.2, 2.4, boxstyle='round,pad=0.08',
                                    facecolor='#EBF3FA', edgecolor='#1F4E79', linewidth=1.2, linestyle=':')
    ax.add_patch(dom2_bg)
    ax.text(8.2, 2.85, 'KHỐI FIRMWARE ENGINE TRÊN VI ĐIỀU KHIỂN ESP32', ha='center', va='center',
            fontsize=8, fontweight='bold', color='#1F4E79')

    # Stages in Domain 1 (Hardware)
    hw_stages = [
        ('1. Cơ học cổ tay', 'Xoay cổ tay (ω)\n+ Vung tịnh tiến (a)', 0.35, 0.95, '#FFFFFF', '#333333'),
        ('2. MEMS 6 trục', 'Khối vi cơ Gyro+Accel\n+ ADC 16-bit nội', 1.45, 1.05, '#FFF2CC', '#B45F06'),
        ('3. Hardware DLPF', 'DLPF Gyro 51.2Hz\nDLPF Accel 50.4Hz', 2.65, 1.1, '#FFE6CC', '#D79B00'),
        ('4. Thanh ghi xuất', 'ACCEL + GYRO\n(Bank 0, 12B thô 0x2D-38)', 3.9, 0.95, '#FFFFFF', '#B45F06'),
    ]

    for title, desc, x, w, fc, ec in hw_stages:
        box = patches.FancyBboxPatch((x, 0.85), w, 1.7, boxstyle='round,pad=0.04', facecolor=fc, edgecolor=ec, linewidth=1.1)
        ax.add_patch(box)
        ax.text(x + w/2, 2.25, title, ha='center', va='center', fontsize=6.8, fontweight='bold', color=ec)
        ax.text(x + w/2, 1.4, desc, ha='center', va='center', fontsize=6.2, color='#333333')
        if x < 3.8:
            ax.annotate('', xy=(x + w + 0.12, 1.7), xytext=(x + w, 1.7),
                        arrowprops=dict(facecolor='#555555', arrowstyle='->', lw=0.9))

    # Connection across boundary: I2C Burst Read
    ax.annotate('', xy=(5.25, 1.7), xytext=(4.9, 1.7),
                arrowprops=dict(facecolor='#1F4E79', edgecolor='#1F4E79', arrowstyle='->', lw=1.5))
    ax.text(5.07, 1.95, 'Bus I2C\n(Burst 12B)', ha='center', va='center', fontsize=6.2, fontweight='bold', color='#1F4E79')

    # Stages in Domain 2 (Firmware)
    fw_stages = [
        ('5. Burst Read 12B', 'Ghép int16_t\nAccel ±4g, Gyro ±500dps', 5.25, 1.1, '#D5E8D4', '#274E13'),
        ('6. Bù Bias & Tĩnh', 'Trừ Zero-Rate Bias\nStationary Detector', 6.5, 1.05, '#FFF2CC', '#B45F06'),
        ('7. Fusion & Nghiêng', 'Quat 6 trục, K=2.0\nƯớc lượng trọng trường', 7.7, 1.05, '#F8CECC', '#B85450'),
        ('8. Chiếu hệ quy chiếu', 'Clutch / Recenter\nLinear Accel / Flick', 8.9, 1.05, '#E1D5E7', '#9673A6'),
        ('9. Rate Mapping & BLE', 'dX, dY qua BLE HID\nMouse Report (100 Hz)', 10.1, 1.05, '#DAE8FC', '#1F4E79')
    ]

    for title, desc, x, w, fc, ec in fw_stages:
        box = patches.FancyBboxPatch((x, 0.85), w, 1.7, boxstyle='round,pad=0.04', facecolor=fc, edgecolor=ec, linewidth=1.1)
        ax.add_patch(box)
        ax.text(x + w/2, 2.25, title, ha='center', va='center', fontsize=6.8, fontweight='bold', color=ec)
        ax.text(x + w/2, 1.4, desc, ha='center', va='center', fontsize=6.2, color='#333333')
        if x < 10.0:
            ax.annotate('', xy=(x + w + 0.12, 1.7), xytext=(x + w, 1.7),
                        arrowprops=dict(facecolor='#555555', arrowstyle='->', lw=0.9))

    ax.text(5.75, 0.22, 'Bản chất 6-axis Fusion: Gyro điều khiển tốc độ xoay Rate-Control; Accel hiệu chỉnh nghiêng Quaternion & nhận dạng Flick qua gia tốc tuyến tính. Magnetometer chưa dùng. Chuột dừng khi vận tốc tiệm cận 0.', 
            ha='center', va='center', fontsize=7.5, style='italic', color='#333333')

    plt.tight_layout()
    plt.savefig('deliverables/assets/fig_motion_pipeline.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_bitfield_diagrams():
    # PWR_MGMT_1
    fig, ax = plt.subplots(figsize=(8.5, 2.0), dpi=250)
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 2.0)
    ax.axis('off')

    ax.text(4.25, 1.8, 'THANH GHI PWR_MGMT_1 (Bank 0, Địa chỉ 0x06) — Giá trị cấu hình: 0x01 (0b00000001)', 
            ha='center', va='center', fontsize=9.0, fontweight='bold', color='#1F4E79')

    bits_pwr = [
        ('Bit 7', 'DEVICE_RESET', '0', '#DAE8FC', '#1F4E79'),
        ('Bit 6', 'SLEEP', '0', '#DAE8FC', '#1F4E79'),
        ('Bit 5', 'LP_EN', '0', '#DAE8FC', '#1F4E79'),
        ('Bit 4', 'Reserved', '0', '#F5F5F5', '#666666'),
        ('Bit 3', 'TEMP_DIS', '0', '#DAE8FC', '#1F4E79'),
        ('Bit 2', 'CLKSEL[2]', '0', '#FFF2CC', '#B45F06'),
        ('Bit 1', 'CLKSEL[1]', '0', '#FFF2CC', '#B45F06'),
        ('Bit 0', 'CLKSEL[0]', '1', '#FFF2CC', '#B45F06'),
    ]

    for i, (bnum, bname, bval, fc, ec) in enumerate(bits_pwr):
        x = 0.4 + i * 0.96
        rect = patches.Rectangle((x, 0.5), 0.9, 1.0, facecolor=fc, edgecolor=ec, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + 0.45, 1.3, bnum, ha='center', va='center', fontsize=7.2, fontweight='bold', color=ec)
        ax.text(x + 0.45, 1.0, bname, ha='center', va='center', fontsize=5.8, fontweight='bold', color='#222222')
        ax.text(x + 0.45, 0.72, f'Bit = {bval}', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#990000' if bval=='1' else '#1F4E79')

    ax.text(4.25, 0.2, 'Tác động phần cứng: Đánh thức chip khỏi Sleep (Bit 6=0) và Tự động chọn nguồn xung PLL tốt nhất (Bits [2:0]=001, dự phòng dao động nội).', 
            ha='center', va='center', fontsize=7.2, style='italic', color='#333333')

    plt.tight_layout()
    plt.savefig('deliverables/assets/fig_bitfield_pwr_mgmt_1.png', dpi=300, bbox_inches='tight')
    plt.close()

    # GYRO_CONFIG_1
    fig, ax = plt.subplots(figsize=(8.5, 2.0), dpi=250)
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 2.0)
    ax.axis('off')

    ax.text(4.25, 1.8, 'THANH GHI GYRO_CONFIG_1 (Bank 2, Địa chỉ 0x01) — Giá trị cấu hình: 0x1B (0b00011011)', 
            ha='center', va='center', fontsize=9.0, fontweight='bold', color='#1F4E79')

    bits_gyro = [
        ('Bit 7', 'Reserved', '0', '#F5F5F5', '#666666'),
        ('Bit 6', 'Reserved', '0', '#F5F5F5', '#666666'),
        ('Bit 5', 'DLPFCFG[2]', '0', '#D5E8D4', '#274E13'),
        ('Bit 4', 'DLPFCFG[1]', '1', '#D5E8D4', '#274E13'),
        ('Bit 3', 'DLPFCFG[0]', '1', '#D5E8D4', '#274E13'),
        ('Bit 2', 'FS_SEL[1]', '0', '#FFE6CC', '#D79B00'),
        ('Bit 1', 'FS_SEL[0]', '1', '#FFE6CC', '#D79B00'),
        ('Bit 0', 'FCHOICE', '1', '#DAE8FC', '#1F4E79'),
    ]

    for i, (bnum, bname, bval, fc, ec) in enumerate(bits_gyro):
        x = 0.4 + i * 0.96
        rect = patches.Rectangle((x, 0.5), 0.9, 1.0, facecolor=fc, edgecolor=ec, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + 0.45, 1.3, bnum, ha='center', va='center', fontsize=7.2, fontweight='bold', color=ec)
        ax.text(x + 0.45, 1.0, bname, ha='center', va='center', fontsize=5.8, fontweight='bold', color='#222222')
        ax.text(x + 0.45, 0.72, f'Bit = {bval}', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#990000' if bval=='1' else '#1F4E79')

    ax.text(4.25, 0.2, 'Tác động phần cứng: Kích hoạt DLPF (Bit 0=1), Băng thông DLPF 51.2Hz làm suy giảm nhiễu cao tần (Bits [5:3]=011), Dải đo ±500°/s (Bits [2:1]=01).', 
            ha='center', va='center', fontsize=7.2, style='italic', color='#333333')

    plt.tight_layout()
    plt.savefig('deliverables/assets/fig_bitfield_gyro_config_1.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_system_block_diagram()
    create_i2c_transaction_diagram()
    create_bank_switching_diagram()
    create_motion_pipeline_diagram()
    create_bitfield_diagrams()
    print('All diagrams updated and regenerated successfully!')
