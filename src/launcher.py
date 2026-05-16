#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 22:55:53
# author calllivecn <calllivecn@outlook.com>



import os
import sys
import time
import shutil
import pprint
import subprocess
import atexit
from pathlib import Path
from string import Template
from urllib import parse
from zipfile import ZipFile



from logs import logger
from funcs import (
    get_json,
    fillpath,
    dler,
    getcp,
    # DotDict,
    get_dotdict,
)
from initconfig import (
    McDirStruct,
    CONF,
    OSTYPE,
    WIN_VERSION,
)

from version import (
    LAUNCHER,
    LAUNCHER_VERSION,
)


#########################
#
#
# 函数定义 start
#
#
#########################


class MCL:


    def __init__(self, username: str, uuid: str, accesstoken: str, mds: McDirStruct, width=None, height=None, debug=False):
        
        self.username = username
        self.uuid = uuid
        self.accesstoken = accesstoken
        self.Duser_home = mds.Duser_home
        
        self.mds = mds

        self.gameDir = mds.gameDir
        self.indexes = mds.indexes
        self.objects = mds.objects
        self.libraries = mds.libraries
        self.versions = mds.versions
        self.version_id = mds.version_id
        self.assets = mds.assets

        if "fabric" in self.version_id:
            self.fabric_init()

        self.client_jar = mds.client_jar
        self.client_json = mds.client_json

        self.Djava_library_path: str = ''

        # 1.21 新更新的
        self.default_user_jvms: list = []

        self.jvm_args: list = []
        self.minecraft_args: list = []
        

        self.height = height
        self.width = width

        self.debug = debug

        self.__get_gameDir()


        # self.mc_json = get_json(self.client_json)
        self.mc_json = get_dotdict(self.client_json)

        self.mainclass = self.mc_json["mainClass"]

        self.timestamp = str(time.time_ns())
        self.__get_Djava_library_path()

        # 从${version}.json里解析
        self.get_game_args()


    def launcher(self):

        if "fabric" in self.version_id:
            self.get_classpath()
            self.fabric()
            self.get_jvm_args()
            self.launcher_cmd = [self.java_path] + self.jvm_customize_args + self.default_user_jvms + self.jvm_args + self.fabric_arguments_jvm + [self.fabric_mainClass] + self.minecraft_args
        else:

            self.get_classpath()
            self.get_jvm_args()

            self.launcher_cmd = [self.java_path] + self.jvm_customize_args + self.default_user_jvms + self.jvm_args + [self.mainclass] + self.minecraft_args

        # 注册清理函数
        atexit.register(self.clear_natives)

        logger.info(f"MC Launcher CMD：{pprint.pformat(self.launcher_cmd)}")

        if self.debug:
            sys.exit(0)

        try:
            subprocess.run(self.launcher_cmd, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(e)
            sys.exit(1)
    
    #  添加 fabric 的支持
    def fabric(self):
        self.jvm_args = [f"-Dminecraft.client.jar={self.client_jar}"] + self.jvm_args
        self.classpath = self.fabric_libraries_cp + self.classpath


    def fabric_init(self):
        self.fabric_version_id = self.version_id
        fabric_json = self.versions.joinpath(self.version_id, self.version_id + ".json")
        self.fabric_json = get_json(fabric_json)

        # 拿到对应的MC client_jar
        self.mds.select_version_id(self.fabric_json["inheritsFrom"])

        self.fabric_mainClass: str = self.fabric_json["mainClass"]
        self.fabric_arguments_jvm: list[str] = self.fabric_json["arguments"]["jvm"]

        self.fabric_libraries_cp = []
        # 解析 fabric_libraries 
        self.fabric_libraries = self.fabric_json["libraries"]
        for lib in self.fabric_libraries:
            libpath, libname, libversion = lib["name"].split(":")
            libpath = libpath.replace(".", os.sep)
            cp = self.libraries.joinpath(libpath, libname, libversion, libname + "-" + libversion + ".jar")
            if cp.exists():
                self.fabric_libraries_cp.append(cp)
            else:
                # "https://maven.fabricmc.net/net/fabricmc/tiny-mappings-parser/0.3.0%2Bbuild.17/tiny-mappings-parser-0.3.0%2Bbuild.17.jar"
                # 创建目录。。。哎，麻烦。
                fillpath(cp)

                url = lib["url"] + parse.quote("/".join([libpath, libname, libversion, libname + "-" + libversion + ".jar"]))
                logger.warning(f"fabric libraries {cp} not exists... download:{url}")
                dler.submit((url, cp))
                self.fabric_libraries_cp.append(cp)
                # sys.exit(1)
    

    def set_java_path(self, java_path: str):
        self.java_path = java_path

    def set_jvm_customize_args(self, jvm_customize_args: str):
        self.jvm_customize_args = jvm_customize_args.split()
    

    def __get_gameDir(self):
        
        if self.gameDir.exists():
            pass
        else:
            logger.error(f"游戏目录不存在: {self.gameDir} 或者 当前没有游戏。")
            sys.exit(1)
        

    def __get_Djava_library_path(self):
        if self.Djava_library_path == "": 
            self.Djava_library_path = CONF.joinpath(self.version_id + '-natives-' + self.timestamp)
            self.Djava_library_path.mkdir()
        logger.debug(f"Djava_libaray_path: {self.Djava_library_path}")
    

    def __unpack_dll(self, realpath, target):

        with ZipFile(realpath) as zf:
            for name in zf.namelist():
                if name.endswith(".so") or name.endswith(".SO") or name.endswith(".dll") or name.endswith(".DLL"):
                    zf.extract(name, target)


    def clear_natives(self):
        """
        2024-12-25
        windows 下，清理时，进程退出后，*.dll库可以还没完全释放。
        使用 sleep 方式清理
        """
        for i in range(60):
            try:
                if hasattr(self, "natives_dll_path"):
                    logger.debug(f"清理native库: {self.natives_dll_path}")
                    shutil.rmtree(self.natives_dll_path)

                else:
                    natives_dll_path = CONF.joinpath(self.version_id + "-natives-" + self.timestamp)
                    if natives_dll_path.is_dir():
                        logger.debug(f"(那这是谁解压的？)清理native库: {natives_dll_path}")
                        shutil.rmtree(natives_dll_path)
            except Exception as e:
                logger.warning(f"清理异常：{e}, slee(3)")
                time.sleep(3)


    def get_classpath(self):
    
        ### 解析 jar 库路径
        jar_path = self.mc_json['libraries']
        cp_path: list[Path] = []
        for class_jar_info in jar_path:
            
            allow = True
            # 如果有rules ， 就需要看在什么条件下启用。
            if class_jar_info.rules:
                for rule in class_jar_info.rules:
                    if rule.action == 'allow':
                        if rule.os:
                            if rule.os.name == OSTYPE:
                                allow = True
                            else:
                                allow = False
                        else:
                            allow = True

                    elif rule.action == 'disallow':
                        if rule.so:
                            if rule.os.name == OSTYPE:
                                allow = False
                            else:
                                allow = True
                        else:
                            allow = True

            if allow:
                downloads = class_jar_info.downloads
                if downloads.artifact:
                    cp_path.append(self.libraries / getcp(downloads.artifact))
                    logger.debug(f"Class Path 添加: {getcp(downloads.artifact)}")
            # else:
                # continue

            
            # 判断 native 不知道从那个版开始没有natives了。但是启动器版号还是没变更。
            # 这版开始的？不需要启动器解压动态库了。2025-07-18
            if class_jar_info.natives:

                natives = class_jar_info.natives
                # 如果当前系统需要这个动态库
                if OSTYPE in natives.keys():

                    native_os = natives[OSTYPE]
                    downloads = class_jar_info.downloads

                    # 这里是从jar 包里解压出 .so | dll 动态库
                    if downloads.classifiers:
                        native_dll = downloads.classifiers.get(native_os)
                        if native_dll is not None:

                            jar_dll_realpath = self.libraries / getcp(native_dll)

                            # 这里为什么要看 self.natives_dll_path 存不存在？2021-07-24
                            self.natives_dll_path = CONF.joinpath(self.version_id + "-natives-" + self.timestamp)
                            # print(f"这里是没有执行吗？{self.natives_dll_path}") # 这里没有执行。。。v1.20.2

                            self.natives_dll_path.mkdir(parents=True, exist_ok=True)
                            if self.Djava_library_path == '':
                                self.Djava_library_path = self.natives_dll_path

                            logger.info(f"解压natives库：{jar_dll_realpath} --> {self.natives_dll_path}")
                            self.__unpack_dll(jar_dll_realpath, self.natives_dll_path)


        cp = []
        for cp_class in cp_path:
            if cp_class.exists():
                cp.append(str(cp_class)) # Path --> str
            else:
                logger.warning(f"不存在：{cp_class}")

        self.classpath = cp

    
    def get_game_args(self):

        mc_args = []
        
        try:
            game_args = self.mc_json["arguments"]
            value_list = game_args["game"]
        except KeyError:
            logger.error("解析 MC json 文件出错")
            logger.error("解析 argments 或 game 时错误")
            sys.exit(1)
        
        for value in value_list:
            allow = False # 默认不启用预制参数。

            logger.debug(f"解析 game_ages 参数：{value}")
            if isinstance(value, dict):

                rules = value["rules"]
                logger.debug(f"rules: {rules}")
                for rule in rules:

                    if rule.action == "allow":
                        if rule.features:
                            for k in rule.features.keys():
                                if k == "is_demo_user":
                                    allow = False
                                    continue
                                elif k == "has_custom_resolution":
                                    allow = False
                                    continue
                        
                    elif rule.action == "disallow":
                        allow = False
                        continue

            elif isinstance(value, str):
                if value.startswith("${") and value.endswith("}"):
                    mc_args.append(value)
                else:
                    mc_args.append(value)

                continue

            else:
                logger.warning(f"未知 minecraft 参数：{value} 尝试忽略。")
                continue

            # # #############
            
            if allow:
                logger.debug(f"启用 minecraft 参数：{value}。")
                for option in value["value"]:

                    if option.startswith("${") and option.endswith("}"):
                        mc_args.append(value)
                    else:
                        mc_args.append(value)
            else:
                logger.debug(f"不启用 minecraft 参数：{value}。")
                continue

        minecraft_args_build_dict = {'auth_player_name': self.username,
                    'version_name': LAUNCHER + LAUNCHER_VERSION,
                    'game_directory': self.gameDir,
                    'assets_root': self.assets,
                    'assets_index_name': self.mc_json.get('assets'),
                    'auth_uuid': self.uuid,
                    'auth_access_token': self.accesstoken,
                    'user_type': 'mojang',
                    # 'user_type': 'legacy',
                    'version_type': self.mc_json.get('type'),
                    }
        
        self.minecraft_args = []
        for option in mc_args:
            if option.startswith("${") and option.endswith("}"):
                op = option[2:][:-1]
                if op in minecraft_args_build_dict:
                    self.minecraft_args.append(minecraft_args_build_dict[op])

            elif option.startswith("--"):
                self.minecraft_args.append(option)

        if self.height is not None and self.width is not None:
            self.minecraft_args.append('--height')
            self.minecraft_args.append(self.height) 
            self.minecraft_args.append('--width')
            self.minecraft_args.append(self.width)

        logger.debug(f"mc game 启动参数：{self.minecraft_args}")

    # 1.21 新添加的
    def get_default_user_jvm(self):
        """
        这里的有rules的情况下allow的默认就是disable的，需要在action是allow 时才启用这个参数
        """

        if default_user_jvm_list := self.mc_json["arguments"].get("default-user-jvm"):
            
            for jvm in default_user_jvm_list:

                if rules := jvm.get("rules"):
            
                    for rule in rules:
                        if rule["os"]["name"] == OSTYPE:
                            default_user_jvms += jvm["value"]
            
                else:
                    default_user_jvms += jvm["value"]

        

    def get_jvm_args(self):
        
        jvms = []
        jvm_list = self.mc_json["arguments"]["jvm"]

        allow = False
        for option_dict in jvm_list:

            if isinstance(option_dict, dict):
                if rules := option_dict.get("rules"):

                    for rule in rules:
                        if os_ := rule.get("os"):
                            if os_name := os_.get("name"):
                                if os_name == OSTYPE:
                                    allow = True
                            """
                            有一个概念需要先厘清：
                                在 Mojang 的 version.json 规范中，x86 特指 32 位的 x86 架构，而 64 位的 x86 架构通常会被标记为 x86_64 或 amd64。
                            这一段配置的目的是：
                                在 32 位系统上，由于可用内存地址空间有限，默认的线程栈大小（Stack Size）
                                可能不够游戏高频调用（容易引发 StackOverflowError），所以强制将其放大到 -Xss1M（1 Megabyte）。
                            
                            # 可以不管
                            elif os_ := rule.get("os"):
                                if os_arch := os_.get("arch"):
                                  if os_arch == "x86":
                                      allow = True
                            """

            elif isinstance(option_dict, str):
                jvms.append(option_dict)
                continue

            if allow:
                value = option_dict.get("value")
                if isinstance(value, list):
                    jvms += value

                elif isinstance(value, str):
                    jvms.append(value)
                
                else:
                    logger.warning(f"启用的 jvm 参数， 但不是 list, str。: {value}")
            else:
                logger.debug(f"不启用的 jvm 参数: {option_dict.get("value")}")

        
        tmp_dict = {'natives_directory': str(self.Djava_library_path),
        'launcher_name' : LAUNCHER,
        'launcher_version' : LAUNCHER_VERSION,
        'classpath' : os.pathsep.join([str(cp) for cp in self.classpath]) + os.pathsep + str(self.client_jar)
        }

        self.jvm_args = Template(" ".join(jvms)).safe_substitute(tmp_dict).split()

        logger.debug(f"jvm 参数：{self.jvm_args}")


