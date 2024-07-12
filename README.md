# Spark-Pulsar Integration

This repository contains instructions and scripts for integrating Apache Spark with Apache Pulsar. 
The integration allows you to stream data from Pulsar to Spark for real-time processing and analysis.

## Prerequisites

- Docker
- Python 
- Apache Pulsar
- Apache Spark
- Pulsar-Spark-Connector.jar

## Installation
### Step 1: Set-up docker

In the terminal, go to the directory where the docker-compose.yml file is located and then enter the code below.
```sh
docker-compose up -d
```
Additional info:

Enter the code below into the terminal for the pulsar-manager WEB-UI.
```
CSRF_TOKEN=$(curl http://localhost:7750/pulsar-manager/csrf-token)
curl \
   -H 'X-XSRF-TOKEN: $CSRF_TOKEN' \
   -H 'Cookie: XSRF-TOKEN=$CSRF_TOKEN;' \
   -H "Content-Type: application/json" \
   -X PUT http://localhost:7750/pulsar-manager/users/superuser \
   -d '{"name": "admin", "password": "apachepulsar", "description": "test", "email": "username@test.org"}'
```
### Step 2: Install necessary libraries

```sh
pip install pyspark
pip install pulsar-client
```
First, you need to run the integrateSpark.py file and then run the importDatas.py file. 
While the integrateSpark.py file is running, you need to run the importDatas.py file.
Do not stop integrateSpark.py. Then go to where integrateSpark's output is.
Now, you see the datas.
