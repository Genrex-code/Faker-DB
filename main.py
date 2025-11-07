from fastapi import FastAPI
from faker_api import Parametros, generar_datos

app = FastAPI()

@app.post("/generar")
def generar(parametros: Parametros):
    resultado = generar_datos(parametros)
    return {"mensaje": resultado}
