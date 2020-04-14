# CrawlAPornWeb

爬全站视频，拿到m3u8文件，下载解密合并，转码

**开发完毕**

下载了一部分，已关掉爬虫

因为视频普遍是720p，渣渣

另外每个视频都有菠菜业的水印，渣渣

不过代码继续公开，就当提供思路做好事

## 该项目

偶然发现一个网站，需要翻墙访问，但是发现数据都在国内，视频比较新
然后就萌生采集全站的想法

该网站用的是视频流

因此需要拿到每个视频的 m3u8 文件

然后还原然后下载合并，需要AES解密的还需要解密

## 目录

    .
    ├── README.md
    ├── already_crawl.txt
    ├── config.py
    ├── config_real.py
    ├── list
    │   ├── 4K岛国_list.csv
    │   ├── JAV高清_list.csv
    │   ├── VR资源_list.csv
    │   ├── 丝袜美腿_list.csv
    │   ├── 中文字幕_list.csv
    │   ├── 亚洲情色_list.csv
    │   ├── 人妖人兽_list.csv
    │   ├── 人妻熟女_list.csv
    │   ├── 伦理三级_list.csv
    │   ├── 制服师生_list.csv
    │   ├── 卡通动漫_list.csv
    │   ├── 国产自拍_list.csv
    │   ├── 强奸乱伦_list.csv
    │   ├── 无码专区_list.csv
    │   ├── 欧美性爱_list.csv
    │   ├── 热门女优_list.csv
    │   ├── 男同女同_list.csv
    │   └── 韩国资源_list.csv
    ├── list_downloader.py
    ├── m3u8
    |   ├── 国产自拍
    │   |   ├── 在课前与性爱的小女生发生性关系
    │   │   |   ├── index.m3u8
    │   │   |   ├── url.txt
    ├── m3u8_downloader.py
    ├── video
    ├── video_downloader.py
    └── video_tmp
        └── 国产自拍
            └── 在课前与性爱的小女生发生性关系
                ├── 1.ts
                ├── 2.ts
                └── 3.ts
    

## 启动说明

关于 list 我已经整理好了， 截止 2020/04/14 的

就不用启动 list_downloader.py 去下载列表

首先是下载 m3u8文件

        python3 m3u8_downloader.py

    文件放到 m3u8/ 这个目录
    按照分类存储
    每个视频文件里有两个文件
        index.m3u8 文件
        url.txt 
    对于无效的视频连接，同样会创建目录
    但是在执行完毕时候，会去做筛查，删除没有文件的目录


然后是下载视频流

        python3 video_downloader.py

    tmp文件会放到 video_tmp 里，按照  1.ts 2.ts .....
    这样保存
    下载完毕会自动核验完整性
    如果是完整的就会把 1.ts->n.ts 合并为一个文件
    同时放入 video这个目录，同时删除video_tmp里目录

