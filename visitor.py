# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 11:15:44 2020

@author: 10365
"""

from  crypto_com import CryptoCom
import socket


webServerHost = '127.0.0.1'
webServerPort =  60000

CAHost = '127.0.0.1'
CAPort = 60001

class Visitor(CryptoCom):
    def __init__():
        return True
    
    
    def prepare():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((webServerHost,webServerPort))
        
    
    
    
    