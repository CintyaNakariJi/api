# main.py
from fastapi import FastAPI
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

app = FastAPI()

# Configura tu conexión
token = "domhk2ocatn5DOrGdYgw_BBm3CZlaFtkxE_4HzGaRy7EvoG9Df3x6f7EvZ3ZXiebKwL0oec2Uh6WYCjvtmpREQ=="
org = "Trabajos"
bucket = "maiz"
url = "http://localhost:8086"

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
