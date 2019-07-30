#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:43:10
# author calllivecn <c-all@qq.com>


__all__ = [
            "loads_json",
            "get_json",
            "set_json",
            "get_uuid",
            "get_Duser_home",
            "getcp",
            "wget",
            "fillpath",
            "get_resources",
            "get_jars",
            "dler",
            "sha1",
            "install_select",
            ]


import os
import sys
import json
import socket
from os import path
from hashlib import md5, sha1
from urllib import request
from urllib.parse import urlsplit
from functools import partial
from threading import Thread
from queue import Queue


from initconfig import *
from logs import logger


BLOCK = 1<<14 # 16k


def loads_json(f):
    return json.loads(f)

def get_json(f):
    with open(f) as fp:
        data = json.load(fp)
    return data

def set_json(obj,f):
    with open(GAME_CONFIG,'w') as fp:
         data = json.dump(obj, fp, ensure_ascii=False, indent=4)
    return data

def get_uuid(username):
    uuid = md5()
    uuid.update(username.encode("utf8"))
    return uuid.hexdigest()

def get_Duser_home():
    abs_path , _ = path.split(path.abspath(sys.argv[0]))
    return abs_path

def getcp(obj):
    url = obj.get("url")
    size = obj.get("size")
    realpath = urlsplit(url).path
    tmp = realpath.replace("/", os.sep)
    return tmp


def fillpath(realpath):
    dirpath = path.dirname(realpath)
    if not path.isdir(dirpath):
        os.makedirs(dirpath)


def wget(url, savepath):
    block = 1<<14 # 16k

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    req = request.Request(url, headers=headers)
    response = request.urlopen(req, timeout=15)

    sha = sha1()
    
    with open(savepath, "wb") as f:
        for data in iter(partial(response.read, block), b""):
            f.write(data)
            sha.update(data)

    return sha.hexdigest()


class Downloader:
    """
    多线程http下载器
    """
    def __init__(self, worker=20):

        self.taskqueue = Queue(100)

        self.threads = []

        self.func

        self.count = 0

        logger.debug("启动下载线程：")
        for _ in range(worker):

            th = Thread(target=self.func, daemon=True)
            logger.debug("线程：{}".format(th.name))
            th.start()
            self.threads.append(th)


    def submit(self, task):
        logger.debug("提交任务：{}".format(task))
        self.count += 1
        self.taskqueue.put(task)
            
    def func(self):

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
        
        while True:

            url, savepath = self.taskqueue.get()

            block = 1<<14 # 16k
            try:
                req = request.Request(url, headers=headers)
                response = request.urlopen(req, timeout=15)
    
                with open(savepath, "wb") as f:
                    for data in iter(partial(response.read, block), b""):
                        f.write(data)
            except socket.timeout:
                logger.warn("下载超时：{}".format(url))
                continue

            finally:
                response.close()
                self.taskqueue.task_done()
                self.count -= 1
                logger.info("下载 {} 完成。".format(savepath))
                logger.debug("当前队列线程数：{}".format(self.count))


    def join(self):
        logger.debug("join 下载队列。")
        self.taskqueue.join()


dler = Downloader()


def sha1sum(filename):
    sha = sha1()
    with open(filename) as f:
        for data in iter(partial(f.read, BLOCK), b""):
            sha.update(data)
    
    return sha.hexdigest()


def get_resources(mc_obj, savepath):
    hash_value = mc_obj.get("hash")
    size = mc_obj.get("size")

    url = RESOURCES_OBJECTS + hash_value[0:2] + "/" + hash_value

    logger.info("开始下载 {} 。。。".format(savepath))
    dler.submit((url, savepath))

def get_jars(jar_obj, savepath):
    sha1_value = jar_obj.get("sha1")
    url = jar_obj.get("url")
    size = jar_obj.get("size")

    logger.info("开始下载 {} 。。。".format(savepath))
    dler.submit((url, savepath))
        


def select(l):
    l_len = len(l)
    
    while True:
        print("输入s切换快照版和正式版，输入q退出")
        user_select = input("请选择版本序号 0-{}: [已选择:{}] ".format(l_len - 1, l_len - 1))

        if user_select == "":
            return l_len - 1

        if user_select == "q":
            sys.exit(0)

        try:
            number = int(user_select)
        except ValueError:
            if user_select == "s":
                return user_select
            else:
                print("请正确输入！")
                continue

        if l_len < number < 0:
            print("请正确输入！")
            continue

        return number

# version_manifest alias vm
def install_select(vm):
    latest = vm.get("latest")
    versions = vm.get("versions")

    #logger.debug("version_manifest: {}".format(versions))

    versions.reverse()
    snapshot_list = []
    release_list = []
    for info in versions:
        type_ = info.get("type")
        logger.debug("遍历游戏版本: {}, type: {}".format(info, type_))
        if type_ == "snapshot":
            logger.debug("加入snapshot list:{}".format(info))
            snapshot_list.append(info)
        elif type_ == "release":
            logger.debug("加入release list:{}".format(info))
            release_list.append(info)
            snapshot_list.append(info)

    release = True
    while True:
        if release:
            i = 0
            for info in release_list:
                print("{}: {}".format(i, info.get("id")))
                i += 1

            id_ = select(release_list)

            if id_ == "s":
                if release:
                    release = False
                    continue
                else:
                    release = True
                    continue

            return release_list[id_]

        else:
            i = 0
            for info in snapshot_list:
                print("{}: {}".format(i, info.get("id")))
                i += 1

            id_ = select(snapshot_list)

            if id_ == "s":
                if release:
                    release = False
                    continue
                else:
                    release = True
                    continue

            return snapshot_list[id_]



# test
if __name__ == "__main__":

    print("sha = ", wget(sys.argv[1], sys.argv[2]))
    


