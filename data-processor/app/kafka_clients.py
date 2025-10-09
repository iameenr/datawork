from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_BROKER_URL = 'kafka:9092'
RAW_EVENTS_TOPIC = 'raw-events'
PROCESSED_EVENTS_TOPIC = 'processed-events'
DEAD_LETTER_TOPIC = 'dead-letter-queue' # for bad messages

def get_kafka_consumer():
    # create and return a kafka consumer
    consumer = KafkaConsumer(
        RAW_EVENTS_TOPIC,
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    return consumer

def get_kafka_producer():
    # create and return a kafka producer
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer