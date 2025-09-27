from faker import Faker
import mysql.connector
import random

def pedir_entero(mensaje, minimo=1, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo and valor < minimo:
                print(f"Pon un número mayor o igual a {minimo}")
                continue
            if maximo and valor > maximo:
                print(f"El número no puede ser mayor que {maximo}")
                continue
            return valor
        except ValueError:
            print("Eso no es un número, intenta de nuevo.")

def pedir_opcion(mensaje, opciones_validas):
    while True:
        valor = input(mensaje).strip().lower()
        if valor in [op.lower() for op in opciones_validas]:
            return valor
        print(f"Opción inválida, escoge entre: {', '.join(opciones_validas)}")

def pedir_tipo_dato(nombre_col):
    while True:
        tipo = input(f"Tipo de dato para {nombre_col} (ej: VARCHAR(100), INT): ").strip().upper()
        if tipo.startswith("INT") or tipo.startswith("VARCHAR"):
            return tipo
        else:
            print("Ese tipo no se acepta, mete INT o VARCHAR(n).")

nombre_bd = input("Escribe el nombre de la base de datos: ")
num_tablas = pedir_entero("¿Cuántas tablas deseas? ", minimo=1)
num_registros = pedir_entero("¿Cuántos registros deseas generar? ", minimo=1, maximo=100000)
coneccion = pedir_opcion("¿Desea el archivo para carga manual o carga en servidor? (manual/servidor): ",
                         ["manual", "servidor"])

if coneccion == "servidor":
    host_S = input("Escribe el host (ej: localhost): ")
    user_S = input("Escribe el usuario de la base de datos: ")
    password_S = input("Escribe la contraseña del usuario: ")
else:
    print("Se generará el archivo para carga manual.")

tablas = []
estructura_tablas = {}

for i in range(num_tablas):
    nombre_tabla = input(f"Escribe el nombre de la tabla {i+1}: ").strip()
    tablas.append(nombre_tabla)
    num_columnas = pedir_entero(f"¿Cuántas columnas tendrá la tabla {nombre_tabla}? ", minimo=1)
    columnas = []
    for j in range(num_columnas):
        nombre_col = input(f"Nombre de la columna {j+1} de la tabla {nombre_tabla}: ").strip()
        tipo_col = pedir_tipo_dato(nombre_col)
        columnas.append(f"{nombre_col} {tipo_col}")
    estructura_tablas[nombre_tabla] = columnas

fake = Faker("es_MX")
Faker.seed(0)
random.seed(0)

generadores = {
    "nombre": fake.name,
    "email": fake.unique.email,
    "telefono": fake.phone_number,
    "ciudad": fake.city,
    "pais": fake.country,
    "username": fake.user_name,
    "empresa": fake.company,
    "trabajo": fake.job,
    "fecha": fake.date,
    "fecha_nacimiento": fake.date_of_birth,
    "color": fake.color_name,
    "producto": fake.word,
    "lenguaje": fake.language_name,
    "numero": lambda: random.randint(1, 10000),
    "precio": lambda: round(random.uniform(10.0, 1000)),
    "salario": lambda: random.randint(3000, 100000),
    "descripcion": lambda: fake.sentence(nb_words=6),
    "civil_estatus": lambda: random.choice(["Soltero", "Casado", "Divorciado", "Viudo"]),
    "genero": lambda: random.choice(["Masculino", "Femenino", "Otro"]),
    "boolean": lambda: random.choice([0, 1]),
}

tematizacion = pedir_opcion("¿Quieres añadir alguna tematización? (si/no): ", ["si", "no"])

if tematizacion == "si":
    extras = pedir_opcion("¿Qué dato extra quieres generar? (curp/rfc/direccion/nif/todos): ",
                          ["curp", "rfc", "direccion", "nif", "todos"])
    if extras in ["curp", "todos"]:
        generadores["curp"] = fake.ssn  # faker no tiene curp real, se usa ssn como sustituto
    if extras in ["rfc", "todos"]:
        generadores["rfc"] = fake.ssn
    if extras in ["direccion", "todos"]:
        generadores["direccion"] = fake.address
    if extras in ["nif", "todos"]:
        generadores["nif"] = fake.ssn

sql_script = f"CREATE DATABASE IF NOT EXISTS {nombre_bd};\nUSE {nombre_bd};\n"

for nombre_tabla, columnas in estructura_tablas.items():
    estructura_columnas = ",\n     ".join(columnas)
    sql_script += f"""
    CREATE TABLE IF NOT EXISTS {nombre_tabla} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {estructura_columnas}
    );
    """
    columnas_nombres = ",".join([col.split()[0] for col in columnas])
    for _ in range(num_registros):
        valores = ",".join(["'VALOR_FAKE'" for _ in columnas])
        sql_script += f"""
        INSERT INTO {nombre_tabla}({columnas_nombres}) VALUES ({valores});
        """

with open("script_generado.sql", "w", encoding="utf-8") as archivo:
    archivo.write(sql_script)

print("\n Script SQL generado con éxito en 'script_generado.sql'")
print("------ Vista previa ------")
print(sql_script[:700], "...\n------ Fin de la vista previa ------")

if coneccion == "servidor":
    try:
        conexion = mysql.connector.connect(
            host=host_S,
            user=user_S,
            password=password_S,
            database=nombre_bd
        )
        print("Conexión exitosa")
        print("Cargando datos a la base de datos...")
    except Exception as e:
        print("Error al conectar a la base de datos:", e)