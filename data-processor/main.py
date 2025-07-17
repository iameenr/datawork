from kafka import KafkaConsumer, KafkaProducer
import json
from pydantic import BaseModel, ValidationError
from datetime import datetime

# Pydantic model for event validation
class Event(BaseModel):
    event_type: str
    product_id: str
    user_id: str

# Kafka Configuration
consumer = KafkaConsumer(
    'raw-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest' # Start reading from the beginning of the topic
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Data processor started...")

for message in consumer:
    event_data = message.value
    print(f"Received event: {event_data}")

    try:
        # 1. Validate event data
        Event(**event_data)
        
        # 2. Enrich event data
        event_data['processed_at'] = datetime.utcnow().isoformat()
        event_data['status'] = 'processed'
        
        # 3. Send to processed-events topic
        producer.send('processed-events', event_data)
        print(f"Processed and sent event: {event_data}")

    except ValidationError as e:
        # 4. Handle invalid data
        error_payload = {
            "error": "validation_failed",
            "details": e.errors(),
            "original_event": event_data
        }
        producer.send('dead-letter-queue', error_payload)
        print(f"Validation failed. Sent to dead-letter-queue: {error_payload}")
    except Exception as e:
        # Handle other potential errors
        error_payload = {
            "error": "processing_failed",
            "details": str(e),
            "original_event": event_data
        }
        producer.send('dead-letter-queue', error_payload)
        print(f"Processing failed. Sent to dead-letter-queue: {error_payload}")
