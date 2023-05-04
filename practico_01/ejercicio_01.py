"""Bloque IF, operadores lógicos, función max y operador ternario."""


def maximo_basico(a: float, b: float) -> float:
    """Toma dos números y devuelve el mayor.
    Restricción: No utilizar la función max"""
   # pass # Completar
    if a > b:
        return a
    elif a==b:
        return "Son iguales"
    else:
        return b


# NO MODIFICAR - INICIO
assert maximo_basico(10, 5) == 10
assert maximo_basico(9, 18) == 18
print(maximo_basico(10,11))
# NO MODIFICAR - FIN


###############################################################################


def maximo_libreria(a: float, b: float) -> float:
    pass  # Completar
    return max(a, b)

# NO MODIFICAR - INICIO
assert maximo_libreria(10, 5) == 10
assert maximo_libreria(9, 18) == 18
print(maximo_libreria(12,153))
# NO MODIFICAR - FIN


###############################################################################


def maximo_ternario(a: float, b: float) -> float:
    """Re-escribir utilizando el operador ternario.
    Referencia: https://docs.python.org/3/reference/expressions.html#conditional-expressions
    """
    pass # Completar
    return a if a > b else b if b > a else "son iguales"

# NO MODIFICAR - INICIO
assert maximo_ternario(10, 5) == 10
assert maximo_ternario(9, 18) == 18
print(maximo_ternario(10,10))
# NO MODIFICAR - FIN
