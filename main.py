from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from influxdb_client import InfluxDBClient
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables de entorno
url = os.getenv("INFLUX_URL")
token = os.getenv("INFLUX_TOKEN")
org = os.getenv("INFLUX_ORG")
bucket = os.getenv("INFLUX_BUCKET")

# Cliente InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)

@app.get("/api/datos")
def leer_datos():
    query = f'from(bucket:"{bucket}") |> range(start: -30d)'
    result = client.query_api().query(org=org, query=query)

    datos = []

    for table in result:
        for record in table.records:
            datos.append({
                "medicion": record.get_measurement(),
                "valor": record.get_value(),
                "time": record.get_time().isoformat()
            })

    return datos
