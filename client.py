# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 01:11:35 2020

@author: 10365
"""

import threading
from   tcpclient  import TcpClient



#线程类
class keyBordInput(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self._sock = sock
        
    def run(self):
        print('input \'quit\' to exit!')
        while True:
            msg = input(str(self._sock.localAdr) + ':')
            if msg == 'quit' or self._sock._closed:
                break
            self._sock.send(msg)
        self._sock.close()   




'''
    普通的客户端程序
'''
if __name__== "__main__":
    IP = '169.254.252.124'
    port = 6000
    client = TcpClient()
    client.connect(IP,port)
    #建立线程，用于接收键盘输入
    th = keyBordInput(client)
    th.start()
    client.receive()
    print('remote server closed connection! press any key to exit!')
    th.join()
    print('client is closed!')