#!/usr/bin/env python3
# coding=utf-8
# date 2019-07-23 12:37:46
# author calllivecn <calllivecn@outlook.com>

__all__ = [
            "get_manifest",
            ]

import sys
import json
import shutil
from os import path
from pathlib import Path

# from launcher import MCL
from logs import logger, setLevel
from initconfig import VERSION_MANIFEST, McDirStruct  # Add other required names explicitly
from funcs import (
    dler,
    http2_get,
    http2_download,
    install_select,
    fillpath,
    get_json,
    getcp,
    get_jars,
    diffsha1,
    get_resources,
    select_local,
)


def get_manifest():
    logger.debug(f"下载：{VERSION_MANIFEST}")
    manifest = http2_get(VERSION_MANIFEST)
    return json.loads(manifest)


def install_game():
    mds = McDirStruct()

    manifest_json = install_select(get_manifest())

    version_id = manifest_json["id"]

    mds.select_version_id(version_id)

    fillpath(mds.client_json)
    if mds.client_json.exists():
        logger.info(f"{mds.client_json} 已存在 ... 跳过")
    else:
        http2_download(manifest_json["url"], mds.client_json)

    versions_json = get_json(mds.client_json)

    downloads = versions_json["downloads"]
    
    # 开始下载 client.jar
    client = downloads["client"]
    fillpath(mds.client_jar)
    logger.info(f"下载 client: {mds.client_jar}")

    if mds.client_jar.exists():
        logger.info("{} 已存在 ... 跳过".format(mds.client_jar))
    else:
        dler.submit((client.get("url"), mds.client_jar))

    # 开始下载 server.jar
    server = downloads["server"]
    fillpath(mds.server_jar)
    logger.info("下载 server: {}".format(mds.server_jar))

    if path.exists(mds.server_jar):
        logger.info("{} 已存在 ... 跳过".format(mds.server_jar))
    else:
        dler.submit((server.get("url"), mds.server_jar))



    logger.info("开始下载jars")
    for lib in versions_json["libraries"]:
        dl = lib["downloads"]
        artifact = dl["artifact"]
    
        if artifact is not None:

            urlpath = getcp(artifact)
            realpath = mds.libraries / urlpath

            logger.debug(f"下载 jar: {mds.libraries=} {realpath=}")
            fillpath(realpath)
            if realpath.exists():
                logger.info(f"{realpath} 已存在 ... 跳过")
            else:
                get_jars(artifact, realpath)

        # 如需要，下载natives 文件
        natives = dl.get("classifiers")
        if natives is not None:
            for value in natives.values():

                urlpath = getcp(value)
                realpath = mds.libraries / urlpath

                fillpath(realpath)
                if realpath.exists():
                    logger.info(f"{realpath} 已存在 ... 跳过")
                else:
                    get_jars(value, realpath)
                

    assetindex = versions_json["assetIndex"]

    # 每个本版 assetindex.json 文个都不一样，要分名保存。
    assetindex_id = assetindex["id"]
    assetindex_json = assetindex_id + ".json"

    assetindex_realpath = mds.indexes / assetindex_json
    fillpath(assetindex_realpath)
    src_sha1 = assetindex["sha1"]
    if assetindex_realpath.exists() and diffsha1(src_sha1, assetindex_realpath):
        logger.info(f"{assetindex_realpath} 已存在, check sha1")
    else:
        logger.info(f"下载 assetindex: {assetindex_realpath}")
        http2_download(assetindex["url"], assetindex_realpath)

    resources = get_json(assetindex_realpath)
    objects = resources["objects"]

    for v in objects.values():
        hash_value = v.get("hash")
        savepath = mds.objects.joinpath(hash_value[0:2], hash_value)
        fillpath(savepath)
        if savepath.exists():
            logger.info(f"{savepath} 已存在。")
        else:
            get_resources(v, savepath)

    dler.join()


def check_game(export_target=None):

    mds = McDirStruct()

    version_id = select_local(mds.versions)

    mds.select_version_id(version_id)

    fillpath(mds.client_json)
    if mds.client_json.exists():
        logger.info(f"{mds.client_json} checking ... ")
    else:
        logger.error(f"{mds.client_json} 不存在？？？")
        sys.exit(1)

    versions_json = get_json(mds.client_json)
    downloads = versions_json["downloads"]
    
    # 开始下载 client.jar
    client = downloads["client"]
    fillpath(mds.client_jar)

    if diffsha1(client.get("sha1"), mds.client_jar):
        logger.info(f"{mds.client_jar} ... ok")
    else:
        logger.info(f"下载 client : {mds.client_jar}")
        dler.submit((client.get("url"), mds.client_jar))

    # 开始下载 server.jar
    server = downloads["server"]
    fillpath(mds.server_jar)

    if diffsha1(server.get("sha1"), mds.server_jar):
        logger.info(f"{mds.server_jar} ... ok")
    else:
        logger.info("check fail 下载 server: {}".format(mds.server_jar))
        dler.submit((server.get("url"), mds.server_jar))



    logger.info("开始检查jars")
    libraries = versions_json["libraries"]
    for lib in libraries:
        dl = lib.get("downloads")
        artifact = dl.get("artifact")
    
        if artifact is not None:

            urlpath = getcp(artifact)
            realpath = mds.libraries / urlpath

            fillpath(realpath)
            if diffsha1(artifact.get("sha1"), realpath):
                logger.info(f"{realpath} ... ok")
            else:
                logger.info(f"check fail 下载: {realpath}")
                get_jars(artifact, realpath)

        # 如需要，下载 natives 文件
        natives = dl.get("classifiers")
        if natives is not None:
            for value in natives.values():

                urlpath = getcp(value)
                realpath = mds.libraries / urlpath

                fillpath(realpath)
                if diffsha1(value.get("sha1"), realpath):
                    logger.info(f"{realpath} ... ok")
                else:
                    logger.info(f"check fail 下载: {realpath}")
                    get_jars(value, realpath)
                

    assetindex = versions_json["assetIndex"]
    # 每个本版 assetindex.json 文个都不一样，要分名保存。
    assetindex_id = assetindex["id"]
    assetindex_json = assetindex_id + ".json"

    assetindex_realpath = mds.indexes / assetindex_json
    fillpath(assetindex_realpath)
    value = assetindex.get("sha1")
    if path.exists(assetindex_realpath) and diffsha1(value, assetindex_realpath):
        logger.info(f"{assetindex_realpath} ... ok")
    else:
        logger.info(f"check fail 下载: {assetindex_realpath}")
        dler.submit((assetindex.get("url"), assetindex_realpath))


    resources = get_json(assetindex_realpath)
    objects = resources["objects"]

    for v in objects.values():
        hash_value = v.get("hash")
        savepath = mds.objects.joinpath(hash_value[0:2], hash_value)
        fillpath(savepath)
        if diffsha1(hash_value, savepath):
            logger.info(f"{savepath} ... ok")
        else:
            logger.info(f"check fail 下载: {savepath}")
            get_resources(v, savepath)

    dler.join()


def copy(fn1, fn2):
    if path.exists(fn2):
        logger.info(f"{fn2} 已存在 ...")
    else:
        fillpath(fn2)
        shutil.copy(fn1, fn2)


def export_game(directory: str):

    mds = McDirStruct()

    mds_new = McDirStruct(Path(directory))

    version_id = select_local(mds.versions)

    mds.select_version_id(version_id)
    mds_new.select_version_id(version_id)

    logger.info(f"export: {mds_new.client_json}")
    copy(mds.client_json, mds_new.client_json)

    versions_json = get_json(mds.client_json)
    
    logger.info(f"export: {mds_new.client_jar}")
    copy(mds.client_jar, mds_new.client_jar)

    logger.info(f"export: {mds_new.server_jar}")
    copy(mds.server_jar, mds_new.server_jar)


    logger.info("开始导出jars")
    libraries = versions_json["libraries"]
    for lib in libraries:
        dl = lib.get("downloads")
        artifact = dl.get("artifact")
    
        if artifact is not None:

            urlpath = getcp(artifact)
            realpath = mds.libraries / urlpath
            realpath_new = mds_new.libraries / urlpath

            logger.info(f"export: {realpath_new}")
            copy(realpath, realpath_new)

        # 如需要，下载 natives 文件
        natives = dl.get("classifiers")
        if natives is not None:
            for value in natives.values():

                urlpath = getcp(value)
                realpath = mds.libraries / urlpath
                realpath_new = mds_new.libraries / urlpath

                logger.info(f"export: {realpath_new}")
                copy(realpath, realpath_new)
                

    logger.info("开始导出 asssetIndex.json 资源")
    assetindex = versions_json["assetIndex"]
    # 每个本版 assetindex.json 文个都不一样，要分名保存。
    assetindex_id = assetindex["id"]
    assetindex_json = assetindex_id + ".json"

    assetindex_realpath = mds.indexes / assetindex_json
    assetindex_realpath_new = mds_new.indexes / assetindex_json

    logger.info(f"export: {assetindex_realpath_new}")
    copy(assetindex_realpath, assetindex_realpath_new)


    logger.info("开始导出 objects 资源")
    resources = get_json(assetindex_realpath)
    objects = resources["objects"]

    for v in objects.values():
        hash_value = v["hash"]
        savepath = mds.objects.joinpath(hash_value[0:2], hash_value)
        savepath_new = mds_new.objects.joinpath(hash_value[0:2], hash_value)

        logger.info(f"export: {savepath_new}")
        copy(savepath, savepath_new)
    
    # 把自身也复制过去
    shutil.copy(sys.argv[0], mds_new.absGameDir)



def main():
    from argparse import ArgumentParser

    parse = ArgumentParser(description='MC下载器',usage='%(prog)s [-v]',epilog='https://www.none.org')

    parse.add_argument("-v", "--verbose", action="count", default=1, help="verbose")

    args = parse.parse_args()

    setLevel(args.verbose)

    install_game()

if __name__ == "__main__":
    main()
