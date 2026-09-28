# Telecom Network Performance Pipeline 

A data engineering project designed to simulate and process large-scale telecom network data using both batch and streaming pipelines.

The project focuses on building a scalable data pipeline for telecom customer, subscription, call, internet usage, and network performance data.

**«Project Status:** Work in Progress
**Current implementation:** Data generation, ingestion, Bronze layer, and Silver-layer processing
**Next phase:** Gold-layer modeling and analytics/visualization»

---

## Architecture

                         Python Data Generators
                                  |
                    +-------------+-------------+
                    |                           |
              Batch Generator            Streaming Generator
                    |                           |
              Parquet Files                JSON Events
                    |                           |
                PostgreSQL                    Kafka
                    |                           |
                    +-------------+-------------+
                                  |
                                 NiFi
                                  |
                                 HDFS
                                  |
                           Bronze Layer
                                  |
                         Spark Processing
                    Cleaning + Validation
                                  |
                           Silver Layer
                                  |
                    -------------------------
                    |                       |
                Gold Layer             Analytics
                    |                       |
              Hive / Iceberg           Power BI
                    |
                 Airflow

The architecture combines batch and streaming data ingestion into a layered data processing pipeline.

---

## Project Objectives

**The main objectives of this project are to:**

- Generate realistic synthetic telecom data at scale.
- Build both batch and streaming data pipelines.
- Process telecom customer and network-related data.
- Ingest streaming events using Kafka.
- Use Apache NiFi for data movement and ingestion.
- Store raw data in HDFS as part of the Bronze layer.
- Process and validate data using Apache Spark.
- Prepare cleaned data for analytical processing in the Silver layer.
- Design a foundation for Gold-layer modeling and BI analytics.

---

## Database Schema

**Customers**

customer_id
gender
birth_date
segment
city_id

**Plans**

plan_id
plan_name
price
internet_gb
voice_minutes
plan_type

**Subscriptions**

subscription_id
customer_id
plan_id
msisdn
activation_date
status
subscription_type

**Cities**

city_id
city_name
region
latitude
longitude

**Cell Towers**

cell_id
technology
latitude
longitude
city_id

**Voice CDR**

cdr_id
subscription_id
start_time
duration_seconds
cell_id
technology
call_status
termination_cause

**Data CDR**

cdr_id
subscription_id
session_start
session_end
uploaded_mb
downloaded_mb
cell_id
technology
throughput_mbps

**Network Performance**

timestamp
cell_id
technology
availability
throughput_dl
throughput_ul
latency_ms
packet_loss
traffic_gb
active_users

---

## Batch Pipeline

**The batch pipeline generates relatively static and historical datasets such as:**

- Customers
- Plans
- Subscriptions
- Cities
- Cell Towers

The generated batch data is written to files and/or PostgreSQL before being processed through the ingestion pipeline.

---

## Streaming Pipeline

**The streaming pipeline simulates real-time telecom events such as:**

- Voice CDR events
- Data usage events
- Network performance metrics

Streaming events are generated as JSON events and sent through Kafka.

The streaming generators include:

stream_voice_cdr.py
stream_data_cdr.py
stream_network_performance.py

Supporting modules handle database interaction, distributions, and streaming utilities.

---

## Data Processing

**Bronze Layer**

The Bronze layer stores the ingested raw data in HDFS.

The purpose of this layer is to preserve the incoming data before applying transformations.

**Silver Layer**

Spark is used to process the Bronze data.

The current processing stage includes:

- Data cleaning
- Data validation
- Transformation
- Preparing structured data for downstream analytical processing

The project currently reaches the Silver layer.

---

**Planned Gold Layer**

The next phase of the project is to build the Gold layer for analytical use cases.

Planned components include:

- Dimensional modeling
- Fact and dimension tables
- Telecom network performance KPIs
- Aggregations by city, tower, technology, and time
- Hive / Apache Iceberg integration
- Power BI dashboards
- Airflow orchestration

---

**Potential Analytics**

The final analytical layer is intended to support telecom network performance analysis such as:

- Network availability
- Average latency
- Packet loss
- Download and upload throughput
- Traffic volume
- Active users
- Network performance by technology
- Network performance by city
- Cell tower performance
- Voice call success/failure analysis
- Data usage patterns

---

## Project Structure

telecom-network-performance-pipeline/
│
├── generators/
│   ├── batch/
│   │   ├── generate_cities.py
│   │   ├── generate_city_towers.py
│   │   ├── generate_customers.py
│   │   ├── generate_plans.py
│   │   └── generate_subscriptions.py
│   │
│   ├── streaming/
│   │   ├── stream_data_cdr.py
│   │   ├── stream_db.py
│   │   ├── stream_distributions.py
│   │   ├── stream_network_performance.py
│   │   ├── stream_utils.py
│   │   └── stream_voice_cdr.py
│   │
│   ├── config.py
│   ├── test_consumer.py
│   ├── test_producer.py
│   └── __init__.py
│
├── db.py
├── main.py
├── requirements.txt
├── docker-compose configuration
│
├── test_connection.py
├── test_db.py
├── test_kafka.py
└── test_psycopg.py

---

## Technologies

- Python
- PostgreSQL
- Apache Kafka
- Apache NiFi
- HDFS
- Apache Spark
- Docker
- Hive / Apache Iceberg (planned)
- Apache Airflow (planned)
- Power BI (planned)

---

## Current Status

**Implemented**

- [x] Synthetic telecom data generation
- [x] Batch data generation
- [x] Streaming data generation
- [x] PostgreSQL integration
- [x] Kafka streaming
- [x] NiFi-based ingestion
- [x] HDFS storage
- [x] Bronze layer
- [x] Spark processing
- [x] Data cleaning and validation
- [x] Silver layer

**Planned**

- [ ] Gold layer
- [ ] Dimensional modeling
- [ ] Hive / Iceberg tables
- [ ] Airflow orchestration
- [ ] Power BI dashboards
- [ ] Final analytical KPIs

---

## Documentation

Additional project documentation and screenshots are available in the "docs/" directory.

---

Notes

This project uses synthetically generated data for educational and portfolio purposes. It does not contain real telecom customer or network data.

The project is currently a work in progress, with the implementation completed through the Silver layer.
