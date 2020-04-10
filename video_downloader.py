# coding=utf-8


import os
import re
import time
import requests
import shutil
from copy import deepcopy
from Crypto.Cipher import AES
from config_real import PROXY_PRO
from multiprocessing import Pool


def all_m3u8_file():
    for i in os.listdir('./m3u8/'):
        if i.strip() == '国产自拍':
            for file in os.listdir('./m3u8/{}'.format(i.strip())):
                path = './m3u8/{0}/{1}'.format(i.strip(), file.strip())
                deal_m3u8_file(path)


def deal_m3u8_file(path):
    print(path)
    already_crawl = set([i.strip() for i in open('./already_crawl.txt', 'r', encoding='utf-8')])
    dot, m3u8, cate, title = path.split('/')
    seed_dict = parse_m3u8(path)
    # 这里需要更改path了
    print('更新目录')
    path_tmp = '/'.join([dot, 'video_tmp', cate, title])
    if path_tmp in already_crawl:
        print('当前文件已经下载,\t{}'.format(path_tmp))
        return
    path_normal = '/'.join([dot, 'video', cate, title])
    if not os.path.exists('/'.join([dot, 'video', cate])):
        print('创建正式目录:\t{0}'.format('/'.join([dot, 'video', cate])))
        os.makedirs('/'.join([dot, 'video', cate]))
    if not os.path.exists(path_tmp):
        print('创建临时目录:\t{0}'.format(path_tmp))
        os.makedirs(path_tmp)

    key = seed_dict.get('key', None)
    uri = seed_dict.get('uri')
    if not key:
        print('当前视频未加密')
    # 开始下载
    print('启动多进程开始下载视频片段')
    pool = Pool(10)
    n = 1
    for i in seed_dict.get('data'):
        url = ''.join([uri, i])
        # download_ts(path_tmp, url, key, n)
        pool.apply_async(download_ts, (path_tmp, url, key, n))
        n += 1
    pool.close()
    pool.join()
    # 下载完毕后，验证完整性,开始合并任务，并删除tmp文件
    while True:
        print('效验文件完整度.........')
        redownload_list = veriy_tmp_file(path_tmp, n)
        if redownload_list:
            # 重新下载
            t = 1
            for i in seed_dict.get('data'):
                if t in redownload_list:
                    url = ''.join([uri, i])
                    print('重新下载编号为:\t{}\t的文件'.format(t))
                    download_ts(path_tmp, url, key, n)
                t += 1
        else:
            print('文件完整')
            break
    all_in_one(n, path_tmp, path_normal)


def veriy_tmp_file(path, n):
    """
    验证是否为完整，返回不存在的
    :return:
    """
    data = []
    for i in range(1, n):
        if not os.path.exists(''.join([path, '/{}.ts'.format(i)])):
            data.append(i)
    return data


def all_in_one(n, path_tmp, path_normal):
    # 合并文件
    with open(''.join([path_normal, '.ts']), 'wb') as f:
        for i in range(1, n):
            p = open(''.join([path_tmp, '/{}.ts'.format(i)]), 'rb')
            f.write(p.read())
            p.close()
            os.remove(''.join([path_tmp, '/{}.ts'.format(i)]))
    
    # 合并完成，开始删除
    # 不便于去重
    print('删除临时目录:\t{}'.format(path_tmp))
    shutil.rmtree(path_tmp)
    # 记录已经采集
    with open('./already_crawl.txt', 'a', encoding='utf-8') as f:
        f.write(path_tmp + '\n')


def download_ts(path, url, key, n):
    print('接收到任务:{}\t开始处理'.format(n))
    ts_content = request_get_whitout_heade(url)
    if key and ts_content:
        # 开始解密
        print('开始解密')
        cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, key.encode('utf-8'))
        ts_content = cryptor.decrypt(ts_content)
        print('保存切片')
        with open(''.join([path, '/{0}.ts'.format(n)]), 'wb') as f:
            f.write(ts_content)
    elif ts_content:
        print('保存切片')
        with open(''.join([path, '/{0}.ts'.format(n)]), 'wb') as f:
            f.write(ts_content)


def parse_m3u8(path):
    """
    解析文件
    直接下载， 是否加密
    加密找到key 和加密方式
    """
    seeds_data = {}
    data = []
    url = open(''.join([path, '/url.txt']), 'r', encoding='utf-8').read()
    url = url.strip().split('index')[0]
    seeds_data.update({'uri': url})
    m3u8_path = ''.join([path, '/index.m3u8'])
    for each in open(m3u8_path, 'r', encoding='utf-8'):
        if each.startswith('#EXT-X-KEY'):
            # 说明有加密
            aes_type = re.findall('METHOD=(.*?),', each)[0]
            print('当前资源有进行加密,加密方式:\t{0}'.format(aes_type))
            key_uri = url + re.findall('URI="(.*)"', each)[0]
            key = download_key(path, key_uri)
            seeds_data.update({'key': key})
            print('当前key为:\t', key)
            continue
        if each.startswith('#'):
            continue
        # 然后才是下载内容
        """
        # 将url 和 保存路径 和 key 放入下载队列
        # 这里也可以用多进程
        # 我使用多进程
        # 特别要注意排序
        """
        data.append(each.strip())
    seeds_data.update({'data': data})
    return seeds_data


def download_key(path, key_uri):
    key = request_get_whitout_heade(key_uri)
    key_path = ''.join([path, '/key.key'])
    with open(key_path, 'w', encoding='utf-8') as f:
        f.write(key.decode('utf-8'))
    return key.decode('utf-8')


def request_get_whitout_heade(uri):
    retry = 5
    html = None
    while retry > 0:
        try:
            if PROXY_PRO:
                resp = requests.get(uri, timeout=30, proxies=PROXY_PRO)
            else:
                resp = requests.get(uri, timeout=30)
            if resp.status_code < 300:
                html = resp.content
                break
        except Exception as e:
            print('请求失败,', e)
            time.sleep(5)
        retry -= 1
    return html


if __name__ == '__main__':
    all_m3u8_file()
