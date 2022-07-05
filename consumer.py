from email.mime import image
from itertools import product
from turtle import title
from main import Product
import pika, json, os
from main import Product, db

params = pika.URLParameters('amqps://rrwpiyra:N1DaWC9wtQAM_AC0-KDdCusQTxWgmvIm@armadillo.rmq.cloudamqp.com/rrwpiyra')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='inventory')

def callback(ch, method, properties, body):
    print('Received in Order module')
    data = json.loads(body)
    print(data, properties)

    if properties.content_type == 'product_created':
        product= Product(id=data['id'],title= data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')

    elif properties.content_type == 'product_Updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')

channel.basic_consume(queue= 'inventory', on_message_callback=callback, auto_ack=True)


print('Started Consuming flask')

channel.start_consuming()

channel.close()