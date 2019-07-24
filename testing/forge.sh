MC_DIR=".minecraft"
java -Dminecraft.client.jar=$MC_DIR/versions/1.12/1.12.jar \
-Dminecraft.launcher.version=2.7.8.33 \
-Dminecraft.launcher.brand="Hello Minecraft! Launcher" \
-XX:+UseG1GC -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow \
-Xmn128m -Xmx1024m \
-Djava.library.path=$MC_DIR/versions/1.12-forge1.12-14.21.1.2443/1.12-forge1.12-14.21.1.2443-natives \
-Dfml.ignoreInvalidMinecraftCertificates=true \
-Dfml.ignorePatchDiscrepancies=true \
-cp $MC_DIR/libraries/net/minecraftforge/forge/1.12-14.21.1.2443/forge-1.12-14.21.1.2443.jar:\
$MC_DIR/libraries/net/minecraft/launchwrapper/1.12/launchwrapper-1.12.jar:\
$MC_DIR/libraries/org/ow2/asm/asm-all/5.2/asm-all-5.2.jar:\
$MC_DIR/libraries/jline/jline/2.13/jline-2.13.jar:\
$MC_DIR/libraries/com/typesafe/akka/akka-actor_2.11/2.3.3/akka-actor_2.11-2.3.3.jar:\
$MC_DIR/libraries/com/typesafe/config/1.2.1/config-1.2.1.jar:\
$MC_DIR/libraries/org/scala-lang/scala-actors-migration_2.11/1.1.0/scala-actors-migration_2.11-1.1.0.jar:\
$MC_DIR/libraries/org/scala-lang/scala-compiler/2.11.1/scala-compiler-2.11.1.jar:\
$MC_DIR/libraries/org/scala-lang/plugins/scala-continuations-library_2.11/1.0.2/scala-continuations-library_2.11-1.0.2.jar:\
$MC_DIR/libraries/org/scala-lang/plugins/scala-continuations-plugin_2.11.1/1.0.2/scala-continuations-plugin_2.11.1-1.0.2.jar:\
$MC_DIR/libraries/org/scala-lang/scala-library/2.11.1/scala-library-2.11.1.jar:\
$MC_DIR/libraries/org/scala-lang/scala-parser-combinators_2.11/1.0.1/scala-parser-combinators_2.11-1.0.1.jar:\
$MC_DIR/libraries/org/scala-lang/scala-reflect/2.11.1/scala-reflect-2.11.1.jar:\
$MC_DIR/libraries/org/scala-lang/scala-swing_2.11/1.0.1/scala-swing_2.11-1.0.1.jar:\
$MC_DIR/libraries/org/scala-lang/scala-xml_2.11/1.0.2/scala-xml_2.11-1.0.2.jar:\
$MC_DIR/libraries/lzma/lzma/0.0.1/lzma-0.0.1.jar:\
$MC_DIR/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:\
$MC_DIR/libraries/java3d/vecmath/1.5.2/vecmath-1.5.2.jar:\
$MC_DIR/libraries/net/sf/trove4j/trove4j/3.0.3/trove4j-3.0.3.jar:\
$MC_DIR/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:\
$MC_DIR/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:\
$MC_DIR/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:\
$MC_DIR/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:\
$MC_DIR/libraries/com/ibm/icu/icu4j-core-mojang/51.2/icu4j-core-mojang-51.2.jar:\
$MC_DIR/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:\
$MC_DIR/libraries/com/paulscode/codecjorbis/20101023/codecjorbis-20101023.jar:\
$MC_DIR/libraries/com/paulscode/codecwav/20101023/codecwav-20101023.jar:\
$MC_DIR/libraries/com/paulscode/libraryjavasound/20101123/libraryjavasound-20101123.jar:\
$MC_DIR/libraries/com/paulscode/librarylwjglopenal/20100824/librarylwjglopenal-20100824.jar:\
$MC_DIR/libraries/com/paulscode/soundsystem/20120107/soundsystem-20120107.jar:\
$MC_DIR/libraries/io/netty/netty-all/4.1.9.Final/netty-all-4.1.9.Final.jar:\
$MC_DIR/libraries/com/google/guava/guava/21.0/guava-21.0.jar:\
$MC_DIR/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:\
$MC_DIR/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:\
$MC_DIR/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:\
$MC_DIR/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:\
$MC_DIR/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:\
$MC_DIR/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:\
$MC_DIR/libraries/com/mojang/authlib/1.5.25/authlib-1.5.25.jar:\
$MC_DIR/libraries/com/mojang/realms/1.10.16/realms-1.10.16.jar:\
$MC_DIR/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:\
$MC_DIR/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:\
$MC_DIR/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:\
$MC_DIR/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:\
$MC_DIR/libraries/it/unimi/dsi/fastutil/7.1.0/fastutil-7.1.0.jar:\
$MC_DIR/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:\
$MC_DIR/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:\
$MC_DIR/libraries/org/lwjgl/lwjgl/lwjgl/2.9.4-nightly-20150209/lwjgl-2.9.4-nightly-20150209.jar:\
$MC_DIR/libraries/org/lwjgl/lwjgl/lwjgl_util/2.9.4-nightly-20150209/lwjgl_util-2.9.4-nightly-20150209.jar:\
$MC_DIR/libraries/com/mojang/text2speech/1.10.3/text2speech-1.10.3.jar:\
$MC_DIR/versions/1.12/1.12.jar net.minecraft.launchwrapper.Launch \
--username ddv12138 --version "HMCL 2.7.8.33" \
--gameDir $MC_DIR --assetsDir $MC_DIR/assets \
--assetIndex 1.12 \
--uuid c6f2228405c082921916d33f6dcb2d8b \
--accessToken c6f2228405c082921916d33f6dcb2d8b \
--userType Legacy --tweakClass net.minecraftforge.fml.common.launcher.FMLTweaker \
--versionType Forge --height 480 --width 854
