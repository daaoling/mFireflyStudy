#coding:utf8


from twisted.internet import  reactor
from firefly.distributed.root import PBRoot,BilateralFactory
from firefly.utils.services import Service,CommandService


root = PBRoot()

service = CommandService("rootServiceHandle")
root.addServiceChannel(service)

def rootServiceHandle(target):
    service.mapTarget(target)

@rootServiceHandle
def printData1(data,data1):
    print data,data1
    print "############################"



reactor.ListenTCP(6553,BilateralFactory(root))
reactor.run();


