# MCLauncher

目前还有几个问题：

	1. 没有GUI。
	2. 不同版本，需要不同的启动解析方式。目前只支持(可能及以上)： 1.16.x, 1.15.x, 1.14.x, 1.13.x (minimumLauncherVersion: 21)

CHANGELOG 2020-08-06：
	1. windows 应该是支持了（手上没机器实测，虚拟机里测试能启动，说要更新openGL驱动。）

CHANGELOG 2020-08-05：
	1. 指定一个游戏版本进行导出(--export-game)
	2. 游戏资源--check-game添加。
	3. 支持选择(--game-version)游戏版本启动, 默认启动本地最新版。

### 使用注意事项：

- 有时候网络不好，下载失败，可以 CTRL+C 关闭安装。在次运行 --install-game 继续安装。


### 游戏下载： 

- 大陆地区，下载游戏需要代理。。。

```shell
	export http_proxy="http://127.0.0.1:9000"
	export https_proxy="http://127.0.0.1:9000"

	python3 MCLauncher.pyz --install-game 根据提示操作。
```


启动游戏：
```shell
	# 首次启动
	python3 MCLahuncher.pyz --username vii

	# 之后启动
	python3 MCLahuncher.pyz
```

