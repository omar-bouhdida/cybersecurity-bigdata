from kafka import KafkaConsumer

consumer = KafkaConsumer(
    bootstrap_servers=["localhost:9092"],
    request_timeout_ms=10000
)

print("Successfully connected to Kafka!")
print("Available topics:", consumer.topics())

consumer.close()
