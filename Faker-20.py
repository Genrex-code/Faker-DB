from faker import Faker

### ingreso de datos
nombre_bd = input("👉 Escribe el nombre de la base de datos: ")
nombre_tabla = input("👉 Escribe el nombre de la tabla: ")

### script SQL inicial
sql_script = f"""
CREATE DATABASE IF NOT EXISTS {nombre_bd};
USE {nombre_bd};

CREATE TABLE IF NOT EXISTS {nombre_tabla} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    telefono VARCHAR(20)
);
"""

# Inicializamos faker con español de México
fake = Faker('es_MX')

# Generamos inserts con datos falsos
for _ in range(10):
    nombre = fake.name()
    email = fake.email()
    telefono = fake.phone_number()

    sql_script += f"""
INSERT INTO {nombre_tabla} (nombre, email, telefono)
VALUES ('{nombre}', '{email}', '{telefono}');
"""

# Guardar script en archivo .sql
with open("script_generado.sql", "w", encoding="utf-8") as archivo:
    archivo.write(sql_script)

# Vista previa
print("\n✅ Script SQL generado con éxito en 'script_generado.sql'")
print("------ Vista previa ------")
print(sql_script)