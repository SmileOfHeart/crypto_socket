# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 01:03:04 2020

@author: 10365
"""


import threading
from   tcpclient  import TcpClient
from  crypto_com import CryptoModule


#线程类
class keyBordInput(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self._sock = sock
        
    def run(self):
        while True:
            msg = input(str(self._sock.localAdr) + ':')
            if msg == 'quit' or self._sock._closed:
                break
            print("send...")
            self._sock.crytoSend(msg)
        self._sock.close()   




'''
    加密的客户端程序
'''
if __name__== "__main__":
    IP = '169.254.252.124'
    port = 6001
    client = TcpClient()
    client.connect(IP,port)
    #等待接收对方公钥
    cryto = CryptoModule() 
    client.setCryto(cryto)
    publicKey = client.receiveKey()
    print(publicKey.decode())
    cryto.importPublicKey(publicKey)
    cryto.GenerateAseKey()
    print('-------------AseKey------------')
#    print(len(cryto.exportAseKey()))
    aseKey = cryto.RsaEncryptCipher.encrypt(cryto.exportAseKey())
    client.sendKey(aseKey)
#    print(len(aseKey))
    #建立线程，用于接收键盘输入
    th = keyBordInput(client)
    th.start()
    client.deCryptoReceive()
    print('remote server closed connection! press any key to exit!')
    th.join()
    print('client is closed!')