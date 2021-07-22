#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:58:30
# author calllivecn <c-all@qq.com>

import os
import sys
import argparse
from pathlib import Path
from argparse import ArgumentParser


import checkdownload
from launcher import MCL
from initconfig import *
from funcs import *
from logs import logger
from usercfg import UserCFG


def parse_args():
    parse = ArgumentParser(description='一个MC启动器 {}'.format(LAUNCHER_VERSION), usage='%(prog)s [optional]',epilog='https://github.com/calllivecn/MCLauncher')

    parse.add_argument("--install-game", action="store_true", help="安装游戏")

    parse.add_argument("--check-game", action="store_true", help="检查游戏资源完整性")

    parse.add_argument("--export-game", action="store", help="导出指定游戏版本到新目录")

    parse.add_argument("-u", "--username", action="store", help="MC 游戏用户名")
    
    parse.add_argument("--online", action="store_true", help="使用微软账号登录")

    parse.add_argument("--select-version", action="store_true", help="指定游戏版本。（默认启动本地最新版）")

    parse.add_argument("--java-path", action="store", help="指定 java 路径")

    parse.add_argument("--jvm-args", action="store", help="设置 jvm 参数")

    parse.add_argument("-v", "--verbose", action="count", default=0, help="verbose")

    parse.add_argument("--parse", action="store_true", help=argparse.SUPPRESS)

    return parse.parse_args()


def main():

    args = parse_args()

    if args.parse:
        print(args)
        sys.exit(0)

    if args.verbose >= 3:
        print("args:", args)
        logger.setLevel(3)
    else:
        logger.setLevel(args.verbose)
    
    if args.install_game:

        if args.verbose <= 1:
            logger.setLevel(1)

        checkdownload.install_game()
        sys.exit(0)
    
    if args.check_game:
        if args.verbose <= 1:
            logger.setLevel(1)

        checkdownload.check_game()
        sys.exit(0)
    
    if args.export_game:

        if args.verbose <= 1:
            logger.setLevel(1)

        checkdownload.export_game(args.export_game)
        sys.exit(0)


    mds = McDirStruct()
    os.chdir(mds.Duser_home)

    usercfg = UserCFG(args)

    # 更新游戏版本
    if args.select_version:
        # 选择游戏版本
        usercfg.currentversion = select_local(mds.versions)

    # 有更新保存配置，无更新不保存配置。
    usercfg.set_cfg()

    mds.select_version_id(usercfg.currentversion)
    mclauncher = MCL(usercfg.username, usercfg.uuid, usercfg.accesstoken, mds)
    
    mclauncher.set_java_path(str(Path(usercfg.java_path)))
    mclauncher.set_jvm_customize_args(usercfg.jvm_args)
    mclauncher.launcher()


if __name__ == "__main__":
    main()
