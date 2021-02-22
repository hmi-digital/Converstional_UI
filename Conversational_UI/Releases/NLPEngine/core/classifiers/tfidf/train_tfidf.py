# -*- coding: utf-8 -*-
import hashlib
import os
import json
import re
import codecs
import pickle
from utils import nlp_config
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
from utils.markdown import process_data
from warnings import simplefilter

# ignore all warnings
from core.classifiers.tfidf.utils import stemmer
from utils import log_util

simplefilter(action='ignore')
scriptDir = os.path.dirname(__file__)


def train(domain, locale, prop):
    datapath = os.path.join(scriptDir, '..', '..', '..', 'trainingData', 'intents')
    vectorDimension = int(nlp_config.getParameter('VECTOR_DIMENSION'))
    iterationNumbers = int(nlp_config.getParameter('ITERATION_NUMBER'))
    format = nlp_config.getParameter('FORMAT')

    utterance = []
    intent = []

    if format == 'md':
        utterance, intent = process_data(domain, locale)
        if not utterance or not intent:
            log_util.logerrormsg("[TRAIN_TFIDF] could not parse the markdown data. Exiting...")
            res = {"intents": "-1", "utterances": "-1"}
            response = str(res).replace("'", '"').strip()
            return response
    elif format == 'json':
        fileData = os.path.join(scriptDir, datapath, domain + '_' + locale + '.json')
        with codecs.open(fileData, 'r', 'utf-8')as dataFile:
            data = json.load(dataFile)
        for nameUtterances in data['tasks']:
            for utt in nameUtterances['utterances']:
                utterance.append(utt)
                intent.append(nameUtterances['name'])
    else:
        log_util.logerrormsg("unsupported format. Exiting...")
        res = {"intents": "-1", "utterances": "-1"}
        response = str(res).replace("'", '"').strip()
        return response

    mIntent = set(intent)

    # check if any changes to config
    if nlp_config.is_config_stale(domain, locale, prop):
        log_util.loginfomsg("[TRAIN_TFIDF] no changes found to training data, using pre-trained model")
        res = {"intents": str(len(mIntent)), "utterances": str(len(intent))}
        response = str(res).replace("'", '"').strip()  # make it a string
        return response
    else:
        pass

    stopListFile = os.path.join(scriptDir, '..', '..', 'dictionary', 'stopwords_' + locale + '.txt')
    arrayWords = []
    stopWords = []

    f = codecs.open(stopListFile, 'r', 'utf-8')
    lines = f.read().split("\n")
    for line in lines:
        if line != "":
            arrayWords.append(line.split(','))

    for a_word in arrayWords:
        for s_word in a_word:
            if (re.sub(' ', '', s_word)) != "":
                stopWords.append(s_word)

    extraStopWords = set(stopWords)
    if locale == 'ar':
        stops = set(stopwords.words('arabic')) | extraStopWords
    elif locale == 'da':
        stops = set(stopwords.words('danish')) | extraStopWords
    elif locale == 'en':
        stops = set(stopwords.words('english')) | extraStopWords
    elif locale == 'es':
        stops = set(stopwords.words('spanish')) | extraStopWords
    elif locale == 'hi':
        stops = extraStopWords
    elif locale == 'mr':
        stops = extraStopWords
    elif locale == 'nl':
        stops = set(stopwords.words('dutch')) | extraStopWords
    elif locale == 'sv':
        stops = set(stopwords.words('swedish')) | extraStopWords
    else:
        res = {"intents": "0", "utterances": "0"}
        response = str(res).replace("'", '"').strip()
        return response

    stemmer.setLocale(locale)

    tfidfVec = TfidfVectorizer(utterance, decode_error='ignore', stop_words=stops, ngram_range=(1, 5),
                               tokenizer=stemmer.stemTokenize)
    trainsetIdfVectorizer = tfidfVec.fit_transform(utterance).toarray()
    vLength = len(trainsetIdfVectorizer[1])
    nDimension = vectorDimension
    if vLength <= vectorDimension:
        nDimension = vLength - 1

    svd = TruncatedSVD(n_components=nDimension, algorithm='randomized', n_iter=iterationNumbers, random_state=42)
    trainLSA = svd.fit_transform(trainsetIdfVectorizer)

    pickle_path = os.path.join(scriptDir, '..', '..', 'models', 'tfidf', domain + '_' + locale + '_')
    fileName = pickle_path + 'utterance.m'
    fileObject = open(fileName, 'wb')
    pickle.dump(utterance, fileObject)
    fileObject.close()
    fileName = pickle_path + 'intent.m'
    fileObject = open(fileName, 'wb')
    pickle.dump(intent, fileObject)
    fileObject.close()
    fileName = pickle_path + 'tfidfVec.m'
    fileObject = open(fileName, 'wb')
    pickle.dump(tfidfVec, fileObject)
    fileObject.close()
    fileName = pickle_path + 'svd.m'
    fileObject = open(fileName, 'wb')
    pickle.dump(svd, fileObject)
    fileObject.close()
    fileName = pickle_path + 'trainLSA.m'
    fileObject = open(fileName, 'wb')
    pickle.dump(trainLSA, fileObject)
    fileObject.close()

    log_util.loginfomsg(f'[TRAIN_TFIDF] identified domain: {domain}')
    log_util.loginfomsg(f'[TRAIN_TFIDF] identified locale: {locale}')
    log_util.loginfomsg(f'[TRAIN_TFIDF] number of utterances for training: {len(intent)}')
    log_util.loginfomsg(f'[TRAIN_TFIDF] number of intents for training: {len(mIntent)}')

    res = {"intents": str(len(mIntent)), "utterances": str(len(intent)), "model": "TFIDF"}
    response = str(res).replace("'", '"').strip()  # make it a string
    return response
