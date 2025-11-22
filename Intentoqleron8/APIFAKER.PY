from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from scripfaker import generar_datos
import uvicorn

app = FastAPI()

# -------------------------------
# MODELO DE PETICIÓN DESDE MENDIX
# -------------------------------
class GenerarRequest(BaseModel):
    nombre_bd: str
    num_tablas: int
    num_registros: int
    modo: str                  # "manual" o "servidor"
    host: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None


# -------------------------------
# ENDPOINT PRINCIPAL
# -------------------------------
@app.post("/generar")
def generar(request: GenerarRequest):

    try:
        resultado = generar_datos(
            nombre_bd=request.nombre_bd,
            num_tablas=request.num_tablas,
            num_registros=request.num_registros,
            modo=request.modo,
            host=request.host,
            user=request.user,
            password=request.password
        )

        # Construimos JSON estructurado
        respuesta = {
            "status": "ok",
            "modo": request.modo,
            "tablas_generadas": request.num_tablas,
            "registros_por_tabla": request.num_registros,
            "script_sql": resultado.get("script", None),
            "errores": None
        }

    except Exception as e:
        respuesta = {
            "status": "error",
            "errores": str(e)
        }

    return respuesta


@app.get("/")
def root():
    return {"mensaje": "API Faker funcionando correctamente"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
