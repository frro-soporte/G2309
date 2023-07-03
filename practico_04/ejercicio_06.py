"""Base de Datos SQL - Creación de tablas auxiliares"""
import sqlite3

from practico_04.ejercicio_01 import *


def crear_tabla_peso():
    """Implementar la funcion crear_tabla_peso, que cree una tabla PersonaPeso con:
        - IdPersona: Int() (Clave Foranea Persona)
        - Fecha: Date()
        - Peso: Int()
    """
    pass # Completar
    conexion = sqlite3.Connection('mi_basedatos.db')
    cursor = conexion.cursor()
    tabla_PersonaPeso = '''
        CREATE TABLE IF NOT EXISTS PersonaPeso (
            idPeso INTEGER PRIMARY KEY AUTOINCREMENT,
            idPersona int, 
            Fecha Date,
            Peso int,
            FOREIGN KEY (IdPersona) REFERENCES Persona (idpersona)
        )
    '''
    cursor.execute(tabla_PersonaPeso)
    conexion.commit()
    conexion.close()
def borrar_tabla_peso():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    pass # Completar
    conexion = sqlite3.Connection('mi_basedatos.db')
    cursor = conexion.cursor()
    tabla_PersonaPeso = '''
        DROP TABLE IF EXISTS PersonaPeso
    '''
    cursor.execute(tabla_PersonaPeso)
    conexion.commit()
    conexion.close()
# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        crear_tabla_peso()
        func()
        borrar_tabla_peso()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN
