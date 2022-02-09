from lib import pd
from lib import c


def resetSesion():
    """[Funcion para resetear el csv de Personajes]

    Returns:
        [dict]: [response: Data borrada]
    """
    # NOTA: al realizar cambios en los atributos de Personajes.csv tienes
    # que revizar que sean los mismo a los de la classe
    # del jugador.
    info_sesion = pd.read_csv(c.DIR_DATA+"info_sesion.csv", index_col=0)
    info_sesion.SeleccionID = ''
    info_sesion.StatusConfirmacion = ''
    info_sesion.to_csv(c.DIR_DATA+"info_sesion.csv")

    personajes = pd.read_csv(c.DIR_DATA+"Personajes.csv", index_col=0)
    personajes.drop(personajes.columns, axis=1, inplace=True)
    for i in range(1, len(personajes.index)+1):
        personajes.at[str(int(i)), 'Disponible'] = 'Si'
        personajes.at[str(int(i)), 'Jugador_ID'] = 'Nada'
        personajes.at[str(int(i)), 'Confirmacion'] = 'pendiente'
    personajes.dropna(inplace=True)

    personajes.to_csv(c.DIR_DATA+"Personajes.csv")

    return {'response': 'Data borrada'}
