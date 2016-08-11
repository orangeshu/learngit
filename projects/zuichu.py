from gpiozero import LED, Button,LightSensor,Buzzer
from time  import sleep

led = LED(17)
button = Button(14)
ldr = LightSensor(4)
buzzer = Buzzer(15) 

while True:
	sleep(0.1)
	print(ldr.value)
	if ldr.value<0.8:
		buzzer.on()
		led.on()
		button.wait_for_press()
		buzzer.off()
		led.off()
		sleep(1)
	else:
		buzzer.off()
  
