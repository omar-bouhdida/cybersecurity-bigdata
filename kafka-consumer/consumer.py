#!/usr/bin/env python3
"""Kafka -> HDFS consumer (at-least-once).

Lit le topic security-logs, regroupe les messages en lots, ecrit chaque lot
dans un nouveau fichier HDFS, puis valide les offsets APRES l'ecriture.
"""
import os
import signal
import subprocess
import tempfile
import time
from datetime import datetime

from kafka import KafkaConsumer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "security-logs")
GROUP = os.getenv("KAFKA_GROUP", "hdfs-writer")
HDFS_DIR = os.getenv("HDFS_DIR", "/cybersecurity/raw/kafka")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
BATCH_SECONDS = float(os.getenv("BATCH_SECONDS", "10"))

running = True


def stop(*_):
    global running
    running = False


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)


def write_batch(lines):
    """Ecrit un lot dans un nouveau fichier HDFS. Leve une exception en cas d'echec."""
    day = datetime.now().strftime("%Y-%m-%d")
    name = f"security-logs-{datetime.now().strftime('%H%M%S%f')}.jsonl"
    hdfs_dir = f"{HDFS_DIR}/{day}"
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", hdfs_dir], check=True)
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as tmp:
        tmp.write("\n".join(lines) + "\n")
        tmp_path = tmp.name
    try:
        subprocess.run(["hdfs", "dfs", "-put", tmp_path, f"{hdfs_dir}/{name}"], check=True)
    finally:
        os.remove(tmp_path)
    return f"{hdfs_dir}/{name}"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id=GROUP,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda b: b.decode("utf-8"),
    )
    print(f"Consumer started: topic={TOPIC} group={GROUP} -> {HDFS_DIR}", flush=True)

    batch = []
    last_flush = time.time()

    def flush():
        nonlocal batch, last_flush
        if batch:
            try:
                path = write_batch(batch)
            except Exception as exc:
                print(f"HDFS write failed, offsets NOT committed: {exc}", flush=True)
                return  # on garde le lot, on reessaie au prochain tour
            consumer.commit()  # commit seulement apres ecriture reussie
            print(f"Wrote {len(batch)} events -> {path}", flush=True)
            batch = []
        last_flush = time.time()

    while running:
        records = consumer.poll(timeout_ms=1000)
        for msgs in records.values():
            for msg in msgs:
                batch.append(msg.value)
        if len(batch) >= BATCH_SIZE or (batch and time.time() - last_flush >= BATCH_SECONDS):
            flush()

    flush()  # vidage final a l'arret propre
    consumer.close()
    print("Consumer stopped.", flush=True)


if __name__ == "__main__":
    main()
