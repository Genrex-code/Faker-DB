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
    "id" :fake.uuid4(),
    "puesto" : fake.job,
    "empresa" : fake.company,
    "url" : fake.url,
    "ip" : fake.ipv4,
    "mac" : fake.mac_address,
    "estado" : fake.state,
    "estado_provincia" : fake.state,
    "region" : fake.state,
    "navegador" : fake.user_agent,
    "curp" : fake.curp,
    "rfc" : fake.rfc,
    "cvv" : fake.credit_card_security_code,
    "marca" : lambda: random.choice(["Toyota", "Ford", "Chevrolet", "Honda", "Nissan"]),
    "modelo" : lambda: random.choice(["Sedan", "SUV", "Hatchback", "Convertible", "Truck"]),
    "año" : lambda: random.randint(1990, 2023),
    "color_auto" : fake.color_name,
    "color_vehiculo" : fake.color_name,
    "curso" : lambda: random.choice(["Matemáticas", "Historia", "Ciencia", "Literatura", "Arte"]),
    "calificacion" : lambda: random.choice(["A", "B", "C", "D", "F"]),
    "nacionalidad" : fake.country,
    "religion" : lambda: random.choice(["Católica", "Protestante", "Musulmana", "Judía", "Hindú", "Budista", "Atea"]),
    "estado_civil" : lambda: random.choice(["Soltero", "Casado", "Divorciado", "Viudo"]),
    "hobby" : lambda: random.choice(["Leer", "Viajar", "Cocinar", "Deportes", "Música", "Jardinería"]),
    "aficion" : lambda: random.choice(["Leer", "Viajar", "Cocinar", "Deportes", "Música", "Jardinería"]),
    "mascota" : lambda: random.choice(["Perro", "Gato", "Pájaro", "Pez", "Hamster"]),
    "animal" : lambda: random.choice(["Perro", "Gato", "Pájaro", "Pez", "Hamster"]),
    "fruta" : lambda: random.choice(["Manzana", "Banana", "Naranja", "Uva", "Fresa"]),
    "verdura" : lambda: random.choice(["Lechuga", "Tomate", "Zanahoria", "Pepino", "Cebolla"]),
    "bebida" : lambda: random.choice(["Agua", "Jugo", "Refresco", "Café", "Té"]),
    "musica" : lambda: random.choice(["Rock", "Pop", "Jazz", "Clásica", "Hip-Hop"]),
    "deporte" : lambda: random.choice(["Fútbol", "Baloncesto", "Tenis", "Natación", "Ciclismo"]),
    "marca_ropa" : lambda: random.choice(["Nike", "Adidas", "Puma", "Reebok", "Under Armour"]),
    "talla_ropa" : lambda: random.choice(["S", "M", "L", "XL", "XXL"]),
    "tipo_sangre" : lambda: random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
    "alergia" : lambda: random.choice(["Polen", "Polvo", "Pelos de animales", "Alimentos", "Medicamentos"]),
    "medicamento" : lambda: random.choice(["Paracetamol", "Ibuprofeno", "Amoxicilina", "Loratadina", "Omeprazol"]),
    "enfermedad" : lambda: random.choice(["Diabetes", "Hipertensión", "Asma", "Alergias", "Artritis"]), 
    "hospital" : fake.company,
    "clinica" : fake.company,
    "universidad" : fake.company,
    "escuela" : fake.company,
    "instituto" : fake.company,
    "titulo" : lambda: random.choice(["Licenciatura", "Maestría", "Doctorado", "Diplomado", "Certificación"]),
    "grado" : lambda: random.choice(["Licenciatura", "Maestría", "Doctorado", "Diplomado", "Certificación"]),
    "idioma" : fake.language_name,
    "calle" : fake.street_name,
    "avenida" : fake.street_name,
    "barrio" : fake.city_suffix,
    "colonia" : fake.city_suffix,
    "municipio" : fake.city,
    "codigo_postal" : fake.postcode,
    "numero_ext" : lambda: str(random.randint(1, 9999)),
    "numero_int" : lambda: str(random.randint(1, 9999)),
    "referencia" : fake.sentence,
    "notas" : fake.text,
    "comentarios" : fake.text,
    "observaciones" : fake.text,
    "biografia" : fake.text,
    "correo_corporativo" : fake.company_email,
    "correo_personal" : fake.email,
    "pagina_web" : fake.url,
    "sitio_web" : fake.url,
    "red_social" : lambda: random.choice(["Facebook", "Twitter", "Instagram", "LinkedIn", "TikTok"]),
    "usuario_red" : fake.user_name,
    "contrasena" : fake.password,
    "password" : fake.password,
    "moneda" : lambda: random.choice(["USD", "EUR", "MXN", "GBP", "JPY"]),
    "cantidad" : lambda: round(random.uniform(1.0, 1000.0), 2),
    "precio" : lambda: round(random.uniform(10.0, 1000.0), 2),
    "descuento" : lambda: round(random.uniform(0.0, 100.0), 2),
    "total" : lambda: round(random.uniform(10.0, 10000.0), 2),
    "iva" : lambda: round(random.uniform(0.0, 100.0), 2),
    "subtotal" : lambda: round(random.uniform(10.0, 10000.0), 2),
    "factura" : fake.bothify(text='????-########'),
    "orden" : fake.bothify(text='ORD-########'),
    "pedido" : fake.bothify(text='PED-########'),
    "producto" : fake.word,
    "servicio" : fake.word,
    "categoria" : lambda: random.choice(["Electrónica", "Ropa", "Hogar", "Juguetes", "Libros"]),
    "marca_producto" : lambda: random.choice(["Sony", "Samsung", "Apple", "LG", "Dell"]),
    "modelo_producto" : lambda: random.choice(["X100", "ProMax", "Ultra", "S20", "Note"]),
    "color_producto" : fake.color_name,
    "talla_producto" : lambda: random.choice(["S", "M", "L", "XL", "XXL"]),
    "peso" : lambda: round(random.uniform(0.1, 100.0), 2),
    "altura" : lambda: round(random.uniform(0.1, 3.0), 2),
    "ancho" : lambda: round(random.uniform(0.1, 3.0), 2),
    "largo" : lambda: round(random.uniform(0.1, 3.0), 2),
    "volumen" : lambda: round(random.uniform(0.1, 100.0), 2),
    "capacidad" : lambda: round(random.uniform(1.0, 1000.0), 2),
    "stock" : lambda: random.randint(0, 1000),
    "inventario" : lambda: random.randint(0, 1000),
    "iban" : fake.iban,
    "swift" : fake.swift,
    "ipv6" : fake.ipv6,
    "Metodo_pago" : lambda: random.choice(["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia bancaria", "PayPal"]),
    "estatus" : lambda: random.choice(["Activo", "Inactivo", "Pendiente", "Completado", "Cancelado"]),
    "estado_pedido" : lambda: random.choice(["Activo", "Inactivo", "Pendiente", "Completado", "Cancelado"]),
    "prioridad" : lambda: random.choice(["Baja", "Media", "Alta"]),
    "nivel" : lambda: random.choice(["Básico", "Intermedio", "Avanzado"]),
    "placa_auto" : fake.license_plate,
    "placa_vehiculo" : fake.license_plate,
    "motor" : lambda: random.choice(["V6", "V8", "I4", "Electric", "Hybrid"]),
    "pais_origen" : fake.country,
    "pais_destino" : fake.country,
    "puerto" : fake.city,
    "aeropuerto" : fake.city,
    "terminal" : fake.city,
    "vuelo" : fake.bothify(text='??####'),
    "asiento" : fake.bothify(text='?#'),
    "clase" : lambda: random.choice(["Económica", "Business", "Primera"]),
    "hotel" : fake.company() + " Hotel",
    "habitacion" : lambda: random.randint(100, 999),
    "noches" : lambda: random.randint(1,30),
    "pasaporte" : fake.bothify(text='??######'),
    "visa" : fake.bothify(text='##########'),
    "licencia" : fake.bothify(text='##########'),
    "certificado" : fake.bothify(text='##########'),
    "numero_seguridad_social" : fake.ssn,
    "numero_seguro_social" : fake.ssn,
    "afiliacion" : fake.bothify(text='##########'),
    "peso_kg" : lambda: round(random.uniform(30.0, 200.0), 2),
    "altura_cm" : lambda: round(random.uniform(100.0, 250.0), 2),
    "imc" : lambda: round(random.uniform(15.0, 40.0), 2),
    "frecuencia_cardiaca" : lambda: random.randint(60, 100),
    "presion_arterial" : lambda: f"{random.randint(90, 140)}/{random.randint(60, 90)}",
    "temperatura" : lambda: round(random.uniform(36.0, 39.0), 1),
    "oxigenacion" : lambda: random.randint(90, 100),
    "glucosa" : lambda: random.randint(70, 140),
    "colesterol" : lambda: random.randint(150, 250),
    "trigliceridos" : lambda: random.randint(50, 200),
    "juego" : fake.word() + " Game",
    "consola" : lambda: random.choice(["PlayStation", "Xbox", "Nintendo Switch", "PC"]),
    "plataforma_juego" : lambda: random.choice(["Steam", "Epic Games", "Origin", "Uplay"]),
    "genero_juego" : lambda: random.choice(["Acción", "Aventura", "RPG", "Estrategia", "Deportes"]),
    "nickname" : fake.user_name,
    "gamer_tag" : fake.user_name,
    "voltaje" : fake.random_number,
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
