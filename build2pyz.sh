#!/bin/bash
# date 2019-07-24 14:59:46
# author calllivecn <c-all@qq.com>

set -e

exit_clear(){
	rm -rf "$1"
}

temp=$(mktemp -d)

trap "exit_clear" SIGINT SIGTERM ERR EXIT

cp -v *.py "$temp"

python3 -m zipapp "$temp" -c -m "main:main" -o MCLauncher.pyz -p "/usr/bin/env python3"

