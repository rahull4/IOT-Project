import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Conversions between binary data and various encodings
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
from machine import Pin       # Define pin
import dht


tempSensor = dht.DHT11(machine.Pin(27))
internalLED = machine.Pin('LED', machine.Pin.OUT)

# adafruit configuration
AIO_SERVER              = "io.adafruit.com"
AIO_PORT                = 1883
AIO_USER                = "rahull"       # Your AIO username
AIO_KEY                 = "aio_tCyr85xg0qpLNjfUllx9fInQchiJ"       # Your AIO key
AIO_CLIENT_ID           = ubinascii.hexlify(machine.unique_id())
AIO_HUMIDITY_FEED       = "rahull/feeds/humidity"       # username/feeds/feed_name
AIO_TEMPERATURE_FEED    = "rahull/feeds/temperature"       # username/feeds/feed_name


last_publish = time.time()
publish_interval = 30


def reset():
    time.sleep(5)
    machine.reset()

def get_temperature_reading():
    return tempSensor.temperature()

def get_humidity_reading():
    return tempSensor.humidity()

def main():
    '''Countinuosly retrieves and publishes sensor data'''

    # Create instance of client and connect
    client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY, keepalive=60)
    client.connect()

    while True:
        global last_publish
        
        if (time.time() - last_publish) >= publish_interval:
            internalLED.toggle()

            # Get sensor readings
            tempSensor.measure()
            temperature = get_temperature_reading()
            humidity = get_humidity_reading()

            # Send data to adafruit
            client.publish(AIO_HUMIDITY_FEED, str(humidity))
            client.publish(AIO_TEMPERATURE_FEED, str(temperature))

            internalLED.toggle()
            last_publish = time.time()
        time.sleep(10)

if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            reset()
