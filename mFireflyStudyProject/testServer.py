#coding:utf8

import sys,os

if os.name!='nt':#对系统的类型的判断，如果不是NT系统的话使用epoll
    from twisted.internet import epollreactor
    epollreactor.install()

from twisted.internet import reactor
from twisted.python import log
from firefly.netconnect.protoc import LiberateFactory
from firefly.utils import services


log.startLogging(sys.stdout)

factory = LiberateFactory()

services = services.CommandService("loginServer")
factory.addServiceChannel(services)

reactor.listen(65533,factory)
reactor.run();



