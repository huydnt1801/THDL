import requests
import json
from kafka import KafkaProducer


def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def serializer(message):
    return json.dumps(message).encode('utf-8')


def producer_send(topic, data):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=serializer
    )
    producer.send(topic, data)


def process_string(s):
    if s is None:
        return ""
    if s == "":
        return ""
    c = s.replace('\r', '').replace('\n', '')
    c = c.replace('\t', '')
    c = c.replace("&nbsp;", "")
    # c = c.replace("\xa0", "")
    c = c.strip()
    c = c.encode('unicode-escape').decode('unicode-escape')
    return c
