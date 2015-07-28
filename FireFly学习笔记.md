#firefly 初级教程

一直以来都在考虑服务器方面的发展，于是参考了firefly学习，官方近期推出的gfirefly打算看完firefly在学。
首先声明，我的教程不会说的很详细，在需要的时候我只会贴出链接，不会再赘述一遍。

这篇教程的目前的初步目标就是分析暗黑世界代码流程再自己写一点，嗯，就先这样。

首先要感谢gfirefly群里的欧拉K，逸飞, gavin等各位大神。对于一个python新手来说哪怕一点点指点都能让我少走多少弯路。

此外我在firefly研究中也发现了一些暂时搞不明白的问题，我也会在教程中列出来希望大家一起交流。

# 1. firefly 安装

##安装流程

具体windows与linux的安装我就不加赘述，详情可以参考下方的链接

基本都是easy_install就完事了

就windows下安装 MySQL-python 与 pywin32 出了点问题，需要手动安装。

我的系统是64 bit, python 版本 2.7  （32bit也有各自对应的）

需要如下两个:
	
	MySQL-python-1.2.5.win-amd64-py2.7.exe
	
	pypiwin32-219.win-amd64-py2.7.exe

下载[附件](http://yunpan.cn/ccXguDMy2YeCa)(访问密码 2ba8)，双击安装即可。

装完之后, import firefly 一下，如果没问题就安装成功了

##参考文档：

[[官方教程] Firefly安装说明 与 常见问题（第三方库帖内下载）](http://www.9miao.com/forum.php?mod=viewthread&tid=33009&fromuid=87)

[firefly wiki ](http://firefly.9miao.com/wiki/index.htm)

[diabloworld_wiki](http://firefly.9miao.com/diabloworld_wiki/index.htm)

[pypi](https://pypi.python.org/pypi)



# 2. firefly 初体验 (总是感觉这个词用的怪怪的)

在学习firefly之前，我建议你阅读以下 [Twisted 文档][Twisted Developer Guides]  和一篇不错的 [中文入门][我看到的最棒的Twisted入门教程]. 

不用了解太多，只要能明白以下概念：
	
	1. reactor 模式

	2. factory =>　protocol

	3. deferred 对象

	4. PB协议

当然如果你打算先了解个大概，那么直接看下面的也是可以的。不过你会很吃力，在一些概念的讲解上。

如果你之前的firefly已经安装完毕， 首先我们新建一个模板工程。

	firefly-admin.py createproject youProjectName

<!-- (http://github.com/yourname/your-repository/raw/master/images-folder/xxx.png) -->

暗黑的工程目录对比，结果如下：

![pic](http://github.com/daaoling/mFireflyStudy/raw/master/pic/projectCompare.png)

点击startmaster.py 运行, 如果没报错那么表示你已经可以开始firefly了.

[Twisted Developer Guides]:http://twistedmatrix.com/documents/current/core/howto/index.html

[我看到的最棒的Twisted入门教程]:http://blog.sina.com.cn/s/blog_704b6af70100py9n.html



# 3. firefly net 模块

我想你在听说firfly的时候应该了解他是一个分布式服务器框架，同时我也假定你了解了一些手游服务器的架构。

如果你没有概念, 你可以参考如下链接:
	
[MMORPG服务器架构][1]

[知乎端游、手游服务端常用的架构是什么样的][2]

如果了解的话，我们看下暗黑的模块分隔：

![pic](http://github.com/daaoling/mFireflyStudy/raw/master/pic/1.png)

![pic](http://github.com/daaoling/mFireflyStudy/raw/master/pic/2.png)

今天在这一篇中我们可以学到：

	*　firefly 进程的启动流程

	*　net 模块对连接的处理

## 子进程初始化

	$ python startmaster.py 

贴上主要代码：

startmaster.py：

	master = Master()
	master.config('config.json','appmain.py')
	master.start()

config.json：

	"servers":{
		"gate":{"rootport":10000,"name":"gate","db":true,"mem":true,"app":"app.gateserver","log":"app/logs/gate.log"},
		
		"dbfront":{"name":"dbfront","db":true,"mem":true,"app":"app.dbfrontserver","log":"app/logs/dbfront.log"},
		
		"net":{"netport":11009,"name":"net","remoteport":[{"rootport":10000,"rootname":"gate"}],"app":"app.netserver","log":"app/logs/net.log"},
		
		"admin":{"remoteport":[{"rootport":10000,"rootname":"gate"}],
	         "name":"admin","db":true,"mem":true,"app":"app.adminserver","log":"app/logs/admin.log"},
		
		"game1":{"remoteport":[{"rootport":10000,"rootname":"gate"}],
	         "name":"game1","db":true,"mem":true,"app":"app.gameserver","reload":"app.game.doreload","log":"app/logs/game1.log"}
	}

master.py => start():

	config = json.load(open(self.configpath,'r'))
	sersconf = config.get('servers')
	for sername in sersconf.keys():
	    cmds = 'python %s %s %s'%(self.mainpath,sername,self.configpath)
	    subprocess.Popen(cmds,shell=True)
	reactor.run()

log如下：

python appmain.py dbfront config.json

python appmain.py gate config.json

python appmain.py net config.json

python appmain.py game1 config.json

python appmain.py admin config.json


走完上述的流程，各个子进程就启动起来了。

对于net子进程，我们从上述的流程图就可以了解到net是直接和客户端打交道的。

##　net子进程，

	$ python appmain.py net config.json


贴上主要代码：

	"net":{"netport":11009,"name":"net","remoteport":[{"rootport":10000,"rootname":"gate"}],"app":"app.netserver","log":"app/logs/net.log"},

appmain.py:	
	ser = FFServer()
    ser.config(serconfig, dbconfig=dbconf, memconfig=memconf,masterconf=masterconf)
    ser.start()

server.FFServer => config(*arg):
    if netport:
	    self.netfactory = LiberateFactory() //建立一个协议工厂
	    netservice = services.CommandService("netservice") //建立一个service 用于消息分发
	    self.netfactory.addServiceChannel(netservice)
	    reactor.listenTCP(netport,self.netfactory) //开始监听
    

    if app:
            __import__(app)  //app.netserver

server.FFServer => start():
    def start(self):
        '''启动服务器
        '''
        log.msg('%s start...'%self.servername)
        log.msg('%s pid: %s'%(self.servername,os.getpid()))
        reactor.run()

这样我们的net子进程就启动了。

## net 模块的启动监听

既然我们已经启动并配置了net进程用于客户端的连接, 我们在细节上做进一步的了解。

我在写这篇文章的时候找到了下面这个系列:

[[笨木头FireFly01]入门篇1·最简单的服务端和客户端连接][3]

他是基于官方一个测试用例进行了讲解，非常适合初学者。相对来说我觉得他可能比我写的更加入门,我建议先看他的系列，然后再看我下面的章节补充一下即可。

一般成熟的服务器与客户端基本的流程都是启动tcp连接进行监听之后，异步事件驱动实现对连接的消息处理。

java就一般用mina,netty实现。

python的twisted就用reactor模式实现监听，使用Protocl用于对连接的处理，Factory用于对连接的管理。

Firefly框架的 netconnect模块就基于上面的机制封装了一下。

下面是官方的一张结构图，我想如果你看完了木头的上述章节这张图一下子就明白了。

![pic](http://github.com/daaoling/mFireflyStudy/raw/master/pic/3.png)

<!-- ###参考文档 -->

[1]:http://www.blogjava.net/landon/archive/2012/07/14/383092.html

[2]:http://www.zhihu.com/question/29779732

[3]:http://www.benmutou.com/archives/718


# 3.firefly 进程间的通信 并 解析gate模块

firefly 号称分布式的服务器框架，那么他一定有一套成熟好用的进程间通信的方式， 这个就是twisted的PB协议。我在写这一章节的时候还是决定按着暗黑的流程在分析。


Firefly对于PB的封装在 /distribute 目录
__init__.py  child.py     manager.py   node.py      reference.py root.py

root.py 实现PB的server功能
node.py 实现PB的client功能。
child.py 每个client连接上root都会初始化一个child来保存该client的相关信息，并且将这些child通过manager来管理。
manager.py 管理root的child，通过一个字典self._childs = {}，实现一个增删改的小管理器。
reference.py 如果你看了前面twisted官网的介绍就会知道，node只要实例化一个 pb.Referenceable 类，并把它传递给root，那么root就能够把这个pb.Referenceble当成句柄来远程调用client的函数。

![pic](http://github.com/daaoling/mFireflyStudy/raw/master/pic/4.png)



下面来看看暗黑对其的主要应用

config.json
	
	"gate":{"rootport":10000,"name":"gate","db":true,"mem":true,"app":"app.gateserver","log":"app/logs/gate.log"},

	"net":{"netport":11009,"name":"net","remoteport":[{"rootport":10000,"rootname":"gate"}],"app":"app.netserver","log":"app/logs/net.log"},

我们这里再来回顾暗黑gate, net节点的配置，发现net 有一个 remoteport 对应 gate 的 rootport

上述配置对应的代码如下:

server.py

    if rootport:
	    self.root = PBRoot()
	    rootservice = services.Service("rootservice")
	    self.root.addServiceChannel(rootservice)
	    reactor.listenTCP(rootport, BilateralFactory(self.root))

    for cnf in self.remoteportlist:
	    rname = cnf.get('rootname')
	    self.remote[rname] = RemoteObject(self.servername)

gate 模块有 PBRoot()

而 net 模块有 对应 gate 的 RemoteObject()

	class RemoteObject(object):
	    '''远程调用对象'''
	    
	    def __init__(self,name):
	        '''初始化远程调用对象
	        @param port: int 远程分布服的端口号
	        @param rootaddr: 根节点服务器地址
	        '''
	        self._name = name
	        self._factory = pb.PBClientFactory()
	        self._reference = ProxyReference()
	        self._addr = None