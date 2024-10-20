import json

import pika


def listen(queue_name: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=f"{queue_name}_result")

    def callback(ch, method, properties, body):
        execution = json.loads(body)
        print(execution)
        # execution = session.get(Execution, execution["id"])
        # execution.score = float(execution["score"])
        #
        # session.add(instance=execution)
        # session.commit()

    channel.basic_consume(queue=f"{queue_name}_result", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
