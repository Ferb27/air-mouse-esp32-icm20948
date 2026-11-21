#ifndef PIN_DEFINITIONS_H
#define PIN_DEFINITIONS_H

// =============================================================================
// HARDWARE PIN ASSIGNMENTS — ESP32 CLASSIC DEVKIT 38-PIN
// Aligned 100% with SCHEMATIC_NETLIST.md and docs/BOM_V1.md
// =============================================================================

// I2C Hardware Bus (I2C0 Controller - Direct 3.3V to WCMCU-20948)
#define PIN_I2C_SDA         21  // ESP32 GPIO21 -> WCMCU-20948 SDA (Direct 3.3V)
#define PIN_I2C_SCL         22  // ESP32 GPIO22 -> WCMCU-20948 SCL (Direct 3.3V)

// User Push Buttons (Active-Low with internal pull-up)
#define PIN_BTN_LEFT        25  // SW2: Left Click (nối GND khi nhấn)
#define PIN_BTN_RIGHT       26  // SW3: Right Click (nối GND khi nhấn)
#define PIN_BTN_MODE        27  // SW4: Mode / Clutch / Recenter / Gesture Arm

// Status Indicator LED (Push-Pull, Active-High)
#define PIN_LED_STATUS      32  // ESP32 GPIO32 -> Trở 1kΩ -> Anode LED D1 (Green)

// Battery Sense ADC (SAR ADC1 Channel 6)
#define PIN_BAT_SENSE       34  // GPIO34 (Input-Only) -> Cầu phân áp 100k/100k từ V_SYS

// I2C Address of ICM-20948 (AD0 connected to GND)
#define ICM20948_I2C_ADDR   0x68

#endif // PIN_DEFINITIONS_H
