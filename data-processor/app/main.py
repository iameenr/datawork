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
        print("Received event: {}".format(event_data))

        try:
            # validate
            Event(**event_data)
            
            # process
            processed_data = process_event(event_data)
            
            # send to processed topic
            producer.send(PROCESSED_EVENTS_TOPIC, processed_data)
            print(f"Processed and sent event: {processed_data}")

        except ValidationError as e:
            # handle invalid data
            error_payload = {
                "error": "validation_failed",
                "details": e.errors(),
                "original_event": event_data
            }
            producer.send(DEAD_LETTER_TOPIC, error_payload)
            print(f"Validation failed. Sent to dead-letter-queue: {error_payload}")
        except Exception as e:
            # Handle other errors
            error_payload = {
                "error": "processing_failed",
                "details": str(e),
                "original_event": event_data
            }
            producer.send(DEAD_LETTER_TOPIC, error_payload)
            print(f"Processing failed. Sent to dead-letter-queue: {error_payload}")