# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 00:04:03 2020

@author: 10365
"""

import socket
from  crypto_com import CryptoModule

'''
基于TCP协议的服务器
循环监听并且接受收来自客户端的数据
线程用于读取键盘输入，发送到客户端
这样一次只允许一个客户端连接
'''
class TcpServer:
    def __init__(self,port):
        self._closed = False
        self._port = port
        self.client = None
        self.remoteAdr = None
        self.cryto = None   
    
    
    '''
        绑定加密模块
    '''
    def setCryto(self,cryto:CryptoModule):
        self.cryto = cryto
       
    '''
        绑定
    '''
    def bind(self):
        #作为一个服务器的工作
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((socket.gethostname(), self._port))
        self.listener.listen(1)
        self.listener.settimeout(180)
        print('Bind in endPoint' + str(self.listener.getsockname()))
        return
    
    
    '''
        一次性监听
    '''
    def listening(self):
        #server 是一个socket对象
            # accept connections from outside
        print('server is running!')
        try:
            (clientsocket, address) = self.listener.accept()
            clientsocket.settimeout(180)
        except socket.timeout as t_out:
            print(t_out)
            print('listenning failed!')
            self.close()
            pass
        else:
        # now do something with the clientsocket
            self.client = clientsocket
            self.remoteAdr = address
            print('remoted Point {} is connected'.format(str(self.remoteAdr)))
        return
    
    '''
        send String msg
    '''
    def send(self, msg):
        byteMsg = msg.encode('utf-8')
        totalsent = 0
        while totalsent < len(byteMsg):
            sent = self.client.send(byteMsg[totalsent:])
            if sent == 0:
                raise RuntimeError()
            totalsent = totalsent + sent
        return


    '''
        send String msg
    '''
    def crytoSend(self, msg):
        byteMsg = msg.encode('utf-8')
        byteMsg = self.cryto.encryptMsg(byteMsg)     #加密
        totalsent = 0
        while totalsent < len(byteMsg):
            sent = self.client.send(byteMsg[totalsent:])
            if sent == 0:
                raise RuntimeError()
            totalsent = totalsent + sent
        return


    
    '''
        循环接收数据，打印到屏幕
    '''
    def receive(self):
        while True:
            if self._closed:
                break
            try:
                chunk = self.client.recv(1024)
            except socket.timeout as t_out:
                print(t_out)
                break
            else:
                if chunk is None or len(chunk) == 0:
                    break
                print('From' + str(self.remoteAdr) + ':' + chunk.decode())
        self._closed = True
        return
    
    '''
        循环接收数据，转换成Str,放到msgBuff列表中
    '''
    def buffReceive(self,MsgBuff):
        while True:
            if self._closed:
                break
            try:
                chunk = self.client.recv(1024)
            except socket.timeout as t_out:
                #防止超时
                self._closed = True
                print(t_out)
                break  
            else:
                MsgBuff.append(chunk.decode())   #字符串解码
        return
    
        '''
        循环接收数据，打印到屏幕
    '''
    def deCryptReceive(self):
        while True:
            if self._closed:
                break
            try:
                chunk = self.client.recv(1024)
            except socket.timeout as t_out:
                print(t_out)
                break
            else:
                if chunk is None or len(chunk) == 0:
                    break
                msg = self.cryto.decryptMsg(chunk)  #解码bytes 数组
                print('From' + str(self.remoteAdr) + ':' + msg.decode())
        self._closed = True
        return
    
    
    def close(self):
        print('client is closing...!')
        self._closed = True   #关闭线程
        self.listener.close()
        if not self.client is None:
            self.client.close()

if __name__== "__main__":
    print('error')

