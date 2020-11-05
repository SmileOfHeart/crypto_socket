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

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoModule():
    def __init__(self):
        #对称加密算法
        self.AseKey = None
        self.rsa = None  #非对称加密
        self.fernet = None  #Ase加解密器
        self.password = b"password"
        return
    
    def setPassword(self,passwd):
        self.password = passwd
    
    def GenerateAseKey(self):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        self.AseKey = base64.urlsafe_b64encode(kdf.derive(self.password))
        self.fernet = Fernet(self.AseKey)

    
    
    def exportAseKey(self):
        return self.AseKey    #这是一个bytes类型
    
    def importAseKey(self,key):
        self.AseKey = key
        self.fernet = Fernet(self.AseKey)
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
    
    
    '''通过ASE进行消息加密
        msg 是字符数组
    '''
    def encryptMsg(self,msg):
        #发送加密后的信息
        crytoMsg = self.fernet.encrypt(msg)
        return crytoMsg
    
    '''通过ASE进行消息解密
       msg 是字符数组
    '''
    def decryptMsg(self,crytoMsg):
        #解密密文信息，都是Byte数组
        print(crytoMsg.decode())
        msg = self.fernet.decrypt(crytoMsg)
        return msg