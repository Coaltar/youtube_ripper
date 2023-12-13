import pika

class RabbitMQClient:
    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, queue_name, message):
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f"Sent message: '{message}' to '{queue_name}'")

    def receive_messages(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Connection closed.")

# Example usage:
if __name__ == "__main__":
    # Configure RabbitMQ connection
    rabbitmq_config = {
        'host': 'localhost',
        'port': 5672,
        'username': 'guest',
        'password': 'guest',
    }

    # Create RabbitMQ client
    client = RabbitMQClient(**rabbitmq_config)

    # Connect to RabbitMQ server
    client.connect()

    # Declare a queue
    queue_name = 'my_queue'
    client.declare_queue(queue_name)

    # Send a message to the queue
    message_to_send = 'Hello, RabbitMQ!'
    client.send_message(queue_name, message_to_send)

    # Define a callback function for receiving messages
    def callback(ch, method, properties, body):
        print(f"Received message: {body}")

    # Receive messages from the queue
    client.receive_messages(queue_name, callback)

    # Close the connection
    client.close_connection()
