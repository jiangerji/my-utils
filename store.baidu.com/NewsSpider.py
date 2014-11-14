#encoding=utf-8
from __future__ import unicode_literals
import json
import sys
import sqlite3
import os
import httplib
import time


"""
pn: 获取页数
limit: 每页的数量
_: 当前的时间
"""
BASE_URL_FORMAT = "http://store.baidu.com/news/api/list?pn=1&limit=10&_=1415932708709"

class NewsInfo:

    def __init__(self, infos):
        self.id = infos.get("id", 0)
        self.create_time = infos.get("create_time", "")
        self.title = infos.get("title", 0)
        self.excerpt = infos.get("excerpt", 0)
        self.status = infos.get("status", 0)
        self.comment_status = infos.get("comment_status", 0)
        self.thumbnails = infos.get("thumbnails", 0)
        self.source = infos.get("source", 0)
        self.cat_id = infos.get("cat_id", 0)
        self.comment_count = infos.get("comment_count", 0)
        self.like_count = infos.get("like_count", 0)
        self.weights = infos.get("weights", 0)

    def __str__(self):
        result = []
        result.append("News Info:")
        result.append("  news id: %s"%str(self.id))
        result.append("  new title: %s"%str(self.title))
        result.append("  new excerpt: %s"%str(self.excerpt))
        result.append("  create_time: %s"%str(self.create_time))
        result.append("  status: %s"%str(self.status))
        result.append("  comment_status: %s"%str(self.comment_status))
        result.append("  thumbnails: %s"%str(self.thumbnails))
        result.append("  source: %s"%str(self.source))
        result.append("  cat_id: %s"%str(self.cat_id))
        result.append("  comment_count: %s"%str(self.comment_count))
        result.append("  like_count: %s"%str(self.like_count))
        result.append("  weights: %s"%str(self.weights))

        return "\n".join(result)

    def toTuple(self):
        return (
            self.id, 
            self.create_time,
            self.title, 
            self.excerpt, 
            self.status,
            self.comment_status,
            self.thumbnails,
            self.source,
            self.cat_id,
            self.comment_count,
            self.like_count,
            self.weights)

def parseNewsList(content):
    global index

    result = []

    all = json.loads(content)
    error_code = all.get("error_code")
    error_msg = all.get("error_msg")
    if error_code == 0:
        # 获取成功
        data = all.get("data")
        news_list = data.get("list")
        for news in news_list:
            news_info = NewsInfo(news)
            result.append(news_info)
    else:
        # 获取失败
        print "获取新闻列表失败，", error_msg

    return result

from utils import *
def news_spider():
    # conn = httplib.HTTPConnection("54.64.105.44")
    # # conn.request('get', '/news/api/list?pn=1&limit=10&_='+str(int(time.time()*100)))
    # # http://store.baidu.com/product/api/recommendList?cat_id=0&orderBy=hot&order=desc&pn=1&limit=36
    # conn.request('get', "/wanketv/live/games")
    # response = conn.getresponse()

    # print response.status
    # if response.status == 200:
    #     # parseNewsList(response.read())
    #     print response.read()
    # conn.close()
    quota = 100

    db = sqlite3.connect("store.sqlite")

    try:
        CREATE_COMMAND = 'CREATE  TABLE  IF NOT EXISTS "news" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "create_time" TEXT, "title" TEXT, "excerpt" TEXT, "status" INTEGER, "comment_status" INTEGER, "thumbnails" TEXT, "source" TEXT, "cat_id" INTEGER, "comment_count" INTEGER, "like_count" INTEGER, "weights" INTEGER)'
        db.execute(CREATE_COMMAND)

        INSERT_COMMAND = "insert into news values (?,?,?,?,?,?,?,?,?,?,?,?)"
        index = 1
        url_format = "http://store.baidu.com/news/api/list?pn=%%d&limit=%d&_=%%s"%quota
        while True:
            url = url_format%(index, str(int(time.time()*100)))

            try:
                news_list = parseNewsList(requestUrlContent(url))

                for news in news_list:
                    try:
                        db.execute(INSERT_COMMAND, news.toTuple())
                    except Exception, e:
                        print "insert product info exception:", e

                print "handle", len(news_list)
                if len(news_list) < quota:
                    break
            except Exception, e:
                print "Handle", url, "exception", e

            index += 1

            time.sleep(1)

    except Exception, e:
        print e

    db.commit()
    db.close()

if __name__ == "__main__":
    news_spider()
    print str(int(time.time()*100))