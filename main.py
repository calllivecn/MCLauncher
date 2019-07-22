#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:58:30
# author calllivecn <c-all@qq.com>

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
