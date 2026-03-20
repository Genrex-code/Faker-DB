#imports rancios
#duerman al programador que hiso esto

print("Generador de base de datos sinteticos")
print("Crea datos para pruebas en ambientes controlados :3")
#si ya se que queda algo inutil pero aca agregare mas limitantes en el futuro cuando
# se tengan que manejar muchos mas datos de forma provicional se queda asi (como la casa del boiler)
# si leen esto WEBOS
#duerman al programador de esto esta sufriendo mucho

def LIMITANTE(maximofila):
    maximofila = 1000000
    return maximofila

def pedir_entero (mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                print("ingresa un numero mayor a 0")
            else:
                return valor
        except:
            ValueError("el dato es incorrecto")

while True:
    NameDataset= str(input("Ingresa el nombre de tu DATASET: "))
    if NameDataset == "":
        print ("El nombre no puede estar vacio")
        if NameDataset == " ":
            print("El Dataset no puede tener espacios")
    else:
        break
    #PREGUNTAR COLUMNAS
while True:
    try:
        NumCol = int(input("Cuantas Columnas Desea???: "))
        break # es un limitante si salio bien 
    
    except  ValueError: 
        print("Error: SOLO SE ADMITEN NUMEROS D:")
#preguntar el nombre de cada columna y de aca sacar el tipo de dato natural a generar
#asi mapeo 2 datos de uno 
COLUMNAS = []
for _ in range (NumCol):
    nombre_col = input(f"Como se llamara su columna {_+1} ???")
    tipocolumnas = input(f"Que tipo de dato nesesita para la columna {_+1}")
    #unimos el desmadre
    COLUMNAS.append(f"{nombre_col} {tipocolumnas}")
# preguntar filas 
while True:
     try:
        NumFila = int(input("Cuantas Filas Nesesitas???"))
        break
     except ValueError:
         print("ERROR: SOLO SE ADMITEN NUMEROS D:")
if NumFila > LIMITANTE(maximofila=1000000):
    print(f"el numero de registros excede el limte {LIMITANTE} se ajustara al limite")
    NumFila = LIMITANTE