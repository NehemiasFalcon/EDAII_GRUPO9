import random
from DoubleHashing import HashTable

Jugadores = []
   
class Jugador:
    def __init__(self, nombre, genero):
        self.__nombre = nombre
        self.__vida = 100
        self.__hashHabilidades = HashTable()
        self.__genero = genero
        self.__habilidad_pref = None
        self.__lista_Preferencias = []
        self.__lista_Nodos_Recorridos = []
        self.__pareja = None

        habilidades_base = ["Fuerza", "Velocidad", "Inteligencia", "Carisma", "Condicion_Fisica"]

        # Se agrega automáticamente a la lista de jugadores
        Jugadores.append(self)
        
        # Generar habilidad con su valor e ingresarlo en el hashHabilidades
        for habilidad in habilidades_base:
            self.__hashHabilidades.insert(habilidad, random.randint(1,100))

        # Generar aleatoriamente una habilidad preferencia respecto a la lista de habilidades_base
        self.__habilidad_pref = habilidades_base[random.randint(0, len(habilidades_base)-1)]
        

    def cambiar_vida(self, cambio):
        self.__vida += cambio

    def agregar_nodo_recorrido(self, nodo):
        if nodo not in self.__lista_Nodos_Recorridos:
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