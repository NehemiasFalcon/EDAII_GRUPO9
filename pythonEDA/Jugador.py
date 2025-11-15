import random
from DoubleHashing import HashTable

Jugadores = []

# ---------------- Estadísticas globales de jugadores----------------
class EstadisticasJugadores:
    suma_habilidades = 0
    num_jugadores = 0
    
    @staticmethod
    def promedio_global():
        if EstadisticasJugadores.num_jugadores == 0:
            return 0
        return EstadisticasJugadores.suma_habilidades / EstadisticasJugadores.num_jugadores

class Jugador:
    habilidades_base = ["Fuerza", "Velocidad", "Inteligencia", "Carisma", "Condicion_Fisica"]

    def __init__(self, nombre, genero):
        self.__nombre = nombre
        self.__vida = 100
        self.__hashHabilidades = HashTable()
        self.__genero = genero
        self.__habilidad_pref = None
        self.__lista_Preferencias = []
        self.__lista_Nodos_Recorridos = []
        self.__pareja = None

        # Se agrega automáticamente a la lista de jugadores
        Jugadores.append(self)
        
        # Generar habilidad con su valor e ingresarlo en el hashHabilidades
        for habilidad in self.habilidades_base:
            self.__hashHabilidades.insert(habilidad, random.randint(1,100))

        # Generar aleatoriamente una habilidad preferencia respecto a la lista de habilidades_base
        self.__habilidad_pref = self.habilidades_base[random.randint(0,4)]
        
        # Promedio inicial
        self.promedio = self.promedio_habilidades()

        # Actualizar estadísticas globales
        EstadisticasJugadores.suma_habilidades += self.promedio
        EstadisticasJugadores.num_jugadores += 1


    def cambiar_vida(self, cambio):
        self.__vida += cambio

    def agregar_nodo_recorrido(self, nodo):
        self.__lista_Nodos_Recorridos.append(nodo)

    def get_vida(self):
        return self.__vida

    def get_nombre(self):
        return self.__nombre

    def get_nodos_recorridos(self):
        return self.__lista_Nodos_Recorridos

    def get_hashHabilidades(self):
        return self.__hashHabilidades

    def agregar_en_lista_preferencias(self, item):
        self.__lista_Preferencias.append(item)
    
    def obtener_habilidad(self, nombre):
        return self.__hashHabilidades.lookup(nombre)
    
    def get_genero(self):
        return self.__genero
    
    def get_habilidad_pref(self):
        return self.__habilidad_pref
    
    def set_pareja(self, pareja):
        self.__pareja = pareja

    def get_pareja(self):
        return self.__pareja

    def __str__(self):
        return f"{self.__nombre} ({self.__genero})"
    
    def mostrar_habilidades(self):
        self.__hashHabilidades.imprimir(self.__nombre)
        print(f"Su habilidad preferida es: {self.__habilidad_pref}")
        print("\n")
        
    # Calcula el promedio individual de habilidades del jugador
    def promedio_habilidades(self):
        total = 0
        for habilidad in self.habilidades_base:
            valor = self.__hashHabilidades.lookup(habilidad)
            if valor is not None:
                total += valor
        return total / len(self.habilidades_base)
    
    # Actualiza el promedio individual y las estadísticas globales cuando el jugador cambia
    def actualizar_promedio(self):
        EstadisticasJugadores.suma_habilidades -= self.promedio
        nuevo = self.promedio_habilidades()
        EstadisticasJugadores.suma_habilidades += nuevo
        self.promedio = nuevo
    
    # Determina si el jugador es fuerte comparado con el resto
    def es_fuerte(self):
        return self.promedio_habilidades() >= EstadisticasJugadores.promedio_global()   
