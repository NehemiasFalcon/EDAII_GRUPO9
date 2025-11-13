import pygame
import Jugador
import random
import time
import math
from Grafo import Grafo


# ---------- Configuración ----------
pygame.init()
WIDTH, HEIGHT = 600, 400
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
numv = 5 #numero de vertices
g = Grafo(numv, es_dirigido=False) #cambiar a True si es dirigido
edge_list = ["0,1",
             "0,2",
             "1,2",
             "1,3",
             "3,4",
             "2,4"]
g.read(edge_list)
g.imprimir()

# Posiciones de los nodos
node_positions = {
    0: (100, 200),
    1: (200, 100),
    2: (200, 300),
    3: (400, 200),
    4: (500, 200)
}

# ---------- Crear jugadores ----------
jugadores = []
hombres = []
mujeres = []
for i in range(1): 
    h = Jugador.Jugador(f"Hombre {i+1}", "Masculino")
    m = Jugador.Jugador(f"Mujer {i+1}", "Femenino")
    hombres.append(h)
    mujeres.append(m)
    jugadores.append(h)
    jugadores.append(m)

current_node = 0
for player in jugadores:
    player.agregar_nodo_recorrido(current_node)

# ---------- Funciones ----------
def draw_graph():
    WIN.fill(WHITE)
    # Dibujar aristas
    for i in range(numv):
        curr = g.adjlist[i]
        while curr:
            start = node_positions[i]
            end = node_positions[curr.y]
            pygame.draw.line(WIN, BLACK, start, end, 2)
            curr = curr.next
    # Dibujar nodos
    for node, pos in node_positions.items():
        color = RED if node == current_node else BLUE
        pygame.draw.circle(WIN, color, pos, RADIUS)
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(node), True, BLACK)
        WIN.blit(img, (pos[0]-8, pos[1]-10))
    
    # Dibujar jugadores
    font = pygame.font.SysFont(None, 24)
    for j in jugadores:
        pos = node_positions[j.get_nodos_recorridos()[-1]]
        pygame.draw.circle(WIN, COLORS[i % len(COLORS)], pos, RADIUS // 2)
        text = font.render(j.get_nombre(), True, BLACK)
        WIN.blit(text, (pos[0] - 25, pos[1] - 30))

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
        start_x = int(cx - (spacing * (count - 1)) / 2)
        for k, (idx, j) in enumerate(listaJugadores):
            px = start_x + k * spacing
            py = cy
            color = COLORS[idx % len(COLORS)]
            pygame.draw.circle(WIN, color, (px, py), player_radius)

    pygame.display.update()

def mover_jugadores():
    for j in jugadores:
        actual = j.get_nodos_recorridos()[-1]
        vecinos = g.get_neighbors(actual)
        if vecinos:
            sig = random.choice(vecinos)
            j.agregar_nodo_recorrido(sig)

# ---------- Loop principal ----------
clock = pygame.time.Clock()
mov_tiempo = 2
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
        sig_mov = now + mov_tiempo
        
pygame.quit()