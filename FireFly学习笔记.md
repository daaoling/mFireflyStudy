#firefly 学习笔记

一直以来都在考虑服务器方面的发展，于是参考了firefly学习，官方近期推出的gfirefly打算看完在学。
首先声明，我的笔记不会说的很详细，在需要的时候我只会贴出链接，不会再赘述一遍。

这篇笔记的目前的初步目标就是分析暗黑世界代码流程再自己写一点，嗯，就先这样。

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

当然如果你打算先了解个大概，那么直接看下面的也是可以的。

首先我们新建一个工程，如果你之前的firefly已经安装完毕，参考[如下][firefly的架设部署]部署

<!-- (http://github.com/yourname/your-repository/raw/master/images-folder/xxx.png) -->

结果如下,对比目录结构：

![pic](http://github.com/daaoling/mFireflyStudy/raw/master/pic/projectCompare.png)

###参考文档

[Twisted Developer Guides]:(http://twistedmatrix.com/documents/current/core/howto/index.html)

[我看到的最棒的Twisted入门教程]:(http://blog.sina.com.cn/s/blog_704b6af70100py9n.html)

[firefly的架设部署]:(http://firefly.9miao.com/wiki/index.htm)