# main.py
from fastapi import FastAPI
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os

app = FastAPI()

# Configura tu conexión
url = os.getenv("https://us-east-1-1.aws.cloud2.influxdata.com")
token = os.getenv("7QJseS0ubDwewDVp7F4j2CwJLI8Gncesop0J6lyQnH-EiUv8BgeHSHtjqb_4td5l4LKAPqLLVxygFOWYe-svWQ==")
org = os.getenv("Trabajos")
bucket = os.getenv("Monitoreo_de_cultivos_maiz")

client = InfluxDBClient(url=url, token=token, org=org)

@app.get("/api/datos")
def leer_datos():
    query = f'from(bucket:"{bucket}") |> range(start: -7d)'
    result = client.query_api().query(org=org, query=query)
    
    datos = []
    for table in result:
        for record in table.records:
            datos.append({
                "time": record.get_time().isoformat(),
                "valor": record.get_value(),
                "medicion": record.get_measurement()  # <--- esto es lo nuevo
            })
    return {"datos": datos}
