import random
from lib import pd, c


def select_personaje_random():
    """[Funcion para seleccionar a los personajes
        de forma aleatoria una vez que se haya terminado
        el temporizador]
        ........................
        IMPORTANTE hay que pasar la tabla completa con la modificaciones
        ........................

    Args:
        tabla_Usuarios ([dataFrame]): [data de personaje o characters]

    Returns:
        [dict]: [responde con el numero de personaje a elegir de forma random
                o nos dice que 'No hay disponibles']
    """
    characters = pd.read_csv(c.DIR_DATA+"Personajes.csv", index_col=0)
    players = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)

    get_NoDisponibles = characters.loc[characters.Disponible == 'No'].index
    get_Disponibles = characters.drop(get_NoDisponibles)

    Dont_habeID = players.iloc[players.SeleccionID.isnull().values]
    HabeID_pendientes = players.loc[players.StatusConfirmacion == 'pendiente']

    print('\n No han seleccionado nada \n',
          Dont_habeID.index, '\n',
          '\n Ya seleccionaron pero estan en pendientes \n',
          HabeID_pendientes.index)

    _lista_ = get_Disponibles.index.to_list()
    if len(get_Disponibles) > 0:

        if len(Dont_habeID) > 0:
            for i in range(len(Dont_habeID)):
                randomFile = random.randrange(len(_lista_))
                characters.at[_lista_[randomFile], 'Jugador_ID'] = Dont_habeID.index[i] # noqa
                characters.at[_lista_[randomFile], 'Disponible'] = 'No'
                characters.at[_lista_[randomFile], 'Confirmacion'] = 'Confirmado' # noqa
                _lista_.remove(_lista_[randomFile])

        if len(HabeID_pendientes) > 0:
            for x in range(len(HabeID_pendientes)):
                characters['Confirmacion'].loc[characters.Jugador_ID == HabeID_pendientes.index[x]] = 'Confirmado' # noqa

        characters.to_csv(c.DIR_DATA+"Personajes.csv")
