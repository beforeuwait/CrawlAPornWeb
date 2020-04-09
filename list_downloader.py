# coding=utf-8


import time
import requests
from lxml import etree
from config import URL_HOST, HEADERS_LIST, CATEGORY, PROXY_PRO


def get_each_category_list():
    for each in CATEGORY:
        downloader_saver(each)


def downloader_saver(seed):
    link, title, count = seed
    num = 1
    while num <= count:
        print(title, '共{}页'.format(count), '当前下载第{}页\n'.format(num))
        resp = request_get(link, num)
        data = parse_html(resp)
        with open('./list/{}_list.csv'.format(title), 'a', encoding='utf-8') as f:
            for each in data:
                f.write('\u0001'.join([each[0], ''.join([URL_HOST, each[1]]), '\n']))
        num += 1
        time.sleep(1)


def parse_html(html):
    data = []
    selector = etree.HTML(html)
    for each in selector.xpath('//div[@class="item "]'):
        path = each.xpath('a/@href')[0].replace('detail', 'conter')
        title = each.xpath('a/@title')[0]
        data.append((title, path))
    return data


def request_get(link, num):
    url = ''.join([URL_HOST, link.format(num)])
    retry = 5
    html = None
    while retry > 0:
        try:
            if PROXY_PRO:
                resp = requests.get(url, headers=HEADERS_LIST, proxies=PROXY_PRO, timeout=30)
            else:
                # 没有代理的情况
                resp = requests.get(url, headers=HEADERS_LIST, timeout=30)
            if resp.status_code < 300:
                html = resp.content.decode('utf-8')
                break
        except Exception as e:
            print('请求出错', e)
            time.sleep(5)
        retry -= 1
    return html


if __name__ == '__main__':
    get_each_category_list()
