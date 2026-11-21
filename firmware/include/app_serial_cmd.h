#ifndef APP_SERIAL_CMD_H
#define APP_SERIAL_CMD_H

// Live tuning over the serial port (115200).
// Lines starting with '@' are the settings protocol for a PC tool (@GET, @SET k=v, @SAVE, @DEFAULTS, @CAL; see
// air_config.h); only "@SAVE" writes to flash. The one-character commands below change the running firmware only
// (reboot = back to the saved settings); "@GET" / "@SAVE" see their effect.
//   '+' / '-'  cursor gain x1.2 / /1.2     '?'  print the gain
//   'c'        recalibrate the gyro bias now (the board must rest still; a rejected window keeps the old bias)
//   'y' / 'Y'  quick-turn flick threshold -20 / +20 deg/s (lower = easier to trigger)
//   '<' / '>'  click-guard look-ahead -10 / +10 ms (0..100 ms)
void app_serial_poll(void);

#endif // APP_SERIAL_CMD_H
