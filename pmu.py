#Date: 2018/08/10
#Editor: Jim Chen
#Version: 1.0.2

import random
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO #GPIO pin library
import os
import sys
import time
import psutil
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from synchrophasor.frame import ConfigFrame2
from synchrophasor.pmu import Pmu

time.sleep(5)

"""
After 5 seconds, pmu will run below code
"""

# TCP Modbus configuration:
client = ModbusClient('192.168.4.194', 502)
client.connect()
# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD) #Set GPIO mode    
    GPIO.setup(11, GPIO.IN) #Set Pin 11 as an Input Pin
    GPIO.setup(13, GPIO.IN) #Set Pin 13 as an Input Pin
    GPIO.setup(29, GPIO.IN) #Set Pin 29 as an Input Pin
    GPIO.setup(31, GPIO.IN) #Set Pin 31 as an Input Pin
    
    pmu = Pmu(ip="192.168.4.194", port=4712) #Device IP parameter 
    
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
    pmu.set_header("This is EDIT PMU")

    pmu.run()

    while True:
           if pmu.clients:
               
               time.sleep(0.02)
               AI_1 = mcp.read_adc(0)
               AI_2 = mcp.read_adc(1)
               AI_3 = mcp.read_adc(2)
               AI_4 = mcp.read_adc(3)
               AI_5 = mcp.read_adc(4)
               AI_6 = mcp.read_adc(5)
               AI_7 = mcp.read_adc(6)
               AI_8 = mcp.read_adc(7)
               Voltage_AI_1 = AI_1 * 3.3 / 1024
               Voltage_AI_2 = AI_2 * 3.3 / 1024
               Voltage_AI_3 = AI_3 * 3.3 / 1024
               Voltage_AI_4 = AI_4 * 3.3 / 1024
               Voltage_AI_5 = AI_5 * 3.3 / 1024
               Voltage_AI_6 = AI_6 * 3.3 / 1024
               Voltage_AI_7 = AI_7 * 3.3 / 1024
               Voltage_AI_8 = AI_8 * 3.3 / 1024               
               DI_1 = GPIO.input(11) #Read Input Pin 11 as a Digital In
               DI_2 = GPIO.input(13) #Read Input Pin 13 as a Digital In
               DI_3 = GPIO.input(29) #Read Input Pin 29 as a Digital In
               DI_4 = GPIO.input(31) #Read Input Pin 31 as a Digital In
               
               #raspberry pi system info
               hour = time.localtime().tm_hour
               minute = time.localtime().tm_min
               seconds = time.localtime().tm_sec
               system_time = hour * 10000 + minute *100 + seconds               
               file = open("/sys/class/thermal/thermal_zone0/temp")
               system_temp = round(float(file.read()) / 100)
               file.close()
               
               
               cpu_usage = round(psutil.cpu_percent(interval=1, percpu=False) * 10)
               virtual_memory_usage = round(psutil.virtual_memory().percent * 10)
               swap_memory_usage = round(psutil.swap_memory().percent * 10)
               disk_usage = round(psutil.disk_usage('/').percent * 10)
               
               file = open("/home/pi/dht22_temperature")
               try:
                   dht22_temp = round(float(file.read()) * 10)
               except ValueError:
                   dht22_temp = 0 
               file.close()
               file = open("/home/pi/dht22_humidity")
               try:
                   dht22_humi = round(float(file.read()) * 10)
               except ValueError:
                   dht22_humi = 0
               file.close()
               
               pmu.send_data(phasors=[(AI_1, 0),
                            (AI_2, 0),
                            (AI_3, 0), (AI_4, 0)],
                          analog=[AI_1, AI_2, AI_3, system_time, system_temp],
                          digital=[DI_1, DI_2, DI_3, DI_4])
               
               client.connect()           
               rr = client.read_input_registers(0, 8, unit=1)
               #rq = client.write_registers(0, [AI_1, AI_2, AI_3, AI_4, AI_5, AI_6, AI_7, AI_8], unit=1)
               rq = client.write_registers(0, AI_1, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(1, AI_2, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(2, AI_3, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(3, AI_4, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(4, AI_5, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(5, AI_6, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(6, AI_7, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(7, AI_8, unit=1)               
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               
               rr = client.read_holding_registers(0, 8, unit=1)
               #rq = client.write_registers(10, [system_temp, cpu_usage, disk_usage, virtual_memory_usage, swap_memory_usage, dht22_temp, dht22_humi, 1], unit=1)
               rq = client.write_registers(10, system_temp, unit=1)
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(11, cpu_usage, unit=1)
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(12, disk_usage, unit=1)
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(13, virtual_memory_usage, unit=1)
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(14, swap_memory_usage, unit=1)
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(15, dht22_temp, unit=1)
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               rq = client.write_registers(16, dht22_humi, unit=1)
               assert(rq.function_code < 0x80)#if FC>0x80 --> Error
               
               rr = client.read_holding_registers(0, 7, unit=1)
               
               rr = client.read_discrete_inputs(0, 4, unit=1)
               rq = client.write_coils(0, [DI_1, DI_2, DI_3, DI_4], unit=1)
               rr = client.read_coils(0, 4, unit=1)
               client.close()
               
     
    pmu.join()
