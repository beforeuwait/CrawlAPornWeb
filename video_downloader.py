# coding=utf-8


import os
import requests
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


"""
key = ""
cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, key.encode('utf-8'))
res = cryptor.decrypt('二进制')
"""