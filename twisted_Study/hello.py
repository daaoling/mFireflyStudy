from twisted.internet import reactor

reactor.callLater(4, reactor.stop)
reactor.run()