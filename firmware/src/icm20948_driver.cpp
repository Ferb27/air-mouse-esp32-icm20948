#include "icm20948_driver.h"
#include "pin_definitions.h"

#ifdef ARDUINO
#include <Arduino.h>
#include <Wire.h>
#else
#include <stdio.h>
#include <string.h>
// Mock environment for host testing
static uint8_t s_mock_regs[4][256];
static uint8_t s_mock_current_bank = 0;
static void delay(uint32_t ms) { (void)ms; }
#endif

static uint8_t s_current_bank = 0xFF; // Uninitialized
static uint32_t s_bus_recoveries = 0;
static icm20948_diag_t s_diag = {0, 0, 0, 0, 0, 0, 0, false};

void imu_selectBank(uint8_t bank) {
    if (s_current_bank == bank) {
        return; // Avoid unnecessary bus traffic
    }

#ifdef ARDUINO
    Wire.beginTransmission(ICM20948_I2C_ADDR);
    Wire.write(REG_BANK_SEL);
    Wire.write((bank & 0x03) << 4);
    Wire.endTransmission();
#else
    s_mock_current_bank = bank & 0x03;
#endif

    s_current_bank = bank & 0x03;
}

bool imu_writeReg(uint8_t bank, uint8_t reg, uint8_t val) {
    imu_selectBank(bank);

#ifdef ARDUINO
    Wire.beginTransmission(ICM20948_I2C_ADDR);
    Wire.write(reg);
    Wire.write(val);
    uint8_t err = Wire.endTransmission();
    return (err == 0);
#else
    s_mock_regs[s_mock_current_bank][reg] = val;
    return true;
#endif
}

uint8_t imu_readReg(uint8_t bank, uint8_t reg) {
    imu_selectBank(bank);

#ifdef ARDUINO
    Wire.beginTransmission(ICM20948_I2C_ADDR);
    Wire.write(reg);
    Wire.endTransmission(false); // Repeated START

    uint8_t count = Wire.requestFrom((uint8_t)ICM20948_I2C_ADDR, (size_t)1);
    if (count == 1) {
        return Wire.read();
    }
    return 0x00;
#else
    return s_mock_regs[s_mock_current_bank][reg];
#endif
}

bool imu_readBurst(uint8_t bank, uint8_t reg, uint8_t* buffer, size_t length) {
    if (!buffer || length == 0) return false;
    imu_selectBank(bank);

#ifdef ARDUINO
    Wire.beginTransmission(ICM20948_I2C_ADDR);
    Wire.write(reg);
    uint8_t err = Wire.endTransmission(false); // Repeated START
    if (err != 0) return false;

    size_t received = Wire.requestFrom((uint8_t)ICM20948_I2C_ADDR, length);
    if (received != length) return false;

    for (size_t i = 0; i < length; ++i) {
        buffer[i] = Wire.read();
    }
    return true;
#else
    for (size_t i = 0; i < length; ++i) {
        buffer[i] = s_mock_regs[s_mock_current_bank][(reg + i) & 0xFF];
    }
    return true;
#endif
}

bool imu_checkWhoAmI(uint8_t* whoami_val) {
#ifndef ARDUINO
    s_mock_regs[0][REG_WHO_AM_I] = VAL_WHO_AM_I_EXPECTED;
#endif
    uint8_t id = imu_readReg(0, REG_WHO_AM_I);
    if (whoami_val) *whoami_val = id;
    return (id == VAL_WHO_AM_I_EXPECTED);
}

uint32_t imu_getBusRecoveries(void) {
    return s_bus_recoveries;
}

bool imu_busRecover(void) {
    s_bus_recoveries++;
#ifdef ARDUINO
    Wire.end();                                          // release the I2C peripheral and the pins
    pinMode(PIN_I2C_SDA, INPUT_PULLUP);
    pinMode(PIN_I2C_SCL, INPUT_PULLUP);
    delayMicroseconds(10);
    // A slave that lost its place in a byte keeps SDA low until it has seen enough clock pulses: give it up to 9.
    for (int i = 0; i < 9 && digitalRead(PIN_I2C_SDA) == LOW; ++i) {
        pinMode(PIN_I2C_SCL, OUTPUT);
        digitalWrite(PIN_I2C_SCL, LOW);
        delayMicroseconds(5);
        pinMode(PIN_I2C_SCL, INPUT_PULLUP);              // released: the pull-up raises it (open-drain style)
        delayMicroseconds(5);
    }
    // STOP condition: SDA goes from low to high while SCL is high
    pinMode(PIN_I2C_SDA, OUTPUT);
    digitalWrite(PIN_I2C_SDA, LOW);
    delayMicroseconds(5);
    pinMode(PIN_I2C_SCL, INPUT_PULLUP);
    delayMicroseconds(5);
    pinMode(PIN_I2C_SDA, INPUT_PULLUP);
    delayMicroseconds(5);
    return digitalRead(PIN_I2C_SDA) == HIGH && digitalRead(PIN_I2C_SCL) == HIGH;
#else
    return true;
#endif
}

bool imu_init(void) {
    s_current_bank = 0xFF;
    memset(&s_diag, 0, sizeof(s_diag));

#ifdef ARDUINO
    Wire.end();                                          // a second Wire.begin() alone does NOT re-initialise the peripheral
    Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL, 400000);        // 400 kHz Fast-Mode
    Wire.setTimeOut(10);                                 // ms; a 12-byte read takes ~0.5 ms, the default 50 ms would stall the 10 ms loop
    delay(10);
#endif

    // Step 1: Verify Chip Identity
    uint8_t whoami = 0;
    if (!imu_checkWhoAmI(&whoami)) {
        s_diag.who_am_i = whoami;
        s_diag.init_success = false;
        return false;
    }
    s_diag.who_am_i = whoami;

    // Step 2: Wake up device and select Auto-PLL clock
    // Bank 0, REG_PWR_MGMT_1 (0x06) = 0x01
    if (!imu_writeReg(0, REG_PWR_MGMT_1, VAL_PWR_MGMT_1_WAKE)) {
        return false;
    }
    delay(10);

    // Readback verification for PWR_MGMT_1
    s_diag.pwr_mgmt_1 = imu_readReg(0, REG_PWR_MGMT_1);

    // Step 3: Configure Gyroscope
    // Bank 2, REG_GYRO_SMPLRT_DIV (0x00) = 10 (~100 Hz ODR)
    imu_writeReg(2, REG_GYRO_SMPLRT_DIV, VAL_GYRO_SMPLRT_DIV_100HZ);
    s_diag.gyro_smplrt_div = imu_readReg(2, REG_GYRO_SMPLRT_DIV);

    // Bank 2, REG_GYRO_CONFIG_1 (0x01) = 0x1B (DLPF=51.2Hz, FS=+/-500dps, FCHOICE=1)
    imu_writeReg(2, REG_GYRO_CONFIG_1, VAL_GYRO_CONFIG_1_DEFAULT);
    s_diag.gyro_config_1 = imu_readReg(2, REG_GYRO_CONFIG_1);

    // Step 4: Configure Accelerometer ODR and Filter
    // Bank 2, REG_ACCEL_SMPLRT_DIV_1/2 (0x10, 0x11) = 10 (~102.27 Hz ODR, matching Gyro)
    imu_writeReg(2, REG_ACCEL_SMPLRT_DIV_1, VAL_ACCEL_SMPLRT_DIV_1_100HZ);
    imu_writeReg(2, REG_ACCEL_SMPLRT_DIV_2, VAL_ACCEL_SMPLRT_DIV_2_100HZ);
    s_diag.accel_smplrt_div_1 = imu_readReg(2, REG_ACCEL_SMPLRT_DIV_1);
    s_diag.accel_smplrt_div_2 = imu_readReg(2, REG_ACCEL_SMPLRT_DIV_2);

    // Bank 2, REG_ACCEL_CONFIG (0x14) = 0x1B (DLPF=50.4Hz [011], FS=+/-4g [01], FCHOICE=1)
    imu_writeReg(2, REG_ACCEL_CONFIG, VAL_ACCEL_CONFIG_DEFAULT);
    s_diag.accel_config = imu_readReg(2, REG_ACCEL_CONFIG);

    // Return to Bank 0 for continuous sensor reading
    imu_selectBank(0);

    s_diag.init_success = (s_diag.who_am_i == VAL_WHO_AM_I_EXPECTED) &&
                          (s_diag.pwr_mgmt_1 == VAL_PWR_MGMT_1_WAKE) &&
                          (s_diag.gyro_config_1 == VAL_GYRO_CONFIG_1_DEFAULT) &&
                          (s_diag.accel_config == VAL_ACCEL_CONFIG_DEFAULT) &&
                          (s_diag.gyro_smplrt_div == VAL_GYRO_SMPLRT_DIV_100HZ) &&
                          (s_diag.accel_smplrt_div_1 == VAL_ACCEL_SMPLRT_DIV_1_100HZ) &&
                          (s_diag.accel_smplrt_div_2 == VAL_ACCEL_SMPLRT_DIV_2_100HZ);

    return s_diag.init_success;
}

bool imu_readRawGyro(int16_t* gx, int16_t* gy, int16_t* gz) {
    uint8_t raw[6];
    if (!imu_readBurst(0, REG_GYRO_XOUT_H, raw, 6)) {
        return false;
    }
    if (gx) *gx = (int16_t)(((uint16_t)raw[0] << 8) | raw[1]);
    if (gy) *gy = (int16_t)(((uint16_t)raw[2] << 8) | raw[3]);
    if (gz) *gz = (int16_t)(((uint16_t)raw[4] << 8) | raw[5]);
    return true;
}

bool imu_readRawAccel(int16_t* ax, int16_t* ay, int16_t* az) {
    uint8_t raw[6];
    if (!imu_readBurst(0, REG_ACCEL_XOUT_H, raw, 6)) {
        return false;
    }
    if (ax) *ax = (int16_t)(((uint16_t)raw[0] << 8) | raw[1]);
    if (ay) *ay = (int16_t)(((uint16_t)raw[2] << 8) | raw[3]);
    if (az) *az = (int16_t)(((uint16_t)raw[4] << 8) | raw[5]);
    return true;
}

bool imu_readData(imu_data_t* data) {
    if (!data) return false;

    // Read combined 12 bytes of Accel and Gyro consecutively
    // Bank 0: Accel 0x2D-0x32 (6 bytes), Gyro 0x33-0x38 (6 bytes)
    uint8_t raw[12];
    if (!imu_readBurst(0, REG_ACCEL_XOUT_H, raw, 12)) {
        return false;
    }

    int16_t raw_ax = (int16_t)(((uint16_t)raw[0] << 8) | raw[1]);
    int16_t raw_ay = (int16_t)(((uint16_t)raw[2] << 8) | raw[3]);
    int16_t raw_az = (int16_t)(((uint16_t)raw[4] << 8) | raw[5]);

    int16_t raw_gx = (int16_t)(((uint16_t)raw[6] << 8) | raw[7]);
    int16_t raw_gy = (int16_t)(((uint16_t)raw[8] << 8) | raw[9]);
    int16_t raw_gz = (int16_t)(((uint16_t)raw[10] << 8) | raw[11]);

    // Convert raw 16-bit to physical units
    data->ax = (float)raw_ax / ICM20948_ACCEL_SCALE_4G;
    data->ay = (float)raw_ay / ICM20948_ACCEL_SCALE_4G;
    data->az = (float)raw_az / ICM20948_ACCEL_SCALE_4G;

    data->gx = (float)raw_gx / ICM20948_GYRO_SCALE_500DPS;
    data->gy = (float)raw_gy / ICM20948_GYRO_SCALE_500DPS;
    data->gz = (float)raw_gz / ICM20948_GYRO_SCALE_500DPS;

    return true;
}

icm20948_diag_t imu_getDiagnostics(void) {
    return s_diag;
}
