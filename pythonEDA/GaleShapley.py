from Jugador import Jugador
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

     # Ranking de chicos sobre chicas (para saber si prefieren nueva propuesta)
    # Aquí usamos también la habilidad preferida del chico
    chico_ranking = [
        {chica: rank for rank, chica in enumerate(
            sorted(
                range(n),
                key=lambda c: chicas[c].obtener_habilidad(chico.get_habilidad_pref()),
                reverse=True
            )
        )}
        for chico in chicos
    ]

    # Inicializar chicos como libres
    chicos_libres = [True] * len(chicos)

    #Gale–Shapley (solo las chicas proponen)
    while chicas_libres:
        g = chicas_libres[-1]  # índice de la chica actual
        b = chicaprefs[g][sig_propuesta[g]]  # chico que la chica prefiere en este turno
        sig_propuesta[g] += 1
        print(f"💌 {chicas[g].get_nombre()} propone a {chicos[b].get_nombre()} "
              f"(basado en su habilidad preferida: {chicas[g].get_habilidad_pref()})")
        
        if chicos_libres[b]:
            # El chico está libre, se forma una nueva pareja
            pareja_chica[g] = b
            pareja_chico[b] = g
            chicos_libres[b] = False
            chicas_libres.pop()

            #Validación visual
            print(f"✅ {chicos[b].get_nombre()} acepta y se empareja con {chicas[g].get_nombre()}")

        else:
             # Chico ya tiene pareja: verificar si prefiere a nueva chica
            g_actual = pareja_chico[b]
            if chico_ranking[b][g] < chico_ranking[b][g_actual]:
                # Prefiere a la nueva chica: divorcio
                pareja_chica[g] = b
                pareja_chico[b] = g
                pareja_chica[g_actual] = -1
                chicas_libres.pop()
                chicas_libres.append(g_actual)  # antigua pareja vuelve a estar libre
                print(f"💔 {chicos[b].get_nombre()} deja a {chicas[g_actual].get_nombre()} y se empareja con {chicas[g].get_nombre()}")
            else:
                # Chico mantiene su pareja actual
                print(f"❌ {chicos[b].get_nombre()} rechaza a {chicas[g].get_nombre()} y sigue con {chicas[g_actual].get_nombre()}")
                continue

    # Guardar parejas como atributo en los objetos Jugador
    for g_idx, b_idx in enumerate(pareja_chica):
        if b_idx != -1:
            chicas[g_idx].set_pareja(chicos[b_idx])
            chicos[b_idx].set_pareja(chicas[g_idx])

    print("\n💖 Parejas finales:")
    for g_idx, b_idx in enumerate(pareja_chica):
        if b_idx != -1:
            print(f"{chicas[g_idx].get_nombre()} 💑 {chicos[b_idx].get_nombre()}")

    return pareja_chico, pareja_chica