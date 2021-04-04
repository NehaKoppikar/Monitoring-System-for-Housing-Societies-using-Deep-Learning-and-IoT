from smbus2 import SMBus
from mlx90614 import MLX90614
from gpiozero import LED
import time
import RPi.GPIO as GPIO

led_1=22
led_2=27
led_3=17


#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)
GPIO.setup(led_3, GPIO.OUT)

#set initial LED states
GPIO.output(led_1, 0)
GPIO.output(led_2, 0)
GPIO.output(led_3, 0)

#main loop
try:
    while 1:
        bus = SMBus(1)
        sensor = MLX90614(bus, address=0x5a)
        print("Ambient temperature: ", sensor.get_ambient())
        print("Object temperature: ", sensor.get_object_1())

        if sensor.get_object_1() < 37:	#change this value to adjust the 'too cold' threshold
                GPIO.output(led_1, 1)
                GPIO.output(led_2, 0)
                GPIO.output(led_3, 0)
    
        if sensor.get_object_1() > 37 and sensor.get_object_1() < 38:	#change these values to adjust the 'comfortable' range
                GPIO.output(led_1, 0)
                GPIO.output(led_2, 1)
                GPIO.output(led_3, 0)
    
        if sensor.get_object_1() > 38:	#change this value to adjust the 'too hot' threshold
                GPIO.output(led_1, 0)
                GPIO.output(led_2, 0)
                GPIO.output(led_3, 1)
    
        time.sleep(1)
        bus.close()

except KeyboardInterrupt:
    GPIO.cleanup()
    print ("Program Exited Cleanly")
        



