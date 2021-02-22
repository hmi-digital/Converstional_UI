# -*- coding: utf-8 -*-
import os
import json
import hashlib
from warnings import simplefilter
from utils import log_util

# ignore all warnings


simplefilter(action='ignore')

##Global parameters
scriptDir = os.path.dirname(__file__)

dataPath = os.path.join(scriptDir, '..', 'trainingData', 'intents')
propertyFile = os.path.join(scriptDir, '..', 'config', 'nlp.properties')

separator = "="
properties = {}


def loadParameters() -> None:
    global properties
    with open(propertyFile) as f:
        for line in f:
            if separator in line:
                name, value = line.split(separator, 1)
                properties[name.strip()] = value.strip()


def getProperties():
    global properties
    return properties


def getParameter(param):
    global properties
    res = ""
    if param in properties:
        res = properties[param]
        return res
    else:
        log_util.loginfomsg('[NLP_CONFIG] the required parameter could not be located'.format(param))
        return res


def checkDataAvaialble(self) -> bool:
    files = os.listdir(dataPath)
    for file in files:
        if (file.startswith(self.domain)):
            if file.endswith(self.format):
                return True
        else:
            pass
    return False


def is_config_stale(domain, locale, properties):
    tmpFile = os.path.join(scriptDir, '..', 'trainingData', 'tmp', domain + '_hashdump')
    try:
        tmp = open(tmpFile, 'r')
    except IOError:
        tmp = open(tmpFile, 'a+')

    hash_original = tmp.read()
    # need to check if any changes to data, property file or rasa config file
    dataFile = os.path.join(dataPath, domain + '_' + locale + '.' + getParameter('FORMAT'))
    data_1 = open(dataFile, 'rb').read()
    #check if any changs in properties
    loadParameters()
    data_2 = json.dumps(getProperties())
    if (getParameter('ALGORITHM') == 'NLU'):
        rasaConfigFile = os.path.join(scriptDir, '..', 'core','config', getParameter('CONFIG_FILE') )
        data_3 = open(rasaConfigFile, 'rb').read()
    else:
        data_3 = None
    totalData = str(data_1) + str(data_2) + str(data_3)
    hash_current = hashlib.md5(totalData.encode('utf-8')).hexdigest()
    if (hash_original == hash_current):
        return True
    else:
        tmp.close()
        tmp = open(tmpFile, 'w')
        tmp.write(hash_current)
        tmp.close()
        return False
