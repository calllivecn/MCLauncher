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
            ]


import sys
import json
from os import path
from hashlib import sha1
from urllib.request import urlopen


from logs import logger




#########################
#
# URL resources define
#
#########################

VERSION_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
RESOURCES_OBJECTS = "https://resources.download.minecraft.net/" # + hash_val[0:2] + "/" + hash_val


def get_json(f):
    with open(f) as fp:
        data = json.load(fp)
    return data

def set_json(obj,f):
    with open(MC_CONFIG,'w') as fp:
         data = json.dump(obj,fp)
    return data

def get_uuid(username):
    uuid = md5()
    uuid.update(username.encode("utf8"))
    return uuid.hexdigest()

def get_Duser_home():
    abs_path , _ = path.split(path.abspath(sys.argv[0]))
    return abs_path



def wget(url, savepath):

    data = urlopen(url).read()
    
    with open(savepath, "wb") as f:
        f.write(data)

    sha = sha1()
    sha.update(data)

    return sha.hexdigest()


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
            return

def get_jars():
    pass

# test
if __name__ == "__main__":

    import sys

    wget(sys.argv[1], sys.argv[2])


