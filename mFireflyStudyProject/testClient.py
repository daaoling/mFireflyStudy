#coding:utf8

from socket import AF_INET,SOCK_STREAM,socket
import struct
HOST="127.0.0.1"
PORT=34530
ADDR=(HOST , PORT)

def sendData(sendstr,commandId):
    HEAD_0 = chr(0)
    HEAD_1 = chr(0)
    HEAD_2 = chr(0)
    HEAD_3 = chr(0)
    ProtoVersion = chr(0)
    ServerVersion = 0
    sendstr = sendstr
    data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                       HEAD_3,ProtoVersion,ServerVersion,\
                       len(sendstr)+4,commandId)
    senddata = data+sendstr
    return senddata

client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)
client.sendall(sendData('asdfe',0))

