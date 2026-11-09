"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Utilidades y Validaciones Defensivas por Consola
========================================================================================
DOCUMENTACION DE TEMAS POR SEMANAS:
- [SEMANAS 5 Y 6 - CICLOS Y VALIDACIONES]:
  * Ciclos 'while True' para bucles de captura con condiciones de salida 'break'.
  * Sentencia 'continue' para reintentar cuando la entrada no cumple criterios.
  * Manejo defensivo de excepciones con bloques 'try - except ValueError'.
  * Validacion de rangos numericos enteros y decimales.
- [SEMANA 7 - TUPLAS, CADENAS Y DICCIONARIOS]:
  * Normalizacion de cadenas con metodos: .strip(), .lower(), .capitalize(), .upper().
  * Validacion de pertenencia contra tuplas inmutables (CATEGORIAS_SERVICIO, CIUDADES).
- [SEMANA 8 - VECTORES]:
  * Validacion de existencia y prefijos de identificadores unicos en vectores (len, zfill).
- [SEMANA 9 - MATRICES EN PYTHON: CREACION, RECORRIDO Y OPERACIONES]:
  * Validacion defensiva para ingreso de celdas matriciales (Guia 9 - Seccion 2):
    Control estricto de floats no negativos (valor >= 0) y capturas con try-except.
  * Validacion de indices de fila [i] y columna [j] dentro de las dimensiones de la matriz.
========================================================================================
"""

from core.constantes import (
    ROLES_SISTEMA,
    CATEGORIAS_SERVICIO,
    CIUDADES_COBERTURA,
    ESTADOS_CONTRATO,
)


def separador(caracter="-", largo=72):
    """Imprime una linea divisoria en consola."""
    print(caracter * largo)


def mostrar_encabezado(subtitulo="SISTEMA DE SERVICIOS A DOMICILIO"):
    """Muestra el encabezado institucional y titulo de la pantalla actual."""
    separador("=")
    print("           YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO")
    print(f"              {subtitulo}")
    separador("=")


def pedir_sn(prompt):
    """
    [SEMANAS 5-6] Solicita al usuario una respuesta binaria (s/n).
    Rechaza numeros, cadenas vacias o palabras distintas.
    """
    while True:
        resp = input(prompt).strip().lower()
        if resp in ("s", "n"):
            return resp
        print("[!] Solo se acepta 's' para Si o 'n' para No.")


def pedir_solo_letras(prompt, campo):
    """
    [SEMANAS 5-7] Exige que el valor contenga al menos una letra alfabetica.
    Rechaza valores vacios o formados unicamente por digitos/simbolos.
    """
    while True:
        valor = input(prompt).strip()
        if valor == "":
            print(f"[!] El campo '{campo}' no puede estar vacio.")
            continue
        tiene_letra = any(c.isalpha() for c in valor)
        if not tiene_letra:
            print(f"[!] '{campo}' debe contener letras, no solo numeros o simbolos.")
            continue
        return valor


def pedir_entero(prompt, minimo, maximo):
    """
    [SEMANAS 5-6] Valida que la entrada sea un entero en el rango [minimo, maximo].
    Controla excepciones de tipo ValueError.
    """
    while True:
        try:
            val = int(input(prompt).strip())
            if val < minimo or val > maximo:
                print(f"[!] Ingrese un numero entero entre {minimo} y {maximo}.")
                continue
            return val
        except ValueError:
            print("[!] Ingrese un numero entero valido.")


def pedir_float(prompt, minimo, maximo):
    """
    [SEMANAS 5-6] Valida que la entrada sea decimal en el rango [minimo, maximo].
    Controla excepciones de tipo ValueError.
    """
    while True:
        try:
            val = float(input(prompt).strip())
            if val < minimo or val > maximo:
                print(f"[!] El valor debe estar entre {minimo} y {maximo}.")
                continue
            return val
        except ValueError:
            print("[!] Ingrese un valor numerico valido.")


# ========================================================================================
# [SEMANA 9 - GUIA 9]: VALIDACION ESPECIFICA PARA INGRESO DE VALORES EN MATRICES
# Cumple el patron exacto ensenado en la Seccion 2 de la Guia de Aprendizaje N.º 9:
# while True -> try float() -> if valor < 0: print(...) continue -> break -> except ValueError
# ========================================================================================

def pedir_valor_matriz_positivo(prompt="Valor: $"):
    """
    [SEMANA 9 - GUIA 9 ACTIVIDAD PRACTICA]:
    Solicita un valor numerico decimal para una celda de matriz garantizando
    que sea no negativo (>= 0) mediante control de excepciones y validacion logica.
    """
    while True:
        try:
            valor = float(input(prompt).strip())
            if valor < 0:
                print("[!] El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("[!] Ingrese un valor numerico valido.")


def pedir_coordenadas_matriz(total_filas, total_columnas, nombres_filas=None, nombres_columnas=None):
    """
    [SEMANA 9 - GUIA 9 ACCESO Y MODIFICACION INDEXADA]:
    Solicita y valida de forma defensiva los indices [i] de fila y [j] de columna
    para consultar o modificar un elemento especifico matriz[i][j].
    Permite al usuario ingresar por numero (1 a N) convirtiendo a base 0.
    """
    print(f"\n  Dimensiones de la matriz: {total_filas} filas x {total_columnas} columnas")
    
    if nombres_filas:
        print("  Filas disponibles:")
        for idx, nom in enumerate(nombres_filas):
            print(f"    [{idx + 1}] {nom}")
    
    fila_sel = pedir_entero(f"  Seleccione Fila (1 a {total_filas}, 0 para cancelar): ", 0, total_filas)
    if fila_sel == 0:
        return None, None
    fila_idx = fila_sel - 1

    if nombres_columnas:
        print("  Columnas disponibles:")
        for idx, nom in enumerate(nombres_columnas):
            print(f"    [{idx + 1}] {nom}")

    col_sel = pedir_entero(f"  Seleccione Columna (1 a {total_columnas}, 0 para cancelar): ", 0, total_columnas)
    if col_sel == 0:
        return None, None
    col_idx = col_sel - 1

    return fila_idx, col_idx


def pedir_categoria():
    """
    [SEMANA 7] Muestra las categorias oficiales (Tupla CATEGORIAS_SERVICIO) y valida la eleccion.
    """
    print(f"  Categorias disponibles: {', '.join(CATEGORIAS_SERVICIO)}")
    while True:
        valor = input("  Categoria: ").strip().capitalize()
        if valor in CATEGORIAS_SERVICIO:
            return valor
        print(f"[!] Categoria invalida. Opciones: {', '.join(CATEGORIAS_SERVICIO)}")


def pedir_ciudad():
    """
    [SEMANA 7] Muestra las ciudades de cobertura (Tupla CIUDADES_COBERTURA) y valida la entrada.
    """
    print(f"  Ciudades disponibles: {', '.join(CIUDADES_COBERTURA)}")
    while True:
        valor = input("  Ciudad: ").strip().capitalize()
        if valor in CIUDADES_COBERTURA:
            return valor
        print(f"[!] Ciudad invalida. Opciones: {', '.join(CIUDADES_COBERTURA)}")


def pedir_correo(prompt):
    """
    [SEMANA 7] Valida que el correo contenga estructura minima usuario@dominio.ext.
    """
    while True:
        correo = input(prompt).strip().lower()
        if correo == "":
            print("[!] El correo no puede estar vacio.")
            continue
        partes = correo.split("@")
        if len(partes) == 2 and partes[0] and "." in partes[1] and partes[1].index(".") > 0:
            return correo
        print("[!] Ingrese un correo valido (ej. nombre@dominio.com).")


def pedir_texto_minimo(prompt, campo, minimo=10):
    """
    [SEMANA 7] Solicita un texto descriptivo con longitud minima y al menos una letra.
    """
    while True:
        valor = input(prompt).strip()
        if len(valor) < minimo:
            print(f"[!] '{campo}' debe tener al menos {minimo} caracteres.")
            continue
        if not any(c.isalpha() for c in valor):
            print(f"[!] '{campo}' debe contener al menos una letra.")
            continue
        return valor


def pedir_id_registro(prompt, prefijo_esperado=None):
    """
    [SEMANA 8] Solicita un identificador de registro por consola.
    Permite cancelar con '0' retornando None.
    """
    while True:
        valor = input(prompt).strip().upper()
        if valor == "0":
            return None
        if valor == "":
            print("[!] El ID no puede estar vacio. Ingrese un ID valido o '0' para cancelar.")
            continue
        if prefijo_esperado and not valor.startswith(prefijo_esperado):
            print(f"[!] El ID debe comenzar con '{prefijo_esperado}' (ej. {prefijo_esperado}-001).")
            continue
        return valor


def generar_id(prefijo, lista):
    """[SEMANA 8] Genera un identificador secuencial unico basado en len(lista)."""
    return f"{prefijo}-{str(len(lista) + 1).zfill(3)}"
