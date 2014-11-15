#encoding=utf-8
from __future__ import unicode_literals

from DownloadManager import *

class ProductInfo:

    def _init(self):
        self.product_id = -1
        self.product_name = ""
        self.product_title = ""
        self.product_intro = ""
        self.comment_count = 0
        self.like_count = 0
        self.product_cover_img = ""
        self.eval_num = 0
        self.product_create_time = ""
        self.product_modified_time = ""
        self.product_thumbnail = []
        self.product_price = ""
        self.star_level = ""
        self.product_uname = ""
        self.product_uid = ""
        self.islike = False
        self.evaluation_count = 0
        self.adjust_score = 0

    def __str__(self):
        result = []
        result.append("Product Info:")
        result.append("  product id: %s"%str(self.product_id))
        result.append("  product name: %s"%str(self.product_name))
        result.append("  product title: %s"%str(self.product_title))
        result.append("  product intro: %s"%str(self.product_intro))
        result.append("  comment count: %s"%str(self.comment_count))
        result.append("  like count: %s"%str(self.like_count))
        result.append("  product cover img: %s"%str(self.product_cover_img))
        result.append("  eval num: %s"%str(self.eval_num))
        result.append("  product create time: %s"%str(self.product_create_time))
        result.append("  product modified time: %s"%str(self.product_modified_time))
        result.append("  product price: %s"%str(self.product_price))
        result.append("  star level: %s"%str(self.star_level))
        result.append("  product uname: %s"%str(self.product_uname))
        result.append("  product uid: %s"%str(self.product_uid))
        result.append("  is like: %s"%str(self.islike))
        result.append("  evaluation count: %s"%str(self.evaluation_count))
        result.append("  adjust score: %s"%str(self.adjust_score))
        result.append("  product thumbnail:")
        for i in self.product_thumbnail:
            result.append("    %s"%str(i))

        return "\n".join(result)

    def __init__(self, infos):
        # infos is a dict
        if type(infos) != type({}):
            self._init()
            return
        self.product_id = infos.get("product_id", -1)
        self.product_name = infos.get("product_name", "")
        self.product_title = infos.get("product_title", "")
        self.product_intro = infos.get("product_intro", "")
        self.comment_count = infos.get("comment_count", 0)
        self.like_count = infos.get("like_count", 0)
        self.product_cover_img = infos.get("product_cover_img", "")
        self.eval_num = infos.get("eval_num", 0)
        self.product_create_time = infos.get("product_create_time", "")
        self.product_modified_time = infos.get("product_modified_time", "")
        self.product_price = infos.get("product_price", -1)
        self.star_level = infos.get("star_level", "")
        self.product_uname = infos.get("product_uname", "")
        self.product_uid = infos.get("product_uid", 0)
        self.islike = infos.get("islike", False)
        self.evaluation_count = infos.get("evaluation_count", 0)
        self.adjust_score = infos.get("adjust_score", 0)
        self.product_thumbnail = infos.get("product_thumbnail", [])

    def downloadImg(self):
        print "开始下载", self.product_name
        if len(self.product_cover_img) > 0:
            downloadFile(self.product_cover_img, str(self.product_id))

        for i in self.product_thumbnail:
            downloadFile(i, str(self.product_id))

    def toTuple(self):
        return (
            self.product_id, 
            self.product_name, 
            self.product_title, 
            self.product_intro, 
            self.comment_count,
            self.like_count,
            self.product_cover_img,
            self.eval_num,
            self.product_create_time,
            self.product_modified_time,
            self.product_price,
            self.star_level,
            self.product_uname,
            self.product_uid,
            self.islike,
            self.evaluation_count,
            self.adjust_score,
            str(self.product_thumbnail))


if __name__ == "__main__":
    p = ProductInfo(None)
    print p.toTuple()