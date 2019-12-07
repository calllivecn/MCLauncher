#!/usr/bin/env python3
# coding=utf-8
# date 2019-07-23 09:34:01
# author calllivecn <c-all@qq.com>


__all__ = [
            "LAUNCHER",
            "LAUNCHER_VERSION",
            "GAME_CONFIG",
            "OSTYPE",
            "McDirStruct",

            # 常量
            "VERSION_MANIFEST",
            "RESOURCES_OBJECTS",
            ]


import os
import sys
from os import path
from platform import system #, process


from logs import logger


LAUNCHER = "MCL"
LAUNCHER_VERSION = "v1.0"


VERSION_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
RESOURCES_OBJECTS = "https://resources.download.minecraft.net/" # + hash_val[0:2] + "/" + hash_val

GAME_CONFIG = "MCLauncher.json"

OSTYPE = system().lower()
#ARCH = process()


class McDirStruct:
    """
    1. mds = McDirSDtruct()
    2. 选择游戏：mds.version_id() 安装游戏：mds.version_id("1.14.4")
    3. 使用 mds ...
    """

    def __init__(self, minecraft=".minecraft"):

        self.absGameDir = path.dirname(path.abspath(sys.argv[0]))
        self.gameDir = self.absGameDir + os.sep + minecraft

        self.Duser_home = self.absGameDir

        self.assets = self.gameDir + os.sep + "assets"
        self.indexes = self.assets + os.sep + "indexes"
        self.objects = self.assets + os.sep + "objects"

        self.libraries = self.gameDir + os.sep + "libraries"
        
        self.versions = self.gameDir + os.sep + "versions"

        

    # 选择 version_id 后才能 self.client_jar self.client_json self.assetindex
    def version_id(self, version_id=None):
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
                self.version_id = vers[0]
                logger.info("选择版本：{}".format(self.version_id))

                self.client_jar = self.versions + os.sep + self.version_id + os.sep + self.version_id + ".jar"

                self.client_json = self.versions + os.sep + self.version_id + os.sep + self.version_id + ".json"

                self.server_jar = self.gameDir + os.sep + "server-" + self.version_id + ".jar"
            
        else:
            
            self.version_id = version_id

            self.client_jar = self.versions + os.sep + self.version_id + os.sep + self.version_id + ".jar"

            self.client_json = self.versions + os.sep + self.version_id + os.sep + self.version_id + ".json"

            self.server_jar = self.gameDir + os.sep + "server-" + self.version_id + ".jar"

        
    def mk_dir_struct(self, version_id):
        
        for d in [self.gameDir, self.assets, self.indexes, self.objects, self.libraries, self.versions, self.version_id]:
        
            try:
                os.mkdir(d)
            except FileExistsError:
                continue 
