from datetime import datetime
import hashlib

def process_event(event_data):
    """Enriches and transforms the event data."""
    # Add a processed timestamp
    event_data['processed_at'] = datetime.utcnow().isoformat()
    
    # Hash the user_id for privacy
    if 'user_id' in event_data:
        event_data['user_id'] = hashlib.sha256(event_data['user_id'].encode()).hexdigest()
        
    event_data['status'] = 'processed'
    return event_data
