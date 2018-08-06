import time
import Adafruit_DHT

time.sleep(3)
sensor =  Adafruit_DHT.DHT22
pin = 4

if __name__ == "__main__":

   while True:
       time.sleep(2)
       humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
       
        
       f = open('/home/pi/dht22_temperature', 'w+')
       f.write(str(temperature))
       f.close()
        
       f = open('/home/pi/dht22_humidity', 'w+')
       f.write(str(humidity))
       f.close()