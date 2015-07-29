#coding:utf8


from firefly.utils.services import Service,CommandService
from firefly.server.globalobject import GlobalObject, netserviceHandle

@netserviceHandle
def forwarding_0(*args, **kwargs):
    print("forwarding_0")
