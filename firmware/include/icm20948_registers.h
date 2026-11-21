#ifndef ICM20948_REGISTERS_H
#define ICM20948_REGISTERS_H

#include <stdint.h>

// =============================================================================
// TDK INVESENSE ICM-20948 REGISTER MAP SPECIFICATION (DS-000189)
// =============================================================================

// Bank Selection Register (Appears across all Banks at fixed address 0x7F)
#define REG_BANK_SEL            0x7F

// --- USER BANK 0: System Control & Primary Data Output ---
#define REG_WHO_AM_I            0x00    // Read-only. Expected value = 0xEA
#define VAL_WHO_AM_I_EXPECTED   0xEA

#define REG_USER_CTRL           0x03    // DMP, I2C Master, SRAM reset
#define REG_LP_CONFIG           0x05    // Duty cycle mode control
#define REG_PWR_MGMT_1          0x06    // Device reset, Sleep, Clock select
#define REG_PWR_MGMT_2          0x07    // Accel & Gyro individual axis power disable
#define REG_INT_PIN_CFG         0x0F    // Interrupt pin bypass & latching config
#define REG_INT_ENABLE_1        0x11    // Raw data ready interrupt enable

// Accelerometer Data Output (Bank 0)
#define REG_ACCEL_XOUT_H        0x2D
#define REG_ACCEL_XOUT_L        0x2E
#define REG_ACCEL_YOUT_H        0x2F
#define REG_ACCEL_YOUT_L        0x30
#define REG_ACCEL_ZOUT_H        0x31
#define REG_ACCEL_ZOUT_L        0x32

// Gyroscope Data Output (Bank 0)
#define REG_GYRO_XOUT_H         0x33
#define REG_GYRO_XOUT_L         0x34
#define REG_GYRO_YOUT_H         0x35
#define REG_GYRO_YOUT_L         0x36
#define REG_GYRO_ZOUT_H         0x37
#define REG_GYRO_ZOUT_L         0x38

// Temperature Data Output (Bank 0)
#define REG_TEMP_OUT_H          0x39
#define REG_TEMP_OUT_L          0x3A

// --- USER BANK 1: Self-Test & Filter Configuration ---
// (Not strictly required for P0/P1 baseline)

// --- USER BANK 2: Sensor Configuration ---
#define REG_GYRO_SMPLRT_DIV     0x00    // Gyro Sample Rate Divider: ODR = 1125 / (1 + DIV)
#define REG_GYRO_CONFIG_1       0x01    // Gyro DLPF, Full Scale Selection, Filter Enable
#define REG_GYRO_CONFIG_2       0x02    // Gyro Averaging filter

#define REG_ACCEL_SMPLRT_DIV_1  0x10    // Accel Sample Rate Div MSB
#define REG_ACCEL_SMPLRT_DIV_2  0x11    // Accel Sample Rate Div LSB
#define REG_ACCEL_CONFIG        0x14    // Accel DLPF, Full Scale Selection, Filter Enable
#define REG_ACCEL_CONFIG_2      0x15    // Accel Decimation filter

// --- USER BANK 3: Auxiliary I2C Master Control ---
#define REG_I2C_MST_ODR_CONFIG  0x00
#define REG_I2C_MST_CTRL        0x01
#define REG_I2C_SLV0_ADDR       0x03
#define REG_I2C_SLV0_REG        0x04
#define REG_I2C_SLV0_CTRL       0x05
#define REG_I2C_SLV0_DO         0x06

// =============================================================================
// BITFIELD ENCODING VALUES (FROZEN BASELINE)
// =============================================================================

// PWR_MGMT_1 (Bank 0, 0x06)
// Bit 6: SLEEP = 0 (Wake up)
// Bit 5: LP_EN = 0 (Continuous high performance mode)
// Bits [2:0]: CLKSEL = 001 (Auto-select best clock PLL / 20MHz internal)
#define VAL_PWR_MGMT_1_WAKE     0x01

// GYRO_CONFIG_1 (Bank 2, 0x01)
// Bits [7:6]: Reserved = 00
// Bits [5:3]: GYRO_DLPFCFG = 011 (3dB Bandwidth 51.2 Hz, NBW 73.3 Hz per DS-000189 Table 16; no latency figure published)
// Bits [2:1]: GYRO_FS_SEL = 01 (+/- 500 dps full scale range, 65.5 LSB/dps)
// Bit 0:      GYRO_FCHOICE = 1 (Enable DLPF)
// Total = 0b00011011 = 0x1B
#define VAL_GYRO_CONFIG_1_DEFAULT 0x1B

// ACCEL_CONFIG (Bank 2, 0x14)
// Bits [7:6]: Reserved = 00
// Bits [5:3]: ACCEL_DLPFCFG = 011 (3dB Bandwidth 50.4 Hz, NBW 68.8 Hz per TDK DS-000189 Table 18; no latency figure published)
//             Note: ACCEL_DLPFCFG = 010 corresponds to 111.4 Hz, NOT 50.4 Hz.
// Bits [2:1]: ACCEL_FS_SEL = 01 (+/- 4g full scale range, 8192 LSB/g)
// Bit 0:      ACCEL_FCHOICE = 1 (Enable DLPF)
// Total = 0b00011011 = 0x1B
#define VAL_ACCEL_CONFIG_DEFAULT 0x1B

// GYRO_SMPLRT_DIV (Bank 2, 0x00)
// ODR = 1125 / (1 + 10) = 102.27 Hz (~100 Hz)
#define VAL_GYRO_SMPLRT_DIV_100HZ 10

// ACCEL_SMPLRT_DIV (Bank 2, 0x10 & 0x11)
// 12-bit divider: ODR = 1125 / (1 + ACCEL_SMPLRT_DIV)
// Synchronized to Gyro ODR (~102.27 Hz) with DIV = 10 (0x000A)
#define VAL_ACCEL_SMPLRT_DIV_1_100HZ 0x00
#define VAL_ACCEL_SMPLRT_DIV_2_100HZ 0x0A
#define VAL_ACCEL_SMPLRT_DIV_100HZ   10

// Sensitivity scale factors
#define ICM20948_GYRO_SCALE_500DPS   65.5f       // LSB per degree/second
#define ICM20948_ACCEL_SCALE_4G      8192.0f     // LSB per g

#endif // ICM20948_REGISTERS_H
