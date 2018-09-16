java -Dminecraft.client.jar=.minecraft/versions/1.12.2/1.12.2.jar \
-Dminecraft.launcher.version=2.7.8.33 \
-Dminecraft.launcher.brand="Hello Minecraft! Launcher" \
-XX:+UseG1GC \
-XX:-UseAdaptiveSizePolicy \
-XX:-OmitStackTraceInFastThrow \
-Xmn128m \
-Xmx1920m \
-Djava.library.path=.minecraft/versions/1.12.2/1.12.2-natives \
-Dfml.ignoreInvalidMinecraftCertificates=true \
-Dfml.ignorePatchDiscrepancies=true \
-Duser.home=null \
-cp \
.minecraft/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:\
.minecraft/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:\
.minecraft/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:\
.minecraft/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:\
.minecraft/libraries/com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar:\
.minecraft/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:\
.minecraft/libraries/com/paulscode/codecjorbis/20101023/codecjorbis-20101023.jar:\
.minecraft/libraries/com/paulscode/codecwav/20101023/codecwav-20101023.jar:\
.minecraft/libraries/com/paulscode/libraryjavasound/20101123/libraryjavasound-20101123.jar:\
.minecraft/libraries/com/paulscode/librarylwjglopenal/20100824/librarylwjglopenal-20100824.jar:\
.minecraft/libraries/com/paulscode/soundsystem/20120107/soundsystem-20120107.jar:\
.minecraft/libraries/io/netty/netty-all/4.1.9.Final/netty-all-4.1.9.Final.jar:\
.minecraft/libraries/com/google/guava/guava/21.0/guava-21.0.jar:\
.minecraft/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:\
.minecraft/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:\
.minecraft/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:\
.minecraft/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:\
.minecraft/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:\
.minecraft/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:\
.minecraft/libraries/com/mojang/authlib/1.5.25/authlib-1.5.25.jar:\
.minecraft/libraries/com/mojang/realms/1.10.17/realms-1.10.17.jar:\
.minecraft/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:\
.minecraft/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:\
.minecraft/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:\
.minecraft/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:\
.minecraft/libraries/it/unimi/dsi/fastutil/7.1.0/fastutil-7.1.0.jar:\
.minecraft/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:\
.minecraft/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:\
.minecraft/libraries/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar:\
.minecraft/libraries/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar:\
.minecraft/libraries/com/mojang/text2speech/1.10.3/text2speech-1.10.3.jar:\
.minecraft/versions/1.12.2/1.12.2.jar \
net.minecraft.client.main.Main \
--username zx \
--version "HMCL 2.7.8.33" \
--gameDir .minecraft \
--assetsDir .minecraft/assets \
--assetIndex 1.12 \
--uuid e6c760b3216a51c656c5861d72d5bf62 \
--accessToken e6c760b3216a51c656c5861d72d5bf62 \
--userType Legacy \
--versionType "HMCL 2.7.8.33" \
--height 480 --width 854 
