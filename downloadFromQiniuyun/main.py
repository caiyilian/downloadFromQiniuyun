# -*- coding: utf-8 -*-
from qiniu import Auth
from qiniu import BucketManager
import requests
import os
import math

access_key = '你的access_key'
secret_key = '你的secret_key'

q = Auth(access_key, secret_key)
bucket = BucketManager(q)
# 空间名字
bucket_name = '你的空间名字'
# 前缀
prefix = None
# 列举条目
limit = 20000
# 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
delimiter = None
# 标记
marker = None


def download_all(save_path):
    """
    args:
        save_path:要保存的本地路径
    return:
        none
    """
    if save_path[-1] == os.sep:
        save_path = save_path[0:-1]

    # 域名
    domain_name = 'http://你的域名'
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
    for i in ret['items']:
        if i['key'] != "class.zip":
            continue
        len_file = i['fsize']
        base_url = domain_name + "/" + i['key']

        # 如果空间有时间戳防盗链或是私有空间，可以调用该方法生成私有链接
        private_url = q.private_download_url(base_url, expires=100)
        r = requests.get(private_url, stream=True)
        batchsSize = 1000000
        batchsNum = math.ceil(i['fsize'] / batchsSize)
        filename = i['key'].split('/')[-1]
        dirname = os.path.dirname(i['key'])
        local_dir = save_path + os.sep + dirname.replace('/', os.sep) + os.sep
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        file = open(local_dir + filename, "wb")
        for i in range(batchsNum):
            print('\r', (i / batchsNum) * 100, "%", end="", flush=True)
            file.write(r.raw.read(1000000))
        file.flush()
        file.close()


download_all("D:/test")
