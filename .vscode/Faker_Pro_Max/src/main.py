import argparse
import sys
# Asumiendo que pipilinais.py tiene tu clase State
from pipilinais import State
# En el futuro importarás tu archivo de inputs así:
# from inputs_arcaicos import menu_interactivo

from inputs.metidas import menu_interactivo
print("🔥 Generador de bases de datos sintéticas (Edición Miku Desvelada) 🔥")
print("Crea datos para pruebas en ambientes controlados :3\n")

def chismesito():
    """Parseo de argumentos de entrada desde la terminal."""
    parse = argparse.ArgumentParser(description="El chismesito: Generador de bases de datos sintéticas")

    parse.add_argument("--debug", action="store_true", help="Habilitar modo debug para ver las tripas del código")
    parse.add_argument("--config", type=str, help="Ruta al archivo de configuración (.json o .yaml)")
    parse.add_argument("--data", type=str, help="Ruta al archivo de datos de entrada")  
    parse.add_argument("--output", type=str, help="Ruta al archivo de salida (.csv, .sql)")
    parse.add_argument("--probadita", type=int, default=0, help="Genera N registros rápido para ver que no explote")
    parse.add_argument("--CLI", action="store_true", help="Habilita el menú interactivo (arcaico) para pedir datos")
    parse.add_argument("--PERRITA", action="store_true", help="demuestra quien es la perra de quien 💋")

    return parse.parse_args()

def main():
    """Punto de entrada principal. El cadenero del antro."""
    args = chismesito()

    # 1. Empaquetamos la "Orden" basada en los argumentos
    # Este es el diccionario global que viajará por todo el programa
    orden_config = {
        "modo_debug": args.debug,
        "archivo_config": args.config,
        "archivo_entrada": args.data,
        "ruta_salida": args.output,
        "test_probadita": args.probadita,
        "modo_arcaico": args.CLI,
        "modo_perrita": args.PERRITA,
        "columnas_pedidas": [] # Aquí guardaremos lo que el usuario pida después
    }

    if args.debug:
        print("🐛 [MODO DEBUG ACTIVADO]: Evaluando el chismesito...")
        print(f"📦 Argumentos empaquetados: {orden_config}\n")

    # 2. Lógica de decisión (Qué quiere hacer el usuario)
    # 2. Lógica de decisión (Qué quiere hacer el usuario)
    if args.CLI:
        print("🦕 Modo CLI arcaico detectado.")
        
        # Invocamos al encuestador
        filas, columnas, formato = menu_interactivo()
        
        # Metemos lo que respondió el usuario a nuestra orden global
        orden_config["columnas_pedidas"] = columnas
        orden_config["filas_a_generar"] = filas
        orden_config["formato_salida"] = formato
        
    elif args.probadita > 0:
        print(f"🧪 Modo Probadita: Vamos a generar {args.probadita} filas de prueba.")
        # Le inyectamos columnas por defecto para que funcione en automático
        orden_config["columnas_pedidas"] = ["nombre", "email"]
        
    elif args.PERRITA:
        print("💋 MODO PERRITA INICIADO. Que Dios se apiade de tu RAM.")
        
    else:
        # Si corren el programa a lo menso, sin flags, forzamos el modo CLI
        print("⚠️ No enviaste flags. Iniciando el flujo interactivo por defecto...")
        orden_config["modo_arcaico"] = True

        #confirmo si faltaba esto -perro
        filas, columnas, formato = menu_interactivo()

        #y ahora se lo pasamos a la orden global
        orden_config["columnas_pedidas"] = columnas
        orden_config["filas_a_generar"] = filas
        orden_config["formato_salida"] = formato

    # 3. Inicializar el Pipeline (Pipilinais)
    try:
        print("\n🚀 Despertando al Pipilinais (State)...")
        # Le pasamos la orden completa al pipeline
        pipeline = State(orden_config)
        
        # Comenta esta línea si tu pipilinais.py aún no tiene la función run()
        pipeline.run() 
        
    except Exception as e:
        # Si algo truena (como el modo perrita), lo atrapamos aquí para no asustar a los niños
        print(f"\n💥 ¡Cagaste! El programa reventó: {e}")
        sys.exit(1)
        
    finally:
        # Esto reemplaza a tu def __exit__ de la clase muricion. 
        # Siempre se imprime, haya errores o no.
        print("\n👋 Espero que les haya sido de utilidad la chingadera esta :3")

if __name__ == "__main__":
    main()