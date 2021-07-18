#!/usr/bin/env python3
#coding=utf-8
# date 2021-07-19 19:36:37
# author calllivecn <c-all@qq.com>



import os
import sys
from os import path
# from pathlib import Path


from logs import logger
from initconfig import GAME_CONFIG
from funcs import (
    get_json,
    get_uuid,
    select_local,
    set_json,
)



class UserCFG:

    def __init__(self, args):

        if path.exists(GAME_CONFIG):
            try:
                user_data = get_json(GAME_CONFIG)
                self.username = user_data['username']
                self.uuid = user_data['uuid']
                self.currentversion = user_data['currentversion']
                self.java_path = user_data['java-path']
                self.jvm_args = user_data['jvm-args']

            except KeyError:
                logger.warning("{} 配置文件格式错误! 请重新启动".format(GAME_CONFIG))
                os.remove(GAME_CONFIG)
                sys.exit(1)

            self.user_data = user_data

        else:
            if args.username is None:
                logger.error("首次启动需要设置一个游戏用户名！")
                sys.exit(1)

        # 是否更新配置
        self.UPDATE_CFG = False

        if args.username:
            self.UPDATE_CFG = True
            self.username = args.username
            self.uuid = get_uuid(args.username)
        
        if args.java_path:
            self.UPDATE_CFG = True
            self.java_path = args.java_path

        if args.jvm_args:
            self.UPDATE_CFG = True
            self.jvm_args = args.jvm_args

    @property
    def currentversion(self):
        return self._v
    
    @currentversion.setter
    def currentversion(self, v):
        self.UPDATE_CFG = True
        self._v = v

    def set_cfg(self):
        self.user_data = {}
        self.user_data['username'] = self.username
        self.user_data['uuid'] = self.uuid
        self.user_data['currentversion'] = self.currentversion
        self.user_data['java-path'] = self.java_path
        self.user_data['jvm-args'] = self.jvm_args

        # 如果有更新，就保存
        if self.UPDATE_CFG:
            logger.debug(f"更新配置: {self.user_data}")
            set_json(self.user_data, GAME_CONFIG)
    