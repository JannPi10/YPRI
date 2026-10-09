"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Utilidades y Validaciones Defensivas por Consola
========================================================================================
Proporciona funciones para validar entradas de teclado y prevenir errores por
datos vacios, tipos incorrectos, valores fuera de rango o formatos invalidos.
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
    Solicita al usuario una respuesta binaria (s/n).
    Rechaza numeros, cadenas vacias o palabras distintas.
    """
    while True:
        resp = input(prompt).strip().lower()
        if resp in ("s", "n"):
            return resp
        print("[!] Solo se acepta 's' para Si o 'n' para No.")


def pedir_solo_letras(prompt, campo):
    """
    Exige que el valor contenga al menos una letra alfabetica.
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
    Valida que la entrada sea un entero dentro del rango [minimo, maximo].
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
    Valida que la entrada sea un valor numerico decimal en el rango [minimo, maximo].
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


def pedir_categoria():
    """
    Muestra las categorias oficiales (Tupla CATEGORIAS_SERVICIO) y valida la eleccion.
    """
    print(f"  Categorias disponibles: {', '.join(CATEGORIAS_SERVICIO)}")
    while True:
        valor = input("  Categoria: ").strip().capitalize()
        if valor in CATEGORIAS_SERVICIO:
            return valor
        print(f"[!] Categoria invalida. Opciones: {', '.join(CATEGORIAS_SERVICIO)}")


def pedir_ciudad():
    """
    Muestra las ciudades de cobertura (Tupla CIUDADES_COBERTURA) y valida la entrada.
    """
    print(f"  Ciudades disponibles: {', '.join(CIUDADES_COBERTURA)}")
    while True:
        valor = input("  Ciudad: ").strip().capitalize()
        if valor in CIUDADES_COBERTURA:
            return valor
        print(f"[!] Ciudad invalida. Opciones: {', '.join(CIUDADES_COBERTURA)}")


def pedir_correo(prompt):
    """
    Valida que el correo electronico contenga estructura minima usuario@dominio.extension.
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
    Solicita un texto descriptivo con longitud minima y al menos una letra.
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
    Solicita un identificador de registro por consola.
    Permite cancelar con '0' retornando None.
    Valida prefijos esperados (ej. 'SERV', 'CONTR', 'USR').
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
    """Genera un identificador secuencial unico basado en la cantidad de registros."""
    return f"{prefijo}-{str(len(lista) + 1).zfill(3)}"
