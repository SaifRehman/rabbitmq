from flask import Flask, request, jsonify
import pika
import urllib.parse

app = Flask(__name__)
QUEUE_NAME = 'demo_queue'

# Decoded RabbitMQ AMQP URI
RABBITMQ_URI = 'amqp://default_user_N3oVfWGiMxXhlmXUkOC:mmFJ_XiJzPGWc7OQZRKErxuZpJYygq-e@route-rabbitmq-broker-rabbitmq.apps.cluster-xs688.dynamic.redhatworkshops.io:80/'

def connect_channel():
    params = pika.URLParameters(RABBITMQ_URI)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    return connection, channel

@app.route('/send', methods=['GET'])
def send_message():
    msg = request.args.get('msg', 'Hello from Flask!')
    connection, channel = connect_channel()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=msg)
    connection.close()
    return jsonify({'status': 'sent', 'message': msg})

@app.route('/read', methods=['GET'])
def read_messages():
    connection, channel = connect_channel()
    messages = []
    while True:
        method_frame, _, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
        if method_frame:
            messages.append(body.decode())
        else:
            break
    connection.close()
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)