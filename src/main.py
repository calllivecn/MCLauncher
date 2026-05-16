#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:58:30
# author calllivecn <calllivecn@outlook.com>

import os
import sys
import argparse
from argparse import ArgumentParser


# 日志要放前面？？？
from logs import logger, setLevel

import checkdownload
from launcher import MCL
from initconfig import McDirStruct
from version import LAUNCHER_VERSION
from funcs import select_local
from usercfg import UserCFG
from usernamecheck import check_username


def parse_args():
    parse = ArgumentParser(
        description=f"一个MC启动器 {LAUNCHER_VERSION}",
        usage='%(prog)s [optional]',
        epilog='https://github.com/calllivecn/MCLauncher'
        )

    parse.add_argument("--install-game", action="store_true", help="安装游戏")

    parse.add_argument("--check-game", action="store_true", help="检查游戏资源完整性, 缺少的会下载。")

    parse.add_argument("--export-game", action="store", help="导出指定游戏版本到新目录")

    parse.add_argument("-u", "--username", action="store", help="MC 游戏用户名。和--online一起使用是切换微软账号。")

    parse.add_argument("-ut", "--username-tmp", action="store_true", default=False, help="临时启动一个用户名。和--username一起使用，不把当前用户信息写入配置。")

    parse.add_argument("--online", action="store_true", help="使用微软账号登录。单独使用时，是添加一个新的微软账号。")

    parse.add_argument("--select-version", action="store_true", help="交互选择游戏版本。")

    parse.add_argument("--resolution", action="store", help="设置游戏启动时窗口大小, 例如：1920x1080（默认自动）")

    parse.add_argument("--java-path", action="store", help="指定java路径")

    parse.add_argument("--jvm-args", action="store", help="设置jvm自定义参数")

    parse.add_argument("-v", "--verbose", action="count", default=0, help="verbose。-vvv：只输出日志和启用参数，不运行游戏。")

    parse.add_argument("--parse", action="store_true", help=argparse.SUPPRESS)

    return parse.parse_args()


def main():

    args = parse_args()

    if args.parse:
        print(args)
        sys.exit(0)
    
    setLevel(args.verbose)

    if args.verbose >= 2:
        logger.debug(f"args: {args}")
    
    if args.install_game:

        if args.verbose <= 1:
            setLevel(1)

        checkdownload.install_game()
        sys.exit(0)
    
    if args.check_game:
        if args.verbose <= 1:
            setLevel(1)

        checkdownload.check_game()
        sys.exit(0)
    
    if args.export_game:

        if args.verbose <= 1:
            setLevel(1)

        checkdownload.export_game(args.export_game)
        sys.exit(0)

    mds = McDirStruct()
    os.chdir(mds.Duser_home)

    usercfg = UserCFG(args)

    # 检测玩家游戏名
    bool_, msg = check_username(args.username)
    if not bool_:
        logger.error(f"玩家名称: [{args.username}] 不合法。{msg}")
        sys.exit(1)

    # 更新游戏版本
    if args.select_version:
        # 选择游戏版本
        usercfg.currentversion = select_local(mds.versions)

    elif usercfg.currentversion is None:
        logger.debug(f"currentversion is None ... --> {usercfg.currentversion}")
        usercfg.currentversion = select_local(mds.versions)

    # else:
        # 选择游戏最新版本
        # usercfg.currentversion = select_local(mds.versions, latest=True)
    

    # 有更新保存配置，无更新不保存配置。如果是临时用户不保存。
    # if not args.username_tmp:
    usercfg.UPDATE_CFG = not args.username_tmp
    usercfg.set_cfg()

    if usercfg.resolution is None:
        height = None
        width = None
    else:
        width, height  = usercfg.resolution.split("x")


    mds.select_version_id(usercfg.currentversion)

    if args.verbose >= 3:
        # debug = True 只输出日志和参数，不运行游戏
        mclauncher = MCL(usercfg.username, usercfg.uuid, usercfg.accesstoken, mds, width, height, debug=True)
    else:
        # debug = False
        mclauncher = MCL(usercfg.username, usercfg.uuid, usercfg.accesstoken, mds, width, height)


    logger.info(f"当前用户名：{usercfg.username}")
    
    mclauncher.set_java_path(usercfg.java_path)
    mclauncher.set_jvm_customize_args(usercfg.jvm_args)
    mclauncher.launcher()


if __name__ == "__main__":
    main()
