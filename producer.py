import json
import time
from kafka import KafkaProducer


def serializer(message):
    return json.dumps(message).encode('utf-8')


def producer_send(topic, data):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        api_version=(0,11,5),
        value_serializer=serializer
    )
    producer.send(topic, value=data, key=bytes(1))


if __name__ == '__main__':
    while True:
        producer_send("test123", {"url": "12367"})
        time.sleep(3)
