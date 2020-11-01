这些代码是拥有加密功能的Socket通信程序，主要分为三部分：
1.支持单连接的Socket服务器和客户端；
2.基于RSA算法和AES算法的加密模块；
3.基于多线程的命令行输入输出外壳。

用途：
1.作为密码学网站通信加密原理学习的例子。
2.作为安全通信软件的socket通信底层代码的基础demo。


代码简介：
1.底层socket通信代码
tcpclient.py        socket客户端
tcpserver.py        socket服务器

2.加密模块代码
crypto_com.py		生成AES算法的加密密钥（用于网络中信息的安全传递），通过RSA算法将密钥进行加密和解密（用于网络中密钥的安全分发）


3.命令行界面操作代码
client.py           启动socket客户端，连接到服务器，并且开启线程以便中命令行中进行交互
server.py        	启动socket服务器，等待连接，并在连接后开启线程以便中命令行中进行交互

4.采用加密后的命令行界面操作代码
crypto_client.py           启动socket客户端，连接到服务器，并且开启线程以便中命令行中进行交互
crypto_server.py           启动socket服务器，等待连接，并在连接后开启线程以便中命令行中进行交互
同时双方还对加密通信进行一些准备工作

安全通信流程：
1.服务器产生并发送RSA公钥；
2.客户端拿到公钥
3.客户端生成AES密钥
4.客户端对AES密钥进行加密并且发送
5.服务器接收加密信息，解密得到客户端的AES密钥
6.双方使用AES密钥进行加密通信。
