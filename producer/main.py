import json
import time
import logging
import random
from datetime import datetime
from kafka import KafkaProducer

# ------------------------------
# CONFIGURATION (Matches your Docker Compose)
# ------------------------------

KAFKA_BOOTSTRAP_SERVER = "localhost:9094"   # INTERNAL Docker network address
TOPIC_PRICES = "market-prices"
TOPIC_VOLUME = "market-volume"
TOPIC_SENTIMENT = "market-sentiment"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=5
)

# Logging
logging.basicConfig(level=logging.INFO)


# ------------------------------------------------
# MOCK API DATA (Replace later with real API calls)
# ------------------------------------------------
def fetch_market_data():
    """
    Simulates real-time stock market API data.
    Replace this later with your actual API.
    """
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "ticker": random.choice(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]),
        "price": round(random.uniform(100, 300), 2),
        "volume": random.randint(1000, 50000),
        "sentiment_score": round(random.uniform(-1, 1), 3)
    }
    return data


# ----------------------------------------------
# STREAM DATA TO KAFKA (REAL-TIME LOOP)
# ----------------------------------------------
def stream_to_kafka():
    logging.info("Starting real-time data streaming to Kafka...")

    while True:
        market_data = fetch_market_data()

        # Send to different Kafka topics
        producer.send(TOPIC_PRICES, {
            "timestamp": market_data["timestamp"],
            "ticker": market_data["ticker"],
            "price": market_data["price"]
        })

        producer.send(TOPIC_VOLUME, {
            "timestamp": market_data["timestamp"],
            "ticker": market_data["ticker"],
            "volume": market_data["volume"]
        })

        producer.send(TOPIC_SENTIMENT, {
            "timestamp": market_data["timestamp"],
            "ticker": market_data["ticker"],
            "sentiment": market_data["sentiment_score"]
        })

        logging.info(f"Published: {market_data}")

        # Simulate real-time streaming every 2 seconds
        time.sleep(2)


if __name__ == "__main__":
    stream_to_kafka()
