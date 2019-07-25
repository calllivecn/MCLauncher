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


def parse_args():
    parse = ArgumentParser(description='一个MC启动器',usage='%(prog)s [optional]',epilog='http://www.none.org')

    parse.add_argument("--install-game", action="store_true", help="安装游戏")

    parse.add_argument("-u", "--username", action="store", help="MC 游戏用户名")

    parse.add_argument("-v", "--verbose", action="count", default=0, help="verbose")
    
    return parse.parse_args()


def main():

    args = parse_args()
    #print("args:", args, args.install_game);sys.exit(0)

    if args.install_game:
        from checkdownload import ext_main

        if args.verbose <= 1:
            ext_main(1)
        else:
            ext_main(args.verbose)

        sys.exit(0)

    logger.setLevel(args.verbose)

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
