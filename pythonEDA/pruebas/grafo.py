class ListaLados:
    def __init__(self, u=0, v=0):
        self.x = u
        self.y = v
        self.next = None

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
    
    def read(self, edge_list):
        for line in edge_list:
            if not line:
                continue
            parts = line.split(',')
            x = int(parts[0])
            y = int(parts[1])
            self.agregarLado(x, y)
    
    def get_neighbors(self, node):
        neighbors = []
        curr = self.adjlist[node]
        while curr:
            neighbors.append(curr.y)
            curr = curr.next
        return neighbors