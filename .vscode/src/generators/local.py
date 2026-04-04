from faker import Faker
from Thevault_pero_bonito_no_como_La_otra_changadera.faker_chingadere import capacidades
import random
import pandas as pd 
import numpy as np
import string

def armar_dataset_local ( filas , columnas ):
    """ la fabrica de datos.
    recive la orden del pipilinais y decide si hacer las coass bien o explotrar"""

    dataset = {}


    # 🌿 MODO NATURAL: Datos con sentido usando tu diccionario
    print(f"🌿 [FÁBRICA] Modo Natural: Extrayendo datos orgánicos de Faker...")
    for col in columnas:
        if col in capacidades:
            # Llamamos a tu diccionario 'filas' veces
            dataset[col] = [capacidades[col]() for _ in range(filas)]
        else:
            # El legendario manejo de errores
            dataset[col] = ["Dato no soporto 💋"] * filas

    return dataset