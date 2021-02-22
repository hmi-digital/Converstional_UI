# -*- coding: utf-8 -*-
import json
import os
import re
import threading
from warnings import simplefilter

import flask
from flask import request, abort, make_response, jsonify
from utils import nlp_config
from utils import log_util
from core import train_model, predict_model
from pubsub import consumer
from pubsub import processMessage
# ignore all warnings
from pubsub import producer as pr

scriptDir = os.path.dirname(__file__)

simplefilter(action='ignore')

# load all the config parameters
nlp_config.loadParameters()

if re.search(nlp_config.getParameter('USE_BROKER'), 'true', re.IGNORECASE):
    log_util.loginfomsg("[APP] broker based NLPEngine enabled")
    # initialise the producer
    pr.initialise()
    # Run consumer listener to process all the NLP_TO_BOT messages
    consumer_ = consumer.initialise(nlp_config.getParameter('TOPIC_BOT_TO_NLP'))
    for msg in consumer_:
        log_util.loginfomsg(msg)
        t = threading.Thread(target=processMessage.process, args=(msg,))
        t.start()
else:
    log_util.loginfomsg("[APP] REST API based NLPEngine enabled")
    app = flask.Flask(__name__)
    scriptDir = os.path.dirname(__file__)
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = nlp_config.getParameter('PORT')


    @app.route('/train', methods=['POST'])
    def trainDomain():
        if not (request.args.get('domain')):
            log_util.logerrormsg("[APP] missing domain parameter")
            abort(404)
        if request.args.get('locale'):
            locale = request.args.get('locale')
        else:
            locale = 'en'
        domain = request.args.get('domain')
        res = train_model.train(domain, locale)
        n = int(json.loads(res)["utterances"])

        if (nlp_config.getParameter('ALGORITHM') == 'TFIDF'):
            md = 'TFIDF'
        else:
            algo = os.path.splitext(nlp_config.getParameter('CONFIG_FILE'))[0]
            algo = algo.split("_")[1].upper()
            md = 'NLU:' + algo

        if n > 0:
            response = {"messageId": "TRAIN_SUCCESS", "domain": domain, "locale": locale, "message": res, "model": md}
        else:
            response = {"messageId": "TRAIN_FAIL", "domain": domain, "locale": locale, "message": res, "model": md}

        return make_response(jsonify(response), 200,
                             {'Content-Type': 'application/json; charset=utf-8'})


    @app.route('/predict', methods=['POST'])
    def predict_query():
        if not (request.args.get('domain') or request.args.get('userUtterance')):
            log_util.logerrormsg("[APP] missing parameters")
            abort(404)
        if request.args.get('locale'):
            locale = request.args.get('locale')
        else:
            locale = 'en'
        utter = request.args.get('userUtterance')
        if locale == 'en':
            utterance = re.sub(r'[^a-zA-Z ]', '', utter)
        domain = request.args.get('domain')

        if (nlp_config.getParameter('ALGORITHM') == 'TFIDF'):
            md = 'TFIDF'
        else:
            algo = os.path.splitext(nlp_config.getParameter('CONFIG_FILE'))[0]
            algo = algo.split("_")[1].upper()
            model = 'NLU:' + algo
        res = {"messageId": "PREDICT", "domain": domain, "locale": locale, "userUtterance": utterance, "model": model,
               "message": predict_model.predict(domain, locale, utterance)}
        return make_response(jsonify(res), 200,
                             {'Content-Type': 'application/json; charset=utf-8'})


    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'response': 'ERROR: Please check your query parameter'}), 404,
                             {'Content-Type': 'application/json; charset=utf-8'})


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    if __name__ == '__main__':
        if re.search(nlp_config.getParameter('HTTPS'), 'true', re.IGNORECASE):
            context_ = ('keys/nlp.crt', 'keys/nlp.pem')
            app.run(debug=False, host=SERVER_HOST, port=SERVER_PORT, threaded=True, ssl_context=context_)
        else:
            app.run(debug=False, host=SERVER_HOST, port=SERVER_PORT, threaded=True)

# result = predictModel.predict("trip", "en", "I want to book a ticket")
# res = {"messageId": "PREDICT", "domain": "trip", "locale": "en", "userUtterance": "I want to book a ticket ","message": result}
# producer.sendMessgae(constants.topicName_2, "d9-DUMMY", json.dumps(res))
# producer.sendMessgae(constants.topicName_2, 'd13-GWP7LBRW2PR1', json.dumps(m1))
