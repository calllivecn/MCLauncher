#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:15:49
# author calllivecn <c-all@qq.com>


__all__ = ["logger", "setLevel"]


from sqlite3 import Time
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from os import path

logger = logging.getLogger("MCL")

if logger is None:
    logger = logging.Logger("MCL")

stream = logging.StreamHandler(sys.stderr)

fmt = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s", datefmt="%Y-%m-%d-%H:%M:%S")

stream.setFormatter(fmt)

logger.addHandler(stream)

logfilename, ext = path.splitext(sys.argv[0])

logfilename = logfilename + ".logs"

#logsname = logging.FileHandler(logfilename, "a")
logsname = TimedRotatingFileHandler(logfilename, when="D",interval=1, backupCount=30)


logsname.setFormatter(fmt)

logger.addHandler(logsname)


logger.setLevel(logging.WARN)


def setLevel(level):

    if level == 0:
        logger.setLevel(logging.WARN)
    elif level == 1:
        logger.setLevel(logging.INFO)
    elif level == 2 or level > 2:
        logger.setLevel(logging.DEBUG)

