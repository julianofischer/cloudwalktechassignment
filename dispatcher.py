from api.conversations import get_conversations
from pika.exceptions import AMQPConnectionError
import pika
import sys
import traceback


def main():
    conversations = get_conversations()
    try:
        for conversation in conversations:
            credentials = pika.PlainCredentials('guest', 'guest')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                                           credentials=credentials))
            channel = connection.channel()
            channel.queue_declare(queue='conversations')
            channel.basic_publish(exchange='', routing_key='conversations', body=conversation)
            connection.close()
    except AMQPConnectionError as amqpe:
        print("[conversation-worker] - Error connecting to RabbitMQ: ", repr(amqpe))
    except Exception as e:
        t, value, tb = sys.exc_info()
        print("[conversation-worker] - Exception running thumbnail service: ", repr(e))
        print("[conversation-worker] - Error line: ", tb.tb_lineno)
        print(traceback.format_exc())



if __name__ == '__main__':
    main()
