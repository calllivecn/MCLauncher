#!/usr/bin/env python3
#coding=utf-8

import os
import sys
import json
import logging
from urllib.parse import urlsplit
from hashlib import md5
from argparse import ArgumentParser
from subprocess import check_call, call
from platform import system


#from pprint import pprint


LAUNCHER = r'MCL'
LAUNCHER_version = r'v1.0'

MC_CONFIG = 'MCLauncher.json'

#LAUNCHER_VERSION = { "21": parser_21 }


#########################
#
#
# 函数定义 start
#
#
#########################

OS_TYPE=system().lower()

ossep = os.sep
pathsep = os.path.pathsep
exists = os.path.exists
isdir = os.path.isdir
abspath = os.path.abspath
dirname = os.path.dirname
pathsplit = os.path.split

def get_json(f):
    with open(f) as fp:
        data = json.load(fp)
    return data

def set_json(obj,f):
    with open(MC_CONFIG,'w') as fp:
         data = json.dump(obj,fp)
    return data

def get_uuid(username):
    uuid = md5()
    uuid.update(username.encode("utf8"))
    return uuid.hexdigest()
    

def get_Duser_home():
    abs_path , _ = pathsplit(abspath(sys.argv[0]))
    return abs_path

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

    def __init__(self,username,uuid,Duser_home):
        
        self.username = username
        self.uuid_and_token = uuid
        self.Duser_home = Duser_home

        # temp
        self.args = ""

        self.abs_gameDir = dirname(abspath(sys.argv[0]))
        self.gameDir = self.abs_gameDir + ossep + self.gameDir

        self.__get_gameDir()
        self.__get_assetsDir()
        self.__get_game_version()

        json_path = self.gameDir + ossep + 'versions' + ossep + self.game_version + ossep + self.game_version + '.json'

        self.mc_jar = self.gameDir + ossep + 'versions' + ossep + self.game_version + ossep + self.game_version + '.jar'
        #print("mc_jar: ", self.mc_jar)

        self.mc_json = get_json(json_path)

        self.mainclass = self.mc_json.get('mainClass')

        # self.__get_Djava_library_path()
        # self.jvm_args = {'Djava_library_path': self.Djava_library_path ,'Duser_home': self.Duser_home }

        self.get_classpath()
        print(self.classpath)

        self.get_jvm_args()

        jvm_other_args=" -Xmx1G -XX:+UseConcMarkSweepGC -XX:-UseAdaptiveSizePolicy -Xmn128M "

        # 从${version}.json里解析
        self.get_game_args()

        self.launcher_cmd = "java" + jvm_other_args + self.jvm_args + ":" + self.mc_jar + " " + self.mainclass + " " + self.minecraft_args
        #self.launcher_cmd = ["java "] + list(self.jvm_args) + list(self.classpath + ":") + list(self.mc_jar) + list(self.mainclass) + list(self.minecraft_args)
        print("-"*100, self.launcher_cmd, "-"*100, sep="\n")

    def launcher(self):
        with open("MCL.sh","w") as f:
            f.write(self.launcher_cmd)

        check_call(self.launcher_cmd,shell=True)



    
    def __get_gameDir(self):
        
        #gamedir = self.Duser_home + ossep + self.gameDir

        if exists(self.gameDir):
            pass
        else:
            print('游戏目录不存在:',self.gameDir)
        
    def __get_game_version(self):
        versions_path = self.gameDir + ossep + 'versions'
        for version in os.listdir(versions_path):
            if isdir(versions_path + ossep + version):
                self.game_version = version # 差多个版本的筛选情况
            else:
                print('没有找到versions目录')
                exit(1)

    def __get_Djava_library_path(self):
        self.Djava_library_path = self.gameDir + ossep + 'versions' + ossep + self.game_version + ossep + self.game_version + '-natives'
        print(self.Djava_library_path,file=sys.stderr)
    
    def __get_assetsDir(self):
        self.assetsDir = self.gameDir + ossep + 'assets'

    #def jvms_for(self, value):
    def __get_arg(self, value):

        arg = value.replace("${","{")

        self.args += arg + " "
        print("-"*100 + "__get_arg() --> ", self.args)

    def get_classpath(self):
    
        def get(tmp):
            url = tmp.get('url')
            size = tmp.get('size')
            sha1 = tmp.get('sha1')
            tmp2 = urlsplit(url).path
            tmp2 = tmp2.replace('/',ossep)
            return tmp2
    
        
        ### 解析 jar 库路径
        jar_path = self.mc_json.get('libraries')
        cp_path = []
        for class_jar_info in jar_path:
            
            # 判断 rules 
            rules = class_jar_info.get('rules')
            if rules is not None:
                rules = rules[0]
                if rules.get('action') == 'allow' and rules.get('os').get('name') == OS_TYPE:
                    pass
                else:
                    continue
            
            # 判断 native
            native = class_jar_info.get('natives')
            if native is not None:
                native_os = native.get(OS_TYPE)
                if native_os is not None:
    
                    download = class_jar_info.get('downloads')
        
                    if download is not None :

                        artifact = download.get('artifact')
                        if artifact is not None:
                            cp_path.append(self.gameDir + ossep + 'libraries' + get(artifact))
                        
                        classifiers = download.get('classifiers')
                        if classifiers is not None:
                            native_os_jar = classifiers.get(native_os)
                            if native_os_jar is not None:
                                cp_path.append( self.gameDir + ossep + 'libraries' + get(native_os_jar))
                        
                else:
                    continue
            else:
            #    continue

                tmp = class_jar_info.get('downloads').get('artifact')

                cp_path.append(self.gameDir + ossep + 'libraries' + get(tmp))
        
        cp=''
        for cp_class in cp_path:
            if exists(cp_class):
                cp += cp_class + pathsep
                #cp = cp + cp_class + pathsep + '\n'
            else:
                print('不存在',cp_class)

        self.classpath = cp.rstrip(':')
        #print("self.classpath -- >");print(self.classpath);exit(0)

    
    def get_game_args(self):

        game_args = ""
        
        try:
            arguments = self.mc_json.get('arguments')
            game_dict = arguments.get('game')
        except KeyError as e:
            print("解析MC json文件出错")
            print("解析argments 或 game时错误")
            raise e
        
        for element in game_dict:

            if isinstance(element, dict):
                rules = element.get("rules")
                values = element.get("value")[0]

                if values == "--demo":
                    continue

                if rules is not None:
                    rule = rules[0]
                    action = rule.get('action')

                    if action is not None and action == "allow":
                        features = rule.get('features')

                        if features is not None:

                            for k in features.keys():
                                if k == "is_demo_user":
                                    continue
                                elif k == "has_custom_resolution":
                                    continue

            elif isinstance(element, str):
            
                if element.startswith("${") and element.endswith("}"):
                    game_args += "{}".format(element.lstrip("$")) + " "
                else:
                    game_args += element + " "

        minecraft_args_build_dict = {'auth_player_name': self.username ,
                    'version_name': LAUNCHER + LAUNCHER_version ,
                    'game_directory': self.gameDir ,
                    'assets_root': self.assetsDir ,
                    'assets_index_name': self.mc_json.get("assetIndex").get('id'),
                    'auth_uuid': self.uuid_and_token ,
                    'auth_access_token': self.uuid_and_token ,
                    'user_type': 'mojang',
                    'version_type': self.mc_json.get('type'),
                    }

        """
        'height': 480 , # height ,
        'width': 800 , # widht 
        }
        """

        #print(mc_args)
        self.minecraft_args = game_args.format(**minecraft_args_build_dict)
        #print("self.mc_args ---> ",self.minecraft_args);exit(0)


    def get_jvm_args(self):
        
        jvm_list = self.mc_json.get("arguments").get("jvm")

        for element in jvm_list:

            print(element,"type(element) -->", type(element))
            if isinstance(element, dict):
                rules = element.get("rules")
                print("jvm rules", rules)

                if rules is not None:
                    rule = rules[0]
                    value = element.get("value")
                    print("每一个value:", value)

                    action = rule.get("action")
                    if action is not None and action == "allow":

                        allow_os = rule.get("os")
                        if allow_os is not None:
                            
                            if allow_os.get("name") == OS_TYPE:
                                # 停时先不管os 版本
                                #  if allow_os.get("verions") == ""
                                for v in value:
                                    self.__get_arg(v)
                            else:
                                continue

                        else:
                            continue
                    else:
                        continue

            if isinstance(element, str):
                self.__get_arg(element)

        print(" jvm_args == self.args -->", self.args)
        
        tmp_dict = {'natives_directory': self.gameDir + ossep + 'versions' + ossep + self.game_version + ossep + self.game_version + '-natives',
        'launcher_name' : LAUNCHER,
        'launcher_version' : LAUNCHER_version,
        'classpath' : self.classpath
        }

        self.jvm_args = self.args.format(**tmp_dict).rstrip(' ')

        self.args = ""
        print("-"*100 + "self.jvm_args --> ", self.jvm_args)


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

    #parse.add_argument()


#########################
#
# 参数解析 argparse end
#
#########################





####### testing data
class args: 
    username = 'test'
    uuid = '73c3632b225043f3b9adfe2387841926'


###### testing 





def main():

    Duser_home = get_Duser_home()
    os.chdir(Duser_home)

    if exists(MC_CONFIG):
        user_data = get_json(MC_CONFIG)
        username = user_data.get('username')
        uuid = user_data.get('uuid')
    else:
        username = args.username
        if args.uuid:
            uuid = get_uuid(username)
        else:
            uuid = __get_uuid()
        user_data = {'username' : username ,'uuid' : uuid}
        set_json(user_data,MC_CONFIG)

    mclauncher = MCL(username,uuid,Duser_home)
    mclauncher.launcher()



if __name__ == "__main__":
    main()
