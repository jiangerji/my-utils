#encoding=utf-8
from __future__ import unicode_literals
import sys
import os
import sqlite3
import zlib

"""
统计每个包名下有多少个异常信息
select PackageName, count(1) from exceptions where PackageName in (select PackageName from exceptions group by PackageName) group by PackageName
"""

reload(sys)
sys.setdefaultencoding('utf-8')

ROOT_DIR = "yxzj"

DB_NAME = "exception.sqlite3"

dbConn = sqlite3.connect(os.path.join(ROOT_DIR, DB_NAME))

COMPRESS = False

def _parserLogFile(filename):
    """
    解析异常日志
    目前有两种格式
    游戏名/包名/版本号/时间戳.txt
    比如王者之剑/com.lk.wzzj.nd/1.0/1398090301192.txt
    """
    filename = os.path.abspath(filename)
    print "parse...", filename
    Timestamp = os.path.splitext(os.path.basename(filename))[0]
    print "  Timestamp:", Timestamp

    parDir = os.path.dirname(filename)
    temp = os.path.basename(parDir)
    InstallId = ""
    GameVersion = None
    if temp.find(".") > -1:
        GameVersion = temp
        print "  GameVersion:", GameVersion
    else:
        # 是install id
        InstallId = temp
        print "  InstallId:", InstallId

    if GameVersion == None:
        parDir = os.path.dirname(parDir)
        GameVersion = os.path.basename(parDir)
        print "  GameVersion:", GameVersion

    parDir = os.path.dirname(parDir)
    PackageName = os.path.basename(parDir)
    print "  PackageName:", PackageName

    parDir = os.path.dirname(parDir)
    GameName = os.path.basename(parDir)
    print "  GameName:", GameName

    # 开始读取日志
    infos = {}
    count = 0
    ExceptionDetail = ""
    NativeCrash = False

    quota = 8
    if len(InstallId) > 3:
        quota = 9

    for line in open(filename).xreadlines():
        if count > quota:
            ExceptionDetail += line
            continue

        index = line.find("=")
        if index > -1:
            if count == quota:
                # 如果为Native Crash
                if infos["CrashReason"].find("Native") > -1:
                    ExceptionDetail += line[index+1:-1]
                    NativeCrash = True
                else:
                    infos["CrashReason"] = line[index+1:-1]
                    ExceptionDetail += infos["CrashReason"] + "\n"
            else:
                key = line[0:index]
                value = line[index+1:-1]
                infos[key] = value
                # print " ",key, value, count

            count += 1

    ExceptionShortMessage = infos["CrashReason"]
    print "  ExceptionShortMessage:", ExceptionShortMessage
    Platform = "android"
    print "  Platform:", Platform
    OSVersion = infos["PhoneOs"]
    print "  OSVersion:", OSVersion
    DeviceType = infos["PhoneModel"]
    print "  DeviceType:", DeviceType
    DeviceId = InstallId
    print "  DeviceId:", DeviceId

    # print "  ExceptionDetail:", ExceptionDetail
    if COMPRESS:
        ExceptionDetail = compress(ExceptionDetail)
    print 

    # 开始插入数据库
    command = "INSERT INTO exceptions (GameName,PackageName,GameVersion,ExceptionShortMessage,Timestamp,Platform,OSVersion,DeviceType,DeviceId,ExceptionDetail) VALUES (?,?,?,?,?,?,?,?,?,?)"
    dbConn.execute(command, (GameName, PackageName, GameVersion, ExceptionShortMessage, Timestamp, Platform, OSVersion, DeviceType, DeviceId, ExceptionDetail))

"""
GameName, PackageName, GameVersion, ExceptionShortMessage, Timestamp, 
Platform, OSVersion, DeviceType, DeviceId, ExceptionDetail
"""

def createDB():
    print "create database..."
    cmd = 'CREATE TABLE IF NOT EXISTS exceptions (_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE DEFAULT 1, GameName VARCHAR NOT NULL , PackageName VARCHAR NOT NULL , GameVersion VARCHAR, ExceptionShortMessage TEXT NOT NULL , Timestamp DATETIME, Platform VARCHAR NOT NULL , OSVersion VARCHAR, DeviceType VARCHAR, DeviceId VARCHAR, ExceptionDetail VARCHAR NOT NULL )'
    dbConn.execute(cmd)
    dbConn.commit()
    print "create database successful!"


# 传入游戏的日志目录
def parseFolder(foldername):
    if not os.path.isdir(foldername):
        print "error:", foldername, "is not folder!"
        return
    for (root, dirs, files) in os.walk(foldername):
        for f in files:
            if f.endswith(".txt"):
                tFile = os.path.join(root, f)
                try:
                    _parserLogFile(tFile)
                except Exception, name:
                    print "Parse Log File Exception:", name
                    print


def compress(message):
    """
    对传入message字符串进行压缩
    """
    compressed = zlib.compress(message)
    print "    Compress rate:", float(len(message))/len(compressed)
    return compressed

def decompress(message):
    """
    对传入message字符串进行解压缩
    """
    decompressed = zlib.decompress(message)
    return decompressed

# def queryAll():


if __name__=="__main__":
    printLog = True
    if len(sys.argv) > 2:
        printLog = False
        COMPRESS = True

    import codecs
    import time
    logFile = codecs.open(ROOT_DIR+os.path.sep+"ParserExceptionLog_" + time.strftime('%Y-%m-%d_%H-%M-%S')+".log", "w", "utf-8")

    oldStdout = sys.stdout
    if printLog:
        sys.stdout = logFile

    createDB()
    parseFolder(ROOT_DIR)
    dbConn.commit()
    dbConn.close()

    logFile.close()  
    if oldStdout:  
        sys.stdout = oldStdout 
