import pygame
from grafo import Grafo

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

# ---------- Crear grafo ----------
numv = 5
g = Grafo(numv, es_dirigido=False)
edge_list = ["0,1","0,2","1,2","1,3","3,4"]
g.read(edge_list)

# Posiciones de los nodos
node_positions = {
    0: (100, 200),
    1: (200, 100),
    2: (200, 300),
    3: (400, 200),
    4: (500, 200)
}

current_node = 0

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
            # Movimiento con flechas (simple)
            if event.key == pygame.K_UP:
                if any(node_positions[n][1] < node_positions[current_node][1] for n in neighbors):
                    for n in neighbors:
                        if node_positions[n][1] < node_positions[current_node][1]:
                            current_node = n
                            break
            elif event.key == pygame.K_DOWN:
                if any(node_positions[n][1] > node_positions[current_node][1] for n in neighbors):
                    for n in neighbors:
                        if node_positions[n][1] > node_positions[current_node][1]:
                            current_node = n
                            break
            elif event.key == pygame.K_LEFT:
                if any(node_positions[n][0] < node_positions[current_node][0] for n in neighbors):
                    for n in neighbors:
                        if node_positions[n][0] < node_positions[current_node][0]:
                            current_node = n
                            break
            elif event.key == pygame.K_RIGHT:
                if any(node_positions[n][0] > node_positions[current_node][0] for n in neighbors):
                    for n in neighbors:
                        if node_positions[n][0] > node_positions[current_node][0]:
                            current_node = n
                            break

pygame.quit()