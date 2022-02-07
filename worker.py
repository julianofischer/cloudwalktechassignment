import pika
import sys
import traceback
from solutions.solutions import solve
from pika.exceptions import AMQPConnectionError


def rabbit_callback(ch, method, properties, body):
    """
    :param ch: pika.channel.Channel
    :param method: pika.spec.Basic.Return
    :param properties: pika.spec.BasicProperties
    :param body: ongoing conversation unique ID
    :return: None
    """
    print(f"[conversation-worker] - Received a conversation id: {body.decode('utf-8')}")
    try:
        conversation_id = body.decode('utf-8')
        solve(conversation_id)
    except Exception as e:
        t, value, tb = sys.exc_info()
        print("[conversation-worker] - Exception running thumbnail service: ", repr(e))
        print("[conversation-worker] - Error line: ", tb.tb_lineno)
        print(traceback.format_exc())
        # if the conversation is not solved, the id is queued again in an error queue
        ch.basic_publish(exchange='', routing_key='errors', body=conversation_id)


def main():
    """ Worker. Consumes from 'conversations' queue trying to solve the conversations' problems.
    :return: None
    """
    try:
        credentials = pika.PlainCredentials('rabbitmq', 'cloudwalk')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                             credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='conversations')
        channel.queue_declare(queue='errors')
        channel.basic_consume(queue='conversations', auto_ack=True,
                              on_message_callback=rabbit_callback)
        while True:
            channel.start_consuming()
    except AMQPConnectionError as amqpe:
        print("[conversation-worker] - Error connecting to RabbitMQ: ", repr(amqpe))
    except Exception as e:
        t, value, tb = sys.exc_info()
        print("[conversation-worker] - Exception running thumbnail service: ", repr(e))
        print("[conversation-worker] - Error line: ", tb.tb_lineno)
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
