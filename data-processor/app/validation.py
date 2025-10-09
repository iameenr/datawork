from pydantic import BaseModel

# event model
class Event(BaseModel):
    event_type: str
    product_id: str
    user_id: str