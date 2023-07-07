"""Base de Datos SQL - Baja"""

import datetime

from practico_04.ejercicio_01 import *
from practico_04.ejercicio_02 import *


def borrar_persona(id_persona):
    """Implementar la funcion borrar_persona, que elimina un registro en la 
    tabla Persona . Devuelve un booleano en base a si encontro el registro y lo
    borro o no."""
    pass # Completar
    conexion = sqlite3.connect('mi_basedatos.db')
    cursor = conexion.cursor()

    cursor.execute('SELECT idpersona FROM Persona WHERE idpersona = ?', (id_persona,))
    resultado = cursor.fetchone()

    if resultado is not None:
        # El registro existe, procedemos a eliminarlo
        cursor.execute('DELETE FROM Persona WHERE idpersona = ?', (id_persona,))
        conexion.commit()
        conexion.close()
        return True
    else:
        # El registro no existe
        conexion.close()
        return False
# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    assert borrar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    assert borrar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
