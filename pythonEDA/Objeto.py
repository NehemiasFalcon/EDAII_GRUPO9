import random

class Objeto:
    objetos_disponibles = {
        "Fuerza": "Guantes de fuerza",
        "Velocidad": "Botas veloces",
        "Inteligencia": "Libro de sabiduría",
        "Carisma": "Collar carismático",
        "Condicion_Fisica": "Proteina"
    }

    def __init__(self):
        # Elegir aleatoriamente un atributo
        self.atributo = random.choice(list(Objeto.objetos_disponibles.keys()))
        self.nombre = Objeto.objetos_disponibles[self.atributo]
        # Incremento aleatorio entre 1 y 2
        azar = random.randint(1,2)
        if azar == 1:
            self.incremento = random.randint(1,2)
        else:
            self.incremento = random.randint(-2,-1)