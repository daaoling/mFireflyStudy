#coding:utf8


class mProcotol():

    def __init__(self):
        self.dataHandler = self.dataHandlerCoroutine()
        # self.dataHandler.next()

    def dataHandlerCoroutine(self):
        while True:
            print("1")
            yield

    def test(self):
        self.dataHandler.send("test")

mTest = mProcotol();
# mTest.test();