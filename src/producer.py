import json
import time
import random
from confluent_kafka import Producer

# Kafka configuration
conf = {
    'bootstrap.servers': 'your-msk-bootstrap-servers',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'your-username',
    'sasl.password': 'your-password'
}

# Initialize producer
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Generate and send random transaction data
def produce_data(topic='transactions'):
    for i in range(1000):
        data = {
            'transaction_id': i,
            'amount': round(random.uniform(10, 1000), 2),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'customer_id': random.randint(1, 100)
        }
        producer.produce(topic, json.dumps(data).encode('utf-8'), callback=delivery_report)
        producer.flush()
        time.sleep(0.1)  # Simulate real-time streaming

if __name__ == '__main__':
    produce_data()