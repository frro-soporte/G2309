"""Base de datos SQL - Listar"""

import datetime

from practico_04.ejercicio_02 import agregar_persona
from practico_04.ejercicio_06 import reset_tabla
from practico_04.ejercicio_07 import *


def listar_pesos(id_persona):
    """Implementar la funcion listar_pesos, que devuelva el historial de pesos 
    para una persona dada.

    Debe validar:
    - Que el ID de la persona ingresada existe (reutilizando las funciones ya 
     implementadas).

    Debe devolver:
    - Lista de (fecha, peso), donde fecha esta representado por el siguiente 
    formato: AAAA-MM-DD.

    Ejemplo:
    [
        ('2018-01-01', 80),
        ('2018-02-01', 85),
        ('2018-03-01', 87),
        ('2018-04-01', 84),
        ('2018-05-01', 82),
    ]

    - False en caso de no cumplir con alguna validacion.

    return []
    """
    conexion = sqlite3.Connection('mi_basedatos.db')
    cursor = conexion.cursor()
    existe = buscar_persona(id_persona)
    if existe is not False:
        cursor.execute('Select fecha, peso from PersonaPeso Where idpersona = ?', (id_persona,))
        resultado = cursor.fetchall()
        conexion.close()
        lista=[]
        for i in range (len(resultado)):
            fechaA = resultado[i][0][:10]
            pesoA = resultado[i][1]
            tupla = (fechaA, pesoA)
            lista.append(tupla)
        return lista
    else:
        conexion.close()
        return False




# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    id_juan = agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    agregar_peso(id_juan, datetime.datetime(2018, 5, 1), 80)
    agregar_peso(id_juan, datetime.datetime(2018, 6, 1), 85)
    pesos_juan = listar_pesos(id_juan)
    pesos_esperados = [
        ('2018-05-01', 80),
        ('2018-06-01', 85),
    ]
    assert pesos_juan == pesos_esperados
    # id incorrecto
    assert listar_pesos(200) == False


if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
