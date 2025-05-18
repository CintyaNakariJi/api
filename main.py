from fastapi import FastAPI
from influxdb_client import InfluxDBClient
import os

app = FastAPI()

# Configura tu conexión con variables de entorno
url = os.getenv("INFLUX_URL")
token = os.getenv("INFLUX_TOKEN")
org = os.getenv("INFLUX_ORG")
bucket = os.getenv("INFLUX_BUCKET")

# Crear cliente de InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)

@app.get("/api/datos")
def leer_datos():
    query = f'from(bucket:"{bucket}") |> range(start: -30d)'
    result = client.query_api().query(org=org, query=query)

    datos = []
    for table in result:
        for record in table.records:
            datos.append({
                "time": record.get_time().isoformat(),
                "valor": record.get_value(),
                "medicion": record.get_measurement()
            })
    return {"datos": datos}
