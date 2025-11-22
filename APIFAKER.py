from fastapi import FastAPI
from faker_api import Parametros, generar_datos

app = FastAPI()

@app.post("/generar")
def generar(parametros: Parametros):
    resultado = generar_datos(parametros)
    return {"mensaje": resultado}
#Nota: agrega un guion raiz para que no truene
#Nota2: QUE CHINGUE A SU MADRE EL AMERICA
#NOTA3: el bot completador de VSC le cae mal chatgpt JAJAJAJAJAJ

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>🚀 API del Generador de Datos Faker</h2>
    <p>Usa <a href='/docs'>/docs</a> para probar los endpoints.</p>
    """
