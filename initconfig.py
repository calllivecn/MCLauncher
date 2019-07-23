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
            ]


import os
import sys
from os import path
from platform import system #, process


from logs import logger


LAUNCHER = "MCL"
LAUNCHER_VERSION = "v1.0"

GAME_CONFIG = "MCLauncher.json"

OSTYPE = system().lower()
#ARCH = process()


class McDirStruct:

    def __init__(self, minecraft=".minecraft", version_id=None):

        self.absGameDir = path.dirname(path.abspath(sys.argv[0]))
        self.gameDir = self.absGameDir + os.sep + minecraft

        self.Duser_home = self.absGameDir

        self.assets = self.gameDir + os.sep + "assets"
        self.indexes = self.assets + os.sep + "indexes"
        self.objects = self.assets + os.sep + "objects"

        self.libraries = self.gameDir + os.sep + "libraries"
        
        self.versions = self.gameDir + os.sep + "versions"
        
        if version_id is None:
            self.__get_version()
        else:
            self.version_id = version_id

        logger.info("选择版本：{}".format(self.version_id))


        self.client_jar = self.versions + os.sep + self.version_id + os.sep + self.version_id + ".jar"

        self.client_json = self.versions + os.sep + self.version_id + os.sep + self.version_id + ".json"


    def __get_version(self):

        vers = os.listdir(self.versions)

        if len(vers) == 0:
            logger.error("{} 没有游戏。".format(self.gameDir))
            sys.exit(1)
        else:
            logger.info("当前版本：{}".format(vers))
            vers.sort()
            self.version_id = vers[0]
        


