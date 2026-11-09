# Team Environment Setup

## Reference VM

- Ubuntu 26.04.1 LTS, x86_64
- 6 vCPU, approximately 7.2 GiB RAM
- 4 GiB swap, 49 GB virtual disk
- Docker Engine 29.1.3
- Docker Compose 2.40.3
- Git 2.53.0
- Python 3.14.4

The VM is resource-constrained for the full stack. Start services one at a time and monitor memory and disk.

## 1. Basic packages

```bash
sudo apt update
sudo apt install -y git curl wget ca-certificates python3 python3-venv python3-pip unzip tar jq
```

## 2. Docker

Install Docker Engine and Compose using the official Ubuntu instructions:
https://docs.docker.com/engine/install/ubuntu/

Verify:

```bash
docker --version
docker compose version
sudo docker run --rm hello-world
```

## 3. Docker permissions

```bash
sudo usermod -aG docker "$USER"
```

Log out of Ubuntu and log back in (or reboot). Then verify:

```bash
groups
docker ps
```

`groups` must include `docker`. If it does not, use `sudo docker ...` temporarily and refresh the login session. If `newgrp` is unavailable, logging out and back in is the simplest solution. The utility can also be installed with `sudo apt install -y util-linux-extra`.

Docker group membership grants effectively root-level control of the host. Use it only for trusted users on the project VM.

## 4. Clone or connect the repository

```bash
git clone <REPOSITORY_URL>
cd cybersecurity-bigdata
```

For an existing local repository instead:

```bash
git remote add origin <REPOSITORY_URL>
git branch -M main
git push -u origin main
```

Replace the placeholder with the actual remote URL.

## 5. Start Kafka

```bash
docker compose config
docker compose up -d kafka
docker compose ps
docker compose logs --tail=100 kafka
```

Check broker:

```bash
docker exec bigdata-kafka /opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

Create topic if needed:

```bash
docker exec bigdata-kafka /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic security-logs --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

Verify topic:

```bash
docker exec bigdata-kafka /opt/kafka/bin/kafka-topics.sh --describe --topic security-logs --bootstrap-server localhost:9092
```

## 6. Producer test

```bash
docker exec -it bigdata-kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic security-logs --producer-property acks=all
```

Paste one JSON event per line:

```json
{"timestamp":"2026-11-09T16:30:00","source_ip":"192.0.2.10","event_type":"FAILED_LOGIN","username":"admin"}
{"timestamp":"2026-11-09T16:31:00","source_ip":"198.51.100.20","event_type":"PORT_SCAN","destination_port":22}
{"timestamp":"2026-11-09T16:32:00","source_ip":"192.0.2.10","event_type":"SUCCESSFUL_LOGIN","username":"analyst"}
```

Press Ctrl+C to stop the producer.

## 7. Consumer test

```bash
docker exec -it bigdata-kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic security-logs --from-beginning --property print.partition=true --property print.offset=true
```

Stop with Ctrl+C. Confirm the three records appear.

Check offsets:

```bash
docker exec bigdata-kafka /opt/kafka/bin/kafka-get-offsets.sh --bootstrap-server localhost:9092 --topic security-logs
```

## 8. Resource checks

```bash
free -h
df -h
docker stats --no-stream
```

Avoid running all Big Data services simultaneously on the 7.2 GiB reference VM.

## 9. Compatibility rule

Kafka 4.1.1 is already validated. Hadoop, Flume, Sqoop, Java and JDBC driver versions must be selected as a compatible set and pinned. Do not independently install the newest version of every component and assume they will work together.
