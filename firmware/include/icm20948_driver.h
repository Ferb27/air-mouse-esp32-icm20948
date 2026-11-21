#ifndef ICM20948_DRIVER_H
#define ICM20948_DRIVER_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include "icm20948_registers.h"

#ifdef __cplusplus
extern "C" {
#endif

// Diagnostics record structure
typedef struct {
    uint8_t who_am_i;
    uint8_t pwr_mgmt_1;
    uint8_t gyro_config_1;
    uint8_t accel_config;
    uint8_t gyro_smplrt_div;
    uint8_t accel_smplrt_div_1;
    uint8_t accel_smplrt_div_2;
    bool init_success;
} icm20948_diag_t;

// Sensor physical measurement data
typedef struct {
    float gx; // Degree per second (dps)
    float gy;
    float gz;
    float ax; // Acceleration in g (1g = 9.80665 m/s^2)
    float ay;
    float az;
} imu_data_t;

// Function prototypes
bool imu_init(void);
// Free an I2C bus a slave is holding (clock SCL up to 9 times until SDA is released, then send a STOP) and leave the
// pins ready for Wire.begin(). Returns true when both lines read high afterwards. Host builds: always true.
bool imu_busRecover(void);
uint32_t imu_getBusRecoveries(void);   // number of imu_busRecover() calls since boot
void imu_selectBank(uint8_t bank);
bool imu_writeReg(uint8_t bank, uint8_t reg, uint8_t val);
uint8_t imu_readReg(uint8_t bank, uint8_t reg);
bool imu_readBurst(uint8_t bank, uint8_t reg, uint8_t* buffer, size_t length);

bool imu_checkWhoAmI(uint8_t* whoami_val);
bool imu_readRawGyro(int16_t* gx, int16_t* gy, int16_t* gz);
bool imu_readRawAccel(int16_t* ax, int16_t* ay, int16_t* az);
bool imu_readData(imu_data_t* data);

icm20948_diag_t imu_getDiagnostics(void);

#ifdef __cplusplus
}
#endif

#endif // ICM20948_DRIVER_H
