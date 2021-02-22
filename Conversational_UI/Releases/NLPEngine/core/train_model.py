# -*- coding: utf-8 -*-
import json
from utils import nlp_config
from utils import log_util
from core.classifiers.tfidf import train_tfidf
from core.classifiers.nlu import train_nlu
from warnings import simplefilter

simplefilter(action='ignore')


def train(domain, locale):
    response = json.loads('{"response":"ERROR: Error during training the data"}')

    if not nlp_config.checkDataAvaialble:
        log_util.logerrormsg("[TRAIN_MODEL] no intent data found. Exiting...")
        return response

    if nlp_config.getParameter('ALGORITHM') == 'TFIDF':
        response = train_tfidf.train(domain, locale, nlp_config.getProperties())
    elif nlp_config.getParameter('ALGORITHM') == 'NLU':
        response = train_nlu.train(domain, locale, nlp_config.getProperties())
    else:
        log_util.logerrormsg("[TRAIN_MODEL] configured algorithm is not supported. Exiting...")
    return response


if __name__ == "__main__":
    train()
