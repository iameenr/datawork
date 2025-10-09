from kafka import KafkaConsumer, KafkaProducer
import json
from pydantic import BaseModel, ValidationError
from datetime import datetime

# event validation
class Event(BaseModel):
    event_type: str
    product_id: str
    user_id: str

# Kafka
KAFKA_URL = 'localhost:9092'
consumer = KafkaConsumer(
    'raw-events',
    bootstrap_servers=[KAFKA_URL],
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest'
)

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_URL],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("starting processor")

for message in consumer:
    event = message.value
    print(f"got event: {event}")

    try:
        Event(**event)
        
        # Enrich
        event['processed_at'] = datetime.utcnow().isoformat()
        event['status'] = 'processed'
        
        # Send
        producer.send('processed-events', event)
        print(f"Processed: {event}")

    except ValidationError as e:
        # invalid data
        err_payload = {
            "error": "validation_failed",
            "details": e.errors(),
            "original_event": event
        }
        producer.send('dead-letter-queue', err_payload)
        print(f"Validation failed: {err_payload}")
    except Exception as e:
        # other errors
        err_payload = {
            "error": "processing_failed", # error msg
            "details": str(e),
            "original_event": event
        }
        producer.send('dead-letter-queue', err_payload)
        print(f"Processing failed: {err_payload}")

# todo: handle graceful shutdown
