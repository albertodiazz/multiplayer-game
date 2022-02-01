import random
from lib.usuario import randomEleccion
from lib import c
from lib import pd


def check():
    Dont_habeID, HabeID_pendientes, get_Disponibles, characters = randomEleccion.read_data() # noqa
    players_sinConfirmar = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col= 0) # noqa

    for i in range(len(Dont_habeID)):
        #characters.at[Dont_habeID.index[i], 'TipoDeUsuario'] = 'user' # noqa
        players_sinConfirmar.at[Dont_habeID.index[i],'TipoDeUsuario'] = 'user' # noqa

    players_sinConfirmar.to_csv(c.DIR_DATA+'info_sesion.csv')
    print('<<<<<<<<<<<',
          'Se descarto a los usuarios que no eligieron',
          '>>>>>>>>>')
