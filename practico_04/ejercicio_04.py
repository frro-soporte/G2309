"""Base de Datos SQL - Búsqueda"""

import datetime
import sqlite3

from practico_04.ejercicio_01 import *
from practico_04.ejercicio_02 import *


def buscar_persona(id_persona):
    """Implementar la funcion buscar_persona, que devuelve el registro de una 
    persona basado en su id. El return es una tupla que contiene sus campos: 
    id, nombre, nacimiento, dni y altura. Si no encuentra ningun registro, 
    devuelve False."""
    pass # Completar
    conexion = sqlite3.Connection('mi_basedatos.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT idpersona, nombre, nacimiento, dni, altura FROM Persona WHERE idpersona = ?', (id_persona,))
    resultado = cursor.fetchone()
    if resultado is not None:
        conexion.close()
        return resultado
    else:
        conexion.close()
        return False


# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    juan = buscar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    assert juan == (1, 'juan perez','1988-05-15 00:00:00', 32165498, 180)
    assert buscar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
