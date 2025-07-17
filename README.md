# E-commerce Data Processing Framework

This framework is a scalable, end-to-end data processing pipeline for an e-commerce website. It includes services for generating dummy events, collecting, processing, and storing them.

## Architecture

The framework is built using a microservices architecture, orchestrated with Docker Compose.

- **Event Generator:** A Python service that continuously generates dummy e-commerce events (e.g., `page_view`, `add_to_cart`, `purchase`) to simulate a real-time data stream.

- **Event Collector:** A FastAPI service that provides a REST API endpoint to collect the event data and publishes it to a `raw-events` Kafka topic.

- **Data Processor:** A Python service that consumes events from the `raw-events` topic. It performs the following actions:
    - **Validation:** Uses Pydantic to validate events against a defined schema.
    - **Enrichment:** Adds a `processed_at` timestamp to valid events.
    - **Routing:** Publishes valid events to a `processed-events` topic. Invalid events are sent to a `dead-letter-queue` topic for later analysis.

- **Data Storage:** A Python service that consumes events from the `processed-events` topic and stores them in a SQLite database.

## How to Run

1. **Build and run the services:**

   ```bash
   docker-compose up --build
   ```
   This command will start all the services. The `event-generator` will automatically start sending events. You will see logs from all services in your terminal.

2. **Check the processed data:**

   The `data-storage` service stores the processed events in a SQLite database file named `processed_events.db`. To query the database, you can run:

   ```bash
   docker-compose exec data-storage sqlite3 /app/processed_events.db "SELECT * FROM events ORDER BY id DESC LIMIT 5;"
   ```

3. **Observing the Dead-Letter Queue:**

   The `data-processor` will log any validation or processing errors and route the problematic events to the `dead-letter-queue`. You can monitor the logs of the `data-processor` to see this in action:

   ```bash
   docker-compose logs -f data-processor
   ```
   (To test this, you could temporarily modify the `event-generator` to send an invalid event, e.g., one missing a required field).
