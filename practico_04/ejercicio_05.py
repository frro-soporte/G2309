"""Base de Datos SQL - Modificación"""

import datetime
import sqlite3

from practico_04.ejercicio_01 import *
from practico_04.ejercicio_02 import agregar_persona
from practico_04.ejercicio_04 import buscar_persona


def actualizar_persona(id_persona, nombre, nacimiento, dni, altura):
    """Implementar la funcion actualizar_persona, que actualiza un registro de
    una persona basado en su id. Devuelve un booleano en base a si encontro el
    registro y lo actualizo o no."""
    pass # Completar
    conexion = sqlite3.Connection('mi_basedatos.db')
    cursor = conexion.cursor()
    cursor.execute('Select idPersona, nombre, nacimiento, dni, altura From Persona Where idPersona = ?', (id_persona,))
    resultado = cursor.fetchone()

    if resultado is not None:
        cursor.execute('UPDATE Persona '
                        'SET nombre = ?, nacimiento = ?, dni = ?, altura = ? '
                        'WHERE idpersona = ?',
                        (nombre, nacimiento, dni, altura, id_persona,))
        conexion.commit()
        conexion.close()
        return True
    else:
        conexion.close()
        return False



# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    id_juan = agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    actualizar_persona(id_juan, 'juan carlos perez', datetime.datetime(1988, 4, 16), 32165497, 181)
    assert buscar_persona(id_juan) == (1, 'juan carlos perez','1988-04-16 00:00:00' , 32165497, 181)
    assert actualizar_persona(123, 'nadie', datetime.datetime(1988, 4, 16), 12312312, 181) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
