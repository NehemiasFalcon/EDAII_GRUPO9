from Jugador import Jugador, Jugadores
from GaleShapley import gale_shapley

jugador1 = Jugador("Nehemias", "Masculino")
jugador2 = Jugador("Mariel", "Femenino")
jugador3 = Jugador("Marisol", "Femenino")
jugador4 = Jugador("Sebastian", "Masculino")
jugador5 = Jugador("Melissa", "Femenino")
jugador6 = Jugador("Candiotti", "Masculino")
jugador7 = Jugador("Guti", "Masculino")
jugador8 = Jugador("Priscila", "Femenino")
jugador9 = Jugador("Ariana", "Femenino")
jugador10 = Jugador("Pekka", "Masculino")

JugadoresHombres = []
JugadoresMujeres = []

# Agregar a las listas dependiendo de su género
for jugador in Jugadores:
    if (jugador.get_genero() == "Masculino"):
        JugadoresHombres.append(jugador)
    else:
        JugadoresMujeres.append(jugador)

# Imprimir las habilidades con sus puntajes de los hombres
for hombre in JugadoresHombres:
    hombre.get_hashHabilidades().imprimir(hombre.get_nombre())

parejaB, parejaG = gale_shapley(JugadoresHombres, JugadoresMujeres)

print("\n---RESULTADO INICIAL (GaleShapley, chicas deciden)---")
for i, chico in enumerate(JugadoresHombres):
    if parejaB[i] != -1:
        chica = JugadoresMujeres[parejaB[i]]
        chico.set_pareja(chica)
        chica.set_pareja(chico)
        print(f"{chico.get_nombre()}  ❤   {chica.get_nombre()}")

# Validar que todo funcione con respecto a matrimonio: 
for jugador in Jugadores:
    print(f"La pareja de {jugador.get_nombre()} es {jugador.get_pareja()}")






# CODIGO QUE SE USARÁ PARA SABER SI OCURRE UN CAMBIO DE PAREJA CUANDO SE ENCUENTRAN DOS PAREJAS.
#Una vez iniciado el juego, recibe dos CHICOS, detecta automáticamente sus parejas, evalúa si hay mejora mutua y realiza el intercambio si conviene.
def intercambio_mutuo_de_parejas(chico1, chico2):
    # Obtener las parejas actuales de ambos chicos
    chica1 = chico1.get_pareja()
    chica2 = chico2.get_pareja()

    # Validación de que ambos tengan pareja
    if chica1 is None or chica2 is None:
        print("❌ No se puede intercambiar: uno de los chicos no tiene pareja.")
        return False

    print("\n🔍 Evaluando posible intercambio:")
    print(f"• {chico1.get_nombre()} ❤ {chica1.get_nombre()}")
    print(f"• {chico2.get_nombre()} ❤ {chica2.get_nombre()}")

    #Habilidades preferidas por cada chico
    pref1 = chico1.get_habilidad_pref()
    pref2 = chico2.get_habilidad_pref()

    #Valores actuales según su preferencia
    chico1_actual = chica1.obtener_habilidad(pref1)
    chico2_actual = chica2.obtener_habilidad(pref2)

    #Aca se almacenan los valores de las habilidades si intercambian
    chico1_con_chica2 = chica2.obtener_habilidad(pref1)
    chico2_con_chica1 = chica1.obtener_habilidad(pref2)

    print(f"\nComparación de mejoras:")
    print(f"- {chico1.get_nombre()}: actual {chico1_actual}, con {chica2.get_nombre()} {chico1_con_chica2}")
    print(f"- {chico2.get_nombre()}: actual {chico2_actual}, con {chica1.get_nombre()} {chico2_con_chica1}")

    #Ver si ambos mejoran
    if chico1_con_chica2 > chico1_actual and chico2_con_chica1 > chico2_actual:

        # --- Realizar intercambio ---
        chico1.set_pareja(chica2)
        chica2.set_pareja(chico1)

        chico2.set_pareja(chica1)
        chica1.set_pareja(chico2)

        print("\n✅ INTERCAMBIO REALIZADO:")
        print(f"   {chico1.get_nombre()} ❤ {chica2.get_nombre()}")
        print(f"   {chico2.get_nombre()} ❤ {chica1.get_nombre()}")
        return True

    print("\n❌ No se realizó el intercambio: no beneficia a ambos.")
    return False