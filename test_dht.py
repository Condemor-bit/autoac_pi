import Adafruit_DHT

sensor = Adafruit_DHT.DHT22 #specify  DHT22 sensor

pin = 2  # were you connected the sensor

humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)

print('The temperature is:', temperatura)

print('The humidity is:', humedad)
