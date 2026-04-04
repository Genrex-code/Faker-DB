import numpy as pn #paresco morro de secu yo se 
import string
import time
import os 
import multiprocessing
import threading

def generar_masivo(filas,columans):
    """MODO PERRITA
    Generacion bruta con Numpy. cero validaciones , cero diccionarios,pura velocidad.
    Hecho para demostrar quien es la perrita de quien
    CONTADOR DE VICTORIAS DEL MODO PERRITA: lllll lllll ll
    CONTADOR DE VICTORIAS DEL USUARIO: lll """

    print (f"[Grandote] Preparando todo like pizza at speed of light...") #OMG GD referencia 
    print   (f"[Grandote] Generando {filas} Registros...")

    #le voa dar un sape a quien mueva esto neta 
    inicio = time.time()
    dataset = {}

    letras = list(string.ascii_uppercase + string.digits) #basura betanumerica

    for col in columans:
        #adivinamos si quiere numeros
        if any (palabra in col.lower() for palabra in ['num','id','edad','saldo']):
            #numpy genera enteros en microsegundos
            #el tolist() para que no llore el pipilinais 
            dataset[col] = pn.random.randint(0, 1000, size=filas).tolist()
        else:
# si no quiere numeros , generamos basura de 10 catacteres al azar
            dataset[col] = [''.join(pn.random.choice(letras, size=10)) for _ in range(filas)]

    FIN = time.time()
    tiempo_total = round (FIN - inicio, 4)
    print (f"[Grandote] Generacion Completa en {tiempo_total} segundos. ¡Soy la perrita más rápida del mundo!")
    return dataset