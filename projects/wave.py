import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)

p=GPIO.PWM(16,100)
p.start(0)
try: 
	while 1:
		for dc in range(0,101):
		    p.ChangeDutyCycle(dc)
		    time.sleep(0.01)
		for dc in range(100,-1,-1):             
		    p.ChangeDutyCycle(dc)
		    time.sleep(0.01)
except KeyboardInterrupt:
	pass
p.stop()
GPIO.cleanup()
		
