# MarketPulse Analytics — Real-Time Financial Data Pipeline

## Company Overview  

**Company Name:** MarketPulse Analytics  
**Location:** New York City, USA  
**Industry:** FinTech, Financial Data Analytics  
**Founded:** 2016  

MarketPulse Analytics is a leading financial technology firm specializing in real-time market insights for institutional investors. The company provides actionable financial data to hedge funds, asset managers, and investment entities. With a focus on delivering timely and relevant data, MarketPulse enables clients to make quick, informed decisions that maximize returns and minimize risks.

---

## Project Overview  

This repository implements a **scalable, real-time financial data pipeline** using Apache Kafka, Apache Spark, and PostgreSQL, containerized with Docker and visualized in Power BI.

The system streams market data through Kafka, processes it in Spark, stores it in PostgreSQL, and exposes insights through dashboards.

---

## Project Objectives  

The primary objectives of this project are:

1. **Develop a scalable data pipeline** using Apache Kafka and Apache Spark.  
2. **Enable real-time analytics** for continuous market data streams.  
3. **Reduce processing latency** to support faster trading decisions.  
4. **Deliver actionable insights** through real-time Power BI dashboards.

---

## System Architecture 
![Data Pipeline Architecture](/img/Data%20pipeline.png)

Figure: Real-time streaming architecture using Kafka for ingestion, Spark for processing, PostgreSQL for persistence, and Power BI for visualization — all orchestrated via Docker Compose on a shared stock_data network.

---

## Technology Stack  

- **Python** — Data ingestion, processing, and streaming applications  
- **Apache Kafka** — Real-time event streaming  
- **Apache Spark** — Distributed real-time analytics  
- **PostgreSQL** — Persistent storage for processed data  
- **Docker & Docker Compose** — Orchestration and containerization  
- **Kafka UI** — Web-based monitoring of Kafka  
- **pgAdmin** — Web interface for PostgreSQL  
- **Power BI** — Business intelligence dashboards  

---

# 🚀 SETUP AND INSTALLATION  

## Prerequisites  

Install the following before proceeding:

- Docker Desktop  
  https://www.docker.com/products/docker-desktop/

- Git  
  https://git-scm.com/

- Power BI Desktop  
  https://www.microsoft.com/en-us/power-platform/products/power-bi/desktop

---

## 1. Clone the Repository  

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

---

## 2. Build and Start All Services  

From the project root, run:

```bash
docker compose up -d --build
```

This will launch:

- **spark-master**
- **spark-worker**
- **kafka**
- **kafka-ui**
- **consumer (your streaming app)**
- **postgres**
- **pgadmin**

Check that everything is running:

```bash
docker ps
```

You should see containers named:

- `spark-master`
- `spark-worker`
- `kafka`
- `kafka-ui`
- `consumer`
- `postgres_db`
- `pgadmin`

---

## 3. Verify Apache Spark  

Open Spark Master UI in your browser:

```
http://localhost:8081
```

Confirm that:

- The master is running  
- At least one worker (`spark-worker`) appears as connected  

---

## 4. Verify Kafka  

### Kafka Bootstrap Servers

From inside Docker containers use:

```
kafka:9092
```

From your local machine use:

```
localhost:9094
```

### List topics (inside container)

```bash
docker exec -it kafka kafka-topics.sh \
  --list --bootstrap-server kafka:9092
```

### Create a topic manually (optional)

```bash
docker exec -it kafka kafka-topics.sh \
  --create --topic market-data \
  --bootstrap-server kafka:9092 \
  --partitions 3 \
  --replication-factor 1
```

---

## 5. Use Kafka Web UI  

Open in browser:

```
http://localhost:8085
```

You can:

- View topics  
- Inspect messages  
- Monitor consumer groups  
- Track partitions and offsets  

---

## 6. Verify PostgreSQL  

### Connect via pgAdmin  

Open:

```
http://localhost:5050
```

Login:

- Email: `admin@admin.com`  
- Password: `admin`

Create a new server with:

- Host: `postgres_db`
- Port: `5432`
- Database: `stock_data`
- Username: `admin`
- Password: `admin`

---

### Or connect via terminal  

```bash
docker exec -it postgres_db psql -U admin -d stock_data
```

List tables:

```sql
\dt;
```

---

# 📘 USAGE EXAMPLES  

## Example 1 — Send Data to Kafka (Python Producer)

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9094'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sample_data = {
    "ticker": "AAPL",
    "price": 175.32,
    "volume": 12000,
    "sentiment": 0.78
}

producer.send("market-data", sample_data)
producer.flush()
```

This sends real-time market data into Kafka.

---

## Example 2 — Read Kafka Stream in Spark (PySpark)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MarketPulseStreaming") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "market-data") \
    .load()

df.writeStream \
  .format("console") \
  .start() \
  .awaitTermination()
```

This runs inside the **consumer container** and processes data in real time.

---

## Example 3 — Write Processed Data to PostgreSQL  

```python
df.write \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://postgres_db:5432/stock_data") \
  .option("dbtable", "market_data") \
  .option("user", "admin") \
  .option("password", "admin") \
  .mode("append") \
  .save()
```

This stores analytics results in PostgreSQL.

---

## 7. Connect Power BI to PostgreSQL  

Open Power BI Desktop and select:

- Get Data → PostgreSQL  

Use:

- Server: `localhost`
- Port: `5434`
- Database: `stock_data`
- Username: `admin`
- Password: `admin`

Load table `market_data` and build dashboards for:

- Stock price trends  
- Trading volume  
- Market sentiment  

---

## Stopping the System  

To shut everything down:

```bash
docker compose down
```

To remove all stored data:

```bash
docker compose down -v
```

---

## Expected Outcomes  

- Scalable real-time data pipeline  
- Low-latency streaming analytics  
- Interactive dashboards in Power BI  
- Reliable data persistence in PostgreSQL  

---

## Skills Developed  

- Real-time data engineering with Kafka and Spark  
- Distributed computing  
- Docker-based microservices  
- Streaming analytics  
- BI visualization with Power BI  

---

## Acknowledgement   


