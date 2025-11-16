import pygame
import Jugador
import random
import time
import math
import heapq
from Grafo import Grafo
from Jugador import HashTable
from GaleShapley import gale_shapley
from Objeto import Objeto

# ---------- Configuración ----------
pygame.init()
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Grafo")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
RED = (255, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (255, 165, 0), (128, 0, 128), (0, 0, 255)]

FPS = 30
RADIUS = 20

# ---------- Crear grafo ---------- HECHO EN CLASE
# Posiciones de los nodos
node_positions = {
    0: (50, 350),
    1: (200, 100),
    2: (200, 300),
    3: (200, 500),
    4: (200, 700),
    5: (350, 200),
    6: (350, 600),
    7: (500, 400),
    8: (500, 125),
    9: (650, 150),
    10: (500, 675),
    11: (650, 550),
    12: (800, 425),
    13: (800, 650),
    14: (350, 750),
    15: (350, 50),
    16: (650, 350)
}


numv = 17 #numero de vertices
g = Grafo(numv, es_dirigido=False, node_positions=node_positions) #cambiar a True si es dirigido
edge_list = [
    "0,1,10",
    "0,2,3",
    "0,3,6",
    "0,4,8",
    "1,2,5",
    "1,5,9",
    "1,15,4",
    "2,3,1",
    "2,5,5",
    "3,4,7",
    "3,6,6",
    "4,6,5",
    "4,14,12",
    "5,15,9",
    "5,8,8",
    "5,7,2",
    "15,8,9",
    "6,7,1",
    "6,14,5",
    "6,10,10",
    "6,5,15",
    "14,10,15",
    "8,7,4",
    "8,9,10",
    "7,9,5",
    "7,11,13",
    "7,10,12",
    "10,11,13",
    "9,12,5",
    "16,7,5",
    "16,9,9",
    "16,11,14",
    "16,12,8",
    "11,12,3",
    "11,13,7",
    "12,13,8",
]
g.read(edge_list)
print("---GRAFO CREADO---")
g.imprimir()
print("------------------") 

# Contador de visitas por cada nodo
nodo_visitas = HashTable(size=numv)
for nodo in range(numv):
    nodo_visitas.insert(str(nodo), 0)

# ---------- Jugador ----------
num_jugadores = 6
jugadores = []
hombres = []
mujeres = []
for i in range(num_jugadores // 2):
    h = Jugador.Jugador(f"Hombre {i+1}", "Masculino")
    m = Jugador.Jugador(f"Mujer {i+1}", "Femenino")
    hombres.append(h)
    mujeres.append(m)
    jugadores.append(h)
    jugadores.append(m)

# Asignar en nodos aleatorios
current_node = 0
nodos_disponibles = list(range(g.numvertices))  # Todos los nodos del grafo
random.shuffle(nodos_disponibles)  # Mezclar nodos para que sea aleatorio

habilidades_promedio = []
for idx, player in enumerate(jugadores):
    nodo_inicial = nodos_disponibles[idx]  # Toma un nodo único de la lista
    player.agregar_nodo_recorrido(nodo_inicial)
    g.agregar_jugador(nodo_inicial, player)  # Asegúrate de agregarlo al grafo
    heapq.heappush(habilidades_promedio, (player.promedio_habilidades(), player))

# ---- Configuración específica por jugador ----

# Hombre 1 y Mujer 1 usarán Prim
h1 = hombres[0]  # Hombre 1
m1 = mujeres[0]  # Mujer 1
h1.camino_prim = [] # para guardar el camino 
m1.camino_prim = []
h1.camino_prim_indice = 0 # para recorrer el camino 
m1.camino_prim_indice = 0

# Hombre 2 y Mujer 2 usarán A*
h2 = hombres[1]  # Hombre 2
m2 = mujeres[1]  # Mujer 2
h2.ultima_ruta = []
h2.ultima_ruta_obj = None
m2.ultima_ruta = []
m2.ultima_ruta_obj = None

for j in [h2, m2]:
    j.prefiere_impar = True       # Baja costo para nodos impares
    j.modo_follow = False         # Inicio sin persecución
    # Objetivo temporal aleatorio, distinto al start
    start = j.get_nodos_recorridos()[-1]
    j.objetivo = start
    while j.objetivo == start:
        j.objetivo = random.randint(0, g.numvertices - 1)

# El resto se moverán aleatoriamente

# ---------- Mostrar habilidades iniciales de los jugadores ----------
print("\n======= HABILIDADES INICIALES DE LOS JUGADORES =======")
for j in jugadores:
    print(f"{j.get_nombre()} ({j.get_genero()}):")
    for habilidad in Jugador.Jugador.habilidades_base:
        valor = j.obtener_habilidad(habilidad)
        print(f"  {habilidad}: {valor}")
    print(f"Habilidad preferida: {j.get_habilidad_pref()}")
    print(f"Promedio de habilidades: {j.promedio_habilidades():.2f}")
    print("-----------------------------------")

# ---------- Emparejar parejas al inicio usando Gale-Shapley ----------
pareja_chico, pareja_chica = gale_shapley(hombres, mujeres)

# Asignar parejas como atributo en cada jugador
for i, h in enumerate(hombres):
    if pareja_chico[i] != -1:
        h.set_pareja(mujeres[pareja_chico[i]])
        mujeres[pareja_chico[i]].set_pareja(h)

print("\n💞 Parejas formadas al inicio del juego:")
for h in hombres:
    if h.get_pareja():
        print(f"{h.get_nombre()} ❤️ {h.get_pareja().get_nombre()}")


# ---------- Funciones ----------
def mostrar_mensaje_flotante(screen, mensaje, duracion=2, color=(255,0,0)):
    
    font = pygame.font.SysFont("arial", 30, bold=True)
    text_surface = font.render(mensaje, True, color)
    # Posición: arriba al centro
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    # Se mantiene por 'duracion' segundos sin bloquear la ventana
    start_time = time.time()
    while time.time() - start_time < duracion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Solo refrescamos la pantalla para que no se congele el juego
        clock.tick(FPS)

def mostrar_ganador_pantalla(screen, ganador, pareja=None):
    font_big = pygame.font.SysFont("arial", 50, bold=True)
    font_small = pygame.font.SysFont("arial", 30)

    screen.fill((0, 0, 0))  # Fondo negro

    # ---------------------
    # GANADOR POR DEFECTO
    # ---------------------
    titulo = font_big.render("GANADOR", True, (255, 215, 0))
    screen.blit(titulo, (200, 120))

    texto_nombre = font_big.render(f"{ganador.get_nombre()}", True, (255, 255, 255))
    screen.blit(texto_nombre, (200, 200))

    # -------------------------------------------------------
    # SI VIENE UNA PAREJA, MOSTRAR TEXTO ESPECIAL DE PAREJA
    # -------------------------------------------------------
    if pareja is not None:
        j1, j2 = pareja

        texto_pareja1 = font_small.render(
            f"Queda una pareja viva: Hombre {j1.get_nombre()} y Mujer {j2.get_nombre()}",
            True, (180, 180, 255)
        )

        texto_pareja2 = font_small.render(
            f"Gana {ganador.get_genero()} {ganador.get_nombre()} por mayor promedio de habilidades.",
            True, (255, 200, 200)
        )

        screen.blit(texto_pareja1, (200, 340))
        screen.blit(texto_pareja2, (200, 380))

    pygame.display.update()
    time.sleep(10)

def draw_graph():
    WIN.fill(WHITE)
    # Dibujar aristas
    for i in range(numv):
        curr = g.adjlist[i]
        while curr:
            start = node_positions[i]
            end = node_positions[curr.y]
            pygame.draw.line(WIN, BLACK, start, end, 2)
            font = pygame.font.SysFont(None, 20)
            text = font.render(str(curr.peso), True, BLACK)
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            WIN.blit(text, (mid_x, mid_y))
            curr = curr.next
    # Dibujar nodos
    for node, pos in node_positions.items():
        color = RED if node == current_node else BLUE
        pygame.draw.circle(WIN, color, pos, RADIUS)
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(node), True, BLACK)
        WIN.blit(img, (pos[0]-8, pos[1]-10))
    
    # Dibujar jugadores
    font = pygame.font.SysFont(None, 18)
    jugadoresXnodo = {}
    for idx, j in enumerate(jugadores):
        nodos = j.get_nodos_recorridos()
        if not nodos:
            continue
        jugadoresXnodo.setdefault(nodos[-1], []).append((idx, j))

    player_radius = max(5, RADIUS // 4)

    for node, listaJugadores in jugadoresXnodo.items():
        cx, cy = node_positions[node]
        count = len(listaJugadores)
        spacing = player_radius * 2 + 4
        # Posición inicial X para centrar a los jugadores en el nodo
        start_x = int(cx - (spacing * (count - 1)) / 2)
        # Posición Y (ligeramente por encima del centro del nodo)
        py = cy - player_radius - 2 
        
        for k, (idx, j) in enumerate(listaJugadores):
            px = start_x + k * spacing
            color = COLORS[idx % len(COLORS)]
            pygame.draw.circle(WIN, color, (px, py), player_radius)
            
            # Dibujar nombre del jugador debajo de su círculo
            text = font.render(j.get_nombre(), True, BLACK)
            text_rect = text.get_rect(center=(px, py + player_radius + 8))
            WIN.blit(text, text_rect)

    pygame.display.update()

def mover_jugadores():
    print("\n -------NUEVO TURNO-------")

    for j in jugadores:
        actual = j.get_nodos_recorridos()[-1]
        sig = actual
        # Indica si el jugador llegó exitosamente al 'sig'. Si no se mueve no consigue objeto
        moved = False  

        # --- NUEVO: remover jugador del nodo actual ---
        g.remover_jugador(actual, j)

        # --- Lógica de Prim para Hombre 1 y Mujer 1 ---
        if j.get_nombre() in ["Hombre 1", "Mujer 1"]:
            # Si ya recorrió todo el camino, calcular uno nuevo
            if j.camino_prim_indice >= len(j.camino_prim):
                es_fuerte = j.es_fuerte()
                tipo_mst = "MAX" if es_fuerte else "MIN"
                print(f"{j.get_nombre()} ({tipo_mst}): nuevo MST desde nodo {actual}.")

                if es_fuerte:
                    mst_lados, total = g.prim_MaximunST(actual)
                else:
                    mst_lados, total = g.prim_MinimumST(actual)
                
                # Construir camino desde los lados
                j.camino_prim = [lado.y for lado in mst_lados]
                j.camino_prim_indice = 0
                
                if not j.camino_prim:
                    print(f"{j.get_nombre()} no tiene camino Prim disponible desde nodo {actual}")
                    vecinos = g.get_neighbors(actual)
                    sig = random.choice(vecinos) if vecinos else actual

            # Si hay camino Prim disponible, avanzar
            if j.camino_prim:
                sig = j.camino_prim[j.camino_prim_indice]
                j.camino_prim_indice += 1
                print(f"PRIM: {j.get_nombre()} va al nodo {sig}")
            else:
                sig = actual  # Quedarse en el mismo nodo
                print(f"{j.get_nombre()} no tiene camino Prim disponible desde nodo {actual}")


        # --- Lógica Algoritmo A* para Hombre 2 y Mujer 2 ---
        elif j.get_nombre() in ["Hombre 2", "Mujer 2"]:
            # Si llegó al objetivo, elegir uno nuevo diferente
            if actual == j.objetivo:
                nuevo_obj = actual
                while nuevo_obj == actual:
                    nuevo_obj = random.randint(0, g.numvertices - 1)
                print(f"A*: {j.get_nombre()} ha llegado a su objetivo y elige nuevo objetivo: desde nodo {actual} a {nuevo_obj}")
                j.objetivo = nuevo_obj

            # Recalcular ruta completa desde nodo actual hasta objetivo
            if not j.ultima_ruta or j.ultima_ruta[0] != actual:
                j.ultima_ruta = g.a_star_modificado(j, actual, j.objetivo, nodo_visitas)
            j.ultima_ruta_obj = j.objetivo
            print(f"{j.get_nombre()} ruta completa hacia nodo {j.objetivo}: {j.ultima_ruta}")

            # Avanzar un nodo por tick
            if len(j.ultima_ruta) > 1:
                # Tomar siguiente nodo
                idx_actual = j.ultima_ruta.index(actual)
                sig = j.ultima_ruta[idx_actual + 1]
            else:
                # Si ruta solo tiene un nodo (ya está en objetivo), tomar nuevo objetivo inmediatamente
                nuevo_obj = actual
                while nuevo_obj == actual:
                    nuevo_obj = random.randint(0, g.numvertices - 1)
                j.objetivo = nuevo_obj
                j.ultima_ruta = g.a_star_modificado(j, actual, j.objetivo, nodo_visitas)
                j.ultima_ruta_obj = j.objetivo
                print(f"{j.get_nombre()} ha llegado a su objetivo y elige nuevo objetivo: desde nodo {actual} a {j.objetivo}")
                print(f"{j.get_nombre()} ruta completa hacia nodo {j.objetivo}: {j.ultima_ruta}")
                if len(j.ultima_ruta) == 1:
                    sig = j.ultima_ruta[0]
                else:
                    sig = j.ultima_ruta[0] if j.ultima_ruta[0] != actual else j.ultima_ruta[1]
            print(f"A*: {j.get_nombre()} va al nodo {sig}")

        # --- Movimiento aleatorio para el resto ---
        # --- Movimiento aleatorio ---
        else:
            vecinos = g.get_neighbors(actual)
            sig = random.choice(vecinos) if vecinos else actual
            print(f"RANDOM: {j.get_nombre()} va al nodo {sig}")

        # ---- LIMITE DE 2 JUGADORES POR NODO ----
        jugadores_en_destino = 0
        for other in jugadores:
            if other is not j and other.get_nodos_recorridos() and other.get_nodos_recorridos()[-1] == sig:
                jugadores_en_destino += 1

        if jugadores_en_destino >= 2:
            print(f"⚠️ Nodo {sig} está LLENO (2 jugadores). {j.get_nombre()} no puede entrar.")
            sig = actual  # se queda

        # Si el jugador realmente cambia de nodo (sig distinto al actual) consideramos moved=True, para objetos.
        # Aquí definimos moved como True solamente si sig != actual.
        if sig != actual:
            moved = True

        # --- AHORA sí mover al jugador ---
        j.agregar_nodo_recorrido(sig)
        g.agregar_jugador(sig, j)

        # ===================================================
        # ----------- OBJETO ÚNICO POR MOVIMIENTO -----------
        # ===================================================
        if moved:
            # genera exactamente 1 objeto y lo aplica (usa tu Objeto.py)
            obj = Objeto()
            atributo = obj.atributo
            incremento = obj.incremento
            valor_actual = j.obtener_habilidad(atributo)
            nuevo_valor = valor_actual + incremento
            # Limitar a 99
            if nuevo_valor > 99:
                nuevo_valor = 99

            j.get_hashHabilidades().insert(atributo, nuevo_valor)
            j.actualizar_promedio()
            print(f"✨ {j.get_nombre()} encuentra {obj.nombre} en nodo {sig} y gana +{incremento} a {atributo}")
        else:
            # No se movió (bloqueado por nodo lleno), no recibe objeto
            print(f"{j.get_nombre()} no se movió, por eso no encuentra objeto.")
            pass
        # Evitar cuellos de botella
        # Actualizar contador de visitas
        visitas_actual = nodo_visitas.lookup(str(sig)) or 0
        nodo_visitas.insert(str(sig), visitas_actual + 1)
        # Actualizar congestión con valor real de visitas
        g.actualizar_congestion(sig, visitas_actual + 1)
   
    # ---------- Peleas entre jugadores en cada nodo ----------
    for nodo, lista_jugadores in g.jugadores_en_nodo.items():
        if len(lista_jugadores) >= 2:
            jugador1 = lista_jugadores[0]
            jugador2 = lista_jugadores[1]

            # --- Nueva regla: parejas no pelean y se curan ---
            if jugador2 == jugador1.get_pareja():
                print(f"💞 {jugador1.get_nombre()} y {jugador2.get_nombre()} son pareja, no pelean y se curan 20 de vida")
                for j in [jugador1, jugador2]:
                    j.cambiar_vida(5)
                    if j.get_vida() > 100:
                        j.cambiar_vida(100 - j.get_vida())
                continue

            print(f"\n⚔️ PELEA en nodo {nodo}: {jugador1.get_nombre()} VS {jugador2.get_nombre()}")

            count_j1 = 0
            count_j2 = 0
            for habilidad in Jugador.Jugador.habilidades_base:
                h1_val = jugador1.obtener_habilidad(habilidad)
                h2_val = jugador2.obtener_habilidad(habilidad)
                if h1_val > h2_val:
                    count_j1 += 1
                elif h2_val > h1_val:
                    count_j2 += 1

            if count_j1 >= 3:
                ganador, perdedor = jugador1, jugador2
            elif count_j2 >= 3:
                ganador, perdedor = jugador2, jugador1
            else:
                ganador = perdedor = None

            if ganador:
                print(f"🏆 Ganador: {ganador.get_nombre()} | Perdedor: {perdedor.get_nombre()} pierde 20 de vida")
                perdedor.cambiar_vida(-20)

                # Revisar si perdió toda la vida
                if perdedor.get_vida() <= 0:
                    print(f"💀 {perdedor.get_nombre()} ha muerto y desaparece del juego")
                    
                    # Mostrar mensaje flotante en pantalla
                    mostrar_mensaje_flotante(WIN, f"{perdedor.get_nombre()} eliminado", nodo)
    
                    # Remover del nodo actual
                    if nodo in g.jugadores_en_nodo and perdedor in g.jugadores_en_nodo[nodo]:
                        g.jugadores_en_nodo[nodo].remove(perdedor)
                    # Remover de la lista principal de jugadores
                    if perdedor in jugadores:
                        jugadores.remove(perdedor)

            else:
                print("🤝 Empate: Ningún jugador pierde vida")

    # ---------- Mostrar jugadores por nodo ----------
    print("\n======= ESTADO DE JUGADORES POR NODO =======")
    for nodo, lista_jugadores in g.jugadores_en_nodo.items():
        if lista_jugadores:
            print(f"\nNodo {nodo} ({len(lista_jugadores)} jugador(es)):")
            for jugador in lista_jugadores:
                print(f"Nombre: {jugador.get_nombre()}")
                print(f"Género: {jugador.get_genero()}")
                print(f"Vida: {jugador.get_vida()}")
                print(f"Nodos recorridos: {jugador.get_nodos_recorridos()}")
                print(f"Habilidad preferida: {jugador.get_habilidad_pref()}")
                print(f"Promedio de habilidades: {jugador.promedio_habilidades():.2f}")
                print("Habilidades individuales:")
                jugador.mostrar_habilidades()
                print("----------------------------")
    
# ---------- Loop principal ----------
clock = pygame.time.Clock()
mov_tiempo = 5
sig_mov = time.time() + mov_tiempo

run = True

while run:
    clock.tick(FPS)
    draw_graph()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = time.time()
    if now >= sig_mov:
        mover_jugadores()
        # ---- DETECTAR GANADOR ----
        jugadores_vivos = [j for j in jugadores if j.get_vida() > 0]

        # 1 jugador → ganador normal
        if len(jugadores_vivos) == 1:
            ganador = jugadores_vivos[0]

            print("\n==============================")
            print(f"¡{ganador.get_nombre()} es el GANADOR del juego!")
            print("==============================\n")

            mostrar_ganador_pantalla(WIN, ganador)
            run = False
            break

        # 2 jugadores → revisar si son pareja
        if len(jugadores_vivos) == 2:
            j1, j2 = jugadores_vivos

            if j1.get_pareja() == j2 and j2.get_pareja() == j1:
                print("\n💞 QUEDAN SOLO 2 Y SON PAREJA")

                ganador = max(jugadores_vivos, key=lambda x: x.promedio_habilidades())

                mostrar_ganador_pantalla(WIN, ganador, pareja=(j1, j2))
                run = False
                break
        sig_mov = now + mov_tiempo
        
pygame.quit()

# Mostrar estado final de los jugadores
print("\nEstado final de los jugadores:")
for j in jugadores:
    print(f"  -> {j.get_nombre()} terminó en el nodo: {j.get_nodos_recorridos()[-1]}")
