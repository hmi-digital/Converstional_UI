# -*- coding: utf-8 -*-
import os
import shutil
from collections import OrderedDict
from utils import nlp_config
from rasa.shared.nlu.training_data.loading import load_data
from rasa.nlu.model import Trainer
from rasa.nlu import config
from utils import log_util
from warnings import simplefilter

simplefilter(action='ignore')

TRAINING_DATA = ''
CONFIG_DATA = ''
MODEL_NAME = ''
TMP_FILE = 'hashdump'

scriptDir = os.path.dirname(__file__)


def train(domain, locale, prop):
    format = nlp_config.getParameter('FORMAT')
    dataFile = os.path.join(scriptDir, '..', '..', '..', 'trainingData', 'intents',
                            domain + '_' + locale + '.' + format)
    configFile = os.path.join(scriptDir, '..', '..', 'config', nlp_config.getParameter('CONFIG_FILE'))
    modelFile = os.path.join(scriptDir, '..', '..', 'models', 'nlu')
    MODEL_NAME = domain + '_' + locale

    try:
        if format == 'md' or format == 'json' or format == 'yml':
            training_data = load_data(dataFile)
            trainer = Trainer(config.load(configFile))

            if not nlp_config.is_config_stale(domain, locale, prop):
                trainer.train(training_data)
                #delete the folder if it exist
                if os.path.exists(modelFile+MODEL_NAME):
                    shutil.rmtree(modelFile+MODEL_NAME)
                trainer.persist(modelFile, fixed_model_name=MODEL_NAME)
            else:
                log_util.loginfomsg("[TRAIN_NLU] no changes found to training data, using pre-trained model")
        else:
            log_util.logerrormsg("[TRAIN_NLU] unsupported format. Exiting...")
            res = {"intents": "-1", "utterances": "-1"}
            response = str(res).replace("'", '"').strip()
            return response
    except FileNotFoundError:
        log_util.logerrormsg("[TRAIN_NLU] could not locate the NLU config file")
        res = {"intents": "-1", "utterances": "-1"}
        response = str(res).replace("'", '"').strip()
        return response

    training_examples = OrderedDict()
    INTENT = 'intent'
    for example in [e.as_dict_nlu() for e in training_data.training_examples]:
        intent = example[INTENT]
        training_examples.setdefault(intent, [])
        training_examples[intent].append(example)
    count = 0
    for x in training_examples:
        if isinstance(training_examples[x], list):
            count += len(training_examples[x])

    log_util.loginfomsg(f'[TRAIN_NLU] identified domain: {domain}')
    log_util.loginfomsg(f'[TRAIN_NLU] identified locale: {locale}')
    log_util.loginfomsg(f'[TRAIN_NLU] number of utterances for training: {count}')
    log_util.loginfomsg(f'[TRAIN_NLU] number of intents for training: {len(training_examples)}')

    algo = os.path.splitext(nlp_config.getParameter('CONFIG_FILE'))[0]
    algo = algo.split("_")[1].upper()
    model = 'NLU:' + algo

    res = {"intents": str(len(training_examples)), "utterances": str(count), "model": model}
    response = str(res).replace("'", '"').strip()  # make it a string
    return response
