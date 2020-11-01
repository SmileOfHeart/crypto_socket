# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 01:11:50 2020

@author: 10365
"""

import threading
from   tcpserver  import TcpServer


#线程函数
def keyBordInput(server):
    while True:
        msg = input('send to ' + str(server.remoteAdr) + ':')
        if msg == 'quit' or server._closed:
            break
        try:
            print("send...")
            server.send(msg)
        except RuntimeError as error:
            print(error.with_traceback())
            print("socket connection broken")
            break            
    server.client.close() 
    return

'''
    普通的服务器端程序
'''         
if __name__== "__main__":
    server = TcpServer(6002)
    server.bind()
    server.listening()
    #以函数的形式启动线程
    ct = threading.Thread(target = keyBordInput, args=[server])
    ct.start()
    server.receive()
    ct.join
    server.close()
    print('server is closed!')