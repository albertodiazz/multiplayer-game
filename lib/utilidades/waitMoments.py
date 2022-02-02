''' WaitMoments solo funciona para el modo multijugador'''

import json
import string
from lib import c
from lib import pd
from lib.utilidades import whoLeavesCharacters
from lib.usuario import automaticElection
from lib.usuario import update_data
from lib.utilidades import handle_json
from lib.usuario import numeroJugadores
from lib import np
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

[ARGS]
    wichLevel [int] : Todas las funciones tiene una variable de ese tipo, ahi
                      es donde seteamos a que nivel apunta nuestra funcion
"""


def wait_join_players(whichLevel=2):
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
                    handle_json.add_levels_manual('level', whichLevel)
                    ##############################
                    break
        elif c.CRONOMETRO == 'STOP':
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                  'Cronometro Stop from Wait Players',
                  '>>>>>>>>>>>>>>>>>>>>>>>>>')
            ##############################
            # Cambiamos de nivel
            handle_json.add_levels_manual('level', whichLevel)
            ##############################
            break


def wait_confirmacion_characters(whichLevel=3):
    # Revizamos que ya hayan confirmado todos los jugadores
    # su personaje si no se los elegimos de forma random

    while True:
        if c.CRONOMETRO == 'PLAY':
            # player = pd.read_csv(c.DIR_DATA+'info_sesion.csv', index_col=0)
            # clean = player.StatusConfirmacion.dropna()
            numPlayers = numeroJugadores.get_players()
            print('Wait confirmacion characters')
            if len(numPlayers) > 0:
                joinAlll = numPlayers.loc[numPlayers.StatusConfirmacion == 'Confirmado'] # noqa
                # Lo revizamos cada segundo un vez que fue llamado
                print(joinAlll, len(joinAlll), c.MAX_JUGADORES)
                time.sleep(1)
                if len(joinAlll) >= len(numPlayers):
                    print('<<<<<<<<<<<<<<<<<<<<<<<<',
                          'Confirmaron todos los jugadores'
                          '>>>>>>>>>>>>>>>>>>>>>>>>>')
                    # Cambiamos de nivel?
                    # randomEleccion.confirm_characters()
                    # update_data.update_info_jugador()
                    # GLOBAL
                    c.CRONOMETRO = 'STOP'
                    ##############################
                    # Cambiamos de nivel
                    handle_json.add_levels_manual('level', whichLevel)
                    ##############################
                    break
        elif c.CRONOMETRO == 'STOP':
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                  'Cronometro Stop from Wait Players',
                  '>>>>>>>>>>>>>>>>>>>>>>>>>')
            whoLeavesCharacters.check()
            automaticElection.confirm_characters()
            update_data.update_info_jugador()
            ###################################
            # Cambiamos de nivel
            handle_json.add_levels_manual('level', whichLevel)
            ###################################
            break


def wait_comparasion_respuestas(reto, respuesta_player):
    # PENDIENTE
    '''
        Esta funcion es para las respuestas, aqui es donde comparamos que los
        usuarios contesten igual y despues de haber constetado igual
        comparamos si acertaron con la respuesta correcta o no
    '''
    open_json = open(c.DIR_DATA + "respuestas.json")
    data_json = json.load(open_json)
    # Player por sesion
    players_sesion = numeroJugadores.get_players()
    num_players = len(players_sesion.index)

    # 1.- Primer momento donde nos sumamos sus respuestas
    # correctas o incorrectas
    if data_json[reto].lower() == respuesta_player.lower():
        '''
        ........................................
        RESPUESTAS CORRECTA ADD
        .......................................
        '''
        print('<<<<<< Correcto >>>>>>>>>')
        add = int(data_json['confirmaciones']['correctas']) + 1
        data_json['confirmaciones']['correctas'] = add
        with open(c.DIR_DATA+"respuestas.json", 'w') as f:
            json.dump(data_json, f)
            f.close()
    else:
        '''
        ........................................
        RESPUESTAS INCORRECTA ADD
        .......................................
        '''
        print('<<<<<<<< Incorrecto >>>>>>>>')
        add = int(data_json['confirmaciones']['incorrectas']) + 1
        data_json['confirmaciones']['incorrectas'] = add
        with open(c.DIR_DATA+"respuestas.json", 'w') as f:
            json.dump(data_json, f)
            f.close()

    # 2.- Una vez que nos llegue la respuesta del ultimo usuario
    # comparamos si todos consteron igual
    getNum_confirm = data_json['confirmaciones']['correctas'] + data_json['confirmaciones']['incorrectas'] # noqa
    if getNum_confirm >= num_players:
        # 3.- Solo si contestaron todos igual mandamos a decir si fue
        # una decision correcta o incorrecta
        if data_json['confirmaciones']['correctas'] == num_players:
            print('Todos estan bien')
            # PENDIENTE [antes de resetear contestar a front]
            # Reseteamos nuestro Json para el siguiente evento
            data_json['confirmaciones']['incorrectas'] = 0
            data_json['confirmaciones']['correctas'] = 0
            with open(c.DIR_DATA+"respuestas.json", 'w') as f:
                json.dump(data_json, f)
                f.close()
        elif data_json['confirmaciones']['incorrectas'] == num_players:
            print('Todos estan mal')
            # PENDIENTE [antes de resetear contestar a front]
            # Reseteamos nuestro Json para el siguiente evento
            data_json['confirmaciones']['incorrectas'] = 0
            data_json['confirmaciones']['correctas'] = 0
            with open(c.DIR_DATA+"respuestas.json", 'w') as f:
                json.dump(data_json, f)
                f.close()
        else:
            print('Alguien no contesto igual')
            # PENDIENTE [antes de resetear contestar a front]
            # Reseteamos nuestro Json para el siguiente evento
            data_json['confirmaciones']['incorrectas'] = 0
            data_json['confirmaciones']['correctas'] = 0
            with open(c.DIR_DATA+"respuestas.json", 'w') as f:
                json.dump(data_json, f)
                f.close()

    open_json.close()
    return


def wait_confirmaciones_json(nivel_name, whichLevel=3):
    """
    Aqui comprobamos las confirmaciones de los usuarios
    desde el json y una vez que los participantes por sesion
    acepten, avanzamos al siguiente nivel o reto.

    Args:
        nivel_name ([string]): [esperamos el nombre del nivel,
                                'nivel_instrucciones',
                                'nivel_empezamos',
                                'nivel_recuerdas']
        whichLevel (int, optional): [a que nivel cambiamos esto
                                    setea en el json la parte de level].
                                    Defaults to 3.
    """

    while True:
        if c.CRONOMETRO == 'PLAY':

            # Players confirmaciones
            open_json = open(c.DIR_DATA+"to_front.json")
            confirmaciones = json.load(open_json)
            num_Confir = confirmaciones['Momentos'][nivel_name]['confirmacion']

            # Player por sesion
            # NOTA [en la funcion de confirmacion characters
            # solo ocupo al inicio el get_player, ya que al
            # cambiar el status de algun player a user el front
            # actualiza una varible global, en change status]
            players_sesion = numeroJugadores.get_players()
            num_players = len(players_sesion.index)

            # Lo revizamos cada segundo un vez que fue llamado
            time.sleep(1)
            open_json.close()
            if num_Confir >= num_players:
                print('<<<<<<<<<<<<<<<<<<<<<<<<',
                      'Confirmaron todos los jugadores',
                      '>>>>>>>>>>>>>>>>>>>>>>>>>')
                # GLOBAL
                c.CRONOMETRO = 'STOP'
                ##############################
                # Cambiamos de nivel
                handle_json.add_levels_manual('level', whichLevel)
                ##############################
                break
        elif c.CRONOMETRO == 'STOP':
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                  'Cronometro Stop from Wait Players',
                  '>>>>>>>>>>>>>>>>>>>>>>>>>')
            automaticElection.confirm_characters()
            update_data.update_info_jugador()
            ###################################
            # Cambiamos de nivel
            handle_json.add_levels_manual('level', whichLevel)
            ###################################
            break

    return


def wait_avanzar_retroceder(nivel_name,
                            mode='Momentos'):
    # Seccion especifica para nivel_empezamos, recuerda que
    # es la parte donde los jugadores pueden avanzar
    # o retroceder en los niveles
    while True:
        # Players confirmaciones
        open_json = open(c.DIR_DATA+"to_front.json")
        confirmaciones = json.load(open_json)
        num_Confir = confirmaciones[mode][nivel_name]['confirmacion']

        # NOTA [en la funcion de confirmacion characters
        # solo ocupo al inicio el get_player, ya que al
        # cambiar el status de algun player a user el front
        # actualiza una varible global, en change status]
        players_sesion = numeroJugadores.get_players()
        num_players = len(players_sesion.index)

        # Lo revizamos cada segundo un vez que fue llamado
        time.sleep(1)
        open_json.close()
        if num_Confir >= num_players:
            print('<<<<<<<<<<<<<<<<<<<<<<<<',
                  'Confirmaron todos los jugadores',
                  '>>>>>>>>>>>>>>>>>>>>>>>>>')

            lista = confirmaciones[mode][nivel_name]['respuestas']
            if type(lista) == list:
                # FIRE: [arreglar esto no funciona]
                if np.all(np.array(lista == 'Si')):
                    print('ALGUIEN CONTESTO DIFERENTE')
                else:
                    print('TODAS SON IGUALES')

            ##############################
            # Cambiamos de nivel
            # handle_json.add_levels_manual('level', whichLevel)
            ##############################
            c.THREADS_CRONOMETRO = False
            break
