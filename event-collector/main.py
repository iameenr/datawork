from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class Event(BaseModel):
    event_type: str
    product_id: str
    user_id: str

@app.post("/events")
def collect_event(event: Event):
    producer.send('raw-events', event.dict())
    return {"status": "event collected"}
