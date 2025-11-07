# Gale-Shapley en Python sin deque

N = 5  # Número de chicos y chicas

# Preferencias de cada chica sobre los chicos (índices comienzan en 1)
chicaprefs = [
    [2, 4, 1, 3, 5],
    [1, 2, 3, 4, 5],
    [2, 4, 3, 1, 5], 
    [4, 1, 3, 2, 5], 
    [4, 1, 3, 2, 5] 
]

# Ranking de cada chico sobre las chicas
chicorango = [
    [1, 2, 3, 4, 5],
    [4, 3, 1, 2, 5],
    [1, 4, 3, 2, 5],
    [1, 3, 2, 4, 5],
    [1, 3, 2, 4, 5]
]


def GaleShapley(n, chicaprefs, chicorango):
    chicaslibres = list(range(n))  # lista como pila de chicas libres
    chicoslibres = [True] * n
    sigpropuesta = [0] * n
    parejaB = [-1] * n  # pareja de cada chico
    parejaG = [-1] * n  # pareja de cada chica

    # Algoritmo principal
    while chicaslibres:
        g = chicaslibres[-1]  # toma la última chica (top de la pila)
        b = chicaprefs[g][sigpropuesta[g]] - 1  # ajustar a índice 0
        sigpropuesta[g] += 1

        if chicoslibres[b]:
            parejaG[g] = b
            parejaB[b] = g
            chicoslibres[b] = False
            chicaslibres.pop()
        else:
            # Ver si el chico prefiere a la nueva chica sobre su pareja actual
            if chicorango[b][g] < chicorango[b][parejaB[b]]:
                chicaslibres.pop()
                chicaslibres.append(parejaB[b])
                parejaG[parejaB[b]] = -1
                parejaG[g] = b
                parejaB[b] = g

    return parejaB, parejaG


# ---------- Programa principal ----------
def main():
    parejaB, parejaG = GaleShapley(N, chicaprefs, chicorango)

    print("Resultados:")
    for i in range(N):
        print(f"Boy {i+1} → Girl {parejaB[i]+1}")
    for i in range(N):
        print(f"Girl {i+1} → Boy {parejaG[i]+1}")


if __name__ == "__main__":
    main()
