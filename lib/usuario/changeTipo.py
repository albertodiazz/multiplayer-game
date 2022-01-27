from lib import pd
from lib import c


def change_to_player(_ID_):
    # Aqui cambiamos el tipo de usuario a player
    player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)

    try:
        if player.loc[_ID_].TipoDeUsuario == 'user':
            player.at[_ID_, 'TipoDeUsuario'] = 'player'
            player.to_csv(c.DIR_DATA+'info_sesion.csv')
            return {'response': 'Se cambio a player'}
        else:
            return {'response': 'Ya es un player'}
    except KeyError:
        print('El usuario no existe:')
        pass
