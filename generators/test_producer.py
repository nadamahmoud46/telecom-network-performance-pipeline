from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

print(producer.bootstrap_connected())

future = producer.send(
    "telecom_voice_cdr",
    {"test": "hello"}
)

print(future.get(timeout=10))

producer.close()