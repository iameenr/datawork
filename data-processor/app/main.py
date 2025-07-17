from .kafka_clients import get_kafka_consumer, get_kafka_producer, PROCESSED_EVENTS_TOPIC, DEAD_LETTER_TOPIC
from .validation import Event
from .processing import process_event
from pydantic import ValidationError

def run():
    consumer = get_kafka_consumer()
    producer = get_kafka_producer()

    print("Data processor started...")

    for message in consumer:
        event_data = message.value
        print(f"Received event: {event_data}")

        try:
            # 1. Validate event data
            Event(**event_data)
            
            # 2. Process and enrich event data
            processed_data = process_event(event_data)
            
            # 3. Send to processed-events topic
            producer.send(PROCESSED_EVENTS_TOPIC, processed_data)
            print(f"Processed and sent event: {processed_data}")

        except ValidationError as e:
            # 4. Handle invalid data
            error_payload = {
                "error": "validation_failed",
                "details": e.errors(),
                "original_event": event_data
            }
            producer.send(DEAD_LETTER_TOPIC, error_payload)
            print(f"Validation failed. Sent to dead-letter-queue: {error_payload}")
        except Exception as e:
            # Handle other potential errors
            error_payload = {
                "error": "processing_failed",
                "details": str(e),
                "original_event": event_data
            }
            producer.send(DEAD_LETTER_TOPIC, error_payload)
            print(f"Processing failed. Sent to dead-letter-queue: {error_payload}")
