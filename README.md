# Cybersecurity Log Analytics with Big Data

University project demonstrating security-data ingestion using Apache Kafka, Apache Flume, Hadoop HDFS, Apache Sqoop and MySQL.

## Current status

| Component | Status |
|---|---|
| Ubuntu + Docker + Compose | Working on reference VM |
| Kafka 4.1.1 (KRaft) | Validated |
| `security-logs` topic | Created with 3 partitions |
| Producer/consumer test | Passed: 3 events produced and consumed |
| Hadoop/HDFS | Pending |
| Flume | Pending |
| MySQL/Sqoop | Pending |
| CIC-IDS2017 preparation | Pending |

Start with [Environment Setup](docs/ENVIRONMENT_SETUP.md), then read [Error Prevention](docs/ERROR_PREVENTION.md) and [Team Tasks](docs/TEAM_TASKS.md).

## Architecture

Three complementary ingestion paths are planned:
1. Security event producer → Kafka topic.
2. Linux-style sample authentication logs → Flume → HDFS.
3. MySQL relational records → Sqoop → HDFS.

HDFS is the intended central storage layer. These are complementary paths, not necessarily one linear pipeline.

**Dataset accuracy:** CIC-IDS2017 primarily contains labelled network traffic/flow records in CSV format. It is not a set of ordinary Linux authentication logs. Synthetic Linux-style logs used for a Flume demonstration must be labelled separately.

## Validated Kafka setup

- Image: `apache/kafka:4.1.1`
- Mode: KRaft, single broker
- Port: `9092`
- Topic: `security-logs`
- Partitions: `3`
- Replication factor: `1`

Replication factor 1 is suitable for a small demo but does not provide broker-level fault tolerance.

## Quick start

```bash
docker compose config
docker compose up -d kafka
docker compose ps
docker compose logs --tail=100 kafka
```

Verify the broker:

```bash
docker exec bigdata-kafka /opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

List topics:

```bash
docker exec bigdata-kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Repository policy

- Pin image and software versions. Never use `latest`.
- Never commit `.env`, passwords, or credentials.
- Do not commit full raw datasets or large generated files.
- Keep small, permitted test samples and scripts in Git.
- Each component owner supplies tested configs, commands, screenshots and version details.

## Git workflow

```bash
git switch -c feature/your-component
git add .
git commit -m "Add component validation"
git push -u origin feature/your-component
```

The project lead reviews changes before merging into `main`.
