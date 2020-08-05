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
    parse = ArgumentParser(description='一个MC启动器',usage='%(prog)s [optional]',epilog='https://github.com/calllivecn/MCLauncher')

    parse.add_argument("--install-game", action="store_true", help="安装游戏")

    parse.add_argument("--check-game", action="store_true", help="检查游戏")

    parse.add_argument("--export-game", action="store", help="导出指定游戏版本到新目录")

    parse.add_argument("-u", "--username", action="store", help="MC 游戏用户名")

    parse.add_argument("-v", "--verbose", action="count", default=0, help="verbose")
    
    return parse.parse_args()


def main():

    args = parse_args()

    if args.verbose >= 3:
        print("args:", args)
        sys.exit(0)

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
        checkdownload.check_game(args.export_game)
        sys.exit(0)
    else:
        print("需要指定一个目录")
        sys.exit(1)


    mds = McDirStruct()
    mds.version_id()

    os.chdir(mds.Duser_home)

    if path.exists(GAME_CONFIG):
        user_data = get_json(GAME_CONFIG)
        username = user_data.get('username')
        uuid = user_data.get('uuid')
    else:
        if args.username is None:
            logger.error("首次启动需要设置一个游戏用户名！")
            sys.exit(1)

        username = args.username
        uuid = get_uuid(username)
        user_data = {'username' : username ,'uuid' : uuid}
        set_json(user_data, GAME_CONFIG)

    mclauncher = MCL(username, uuid, mds)
    mclauncher.launcher()


if __name__ == "__main__":
    main()
