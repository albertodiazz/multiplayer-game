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
    count_retos = 0

    count_retos = int(retos['reto']['wich']) + 1
    retos['reto']['wich'] = count_retos

    if count_retos > c.CANTIDAD_RETOS:
        retos['reto']['wich'] = 0
        with open(c.DIR_DATA+"to_front.json", 'w') as f:
            json.dump(retos, f)
            f.close()
    else:
        with open(c.DIR_DATA+"to_front.json", 'w') as f:
            json.dump(retos, f)
            f.close()

    open_json.close()
    return {'response': 'Ok add_reto_automaic'}


def add_confirmaciones_automatic(nivel_name):
    """[Esta funcion debebemos ocuparla para
        todos los niveles que necesiten confirmaciones
        por parte de todos los jugadores. Lo que hace es agregar
        de forma automatica al json los jugadores que le han dado
        ha cofirmar]
    ..................................................
    IMPORTANTE si agregas un nivel nuevo recuerda en seguir
    la estructura del json ['nivel_name']['confirmacion']
    ..................................................
    Args:
        nivel_name ([string]): [nombre del nivel en el json]
    """
    # Necesitamos saber de quien viene la confirmacion?
    # Considero que no ya que no aparece un mensaje especial por jugador
    open_json = open(c.DIR_DATA+"to_front.json")
    confirmaciones = json.load(open_json)
    count_confir = 0

    count_confir = int(confirmaciones['Momentos'][nivel_name]['confirmacion']) + 1 # noqa
    confirmaciones['Momentos'][nivel_name]['confirmacion'] = count_confir

    with open(c.DIR_DATA+"to_front.json", 'w') as f:
        json.dump(confirmaciones, f)
        f.close()
    open_json.close()


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
