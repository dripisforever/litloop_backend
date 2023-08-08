import pika

params = pika.URLParameters('amqps://eklxfrum:ziIjwSNp1GeajIR74cdn1nR77zIjybnM@sparrow.rmq.cloudamqp.com/eklxfrum')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback)

print('Started consuming')

channel.start_consuming()

channel.close()
