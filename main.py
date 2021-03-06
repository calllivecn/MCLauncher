#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:58:30
# author calllivecn <c-all@qq.com>

import os
import sys
from os import path
from argparse import ArgumentParser

from launcher import MCL
from initconfig import *
from funcs import *
from logs import logger
import checkdownload


def parse_args():
    parse = ArgumentParser(description='一个MC启动器 {}'.format(LAUNCHER_VERSION), usage='%(prog)s [optional]',epilog='https://github.com/calllivecn/MCLauncher')

    parse.add_argument("--install-game", action="store_true", help="安装游戏")

    parse.add_argument("--check-game", action="store_true", help="检查游戏资源完整性")

    parse.add_argument("--export-game", action="store", help="导出指定游戏版本到新目录")

    parse.add_argument("-u", "--username", action="store", help="MC 游戏用户名")

    parse.add_argument("--game-version", action="store_true", help="指定游戏版本。（默认启动本地最新版）")

    parse.add_argument("-v", "--verbose", action="count", default=0, help="verbose")
    
    return parse.parse_args()


def main():

    args = parse_args()

    if args.verbose >= 3:
        print("args:", args)
        sys.exit(0)

    logger.setLevel(args.verbose)

    if args.install_game:
        checkdownload.install_game()
        sys.exit(0)
    
    if args.check_game:
        if args.verbose <= 1:
            logger.setLevel(1)

        checkdownload.check_game()
        sys.exit(0)
    
    if args.export_game:
        checkdownload.export_game(args.export_game)
        sys.exit(0)


    mds = McDirStruct()
    os.chdir(mds.Duser_home)

    if path.exists(GAME_CONFIG):

        mds.version_id()
        
        user_data = get_json(GAME_CONFIG)

        if args.game_version:
            currentversion = select_local(mds.versions)
            user_data["currentversion"] = currentversion
            set_json(user_data, GAME_CONFIG)

        try:
            username = user_data['username']
            uuid = user_data['uuid']
            version = user_data['currentversion']
        except KeyError:
            logger.warning("{} 配置文件格式错误! 请重新启动".format(GAME_CONFIG))
            os.remove(GAME_CONFIG)
            sys.exit(1)

    else:

        if args.username is None:
            logger.error("首次启动需要设置一个游戏用户名！")
            sys.exit(1)
        
        username = args.username
        uuid = get_uuid(username)

        currentversion = select_local(mds.versions)

        mds.version_id(currentversion)

        user_data = {'username' : username ,'uuid' : uuid, 'currentversion': currentversion}
        set_json(user_data, GAME_CONFIG)

    mclauncher = MCL(username, uuid, mds)
    mclauncher.launcher()


if __name__ == "__main__":
    main()
