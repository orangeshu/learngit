# coding=utf-8
import socket
import struct
import binascii

__author__ = 'rockychi1001@gmail.com'

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


if __name__ == '__main__':
    data = (1, 2, 3.0123)
    send_data2server(data)
