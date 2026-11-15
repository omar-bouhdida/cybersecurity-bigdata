import json
import subprocess
import logging
import time

from datetime import datetime, timezone
from pathlib import Path

from kafka import KafkaConsumer


# ==========================================
# CONFIGURATION
# ==========================================

KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
KAFKA_TOPIC = "security-logs"
KAFKA_GROUP_ID = "security-hdfs-consumer"

HDFS_BASE_PATH = "/cybersecurity/raw/kafka"

BATCH_SIZE = 10
BATCH_TIMEOUT = 5
POLL_TIMEOUT_MS = 1000


# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.getLogger("kafka").setLevel(logging.WARNING)


# ==========================================
# HDFS WRITER
# ==========================================

def write_to_hdfs(events):

    now = datetime.now(timezone.utc)

    timestamp = now.strftime("%Y%m%d_%H%M%S_%f")

    local_file = Path(f"/tmp/kafka_batch_{timestamp}.jsonl")

    hdfs_directory = (
        f"{HDFS_BASE_PATH}/"
        f"year={now.strftime('%Y')}/"
        f"month={now.strftime('%m')}/"
        f"day={now.strftime('%d')}"
    )

    hdfs_file = (
        f"{hdfs_directory}/security-events-{timestamp}.jsonl"
    )

    try:
        with local_file.open("w", encoding="utf-8") as file:
            for event in events:
                file.write(
                    json.dumps(event, ensure_ascii=False) + "\n"
                )

        subprocess.run(
            ["hdfs", "dfs", "-mkdir", "-p", hdfs_directory],
            check=True,
            capture_output=True,
            text=True
        )

        subprocess.run(
            ["hdfs", "dfs", "-put", str(local_file), hdfs_file],
            check=True,
            capture_output=True,
            text=True
        )

        logging.info(
            "Successfully wrote %d events to HDFS: %s",
            len(events),
            hdfs_file
        )

    except subprocess.CalledProcessError as error:
        logging.error("HDFS operation failed: %s", error.stderr)
        raise

    finally:
        local_file.unlink(missing_ok=True)


# ==========================================
# KAFKA CONSUMER
# ==========================================

def main():

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        enable_auto_commit=False,
        auto_offset_reset="earliest"
    )

    consumer.subscribe([KAFKA_TOPIC])

    logging.info("Kafka consumer started.")
    logging.info("Topic: %s", KAFKA_TOPIC)
    logging.info("Consumer group: %s", KAFKA_GROUP_ID)
    logging.info("Batch size: %d", BATCH_SIZE)
    logging.info("Batch timeout: %d seconds", BATCH_TIMEOUT)

    batch = []
    last_flush = time.monotonic()

    try:

        while True:

            remaining = BATCH_SIZE - len(batch)

            records = consumer.poll(
                timeout_ms=POLL_TIMEOUT_MS,
                max_records=remaining
            )

            for messages in records.values():

                for message in messages:

                    event = json.loads(
                        message.value.decode("utf-8")
                    )

                    batch.append(event)

            elapsed = time.monotonic() - last_flush

            if batch and (
                len(batch) >= BATCH_SIZE
                or elapsed >= BATCH_TIMEOUT
            ):

                logging.info(
                    "Flushing batch containing %d events...",
                    len(batch)
                )

                # Write to HDFS before committing Kafka offsets.
                write_to_hdfs(batch)

                consumer.commit()

                logging.info("Kafka offsets committed successfully.")

                batch.clear()
                last_flush = time.monotonic()

    except KeyboardInterrupt:

        logging.info("Shutdown requested.")

        if batch:

            logging.info(
                "Flushing remaining %d events...",
                len(batch)
            )

            write_to_hdfs(batch)

            consumer.commit()

            logging.info("Final batch persisted and offsets committed.")

    finally:

        consumer.close()

        logging.info("Kafka consumer stopped.")


if __name__ == "__main__":
    main()
