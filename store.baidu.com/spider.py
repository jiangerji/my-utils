#encoding=utf-8
from __future__ import unicode_literals
import json
import sys
import sqlite3
import os
import httplib
import time

from productInfo import ProductInfo

reload(sys)
sys.setdefaultencoding('utf-8')


def parseProductList(content):
    result = []

    all = json.loads(content)
    error_code = all.get("error_code")
    error_msg = all.get("error_msg")
    if error_code == 0:
        # 获取成功
        data = all.get("data")
        product_list = data.get("list")
        for product in product_list:
            product_info = ProductInfo(product)
            result.append(product_info)
    else:
        # 获取失败
        print "获取产品列表失败，", error_msg

    return result


def getProductListByHot():
    """
    http://store.baidu.com/product/api/recommendList?cat_id=0&orderBy=hot&order=desc&pn=1&limit=36
    """
    db = sqlite3.connect("store.sqlite")

    try:
        CREATE_COMMAND = 'CREATE  TABLE  IF NOT EXISTS "productsInfo" ("product_id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "product_name" TEXT, "product_title" TEXT, "product_intro" TEXT, "comment_count" INTEGER DEFAULT 0, "like_count" INTEGER DEFAULT 0, "product_cover_img" TEXT, "eval_num" INTEGER DEFAULT 0, "product_create_time" TEXT, "product_modified_time" TEXT, "product_price" FLOAT DEFAULT -1, "star_level" INTEGER DEFAULT 0, "product_uname" TEXT, "product_uid" TEXT, "islike" BOOL DEFAULT 0, "evaluation_count" INTEGER, "adjust_score" INTEGER DEFAULT 0, "product_thumbnail" TEXT)'
        db.execute(CREATE_COMMAND)

        INSERT_COMMAND = "insert into productsInfo values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        # for i in range(1, 8):
        #     fp = open(str(i), "r")
        #     for i in parseProductList(fp.read()):
        #         try:
        #             db.execute(INSERT_COMMAND, i.toTuple())
        #         except Exception, e:
        #             print "insert product info exception:", e
        index = 1
        conn = httplib.HTTPConnection("store.baidu.com")
        while True:
            conn.request("GET", "/product/api/recommendList?cat_id=0&orderBy=hot&order=desc&pn=%d&limit=36"%index)
            response = conn.getresponse()
            if response.status:
                pl = parseProductList(response.read())

                for p in pl:
                    try:
                        # db.execute(INSERT_COMMAND, p.toTuple())
                        pass
                    except Exception, e:
                        print "insert product info exception:", e

                    p.downloadImg()

                if len(pl) < 36:
                    break
                index += 1
                time.sleep(1)

    except Exception, e:
        print "create productsInfo table exception:", e

    db.commit()

# getProductListByHot()        

# fp = open("1", "r")
# for i in parseProductList(fp.read()):
#     print i

if __name__ == "__main__":
    #http://store.baidu.com/product/api/recommendList?cat_id=0&orderBy=hot&order=desc&pn=1&limit=36
    # conn = httplib.HTTPConnection("store.baidu.com")
    # conn.request("GET", "/product/api/recommendList?cat_id=0&orderBy=hot&order=desc&pn=1&limit=36")
    # r1 = conn.getresponse()
    # print r1.status, r1.reason
    # data1 = r1.read()
    # print data1
    getProductListByHot()
    














