# Implementar los metodos de la capa de negocio de socios.

from practico_05.ejercicio_01 import Socio
from practico_05.ejercicio_02 import DatosSocio


class DniRepetido(Exception):
    pass


class LongitudInvalida(Exception):
    pass


class MaximoAlcanzado(Exception):
    pass


class NegocioSocio(object):

    MIN_CARACTERES = 3
    MAX_CARACTERES = 15
    MAX_SOCIOS = 200

    def __init__(self):
        self.datos = DatosSocio()

    def buscar(self, id_socio):
        """
        Devuelve la instancia del socio, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        socio = self.datos.buscar(id_socio);
        if socio is not None:
            print('El socio encontrado es: ', socio.nombre , ' ', socio.apellido)
            return socio
        else:
            return None
        

    def buscar_dni(self, dni_socio):
        """
        Devuelve la instancia del socio, dado su dni.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        socio = self.datos.buscar_dni(dni_socio);
        if socio is not None:
            print('El socio encontrado es: ', socio.nombre , ' ', socio.apellido)
            return socio
        else:
            return None

    def todos(self):
        """
        Devuelve listado de todos los socios.
        :rtype: list
        """
        socios = self.datos.todos()
        if socios is not None:
            print('Los socios encontrados son: ')
            for socio in socios:
                print(socio.nombre , ' ', socio.apellido)
            return socios
        else:
            print('No se encontraron socios')
            return None

    def alta(self, socio):
        """
        Da de alta un socio.
        Se deben validar las 3 reglas de negocio primero.
        Si no validan, levantar la excepcion correspondiente.
        Devuelve True si el alta fue exitoso.
        :type socio: Socio
        :rtype: bool
        """
        if self.regla_1(socio) and self.regla_2(socio) and self.regla_3():
            socioCreado = self.datos.alta(socio)
            if socioCreado is not None:
                print('El socio creado es: ', socio.nombre , ' ', socio.apellido)
                return True
            else:
                print ('No se pudo crear el socio')
                return False
        else:
            print ('No se cumplieron las reglas de negocio')
            return False

    def baja(self, id_socio):
        """
        Borra el socio especificado por el id.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        if self.datos.baja(id_socio):
            print('El socio fue borrado')
            return True
        else:
            print('El socio no fue borrado')
            return False

    def modificacion(self, socio):
        """
        Modifica un socio.
        Se debe validar la regla 2 primero.
        Si no valida, levantar la excepcion correspondiente.
        Devuelve True si la modificacion fue exitosa.
        :type socio: Socio
        :rtype: bool
        """
        if self.regla_2(socio):
            socioModificado = self.datos.modificacion(socio)
            if socioModificado is not None:
                print('El socio modificado es: ', socio.nombre , ' ', socio.apellido)
                return True
            else:
                return False
        else:
            return False

    def regla_1(self, socio):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: DniRepetido
        :return: bool
        """
        if self.datos.buscar_dni(socio.dni) is None:
            return True
        else:
            raise Exception("No se puede dar de alta al socio: no cumple con la regla 1 (DNI repetido))")
        return False

    def regla_2(self, socio):
        """
        Validar que el nombre y el apellido del socio cuenten con mas de 3 caracteres pero menos de 15.
        :type socio: Socio
        :raise: LongitudInvalida
        :return: bool
        """
        if len(socio.nombre) > self.MIN_CARACTERES and len(socio.nombre) < self.MAX_CARACTERES:
            if len(socio.apellido) > self.MIN_CARACTERES and len(socio.apellido) < self.MAX_CARACTERES:
                return True
            else:
                raise Exception("No se puede dar de alta al socio: no cumple con la regla 2 (Longitud del apellido invalida)")
        else:
            raise Exception("No se puede dar de alta al socio: no cumple con la regla 2 (Longitud del nombre invalida)")


    def regla_3(self):
        """
        Validar que no se esta excediendo la cantidad maxima de socios.
        :raise: MaximoAlcanzado
        :return: bool
        """
        if len(self.datos.todos()) < self.MAX_SOCIOS:
            return True
        else:
            raise Exception("No se puede dar de alta al socio: no cumple con la regla 3 (Maximo de socios alcanzado)")
        
