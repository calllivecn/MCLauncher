# MCLauncher

目前还有几个问题：

	1. 有了GUI， 还没接入。
	2. 不同版本，需要不同的启动解析方式。目前只支持(可能及以上)：1.13.x ~ 1.21.x (minimumLauncherVersion: 21)


CHANGELOG 2026-10-12：

	1. 切换使用新的账号生成算法(切换为HMCL 一样的离线账号生成算法)
	2. 更新支持 微软账号的新登录方法(当时可以正确登录)

CHANGELOG 2026-05-17：

	1. 支持26.1 ~ 26.2 新版本号方式

CHANGELOG 2025-10-10：

	1. 需要python 3.12以上
    2. 修复一些小问题
    3. 使用pyinstaler打包生成，直接执行二进制文件。
	4. 支持fabric。

CHANGELOG 2024-12-25：

	1. 修复windows问题。
    2. 修复迁移到httpx的问题。

CHANGELOG 2021-12-01：

	1. 多个小bug修复。

CHANGELOG 2021-08-07：

	1. 可以使用了，只是不熟悉命令行的人，还不友好。

CHANGELOG 2021-07-24：

	1. 添加微软账号登录。
	2. 添加多启动。

CHANGELOG 2021-02-18：

	1. fix  --game-version 选择游戏后不能启动对应版本。
	2. modify --game-version to --select-version
	3. 还有修改用户名后，不能生效的问题。（之后在修）

CHANGELOG 2020-08-06：

	1. windows 支持。

CHANGELOG 2020-08-05：

	1. 选择一个游戏版本进行导出(--export-game)
	2. 游戏资源检查+修补(--check-game)
	3. 支持选择(--select-version)游戏版本启动, 默认启动本地最新版。

## 使用注意事项：

- 有时候网络不好，下载失败，可以 CTRL+C 关闭安装。在次运行 --install-game 继续安装。

## 在release下载二进制文件 快速尝试

- 大陆地区，下载游戏需要代理。。。

```shell
	export http_proxy="http://127.0.0.1:9000"
	export https_proxy="http://127.0.0.1:9000"

	./MCLauncher --install-game 根据提示操作。

	# 使用离线账号启动
	./MCLahuncher --username vii

	# 使用 微软账号启动 (这会打开你的默认浏览器，让你登录微软账号。)
	./MCLahuncher --username vii --online
```

## 使用uv 管理方式 快速尝试

```shell
git clone https://github.com/calllivecn/MCLauncher
cd MCLauncher/
uv sync
uv run src/main.py --help
```

- 使用示例

```shell
	# 首次启动(使用本地账号)
	./MCLahuncher --username vii

	# 使用微软账号登录。 (这会打开你的默认浏览器，让你登录微软账号。)
	./MCLahuncher --online

	# 之后启动
	./MCLahuncher

	# 切换游戏版本
	./MCLahuncher --select-version

	# 修改本地用户名
	./MCLahuncher --username <名字>

	# 临时本地用户名(不保存用户信息,同时多启动游戏时使用。)
	./MCLahuncher --username-tmp --username <名字>

	# 切换微软用户名
	./MCLahuncher --online --username <名字>
```

