''' WaitMoments solo funciona para el modo multijugador'''

from lib import c
from lib import pd
from lib.usuario import randomEleccion
from lib.usuario import update_data
from lib.utilidades import handle_json
import time

"""[Todas estas funciones deben correr con un seguro
    en este caso todas estan inicializadas en base
    al cronometro su ciclo depende de la duracion
    de este o en de la condicion asignada para cada funcion]
............................................................
IMPORTANTE todas estaas funciones solo sirven para el modo MULTIJUGADOR
ya que en modo SOLO no tiene que caso esperar respuestas de los de mas
jugadores ya que en ese modo asi como nos constentan respondemos.
............................................................

"""


def wait_join_players():
    # Revizamos que ya se hayan unido todo los jugadores
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


def wait_respuestas_iguales():
    # Aqui comparamos las respuestas de los player
    # 1.- respuestas = iguales, diferents o ''
    return


def wait_respuestas_correctas():
    # Aqui comprobamos si fueron correctas o incorrectas
    # 1.- respuestaCorrecta = True/False
    return
