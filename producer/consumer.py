import json
from kafka import KafkaConsumer

# ==============================
# Kafka Connection (choose one)
# ==============================

# If running LOCALLY:
KAFKA_BOOTSTRAP_SERVER = "localhost:9094"


TOPICS = [
    "market-prices",
    "market-volume",
    "market-sentiment"
]

consumer = KafkaConsumer(
    *TOPICS,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Listening to Kafka topics...\n")

for message in consumer:
    print("--------------------------------------------------")
    print(f"Topic   : {message.topic}")
    print(f"Offset  : {message.offset}")
    print(f"Payload : {message.value}")
