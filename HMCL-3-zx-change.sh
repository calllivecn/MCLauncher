#!/bin/bash

# osx 才用
# "-XstartOnFirstThread" \

base_dir=$(dirname ${0})

MC_dir="${base_dir}/.minecraft"

java "-Dminecraft.client.jar=${MC_dir}/versions/1.13.1/1.13.1.jar" \
-Xmn128m -Xmx1024m \
-Xss1M \
"-Dfml.ignoreInvalidMinecraftCertificates=true" \
"-Dfml.ignorePatchDiscrepancies=true" \
"-Djava.library.path=${MC_dir}/versions/1.13.1/1.13.1-natives" \
"-Dminecraft.launcher.brand=HMCL" \
"-Dminecraft.launcher.version=3.1.94" \
-cp $MC_dir/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:\
$MC_dir/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:\
$MC_dir/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:\
$MC_dir/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:\
$MC_dir/libraries/com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar:\
$MC_dir/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:\
$MC_dir/libraries/com/paulscode/codecjorbis/20101023/codecjorbis-20101023.jar:\
$MC_dir/libraries/com/paulscode/codecwav/20101023/codecwav-20101023.jar:\
$MC_dir/libraries/com/paulscode/libraryjavasound/20101123/libraryjavasound-20101123.jar:\
$MC_dir/libraries/com/paulscode/soundsystem/20120107/soundsystem-20120107.jar:\
$MC_dir/libraries/io/netty/netty-all/4.1.25.Final/netty-all-4.1.25.Final.jar:\
$MC_dir/libraries/com/google/guava/guava/21.0/guava-21.0.jar:\
$MC_dir/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:\
$MC_dir/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:\
$MC_dir/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:\
$MC_dir/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:\
$MC_dir/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:\
$MC_dir/libraries/com/mojang/brigadier/1.0.14/brigadier-1.0.14.jar:\
$MC_dir/libraries/com/mojang/datafixerupper/1.0.16/datafixerupper-1.0.16.jar:\
$MC_dir/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:\
$MC_dir/libraries/com/mojang/authlib/1.5.25/authlib-1.5.25.jar:\
$MC_dir/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:\
$MC_dir/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:\
$MC_dir/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:\
$MC_dir/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:\
$MC_dir/libraries/it/unimi/dsi/fastutil/8.2.1/fastutil-8.2.1.jar:\
$MC_dir/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:\
$MC_dir/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:\
$MC_dir/libraries/com/mojang/realms/1.13.6/realms-1.13.6.jar:\
$MC_dir/libraries/org/lwjgl/lwjgl/3.1.6/lwjgl-3.1.6.jar:\
$MC_dir/libraries/org/lwjgl/lwjgl-jemalloc/3.1.6/lwjgl-jemalloc-3.1.6.jar:\
$MC_dir/libraries/org/lwjgl/lwjgl-openal/3.1.6/lwjgl-openal-3.1.6.jar:\
$MC_dir/libraries/org/lwjgl/lwjgl-opengl/3.1.6/lwjgl-opengl-3.1.6.jar:\
$MC_dir/libraries/org/lwjgl/lwjgl-glfw/3.1.6/lwjgl-glfw-3.1.6.jar:\
$MC_dir/libraries/org/lwjgl/lwjgl-stb/3.1.6/lwjgl-stb-3.1.6.jar:\
$MC_dir/libraries/com/mojang/text2speech/1.10.3/text2speech-1.10.3.jar:\
$MC_dir/versions/1.13.1/1.13.1.jar "net.minecraft.client.main.Main" \
--username zx --version "HMCL 3.1.94" --gameDir $MC_dir \
--assetsDir $MC_dir/assets --assetIndex 1.13.1 \
--uuid e6c760b3216a51c656c5861d72d5bf62 \
--accessToken b1f1a3df8beb4eff8672c64bdf03a462 \
--userType mojang --versionType release \
--width 1400 --height 800
