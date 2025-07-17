from kafka import KafkaConsumer
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

# Database Setup
DATABASE_URL = "sqlite:///processed_events.db"
engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Event model
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    product_id = Column(String)
    user_id = Column(String)
    processed_at = Column(String) # Using String for simplicity with ISO format
    status = Column(String)

# Create the table
Base.metadata.create_all(bind=engine)

# Kafka Consumer
consumer = KafkaConsumer(
    'processed-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest'
)

print("Data storage service started...")

db = SessionLocal()

try:
    for message in consumer:
        event_data = message.value
        print(f"Received processed event: {event_data}")

        # Create a new event record
        db_event = Event(
            event_type=event_data.get('event_type'),
            product_id=event_data.get('product_id'),
            user_id=event_data.get('user_id'),
            processed_at=event_data.get('processed_at'),
            status=event_data.get('status')
        )

        # Add to session and commit
        db.add(db_event)
        db.commit()
        print(f"Stored event id={db_event.id} to database.")
finally:
    db.close()
