#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:43:10
# author calllivecn <c-all@qq.com>


__all__ = [
            "get_json",
            "set_json",
            "get_uuid",
            "get_Duser_home",
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
from functools import partial


from initconfig import *
from logs import logger


BLOCK = 1<<14 # 16k

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


def fillpath(realpath):
    dirpath, _ = path.dirname(realpath)
    if path.isdir(dirpath):
        os.makedirs(dirpaht)

def wget(url, savepath):
    block = 1<<14 # 16k
    response = urlopen(url)

    sha = sha1()
    
    with open(savepath, "wb") as f:
        for data in iter(partial(response.read, block), b""):
            f.write(data)
            sha.update(data)

    return sha.hexdigest()


def sha1(filename):
    sha = sha1()
    with open(filename) as f:
        for data in iter(partial(f.read, BLOCK), b""):
            sha.update(data)
    
    return sha.hexdigest()


def select(l):
    l_len = len(l)
    
    while True:
        user_select = input("请选择版本序号0-{} 或者查看snaphost版输入s：")
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

    snaphost_list = []
    release_list = []
    for info in versions:
        type_ = info.get("type")
        if type_ == "snapshot" or type_ == "release":
            snaphost_list.append(info.get("id"))
        elif type_ == "release":
            release_list.append(info.get("id"))

    release = True
    while True:
        if release:
            i = 0
            for info in release_list:
                print("{}: {}".format(i, info.get("id")))

            id_ = select(release_list)

            if id_ == "s" 
                release = False
                continue
            elif id_ == "r":
                release = True
                continue

            return release_list[id_]

        else:
            i = 0
            for info in snaphost_list:
                print("{}: {}".format(i, info.get("id")))

            id_ = select(snaphost_list)

            if id_ == "s" 
                release = False
                continue
            elif id_ == "r":
                release = True
                continue

            return snaphost_list[id_]


def get_resources(assets_obj, mc_obj):
    hash_value = mc_obj.get("hash")
    size = mc_obj.get("size")

    url = RESOURCES_OBJECTS + hash_value[0:2] + "/" + hash_value
    savepath = assets_obj + ossep + hash_value[0:2] + ossep + hash_value

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
        sha1 = wget(url, savepath)
        
        if sha1 != sha1_value:
            logger.warn("下载 {} sha1错误，重试 {}/3".format(savepath, i))
        else:
            logger.info("下载 {} 完成。".format(savepath))
            break


# test
if __name__ == "__main__":

    print("sha = ", wget(sys.argv[1], sys.argv[2]))
    


