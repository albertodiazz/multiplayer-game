from lib import pd
from lib import c


def resetSesion():
    """[Funcion para resetear los csv]

    Returns:
        [dict]: [response: Data borrada]
    """
    lista_columnas = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
    lista_columnas = list(lista_columnas.columns)
    info_sesion = pd.DataFrame(columns=lista_columnas)
    info_sesion.index.name = 'ID'
    info_sesion.dropna(inplace=True)
    info_sesion.to_csv(c.DIR_DATA+'info_sesion.csv')

    # NOTA: al realizar cambios en los atributos tienes
    # que revizar que sean los mismo a los de la classe
    # del jugador.
    personajes = pd.read_csv(c.DIR_DATA+"Personajes.csv", index_col=0)
    personajes.drop(personajes.columns, axis=1, inplace=True)
    for i in range(1, len(personajes.index)+1):
        personajes.at[str(int(i)), 'Disponible'] = 'Si'
        personajes.at[str(int(i)), 'Jugador_ID'] = 'Nada'
        personajes.at[str(int(i)), 'Confirmacion'] = 'pendiente'
    personajes.dropna(inplace=True)

    personajes.to_csv(c.DIR_DATA+"Personajes.csv")

    return {'response': 'Data borrada'}
