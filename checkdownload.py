#!/usr/bin/env python3
# coding=utf-8
# date 2019-07-23 12:37:46
# author calllivecn <c-all@qq.com>

__all__ = [
            "get_manifest",
            ]

import os
import shutil
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
    
    # 开始下载 client.jar
    client = downloads.get("client")
    fillpath(mds.client_jar)
    logger.info("下载 client: {}".format(mds.client_jar))

    if path.exists(mds.client_jar):
        logger.info("{} 已存在 ... 跳过".format(mds.client_jar))
    else:
        wget(client.get("url"), mds.client_jar)

    # 开始下载 server.jar
    server = downloads.get("server")
    fillpath(mds.server_jar)
    logger.info("下载 server: {}".format(mds.server_jar))

    if path.exists(mds.server_jar):
        logger.info("{} 已存在 ... 跳过".format(mds.server_jar))
    else:
        wget(server.get("url"), mds.server_jar)



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


def check_game(export_target=None):

    mds = McDirStruct()

    version_id = select_local(mds.versions)

    mds.version_id(version_id)

    fillpath(mds.client_json)
    if path.exists(mds.client_json):
        logger.info("{} checking ... ".format(mds.client_json))
    else:
        logger.error("{} 不存在？？？".format(mds.client_json))
        sys.exit(1)

    versions_json = get_json(mds.client_json)
    downloads = versions_json.get("downloads")
    
    # 开始下载 client.jar
    client = downloads.get("client")
    fillpath(mds.client_jar)

    if diffsha1(client.get("sha1"), mds.client_jar):
        logger.info("{} ... ok".format(mds.client_jar))
    else:
        logger.info("下载 client : {}".format(mds.client_jar))
        wget(client.get("url"), mds.client_jar)

    # 开始下载 server.jar
    server = downloads.get("server")
    fillpath(mds.server_jar)

    if diffsha1(server.get("sha1"), mds.server_jar):
        logger.info("{} ... ok".format(mds.server_jar))
    else:
        logger.info("check fail 下载 server: {}".format(mds.server_jar))
        wget(server.get("url"), mds.server_jar)



    logger.info("开始检查jars")
    libraries = versions_json.get("libraries")
    for lib in libraries:
        dl = lib.get("downloads")
        artifact = dl.get("artifact")
    
        if artifact is not None:

            urlpath = getcp(artifact)
            realpath = mds.libraries + urlpath

            fillpath(realpath)
            if diffsha1(artifact.get("sha1"), realpath):
                logger.info("{} ... ok".format(realpath))
            else:
                logger.info("check fail 下载: {}".format(realpath))
                get_jars(artifact, realpath)

        # 如需要，下载 natives 文件
        natives = dl.get("classifiers")
        if natives is not None:
            for value in natives.values():

                urlpath = getcp(value)
                realpath = mds.libraries + urlpath

                fillpath(realpath)
                if diffsha1(value.get("sha1"), realpath):
                    logger.info("{} ... ok".format(realpath))
                else:
                    logger.info("check fail 下载: {}".format(realpath))
                    get_jars(value, realpath)
                

    assetindex = versions_json.get("assetIndex")
    assetindex_id = assetindex.get("id")
    
    assetindex_json = assetindex_id + ".json"

    assetindex_realpath = joinpath(mds.indexes, assetindex_json)
    fillpath(assetindex_realpath)
    if path.exists(assetindex_realpath):
        logger.info("{} 已存在。".format(assetindex_realpath))
    else:
        logger.info("{} 不存在。".format(assetindex_realpath))
        sys.exit(1)

    resources = get_json(assetindex_realpath)
    objects = resources.get("objects")

    for v in objects.values():
        hash_value = v.get("hash")
        savepath = joinpath(mds.objects, hash_value[0:2], hash_value)
        fillpath(savepath)
        if diffsha1(hash_value, savepath):
            logger.info("{} ... ok".format(savepath))
        else:
            logger.info("check fail 下载: {}".format(savepath))
            get_resources(v, savepath)

    dler.join()


def copy(fn1, fn2):
    fillpath(fn2)
    shutil.copy(fn1, fn2)


def export_game(directory):

    mds = McDirStruct()

    mds_new = McDirStruct(directory)

    version_id = select_local(mds.versions)

    mds.version_id(version_id)
    mds_new.version_id(version_id)

    logger.info("export: {}".format(mds_new.client_json))
    copy(mds.client_json, mds_new.client_json)

    versions_json = get_json(mds.client_json)
    downloads = versions_json.get("downloads")
    
    # 开始下载 client.jar
    client = downloads.get("client")
    logger.info("export: {}".format(mds_new.client_jar))
    copy(mds.client_jar, mds_new.client_jar)

    # 开始下载 server.jar
    server = downloads.get("server")
    logger.info("export: {}".format(mds_new.server_jar))
    copy(mds.server_jar, mds_new.server_jar)


    logger.info("开始导出jars")
    libraries = versions_json.get("libraries")
    for lib in libraries:
        dl = lib.get("downloads")
        artifact = dl.get("artifact")
    
        if artifact is not None:

            urlpath = getcp(artifact)
            realpath = joinpath(mds.libraries, urlpath)
            realpath_new = joinpath(mds_new.libraries, urlpath)

            logger.info("export: {}".format(realpath_new))
            copy(realpath, realpath_new)

        # 如需要，下载 natives 文件
        natives = dl.get("classifiers")
        if natives is not None:
            for value in natives.values():

                urlpath = getcp(value)
                realpath = joinpath(mds.libraries, urlpath)
                realpath_new = joinpath(mds_new.libraries + urlpath)

                logger.info("export: {}".format(realpath_new))
                copy(realpath, realpath_new)
                

    logger.info("开始导出 asssetIndex.json 资源")
    assetindex = versions_json.get("assetIndex")
    assetindex_id = assetindex.get("id")
    
    assetindex_json = assetindex_id + ".json"

    assetindex_realpath = joinpath(mds.indexes, assetindex_json)
    assetindex_realpath_new = joinpath(mds_new.indexes, assetindex_json)

    logger.info("export: {}".format(assetindex_realpath_new))
    copy(assetindex_realpath, assetindex_realpath_new)
                

    logger.info("开始导出 objects 资源")
    resources = get_json(assetindex_realpath)
    objects = resources.get("objects")

    for v in objects.values():
        hash_value = v.get("hash")
        savepath = joinpath(mds.objects, hash_value[0:2], hash_value)
        savepath_new = joinpath(mds_new.objects, hash_value[0:2], hash_value)

        logger.info("export: {}".format(savepath_new))
        copy(savepath, savepath_new)
                


def main():
    from argparse import ArgumentParser

    parse = ArgumentParser(description='MC下载器',usage='%(prog)s [-v]',epilog='https://www.none.org')

    parse.add_argument("-v", "--verbose", action="count", default=1, help="verbose")

    args = parse.parse_args()

    setLevel(args.verbose)

    install_game()

if __name__ == "__main__":
    main()
