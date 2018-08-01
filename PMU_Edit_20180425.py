#Date: 2018/04/25
#Editor: Jim Chen
#Version: 1.0.0

import random
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO #GPIO pin library
import os
import time
from synchrophasor.frame import ConfigFrame2
from synchrophasor.pmu import Pmu


"""
PMU will listen on ip:port for incoming connections.
After request to start sending measurements - random & dht22 data
values for phasors will be sent.
"""
# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD) #Set GPIO mode    
    GPIO.setup(11, GPIO.IN) #Set Pin 11 as an Input Pin
    GPIO.setup(13, GPIO.IN) #set Pin 13


    pmu = Pmu(ip="192.168.1.6", port=4712) #Device 
    pmu.logger.setLevel("DEBUG")

    cfg = ConfigFrame2(1,  # PMU_ID
                       1000000,  # TIME_BASE
                       1,  # Number of PMUs included in data frame
                       "Edit Station",  # Station name
                       33,  # Data-stream ID(s)
                       (True, True, True, True),  # Data format - POLAR; PH - REAL; AN - REAL; FREQ - REAL;
                       4,  # Number of phasors
                       5,  # Number of analog values
                       4,  # Number of digital status words
                       ["VA", "VB", "VC", "VD", "ANALOG1", "ANALOG2", "ANALOG3", "ANALOG4", "ANALOG5", "BREAKER 01 STATUS",
                        "BREAKER 02 STATUS", "BREAKER 03 STATUS", "BREAKER 04 STATUS", "BREAKER 05 STATUS",
                        "BREAKER 06 STATUS", "BREAKER 07 STATUS", "BREAKER 08 STATUS", "BREAKER 09 STATUS",
                        "BREAKER 0A STATUS", "BREAKER 0B STATUS", "BREAKER 0C STATUS", "BREAKER 0D STATUS",
                        "BREAKER 0E STATUS", "BREAKER 0F STATUS", "BREAKER 0G STATUS", "BREAKER 11 STATUS",
                        "BREAKER 12 STATUS", "BREAKER 13 STATUS", "BREAKER 14 STATUS", "BREAKER 15 STATUS",
                        "BREAKER 16 STATUS", "BREAKER 17 STATUS", "BREAKER 18 STATUS", "BREAKER 19 STATUS",
                        "BREAKER 1A STATUS", "BREAKER 1B STATUS", "BREAKER 1C STATUS", "BREAKER 1D STATUS",
                        "BREAKER 1E STATUS", "BREAKER 1F STATUS", "BREAKER 1G STATUS", "BREAKER 21 STATUS",
                        "BREAKER 22 STATUS", "BREAKER 23 STATUS", "BREAKER 24 STATUS", "BREAKER 25 STATUS",
                        "BREAKER 26 STATUS", "BREAKER 27 STATUS", "BREAKER 28 STATUS", "BREAKER 29 STATUS",
                        "BREAKER 2A STATUS", "BREAKER 2B STATUS", "BREAKER 2C STATUS", "BREAKER 2D STATUS",
                        "BREAKER 2E STATUS", "BREAKER 2F STATUS", "BREAKER 2G STATUS", "BREAKER 31 STATUS",
                        "BREAKER 32 STATUS", "BREAKER 33 STATUS", "BREAKER 34 STATUS", "BREAKER 35 STATUS",
                        "BREAKER 36 STATUS", "BREAKER 37 STATUS", "BREAKER 38 STATUS", "BREAKER 39 STATUS",
                        "BREAKER 3A STATUS", "BREAKER 3B STATUS", "BREAKER 3C STATUS", "BREAKER 3D STATUS",
                        "BREAKER 3E STATUS", "BREAKER 3F STATUS", "BREAKER 3G STATUS"],  # Channel Names
                       [(0, "v"), (0, "v"),
                        (0, "v"), (0, "v")],  # Conversion factor for phasor channels - (float representation, not important)
                       [(1, "pow"), (1, "pow"), (1, "pow"), (1, "pow"), (1, "pow")],  # Conversion factor for analog channels
                       [(0x0000, 0xffff), (0x0000, 0xffff), (0x0000, 0xffff), (0x0000, 0xffff)],  # Mask words for digital status words
                       50,  # Nominal frequency
                       1,  # Configuration change count
                       60)  # Rate of phasor data transmission)

    pmu.set_configuration(cfg)
    pmu.set_header("This is EIDT PMU")

    pmu.run()

    while True:
            if pmu.clients:
               value_1 = mcp.read_adc(0)
               value_2 = mcp.read_adc(1)
               voltage_1 = value_1 * 3.3 / 1024
               voltage_2 = value_2 * 3.3 / 1024               
               DI = GPIO.input(11) #Set Input Pin 11 as a Digital In
               AI = GPIO.input(13) #Set Input Pin 13
               hour = time.localtime().tm_hour
               minute = time.localtime().tm_min
               seconds = time.localtime().tm_sec
               system_time = hour * 10000 + minute *100 + seconds
               time.sleep(0.02)
               file = open("/sys/class/thermal/thermal_zone0/temp")
               system_temp = float(file.read()) /1000
               file.close()
               pmu.send_data(phasors=[(value_1, 0),
                            (value_2, 0),
                            (DI, 0), (DI, 0)],
                          analog=[voltage_1, voltage_2, system_time, system_temp, AI],
                          digital=[DI, DI, DI, DI])
               print('*' * 57)
          
    pmu.join()
