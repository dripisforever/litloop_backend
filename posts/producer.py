# ref https://www.youtube.com/watch?v=ddrucr_aAzA
import pika

params = pika.URLParameters('amqps://eklxfrum:ziIjwSNp1GeajIR74cdn1nR77zIjybnM@sparrow.rmq.cloudamqp.com/eklxfrum')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
