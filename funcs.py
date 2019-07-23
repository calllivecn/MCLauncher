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
            "sha1",
            "install_select",
            ]


import os
import sys
import json
from os import path
from hashlib import md5, sha1
from urllib.request import urlopen
from urllib.parse import urlsplit
from functools import partial


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
         data = json.dump(obj,fp)
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
    response = urlopen(url)

    sha = sha1()
    
    with open(savepath, "wb") as f:
        for data in iter(partial(response.read, block), b""):
            f.write(data)
            sha.update(data)

    return sha.hexdigest()


def sha1sum(filename):
    sha = sha1()
    with open(filename) as f:
        for data in iter(partial(f.read, BLOCK), b""):
            sha.update(data)
    
    return sha.hexdigest()


def select(l):
    l_len = len(l)
    
    while True:
        user_select = input("请选择版本序号0-{} 或者查看snaphost版输入s：[已选择:{}]".format(l_len, l_len-1))
        if user_select == "":
            return l_len - 1

        try:
            number = int(user_select)
        except ValueError:
            if user_select == "s" or user_select == "r":
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
                release = False
                continue
            elif id_ == "r":
                release = True
                continue

            return release_list[id_]

        else:
            i = 0
            for info in snapshot_list:
                print("{}: {}".format(i, info.get("id")))
                i += 1

            id_ = select(snapshotlist)

            if id_ == "s":
                release = False
                continue
            elif id_ == "r":
                release = True
                continue

            return snapshot_list[id_]


def get_resources(mc_obj, savepath):
    hash_value = mc_obj.get("hash")
    size = mc_obj.get("size")

    url = RESOURCES_OBJECTS + hash_value[0:2] + "/" + hash_value

    for i in range(1, 3 + 1):

        wget_hash_value = wget(url, savepath)

        if wget_hash_value != hash_value:
            logger.warn("下载 {} sha1错误，重试 {}/3".format(savepath, i))
        else:
            logger.info("下载 {} 完成。".format(savepath))
            break

def get_jars(jar_obj, savepath):
    sha1_value = jar_obj.get("sha1")
    url = jar_obj.get("url")
    size = jar_obj.get("size")

    for i in range(1, 3 + 1):

        sha = wget(url, savepath)
        
        if sha != sha1_value:
            logger.warn("下载 {} sha1错误，重试 {}/3".format(savepath, i))
        else:
            logger.info("下载 {} 完成。".format(savepath))
            break


# test
if __name__ == "__main__":

    print("sha = ", wget(sys.argv[1], sys.argv[2]))
    


