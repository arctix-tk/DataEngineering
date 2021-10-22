# https://www.rabbitmq.com/tutorials/tutorial-one-python.html
# start RabbitMQ with docker:
# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
# python package for RabbitMQ
import pika
from datetime import datetime
# connect to RabbitMQ-Broker on localhost
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()

# create a queue to which the message will be delivered
# the name of the queue is idempotent; if the queue exists, nothing happens
channel.queue_declare(queue='hello')


# publish the message (body) to the queue (routing_key)
t0 = str(datetime.now()).encode('utf-8')
for x in range(0,100000):
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='a')
    
channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=t0)

#print(" [x] Sent 'Hello World!'")
# close the connection
connection.close()
