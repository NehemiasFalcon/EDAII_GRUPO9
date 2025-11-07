import pygame
from Grafo import Grafo
from Jugador import Jugador

# ---------- Configuración ----------
pygame.init()
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Grafo")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

FPS = 30
RADIUS = 20

# ---------- Crear grafo ---------- HECHO EN CLASE
numv = 5 #numero de vertices
g = Grafo(numv, es_dirigido=False) #cambiar a True si es dirigido
edge_list = ["0,1",
             "0,2",
             "1,2",
             "1,3",
             "3,4"]
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

# ---------- Jugador ----------
player = Jugador("M")
player.agregar_habilidad("fuerza", 10)  # Ejemplo de habilidad
player.agregar_habilidad("velocidad", 8)

current_node = 0
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
    # Mostrar vida y habilidades
    font = pygame.font.SysFont(None, 24)
    vida_text = font.render(f"Vida: {player.get_vida()}", True, BLACK)
    fuerza_text = font.render(f"Fuerza: {player.obtener_habilidad('fuerza')}", True, BLACK)
    WIN.blit(vida_text, (10, 10))
    WIN.blit(fuerza_text, (10, 30))    
    pygame.display.update()

# ---------- Loop principal ----------
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    draw_graph()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            neighbors = g.get_neighbors(current_node)
            moved = False
            # Movimiento con flechas (simple)
            if event.key == pygame.K_UP:
                for n in neighbors:
                    if node_positions[n][1] < node_positions[current_node][1]:
                        current_node = n
                        moved = True
                        break
            elif event.key == pygame.K_DOWN:
                for n in neighbors:
                    if node_positions[n][1] > node_positions[current_node][1]:
                        current_node = n
                        moved = True
                        break
            elif event.key == pygame.K_LEFT:
                for n in neighbors:
                    if node_positions[n][0] < node_positions[current_node][0]:
                        current_node = n
                        moved = True
                        break
            elif event.key == pygame.K_RIGHT:
                for n in neighbors:
                    if node_positions[n][0] > node_positions[current_node][0]:
                        current_node = n
                        moved = True
                        break
            if moved:
                player.agregar_nodo_recorrido(current_node)

pygame.quit()