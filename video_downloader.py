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


def all_m3u8_file():
    for i in os.listdir('./m3u8/'):
        for file in os.listdir('./m3u8/{}'.format(i.strip())):
            path = './m3u8/{0}/{1}'.format(i.strip(), file.strip())
            deal_m3u8_file(path)
            break
        break


def deal_m3u8_file(path):
    url = open(''.join([path, '/url.txt']), 'r', encoding='utf-8').read()
    print(url)
    for each in open(''.join([path, '/index.m3u8']), 'r', encoding='utf-8'):
        print(each.strip())

if __name__ == '__main__':
    all_m3u8_file()