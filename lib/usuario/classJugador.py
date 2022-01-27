from lib import pd


class Jugadores:
    """
        Clase donde agregamos atributos del Jugador
        siempre que querramos agregar cosas o eliminar msg
        hay que modificar sobre esta clase

        ---------------------------
        IMPORTANTE: para eliminar la columna tenemos que quitarla manual
        del csv y quitarla de los atributos.
        En el caso de agregar esto pasa en automatico y no hay mas que
        agregarlo como atributo
        ---------------------------

        TipoDeUsuario: user / player
    """

    def __init__(self):
        df = pd.DataFrame([{
            'ID': 'null',
            'SeleccionID': 'null',
            'StatusConfirmacion': 'null',
            'Nivel': 'null',
            'Reto': 'null',
            'Seleccion': 'False',
            'TipoDeUsuario': 'user'
        }])
        self.Datos = df

    @property
    def get_playerID(self):
        return self.Datos['ID'][0]

    def newPlayer(self, _ID):
        self.Datos['ID'] = _ID
        self.Datos.set_index('ID', inplace=True)
        return self
