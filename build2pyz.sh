#!/bin/bash
# date 2019-07-24 14:59:46
# author calllivecn <c-all@qq.com>


temp=$(mktemp -d)

cp -v *.py "$temp"

python3 -m zipapp "$temp" -m "main:main" -o MCLauncher.pyz -p "/usr/bin/env python3"

