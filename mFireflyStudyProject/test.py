#coding:utf8


def handle(start):
    print("test","test")
    return start

@handle
def start(a,b):
    print("start","start")

# start(1,1)