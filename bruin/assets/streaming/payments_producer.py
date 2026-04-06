import csv
import os
from pathlib import Path

# Simple Kafka producer to stream payment records.

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "olist-payments")
SOURCE_FILE = Path(os.getenv("PAYMENTS_CSV", "data/raw/olist_order_payments_dataset.csv"))
MAX_ROWS = int(os.getenv("MAX_ROWS", "1000"))


def main() -> None:
    try:
        from kafka import KafkaProducer
    except ImportError as exc:
        raise SystemExit("Missing dependency: kafka-python. Install with `pip install kafka-python`.") from exc

    if not SOURCE_FILE.exists():
        raise SystemExit(f"Source file not found: {SOURCE_FILE}")

    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

    with SOURCE_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for idx, row in enumerate(reader, start=1):
            producer.send(TOPIC, value=str(row).encode("utf-8"))
            if idx >= MAX_ROWS:
                break

    producer.flush()
    print(f"Published {min(MAX_ROWS, idx)} rows to {TOPIC}")


if __name__ == "__main__":
    main()
