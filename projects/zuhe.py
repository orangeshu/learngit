import math
import time 
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

print('Reading MCP3008 values, press Ctrl-C to quit...')
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
while True:
    values = [0]*8
    i=4
    time.sleep(0.00023)
    values[i] = mcp.read_adc(i)
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |{4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    x = (3.3/1024)*0.17*values[i]-0.1
    print('pm2.5 = %f' % x)
    time.sleep(2)

