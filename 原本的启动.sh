#!/bin/bash

MC_DIR="."


java -Xmx1G -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode -XX:-UseAdaptiveSizePolicy -Xmn128M \
-Djava.library.path=/home/zx/.minecraft/versions/1.14.4/1.14.4-natives-10740991767113 \
-Dminecraft.launcher.brand=java-minecraft-launcher \
-Dminecraft.launcher.version=1.6.89-j \
-cp ./.minecraft/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:\
./.minecraft/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:\
./.minecraft/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:\
./.minecraft/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:\
./.minecraft/libraries/com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar:\
./.minecraft/libraries/com/mojang/javabridge/1.0.22/javabridge-1.0.22.jar:\
./.minecraft/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:\
./.minecraft/libraries/io/netty/netty-all/4.1.25.Final/netty-all-4.1.25.Final.jar:\
./.minecraft/libraries/com/google/guava/guava/21.0/guava-21.0.jar:\
./.minecraft/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:\
./.minecraft/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:\
./.minecraft/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:\
./.minecraft/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:\
./.minecraft/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:\
./.minecraft/libraries/com/mojang/brigadier/1.0.17/brigadier-1.0.17.jar:\
./.minecraft/libraries/com/mojang/datafixerupper/2.0.24/datafixerupper-2.0.24.jar:\
./.minecraft/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:\
./.minecraft/libraries/com/mojang/authlib/1.5.25/authlib-1.5.25.jar:\
./.minecraft/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:\
./.minecraft/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:\
./.minecraft/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:\
./.minecraft/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:\
./.minecraft/libraries/it/unimi/dsi/fastutil/8.2.1/fastutil-8.2.1.jar:\
./.minecraft/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:\
./.minecraft/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:\
./.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:\
./.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:\
./.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:\
./.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:\
./.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:\
./.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:\
./.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar:\
./.minecraft/versions/1.14.4/1.14.4.jar \
net.minecraft.client.main.Main \
--username Player \
--version 1.14.4 \
--gameDir /home/zx/.minecraft \
--assetsDir /home/zx/.minecraft/assets \
--assetIndex 1.14 \
--uuid 00000000-0000-0000-0000-000000000000 \
--accessToken 6daf3053ca3e4df5b1a90f4e6fe74630 \
--userType legacy --versionType release
