import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)

p=GPIO.PWM(16,100)
p.start(2.7)

while 1:
		a = 1;
		
p.stop()
GPIO.cleanup()

		
