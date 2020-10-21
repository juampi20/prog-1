#!/usr/bin/python3
import time, json
from random import uniform, random, randint, uniform
import socket, sys, time

def send_data():
    value_sensor = {
    'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
    'depth': randint(5,250) ,
    'magnitude': round(uniform(2.0,5.5), 1),
    'latitude': uniform(-180,180),
    'longitude': uniform(-90, 90)
    }
    return value_sensor

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
"""
socket.socket(FamiliaProtocolos, TipoSocket)
    FamiliaProtocolos: AF_INET / AF_UNIX
    TipoSocket: SOCK_DGRAM - socket datagrama (UDP)
                SOCK_STREAM - socket de flujo (TCP)
"""

# get local machine name
#host = socket.gethostname()
host = ""
"""
    el socket atiende en todas las IP's locales: 0.0.0.0
        ej. 127.0.0.1, 192.168.0.10, 10.0.0.1, ...
"""
port = int(sys.argv[1])

# bind to the port
serversocket.bind((host, port))

while True:
    # establish a connection
    print("Listening...")
    data,addr = serversocket.recvfrom(1024)
    print(addr)
    address = addr[0]
    port = addr[1]
    print("Address: %s - Port %d" % (address, port))
    msg = json.dumps(send_data())
    serversocket.sendto(msg.encode(), addr)
clientsocket.close()

"""
Conectar al cliente usando ncat:
    ncat 127.0.0.1 1234 -u -v
"""
