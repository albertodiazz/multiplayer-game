import time

# NOTA = tal vez no sea necesario esta funcion global revizalo
# una vez que lo integres con socketIO
tiempoGlobal = {'minutos': 0, 'segundos': 0}


def convert(seconds):
    """[Funcion para convertir segundos a formato 00:00]

    Args:
        seconds ([int]): [esperamos el time_in_seconds de cronometro]

    Returns:
        [array]: [regresamos dos strings]
    """
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d" % (minutes), "%02d" % (seconds)


def comparacionTiempos(tiempo, minutos_meta, segundos_meta, emit=None):
    """[Funcion en donde restamos los valores del tiempo meta]
        .......................
        IMPORTANTE aqui usamos la variable global
        .......................
    Args:
        tiempo ([dict]): [minutos y segundos de la funcion cronometro]
        minutos_meta ([string]): [esperamos string de la funcion convert]
        segundos_meta ([string]): [esperamos string de la funcion convert]
        emit ([socketIO]): [Eso hay que agragarlo cundo lo setemos a socket io]
    """
    global tiempoGlobal
    minutos = "%02d" % (tiempo['minutos'])
    segundos = "%02d" % (tiempo['segundos'])
    if int(segundos_meta) != 0:
        tiempoGlobal['minutos'] = "%02d" % (int(minutos_meta)-(int(minutos)))
        tiempoGlobal['segundos'] = "%02d" % (int(segundos_meta)-int(segundos))
        # PENDIENTE = agregar al queue
        print(tiempoGlobal)
    elif int(segundos_meta) == 0:
        tiempoGlobal['minutos'] = "%02d" % (int(minutos_meta)-(int(minutos)))
        tiempoGlobal['segundos'] = "%02d" % (int(59)-int(segundos))
        print(tiempoGlobal)


def temporizador(time_in_seconds):
    """[Funcion de temporizador]
        ................................
        Funciona para restar el tiempo, sera utilizada como temporizador en
        un juego multijugador. Donde al terminar el tiempo se ejecutara una
        accion en el juego.
        ................................
    Args:
        time_in_seconds ([int]): [hay que meter los minutos en conversion a
                                    segundos tipo 120 para 2 minutos]
    Returns:
        [array]: [regresamos dos strings]
    """
    minutos_meta, segundos_meta = convert(time_in_seconds)
    count = 0
    tiempo = {'minutos': 0, 'segundos': -1}
    seguro = 0
    while True:
        tiempo['segundos'] += 1
        if tiempo['segundos'] > 59:
            tiempo['segundos'] = 0
            tiempo['minutos'] += 1
        elif int(segundos_meta) > seguro:
            if count > int(segundos_meta):
                segundos_meta = 59
                tiempo['segundos'] = 0
                tiempo['minutos'] += 1
                seguro = 129128098
        comparacionTiempos(tiempo, minutos_meta, segundos_meta)
        # print("%02d:%02d" % (tiempo['minutos'], tiempo['segundos']))
        time.sleep(1)
        count += 1
        if count > time_in_seconds:
            return True
