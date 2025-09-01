from faker import Faker

### ingreso de datos
nombre_bd = input("👉 Escribe el nombre de la base de datos: ")
nombre_tabla = input("👉 Escribe el nombre de la tabla: ")
num_columnas = int(input("👉 ¿Cuántas columnas tendrá la tabla? "))
num_registros = int(input("👉 ¿Cuántos registros deseas generar? "))
#limitante para evitar que esta madre truene
#aca se consideran sanos alrededor de 4 columnas solamente
LIMITE_REGISTROS = 100000
if num_registros > LIMITE_REGISTROS:
    print("pon un numero mas bajo o va a tronar esta chingadera D:")
    num_registros = LIMITE_REGISTROS
#aca como se llamaran las columas y sus tipos de datos que limitamos a char y int
columnas = []
for i in range(num_columnas):
    nombre_col = input(f"Nombre de la columna {i+1}: ")
    tipo_col = input(f"Tipo de dato para {nombre_col} (ej: VARCHAR(100), INT): ")
    columnas.append(f"{nombre_col} {tipo_col}")
#esto convierte la lista de columnas en una cadena separada por comas y saltos de línea
# para usarla en la creación de la tabla
estructura_columnas = ",\n     ".join(columnas)
### script SQL inicial
sql_script = f"""
CREATE DATABASE IF NOT EXISTS {nombre_bd};
USE {nombre_bd};

CREATE TABLE IF NOT EXISTS {nombre_tabla} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {estructura_columnas}
);
"""
#que chingue su madre el america
# Inicializamos faker con 
# español de México de america 
# latina de continten africano
# porque todos aca son negros D:
fake = Faker('es_MX')

# Generamos inserts con datos falsos
#nota se cambio a un metodo delimitado porque estoy tonto
#  para programar algo mas complejo :D

for _ in range(num_registros):
    valores = []
    #este for recorre faker a una estructura pre hecha segun chatgpt
    for col in columnas:
        nombre_col, tipo_col = col.split()[0], col.split()[1]
        tipo_col = tipo_col.lower()
         #esto recorre como tal com un case de java(odio java)
        #de aca podemos agregar mas if y asi añadir mas categorias
        if "char" in tipo_col or "text" in tipo_col:
            if "nombre" in nombre_col.lower():
                valores.append(f"'{fake.name()}'")
            elif "email" in nombre_col.lower():
                valores.append(f"'{fake.email()}'")
            elif "telefono" in nombre_col.lower() or "tel" in nombre_col.lower() or "celular" in nombre_col.lower():
                valores.append(f"'{fake.phone_number()}'")
            else:
                valores.append(f"'{fake.word()}'")
                #aca coloque un limitante para el generador de numero si no truena esta chingadera
        elif "INT" in tipo_col:
            valores.append(f"{fake.random_int(min=1, max=1000)}")
        else:
            valor = (f"'{fake.word()}'") #valor por defecto si no se reconoce el tipo o el usuario esta muy baboso y no sabe escribir bien porque le muy tarado tiene down o algo asi
    #aca se inserta al 
    sql_script += f"""
INSERT INTO {nombre_tabla}({", ".join([col.split()[0] for col in columnas])}) VALUES ({", ".join(valores)});
"""

# Guardar script en archivo .sql
with open("script_generado.sql", "w", encoding="utf-8") as archivo:
    archivo.write(sql_script)

# Vista previa
print("\n✅ Script SQL generado con éxito en 'script_generado.sql'")
print("------ Vista previa ------")
print(sql_script)