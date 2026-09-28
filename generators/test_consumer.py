from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    "telecom_voice_cdr",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="test-group-1",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)


print("Waiting for messages...")


for message in consumer:
    print(
        "Partition:",
        message.partition,
        "Offset:",
        message.offset
    )
    print(message.value)