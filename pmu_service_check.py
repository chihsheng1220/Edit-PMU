#Date: 2018/08/010
#Editor: Jim Chen
#Version: 1.0.1

import os
import subprocess
import lcd_i2c_driver
import sys
import time

time.sleep(3)

pmu_lcd = lcd_i2c_driver.lcd()


def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
        return exit_code == 0

if __name__ == "__main__":
    pmu_lcd.lcd_clear()

    while True:
        pmu_lcd.lcd_clear()
        if not is_service_running('pmu'):
            pmu_lcd.lcd_display_string_pos("pmu service is", 1, 0)
            pmu_lcd.lcd_display_string_pos("not running", 2, 0)
        if is_service_running('pmu'):
            pmu_lcd.lcd_display_string_pos("pmu service is", 1, 0)
            pmu_lcd.lcd_display_string_pos("running", 2, 0)
        time.sleep(10)
        pmu_lcd.lcd_clear()
        if not is_service_running('pmu_mbserver'):
            pmu_lcd.lcd_display_string_pos("pmu_mbserver is ", 1, 0)
            pmu_lcd.lcd_display_string_pos("not running", 2, 0)
        if is_service_running('pmu_mbserver'):
            pmu_lcd.lcd_display_string_pos("pmu_mbserver is ", 1, 0)
            pmu_lcd.lcd_display_string_pos("running", 2, 0)
        time.sleep(10)
            