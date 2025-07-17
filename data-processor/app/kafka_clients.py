from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_BROKER_URL = 'kafka:9092'
RAW_EVENTS_TOPIC = 'raw-events'
PROCESSED_EVENTS_TOPIC = 'processed-events'
DEAD_LETTER_TOPIC = 'dead-letter-queue'

def get_kafka_consumer():
    return KafkaConsumer(
        RAW_EVENTS_TOPIC,
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest'
    )

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
