LAUNCHER = "MCL"
LAUNCHER_VERSION = "v1.9.0"


tmp = LAUNCHER_VERSION[1:]
# 生成
LAUNCHER_VERSION_INTO = tuple(map(int, tmp.split(".")))


if __name__ == "__main__":
    print(locals())
