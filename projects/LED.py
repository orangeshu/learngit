import RPi.GPIO
import time

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(12,RPi.GPIO.OUT)

for i in range(0, 100):
    RPi.GPIO.output(12, True)
    time.sleep(0.2)
    RPi.GPIO.output(12, False)
    time.sleep(0.2)
 
RPi.GPIO.cleanup()



 
     

