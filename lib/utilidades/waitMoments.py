''' WaitMoments solo funciona para el modo multijugador'''

from lib import c
from lib import pd
from lib.usuario import randomEleccion
from lib.usuario import update_data
from lib.utilidades import handle_json
from lib.usuario import numeroJugadores
import time

"""[Todas estas funciones deben correr con un seguro
    en este caso todas estan inicializadas en base
    al cronometro su ciclo depende de la duracion
    de este o en de la condicion asignada para cada funcion]
............................................................
IMPORTANTE todas estaas funciones solo sirven para el modo MULTIJUGADOR
ya que en modo SOLO no tiene que caso esperar respuestas de los de mas
jugadores ya que en ese modo asi como nos constentan respondemos.

- Otro punto importante es entender que todos los cronometros empiezan apartir
de que existe interaccion con algun boton. Ya que ahi es donde tomamos
iniciativa de seguir con la actividad de juego antes de eso si nadie presiona,
quiere decir que hay inactividad por lo tanto entra en juego el cronometro del
Cliente que es quien decide que nos regresemos al prinicpio de la aplicacion
............................................................

"""


def wait_join_players():
    # Esperamos a los usuarios que se unen a la sesion de player
    # en base a c.MAX_JUGADORES
    while True:
        if c.CRONOMETRO == 'PLAY':
            player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
            clean = player.TipoDeUsuario.dropna()
            print('Wait confirmacoin unirse')
            if len(clean) > 0:
                joinAlll = clean.loc[clean.values == 'player']
                # Lo revizamos cada segundo un vez que fue llamado
                time.sleep(1)
                if len(joinAlll) >= c.MAX_JUGADORES:
                    print('<<<<<<<<<<<<<<<<<<<<<<<<',
                          'Se unieron todos los jugadores'
                          '>>>>>>>>>>>>>>>>>>>>>>>>>')
                    # GLOBAL
                    c.CRONOMETRO = 'STOP'
                    # Cambiamos de nivel?
                    ##############################
                    # Cambiamos de nivel
                    handle_json.add_levels_manual('level', 2)
                    ##############################
                    break
        elif c.CRONOMETRO == 'STOP':
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                  'Cronometro Stop from Wait Players',
                  '>>>>>>>>>>>>>>>>>>>>>>>>>')
            ##############################
            # Cambiamos de nivel
            handle_json.add_levels_manual('level', 2)
            ##############################
            break


def wait_confirmacion_characters():
    # Revizamos que ya hayan confirmado todos los jugadores
    # su personaje si no se los elegimos de forma random
    while True:
        if c.CRONOMETRO == 'PLAY':
            player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
            clean = player.StatusConfirmacion.dropna()
            print('Wait confirmacion characters')
            if len(clean) > 0:
                joinAlll = clean.loc[clean.values == 'player']
                # Lo revizamos cada segundo un vez que fue llamado
                time.sleep(1)
                if len(joinAlll) >= c.MAX_JUGADORES:
                    print('<<<<<<<<<<<<<<<<<<<<<<<<',
                          'Confirmaron todos los jugadores'
                          '>>>>>>>>>>>>>>>>>>>>>>>>>')
                    # Cambiamos de nivel?
                    randomEleccion.select_personaje_random()
                    update_data.update_info_jugador()
                    # GLOBAL
                    c.CRONOMETRO = 'STOP'
                    ##############################
                    # Cambiamos de nivel
                    handle_json.add_levels_manual('level', 3)
                    ##############################
                    break
        elif c.CRONOMETRO == 'STOP':
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                  'Cronometro Stop from Wait Players',
                  '>>>>>>>>>>>>>>>>>>>>>>>>>')
            randomEleccion.select_personaje_random()
            update_data.update_info_jugador()
            ###################################
            # Cambiamos de nivel
            handle_json.add_levels_manual('level', 3)
            ###################################
            break


def wait_confirmaciones_json(nivel_name):
    # FIRE
    # Aqui comprobamos las confirmaciones de los usuarios
    # desde el json, recuerda que la diferencia entre esta funcion
    # y las anteriores es de que aqui no sabes quien confirmo
    # En vez de ocupar c.MAX_JUGADORES necesitas num_jugadores
    # ya que son el numero de jugadores por sesion
    handle_json.add_confirmaciones_automatic(nivel_name)
    players_sesion = numeroJugadores.get_players()
    num_players = len(players_sesion.index)

    return
