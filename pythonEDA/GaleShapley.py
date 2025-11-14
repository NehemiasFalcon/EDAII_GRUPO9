#Algoritmo similar al de Gale-Shapley donde SOLO las chicas proponen al inicio del juego
def gale_shapley(chicos, chicas): #Lo hecho en clase a Python menos chicaprefs
    n = len(chicas)
    chicas_libres = list(range(n))
    chicos_libres = [True] * len(chicos)
    sig_propuesta = [0] * n
    pareja_chico = [-1] * len(chicos)
    pareja_chica = [-1] * n

    # Preferencias de cada chica basadas en su habilidad preferida
    chicaprefs = [
        sorted(
            range(len(chicos)),
            key=lambda i: chicos[i].obtener_habilidad(chica.get_habilidad_pref()),
            reverse=True
        )
        for chica in chicas
    ]

    #Gale–Shapley (solo las chicas proponen)
    while chicas_libres:
        g = chicas_libres[-1]  # índice de la chica actual
        b = chicaprefs[g][sig_propuesta[g]]  # chico que la chica prefiere en este turno
        sig_propuesta[g] += 1

        if chicos_libres[b]:
            # El chico está libre, se forma una nueva pareja
            pareja_chica[g] = b
            pareja_chico[b] = g
            chicos_libres[b] = False
            chicas_libres.pop()

            #Validación visual
            print(f"❤  {chicas[g].get_nombre()} elige por primera vez a {chicos[b].get_nombre()} "
                f"(basado en su habilidad preferida: {chicas[g].get_habilidad_pref()})")

        else:
            #el chico ya tiene pareja, no cambia porque el chico no decide aun
            print(f"❌  {chicas[g].get_nombre()} intenta elegir a {chicos[b].get_nombre()}, "
                f"pero él ya está emparejado con {chicas[pareja_chico[b]].get_nombre()}.")
            # La chica intentará con su siguiente opción en el próximo ciclo
            continue

    return pareja_chico, pareja_chica