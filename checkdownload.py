#!/usr/bin/env python3
# coding=utf-8
# date 2019-07-23 12:37:46
# author calllivecn <c-all@qq.com>

__all__ = [
            "downloadall",
            ]


from launcher import MCL
from logs import logger
from initconfig import *
from funcs import *


def get_manifest():
    logger.debug("下载：{}".format(VERSION_MANIFEST))
    manifest = wget(VERSION_MANIFEST)
    return get_json(manifest.read())

def downloadall(mds):
    pass

def install_game():
    mds = McDirStruct()

    manifest_json = install_select(get_manifest())

    version_id = manifest_json.get("id")

    mds.version_id(version_id)

    fillpath(mds.client_json)
    wget(manifest_json.get("url"), mds.client_json)

    version_json = get_json(mds.client_json)
    for 

