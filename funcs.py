#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:43:10
# author calllivecn <c-all@qq.com>


__all__ = (
            "loads_json",
            "get_json",
            "set_json",
            "get_uuid",
            "get_Duser_home",
            "getcp",
            "wget",
            "fillpath",
            "joinpath",
            "get_resources",
            "get_jars",
            "dler",
            "sha1sum",
            "diffsha1",
            "install_select",
            "select_local",
            "DotDict",
            "get_dotdict",
            "set_dotdict",
)


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


from logs import logger


RESOURCES_OBJECTS = "https://resources.download.minecraft.net" # + hash_val[0:2] + "/" + hash_val
USER_AGENT = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}

BLOCK = 1<<14 # 16k


def loads_json(f):
    return json.loads(f)

def get_json(f):
    with open(f) as fp:
        data = json.load(fp)
    return data

def set_json(obj,f):
    with open(f,'w') as fp:
         data = json.dump(obj, fp, ensure_ascii=False, indent=4)
    return data

def get_dotdict(f):
    d = DotDict()
    with open(f) as fp:
        d.load(fp)
    return d

def set_dotdict(d, f):
    with open(f, "w") as fp:
        data = d.dump(fp, ensure_ascii=False, indent=4)
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


def joinpath(*args):
    return os.sep.join(args)

def wget(url, savepath):
    block = 1<<14 # 16k

    # headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    req = request.Request(url, headers=USER_AGENT)
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

        # headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
        
        while True:

            url, savepath = self.taskqueue.get()

            block = 1<<14 # 16k
            try:
                req = request.Request(url, headers=USER_AGENT)
                with request.urlopen(req, timeout=60) as response:
                    with open(savepath, "wb") as f:
                        for data in iter(partial(response.read, block), b""):
                            f.write(data)

            except socket.timeout:
                logger.warning("下载超时：{}".format(url))
                os.remove(savepath)
                self.count += 1
                self.taskqueue.put((url, savepath))
                continue
            except Exception as e:
                logger.error("出错：{}".format(e))
                logger.error("出错url：{}".format(url))
                self.count += 1
                self.taskqueue.put((url, savepath))

            finally:
                # response.close()
                self.taskqueue.task_done()
                self.count -= 1
                logger.info("下载完成：{}".format(savepath))
                logger.debug("当前队列任务数：{}".format(self.count))


    def join(self):
        logger.debug("join 下载队列。")
        self.taskqueue.join()


dler = Downloader()

class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def loads(self, str_byte, *args, **kwargs):
        self.update(json.loads(str_byte, *args, **kwargs, object_hook=self.__d2dd))

    def dumps(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs, default=self.__dd2d)

    def load(self, fp, *args, **kwargs):
        self.update(json.load(fp, *args, **kwargs, object_hook=self.__d2dd))

    def dump(self, fp, *args, **kwargs):
        return json.dump(self, fp, *args, **kwargs, default=self.__dd2d)
    
    @classmethod
    def __d2dd(cls, obj):
        return cls(obj)

    @classmethod
    def __dd2d(cls, obj):

        if isinstance(obj, cls):
            return obj

        return obj

def sha1sum(filename):
    sha = sha1()
    with open(filename, "rb") as f:
        for data in iter(partial(f.read, BLOCK), b""):
            sha.update(data)
    
    return sha.hexdigest()


def diffsha1(sha, filename):
    if path.exists(filename):
        fn_sha = sha1sum(filename)
    else:
        logger.warning("{} 不在 ...".format(filename))
        return False

    if sha == fn_sha:
        return True
    else:
        return False


def get_resources(mc_obj, savepath):
    hash_value = mc_obj.get("hash")
    size = mc_obj.get("size")

    url = "/".join([RESOURCES_OBJECTS, hash_value[0:2], hash_value])

    logger.info("开始下载：{} ...".format(savepath))
    dler.submit((url, savepath))

def get_jars(jar_obj, savepath):
    sha1_value = jar_obj.get("sha1")
    url = jar_obj.get("url")
    size = jar_obj.get("size")

    logger.info("开始下载：{} ...".format(savepath))
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
    latest_release = latest.get("release")
    snapshot_stop = True
    versions = vm.get("versions")

    #logger.debug("version_manifest: {}".format(versions))

    #versions.reverse()
    snapshot_list = []
    release_list = []
    for info in versions:

        if info.get("id") == "1.13":
            break

        type_ = info.get("type")
        logger.debug("遍历游戏版本: {}, type: {}".format(info, type_))
        if type_ == "snapshot" and snapshot_stop:
            logger.debug("加入snapshot list:{}".format(info))
            snapshot_list.append(info)
        elif type_ == "release":

            if info.get("id") == latest_release:
                snapshot_stop = False

            logger.debug("加入release list:{}".format(info))
            release_list.append(info)
            snapshot_list.append(info)


    snapshot_list.reverse()
    release_list.reverse()
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


# def select_local(versions_path, latest=True):
def select_local(versions_path):
    vs = os.listdir(versions_path)
    l_len = len(vs)
    vs.sort()

    for i in range(l_len):
        print("{}: {}".format(i, vs[i]))
    
    while True:
        print("选择一个游戏版本，输入q退出")
        user_select = input("请选择版本序号 0-{}: [已选择:{}] ".format(l_len - 1, l_len - 1))

        if user_select == "":
            return vs[l_len - 1]

        if user_select == "q":
            sys.exit(0)

        try:
            number = int(user_select)
        except ValueError:
            print("请正确输入！")
            continue

        if l_len < number < 0:
            print("请正确输入！")
            continue

        return vs[number]

# test
if __name__ == "__main__":

    print("sha = ", wget(sys.argv[1], sys.argv[2]))

