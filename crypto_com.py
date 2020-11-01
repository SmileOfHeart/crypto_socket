# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 12:17:06 2020

@author: 10365
"""


from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


'''
    生成对称加密算法ASE加密密钥
    通过非对称加密算法交换ASE密钥
    通过对称加密算法进行加密
    加密都是byte数组
'''

class CryptoModule():
    def __init__(self):
        #对称加密算法
        self.AseKey = b' ASE_KEY '
        self.rsa = None  #非对称加密
        return
    
    
    
    ''' 导入对方公钥,生成加密器'''
    def importPublicKey(self,publicKey):
        oppRsa = RSA.importKey(publicKey)       
        self.RsaEncryptCipher =PKCS1_OAEP.new(oppRsa)   #利用对方的公钥生成加密器
        print('successfully import public key')
        return
    
    '''导出公钥,并利用私钥生成解密器'''
    def exportPublicKey(self):
        randgen = Random.new().read
        self.rsa = RSA.generate(1024, randgen) #产生私钥和公钥
        publicKey = self.rsa.publickey().exportKey()
        self.RsaDecryptCipher = PKCS1_OAEP.new(self.rsa)      #利用自己的私钥生成加密器
        return publicKey
    
    
    def exportAseKey(self):
        return self.AseKey
    
    def importAseKey(self,key):
        self.AseKey = key
        return 
    
    '''通过ASE进行消息加密
        msg 是字符数组
    '''
    def encryptMsg(self,msg):
        #发送由对方公钥加密后的信息
#        crytoMsg = self.encryptCipher.encrypt(msg)
        crytoMsg = msg + self.AseKey
        return crytoMsg
    
    '''通过ASE进行消息解密
       msg 是字符数组
    '''
    def decryptMsg(self,crytoMsg):
        #接收自己公钥密文信息
        #并且采用自己的私钥进行解密
#        msg = self.decr.yptCipher.decrypt(crytoMsg)
        msg = self.AseKey + crytoMsg 
        return msg