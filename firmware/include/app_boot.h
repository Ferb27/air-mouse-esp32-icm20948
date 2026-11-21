#ifndef APP_BOOT_H
#define APP_BOOT_H

// Everything that runs once at power-up, in this order:
//   serial + banner -> GPIO (buttons, LED) -> ICM-20948 init + register read-back (blinks forever if it fails) ->
//   motion pipeline -> gyro bias calibration (validated, up to 5 attempts) -> BLE advertising -> start the 100 Hz loop.
void app_boot(void);

#endif // APP_BOOT_H
