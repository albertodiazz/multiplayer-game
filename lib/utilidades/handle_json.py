from itertools import count
from lib import json
from lib import c
# PENDIENTE
# consume los datos
# Depues de notar cambios en la base de datos
# envialos


def add_levels_automatic():
    open_json = open(c.DIR_DATA+"to_front.json")
    levels = json.load(open_json)
    count_levels = None

    count_levels = int(levels['level']) + 1
    levels['level'] = count_levels

    if count_levels > c.CANTIDAD_NIVELES:
        levels['level'] = 0
        with open(c.DIR_DATA+"to_front.json", 'w') as f:
            json.dump(levels, f)
            f.close()
    else:
        with open(c.DIR_DATA+"to_front.json", 'w') as f:
            json.dump(levels, f)
            f.close()

    open_json.close()
    return {'response': 'Ok add_level_automaic'}


def add_retos_automatic():
    open_json = open(c.DIR_DATA+"to_front.json")
    retos = json.load(open_json)
    count_retos = None

    count_retos = int(retos['reto']) + 1
    retos['reto'] = count_retos

    if count_retos > c.CANTIDAD_NIVELES:
        retos['reto'] = 0
        with open(c.DIR_DATA+"to_front.json", 'w') as f:
            json.dump(retos, f)
            f.close()
    else:
        with open(c.DIR_DATA+"to_front.json", 'w') as f:
            json.dump(retos, f)
            f.close()

    open_json.close()
    return {'response': 'Ok add_reto_automaic'}


def add_levels_manual(msg, value):
    """[Funcion para agregar nivel de forma manual]

    Args:
        msg ([string]): [encontramos el atributo json]
        value ([string/int]): [depende del atributo seteamos el valor]
    """
    # Aqui seteamos en que momentos esta la base
    # de datos para no depender de los usuarios
    open_json = open(c.DIR_DATA+"to_front.json")
    to_front = json.load(open_json)
    to_front[msg] = value

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(to_front, f)
        f.close()
    open_json.close()

    return
