# Kafka Installation and Validation

## Environment
- Platform: Ubuntu 26.04.1 LTS
- Deployment: Docker Compose
- Kafka version: 4.1.1
- Kafka mode: KRaft
- Broker: bigdata-kafka
- Port: 9092

## Topic configuration
- Topic: security-logs
- Partitions: 3
- Replication factor: 1

## Functional tests
1. Kafka broker startup: SUCCESS
2. Topic creation: SUCCESS
3. Topic description: SUCCESS
4. Producer test: SUCCESS
5. Consumer test: SUCCESS
6. Message persistence: SUCCESS

## Test events
- FAILED_LOGIN
- PORT_SCAN
- SUCCESSFUL_LOGIN

## Final result
Three security events were successfully produced,
stored in Kafka partition 2, and consumed.

## Limitation
The demonstration uses one Kafka broker with replication
factor 1. It demonstrates event streaming but does not
provide broker-level fault tolerance.
