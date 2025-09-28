from faker import Faker
import mysql.connector
import random
from datetime import date, datetime

# ingreso de datos
nombre_bd = input("Escribe el nombre de la base de datos: ")
num_tablas = int(input("¿Cuántas tablas deseas? "))
num_registros = int(input("¿Cuántos registros deseas generar? "))
coneccion = input("¿Desea el archivo para carga manual o carga en servidor? (manual/servidor): ")

if coneccion.lower() == "servidor":
    host_S = input("Escribe el host (ej: localhost): ")
    user_S = input("Escribe el usuario de la base de datos: ")
    password_S = input("Escribe la contraseña del usuario: ")
else:
    print("Se generará el archivo para carga manual")

tablas = []
estructura_tablas = {}  # diccionario para almacenar columnas de cada tabla

for i in range(num_tablas):
    nombre_tabla = input(f"Escribe el nombre de la tabla {i+1}: ")
    tablas.append(nombre_tabla)
    num_columnas = int(input(f"¿Cuántas columnas tendrá la tabla {nombre_tabla}? (Recomendado ≤ 4) "))
    columnas = []
    for j in range(num_columnas):
        nombre_col = input(f"Nombre de la columna {j+1} de la tabla {nombre_tabla}:\n (Ej: nombre, email, telefono, ciudad, pais, direccion, postal, ssn, usuario, compañia, trabajo, fecha, color, producto, lenguaje, numero, tarjeta, precio, salario): ")
        tipo_col = input(f"Tipo de dato para {nombre_col} (ej: VARCHAR(100), INT): ")
        columnas.append(f"{nombre_col} {tipo_col}")
    estructura_tablas[nombre_tabla] = columnas

LIMITE_REGISTROS = 50000
if num_registros > LIMITE_REGISTROS:
    print(f"El número de registros excede el límite {LIMITE_REGISTROS}, se ajustará a este valor.")
    num_registros = LIMITE_REGISTROS

# Inicializamos faker
fake = Faker('es_MX')
Faker.seed(0)
random.seed(0)

generadores = {
    "nombre": fake.name,
    "email": fake.unique.email,
    "telefono": fake.phone_number,
    "celular": fake.phone_number,
    "ciudad": fake.city,
    "pais": fake.country,
    "direccion": fake.address,
    "postal": fake.postcode,
    "postcode": fake.postcode,
    "ssn": fake.ssn,
    "username": fake.user_name,
    "usuario": fake.user_name,
    "compañia": fake.company,
    "empresa": fake.company,
    "trabajo": fake.job,
    "fecha": fake.date,
    "fecha_nacimiento": fake.date_of_birth,
    "color" : fake.color_name,
    "producto": fake.word,
    "lenguaje": fake.language_name,
    "idioma" : fake.language_name,
    "numero": lambda: random.randint(1, 10000),
    "tarjeta" : fake.credit_card_number,
    "precio" : lambda: round(random.uniform(10.0, 1000), 2),
    "salario" : lambda: random.randint(3000, 100000),
    "int": lambda: random.randint(1, 10000),
    "varchar": lambda: fake.word(),
    "descripcion" : lambda: fake.sentence(nb_words=6),
    "civil_estatus" : lambda: random.choice(["Soltero", "Casado", "Divorciado", "Viudo"]),
    "genero" : lambda: random.choice(["Masculino", "Femenino", "Otro"]),
    "boolean": lambda: random.choice([0, 1]),
}

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
    t = tipo_col.lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (date, datetime)):
        return f"'{value.strftime('%Y-%m-%d')}'"
    if "int" in t or "decimal" in t or "float" in t or "double" in t or "numeric" in t:
        return str(value)
    s = str(value)
    s = s.replace("'", "''")  # Escapar comillas simples para SQL
    return f"'{s}'"

def generar_valor_raw(nombre_col, tipo_col):
    name = nombre_col.lower()
    t = tipo_col.lower()
    # Números enteros
    if "int" in t or "integer" in t or "bigint" in t or "smallint" in t or "tinyint" in t:
        return random.randint(1, 10000)
    # Números con decimales
    if "float" in t or "double" in t or "decimal" in t or "numeric" in t or "real" in t:
        return round(random.uniform(1.0, 10000.0), 2)
    # Fechas
    if "date" in t or "time" in t or "timestamp" in t:
        if "nacimiento" in name or "birth" in name or "cumpl" in name:
            dob = safe_call_generador(generadores.get("fecha_nacimiento"))
            if dob:
                return dob
        d = safe_call_generador(generadores.get("fecha"))
        return d
    # Intentar usar generadores por palabra clave
    for clave, func in generadores.items():
        if clave in name:
            val = safe_call_generador(func)
            if val is not None:
                return val
    # Por defecto, generar palabra corta
    return fake.word()

# Generar script SQL inicial para base y tablas
sql_script = f"""
CREATE DATABASE IF NOT EXISTS {nombre_bd};
USE {nombre_bd};
"""

for nombre_tabla, columnas in estructura_tablas.items():
    estructura_columnas = ",\n    ".join(columnas)
    sql_script += f"""
CREATE TABLE IF NOT EXISTS {nombre_tabla} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {estructura_columnas}
);
"""

# Generar datos e inserts para cada tabla
for nombre_tabla, columnas in estructura_tablas.items():
    columnas_nombres = ",".join([col.split()[0] for col in columnas])
    for _ in range(num_registros):
        valores_raw = [generar_valor_raw(col.split()[0], col.split()[1]) for col in columnas]
        valores_sql = [sql_literal(val, col.split()[1]) for val, col in zip(valores_raw, columnas)]
        sql_script += f"INSERT INTO {nombre_tabla}({columnas_nombres}) VALUES ({','.join(valores_sql)});\n"

# Guardar script en archivo .sql
with open("script_generado.sql", "w", encoding="utf-8") as archivo:
    archivo.write(sql_script)

print("\nScript SQL generado con éxito en 'script_generado.sql'")
print("------ Vista previa ------")
print(sql_script[:700], "...\n------ Fin de la vista previa ------\n------ EL RESTO ESTÁ EN WORKBENCH ------\n")

if coneccion.lower() == "servidor":
    try:
        conexion = mysql.connector.connect(
            host=host_S,
            user=user_S,
            password=password_S,
            database=nombre_bd
        )
        cursor = conexion.cursor()
        print("Conexión exitosa :D")
        print("Creando base de datos y tablas...")
        for query in sql_script.split(';'):
            query = query.strip()
            if query:
                cursor.execute(query)
        conexion.commit()

        print("Insertando datos ... esto puede tardar un poco dependiendo de la cantidad de datos...")
        print("No cierres el programa >:v")

        # Ejecución de los inserts (solo la parte INSERT)
        inserts = [line for line in sql_script.split('\n') if line.strip().upper().startswith("INSERT INTO")]
        total_inserts = len(inserts)
        for i, insert in enumerate(inserts, 1):
            cursor.execute(insert)
            if i % 1000 == 0:
                conexion.commit()
                print(f"{i} de {total_inserts} registros insertados...")
        conexion.commit()
        print("Datos insertados correctamente.")
        cursor.close()
        conexion.close()
    except Exception as e:
        print("Error al conectar o insertar en la base de datos:", e)
