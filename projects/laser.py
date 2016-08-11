from gpiozero import LightSensor, Buzzer
from time import sleep


ldr = LightSensor(4)
buzzer = Buzzer(17)   # alter if using a different pin

while True:
	sleep(0.1)
	print(ldr.value)
	if ldr.value<0.8: # adjust this to make the circuit more or less sensitive
		buzzer.on()
		# uncomment the next line to have the alarm trigger for 30 seconds.	
	else:
		buzzer.off()


