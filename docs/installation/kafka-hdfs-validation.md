# Kafka → HDFS Integration Validation

## 1. Overview

This component implements a streaming ingestion pipeline that transfers cybersecurity events from Apache Kafka into Hadoop Distributed File System (HDFS).

### Architecture

Security Event Producer → Kafka Topic (`security-logs`) → Python Kafka Consumer → HDFS

## 2. Environment

| Component | Version |
|---|---|
| Apache Kafka | 4.1.1 |
| Python | 3.14.4 |
| kafka-python | 3.0.13 |
| Hadoop | 3.3.6 |
| Operating System | Ubuntu 26.04.1 LTS |

## 3. Python Dependencies

A Python virtual environment is used to isolate dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install kafka-python
```

## 4. Kafka Configuration

- Broker: `localhost:9092`
- Topic: `security-logs`
- Partitions: 3
- Replication factor: 1
- Consumer group: `security-hdfs-consumer`

## 5. HDFS Destination

Events are stored under:

```text
/cybersecurity/raw/kafka/
```

The output directory uses date-based partitioning:

```text
year=YYYY/month=MM/day=DD/
```

Output files use JSON Lines format (`.jsonl`).

## 6. Consumer Implementation

The Python consumer:

1. Connects to the Kafka broker.
2. Subscribes to `security-logs`.
3. Receives JSON security events.
4. Collects events into batches.
5. Flushes a batch when it reaches 10 events or after 5 seconds.
6. Writes the batch to HDFS.
7. Commits Kafka offsets after successful HDFS persistence.

The consumer supports continuous operation and graceful shutdown using Ctrl+C.

## 7. Execution

Start the consumer:

```bash
python scripts/kafka/kafka_to_hdfs.py
```

Produce test events:

```bash
docker exec -i bigdata-kafka /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic security-logs
```

Example event:

```json
{"event_id":"FINAL-TEST-001","event_type":"BRUTE_FORCE","severity":"CRITICAL","source_ip":"192.0.2.201"}
```

## 8. Validation Results

The integration was tested using synthetic cybersecurity events.

| Test | Result |
|---|---|
| Kafka connectivity | PASS |
| Topic subscription | PASS |
| Consumer group assignment | PASS |
| JSON event processing | PASS |
| Batch processing | PASS |
| HDFS directory creation | PASS |
| HDFS file writing | PASS |
| Kafka offset commit | PASS |
| HDFS read-back verification | PASS |
| Graceful shutdown | PASS |

Final test events verified in HDFS:

- `FINAL-TEST-001`: BRUTE_FORCE, CRITICAL
- `FINAL-TEST-002`: SUSPICIOUS_TRAFFIC, HIGH

## 9. Evidence

Evidence files:

```text
docs/evidence/kafka/
├── hdfs-directory-listing.txt
└── kafka-hdfs-output.jsonl
```

## 10. Limitations

- The demonstration uses one Kafka broker.
- Replication factor is 1, so broker failure can cause data unavailability.
- The HDFS cluster uses one DataNode and replication factor 1.
- Delivery semantics are at-least-once, not exactly-once. A failure after HDFS persistence but before Kafka offset commit can result in duplicate records.
- The demonstration events are synthetic and are not real security incidents.

## 11. Conclusion

The Kafka-to-HDFS integration was successfully implemented and validated. Security events published to Kafka were consumed by the Python application, grouped into batches, persisted in HDFS, and verified through HDFS read-back operations.
