# ETL Pipeline with Apache Kafka for Trading Market Data

This project demonstrates the implementation of an ETL (Extract, Transform, Load) pipeline using Apache Kafka for streaming trading market data. The project is divided into 8 steps (from 00 to 07) to provide an step by step understanding of how a live data streaming system works and how the infrastructure is built. Each step has its own README.md file that explains how to run the code and the schema of the infrastructure at that step.

## Project Overview

The goal of this project is to help individuals learn how to set up a data streaming platform and, also those who want build the infrastructure needed to implement trading data platforms. The project covers the following components and services:

- **Apache Kafka**: For streaming live market data.
- **PostgreSQL**: For OLTP and OLAP databases.
- **Redis**: For caching.
- **Docker**: For Containerization.

## Steps

The project is divided into the following steps:

1. **Step 00**: a very simple yet functional kafka cluster (not actually cluster yet!)
2. **Step 01**: stream real data from a data source with apache kafka (E of ETL)
3. **Step 02**: load streamed data to a database (E&L of ETL)
4. **Step 03**: like step 00 but Containerized all project components
5. **Step 04**: like step  but Containerized all project components
6. **Step 05**: an End to End platform for streaming trading market data with Apache Kafka
7. **Step 06**: Redis get involved for Caching
8. **Step 07**: a very simple ETL pipeline with Apache Kafka

Each step includes a README.md file with detailed instructions on how to run the code and the schema of the infrastructure at that step.

## Getting Started

To get started with this project, follow the instructions provided in each step's README.md file. The instructions will guide you through setting up the environment, running the code, and understanding the infrastructure.

## Prerequisites

Before you begin, ensure you have the following installed:

- Apache Kafka
- PostgreSQL
- Redis
- Docker

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/karrabi/Samplate.git
   cd Samplate/StreamingForexDataWithApacheKafka
   ```

2. Follow the instructions in each step's README.md file to set up the environment and run the code.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the Apache License 2.0
