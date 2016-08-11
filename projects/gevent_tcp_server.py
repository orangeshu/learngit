# coding=utf-8
import struct
import binascii
from gevent.pool import Pool
from gevent.server import StreamServer
from gevent import socket

__author__ = 'rockychi1001@gmail.com'

# ===Server configuration begin=== #
# server port
SERVER_PORT = 20199
# max tcp connection size(max value 50000)
POOL_SIZE = 1000
# tcp socket timeout(in seconds)
TIMEOUT = 60
socket.setdefaulttimeout(TIMEOUT)
# ===Server configuration end=== #

socket_dict = dict()

unpacker = struct.Struct('!H H f')


def handle(sock, address):
    socket_dict[address] = sock
    print("Connected:<%s:%s>" % address)
    try:
        while True:
            # Just echos whatever it receives
            try:
                data = sock.recv(unpacker.size)
                if data:
                    print('received "%s"' % binascii.hexlify(data))
                    unpacked_data = unpacker.unpack(data)
                    print('unpacked:', unpacked_data)
                else:
                    break
            except socket.timeout as st:
                print(st)
                break
            except Exception as e:
                print(e)
                continue
    finally:
        print("Disconnected:<%s:%s>" % address)
        try:
            sock.shutdown(socket.SHUT_WR)
            sock.close()
        except Exception as e:
            print('Error:', e)
        finally:
            socket_dict.pop(address)


pool = Pool(POOL_SIZE)
server = StreamServer(('0.0.0.0', SERVER_PORT), handle, spawn=pool)
try:
    print("Tcp server listening on:%s" % SERVER_PORT)
    server.serve_forever()
except:
    print('Tcp server Exiting...')
finally:
    print("Shutting down all sockets...")
    for _address, _sock in socket_dict.items():
        print("Disconnected:<%s:%s>" % _address)
        try:
            if _sock:
                _sock.shutdown(socket.SHUT_WR)
                _sock.close()
        except:
            continue

    print('Tcp server closed')
