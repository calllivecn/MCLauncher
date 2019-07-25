#!/usr/bin/env python3
# coding=utf-8
# date 2019-07-23 12:37:46
# author calllivecn <c-all@qq.com>

__all__ = [
            "downloadall",
            ]

import os
from os import path
from urllib.request import urlopen

from launcher import MCL
from logs import logger, setLevel
from initconfig import *
from funcs import *


def get_manifest():
    logger.debug("下载：{}".format(VERSION_MANIFEST))
    manifest = urlopen(VERSION_MANIFEST)
    return loads_json(manifest.read())

def downloadall(mds):
    pass

def install_game():
    mds = McDirStruct()

    manifest_json = install_select(get_manifest())

    version_id = manifest_json.get("id")

    mds.version_id(version_id)

    fillpath(mds.client_json)
    if path.exists(mds.client_json):
        logger.info("{} 已存在 ... 跳过".format(mds.client_json))
    else:
        wget(manifest_json.get("url"), mds.client_json)

    versions_json = get_json(mds.client_json)

    downloads = versions_json.get("downloads")
    
    client = downloads.get("client")
    fillpath(mds.client_jar)
    logger.info("下载 client: {}".format(mds.client_jar))

    if path.exists(mds.client_jar):
        logger.info("{} 已存在 ... 跳过".format(mds.client_jar))
    else:
        wget(client.get("url"), mds.client_jar)

    logger.info("开始下载jars")
    libraries = versions_json.get("libraries")
    for lib in libraries:
        dl = lib.get("downloads")
        artifact = dl.get("artifact")
    
        if artifact is not None:

            urlpath = getcp(artifact)
            realpath = mds.libraries + urlpath

            fillpath(realpath)
            if path.exists(realpath):
                logger.info("{} 已存在 ... 跳过".format(realpath))
            else:
                get_jars(artifact, realpath)

        # 如需要，下载natives 文件
        natives = dl.get("classifiers")
        if natives is not None:
            for value in natives.values():

                urlpath = getcp(value)
                realpath = mds.libraries + urlpath

                fillpath(realpath)
                if path.exists(realpath):
                    logger.info("{} 已存在 ... 跳过".format(realpath))
                else:
                    get_jars(value, realpath)
                

    assetindex = versions_json.get("assetIndex")
    assetindex_id = assetindex.get("id")
    
    assetindex_json = assetindex_id + ".json"

    assetindex_realpath = mds.indexes + os.sep + assetindex_json
    fillpath(assetindex_realpath)
    if path.exists(assetindex_realpath):
        logger.info("{} 已存在。".format(assetindex_realpath))
    else:
        logger.info("下载 assetindex: {}".format(assetindex_realpath))
        wget(assetindex.get("url"), assetindex_realpath)

    resources = get_json(assetindex_realpath)
    objects = resources.get("objects")

    for v in objects.values():
        hash_value = v.get("hash")
        savepath = mds.objects + os.sep + hash_value[0:2] + os.sep + hash_value
        fillpath(savepath)
        if path.exists(savepath):
            logger.info("{} 已存在。".format(savepath))
        else:
            get_resources(v, savepath)

    dler.join()
        

def ext_main(level):
    setLevel(level)
    install_game()

def main():
    from argparse import ArgumentParser

    parse = ArgumentParser(description='MC下载器',usage='%(prog)s [-v]',epilog='http://www.none.org')

    parse.add_argument("-v", "--verbose", action="count", default=1, help="verbose")

    args = parse.parse_args()

    setLevel(args.verbose)

    install_game()

if __name__ == "__main__":
    main()
