
'''
BUG : al momento de comparar los ID, si el fron manda null no ocurre nada y
tampoco se levanta el raise
'''
import threading
import flask
from lib import SocketIO, disconnect
from lib import Flask
from lib import c
from lib import json
from lib import queue
from lib import pd
from lib import funcionesJugador
from lib import cronometro
from lib import update_data
from lib import resetAll as reset
from lib import changeTipo
from lib import deletUser
from lib import waitMoments
from lib import numeroJugadores
from lib import handle_json

app = Flask(__name__, template_folder=c.DIR_INDEX)
socketio = SocketIO(app, async_mode=c.ASYNC_MODE)

work_queue = queue.Queue()


class SocketIOEventos(Exception):
    pass


# Con esta condicion lo que hacemos es setear el modo, si quieres cambiarlo
# ve al archivo de config.py y pon el INDEX_MODE = False
if c.INDEX_MODE:
    print(c.INDEX_MODE)
    from flask import render_template

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html', async_mode=socketio.async_mode)
else:
    @app.route('/')
    def index():
        return '<p>Hellow World desde Flask </p>'


@socketio.on('connect')
def connect():
    # Aqui no importa si son dos o mas jugadores
    try:
        # Comprobamos conexiones de clientes
        app.logger.info('connect: ',
                        'Alguien se conecto al servidor: ',
                        flask.request.sid)
        # Creamos jugador por sesion con el atributo user
        # en unirse se lo cambiamos a player
        funcionesJugador.create_player(flask.request.sid)
    except TypeError:
        app.logger.info('No hay conexion con el servidor')
        return


@socketio.on('disconnect')
def on_disconnect():
    try:
        deletUser.delete(flask.request.sid)
        print('\n', '<<<<<<<< Alguien se deconecto >>>>>>>')
        print(flask.request.sid)
    except TypeError:
        app.logger.info('No hay conexion con el servidor')
        disconnect()
        return


@socketio.on('/user/start')
def userStart(jsonMsg):
    """[Solo funciona para cambiar el video]"""
    # Una vez recibamos el ID de quien sea empezamos la applicacion
    # Aqui no importa si son dos o mas jugadores
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Aqui ejecutamos la funcion
            app.logger.info({'userStart': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userStart': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/user/unirme')
def userUnirme(jsonMsg):
    """[Aqui es donde creamos el Jugador]"""
    # Aqui es donde manejamos los usuarios que se unan al juego
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Aqui ejecutamos la funcion
            changeTipo.change_to_player(msg['ID'])
            ##########################################
            '''IMPORTANTE aqui revizamos el modo de juego
               una vez acabado el temporizador'''
            ##########################################
            # GLOBAL
            if c.THREADS_CRONOMETRO:
                print('<<<<<<<< Cronometo is running >>>>>>>>>')
            else:
                print('<<<<<<<< Cronometo START >>>>>>>>>')
                _cronometro_ = threading.Thread(target=cronometro.temporizador,
                                                args=(c.JOIN_SECONDS,
                                                      work_queue))
                _cronometro_.start()
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                _waitMoments_ = threading.Thread(target=waitMoments.wait_join_players) # noqa
                _waitMoments_.start()

                # GLOBAL
                c.THREADS_CRONOMETRO = _waitMoments_.isAlive()
            app.logger.info({'userUnirme': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userUnirme': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/player/seleccion')
def userSeleccion(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            if len(msg['seleccion']) >= 2:
                ''' Aqui ejecutamos la funcion '''
                # PENDIENTE
                # 1.- Logica de si es mas de un jugador
                # esto ya lo tenemos a nivel variable global
                # FIRE aqui el cronometro empieza desde el principio
                # antes de que le presionen al boton
                players = pd.read_csv(c.DIR_DATA+'info_sesion.csv',
                                      index_col=0)
                seleccion = int(msg['seleccion'][0])

                _cronometro_ = threading.Thread(target=cronometro.temporizador,
                                                args=(c.TIME_SECONDS,
                                                      work_queue))
                # GLOBAL
                if c.THREADS_CRONOMETRO:
                    # Revizamos que no este corriendo el Thread
                    print('<<<<<<<<<<<<<<<<< ',
                          'Cronometro is running', ' >>>>>>>>>')
                else:
                    # Si no esta corriendo
                    # Corremos el cronometro en segundo plano
                    # Seteamos nuestra variable gobal
                    _cronometro_.start()
                    # GLOBAL
                    c.THREADS_CRONOMETRO = _cronometro_.isAlive()
                    print('<<<<<<<<<<<<<<<<< ', 'Start Cronometro: ',
                          c.THREADS_CRONOMETRO, ' >>>>>>>>>>>>>')

                if msg['seleccion'][1] == 'True':
                    # No han mandado confirmacion
                    funcionesJugador.seleccionDePersonaje(msg['ID'],
                                                          seleccion,
                                                          players,
                                                          True)

                else:
                    funcionesJugador.seleccionDePersonaje(msg['ID'],
                                                          seleccion,
                                                          players)
                # Actualizamos la data main de info_sesion.csv
                update_data.update_info_jugador()

                app.logger.info({'userSeleccion': {'ID': msg['ID']}})
            else:
                raise SocketIOEventos({
                    msg['ID']: 'Faltan atributos'
                })
        else:
            raise SocketIOEventos({
                'userSeleccion': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/momentos/confirmaciones')
def espera_confirmacion(jsonMsg):
    """[Aqui es donde esperamos las confirmaciones de
        los diferentes momentos]"""
    try:
        msg = json.loads(jsonMsg)
        if len(msg['Momento']) >= 0:
            # Aqui ejecutamos la funcion
            ##########################################
            '''IMPORTANTE aqui revizamos el modo de juego
               una vez acabado el temporizador'''
            ##########################################
            # No nos importa cuantas veces lo llamen aqui ponemos
            # un append para el json y en back lo revizamos todo el tiempo
            # revizando que corresponda con el numero de
            # participantes por sesion
            handle_json.add_confirmaciones_automatic(msg['Momento'])

            # GLOBAL
            if c.THREADS_CRONOMETRO:
                print('<<<<<<<< Cronometo is running >>>>>>>>>')
            else:
                print('<<<<<<<< Cronometo START >>>>>>>>>')
                _cronometro_ = threading.Thread(target=cronometro.temporizador,
                                                args=(c.JOIN_SECONDS,
                                                      work_queue))
                _cronometro_.start()
                print('<<<<<<<< Wait Moments >>>>>>>>>')
                _waitMoments_ = threading.Thread(target=waitMoments.wait_confirmaciones_json, # noqa
                                                 args=(msg['Momento'],))
                _waitMoments_.start()

                # GLOBAL
                c.THREADS_CRONOMETRO = _waitMoments_.isAlive()
        else:
            raise SocketIOEventos({
                'Response': 'no enviaste nada'
                })
    except TypeError:
        return


@socketio.on('/player/respuesta')
def setRespuestas(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            if len(msg['respuestas']) == 4:
                # Aqi ejecutamos la funcion
                # PENDIENTE: setear repuestas en los usuarios
                app.logger.info({'setRespuestas': {'ID': msg['ID']}})
            else:
                raise SocketIOEventos({
                    msg['ID']: 'Faltan atributos'
                })
        else:
            raise SocketIOEventos({
                'setRespuestas': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


@socketio.on('/player/changeStatus')
def change_player_to_user(jsonMsg):
    """[Funcion en donde cambiamos al player to user
        esto significa que pasara de ser un jugador a un
        usuario nada mas]
    """
    # TEST
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Aqui ejecutamos la funcion
            changeTipo.change_to_user(msg['ID'])
            app.logger.info({'userUnirme': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userUnirme': 'no recivimos el ID del participante'
                })
    except TypeError:
        return

    return


@socketio.on('/sesion/resetAll')
def resetAll(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # FIRE: recuerda en resetear el json a su estado original
            # Aqui reseteamos Personajes.csv
            reset.resetSesion()
            # Aqui reseteamos queue y thread
            c.THREADS_CRONOMETRO = False
            # work_queue.get()

            app.logger.info({'userStart': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userStart': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


def runSocketIO():
    print('Iniciando Socket IO')
    socketio.run(app, port=c.PORT, debug=c.DEBUG_MODE)


if __name__ == '__main__':
    print('Inciando App de Radiografias del Banco de Mexico')
    runSocketIO()
