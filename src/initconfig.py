#!/usr/bin/env python3
# coding=utf-8
# date 2019-07-23 09:34:01
# author calllivecn <calllivecn@outlook.com>


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
from pathlib import Path
from platform import system #, process


from logs import logger

LAUNCHER = "MCL"
LAUNCHER_VERSION = "v1.8.5"

VERSION_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
RESOURCES_OBJECTS = "https://resources.download.minecraft.net/" # + hash_val[0:2] + "/" + hash_val

# sys.argv[0] 所在目录
program = Path(sys.argv[0]).parent

GAME_CONFIG = program / "MCLauncher.json"
CONF = program / ".mcl"

if not CONF.exists():
    CONF.mkdir()


OSTYPE = system().lower()


class McDirStruct:
    """
    1. mds = McDirSDtruct()
    2. 选择游戏：mds.version_id() 安装游戏：mds.version_id("1.14.4")
    3. 使用 mds ...
    """

    def __init__(self, minecraft: Path|None =None):
        """
        :param minecraft: Minecraft 目录，默认为当前工作目录。
        """

        if minecraft is None:
            self.absGameDir = Path(os.getcwd()) # 当前工作目录
        else:
            minecraft_path = minecraft
            if minecraft_path.is_dir():
                self.absGameDir = minecraft_path.absolute()
            else:
                print(f"{minecraft_path} 目录不存在！")
                sys.exit(1)
        
        self.gameDir = self.absGameDir / ".minecraft"
        self.serverDir = self.absGameDir / "server"

        self.Duser_home = self.absGameDir

        self.assets = self.gameDir / "assets"
        self.indexes = self.assets / "indexes"
        self.objects = self.assets / "objects"

        self.libraries = self.gameDir / "libraries"
        
        self.versions = self.gameDir / "versions"

        

    # 选择 version_id 后才能 self.client_jar self.client_json self.assetindex
    def select_version_id(self, version_id: str| None =None):
        """
        param: version_id 默认为None, version_id 为非None 时为创建MC 目录构造。
        """

        if version_id is None:
            vers = os.listdir(self.versions)
            if len(vers) == 0:
                logger.error("{} 没有游戏。".format(self.gameDir))
                sys.exit(1)

            elif version_id not in vers:
                logger.warning("选择的游戏版本不存在")
                sys.exit(1)

            else:
                logger.info(f"当前版本：{vers}")
                vers.sort()
                self.version_id = vers[-1]
                logger.info(f"默认选择版本：{self.version_id}")

                self.client_jar = self.versions.joinpath(self.version_id, self.version_id + ".jar")

                self.client_json = self.versions.joinpath(self.version_id, self.version_id + ".json")

                self.server_jar = self.serverDir.joinpath("server-" + self.version_id + ".jar")
            
        else:
            
            self.version_id = version_id

            self.client_jar = self.versions.joinpath(self.version_id, self.version_id + ".jar")

            self.client_json = self.versions.joinpath(self.version_id, self.version_id + ".json")

            self.server_jar = self.serverDir.joinpath("server-" + self.version_id + ".jar")

        
