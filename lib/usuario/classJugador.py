from lib import pd


class Jugadores:
    """
        Clase donde agregamos atributos del Jugador
        siempre que querramos agregar cosas o eliminar msg
        hay que modificar sobre esta clase
    """

    def __init__(self):
        df = pd.DataFrame([{
            'ID': 'null',
            'SeleccionID': 'null',
            'StatusConfirmacion': 'null',
            'Nivel': 'null',
            'Reto': 'null',
            'Seleccion': 'False'
        }])
        self.Datos = df

    @property
    def get_playerID(self):
        return self.Datos['ID'][0]

    def newPlayer(self, _ID):
        self.Datos['ID'] = _ID
        self.Datos.set_index('ID', inplace=True)
        return self
