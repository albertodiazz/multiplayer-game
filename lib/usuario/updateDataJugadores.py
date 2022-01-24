def updateData_Jugadores(data, ID=None, Columna=None, msg=None):
    # PENDIENTE = Actualizar las metada de los Jugadores
    # con la data de la tabla de los personajes y las respuestas de los niveles

    # Aqui seteamos todas las columnas de nuestra tabla de Jugadores
    # Recuerda que trabajamos tres tablas la de personajes,
    # respuestas correctas por nivel y Jugadores donde se centralizan,
    # las otras tablas
    if Columna == 'Nivel':
        if msg != None:
            data.at[ID, Columna] += ',' + msg
            data.at[ID, Columna] = data.loc[ID, Columna].replace("null,", "")
    else:
        if msg != None:
            data.at[ID, Columna] = msg
