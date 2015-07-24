#firefly 初级教程

一直以来都在考虑服务器方面的发展，于是参考了firefly学习，官方近期推出的gfirefly打算看完firefly在学。
首先声明，我的教程不会说的很详细，在需要的时候我只会贴出链接，不会再赘述一遍。

这篇教程的目前的初步目标就是分析暗黑世界代码流程再自己写一点，嗯，就先这样。

首先要感谢gfirefly群里的欧拉K，逸飞等各位大神。对于一个python新手来说哪怕一点点指点都能让我少走多少弯路。



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

结果如下：

![pic](http://github.com/daaoling/mFireflyStudy/raw/master/pic/projectCompare.png)

点击startmaster.py 运行, 如果没报错那么表示你已经可以开始firefly了.

###参考文档

[Twisted Developer Guides]:(http://twistedmatrix.com/documents/current/core/howto/index.html)

[我看到的最棒的Twisted入门教程]:(http://blog.sina.com.cn/s/blog_704b6af70100py9n.html)



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
	
	*　factory 和 Protocol 关系

	*　拆包解包

## 首先，我们实现子进程初始化

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

##　然后，我们要分析的就是net子进程，

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
            __import__(app)


server.FFServer => start():
    
    def start(self):
        '''启动服务器
        '''
        log.msg('%s start...'%self.servername)
        log.msg('%s pid: %s'%(self.servername,os.getpid()))
        reactor.run()

这样我们的net子进程就启动了。

##  net 的 监听模型

既然我们已经启动并配置了net进程用于客户端的连接, 我们在细节上做进一步的了解。

此时我假定你已经对twisted有所了解，不然接下来涉及到的术语可能在阅读上有些困难。




##  拆包，解包

###参考文档

[1]:(http://www.blogjava.net/landon/archive/2012/07/14/383092.html)

[2]:(http://www.zhihu.com/question/29779732)



对于net模块的初级通信我在开始写的时候发现了一篇差不多的文章

[[笨木头FireFly01]入门篇1·最简单的服务端和客户端连接](http://www.benmutou.com/archives/718)

他是基于官方一个测试用例进行了讲解，非常适合初学者。哪怕你什么都不懂，看完他的文章你也会有一点最基本的认知。

不过我倾向于在firefly的框架下, 进行解析。

我们来看DiabloWorld/config.json

"servers":{
	"net":{"netport":11009,"name":"net","remoteport":[{"rootport":10000,"rootname":"gate"}],"app":"app.netserver","log":"app/logs/net.log"},
}

