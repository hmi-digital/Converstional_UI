# -*- coding: utf-8 -*-
import logging
import json
from utils import nlp_config
from utils import log_util
from core.classifiers.tfidf import predict_tfidf
from core.classifiers.nlu import predict_nlu
from warnings import simplefilter

# ignore all warnings
simplefilter(action='ignore')

def predict(domain, locale, userUtterance):

    response = json.loads('{"response":"ERROR: error during predicting the user utterance"}')

    if not nlp_config.checkDataAvaialble:
        log_util.logerrormsg("[PREDICT_MODEL] no intent data found. Exiting...")
        return json.loads('{"response":"ERROR: no intent data found. Exiting..."}')

    if nlp_config.getParameter('ALGORITHM') == 'TFIDF':
        response = predict_tfidf.predict(domain, locale, userUtterance)
    elif nlp_config.getParameter('ALGORITHM') == 'NLU':
        response = predict_nlu.predict(domain, locale, userUtterance)
    else:
        log_util.logerrormsg("[PREDICT_MODEL] configured algorithm is not supported. Exiting...")
    return response


if __name__ == "__main__":
    predict()
