#coding:utf8

import sys,os

if os.name!='nt':#对系统的类型的判断，如果不是NT系统的话使用epoll
    from twisted.internet import epollreactor
    epollreactor.install()

from twisted.internet import reactor
from twisted.python import log
from firefly.netconnect.protoc import LiberateFactory
from firefly.utils import services

reactor = reactor

log.startLogging(sys.stdout)

services = services.CommandService("loginServer")

def netserviceHandle(target):
    services.mapTarget(target)

@netserviceHandle
def forward_0(*args,**kw):
    print("forward_0")

factory = LiberateFactory()
factory.addServiceChannel(services)

reactor.listenTCP(34530,factory)
reactor.run();



