from lib import Players
from lib import pd
from lib import np
from lib import c
from lib.usuario import checkRepeatID

allData = pd.DataFrame([])
players = []


def create_player(ID):
    """ Funcion para crear personajes
    ...............
    -[No hay un limite de personajes]
    -safeID ([def]) = [arreglamos ID repetidos]
    ...............
    Args:
        ID ([string]): [Id del Jugador en sesion]

    Returns:
        [players ([dataFrame]),allData ([array]), numJugadores ([int])]: [
            .......................................
            -players = dataFrame,
            -allData = atributos de la clase,
            -numJugadores = numero de jugadores
            .......................................
            ]
    """
    global players
    global allData
    players.append(Players.Jugadores())
    numJugadores = len(players)
    players[len(players)-1].newPlayer(ID)
    allData = allData.append([players[len(players)-1].Datos])
    try:
        allData, numFix = checkRepeatID.safeID(ID, allData)
        numJugadores = numFix
        return allData, players, numJugadores
    except checkRepeatID.no_hay_repetidos:
        print('Todo bien')
        # BUG=  El numJugadores esta contando todos los que se unen
        # y no esta depurando los errores
        return allData, players, numJugadores


def seleccionDePersonaje(ID, ID_Person, data, confirmacion=False):
    """Funcion para seleccion personaje

    Args:
        ID ([string]): [ID del Jugador]
        ID_Person ([int]): [ID del personaje ha elegir]
        data ([dataFrame]): [Tabla de datos de Usuarios]
        confirmacion (bool, optional): [
            1.- Solo debe ser enviada una vez].
                                                Defaults to False.

    Returns:
        [type]: [description]
    """
    personT = pd.read_csv(c.DIR_DATA+"Personajes.csv", index_col=0)
    getSi = personT.loc[personT.Disponible == 'Si'].index
    estaDisponible = np.any(np.array(getSi == ID_Person))
    habiaElegido = personT.loc[personT.Jugador_ID == ID].index
    # FIRE= agregar cronometro y funcion de random creo que esto ira
    # de forma async para implementar esta funcion ya tienes que empezar
    # a implementar esta funcion en socket io para no mezclar las funciones
    # dentro de otras funciones y tener mejor control sobre las cosas
    confirmados = personT.loc[personT['Confirmacion'] == 'Confirmado']
    confirResultado = np.any(np.array(confirmados.Jugador_ID == ID))
    if confirResultado:
        return {'response': 'Ya no puedes elegir, haz confirmado un personaje'}
    else:
        if len(data.index[data.index == ID]) > 0:
            if confirmacion:
                if len(habiaElegido) > 0:
                    if personT.loc[personT.Jugador_ID == ID].index[0] == ID_Person: # noqa
                        personT.at[ID_Person, 'Confirmacion'] = 'Confirmado'
                        personT.to_csv(c.DIR_DATA + "Personajes.csv")
                        print({'reponse': 'Confirmado'})
                    else:
                        return {'response': 'Este personaje no es tuyo'}
                else:
                    return {'response': 'Elige primero el personaje'}
            elif estaDisponible:
                if len(habiaElegido) > 0:
                    select = personT.loc[personT.Jugador_ID == ID].index[0]
                    personT.at[select, 'Jugador_ID'] = 'Nada'
                    personT.at[select, 'Disponible'] = 'Si'
                # Ojo aqui no pongo condicional solo utilizo
                # la logica de ejecucion de Python
                personT.at[ID_Person, 'Jugador_ID'] = ID
                personT.at[ID_Person, 'Disponible'] = 'No'
                personT.to_csv(c.DIR_DATA+"Personajes.csv")
                # Aqui marcamos la verificacion una vez que nos confirme
                return {'response': 'Se modifico la tabla de Personajes'}
            else:
                print(estaDisponible)
                return {'response': 'No disponible'}
        else:
            return {'response': 'No existe el ID del Jugador'}


def resetSesion(data):
    """[Funcion para borrar toda la data por sesion]

    Args:
        data ([dataFrame]): [tabla de Personajes.csv]

    Returns:
        [type]: [description]
    """
    data.drop(data.index, inplace=True)
    personT = pd.read_csv(c.DIR_DATA+"Personajes.csv", index_col=0)
    personT.drop(personT.columns, axis=1, inplace=True)
    for i in range(1, len(personT.index)+1):
        personT.at[str(int(i)), 'Disponible'] = 'Si'
        personT.at[str(int(i)), 'Jugador_ID'] = 'Nada'
        personT.at[str(int(i)), 'Confirmacion'] = 'pendiente'
    personT.dropna(inplace=True)
    personT.to_csv(c.DIR_DATA+"Personajes.csv")
    # PENDIENTE
    # [Hay que resetear nuestros arrays por Sesion]
    return {'response': 'Data borrada'}
