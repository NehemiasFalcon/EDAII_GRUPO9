# Grafo.py

from ListaLados import ListaLados

class Grafo:
    def __init__(self, n=0, es_dirigido=False):
        self.numvertices = n
        self.dirigido = es_dirigido
        self.adjlist = [None for _ in range(n)]
    
    def agregarLado(self, x, y):
        curr = ListaLados(x, y)
        curr.next = self.adjlist[x]
        self.adjlist[x] = curr
        if not self.dirigido:
            curr = ListaLados(y, x)
            curr.next = self.adjlist[y]
            self.adjlist[y] = curr
    
    def mostrar_lados(self, x):
        curr = self.adjlist[x]
        while curr:
            print(f"({curr.x},{curr.y}) -> ", end="")
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
            x = int(parts[0])
            y = int(parts[1])
            self.agregarLado(x, y)
    
    #Sirve para obtener los nodos vecinos de un nodo dado,
    # lo cual es necesario para mover el personaje entre nodos en el juego.
    def get_neighbors(self, node):
        neighbors = []
        curr = self.adjlist[node]
        while curr:
            neighbors.append(curr.y)
            curr = curr.next
        return neighbors
