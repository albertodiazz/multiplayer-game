
# SOCKETIO PORT
PORT = 3000
# Seteamos a produccion o seguimos en debug mode que es True
DEBUG_MODE = True
ASYNC_MODE = None
# Aqui seteamos si queremos usar el index html
INDEX_MODE = True
# Aqui es donde tenemos almacenado el index HTML
DIR_INDEX = 'D:/trabajo/cocay/ramodelacion_Mide/radioGrafia_BancoCentral/Backend/lib/socketIO/frontTest/' # noqa
# Aqui seteamos el url de la carpeta data
DIR_DATA = 'data/'
'''
..............................
        GLOBAL VARIABLES
..............................
'''
# Para saber si hay un thread del cronometro corriendo
# Nos sirve para saber cuando fue incializado en app.py
THREADS_CRONOMETRO = False
# Con esta variable sabemos cuando el cronometro esta en
# STOP/PLAY. Esta variable la solemos utilizar en subfunciones
# por ejemplo en waitMoments
CRONOMETRO = 'STOP'
# En este variable obetnemos nuestro contador de mayor a menor
TIEMPO_GLOBAL = {'minutos': 0, 'segundos': 0}
'''
..............................
        SETUP JUEGO
..............................
'''
####################################
# Modo de Juego "Solo/MultiJugador"
MODO_DE_JUEGO = 'Multijugador'
####################################
# Tiempos expresado en segundos si quieres 2min serian 120s
# Temporizador para seleccionar personajes
TIME_SECONDS = 30
####################################
# Temporizador para unirse al juego
JOIN_SECONDS = 10
####################################
MOMENTOS_SECONDS = 10
####################################
# Cantidad de Niveles recuerda que se cuenta desde el 0
# ejemplo: 6 seria [0,1,2,3,4,5], etc...
CANTIDAD_NIVELES = 7
CANTIDAD_RETOS = 9
####################################
# Cantindad maxima de jugadores. La app no tiene un limite
# de jugadores, sin embargo esta varibale es necesaria setearla,
# para el tiempo de espera en la pantalla de unirse, ya que si se
# se unes los dictados por esta variable omitimos el cronometro
MAX_JUGADORES = 3
####################################
