from faker import Faker
import mysql.connector
import random
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


# -------------------------------
# Modelo de parámetros para el API
# -------------------------------
class Parametros(BaseModel):
    nombre_bd: str
    num_tablas: int
    num_registros: int
    modo: str  # "manual" o "servidor"
    host: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None


# -------------------------------
# Función principal de generación
# -------------------------------
def generar_datos(param: Parametros):
    # -------------------------------
    # Límite de seguridad para no generar demasiados datos
    # -------------------------------
    LIMITE_REGISTROS = 100
    mensaje_aviso = ""
    if param.num_registros > LIMITE_REGISTROS:
        mensaje_aviso = f"⚠️ Se ajustó la cantidad máxima a {LIMITE_REGISTROS} registros."
        param.num_registros = LIMITE_REGISTROS

    # -------------------------------
    # Inicialización de Faker y aleatorios
    # -------------------------------
    fake = Faker('es_MX')
    Faker.seed(0)
    random.seed(0)

    # -------------------------------
    # Diccionario de generadores (resumen del original)
    # -------------------------------
    generadores = {
        "nombre": fake.name,
        "email": fake.email,
        "telefono": fake.phone_number,
        "empresa": fake.company,
        "producto": fake.word,
        "precio": lambda: round(random.uniform(10.0, 1000), 2),
        "direccion": fake.address,
        "fecha": fake.date,
        "ciudad": fake.city,
        "pais": fake.country,
        "usuario": fake.user_name,
        "color": fake.color_name,
        "trabajo": fake.job,
        "descripcion": lambda: fake.sentence(nb_words=6),
        "boolean": lambda: random.choice([0, 1]),
        "edad": lambda: random.randint(18, 80),
        "salario": lambda: random.randint(5000, 50000),
        "curp": fake.curp,
        "rfc": fake.rfc,
        "ip": fake.ipv4,
        "url": fake.url,
        "fecha_nacimiento": fake.date_of_birth,
        "marca": lambda: random.choice(["Toyota", "Ford", "Chevrolet", "Honda", "Nissan"]),
        "modelo": lambda: random.choice(["Sedan", "SUV", "Hatchback", "Truck"]),
        "año": lambda: random.randint(1990, 2025),
        "estado": fake.state,
        "curso": lambda: random.choice(["Matemáticas", "Historia", "Ciencia", "Arte"]),
        "calificacion": lambda: random.choice(["A", "B", "C", "D", "F"]),
        "deporte": lambda: random.choice(["Fútbol", "Baloncesto", "Tenis", "Ciclismo"]),
        "marca_ropa": lambda: random.choice(["Nike", "Adidas", "Puma", "Reebok"]),
        "tipo_sangre": lambda: random.choice(["A+", "O-", "B+", "AB-"]),
    }

    # -------------------------------
    # Funciones auxiliares
    # -------------------------------
    def safe_call_generador(func):
        try:
            if func is None:
                return None
            return func()
        except Exception:
            return None

    def sql_literal(value, tipo_col):
        if value is None:
            return "NULL"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, (date, datetime)):
            return f"'{value.strftime('%Y-%m-%d')}'"
        s = str(value).replace("'", "''")
        return f"'{s}'"

    def generar_valor_raw(nombre_col, tipo_col):
        name = nombre_col.lower()
        t = tipo_col.lower()

        if "int" in t or "integer" in t:
            return random.randint(1, 10000)
        if "float" in t or "double" in t or "decimal" in t:
            return round(random.uniform(1.0, 10000.0), 2)
        if "date" in t or "time" in t:
            return safe_call_generador(generadores.get("fecha"))

        for clave, func in generadores.items():
            if clave in name:
                val = safe_call_generador(func)
                if val is not None:
                    return val
        return fake.word()

    # -------------------------------
    # Generación del script SQL
    # -------------------------------
    sql_script = f"CREATE DATABASE IF NOT EXISTS {param.nombre_bd};\nUSE {param.nombre_bd};\n"

    for i in range(param.num_tablas):
        nombre_tabla = f"tabla_{i+1}"
        columnas = [
            "nombre VARCHAR(100)",
            "email VARCHAR(100)",
            "telefono VARCHAR(50)",
            "empresa VARCHAR(100)",
            "precio FLOAT",
            "fecha DATE"
        ]
        sql_script += f"""
CREATE TABLE IF NOT EXISTS {nombre_tabla} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {', '.join(columnas)}
);
"""
        columnas_nombres = ",".join([col.split()[0] for col in columnas])
        for _ in range(param.num_registros):
            valores_raw = [generar_valor_raw(col.split()[0], col.split()[1]) for col in columnas]
            valores_sql = [sql_literal(val, col.split()[1]) for val, col in zip(valores_raw, columnas)]
            sql_script += f"INSERT INTO {nombre_tabla}({columnas_nombres}) VALUES ({','.join(valores_sql)});\n"

    # -------------------------------
    # Modo MANUAL → genera archivo .sql
    # -------------------------------
    if param.modo.lower() == "manual":
        with open("script_generado.sql", "w", encoding="utf-8") as f:
            f.write(sql_script)
        return f"{mensaje_aviso} {param.num_registros} registros generados en {param.num_tablas} tabla(s). Archivo 'script_generado.sql' listo."

    # -------------------------------
    # Modo SERVIDOR → inserta en MySQL
    # -------------------------------
    elif param.modo.lower() == "servidor":
        try:
            conexion = mysql.connector.connect(
                host=param.host,
                user=param.user,
                password=param.password
            )
            cursor = conexion.cursor()
            for query in sql_script.split(';'):
                q = query.strip()
                if q:
                    cursor.execute(q)
            conexion.commit()
            cursor.close()
            conexion.close()
            return f"{mensaje_aviso} {param.num_registros} registros insertados en {param.num_tablas} tabla(s) de la base '{param.nombre_bd}'."
        except Exception as e:
            return f"❌ Error al conectar o insertar en MySQL: {e}"

    # -------------------------------
    # Si el modo no es válido
    # -------------------------------
    else:
        return "⚠️ Modo no válido. Usa 'manual' o 'servidor'."
