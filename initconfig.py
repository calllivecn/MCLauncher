#!/usr/bin/env python3
# coding=utf-8
# date 2019-07-23 09:34:01
# author calllivecn <c-all@qq.com>


__all__ = [
            "LAUNCHER",
            "LAUNCHER_VERSION",
            "GAME_CONFIG",
            "CONF",
            "OSTYPE",
            "McDirStruct",

            # 常量
            "VERSION_MANIFEST",
            "RESOURCES_OBJECTS",
            ]


import os
import sys
from os import path
from pathlib import Path
from platform import system #, process


from funcs import joinpath
from logs import logger


LAUNCHER = "MCL"
LAUNCHER_VERSION = "v1.5"


VERSION_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
RESOURCES_OBJECTS = "https://resources.download.minecraft.net/" # + hash_val[0:2] + "/" + hash_val

GAME_CONFIG = Path("MCLauncher.json")
CONF = Path("conf")

OSTYPE = system().lower()
#ARCH = process()


class McDirStruct:
    """
    1. mds = McDirSDtruct()
    2. 选择游戏：mds.version_id() 安装游戏：mds.version_id("1.14.4")
    3. 使用 mds ...
    """

    def __init__(self, minecraft=None):

        if minecraft is None:
            self.absGameDir = os.getcwd()
        else:
            if path.isdir(minecraft):
                self.absGameDir = path.abspath(minecraft)
            else:
                print("{} 目录不存在！".format(minecraft))
                sys.exit(1)
        
        self.gameDir = joinpath(self.absGameDir, ".minecraft")
        self.serverDir = joinpath(self.absGameDir, "server")

        self.Duser_home = self.absGameDir

        self.assets = joinpath(self.gameDir, "assets")
        self.indexes = joinpath(self.assets, "indexes")
        self.objects = joinpath(self.assets, "objects")

        self.libraries = joinpath(self.gameDir, "libraries")
        
        self.versions = joinpath(self.gameDir, "versions")

        

    # 选择 version_id 后才能 self.client_jar self.client_json self.assetindex
    def select_version_id(self, version_id=None):
        """
        param: version_id 默认为None, version_id 为非None 时为创建MC 目录构造。
        """

        if version_id is None:
            vers = os.listdir(self.versions)

            if len(vers) == 0:
                logger.error("{} 没有游戏。".format(self.gameDir))
                sys.exit(1)
            else:
                logger.info("当前版本：{}".format(vers))
                vers.sort()
                self.version_id = vers[-1]
                logger.info("默认选择版本：{}".format(self.version_id))

                self.client_jar = joinpath(self.versions, self.version_id, self.version_id + ".jar")

                self.client_json = joinpath(self.versions, self.version_id, self.version_id + ".json")

                self.server_jar = joinpath(self.serverDir, "server-" + self.version_id + ".jar")
            
        else:
            
            self.version_id = version_id

            self.client_jar = joinpath(self.versions, self.version_id, self.version_id + ".jar")

            self.client_json = joinpath(self.versions, self.version_id, self.version_id + ".json")

            self.server_jar = joinpath(self.serverDir, "server-" + self.version_id + ".jar")

        
    def mk_dir_struct(self, version_id):
        
        for d in [self.gameDir, self.serverDir, self.assets, self.indexes, self.objects, self.libraries, self.versions, self.version_id]:
        
            try:
                os.mkdir(d)
            except FileExistsError:
                continue 
