from faker import Faker
from F_dic.faker_chingadere import capacidades , fake
from main import *
from main import tipocolumnas,COLUMNAS
import random
import pandas as pd 
import numpy as np
import string 
#el import pasado lo pasare como argumentos de def

fake = Faker ('es_MX')
#recordar agregar el cambiar de idioma
#nota les meti abreviaciones porque si
# para que se vea mas chingon poes :3
#amn es = amount o cantidad en inglish para hacernos los 
#que si sabesmos aunque estemos vagnado con esto

#busca en el diccionario y ejecuta la funcion
def natural (NumFila,tipocolumna,nombre_col):
    #para buscar
    if capacidades in capacidades:
        return [capacidades() for i in range(NumFila)]
    else:
        return fake.word(),["ERROR:NO SE ENCONTRO UN TIPO EXACTO SE APLICARA UN GENERATIVO GENERICO"]
    
def BIGINT (NumFila,tipocolumna,nombre_col):
    name = nombre_col.lower()
    type = tipocolumna.lower()
    amn = NumFila
    if "bigint" in type:
        return random.randint(1,100000)

def BIGDEC (NumFila,tipocolumna,nombre_col):
    name = nombre_col.lower()
    type = tipocolumna.lower()
    amn = NumFila
    if "bigdec" in type:
        return random.uniform(1.0,100000.0)

def BIGSTR (NumFila,tipocolumna,nombre_col):
    name = nombre_col.lower()
    type = tipocolumna.lower()
    amn = NumFila
    if "bigstr" in type:
        return random.choice(string.ascii_letters)

#dinamico dinamistico
#neta como me gusta la musica de linkin park 
#la nueva vocalista es wena y nadie me llevara la contraria >:l
def ARMADO (NumFila,tipocolumna,nombre_col):
    #lista basia para que no truene 
    dataset = {}
    for col in COLUMNAS:
        #aca se hace la buscqueda de lo que se escribio el usuario en la terminal (luego interfaz)
        #en nuestro diccionario
        if col in capacidades:
            dataset[col] = [capacidades[col]() for _ in range (NumFila)]
            #debi haber usado un elif pero nooo queria hacerme el que si sabia
            #duerman al programador y regresenlo al kinder
        else:
            dataset [col] = ["Dato no soporto 💋"] * NumFila
