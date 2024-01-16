#!/bin/bash
# date 2019-07-24 14:59:46
# author calllivecn <c-all@qq.com>

set -e

exit_clear(){
	rm -rf "$1"
}

temp=$(mktemp -d)

trap "exit_clear" SIGINT SIGTERM ERR EXIT

cp -v src/*.py "$temp"

# 2024-01-17
pip install --no-compile --target "$temp" httpx[http2]

python3 -m zipapp "$temp" -c -m "main:main" -o MCLauncher.pyz -p "/usr/bin/env python3"

