from datetime import datetime
import hashlib

def process_event(event_data):
    # process the event
    event_data['processed_at'] = datetime.utcnow().isoformat()
    event_data['status'] = 'processed'
    
    if 'user_id' in event_data:
        event_data['user_id'] = hashlib.sha256(event_data['user_id'].encode()).hexdigest()
        
    return event_data