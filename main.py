from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from influxdb_client import InfluxDBClient
import os
from collections import defaultdict

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

    datos_dict = defaultdict(dict)

    for record in table.records:
        time_obj = record.get_time().replace(microsecond=0)
        time_str = time_obj.isoformat()
        datos_dict[time_str]["time"] = time_str
        valor = record.get_value()
        if isinstance(valor, (int, float)):
            valor = round(valor, 2)
        datos_dict[time_str][record.get_measurement()] = valor

    datos = []
    for i, data in enumerate(sorted(datos_dict.values(), key=lambda x: x["time"])):
        data["id"] = i + 1
        datos.append(data)

    return datos
