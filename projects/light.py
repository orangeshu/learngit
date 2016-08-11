import socket
import struct
from time import sleep
import binascii

from gpiozero import LightSensor, Buzzer

ldr = LightSensor(4)  # alter if using a different pin
buzzer = Buzzer(15)  # alter if using a different pin

# ===added by rocky at 2016-07-06 start===
# ===============TCP Socket Helper start=============== #
DEBUG = True

DST_SERVER_IP = '115.28.150.131'
DST_SERVER_PORT = 20199

packer = struct.Struct('!H H f')
sockets_dict = dict()


def get_tcp_socket():
    server_address = (DST_SERVER_IP, DST_SERVER_PORT)
    sock = sockets_dict.get(server_address)
    if not sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        sockets_dict[server_address] = sock
    return sock


def send_data2server(data):
    sock = get_tcp_socket()
    if sock:
        try:
            packed_data = packer.pack(*data)
            sock.sendall(packed_data)
            if DEBUG:
                print('Succeed in sending "{}{}" to {}'.
                      format(binascii.hexlify(packed_data), data, sock.getpeername()))
        except Exception as e:
            print('Error:', e)


# ===============TCP Socket Helper end=============== #
# check and send data interval(in seconds)
CHECK_INTERVAL = 1
# mark the device with unique id(This id should be registered on http://115.28.150.131:20180/)
DEVICE_ID = 1
# mark the sensor with unique id(This id should be registered on http://115.28.150.131:20180/)
SENSOR_ID = 1
# ===added by rocky at 2016-07-06 end===

while True:
    sleep(CHECK_INTERVAL)
    print(ldr.value)
    # ===added by rocky at 2016-07-06 start===
    data = (DEVICE_ID, SENSOR_ID, "%.4f" % ldr.value)
    send_data2server(data)
    # ===added by rocky at 2016-07-06 end===

    if ldr.value < 0.8:  # adjust this to make the circuit more or less sensitive
        buzzer.on()
    # uncomment the next line to have the alarm trigger for 30 seconds.
    else:
        buzzer.off()
