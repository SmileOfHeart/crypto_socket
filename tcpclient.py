# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 11:30:43 2020

@author: 10365
"""

''' TCP 通信模块 '''

import socket
from  crypto_com import CryptoModule

'''
基于TCP协议的Client，循环收来自服务器的数据
可以建立一个线程，读取键盘输入，发送到服务器
'''

class TcpClient:
    def __init__(self,sock=None):
        if sock is None:
            self.sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self._closed = False
        self.cryto = None   #RSACrypto对象

    '''
        绑定加密模块
    '''
    def setCryto(self,cryto:CryptoModule):
        self.cryto = cryto
       

         
    '''
        host: server ip
        port: server port
    '''
    def connect(self, host, port):
        #host 是一个IP地址字符串 ports是一个整数
        self.sock.connect((host, port))
        self.sock.settimeout(180)
        self.localAdr = self.sock.getsockname()
        self.serverAdr = self.sock.getpeername()
        return

    '''
        send String msg
    '''
    def send(self, msg):
        byteMsg = msg.encode('utf-8')
        totalsent = 0
        while totalsent < len(byteMsg):
            sent = self.sock.send(byteMsg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        return
    
    
    '''
        send String msg
    '''
    def sendPublicKey(self):
        byteMsg = self.cryto.GetMyPublicKey()     #pulickey是bytes数组
        totalsent = 0
        while totalsent < len(byteMsg):
            sent = self.sock.send(byteMsg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        return
    
    '''
        send encryto String msg  By
    '''
    def crytoSend(self, msg,):
        byteMsg = msg.encode('utf-8')
        byteMsg = self.cryto.encryptMsg(byteMsg)     #加密
        totalsent = 0
        while totalsent < len(byteMsg):
            sent = self.sock.send(byteMsg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
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
                chunk = self.sock.recv(4096)
            except socket.timeout as t_out:
                print(t_out)
                break
            else:
                if chunk is None or len(chunk) == 0:
                    break
                print(str(self.serverAdr) + ':' + chunk.decode())
        self._closed = True
        return
    
    '''
        接收密钥
    '''
    def receiveKey(self):
        try:
            chunk = self.sock.recv(4096)
        except socket.timeout as t_out:
            print(t_out)
        else:
            if chunk is None or len(chunk) == 0:
                self._closed = True
                return
            self.cryto.importPublicKey()
        return

    '''
        循环接收数据，转换成Str,放到msgBuff列表中
    '''
    def buffReceive(self,MsgBuff):
        while True:
            if self._closed:
                break
            try:
                chunk = self.sock.recv(1024)
            except socket.timeout as t_out:
                #防止超时
                self._closed = True
                print(t_out)
                break  
            else:
                MsgBuff.append(chunk.decode())
        return 
  
    
    '''
        解密接收数据，转换成Str,打印到屏幕
    '''
    def deCryptoReceive(self):
        while True:
            if self._closed:
                break
            try:
                chunk = self.sock.recv(1024)
            except socket.timeout as t_out:
                print(t_out)
                break
            else:
                if chunk is None or len(chunk) == 0:
                    break 
                msg = self.cryto.decryptMsg(chunk)  #解码bytes 数组
                print('From' + str(self.serverAdr) + ':' + msg.decode())
        self._closed = True
        return
    
    
    def close(self):
        print('client is closing...!')
        self._closed = True
        self.sock.close()




if __name__== "__main__":
    print('error')


    
    


