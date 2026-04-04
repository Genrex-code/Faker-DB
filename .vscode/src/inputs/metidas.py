
# El purgatorio de los usuarios que no saben usar flags en la terminal

def pedir_entero(mensaje):
    """Bucle infinito hasta que el usuario entienda que debe meter un número positivo."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                print("❌ No seas payaso, ingresa un número mayor a 0.")
            else:
                return valor
        except ValueError:
            print("❌ Error: Comprensión lectora fallida. SOLO SE ADMITEN NÚMEROS ENTEROS.")

def menu_interactivo():
    """
    Despliega el menú para el usuario común y silvestre.
    Retorna las filas, la lista de columnas y el formato de salida.
    """
    print("\n" + "="*50)
    print(" 🦕 BIENVENIDO AL MODO INTERACTIVO (ARCAICO) 🦕 ")
    print("="*50)

    # 1. Pedir Filas
    filas = pedir_entero("\n👉 ¿Cuántas filas/registros de datos necesitas?: ")

    # 2. Pedir Columnas (El nombre de la columna ES el tipo de dato)
    print("\n👉 Ingresa los datos que necesitas separados por coma.")
    print("💡 Ejemplos soportados: nombre, email, rfc, telefono, id_caos")
    columnas_raw = input("Tipos de datos: ")
    
    # Limpiamos los espacios extras y convertimos a minúsculas por si el usuario escribe feo (" Nombre,  eMail")
    columnas = [col.strip().lower() for col in columnas_raw.split(",")]

    # 3. Formato de Salida
    print("\n👉 ¿A dónde quieres mandar este desmadre?")
    print("   1) Archivo Excel (.csv)")
    print("   2) Script de Base de Datos (.sql)")
    print("   3) Solo mostrar en la terminal (Dataset en crudo)")
    
    while True:
        opcion = pedir_entero("Elige el número de tu opción (1-3): ")
        if opcion == 1:
            formato_salida = "csv"
            break
        elif opcion == 2:
            formato_salida = "sql"
            break
        elif opcion == 3:
            formato_salida = "terminal"
            break
        else:
            print("❌ Opción no válida. Es 1, 2 o 3. No es tan difícil.")

    print("\n✅ ¡Información recolectada con éxito!")
    return filas, columnas, formato_salida