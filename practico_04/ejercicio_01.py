"""Base de Datos SQL - Crear y Borrar Tablas"""

import sqlite3

def crear_tabla():
    """Implementar la funcion crear_tabla, que cree una tabla Persona con:
        - IdPersona: Int() (autoincremental)
        - Nombre: Char(30)
        - FechaNacimiento: Date()
        - DNI: Int()
        - Altura: Int()
    """
    pass # Completar
    conexion = sqlite3.connect('mi_basedatos.db')
    cursor = conexion.cursor()
    tabla_Persona = '''
    CREATE TABLE IF NOT EXISTS Persona (
        idpersona INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre Char(30),
        nacimiento Date,
        DNI int,
        Altura int
    )
'''
    cursor.execute(tabla_Persona)
    conexion.commit()
    conexion.close()


def borrar_tabla():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    pass # Completar
conexion = sqlite3.connect('mi_basedatos.db')
cursor = conexion.cursor()
tabla_Persona = '''
    DROP TABLE IF EXISTS Persona
'''
cursor.execute(tabla_Persona)
conexion.commit()
conexion.close()


# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        func()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN
