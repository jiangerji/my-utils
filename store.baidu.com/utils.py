#encoding=utf-8
from __future__ import unicode_literals
import os
import hashlib

def md5(source):
    result = hashlib.md5(source.encode('utf-8')).hexdigest()
    return result

def requestUrlContent(url, cache_dir=".cache", filename=None):
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    if filename == None:
        filename = md5(url)

    target_path = os.path.join(".", cache_dir)
    target_path = os.path.join(target_path, filename)
    command = 'wget "%s" -O %s '%(url, target_path)
    state = os.system(command)
    # print state
    return open(target_path).read()

if __name__ == "__main__":
    requestUrlContent("http://store.baidu.com/product/api/recommendList?cat_id=0&orderBy=hot&order=desc&pn=1&limit=36")