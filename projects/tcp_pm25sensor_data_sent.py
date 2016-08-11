import spidev
import time
import os
import RPi.GPIO as GPIO
import socket
import struct
import binascii
import math

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# ===added by rocky at 2016-07-06 start===
# ===============TCP Socket Helper start=============== #
DEBUG = True

DST_SERVER_IP = '115.28.150.131'
DST_SERVER_PORT = 20199

packer = struct.Struct('!H H f')


def get_tcp_socket():
    server_address = (DST_SERVER_IP, DST_SERVER_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.connect(server_address)
    return sock


def send_data2server(data):
    sock = None
    try:
        sock = get_tcp_socket()
        packed_data = packer.pack(*data)
        sock.sendall(packed_data)
        if DEBUG:
            print('Succeed in sending "{} {}" to {}'.
                  format(binascii.hexlify(packed_data), data, sock.getpeername()))
    except Exception as e:
        print('Error:', e)
    finally:
        if sock:
            sock.close()
# ===============TCP Socket Helper end=============== #
# check and send data interval(in seconds)
CHECK_INTERVAL = 1
# mark the device with unique id(This id should be registered on http://115.28.150.131:20180/)
DEVICE_ID = 1
# mark the sensor with unique id(This id should be registered on http://115.28.150.131:20180/)
SENSOR_ID = 3
# ===added by rocky at 2016-07-06 end===


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data



  
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertSharp(data,places):
	sharp = ((data * 3.3)/float(1023))
	sharp = round(sharp,places)
	return sharp
  
# Define sensor channels
#light_channel = 0
sharp_channel  = 4

# Define delay between readings


i=0
sum_volts=0
sum_level=0
base_volts=0.6*0.63*300
while True:
  GPIO.output(18,True)
  time.sleep(0.00028)

  # Read the light sensor data
  #light_level = ReadChannel(light_channel)
  #light_volts = ConvertVolts(light_level,2)

  # Read the temperature sensor data
  sharp_level = ReadChannel(sharp_channel)
  sharp_volts = ConvertSharp(sharp_level,2)
  
 
  GPIO.output(18,False)
  time.sleep(0.00968)
  
  sum_volts=sum_volts+sharp_volts
  sum_level=sum_level+sharp_level
  i+=1
  
  if i > 2998:
	  average_volts = sum_volts/i
	  average_level = sum_level/i
	  pm25 = 0.6*0.63*1000*average_volts-base_volts
	  i=0
	  sum_level=0
	  sum_volts=0
	  print(('the pm2.5 is %f' %pm25))
	  print "--------------------------------------------"  
	  #print("Light : {} ({}V)".format(light_level,light_volts))  
	  print("Sharp  : {} ({}V)".format(average_level,average_volts)) 
	  data = (DEVICE_ID , SENSOR_ID,pm25)
	  send_data2server(data)
   
   
 


 
