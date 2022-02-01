from lib import numeroJugadores
from lib import c


def update():
    numJ = numeroJugadores.get_players()

    if len(numJ.index) < 2:
        c.MODO_DE_JUEGO = 'Solo'
        print('<<<<<<<<<<<<<<<<<<<<<<<<',
              ' Solo ',
              '>>>>>>>>>>>>>>>>>>>>>>>>')
    else:
        c.MODO_DE_JUEGO = 'Multijugador'
        print('<<<<<<<<<<<<<<<<<<<<<<<<',
              ' Multijugador ',
              '>>>>>>>>>>>>>>>>>>>>>>>>')
