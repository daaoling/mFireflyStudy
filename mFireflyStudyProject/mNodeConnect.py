#coding:utf8

from firefly.distributed.node import RemoteObject

remote = RemoteObject("testNode")

addr = ("127.0.0.1",6553)


def startClient():
    remote.connect(addr)

if __name__ == "__main__":
    startClient()