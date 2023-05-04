"""Comparaciones Encadenadas, Cantidad Arbitraria de Parámetros, Recursividad."""


def maximo_encadenado(a: float, b: float, c: float) -> float:
    """Toma 3 números y devuelve el máximo.

    Restricción: Utilizar UNICAMENTE tres IFs y comparaciones encadenadas.
    Referencia: https://docs.python.org/3/reference/expressions.html#comparisons
    """
  #  pass # Completar
    if a>=b and a>=c:
        return a
    elif b>=c :
        return b
    else:
        return c

# NO MODIFICAR - INICIO
assert maximo_encadenado(1, 10, 5) == 10
assert maximo_encadenado(4, 9, 18) == 18
assert maximo_encadenado(24, 9, 18) == 24
print(maximo_encadenado(12,12,12))
# NO MODIFICAR - FIN


###############################################################################


def maximo_cuadruple(a: float, b: float, c: float, d: float) -> float:
    """Re-escribir para que tome 4 parámetros, utilizar la función max.

    Referencia: https://docs.python.org/3/library/functions.html#max"""
    pass # Completar
    return max(a,b,c,d)

# NO MODIFICAR - INICIO
assert maximo_cuadruple(1, 10, 5, -5) == 10
assert maximo_cuadruple(4, 9, 18, 6) == 18
assert maximo_cuadruple(24, 9, 18, 20) == 24
assert maximo_cuadruple(24, 9, 18, 30) == 30
print(maximo_cuadruple(100,103,101,999))
# NO MODIFICAR - FIN


###############################################################################


def maximo_arbitrario(*args) -> float:
    """Re-escribir para que tome una cantidad arbitraria de parámetros.
    Referencia: https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists
    """
    pass # Completar
    return max(args)

# NO MODIFICAR - INICIO
assert maximo_arbitrario(1, 10, 5, -5) == 10
assert maximo_arbitrario(4, 9, 18, 6) == 18
assert maximo_arbitrario(24, 9, 18, 20) == 24
assert maximo_arbitrario(24, 9, 18, 30) == 30
print(maximo_arbitrario(100,103,101,999,10000,999879,7898740,123212321))
# NO MODIFICAR - FIN


###############################################################################


def maximo_recursivo(*args) -> float:
    """Re-Escribir de forma recursiva."""
    pass # Completar
        if len(args) == 1:
            return args[0]
        elif len(args) == 2:
            return args[0] if args[0] > args[1] else args[1]
        else:
            sub_max = maximo_recursivo(*args[1:])
            return args[0] if args[0] > sub_max else sub_max


# NO MODIFICAR - INICIO
assert maximo_recursivo(1, 10, 5, -5) == 10
assert maximo_recursivo(4, 9, 18, 6) == 18
assert maximo_recursivo(24, 9, 18, 20) == 24
assert maximo_recursivo(24, 9, 18, 30) == 30
#print (maximo_recursivo(24, 9, 18, 20) )
#print (maximo_recursivo(24, 9, 18, 30) )
# NO MODIFICAR - FIN
