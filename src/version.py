LAUNCHER = "MCL"
LAUNCHER_VERSION = "1.9.0"


# 生成
LAUNCHER_VERSION_INTO = tuple(map(int, LAUNCHER_VERSION.split(".")))


if __name__ == "__main__":
    print(locals())
