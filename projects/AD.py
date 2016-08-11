import RPi.GPIO as GPIO
import time
import sys

CLK = 18
MISO = 23
MOSI = 24
CS = 25

def setupSpiPins(clkPin,misoPin,mosiPin,csPin):
    '''Set all pins as an output except MISO(Master Input,Slave Output)'''
    pass
    
def readAdc(channel,clkPin,misoPin,mosiPin,csPin):
	if (channel<0)or(channel>7):
		print"Invalid ADC Channel"
		return  -1
	read_command = 0x18
	read_command |= channel
	
	sendBits(read_command,5,clkPin,mosiPin)
	adcValue = recBits(12,clkPin,misoPin)
	return adcValue
	
def sendBits(data,numBits,clkPin,mosiPin):
	'''Send 1 Byte or less of data'''
	data <<=(8 - numBits)
	for bit in range(numBits):
		pass
	
def recBits(numBits,clkPin,misoPin):
	'''Receives arbitrary number of bits'''
	retVal = 0
	return(retVal/2)
	
if __name__ =='__main__':
   try:
	   GPIO.setmode(GPIO.BCM)
	   setupSpiPins(CLK,MISO,MOSI,CS)
	   while True:
		   val = readAdc(0,CLK,MISO,MOSI,CS)
		   print "ADC Result: ",str(val)
		   time.sleep(0.1)
	   
   except KeyboardInterrupt:
	 GPIO.cleanup()
	 sys.exit(0)
	
