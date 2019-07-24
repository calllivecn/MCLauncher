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
    parse = ArgumentParser(description='一个MC启动器',usage='%(prog)s [-u|--username]',epilog='http://www.none.org')

    parse.add_argument("-u", "--username", action="store", help="MC 游戏用户名")

    parse.add_argument("-v", "--verbose", action="count", default=0, help="verbose")
    
    return parse.parse_args()


def main():

    args = parse_args()

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
2019-07-24-18:17:34 initconfig.py:78 INFO 当前版本：['1.14.4']
2019-07-24-18:17:34 initconfig.py:81 INFO 选择版本：1.14.4
2019-07-24-18:17:34 launcher.py:103 DEBUG Djava_libaray_path: /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4-natives
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/mojang/patchy/1.1/patchy-1.1.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /oshi-project/oshi-core/1.1/oshi-core-1.1.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/mojang/javabridge/1.0.22/javabridge-1.0.22.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /io/netty/netty-all/4.1.25.Final/netty-all-4.1.25.Final.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/google/guava/guava/21.0/guava-21.0.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /commons-io/commons-io/2.5/commons-io-2.5.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /commons-codec/commons-codec/1.10/commons-codec-1.10.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/mojang/brigadier/1.0.17/brigadier-1.0.17.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/mojang/datafixerupper/2.0.24/datafixerupper-2.0.24.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/google/code/gson/gson/2.8.0/gson-2.8.0.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/mojang/authlib/1.5.25/authlib-1.5.25.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /it/unimi/dsi/fastutil/8.2.1/fastutil-8.2.1.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar
2019-07-24-18:17:34 launcher.py:205 INFO 解压natives库：/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2-natives-linux.jar --> /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar
2019-07-24-18:17:34 launcher.py:200 INFO 解压natives库：/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2-natives-linux.jar --> /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar
2019-07-24-18:17:34 launcher.py:200 INFO 解压natives库：/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2-natives-linux.jar --> /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar
2019-07-24-18:17:34 launcher.py:200 INFO 解压natives库：/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2-natives-linux.jar --> /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar
2019-07-24-18:17:34 launcher.py:200 INFO 解压natives库：/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2-natives-linux.jar --> /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives
2019-07-24-18:17:34 launcher.py:161 DEBUG Class Path 添加: /org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar
2019-07-24-18:17:34 launcher.py:200 INFO 解压natives库：/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2-natives-linux.jar --> /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar
2019-07-24-18:17:34 launcher.py:172 DEBUG Class Path 添加: /com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar
2019-07-24-18:17:34 launcher.py:200 INFO 解压natives库：/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3-natives-linux.jar --> /home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives
2019-07-24-18:17:34 launcher.py:217 DEBUG self.classpath -- >
/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/javabridge/1.0.22/javabridge-1.0.22.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/io/netty/netty-all/4.1.25.Final/netty-all-4.1.25.Final.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/google/guava/guava/21.0/guava-21.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/brigadier/1.0.17/brigadier-1.0.17.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/datafixerupper/2.0.24/datafixerupper-2.0.24.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/authlib/1.5.25/authlib-1.5.25.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/it/unimi/dsi/fastutil/8.2.1/fastutil-8.2.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar
2019-07-24-18:17:34 launcher.py:380 DEBUG jvm 参数(解析前)：-Djava.library.path="{natives_directory}" -Dminecraft.launcher.brand="{launcher_name}" -Dminecraft.launcher.version="{launcher_version}" -cp "{classpath}" 
2019-07-24-18:17:34 launcher.py:382 DEBUG jvm 参数：-Djava.library.path="/home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives" -Dminecraft.launcher.brand="MCL" -Dminecraft.launcher.version="v1.0" -cp "/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/javabridge/1.0.22/javabridge-1.0.22.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/io/netty/netty-all/4.1.25.Final/netty-all-4.1.25.Final.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/google/guava/guava/21.0/guava-21.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/brigadier/1.0.17/brigadier-1.0.17.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/datafixerupper/2.0.24/datafixerupper-2.0.24.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/authlib/1.5.25/authlib-1.5.25.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/it/unimi/dsi/fastutil/8.2.1/fastutil-8.2.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar
2019-07-24-18:17:34 launcher.py:282 DEBUG 不启用minecraft 参数：{'rules': [{'action': 'allow', 'features': {'is_demo_user': True}}], 'value': '--demo'}。
2019-07-24-18:17:34 launcher.py:282 DEBUG 不启用minecraft 参数：{'rules': [{'action': 'allow', 'features': {'has_custom_resolution': True}}], 'value': ['--width', '${resolution_width}', '--height', '${resolution_height}']}。
2019-07-24-18:17:34 launcher.py:304 DEBUG mc 启动参数：--username VII --version MCLv1.0 --gameDir /home/zx/mc/MCLauncher/.minecraft --assetsDir /home/zx/mc/MCLauncher/.minecraft/assets --assetIndex 1.14 --uuid eca282d789d1095c7d21f0f3e0b12774 --accessToken eca282d789d1095c7d21f0f3e0b12774 --userType legacy --versionType release 
2019-07-24-18:17:34 launcher.py:80 DEBUG MC Launcher CMD：java -Xmx1G -XX:+UseConcMarkSweepGC -XX:-UseAdaptiveSizePolicy -Xmn128M -Djava.library.path="/home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4-natives" -Dminecraft.launcher.brand="MCL" -Dminecraft.launcher.version="v1.0" -cp "/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/javabridge/1.0.22/javabridge-1.0.22.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/io/netty/netty-all/4.1.25.Final/netty-all-4.1.25.Final.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/google/guava/guava/21.0/guava-21.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/brigadier/1.0.17/brigadier-1.0.17.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/datafixerupper/2.0.24/datafixerupper-2.0.24.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/authlib/1.5.25/authlib-1.5.25.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/it/unimi/dsi/fastutil/8.2.1/fastutil-8.2.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar:/home/zx/mc/MCLauncher/.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar:/home/zx/mc/MCLauncher/.minecraft/versions/1.14.4/1.14.4.jar" net.minecraft.client.main.Main --username VII --version MCLv1.0 --gameDir /home/zx/mc/MCLauncher/.minecraft --assetsDir /home/zx/mc/MCLauncher/.minecraft/assets --assetIndex 1.14 --uuid eca282d789d1095c7d21f0f3e0b12774 --accessToken eca282d789d1095c7d21f0f3e0b12774 --userType legacy --versionType release 
