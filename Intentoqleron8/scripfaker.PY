from faker import Faker
import mysql.connector
from datetime import datetime
import random

fake = Faker("es_MX")


def generar_datos(nombre_bd, num_tablas, num_registros, modo, host=None, user=None, password=None):

    if num_registros > 100:
        raise ValueError("No puedes generar más de 100 registros por tabla.")

    script_sql = []
    tablas_generadas = 0

    columnas = [
        "nombre VARCHAR(100)",
        "email VARCHAR(120)",
        "telefono VARCHAR(20)",
        "empresa VARCHAR(100)",
        "precio FLOAT",
        "fecha DATE"
    ]

    # Si es modo servidor intentamos conectar
    conexion = None
    cursor = None

    if modo == "servidor":
        if not host or not user or not password:
            raise ValueError("Modo servidor requiere host, user y password.")

        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conexion.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_bd}")
        cursor.execute(f"USE {nombre_bd}")

    # Generamos tablas
    for i in range(1, num_tablas + 1):

        nombre_tabla = f"tabla_{i}"

        sql_crear = f"CREATE TABLE {nombre_tabla} ({', '.join(columnas)});"
        script_sql.append(sql_crear)

        if modo == "servidor":
            cursor.execute(sql_crear)

        # Inserts
        for _ in range(num_registros):

            nombre = fake.name()
            email = fake.email()
            telefono = fake.phone_number()
            empresa = fake.company()
            precio = round(random.uniform(10, 5000), 2)
            fecha = datetime.now().strftime("%Y-%m-%d")

            sql_insert = (
                f"INSERT INTO {nombre_tabla} "
                f"(nombre, email, telefono, empresa, precio, fecha) VALUES "
                f"('{nombre}', '{email}', '{telefono}', '{empresa}', {precio}, '{fecha}');"
            )

            script_sql.append(sql_insert)

            if modo == "servidor":
                cursor.execute(sql_insert)

        tablas_generadas += 1

    if conexion:
        conexion.commit()
        conexion.close()

    return {
        "script": "\n".join(script_sql),
        "tablas": tablas_generadas
    }
