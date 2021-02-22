# -*- coding: utf-8 -*-
import logging
import re
import sys


# this function will return partition number based on key value for proper distribution of topic records across partitions
def getPartition(key, partitionCount):
    return (parseKey(key) % partitionCount)


def parseKey(key):
    pNumber = 0
    p = re.compile("d(.*?)-")
    m = p.match(key)
    if m:
        pNumber = m.group(0)[1:-1]
    return int(pNumber)
