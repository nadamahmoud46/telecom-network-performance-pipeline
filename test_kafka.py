from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

message = {
    "cdr_id": 1,
    "cell_id": "CELL001",
    "technology": "4G",
    "duration_seconds": 120
}

future = producer.send(
    "telecom_voice_cdr",
    value=message
)

print(future.get(timeout=10))

producer.flush()
producer.close()

print("Message sent successfully")