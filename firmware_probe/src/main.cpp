// =============================================================================
// Air Mouse Hardware Bring-Up Probe (Standalone Test)
// Target: ESP32 Classic DevKit 38-Pin + WCMCU-20948 (Direct 3.3V)
// Pins: SDA = GPIO21, SCL = GPIO22
// =============================================================================

#include <Arduino.h>
#include <Wire.h>

#define I2C_SDA_PIN 21
#define I2C_SCL_PIN 22
#define TARGET_ADDR_PRIMARY 0x68
#define TARGET_ADDR_SECONDARY 0x69

void scanI2C(uint32_t speed_hz) {
    Serial.printf("\n>>> STARTING I2C SCAN @ %u Hz (SDA=%d, SCL=%d) <<<\n", speed_hz, I2C_SDA_PIN, I2C_SCL_PIN);
    Wire.setClock(speed_hz);
    
    int devices_found = 0;
    for (uint8_t addr = 0x08; addr <= 0x77; addr++) {
        Wire.beginTransmission(addr);
        uint8_t err = Wire.endTransmission();
        
        if (err == 0) {
            Serial.printf("  [I2C ACK] Found device at address: 0x%02X\n", addr);
            devices_found++;
        } else if (err == 4) {
            Serial.printf("  [I2C ERROR] Unknown error at address: 0x%02X\n", addr);
        }
    }
    
    if (devices_found == 0) {
        Serial.println("  [I2C SCAN RESULT] NO I2C devices found on bus!");
    } else {
        Serial.printf("  [I2C SCAN RESULT] Found %d device(s) total.\n", devices_found);
    }
}

uint8_t readRegister(uint8_t devAddr, uint8_t regAddr, uint8_t *valOut) {
    Wire.beginTransmission(devAddr);
    Wire.write(regAddr);
    uint8_t err = Wire.endTransmission(false); // Repeated start
    if (err != 0) {
        return err; // 1: data too long, 2: NACK on addr, 3: NACK on data, 4: other
    }
    
    uint8_t count = Wire.requestFrom((uint8_t)devAddr, (uint8_t)1);
    if (count != 1) {
        return 5; // Read count mismatch
    }
    *valOut = Wire.read();
    return 0; // Success
}

uint8_t writeRegister(uint8_t devAddr, uint8_t regAddr, uint8_t val) {
    Wire.beginTransmission(devAddr);
    Wire.write(regAddr);
    Wire.write(val);
    return Wire.endTransmission();
}

void setup() {
    Serial.begin(115200);
    delay(2000);
    
    Serial.println("\n=======================================================");
    Serial.println("   ESP32 & WCMCU-20948 HARDWARE BRING-UP PROBE");
    Serial.println("   Direct 3.3V Connection Verification");
    Serial.println("=======================================================");
    
    // Step 1: Initialize I2C at 100 kHz
    Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN, 100000);
    delay(100);
    
    // Step 2: Scan bus at 100 kHz
    scanI2C(100000);
    
    // Step 3: Check targets 0x68 and 0x69
    uint8_t activeAddr = 0;
    Wire.beginTransmission(TARGET_ADDR_PRIMARY);
    if (Wire.endTransmission() == 0) {
        activeAddr = TARGET_ADDR_PRIMARY;
        Serial.printf("\n[TARGET DETECTED] Primary address 0x%02X is responding with ACK!\n", activeAddr);
    } else {
        Wire.beginTransmission(TARGET_ADDR_SECONDARY);
        if (Wire.endTransmission() == 0) {
            activeAddr = TARGET_ADDR_SECONDARY;
            Serial.printf("\n[TARGET DETECTED] Secondary address 0x%02X is responding with ACK!\n", activeAddr);
        } else {
            Serial.println("\n[ERROR] Neither 0x68 nor 0x69 responded to I2C ping!");
        }
    }
    
    if (activeAddr != 0) {
        // Step 4: Select Bank 0
        Serial.printf("\nSelecting User Bank 0 on device 0x%02X via REG_BANK_SEL (0x7F = 0x00)...\n", activeAddr);
        uint8_t b_err = writeRegister(activeAddr, 0x7F, 0x00);
        Serial.printf("  Bank select result: Wire.endTransmission() returned %d (%s)\n", 
                      b_err, (b_err == 0 ? "SUCCESS" : "FAIL"));
        
        // Step 5: Read WHO_AM_I (0x00)
        uint8_t whoami = 0;
        uint8_t r_err = readRegister(activeAddr, 0x00, &whoami);
        Serial.printf("\n--- WHO_AM_I VERIFICATION ---\n");
        Serial.printf("  Wire status code: %d\n", r_err);
        Serial.printf("  WHO_AM_I Raw Byte: 0x%02X\n", whoami);
        Serial.printf("  Expected: 0xEA\n");
        
        if (r_err == 0 && whoami == 0xEA) {
            Serial.println("  >>> WHO_AM_I MATCH: 0xEA (ICM-20948 HARDWARE CONFIRMED!) <<<");
            
            // Step 6: Wake up chip (PWR_MGMT_1 = 0x01)
            Serial.println("\nWaking up chip via PWR_MGMT_1 (0x06 = 0x01)...");
            writeRegister(activeAddr, 0x06, 0x01);
            delay(50);
            
            // Step 7: Stability test at 100 kHz (100 reads of WHO_AM_I + burst)
            Serial.println("\nRunning 100-cycle Stability Test @ 100 kHz...");
            int nack_100k = 0;
            for (int i = 0; i < 100; i++) {
                uint8_t test_val = 0;
                if (readRegister(activeAddr, 0x00, &test_val) != 0 || test_val != 0xEA) {
                    nack_100k++;
                }
                delay(2);
            }
            Serial.printf("  100 kHz Result: %d/100 successful (NACK/Errors: %d)\n", 100 - nack_100k, nack_100k);
            
            // Step 8: Stability test at 400 kHz
            Serial.println("\nSwitching to Fast Mode @ 400 kHz...");
            Wire.setClock(400000);
            delay(50);
            
            int nack_400k = 0;
            for (int i = 0; i < 100; i++) {
                uint8_t test_val = 0;
                if (readRegister(activeAddr, 0x00, &test_val) != 0 || test_val != 0xEA) {
                    nack_400k++;
                }
                delay(2);
            }
            Serial.printf("  400 kHz Result: %d/100 successful (NACK/Errors: %d)\n", 100 - nack_400k, nack_400k);
            
            if (nack_400k == 0) {
                Serial.println("  >>> 400 kHz FAST MODE IS 100% STABLE! <<<");
            } else if (nack_100k == 0) {
                Serial.println("  >>> WARNING: 400 kHz had errors, but 100 kHz is 100% STABLE! Recommend 100 kHz. <<<");
            } else {
                Serial.println("  >>> WARNING: Both 100 kHz and 400 kHz had bus errors! Check pull-ups. <<<");
            }
        } else {
            Serial.printf("  >>> WHO_AM_I MISMATCH! Got 0x%02X, expected 0xEA <<<\n", whoami);
        }
    }
    
    Serial.println("\n=======================================================");
    Serial.println("Entering continuous live monitoring loop...");
    Serial.println("Columns: [Cycle] WHO_AM_I | Accel (X, Y, Z) | Gyro (X, Y, Z) | Bus Status");
    Serial.println("=======================================================\n");
}

uint32_t cycle_count = 0;

void loop() {
    cycle_count++;
    uint8_t whoami = 0;
    uint8_t err = readRegister(TARGET_ADDR_PRIMARY, 0x00, &whoami);
    
    if (err == 0 && whoami == 0xEA) {
        // Read burst 12 bytes (ACCEL: 0x2D..0x32, GYRO: 0x33..0x38)
        Wire.beginTransmission(TARGET_ADDR_PRIMARY);
        Wire.write(0x2D);
        Wire.endTransmission(false);
        
        uint8_t buf[12];
        uint8_t count = Wire.requestFrom((uint8_t)TARGET_ADDR_PRIMARY, (uint8_t)12);
        if (count == 12) {
            for (int i = 0; i < 12; i++) buf[i] = Wire.read();
            
            int16_t ax = (int16_t)(((uint16_t)buf[0] << 8) | buf[1]);
            int16_t ay = (int16_t)(((uint16_t)buf[2] << 8) | buf[3]);
            int16_t az = (int16_t)(((uint16_t)buf[4] << 8) | buf[5]);
            
            int16_t gx = (int16_t)(((uint16_t)buf[6] << 8) | buf[7]);
            int16_t gy = (int16_t)(((uint16_t)buf[8] << 8) | buf[9]);
            int16_t gz = (int16_t)(((uint16_t)buf[10] << 8) | buf[11]);
            
            Serial.printf("[%05u] WHO=0x%02X | A:(%+6d, %+6d, %+6d) | G:(%+6d, %+6d, %+6d) | OK\n",
                          cycle_count, whoami, ax, ay, az, gx, gy, gz);
        } else {
            Serial.printf("[%05u] WHO=0x%02X | Burst read failed (count=%d)\n", cycle_count, whoami, count);
        }
    } else {
        Serial.printf("[%05u] Read error (code=%d, whoami=0x%02X)\n", cycle_count, err, whoami);
    }
    
    delay(200);
}
