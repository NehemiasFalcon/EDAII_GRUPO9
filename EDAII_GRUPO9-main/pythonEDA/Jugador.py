import random

# Acá se añadirán a todos los jugadores
Jugadores = []

# ---------------- Double Hashing ----------------
class Entry:
    # Código trabajado en clase pasado a lenguaje python, sin cambios
    def __init__(self, key: str, value: int):
        self._key = key
        self._value = value
        self._isDeleted = False

class HashTable:
    # Código trabjado en clase pasado a lenguaje python, solo con la implementación de una nueva variable
    def __init__(self, size=5):
        self.__size = size
        self.__bins = [None] * size
        self.__num_keys = 0
        # Se establece el primo menor respecto al tamaño fijo que se ha establecido antes, el cual viene a ser size = 5. Esto se debe a que
        # el double hashing recomienda que sea así para que el salto que se hará, sea un recorrido dentro de la tabla.
        self.__R = 3

    # Código trabajado de hashFunction pasado a lenguaje python, sin cambios.
    def hashFunction(self, key: str):
        hash_val = 0
        for c in key:
            hash_val = (hash_val * 31 + ord(c)) % self.__size
        return hash_val

    # Función hashFunction2 que ayuda a determinar el salto que dará por la clave que se ingresará
    def hashFunction2(self, key: str):
        hash_val = 0
        # Se usará otro primo diferente respecto al hashFunction para que devuelva un valor diferente,
        # en este caso se usará un valor de 17
        for c in key:
            hash_val = (hash_val * 31 + ord(c)) % self.__size
        # Se halla el valor del salto que dará por la clave que se ingresará
        step = self.__R - (hash_val % self.__R)
        # Si en caso el valor del salto es 0, entonces se cambiará por el valor de 1, ya que el double hashing establece la restricción que el salto
        # no puede ser 0.
        if step == 0:
            step = 1
        return step

    # Función find que cumple el mismo objetivo del libro de Weiss donde se adaptó el double hashing (en el que se puede ver un método find), el cual
    # busca determinar la posición de la clave, pero mediante el step, de modo que mejora la búsqueda.
    def find(self, key: str):
        index = self.hashFunction(key)
        step  = self.hashFunction2(key)
        count = 0

        while self.__bins[index] is not None and not self.__bins[index]._isDeleted and self.__bins[index]._key != key and count < self.__size:
            index = (index + step) % self.__size
            count += 1

        return index

    # Función insert que fue adaptado del libro de Weiss, el cual buscar insertar o actualizar un valor.
    def insert(self, key: str, value: int):
        # Llama a la función find para determinar la posición de la clave.
        pos = self.find(key)

        # En caso la posición no esté ocupada, entonces se insertará la llave con su valor.
        if self.__bins[pos] is None or self.__bins[pos]._isDeleted:
            self.__bins[pos] = Entry(key, value)
            self.__num_keys += 1
        # Caso contrario, se actualizará el valor
        else:
            self.__bins[pos]._value = value

        return True

    #La función lookup fue modificada para que haga los saltos establecidos en cada llave, de modo que, se optimice la búsqueda.
    def lookup(self, key: str):
        index = self.hashFunction(key)
        step = self.hashFunction2(key)
        count = 0

        while self.__bins[index] is not None and count < self.__size:
            if not self.__bins[index]._isDeleted and self.__bins[index]._key == key:
                return self.__bins[index]._value
            # En vez de sumar + 1, sumará con el salto para que realice una búsqueda más rapida
            index = (index + step) % self.__size
            count += 1
        return None

    # Código imprimir trabajado en clase pasado a lenguaje python, con la única modificación que se adapte a un jugador.
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



#Algoritmo similar al de Gale-Shapley donde SOLO las chicas proponen al inicio del juego
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
            print(f"❤  {chicas[g].get_nombre()} elige por primera vez a {chicos[b].get_nombre()} "
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
        print(f"{chico.get_nombre()}  ❤   {chica.get_nombre()}")



# Validar que todo funcione con respecto a matrimonio: 
for jugador in Jugadores:
    print(f"La pareja de {jugador.get_nombre()} es {jugador.get_pareja()}")


#Una vez iniciado el juego, recibe dos CHICOS, detecta automáticamente sus parejas, evalúa si hay mejora mutua y realiza el intercambio si conviene.
def intercambio_mutuo_de_parejas(chico1, chico2):
    # Obtener las parejas actuales de ambos chicos
    chica1 = chico1.get_pareja()
    chica2 = chico2.get_pareja()

    # Validación de que ambos tengan pareja
    if chica1 is None or chica2 is None:
        print("❌ No se puede intercambiar: uno de los chicos no tiene pareja.")
        return False

    print("\n🔍 Evaluando posible intercambio:")
    print(f"• {chico1.get_nombre()} ❤ {chica1.get_nombre()}")
    print(f"• {chico2.get_nombre()} ❤ {chica2.get_nombre()}")

    #Habilidades preferidas por cada chico
    pref1 = chico1.get_habilidad_pref()
    pref2 = chico2.get_habilidad_pref()

    #Valores actuales según su preferencia
    chico1_actual = chica1.obtener_habilidad(pref1)
    chico2_actual = chica2.obtener_habilidad(pref2)

    #Aca se almacenan los valores de las habilidades si intercambian
    chico1_con_chica2 = chica2.obtener_habilidad(pref1)
    chico2_con_chica1 = chica1.obtener_habilidad(pref2)

    print(f"\nComparación de mejoras:")
    print(f"- {chico1.get_nombre()}: actual {chico1_actual}, con {chica2.get_nombre()} {chico1_con_chica2}")
    print(f"- {chico2.get_nombre()}: actual {chico2_actual}, con {chica1.get_nombre()} {chico2_con_chica1}")

    #Ver si ambos mejoran
    if chico1_con_chica2 > chico1_actual and chico2_con_chica1 > chico2_actual:

        # --- Realizar intercambio ---
        chico1.set_pareja(chica2)
        chica2.set_pareja(chico1)

        chico2.set_pareja(chica1)
        chica1.set_pareja(chico2)

        print("\n✅ INTERCAMBIO REALIZADO:")
        print(f"   {chico1.get_nombre()} ❤ {chica2.get_nombre()}")
        print(f"   {chico2.get_nombre()} ❤ {chica1.get_nombre()}")
        return True

    print("\n❌ No se realizó el intercambio: no beneficia a ambos.")
    return False