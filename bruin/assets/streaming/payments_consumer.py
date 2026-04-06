import os
from pathlib import Path

# Simple Kafka consumer to persist streamed payments for downstream loading.

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "olist-payments")
SINK_PATH = Path(os.getenv("STREAM_SINK", "data/stream/payments.jsonl"))
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", "1000"))


def main() -> None:
    try:
        from kafka import KafkaConsumer
    except ImportError as exc:
        raise SystemExit("Missing dependency: kafka-python. Install with `pip install kafka-python`.") from exc

    SINK_PATH.parent.mkdir(parents=True, exist_ok=True)

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    count = 0
    with SINK_PATH.open("a", encoding="utf-8") as handle:
        for message in consumer:
            handle.write(message.value.decode("utf-8") + "\n")
            count += 1
            if count >= MAX_MESSAGES:
                break

    print(f"Consumed {count} messages into {SINK_PATH}")


if __name__ == "__main__":
    main()
