import pandas as pd 
import os 

def export_al_csv(dataset,nombre_archivo = "dataset_generado.csv"):
    """
    recibe el diccionario de datos crudos, lo convierte en tabla
    y lo vomita como un archivo de excel o hoja de calculo si son jodidos"""

    print(f"\n [EXPORTER] preparando los datos para exportacion...")

    try: 
        # la magia de pandas: hace el diccionario en tabla 
        df = pd.DataFrame(dataset)

        if not nombre_archivo.endswith(".csv"):
            nombre_archivo += ".csv"

        #GUARDAMOS EL ARCHIVO
        #index = false evita que pandas agrege una columna inutil como el programador de esta chingadera

        df.to_csv(nombre_archivo, index=False, encoding='utf-8')

        #obtenemos la ruta absoluta para que el usuario sepa onde se va todo 

        ruta_completa = os.path.abspath(nombre_archivo)
        print(f"\n [EXPORTER] archivo exportado correctamente: {ruta_completa}")
        print (f"[EXPORTER] Resumen: {len(df)} filas exportadas")

        return True
    except Exception as e:
        print(f"\n [EXPORTER] Error al exportar el archivo: {e}")
        return False