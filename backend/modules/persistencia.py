"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Persistencia en Archivos (Guia 11 - Actividad 1)
========================================================================================
[GUIA 11 - ACTIVIDAD 1 - IMPLEMENTACION DE ARCHIVOS]:
  1. guardar_datos(): escribe usuarios, servicios, contratos, calificaciones y matrices
     en 'datos/ypri_datos.json' con open(..., "w").
  2. cargar_datos(): lee ese archivo con open(..., "r") al iniciar el programa.
  3. Los datos se recuperan al cerrar y volver a ejecutar YPRI: main.py llama a
     cargar_datos() al arrancar y a guardar_datos() al cerrar sesion y al salir.
  4. Control de errores: si el archivo no existe (FileNotFoundError) se crea con los
     datos iniciales; si esta danado (json.JSONDecodeError) se respalda con otro nombre
     y se usan los datos iniciales; los errores de disco (OSError) se informan sin
     detener el programa.
  * registrar_evento() agrega lineas al historial con open(..., "a") y leer_historial()
    las recupera con open(..., "r").

Las listas se actualizan "en el lugar" (lista[:] = ...), de modo que todos los modulos
que ya importaron 'servicios' o 'usuarios' ven los datos cargados.
========================================================================================
"""

import json
import os
from datetime import datetime

import data.database as db

# Rutas de los archivos de datos, relativas a la carpeta del proyecto
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(CARPETA_PROYECTO, "datos")
RUTA_DATOS = os.path.join(CARPETA_DATOS, "ypri_datos.json")
RUTA_HISTORIAL = os.path.join(CARPETA_DATOS, "historial_operaciones.txt")

# Colecciones que se guardan. Tupla inmutable con los nombres de las variables de database.py
COLECCIONES = ("usuarios", "servicios", "contratos", "calificaciones",
               "matriz_ventas_semanales", "matriz_ventas_ciudades")


def obtener_estado_actual():
    """Funcion con return: arma un diccionario con todas las colecciones del sistema."""
    estado = {}
    for nombre in COLECCIONES:
        estado[nombre] = getattr(db, nombre)
    return estado


def guardar_datos(ruta=RUTA_DATOS):
    """
    Guarda toda la informacion del sistema en un archivo JSON.
    Retorna True si se guardo y False si hubo un error de escritura.
    """
    contenido = {
        "guardado_en": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "datos": obtener_estado_actual(),
    }
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        # Modo "w": crea el archivo o reemplaza su contenido anterior
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=2)
        return True
    except OSError as error:
        print(f"[!] No se pudo guardar el archivo de datos: {error}")
        return False


def cargar_datos(ruta=RUTA_DATOS):
    """
    Lee el archivo de datos y reemplaza el contenido de las colecciones en memoria.
    Retorna un texto que describe el resultado: 'cargado', 'nuevo' o 'danado'.
    """
    try:
        # Modo "r": lee un archivo existente
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
        datos = contenido["datos"]
        for nombre in COLECCIONES:
            if nombre in datos and isinstance(datos[nombre], list):
                lista_en_memoria = getattr(db, nombre)
                lista_en_memoria[:] = datos[nombre]
        return "cargado"
    except FileNotFoundError:
        # Primera ejecucion: se crea el archivo con los datos iniciales del sistema
        guardar_datos(ruta)
        return "nuevo"
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        respaldo = ruta + ".danado"
        print(f"[!] El archivo de datos esta danado ({error.__class__.__name__}).")
        try:
            os.replace(ruta, respaldo)
            print(f"    Se guardo una copia en '{os.path.basename(respaldo)}' y se usan los datos iniciales.")
        except OSError:
            pass
        guardar_datos(ruta)
        return "danado"
    except OSError as error:
        print(f"[!] No se pudo leer el archivo de datos: {error}. Se usan los datos iniciales.")
        return "danado"


def registrar_evento(descripcion, ruta=RUTA_HISTORIAL):
    """Procedimiento: agrega una linea al historial sin borrar las anteriores (modo "a")."""
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | {descripcion}\n")
    except OSError as error:
        print(f"[!] No se pudo escribir en el historial: {error}")


def leer_historial(ruta=RUTA_HISTORIAL, ultimas=15):
    """Funcion con return: devuelve las ultimas lineas del historial (lista vacia si no existe)."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = [linea.strip() for linea in archivo if linea.strip()]
        return lineas[-ultimas:]
    except FileNotFoundError:
        return []


def mostrar_historial():
    """Procedimiento: imprime el historial de operaciones guardado en archivo."""
    lineas = leer_historial()
    if len(lineas) == 0:
        print("  [i] Todavia no hay operaciones registradas en el historial.")
        return
    print(f"  Ultimas {len(lineas)} operaciones ({os.path.basename(RUTA_HISTORIAL)}):")
    for linea in lineas:
        print(f"   {linea}")
