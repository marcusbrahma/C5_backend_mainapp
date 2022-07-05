from itertools import product
from flask import jsonify
import pika, json

params = pika.URLParameters('amqps://rrwpiyra:N1DaWC9wtQAM_AC0-KDdCusQTxWgmvIm@armadillo.rmq.cloudamqp.com/rrwpiyra')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='orders', body=json.dumps(body), properties=properties)
    print (jsonify(body))