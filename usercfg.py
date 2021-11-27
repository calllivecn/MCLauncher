#!/usr/bin/env python3
#coding=utf-8
# date 2021-07-19 19:36:37
# author calllivecn <c-all@qq.com>



import os
import sys
from pathlib import Path


from logs import logger
from initconfig import CONF, GAME_CONFIG
from auth import MicrosoftAuthorized
from funcs import (
    get_json,
    get_uuid,
    select_local,
    set_json,
    DotDict,
    get_dotdict,
    set_dotdict,
)



class UserCFG:

    def __init__(self, args):

        # 切换正版用户
        if args.username and args.online:

            self.loadcfg()

            user_conf = CONF / (args.username + ".json")

            if user_conf.exists():
                account = MicrosoftAuthorized(args.username)
            else:
                logger.info("添加一个正版用户")
                account = MicrosoftAuthorized()

            self.username, self.uuid, self.accesstoken = account.user()

            self.online = True

        # 添加正版用户
        elif args.username is None and args.online:
            self.loadcfg()

            logger.info("添加一个正版用户")
            account = MicrosoftAuthorized()
            self.username, self.uuid, self.accesstoken = account.user()

            self.online = True
        
        # 切换为一个离线用户
        elif args.username and not args.online:
            self.loadcfg()

            self.username = args.username
            self.uuid = get_uuid(self.username)
            self.accesstoken = self.uuid

            self.online = False
        
        # 使用配置文件
        else:

            if not GAME_CONFIG.exists():
                logger.error("首次启动需要设置一个游戏用户名！")
                logger.error("使用--username添加一个离线账号(同时也是MC角色用户名！)")
                logger.error("或者使用--online添加一个微软账号(正版账号)")
                sys.exit(1)

            self.loadcfg()

            if self.online:
                account = MicrosoftAuthorized(self.username)
                self.username, self.uuid, self.accesstoken = account.user()

        self._v = None

        # 是否更新配置
        self.UPDATE_CFG = False

        if args.username:
            self.UPDATE_CFG = True

        
        if GAME_CONFIG.exists():
            if args.java_path:
                self.UPDATE_CFG = True
                self.java_path = args.java_path
        else:
            self.java_path = "java"

        if GAME_CONFIG.exists():
            if args.jvm_args:
                self.UPDATE_CFG = True
                self.jvm_args = args.jvm_args
        else:
            self.jvm_args = "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M"
        
        if GAME_CONFIG.exists():
            if args.resolution:
                self.UPDATE_CFG = True
                self.resolution = args.resolution
    
    def loadcfg(self):
        if GAME_CONFIG.exists():
            try:
                self.user_data = get_dotdict(GAME_CONFIG)

                self.username = self.user_data['username']
                self.uuid = self.user_data['uuid']
                self.accesstoken = self.user_data["accesstoken"]
                self.currentversion = self.user_data['currentversion']
                self.java_path = self.user_data['java-path']
                self.jvm_args = self.user_data['jvm-args']
                self.online = self.user_data['online']

                if self.user_data.resolution:
                    self.resolution = self.user_data.resolution

            except KeyError:
                logger.error("{} 配置文件格式错误！已清理，请重新启动".format(GAME_CONFIG))
                os.remove(GAME_CONFIG)
                sys.exit(1)
                # 解析出错 End


    @property
    def currentversion(self):
        return self._v
    
    @currentversion.setter
    def currentversion(self, v):
        self.UPDATE_CFG = True
        self._v = v

    @property
    def online(self):
        return self._online
    
    @online.setter
    def online(self, online):
        self.UPDATE_CFG = True
        self._online = online


    def set_cfg(self):
        self.user_data = DotDict()
        self.user_data['username'] = self.username
        self.user_data['uuid'] = self.uuid
        self.user_data['accesstoken'] = self.accesstoken
        self.user_data['currentversion'] = self.currentversion
        self.user_data['java-path'] = self.java_path
        self.user_data['jvm-args'] = self.jvm_args
        self.user_data["online"] = self.online

        if self.resolution:
            self.user_data['resolution'] = self.resolution

        # 如果有更新，就保存
        if self.UPDATE_CFG:
            logger.debug(f"更新配置: {self.user_data}")
            set_dotdict(self.user_data, GAME_CONFIG)
    
