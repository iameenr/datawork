from pydantic import BaseModel

class Event(BaseModel):
    event_type: str
    product_id: str
    user_id: str
