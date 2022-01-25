
'''
BUG : al momento de comparar los ID, si el fron manda null no ocurre nada y
tampoco se levanta el raise
'''
from numpy import empty
from lib import SocketIO, disconnect
from lib import Flask
from lib import c
from lib import json
from lib import queue
from lib import pd
from lib import funcionesJugador
from lib import update_data

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
    try:
        # Comprobamos conexiones de clientes
        app.logger.info('Alguien se conecto al servidor')
    except TypeError:
        app.logger.info('No hay conexion con el servidor')
        disconnect()
        return


# Una vez recibamos el ID de quie sea empezamos la applicacion
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
        if len(msg['ID']) >= 0:

            # Aqui ejecutamos la funcion
            # data_copy = pd.DataFrame([])
            funcionesJugador.create_player(msg['ID'])
            # data_copy = data
            # TEST= aun no lo probamos
            # Lo que hacemos es comprobar que nuestro cue siempre este limpio
            # y asi solo subir la ultima version de nuestra data
            # while True:
            #     if work_queue.empty():
            #         work_queue.put(data_copy)
            #         break
            #     else:
            #         work_queue.get()

            app.logger.info({'userUnirme': {'ID': msg['ID']}})
        else:
            raise SocketIOEventos({
                'userUnirme': 'no recivimos el ID del participante'
                })
    except TypeError:
        return


def funcionX():
    # PENDIENTE = agregar funcion de coninuar que funciona como
    # un cuarto nivel, en el cual tendras que implementar la logica
    # de si es mas de un jugador o no.
    # Considero que lo mejor es crear una funcion de logica de cantidad
    # de jugadores
    return


# Aqui el usuario nos envia su eleccion de personaje y confirmacion
# si no confirma no lo bloqueamos en la base de datos
@socketio.on('/user/seleccion')
def userSeleccion(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            if len(msg['seleccion']) >= 2:
                ''' Aqui ejecutamos la funcion '''
                # FIRE
                # 1.- Agregar temporizador
                # 2.- Logica de si es mas de un jugador
                # El cronometro no es una funcion por jugador entonces debemos
                # correr la funcion en back como algo general
                # TEST= Aun esta incompleta ya que falta la opcion de data
                #       en seleccionDePersonaje()
                players = pd.read_csv(c.DIR_DATA+'info_sesion.csv',
                                      index_col=0)
                seleccion = int(msg['seleccion'][0])
                if msg['seleccion'][1] == 'True':
                    print('El jugador ha confirmado')
                    funcionesJugador.seleccionDePersonaje(msg['ID'],
                                                          seleccion,
                                                          players,
                                                          True)

                    update_data.update_info_jugador()
                else:
                    funcionesJugador.seleccionDePersonaje(msg['ID'],
                                                          seleccion,
                                                          players)
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


# Aqui seteamos las respuestas por reto y jugador
@socketio.on('/user/respuesta')
def setRespuestas(jsonMsg):
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            if len(msg['respuestas']) == 4:
                # Aqi ejecutamos la funcion
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
    try:
        msg = json.loads(jsonMsg)
        if len(msg['ID']) >= 0:
            # Aqui ejecutamos la funcion
            # IMPORTANTE hay que resetar el array de players
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

