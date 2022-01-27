
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

app = Flask(__name__, template_folder=c.DIR_INDEX)
socketio = SocketIO(app, async_mode=c.ASYNC_MODE)

work_queue = queue.Queue()
thread_runing = False


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
        disconnect()
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


# Una vez recibamos el ID de quien sea empezamos la applicacion
@socketio.on('/user/start')
def userStart(jsonMsg):
    """[Solo funciona para cambiar el video]"""
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


# Aqui es donde manejamos los usuarios que se unan al juego
@socketio.on('/user/unirme')
def userUnirme(jsonMsg):
    """[Aqui es donde creamos el Jugador]"""
    try:
        msg = json.loads(jsonMsg)
        print(msg)
        if len(msg['ID']) >= 0:
            # Aqui ejecutamos la funcion
            changeTipo.change_to_player(msg['ID'])
            app.logger.info({'userUnirme': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userUnirme': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


def funcionX():
    # PENDIENTE = agregar funcion de continuar que funciona como
    # un cuarto nivel, en el cual tendras que implementar la logica
    # de si es mas de un jugador o no.
    # Considero que lo mejor es crear una funcion de logica de cantidad
    # de jugadores
    return


# Aqui el usuario nos envia su eleccion de personaje y confirmacion
# si no confirma no lo bloqueamos en la base de datos
@socketio.on('/user/seleccion')
def userSeleccion(jsonMsg):
    global thread_runing
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            if len(msg['seleccion']) >= 2:
                ''' Aqui ejecutamos la funcion '''
                # FIRE
                # 1.- Agregar temporizador ---- Listo ----
                # 2.- Logica de si es mas de un jugador
                # 3.- Resetear variable global y queue ---- Listo ----

                # El cronometro no es una funcion por jugador entonces debemos
                # correr la funcion en back como algo general
                players = pd.read_csv(c.DIR_DATA+'info_sesion.csv',
                                      index_col=0)
                seleccion = int(msg['seleccion'][0])

                if work_queue.empty():
                    # Quiere decir que el queue esta vacio ya que el
                    # temporizador aun no termina
                    thr1 = threading.Thread(target=cronometro.temporizador,
                                            args=(c.TIME_SECONDS,
                                                  work_queue))

                    if thread_runing:
                        # Revizamos que no este corriendo el Thread
                        print('<<<<<<<<<<<<<<<<< ',
                              'Cronometro is running', ' >>>>>>>>>')
                    else:
                        # Si no esta corriendo
                        # Corremos el cronometro en segundo plano
                        # Seteamos nuestra variable gobal
                        thr1.start()
                        thread_runing = thr1.isAlive()
                        print('<<<<<<<<<<<<<<<<< ', 'Start Cronometro: ',
                              thread_runing, ' >>>>>>>>>>>>>')

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
                    # Actualizamos la data main que info_sesion.csv
                    update_data.update_info_jugador()
                else:
                    # LLegamos a este punto cuando nuestro tiempo se ha acabado
                    # la forma de resetear el cronometro es limpiando el queu
                    # work_queue.get()
                    app.logger.info('Ya no hay tiempo de eleccion')
                    return {'response': 'Resetea el temporizador'}

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


# Aqui seteamos las respuestas por reto y jugador
@socketio.on('/user/respuesta')
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


# Reseteamos los datos por sesion de usuario
@socketio.on('/user/resetAll')
def resetAll(jsonMsg):
    global thread_runing
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Aqui reseteamos queue y thread
            thread_runing = False
            work_queue.get()
            # Aqui reseteamos Personajes.csv
            reset.resetSesion()

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
