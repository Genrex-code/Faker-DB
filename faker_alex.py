from faker import Faker
import mysql.connector
import random
from datetime import date, datetime

# Colores para que el código sea más fácil de leer
class bcolors:
    HEADER = '\033[95m' # Púrpura
    OKBLUE = '\033[94m'# Azul ligeramente más oscuro
    OKCYAN = '\033[96m' # Azul 
    OKGREEN = '\033[92m' # Verde azul
    WARNING = '\033[93m' # Amarillo brillante
    FAIL = '\033[91m'# Rojo
    ENDC = '\033[0m' # Terminar bcolors (???????)
    BOLD = '\033[1m' # Negritas
    UNDERLINE = '\033[4m' # Subrayar texto

# Límite de registros de las tablas


### ingreso de datos
nombre_bd = input(bcolors.BOLD + "Escribe el nombre de la base de datos: "+ bcolors.ENDC)
##ponle INT a los cosos que sean puro numero
while True:
                try:
                   num_tablas = int(input("¿Cuántas tablas deseas generar? "))
                except ValueError:
                      print(bcolors.HEADER + "Mensaje de error escrito por el mayor fan de katamari damacy"+ bcolors.ENDC)              
                      continue
                
                #while num_tablas > 0:
                      #print(bcolors.HEADER + "Mensaje de error escrito por el mayor fan de katamari damacy"+ bcolors.ENDC) 


                else:
                      break

while True:
                try:
                   
                   num_registros = int(input("¿Cuántos registros deseas generar? "))
                except ValueError:
                      print(bcolors.HEADER + "Mensaje de error escrito por el mayor fan de katamari damacy"+ bcolors.ENDC)
                      continue
                #except num_registros > LIMITE_REGISTROS:
                      #print(bcolors.HEADER + "Mensaje de error escrito por el mayor fan de katamari damacy"+ bcolors.ENDC)
                      #continue
                else:
                      break    

coneccion = input("¿Desea el archivo para carga manual o carga en servidor? (manual/servidor): ")
#este if sirve para separar la automatizacion del scrip de generacion estandar
if coneccion.lower() == "servidor":
    #le puse una S para que se vea mas bonito :3
    host_S = input("Escribe el host (ej: localhost): ")
    user_S = input("Escribe el usuario de la base de datos: ")
    password_S = input("Escribe la contraseña del usuario: ")
else:
    print("Se generará el archivo para carga manual")
#aca agrego la capacidad de crear varias tablas aunque no se si funcione bien
#porque no lo he probado y me quede sin cereal :D
tablas = []
estructura_tablas = {} #diccionario para almacenar la estructura de cada tabla
for i in range(num_tablas):
               nombre_tabla = input(f"Escribe el nombre de la tabla {i+1}: ")
               tablas.append ("{nombre_tabla}")

while True:
                try:
                   num_columnas = int(input(f"¿Cuántas columnas tendrá la tabla '{nombre_tabla}'? "))
                except ValueError:
                      print(bcolors.HEADER + "Mensaje de error escrito por el mayor fan de katamari damacy"+ bcolors.ENDC)
                      continue
                else:
                      break

               
               
columnas = []
#aca como se llamaran las columas y sus tipos de datos que limitamos a char y int
#aca diccionario de cada tabla 19/09/2025
for j in range(num_columnas):
    nombre_col = input(f"Nombre de la columna número {j+1} de la tabla '{nombre_tabla}': ")
    tipo_col = input(f"Tipo de dato para '{nombre_col}' (ej: VARCHAR (Texto), INT (Números)): ")
    columnas.append(f"{nombre_col} {tipo_col}")
    estructura_tablas[nombre_tabla] = columnas
#se borro el join porque ahora se maneja como diccionario (don pejdo ya se perdio)
#limitante para evitar que esta madre truene
#aca se consideran sanos alrededor de 4 columnas solamente
#el limitante se bajo de lugar para evitar desmadre+
#
#
#
#NOTA DE NOTAS DE NOTAS CAMBIAR LAS GROSERIAS DE ESTE CODIGO
#PORQUE YA ME CANSE DE PONER GROSERIAS EN EL CODIGO
LIMITE_REGISTROS = 100000
if num_registros > LIMITE_REGISTROS:
       print("Número demasiado alto. Ingresa uno más pequeño")
       num_registros = LIMITE_REGISTROS

#mejor hare como un stencil y que el usuario meta lo que quiera
#esto es para crear la estructura de la base de datos
### script SQL inicial
sql_script = f"""
CREATE DATABASE IF NOT EXISTS {nombre_bd};
USE {nombre_bd};
"""
#se crea un buccle para cada pedassito 
for nombre_tabla, columnas in estructura_tablas.items():
    estructura_columnas = ",\n     ".join(columnas)
    sql_script += f"""
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
#con esto se genera como maincra :0
fake = Faker('es_MX')
Faker.seed(0)
random.seed(0)
# Generamos inserts con datos falsos
#nota se cambio a un metodo delimitado porque estoy tonto
#  para programar algo mas complejo :D
#borre el desmadre que tenia para incluirlo mejor como un
#  diccionario optimisando asi el ingreso de datos cuando
#  se traten de cosas mas grandes de 1 millon de datyos
for _ in range(num_registros):
      columnas_nombres = ",".join([col.split()[0] for col in columnas])
      valores = ",".join(["VALOR_FAKE" for _ in columnas])
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
    "precio" : lambda: round(random.uniform(10.0, 1000)),
    "salario" : lambda: random.randint(3000, 100000),
    "int": lambda: random.randint(1, 10000),
    "varchar": lambda: fake.word(),
    "descripcion" : lambda: fake.sentence(nb_words=6),
    #los que siguen aca abajo los estoy testeando por eso esta asi
    #"banco" : fake.bank,
    #"curp" : fake.curp,
    #"nif" : fake.nif,
    #"rfc" : fake.rfc,
    "civil_estatus" : lambda: random.choice(["Soltero", "Casado", "Divorciado", "Viudo"]),
    "genero" : lambda: random.choice(["Masculino", "Femenino", "Otro"]),
    "boolean": lambda: random.choice([0, 1]),
}
      #se carga los inserts
sql_script += f"""
INSERT INTO {nombre_tabla}({columnas_nombres}) VALUES ({valores})
"""
# Guardar script en archivo .sql 
# se incluye un limitante de que tanto se muestra para no colapsar la terminal
# que es otra limitante poes >:v
with open("script_generado.sql", "w", encoding="utf-8") as archivo:
    archivo.write(sql_script)
# Vista previa
#ya no tan previa >:v
print("\n Script SQL generado con éxito en 'script_generado.sql'")
print("------ Vista previa ------")
print(sql_script[:700],"...""\n------ Fin de la vista previa ------,\n------EL RESTO ESTA EN WORKBECH------")
# aca va la coneccion a servidor no tan servidor de workbech
if coneccion.lower() == "servidor":
     try:
            conexion = mysql.connector.connect(
                host=host_S,
                user=user_S,
                password=password_S,
                database=nombre_bd
            )
            print("Conexión exitosa")
            print("Cargando datos a la base de datos...")
            print("Dependiendo de la cantidad de datos, este proceso puede tardar")
            #print("esto puede tardar un poco dependiendo de la cantidad de datos")
            print("No cierre el programa")
            print("------ Cargando... ------")
            print("Aún no se han generado los Queries")
            #print("TODABIA NO HAN GENERADO QUERIES :D ESO LO HACES TU")
     except Exception as e:
            print("Error al conectar a la base de datos:", e)