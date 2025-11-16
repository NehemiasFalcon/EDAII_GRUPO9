import random

# Objeto almacenará lo que aparezca cuando se muevan los jugadores y lleguen a un nodo
class Objeto:
    objetos_disponibles = {
        "Fuerza": "Guantes de fuerza",
        "Velocidad": "Botas veloces",
        "Inteligencia": "Libro de sabiduría",
        "Carisma": "Collar carismático",
        "Condicion_Fisica": "Proteina"
    }

    def __init__(self):
        # Elegir aleatoriamente una habilidad que se usará para modificarlo durante un movimiento
        self.atributo = random.choice(list(Objeto.objetos_disponibles.keys()))
        self.nombre = Objeto.objetos_disponibles[self.atributo]
        # Azar establece si se bajará o subirá la habilidad que se escogió previamente
        azar = random.randint(1,2)

        if azar == 1:
            # Incremento aleatorio entre 1 y 2
            self.incremento = random.randint(1,2)
        else:
            # Disminución aleatorio entre -1 y -2
            self.incremento = random.randint(-2,-1)