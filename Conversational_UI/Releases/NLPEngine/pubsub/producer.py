# -*- coding: utf-8 -*-
import json
from utils import nlp_config
from utils import log_util
from kafka import KafkaProducer
from pubsub import utils

producer = None


def initialise():
    global producer
    producer = KafkaProducer(bootstrap_servers=nlp_config.getParameter('KAFKA_BROKERS').split(","),
                             client_id=nlp_config.getParameter('CLIENT_ID'),
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                             linger_ms=1000,
                             retries=1
                             )


def sendMessgae(topicName, key, value):
    global producer
    pNum = utils.getPartition(key, int(nlp_config.getParameter('PARTITIONS')))
    msg = json.loads(value)
    producer.send(topicName, value=msg, key=key.encode('utf-8'), partition=pNum)
    producer.flush()
    log_util.loginfomsg("[PRODUCER] sending message: \"{}\"".format(value))
    log_util.loginfomsg("[PRODUCER] message sent with key: \"{}\" to partition \"{}\"!".format(key, pNum))
