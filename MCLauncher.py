#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 22:55:53
# author calllivecn <c-all@qq.com>


LAUNCHER = r'MCL'
LAUNCHER_version = r'v1.0'

MC_CONFIG = 'MCLauncher.json'

import os
import sys
from os import path
from urllib.parse import urlsplit
from hashlib import md5, sha1
from argparse import ArgumentParser
from zipfile import ZipFile
from subprocess import check_call, call
from platform import system
#from pprint import pprint

from funcs import *
from logs import logger


#########################
#
#
# 函数定义 start
#
#
#########################

OS_TYPE = system().lower()

class MCL:
    username = ''
    abs_gameDir = ''
    gameDir = '.minecraft'
    game_version = '' # __get_game_version()
    json_path = ''

    Djava_library_path = ''

    jvm_args = ''
    cp_args = ''
    minecraft_args = ''

    def __init__(self, username, uuid, Duser_home):
        
        self.username = username
        self.uuid_and_token = uuid
        self.Duser_home = Duser_home

        self.abs_gameDir = path.dirname(path.abspath(sys.argv[0]))
        self.gameDir = self.abs_gameDir + os.sep + self.gameDir

        self.__get_gameDir()
        self.__get_assetsDir()
        self.__get_game_version()

        self.json_path = self.gameDir + os.sep + 'versions' + os.sep + self.game_version + os.sep + self.game_version + '.json'

        self.mc_jar = self.gameDir + os.sep + 'versions' + os.sep + self.game_version + os.sep + self.game_version + '.jar'

        self.mc_json = get_json(self.json_path)

        self.mainclass = self.mc_json.get('mainClass')

        self.__get_Djava_library_path()
        # self.jvm_args = {'Djava_library_path': self.Djava_library_path ,'Duser_home': self.Duser_home }

        self.get_classpath()

        self.get_jvm_args()

        jvm_other_args=" "

        # 从${version}.json里解析
        self.get_minecraft_args()

        self.launcher_cmd = "java" + jvm_other_args + self.jvm_args + ":" + self.mc_jar + " " + self.mainclass + " " + self.minecraft_args
        #self.launcher_cmd = ["java "] + list(self.jvm_args) + list(self.classpath + ":") + list(self.mc_jar) + list(self.mainclass) + list(self.minecraft_args)
        logger.debug("MC Launcher CMD：{}".format(self.launcher_cmd))

    def launcher(self):
        #with open("MCL.sh","w") as f:
        #    f.write(self.launcher_cmd)

        check_call(self.launcher_cmd,shell=True)

    
    def __get_gameDir(self):
        
        #gamedir = self.Duser_home + os.sep + self.gameDir

        if path.exists(self.gameDir):
            pass
        else:
            logger.debug('游戏目录不存在: {}'.format(self.gameDir))
            sys.exit(1)
        
    def __get_game_version(self):

        versions_path = self.gameDir + os.sep + 'versions'

        for version in os.listdir(versions_path):

            if path.isdir(versions_path + os.sep + version):
                self.game_version = version # 差多个版本的筛选情况

            else:

                logger.debug('没有找到versions目录')
                sys.exit(1)

    def __get_Djava_library_path(self):
        if self.Djava_library_path == "":
            self.Djava_library_path = self.gameDir + os.sep + 'versions' + os.sep + self.game_version + os.sep + self.game_version + '-natives'
        logger.debug("Djava_libaray_path: {}".format(self.Djava_library_path))
    
    def __get_assetsDir(self):
        self.assetsDir = self.gameDir + os.sep + 'assets'

    def __unpack_dll(self, realpath, target):

        with ZipFile(realpath) as zf:
            for name in zf.namelist():
                if name.endswith(".so") or name.endswith(".SO") or name.endswith(".dll") or name.endswith(".DLL"):
                    zf.extract(name, target)

    def __getcp(self, tmp):
        url = tmp.get('url')
        size = tmp.get('size')
        sha1 = tmp.get('sha1')
        tmp2 = urlsplit(url).path
        tmp2 = tmp2.replace('/', os.sep)
        return tmp2
    

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
                            if ostype == OS_TYPE:
                                allow = True
                            else:
                                allow = False

                    elif action == 'disallow':
                        os_ = rule.get('os')
                        if os_ is None:
                            allow = True
                        else:
                            ostype = os_.get('name')
                            if ostype == OS_TYPE:
                                allow = False
                            else:
                                allow = True

                if allow:

                    downloads = class_jar_info.get('downloads')
                    if downloads is not None:

                        artifact = downloads.get('artifact')
                        if artifact is not None:
                            cp_path.append(self.gameDir + os.sep + 'libraries' + self.__getcp(artifact))
                            logger.debug("Class Path 添加: {}".format(self.__getcp(artifact)))
                else:
                    continue
            else:

                downloads = class_jar_info.get('downloads')
                if downloads is not None:

                    artifact = downloads.get('artifact')
                    if artifact is not None:
                        cp_path.append(self.gameDir + os.sep + 'libraries' + self.__getcp(artifact))
                        logger.debug("Class Path 添加: {}".format(self.__getcp(artifact)))

            
            # 判断 native
            natives = class_jar_info.get('natives')
            if natives is not None:

                # 如果当前系统需要这个动态库
                if OS_TYPE in natives.keys():

                    native_os = natives.get(OS_TYPE)
                    if native_os is not None:
                        downloads = class_jar_info.get("downloads")
                        if downloads is not None:

                            # 这里是从jar 包里解压出 .so | dll 动态库
                            classifiers = downloads.get('classifiers')
                            if classifiers is not None:
                                native_dll = classifiers.get(native_os)
                                if native_dll is not None:

                                    jar_dll_realpath = self.gameDir + os.sep + 'libraries' + os.sep + self.__getcp(native_dll)
                                    natives_dll_path = self.gameDir + os.sep + 'versions' + os.sep + self.game_version + os.sep + self.game_version + "-natives"

                                    logger.debug("natives_dll -- 解压")
                                    if path.isdir(natives_dll_path):
                                        if self.Djava_library_path == '':
                                            self.Djava_library_path = natives_dll_path

                                        logger.info("解压natives库：{} --> {}".format(jar_dll_realpath, natives_dll_path))
                                        self.__unpack_dll(jar_dll_realpath, natives_dll_path)

                                    else:
                                        os.mkdir(natives_dll_path)
                                        logger.info("解压natives库：{} --> {}".format(jar_dll_realpath, natives_dll_path))
                                        self.__unpack_dll(jar_dll_realpath, natives_dll_path)
                        

                #tmp = class_jar_info.get('downloads').get('artifact')
                #cp_path.append(self.gameDir + os.sep + 'libraries' + self.__getcp(tmp))
        
        cp=''
        for cp_class in cp_path:
            if path.exists(cp_class):
                cp += cp_class + path.pathsep
                #cp = cp + cp_class + path.pathsep + '\n'
                #logger.debug('存在', cp_class)
            else:
                logger.warn('不存在：{}'.format(cp_class))

        self.classpath = cp.rstrip(path.pathsep)
        logger.debug("self.classpath -- >")
        logger.debug(self.classpath)

    
    def get_minecraft_args(self):

        mc_args = ""
        
        try:
            game_args = self.mc_json.get('arguments')
            value_list = game_args.get('game')
        except KeyError as e:
            logger.debug("解析MC json文件出错")
            logger.debug("解析argments 或 game时错误")
            raise e
        
        for value in value_list:
            set_flag = True
            compatibilityRules = value.get("compatibilityRules")
            if compatibilityRules is not None:
                # 从这个list中拿和dict
                for compatibilityRules_dict in compatibilityRules:
                    action = compatibilityRules_dict.get('action')
                    if action is not None and action == "allow":
                        
                        features =  compatibilityRules_dict.get('features')
                        if features is not None:

                            for k in features.keys():
                                if k == "is_demo_user":
                                    set_flag = False
                                    continue
                                elif k == "has_custom_resolution":
                                    set_flag = False
                                    continue
                        
                    else:
                        set_flag = False
                        continue

            # # #############
            
            if set_flag:
                for option in value.get('value'):

                    if option.startswith("${") and option.endswith("}"):
                        mc_args += "{}".format(option.lstrip("$")) + " "
                    else:
                        mc_args += option + " "
            else:
                continue

        minecraft_args_build_dict = {'auth_player_name': self.username ,
                    'version_name': LAUNCHER + LAUNCHER_version ,
                    'game_directory': self.gameDir ,
                    'assets_root': self.assetsDir ,
                    'assets_index_name': self.mc_json.get('assets'),
                    'auth_uuid': self.uuid_and_token ,
                    'auth_access_token': self.uuid_and_token ,
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
        logger.debug("mc 启动参数：{}".format(self.minecraft_args))


    def get_jvm_args(self):
        
        jvms = ''

        def jvms_for(vaule_list):

            nonlocal jvms

            for jvm_arg in option_dict.get("value"):

                jvm_arg = jvm_arg.replace("${","{")

                jvms += jvm_arg + " "

            
        
        jvm_list = self.mc_json.get("arguments").get("jvm")

        for option_dict in jvm_list:

            compatibilityRules = option_dict.get("compatibilityRules")
            if compatibilityRules is not None:
                # 先不管它有没多个 compatibilityRules

                for compatibilityRule in compatibilityRules:

                    action = compatibilityRule.get("action")
                    if action == "allow":

                        allow_os = compatibilityRule.get("os")
                        if allow_os is not None:
                            
                            if allow_os.get("name") == OS_TYPE:
                                # 停时先不管os 版本
                                #  if allow_os.get("verions") == ""
                                jvms_for(option_dict.get("value"))

                    elif action == "disallow":
                        pass

            else:

                jvms_for(option_dict.get("value"))

        
        tmp_dict = {'natives_directory': self.gameDir + os.sep + 'versions' + os.sep + self.game_version + os.sep + self.game_version + '-natives',
        'launcher_name' : LAUNCHER,
        'launcher_version' : LAUNCHER_version,
        'classpath' : self.classpath
        }
        self.jvm_args = jvms.format(**tmp_dict).rstrip(' ')
        logger.debug("jvm 参数：{}".format(self.jvm_args))


#########################
#
#
# 函数定义 end 
#
#
#########################



#########################
#
# 参数解析 argparse start
#
#########################

def parse_args():
    parse = ArgumentParser(description='一个MC启动器',usage=' Using : %(prog)s [-u|--username]',epilog='http://www.none.org')

    parse.add_argument("-u", "--username", action="store", help="MC 游戏用户名")
    
    return parse.parse_args()


#########################
#
# 参数解析 argparse end
#
#########################


###### testing 

def test():

    args = parse_args()

    Duser_home = get_Duser_home()
    os.chdir(Duser_home)

    if path.exists(MC_CONFIG):
        user_data = get_json(MC_CONFIG)
        username = user_data.get('username')
        uuid = user_data.get('uuid')
    else:
        if args.username is None:
            logger.debug("首次启动需要设置一个游戏用户名！")
            sys.exit(1)

        username = args.username
        uuid = get_uuid(username)
        user_data = {'username' : username ,'uuid' : uuid}
        set_json(user_data,MC_CONFIG)

    mclauncher = MCL(username,uuid,Duser_home)
    mclauncher.launcher()


if __name__ == "__main__":
    test()
