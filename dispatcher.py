from api.conversations import get_conversations
from pika.exceptions import AMQPConnectionError
import pika
import sys
import traceback


def main():
    """Query all ongoing conversations and queue it.
    :return: None
    """
    conversations = get_conversations()
    try:
        for conversation in conversations:
            credentials = pika.PlainCredentials('rabbitmq', 'cloudwalk')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672,
                                                                           credentials=credentials))
            channel = connection.channel()
            channel.queue_declare(queue='conversations')
            channel.basic_publish(exchange='', routing_key='conversations', body=conversation)
            connection.close()
    except AMQPConnectionError as amqpe:
        print("[conversation-dispatcher] - Error connecting to RabbitMQ: ", repr(amqpe))
    except Exception as e:
        t, value, tb = sys.exc_info()
        print("[conversation-dispatcher] - Exception running thumbnail service: ", repr(e))
        print("[conversation-dispatcher] - Error line: ", tb.tb_lineno)
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
