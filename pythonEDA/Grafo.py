import math
import heapq
import random
from ListaLados import ListaLados
from Objeto import Objeto

class Grafo:
    def __init__(self, n=0, es_dirigido=False, node_positions=None):
        self.numvertices = n
        self.dirigido = es_dirigido
        self.adjlist = [None for _ in range(n)]
        self.objetos_en_nodo = {}

        # Parámetros de congestión y alerta
        self.peso_nodos = {i: 1 for i in range(n)}
        self.umbral = 5 # A partir de este numero de visitas el nodo se considera congestionado
        self.max_congestion = 3 #máximo de nodos congestionados simultáneamente
        self.alerta = {i: 0 for i in range(n)} # 0= libre, 1= congestión
        self.cola_congestion = [] 

        # Parámetros A*
        self.factor_preferencia = 1.0 # Reducción de costos para nodos impares
        self.factor_congestion = 1.0 # Aumento de costo por congestión
        self.k_sigmoidea = 1.0  # Sigmoidea
        self.EPS = 0.1  # Epilson, indica mínimo valor permitido
        self.node_positions = node_positions or {i: (0,0) for i in range(n)}
        self.jugadores_en_nodo = {i: [] for i in range(n)}  # lista de jugadores por nodo

        # Agregar un jugador a un nodo
    def agregar_jugador(self, nodo, jugador):
        if jugador not in self.jugadores_en_nodo[nodo]:
            self.jugadores_en_nodo[nodo].append(jugador)

    # Remover un jugador de un nodo
    def remover_jugador(self, nodo, jugador):
        if jugador in self.jugadores_en_nodo[nodo]:
            self.jugadores_en_nodo[nodo].remove(jugador)

    # Obtener jugadores en un nodo
    def get_jugadores(self, nodo):
        return self.jugadores_en_nodo.get(nodo, [])



    def agregarLado(self, x, y, w):
        curr = ListaLados(x, y, w)
        curr.next = self.adjlist[x]
        self.adjlist[x] = curr
        if not self.dirigido:
            curr = ListaLados(y, x, w)
            curr.next = self.adjlist[y]
            self.adjlist[y] = curr
    
    def mostrar_lados(self, x):
        curr = self.adjlist[x]
        while curr:
            print(f"({curr.x},{curr.y}), w = {curr.peso} -> ", end="")
            curr = curr.next
        print()
    
    def imprimir(self):
        print("num vertices:", self.numvertices)
        print("es dirigido?", self.dirigido)
        for i in range(self.numvertices):
            self.mostrar_lados(i)
    
    def read(self, edge_list):
        for line in edge_list:
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                raise ValueError("Cada línea debe tener el formato 'u,v,peso'")

            x = int(parts[0])
            y = int(parts[1])
            w = int(parts[2])
            self.agregarLado(x, y, w)
    
    #Sirve para obtener los nodos vecinos de un nodo dado,
    # lo cual es necesario para mover el personaje entre nodos en el juego.
    def get_neighbors(self, node):
        neighbors = []
        curr = self.adjlist[node]
        while curr:
            neighbors.append(curr.y)
            curr = curr.next
        return neighbors

    # --- Manejo de congestión ---
    # Actualizar peso base de un nodo y sus vecinos (congestión)
    def actualizar_pesos(self, nodo, incremento):
        self.peso_nodos[nodo] += incremento
        for vecino in self.get_neighbors(nodo):
            self.peso_nodos[vecino] += 2 # Aumenta en 2 los pesos de los vecinos del nodo congestionado

    # Actualizar congestión y alertas
    def actualizar_congestion(self, nodo, visitas):
        # Si llegó al umbral y aún no estaba en alerta
        if visitas >= self.umbral and self.alerta[nodo] == 0:
            print(f"⚠️ Nodo {nodo} congestionado!")
            self.alerta[nodo] = 1
            self.cola_congestion.append(nodo)
            self.actualizar_pesos(nodo, incremento=3) # Aumentar en 3 el peso del nodo congestionado


        # Si hay demasiados congestionados -> descongestionar uno
        while len(self.cola_congestion) > self.max_congestion:
            nodo_a_descongestionar = self.cola_congestion.pop(0)
            self.alerta[nodo_a_descongestionar] = 0
            self.peso_nodos[nodo_a_descongestionar] = max(1, self.peso_nodos[nodo_a_descongestionar] - 2) # Disminuye en 2 unidades el peso de los nodos descongestionados
            print(f"✅ Nodo {nodo_a_descongestionar} descongestionado")





    #----- Implementación del algoritmo A* -----
    # Función heurística: distancia absoluta entre el nodo actual y el objetivo
    def heuristica(self, nodo, objetivo):
        x1, y1 = self.node_positions[nodo]
        x2, y2 = self.node_positions[objetivo]
        return math.hypot(x2 - x1, y2 - y1)


    # Peso dinámico considerando congestión y preferencias del jugador
    def peso_dinamico(self, nodo, jugador, nodo_visitas):
        visitas = nodo_visitas.lookup(str(nodo)) or 0
        peso_base = self.peso_nodos.get(nodo, 1.0) # peso histórico/acumulado
        congest = 3 / (1 + math.exp(-(visitas - self.umbral)/self.k_sigmoidea)) # congestión actual
        #Si visitas << umbral, congest = 0 -> el nodo está libre, costo bajo
        #Si visitas = umbral, congest = 1.5 -> empieza a congestionarse, costo aumenta
        #Si visitas >> umbral, congest = 3 -> nodo muy congestionado, costo máximo
        indicador_impar = 1 if (nodo % 2 != 0 and getattr(jugador, "prefiere_impar", False)) else 0 # Preferencia por nodos impares
        peso_real = peso_base + self.factor_congestion * congest - self.factor_preferencia * indicador_impar # Peso final dinámico
        return max(peso_real, self.EPS)


    # Algoritmo A* modificado con selección aleatoria entre caminos óptimos
    def a_star_modificado(self, jugador, start, goal, nodo_visitas):
        if start == goal:
            return [start] 

        open_heap = [(0, start)] # lista de nodos por explorar ordenados por (f(n), nodo), donde: f(n)=costo total estimado
        came_from = {}
        visited = set() #conjunto de nodos ya explorados

        g_score = {i: float('inf') for i in range(self.numvertices)}
        g_score = {start: 0} 

        while open_heap:
            # Obtener nodo con f(n) mínimo
            f, current = heapq.heappop(open_heap)
            
            # Marcar que estamos pasando por current
            visitas_actual = nodo_visitas.lookup(str(current)) or 0
            nodo_visitas.insert(str(current), visitas_actual + 1)

            # Actualizar congestión si aplica
            self.actualizar_congestion(current, visitas_actual + 1)


            # Verificar si se llegó al objetivo
            if current == goal:
                # Reconstruir ruta completa
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()  # Para que vaya desde start hasta goal
                return path  # Devuelve toda la ruta
            
            # Marcar nodo como visitado
            if current in visited:
                continue
            visited.add(current)

            # Explorar vecinos
            vecinos = self.get_neighbors(current)
            random.shuffle(vecinos) # Aleatorizar el orden de exploración
            if not vecinos:
                continue

            # Calcular f(n) para cada vecino  
            for nb in vecinos:
                if nb in visited:
                    continue
                g_tentativo = g_score[current] + self.peso_dinamico(nb, jugador, nodo_visitas)
                if g_tentativo < g_score.get(nb, float('inf')):
                    came_from[nb] = current
                    g_score[nb] = g_tentativo
                    f_tentativo = g_tentativo + self.heuristica(nb, goal)
                    heapq.heappush(open_heap, (f_tentativo + random.uniform(0, 1e-6), nb))

        # Si no hay ruta, quedarse en el nodo actual
        return [start]

    # ----- Algoritmo de Prim -----
    # recorrido por el camino con menor peso usando Prim
    def prim_MinimumST(self, inicio):
        visitado = set()
        mst_lados = []
        p_queue = [] # priority queue (min-heap)
        total = 0

        # se añaden los lados del nodo inicial a la cola de prioridad
        visitado.add(inicio)
        curr = self.adjlist[inicio]
        while curr:
            heapq.heappush(p_queue, (curr.peso, inicio, curr.y))
            total += curr.peso
            curr = curr.next
        # mientras aún haya nodos por visitar
        while p_queue and len(visitado) < self.numvertices:
            peso, u, v = heapq.heappop(p_queue) # esto da el lado de menor peso

            # para evitar ciclos
            if v in visitado:
                continue
            
            visitado.add(v)
            mst_lados.append(ListaLados(u, v, peso))
            curr = self.adjlist[v]
            while curr:
                if curr.y not in visitado:
                    heapq.heappush(p_queue, (curr.peso, v, curr.y))
                    total += curr.peso
                curr = curr.next
        return mst_lados, total

    # recorrido por el camino con MAYOR peso usando Prim
    def prim_MaximunST(self, inicio):
        visitado = set()
        mst_lados = []
        p_queue = [] # para ahorrar espacio, se usará un min-heap con pesos negativos
        total = 0

        # se añaden los lados del nodo inicial a la cola de prioridad
        visitado.add(inicio)
        curr = self.adjlist[inicio]
        while curr:
            heapq.heappush(p_queue, (-curr.peso, inicio, curr.y))
            total += (-1*curr.peso)
            curr = curr.next
        # mientras aún haya nodos por visitar
        while p_queue and len(visitado) < self.numvertices:
            peso_neg, u, v = heapq.heappop(p_queue) # esto da el lado de mayor peso en negativo
            peso = -peso_neg # convertir de nuevo a positivo

            # para evitar ciclos
            if v in visitado:
                continue
            
            visitado.add(v)
            mst_lados.append(ListaLados(u, v, peso))
            curr = self.adjlist[v]
            while curr:
                if curr.y not in visitado:
                    heapq.heappush(p_queue, (-curr.peso, v, curr.y))
                    total += (-1*curr.peso)
                curr = curr.next
        return mst_lados, total
    