# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 01:05:04 2020

@author: 10365
"""

import threading
from   tcpserver  import TcpServer
from  crypto_com import CryptoModule



#线程函数
def keyBordInput(server):
    while True:
        msg = input('send to ' + str(server.remoteAdr) + ':')
        if msg == 'quit' or server._closed:
            break
        try:
            print("send...")
            server.crytoSend(msg)
        except RuntimeError as error:
            print(error.with_traceback())
            print("socket connection broken")
            break            
    server.client.close() 
    return

'''
    加密的服务器端程序
'''         
if __name__== "__main__":
    server = TcpServer(6006ok)
    server.bind()
    server.listening()
    #产生加密模块
    cryto = CryptoModule() 
    publicKey = cryto.exportPublicKey()
    server.client.send(publicKey[0:])       #发送公钥
    aseKey = cryto.RsaDecryptCipher.decrypt(server.client.recv(2048))   #解密ASE私钥
    print(aseKey.decode())
    cryto.importAseKey(aseKey)
    server.setCryto(cryto)
    #以函数的形式启动线程
    ct = threading.Thread(target = keyBordInput, args=[server])
    ct.start()
    server.deCryptReceive()
    ct.join
    server.close()
    print('server is closed!')