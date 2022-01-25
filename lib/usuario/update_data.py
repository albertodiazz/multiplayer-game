from lib import pd
from lib import c
from lib import np


def update(_ID):
    # FIRE
    # 1.- Hay que encontrar los id que se ecneuntren ya seteados
    #     en la tabla de Personajes
    # 2.- Al saber cuales se repiten asignamos asi:
    #     player_sesion.SeleccionID: Personajes.ID
    #     player_sesion.StatusConfirmacion: Personajes.Confirmacion

    players_sesion = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
    personajes = pd.read_csv(c.DIR_DATA+'Personajes.csv', index_col=0)

    arrayA = np.array(players_sesion.index)
    arrayB = np.array(personajes.Jugador_ID.velues.values)
    comparasion = arrayA == arrayB

    if comparasion:
        print('Existe el ID en las dos bases de datos')

    # getSi = personT.loc[personT.Disponible == 'Si'].index
    # estaDisponible = np.any(np.array(getSi == ID_Person))


def append_niveles(data, ID, Columna, msg=None):
    if Columna == 'Nivel':
        if msg is not None:
            data.at[ID, Columna] += ',' + msg
            data.at[ID, Columna] = data.loc[ID, Columna].replace("null,", "")
    else:
        if msg is not None:
            data.at[ID, Columna] = msg
