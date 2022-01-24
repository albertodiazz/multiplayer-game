import random


def select_personaje_random(tabla_Usuarios):
    """[Funcion para seleccionar a los personajes
        de forma aleatoria una vez que se haya terminado
        el temporizador]
        ........................
        IMPORTANTE hay que pasar la tabla completa con la modificaciones
        ........................

    Args:
        tabla_Usuarios ([dataFrame]): [data de personaje]

    Returns:
        [dict]: [responde con el numero de personaje a elegir de forma random
                o nos dice que 'No hay disponibles']
    """
    personT = tabla_Usuarios
    get_NoDisponibles = personT.loc[personT.Disponible == 'No'].index
    get_Disponibles = personT.drop(get_NoDisponibles)
    if len(get_Disponibles) > 0:
        randomFile = random.randrange(len(get_Disponibles))
        return {'response': get_Disponibles.index[randomFile]}
    else:
        return {'response': 'No hay disponibles'}
