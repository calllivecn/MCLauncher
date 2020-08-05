#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 22:55:53
# author calllivecn <c-all@qq.com>



import os
import sys
import pprint
import atexit
from os import path
from shutil import rmtree
from hashlib import md5
from zipfile import ZipFile
from subprocess import run, CalledProcessError
from platform import system


from funcs import *
from initconfig import *
from logs import logger


#########################
#
#
# 函数定义 start
#
#
#########################


class MCL:
    Djava_library_path = ''

    jvm_args = ''
    cp_args = ''
    minecraft_args = ''

    def __init__(self, username, uuid, mds):
        
        self.username = username
        self.uuid_token = uuid
        self.Duser_home = mds.Duser_home
        
        self.mds = mds

        self.gameDir = mds.gameDir
        self.indexes = mds.indexes
        self.objects = mds.objects
        self.libraries = mds.libraries

        self.versions = mds.versions

        self.version_id = mds.version_id
        self.assets = mds.assets

        self.__get_gameDir()

        self.client_jar = mds.client_jar
        self.client_json = mds.client_json

        self.mc_json = get_json(self.client_json)

        self.mainclass = self.mc_json.get('mainClass')

        self.__get_Djava_library_path()

        self.get_classpath()

        self.get_jvm_args()

        jvm_other_args =["-XX:+UseConcMarkSweepGC", "-XX:-UseAdaptiveSizePolicy", "-Xmn256M"]

        # 从${version}.json里解析
        self.get_minecraft_args()

        self.launcher_cmd = ["java"] + jvm_other_args + self.jvm_args + [self.mainclass] + self.minecraft_args

    def launcher(self):
        # 注册清理函数
        atexit.register(self.clear_natives)

        logger.debug("MC Launcher CMD：{}".format(pprint.pformat(self.launcher_cmd)))
        try:
            run(self.launcher_cmd, check=True)
        except CalledProcessError as e:
            logger.error(e)
            sys.exit(1)

    
    def __get_gameDir(self):
        
        if path.exists(self.gameDir):
            pass
        else:
            logger.error('游戏目录不存在: {} 或者 当前没有游戏。'.format(self.gameDir))
            sys.exit(1)
        
    def __get_game_version(self):

        if not path.isdir(self.version_id):
            logger.error('没有找到versions目录')
            sys.exit(1)

    def __get_Djava_library_path(self):
        if self.Djava_library_path == "":
            self.Djava_library_path = joinpath(self.versions, self.version_id + '-natives')
        logger.debug("Djava_libaray_path: {}".format(self.Djava_library_path))
    

    def __unpack_dll(self, realpath, target):

        with ZipFile(realpath) as zf:
            for name in zf.namelist():
                if name.endswith(".so") or name.endswith(".SO") or name.endswith(".dll") or name.endswith(".DLL"):
                    zf.extract(name, target)

    def clear_natives(self):
        rmtree(self.natives_dll_path)

    def get_classpath(self):
    
        ### 解析 jar 库路径
        jar_path = self.mc_json.get('libraries')
        cp_path = []
        for class_jar_info in jar_path:
            
            # 判断 rules 
            rules = class_jar_info.get('rules')

            if rules is not None:
                for rule in rules:
                    
                    action = rule.get('action')
                    if action == 'allow':

                        os_ = rule.get('os')
                        if os_ is None:
                            allow = True
                        else:
                            ostype = os_.get('name')
                            if ostype == OSTYPE:
                                allow = True
                            else:
                                allow = False

                    elif action == 'disallow':
                        os_ = rule.get('os')
                        if os_ is None:
                            allow = True
                        else:
                            ostype = os_.get('name')
                            if ostype == OSTYPE:
                                allow = False
                            else:
                                allow = True

                if allow:

                    downloads = class_jar_info.get('downloads')
                    if downloads is not None:

                        artifact = downloads.get('artifact')
                        if artifact is not None:
                            cp_path.append(self.libraries + getcp(artifact))
                            logger.debug("Class Path 添加: {}".format(getcp(artifact)))
                else:
                    continue
            else:

                downloads = class_jar_info.get('downloads')
                if downloads is not None:

                    artifact = downloads.get('artifact')
                    if artifact is not None:
                        cp_path.append(self.libraries + getcp(artifact))
                        logger.debug("Class Path 添加: {}".format(getcp(artifact)))

            
            # 判断 native
            natives = class_jar_info.get('natives')
            if natives is not None:

                # 如果当前系统需要这个动态库
                if OSTYPE in natives.keys():

                    native_os = natives.get(OSTYPE)
                    if native_os is not None:
                        downloads = class_jar_info.get("downloads")
                        if downloads is not None:

                            # 这里是从jar 包里解压出 .so | dll 动态库
                            classifiers = downloads.get('classifiers')
                            if classifiers is not None:
                                native_dll = classifiers.get(native_os)
                                if native_dll is not None:

                                    jar_dll_realpath = self.libraries + getcp(native_dll)
                                    self.natives_dll_path = joinpath(self.versions, self.version_id, self.version_id + "-natives")

                                    if path.isdir(self.natives_dll_path):
                                        if self.Djava_library_path == '':
                                            self.Djava_library_path = self.natives_dll_path

                                        logger.info("解压natives库：{} --> {}".format(jar_dll_realpath, self.natives_dll_path))
                                        self.__unpack_dll(jar_dll_realpath, self.natives_dll_path)

                                    else:
                                        os.mkdir(self.natives_dll_path)
                                        logger.info("解压natives库：{} --> {}".format(jar_dll_realpath, self.natives_dll_path))
                                        self.__unpack_dll(jar_dll_realpath, self.natives_dll_path)
                        

        cp = ''
        for cp_class in cp_path:
            if path.exists(cp_class):
                cp += cp_class + path.pathsep
            else:
                logger.warning('不存在：{}'.format(cp_class))

        #self.classpath = cp.rstrip(path.pathsep)
        self.classpath = cp
        logger.debug("self.classpath -- >\n{}".format(self.classpath))

    
    def get_minecraft_args(self):

        mc_args = ""
        
        try:
            game_args = self.mc_json.get('arguments')
            value_list = game_args.get('game')
        except KeyError as e:
            logger.error("解析 MC json 文件出错")
            logger.error("解析 argments 或 game 时错误")
            sys.exit(1)
        
        allow = True
        for value in value_list:

            if isinstance(value, dict):
                
                rules = value.get("rules")
                for rule in rules:

                    action = rule.get('action')
                    if action == "allow":

                        features =  rule.get('features')
                        if features is not None:

                            for k in features.keys():
                                if k == "is_demo_user":
                                    allow = False
                                    continue
                                elif k == "has_custom_resolution":
                                    allow = False
                                    continue
                        
                    elif action == "disallow":
                        allow = False
                        continue


            elif isinstance(value, str):
                if value.startswith("${") and value.endswith("}"):
                    value = value.replace('${', '{').replace('}', '}')
                    mc_args += value + " "
                else:
                    mc_args += value + " "

                continue

            else:
                logger.warning("未知 minecraft 参数：{} 尝试忽略。".format(value))
                continue

            # # #############
            
            if allow:
                logger.debug("启用 minecraft 参数：{}。".format(value))
                for option in value.get('value'):

                    if option.startswith("${") and option.endswith("}"):
                        mc_args += "{}".format(option.lstrip("$")) + " "
                    else:
                        mc_args += option + " "
            else:
                logger.debug("不启用 minecraft 参数：{}。".format(value))
                continue

        minecraft_args_build_dict = {'auth_player_name': self.username,
                    'version_name': LAUNCHER + LAUNCHER_VERSION,
                    'game_directory': self.gameDir,
                    'assets_root': self.assets,
                    'assets_index_name': self.mc_json.get('assets'),
                    'auth_uuid': self.uuid_token,
                    'auth_access_token': self.uuid_token,
                    #'user_type': 'mojang',
                    'user_type': 'legacy',
                    'version_type': self.mc_json.get('type'),
                    }

        """
        'height': 480 , # height ,
        'width': 800 , # widht 
        }
        """

        self.minecraft_args = mc_args.format(**minecraft_args_build_dict)
        self.minecraft_args = self.minecraft_args.split()
        logger.debug("mc 启动参数：{}".format(self.minecraft_args))


    def get_jvm_args(self):
        
        jvms = ""

        def jvms_for(value):

            nonlocal jvms

            if isinstance(value, str):
                value = value.replace('${','{') 
                jvms += value.replace('}', '}') + " "

            elif isinstance(value, list):

                for jvm_arg in option_dict.get("value"):
                    jvm_arg = jvm_arg.replace('${', '{')
                    jvms += jvm_arg.replace('}','}') + ""
        
        jvm_list = self.mc_json.get("arguments").get("jvm")

        allow = True
        for option_dict in jvm_list:

            if isinstance(option_dict, dict):

                rules = option_dict.get("rules")
                for rule in rules:

                    action = rule.get("action")
                    if action == "allow":

                        allow_os = rule.get("os")
                        if allow_os is not None:

                            os_name = allow_os.get("name")
                            if os_name is not None:

                                if os_name == OSTYPE:
                                # 停时先不管os 版本
                                #  if allow_os.get("verions") == ""
                                    allow = True
                                else:
                                    allow = False
                            else:
                                allow = False
                        else:
                            allow = False

                    elif action == "disallow":

                        allow_os = rule.get("os")
                        if allow_os is not None:

                            os_name = allow_os.get("name") 
                            if os_name == OSTYPE:
                                allow = False
                            else:
                                allow = True
                        else:
                            allow = False
            else:
                jvms_for(option_dict)
                continue

            if allow:
                jvms_for(option_dict.get("value"))

        
        tmp_dict = {'natives_directory': joinpath(self.versions, self.version_id, self.version_id + '-natives'),
        'launcher_name' : LAUNCHER,
        'launcher_version' : LAUNCHER_VERSION,
        'classpath' : self.classpath + self.client_jar
        }
        logger.debug("jvm 参数(解析前)：{}".format(jvms))
        logger.debug("jvm 参数(解析前) tmp_dirct：{}".format(pprint.pformat(tmp_dict)))
        self.jvm_args = jvms.format(**tmp_dict)
        self.jvm_args = self.jvm_args.split()
        logger.debug("jvm 参数：{}".format(self.jvm_args))


