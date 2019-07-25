# MCLauncher

目前还有几个问题：

	1. 没有GUI。
	2. 不同版本，需要不同的启动解析方式。目前，只测试了，minimumLauncherVersion: 21, (1.14.x, 1.13.x)
	3. 游戏资源check还未添加。
	4. 目前不支持选择游戏版本。


使用注意事项：
	- 最好每次安装游戏，都新建一个目录。

游戏下载：

大陆地区，下载游戏需要代理，，，。。。。

	例子：

	export http_proxy="http://127.0.0.1:9000"
	export https_proxy="http://127.0.0.1:9000"

```shell
	python3 main.py 根据提示操作。
	或者 python3 MCLauncher.pyz
```


启动游戏：
```shell
	./MCLauncher.pyz 
	或者 python3 MCLahuncher.pyz
```
