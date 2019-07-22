#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:15:49
# author calllivecn <c-all@qq.com>


__all__ = ["logger"]


import sys
import logging

logger = logging.Logger("MCL")

stream = logging.StreamHandler(sys.stderr)

fmt = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(message)s", datefmt="%Y-%m-%d-%H:%M:%S")

stream.setFormatter(fmt)

logger.addHandler(stream)

logger.setLevel(logging.WARN)



#def getlogger(level=logging.WRAN):
#
#    logger = logging.Logger("MCL")
#    
#    stream = logging.StreamHandler(sys.stderr)
#    
#    fmt = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(message)s", datefmt="%Y-%m-%d-%H:%M:%S")
#    
#    stream.setFormatter(fmt)
#    
#    logger.addHandler(stream)
#
#    return logger.setLevel(level)


#logger = getlogger()
