# si te lo preguntas si es un pipeline normal solo que quiero ser esquiso por un rato con mis tonterias ramdon ok?
# aca entran todos los datos de forma global y se van a ir procesando en cada etapa del pipeline

import sys
from generators.local import armar_dataset_local
# NOTA MENTAL: Cuando quieras que el CSV funcione de verdad, importa tu exporter aquí arriba.
from generators.grandote import generar_masivo # Importamos el generador de alto rendimiento
class State: 
    """
    EL pipilinais: director del flujo de trabajo recibe la orden del main y manda a trabajar a los generadores y exportadores
    """

    def __init__(self, config):
        # guardamos la orden mundial del mian
        self.config = config
        # aqui guardamos nuestra macorden
        self.dataset = None # Aquí se guardará el dataset generador

    def run(self):
        """
        el boton de encendido del pipilinais
        """
        print("\n[Pipilinais] Iniciando el proceso de generación de datos...")

        # 1.- Extraemos lo importante de la configuracion
        # usamos .get() por si la llaves no existe no se caleinte y truene
        filas = self.config.get("filas_a_generar", 0) # Por defecto 0
        columnas = self.config.get("columnas_pedidas", [])
        formato_salida = self.config.get("formato_salida", "terminal")
        modo_debug = self.config.get("modo_debug", False)
        
        # el modo perrita es el modo de alto rendimiento sin validaciones ni limitantes directamente control
        # as el sistema desde su formato mas RAW💋
        modo_perrita = self.config.get("modo_perrita", False)
        
        if not columnas:
            columnas = ['nombre', 'email']
            print(" tienes que escribir columnas para generar columnas tonoto")

        if modo_debug:
            print(f"🐛 [DEBUG] Configuración recibida en el Pipilinais: {self.config}")
            print(f"🐛 [DEBUG] Parámetros extraídos - Filas: {filas}, Columnas: {columnas}, Formato: {formato_salida}, Modo Perrita: {modo_perrita}")

        if modo_perrita:
            print("💋 MODO PERRITA ACTIVADO: Sin validaciones, sin límites. Y LA QUESO 💋.")
            
            # Como el modo perrita se lanza por comando sin preguntar en el menú,
            # si el usuario no mandó filas, le ensartamos 1 millón para el test de estrés xd
            if filas == 0:
                filas = 1000000
                print(f"🐶 [PIPILINAIS] Como no especificaste, te van {filas} filas por defecto.")
            
            # Si las columnas están por defecto de los tonotos, metemos basura
            if columnas == ['nombre', 'email']:
                columnas = ['id_caos', 'texto_basura1', 'texto_basura2']
                
            # Mandamos a llamar al grandote
            self.dataset = generar_masivo(filas, columnas)
            
        else:
            # Flujo normal para los mortales
            self.dataset = armar_dataset_local(filas, columnas)

        # La exportación sigue igual para todos
        self.exportar_datos(formato_salida)
    
        # ¡Corregido! Ya están dentro del 'run' y usando 'self.dataset'
        self.dataset = armar_dataset_local(filas, columnas)
        self.exportar_datos(formato_salida)

    def exportar_datos(self, formato):
        """Se encarga de decidir cómo se entrega el paquete al usuario."""
        print("\n[PIPILINAIS] 🚚 Preparando la entrega de datos...")

        if formato == "terminal":
            self.mostrar_en_terminal()
            
        elif formato == "csv":
            print("📊 [EXPORTER] (Simulación) Guardando archivo CSV/Excel... (Falta conectar Pandas)")
            # Aquí en el futuro llamarás a tu archivo de exportación con Pandas
            self.mostrar_en_terminal() # Lo mostramos en terminal por ahora para ver que funcione
            
        elif formato == "sql":
            print("🛢️ [EXPORTER] (Simulación) Generando script SQL... (Falta armar la lógica)")
            self.mostrar_en_terminal()
            
        else:
            print(f"❌ [PIPILINAIS] Formato '{formato}' desconocido. Te lo imprimo aquí para que no llores.")
            self.mostrar_en_terminal()

    def mostrar_en_terminal(self):
        """ inprime los datos crudos para validar que la maquina sirve"""
        print("\n ---Resultado del dataset generado---")
         
        # Cambiamos dataset_final por dataset (como lo pusiste en el init)
        if self.dataset is None:
            print("❌ No hay datos para mostrar, la fábrica explotó.")
            return

        for columna, valores in self.dataset.items():
            muestra = valores[:5]
            sobrantes = len(valores) - len(muestra) # ¡Aquí calculamos los sobrantes!
             
            if sobrantes > 0: 
                print(f"👉 {columna.upper()}: {muestra} (y {sobrantes} más...)")
            else:
                print(f"👉 {columna.upper()}: {valores}")