import random

# Acá se añadirán a todos los jugadores
Jugadores = []

# ---------------- HashTable - Linear Probing ----------------
class Entry:
    def __init__(self, key: str, value: int):
        self._key = key
        self._value = value
        self._isDeleted = False

class HashTable:
    def __init__(self, size=5):
        self.__size = size
        self.__bins = [None] * size
        self.__num_keys = 0

    def hashFunction(self, key: str):
        hash_val = 0
        for c in key:
            hash_val = (hash_val * 31 + ord(c)) % self.__size
        return hash_val

    def insert(self, key: str, value: int):
        index = self.hashFunction(key)
        count = 0
        while self.__bins[index] is not None and not self.__bins[index]._isDeleted and self.__bins[index]._key != key and count < self.__size:
            index = (index + 1) % self.__size
            count = count + 1
        
        if count == self.__size:
            return False
        
        if self.__bins[index] is None or self.__bins[index]._isDeleted:
            self.__bins[index] = Entry(key, value)
            self.__num_keys = self.__num_keys + 1
        else:
            self.__bins[index]._value = value

        return True
    
    def lookup(self, key: str):
        index = self.hashFunction(key)
        count = 0
        while self.__bins[index] is not None and count < self.__size:
            if not self.__bins[index]._isDeleted and self.__bins[index]._key == key:
                return self.__bins[index]._value
            index = (index + 1) % self.__size
            count = count + 1
        return None

    def imprimir(self, nombre):
        print(f"HABILIDADES DE {nombre.upper()}: ")
        for index in range(self.__size):
            print(f"[{index}]: ", end = "")
            if self.__bins[index] is None:
                print("null")
            elif self.__bins[index]._isDeleted:
                print("deleted")
            else:
                print(f"({self.__bins[index]._key}, {self.__bins[index]._value})")
        print()

            
# ---------------- Jugador ----------------
class Jugador:
    def __init__(self, nombre, genero):
        self.__nombre = nombre
        self.__vida = 100
        self.__hashHabilidades = HashTable()  # HashTable dentro del jugador
        self.__genero = genero
        self.__habilidad_pref = None #funcion, con igual de probabilidad? /
        self.__lista_Preferencias = [] #/
        self.__lista_Nodos_Recorridos = [] #/
        self.__pareja = None #nombre de pareja

        habilidades_base = ["Fuerza", "Velocidad", "Inteligencia", "Carisma", "Condicion_Fisica"]

        # Se agrega automáticamente a la lista de jugadores
        Jugadores.append(self)
        
        # Generar habilidad con su valor e ingresarlo en el hashHabilidades
        for habilidad in habilidades_base:
            self.__hashHabilidades.insert(habilidad, random.randint(1,100))

        # Generar aleatoriamente una habilidad preferencia respecto a la lista de habilidades_base
        self.__habilidad_pref = habilidades_base[random.randint(0,4)]
        

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

    def agregar_en_lista_preferencias():
        return None
    
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

    def get_color(self):
        return self.__color

    def __str__(self):
        return f"{self.__nombre} ({self.__genero})"
    
    def mostrar_habilidades(self):
        self.__hashHabilidades.imprimir(self.__nombre)
        print(f"Su habilidad preferida es: {self.__habilidad_pref}")
        print("\n")
    

# Crear jugadores

jugador1 = Jugador("Nehemias", "Masculino")
jugador2 = Jugador("Mariel", "Femenino")
jugador3 = Jugador("Marisol", "Femenino")
jugador4 = Jugador("Sebastian", "Masculino")
jugador5 = Jugador("Melissa", "Femenino")
jugador6 = Jugador("Candiotti", "Masculino")
jugador7 = Jugador("Guti", "Masculino")
jugador8 = Jugador("Priscila", "Femenino")
jugador9 = Jugador("Ariana", "Femenino")
jugador10 = Jugador("Pekka", "Masculino")

# Crear las listas de géneros
JugadoresHombres = []
JugadoresMujeres = []

print("///////////////////////////////////////////")

# Agregar a las listas dependiendo de su género
for jugador in Jugadores:
    if (jugador.get_genero() == "Masculino"):
        JugadoresHombres.append(jugador)
    else:
        JugadoresMujeres.append(jugador)

# Imprimir las habilidades con sus puntajes de los hombres
for hombre in JugadoresHombres:
    hombre.get_hashHabilidades().imprimir(hombre.get_nombre())



#Algoritmo Gale-Shapley donde las chicas proponen al inicio del juego
def gale_shapley(chicos, chicas): #Lo hecho en clase a Python menos chicaprefs
    n = len(chicas)
    chicas_libres = list(range(n))
    chicos_libres = [True] * len(chicos)
    sig_propuesta = [0] * n
    pareja_chico = [-1] * len(chicos)
    pareja_chica = [-1] * n

    # Preferencias de cada chica basadas en su habilidad preferida
    chicaprefs = [
        sorted(
            range(len(chicos)),
            key=lambda i: chicos[i].obtener_habilidad(chica.get_habilidad_pref()),
            reverse=True
        )
        for chica in chicas
    ]

    #Gale–Shapley (solo las chicas proponen)
    while chicas_libres:
        g = chicas_libres[-1]  # índice de la chica actual
        b = chicaprefs[g][sig_propuesta[g]]  # chico que la chica prefiere en este turno
        sig_propuesta[g] += 1

        if chicos_libres[b]:
            # El chico está libre, se forma una nueva pareja
            pareja_chica[g] = b
            pareja_chico[b] = g
            chicos_libres[b] = False
            chicas_libres.pop()

            #Validación visual
            print(f"❤️  {chicas[g].get_nombre()} elige por primera vez a {chicos[b].get_nombre()} "
                f"(basado en su habilidad preferida: {chicas[g].get_habilidad_pref()})")

        else:
            #el chico ya tiene pareja, no cambia porque el chico no decide aun
            print(f"❌  {chicas[g].get_nombre()} intenta elegir a {chicos[b].get_nombre()}, "
                f"pero él ya está emparejado con {chicas[pareja_chico[b]].get_nombre()}.")
            # La chica intentará con su siguiente opción en el próximo ciclo
            continue

    return pareja_chico, pareja_chica


parejaB, parejaG = gale_shapley(JugadoresHombres, JugadoresMujeres)

print("\n---RESULTADO INICIAL (GaleShapley, chicas deciden)---")
for i, chico in enumerate(JugadoresHombres):
    if parejaB[i] != -1:
        chica = JugadoresMujeres[parejaB[i]]
        chico.set_pareja(chica)
        chica.set_pareja(chico)
        print(f"{chico.get_nombre()}  ❤️   {chica.get_nombre()}")



# Validar que todo funcione con respecto a matrimonio: 
for jugador in Jugadores:
    print(f"La pareja de {jugador.get_nombre()} es {jugador.get_pareja()}")