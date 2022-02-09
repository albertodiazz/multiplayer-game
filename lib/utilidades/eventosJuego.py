import re


def reto_nivel_check(levelFromFront):
    """[Obtenemos la posicion anterior o posterior del nivel]

    Args:
        levelFromFront ([type]): [description]

    Returns:
        [dict]: ['atras', 'adelante']
    """
    enQueNivelEstamos = levelFromFront
    temp = re.compile("([a-zA-Z]+)([0-9]+)")
    filterString = temp.match(enQueNivelEstamos).groups()

    nivelAdelante = filterString[0] + str(int(filterString[1]) + 1)

    if int(filterString[1]) > 0:
        nivelAtras = filterString[0] + str(int(filterString[1]) - 1)
    else:
        nivelAtras = filterString[0] + '0'

    posiciones = {
        'atras': nivelAtras,
        'adelante': nivelAdelante
    }
    return posiciones
