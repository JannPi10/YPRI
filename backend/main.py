"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Punto de Entrada Principal (CLI y Menus Interactivos por Rol)
========================================================================================
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos
Integrantes: Jann Pierre Ortiz Zambrano y Josue David Rincon Palomino
Institucion: Fundacion de Estudios Superiores Comfanorte (FESC) - 2026
========================================================================================
DOCUMENTACION DE TEMAS POR SEMANAS:
- [SEMANAS 5 Y 6]: Estructura general basada en bucles 'while True', sentencias 'break',
  'continue' y menus interactivos con navegacion por teclado.
- [SEMANA 7 - TUPLAS, CADENAS Y DICCIONARIOS]: Control de sesion autenticada en memoria,
  normalizacion de texto (.strip(), .lower()) y validaciones defensivas.
- [SEMANA 8 - VECTORES]: Menu de catalogo avanzado (ordenamientos asc/desc, busqueda
  secuencial y por atributos, reto de integracion con min/max y ranking).
- [SEMANA 9 - MATRICES EN PYTHON]: Nuevo modulo interactivo para la creacion, recorrido,
  consulta, modificacion y operaciones matematicas sobre matrices bidimensionales (Guia 9).
- [SEMANA 10 - SUBALGORITMOS EN PYTHON]: Modularizacion con funciones puras con return,
  procedimientos de presentacion, funciones lambda y paso de argumentos (Guia 10).
- [SEMANA 11 - ARCHIVOS, EXCEL Y POO]: los datos se cargan desde 'datos/ypri_datos.json'
  al iniciar y se guardan al cerrar sesion y al salir (modules/persistencia.py); los
  menus de prestador y administrador abren el submenu de Excel (modules/reportes_excel.py)
  y la opcion de eliminar servicios (.remove()). Las clases estan en la carpeta models/.
========================================================================================
"""

import atexit
import sys
import os

# Asegurar resolucion de modulos internos independientemente de la ruta de ejecucion
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.validaciones import (
    separador,
    mostrar_encabezado,
    pedir_sn,
)
from data.database import get_sesion_actual
from modules.auth import login, cerrar_sesion as cerrar_sesion_base, registrar_usuario
from modules.persistencia import cargar_datos, guardar_datos, registrar_evento, RUTA_DATOS
from modules.reportes_excel import menu_archivos_excel
from modules.servicios import (
    listar_servicios,
    ver_detalle_servicio,
    publicar_servicio,
    modificar_servicio,
    eliminar_servicio,
    menu_catalogo_avanzado,
)
from modules.contratos import (
    solicitar_servicio,
    ver_mis_contratos,
    actualizar_estado_contrato,
)
from modules.calificaciones import calificar_servicio
from modules.admin import (
    listar_usuarios,
    ver_estadisticas,
    ver_reporte_matricial_admin,
)
from modules.matrices import menu_matrices_interactivo
from modules.subalgoritmos import (
    menu_subalgoritmos_interactivo,
    mostrar_tarjeta_rendimiento_prestador,
    calcular_metricas_prestador,
)

from modules.geolocalizacion import menu_geolocalizacion_interactivo


def cerrar_sesion():
    """Cierra la sesion y guarda los datos en archivo (Guia 11)."""
    usuario = get_sesion_actual()
    if usuario:
        registrar_evento(f"Cierre de sesion: {usuario['correo']}")
    guardar_datos()
    cerrar_sesion_base()

def menu_cliente():
    """Menu interactivo del ciclo while para usuarios con rol 'cliente'."""
    while True:
        usuario = get_sesion_actual()
        if not usuario:
            break

        mostrar_encabezado(f"MENU CLIENTE — {usuario['nombre']}")
        print()
        print("  1. Catalogo, busqueda y ordenamiento de servicios (Guia 8)")
        print("  2. Ver detalle de un servicio por codigo")
        print("  3. Solicitar servicio (cotizacion y contrato)")
        print("  4. Ver mis contratos")
        print("  5. Calificar un servicio completado")
        print("  6. Explorar Matrices Analiticas de YPRI (Guia 9)")
        print("  7. Explorador de Subalgoritmos y Cotizador Avanzado (Guia 10)")
        print("  8. Profesionales cerca de mi (Geolocalizacion)")
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-8): ").strip()

        if opcion == "1":
            menu_catalogo_avanzado()
        elif opcion == "2":
            ver_detalle_servicio()
        elif opcion == "3":
            solicitar_servicio()
        elif opcion == "4":
            ver_mis_contratos()
        elif opcion == "5":
            calificar_servicio()
        elif opcion == "6":
            menu_matrices_interactivo()
        elif opcion == "7":
            menu_subalgoritmos_interactivo()
        elif opcion == "8":
            menu_geolocalizacion_interactivo()
        elif opcion == "0":
            cerrar_sesion()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 8.")

        input("\n  Presione Enter para continuar...")
        print()


def menu_prestador():
    """Menu interactivo del ciclo while para usuarios con rol 'prestador'."""
    while True:
        usuario = get_sesion_actual()
        if not usuario:
            break

        mostrar_encabezado(f"MENU PRESTADOR — {usuario['nombre']}")
        print()
        print("  1. Ver catalogo de servicios en mi ciudad")
        print("  2. Publicar nuevo servicio")
        print("  3. Modificar un servicio propio")
        print("  4. Ver contratos asociados")
        print("  5. Actualizar estado de contrato")
        print("  6. Explorar Matrices de Facturacion (Guia 9)")
        print("  7. Tarjeta de Rendimiento Operativo y Comisiones (Guia 10)")
        print("  8. Eliminar un servicio propio")
        print("  9. Archivos y reportes Excel: exportar, importar, respaldo (Guia 11)")
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-9): ").strip()

        if opcion == "1":
            listar_servicios(filtro_ciudad=usuario["ciudad"])
        elif opcion == "2":
            publicar_servicio()
        elif opcion == "3":
            modificar_servicio()
        elif opcion == "4":
            ver_mis_contratos()
        elif opcion == "5":
            actualizar_estado_contrato()
        elif opcion == "6":
            menu_matrices_interactivo()
        elif opcion == "7":
            from data.database import contratos, calificaciones
            metricas = calcular_metricas_prestador(usuario["id"], contratos, calificaciones)
            mostrar_tarjeta_rendimiento_prestador(usuario["nombre"], metricas)
        elif opcion == "8":
            eliminar_servicio()
        elif opcion == "9":
            menu_archivos_excel()
            continue
        elif opcion == "0":
            cerrar_sesion()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 9.")

        input("\n  Presione Enter para continuar...")
        print()


def menu_admin():
    """Menu interactivo del ciclo while para usuarios con rol 'admin'."""
    while True:
        usuario = get_sesion_actual()
        if not usuario:
            break

        mostrar_encabezado(f"PANEL DE ADMINISTRACION — {usuario['nombre']}")
        print()
        print("  1. Listar todos los usuarios del sistema")
        print("  2. Ver catalogo general de servicios")
        print("  3. Ver todos los contratos")
        print("  4. Actualizar estado de contrato")
        print("  5. Ver reporte consolidado de metricas y estadisticas")
        print("  6. Modulo de Matrices en Python (Guia 9: Ventas, Especiales, Ejercicio)")
        print("  7. Auditoria visual de matrices completas (Admin)")
        print("  8. Modificar informacion de un servicio")
        print("  9. Modulo de Subalgoritmos y Metricas Modulares (Guia 10)")
        print(" 10. Eliminar un servicio del catalogo")
        print(" 11. Archivos y reportes Excel: exportar, importar, respaldo (Guia 11)")
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-11): ").strip()

        if opcion == "1":
            listar_usuarios()
        elif opcion == "2":
            listar_servicios()
        elif opcion == "3":
            ver_mis_contratos()
        elif opcion == "4":
            actualizar_estado_contrato()
        elif opcion == "5":
            ver_estadisticas()
        elif opcion == "6":
            menu_matrices_interactivo()
        elif opcion == "7":
            ver_reporte_matricial_admin()
        elif opcion == "8":
            modificar_servicio()
        elif opcion == "9":
            menu_subalgoritmos_interactivo()
        elif opcion == "10":
            eliminar_servicio()
        elif opcion == "11":
            menu_archivos_excel()
            continue
        elif opcion == "0":
            cerrar_sesion()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 11.")

        input("\n  Presione Enter para continuar...")
        print()


def main():
    """
    Punto de entrada principal.
    Permite operar en modo consola o abrir la interfaz grafica moderna (GUI).
    """
    # Consola en UTF-8 para que tildes y simbolos se vean bien en Windows
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    # GUIA 11 - ACTIVIDAD 1: recuperar la informacion guardada en la ejecucion anterior
    estado = cargar_datos()
    if estado == "cargado":
        print(f"[i] Datos recuperados desde {os.path.relpath(RUTA_DATOS)}")
    elif estado == "nuevo":
        print(f"[i] Primera ejecucion: se creo el archivo {os.path.relpath(RUTA_DATOS)}")
    # Respaldo final aunque el programa se cierre con Ctrl+C
    atexit.register(guardar_datos)

    if len(sys.argv) > 1 and ("--gui" in sys.argv or "-g" in sys.argv):
        from app_gui import main_gui
        main_gui()
        return

    while True:
        mostrar_encabezado("BIENVENIDO A YPRI")
        print()
        print("  1. Iniciar sesion (Modo Consola)")
        print("  2. Registrarse como nuevo usuario")
        print("  3. Matrices de facturacion y demanda de YPRI (Guia 9)")
        print("  4. Subalgoritmos y cotizador de YPRI (Guia 10)")
        print("  5. Abrir Interfaz Grafica de Escritorio (Tkinter)")
        print("  0. Salir")
        separador()

        opcion = input("  Seleccione una opcion (0-5): ").strip()

        if opcion == "1":
            if login():
                usuario = get_sesion_actual()
                if usuario["rol"] == "cliente":
                    menu_cliente()
                elif usuario["rol"] == "prestador":
                    menu_prestador()
                elif usuario["rol"] == "admin":
                    menu_admin()
        elif opcion == "2":
            registrar_usuario()
            input("\n  Presione Enter para continuar...")
        elif opcion == "3":
            menu_matrices_interactivo()
        elif opcion == "4":
            menu_subalgoritmos_interactivo()
        elif opcion == "5":
            print("\n  [i] Iniciando interfaz grafica de escritorio de YPRI...")
            from app_gui import main_gui
            main_gui()
        elif opcion == "0":
            if guardar_datos():
                print(f"\n  [OK] Datos guardados en {os.path.relpath(RUTA_DATOS)}")
            print("\n  Gracias por utilizar YPRI.")
            print("  Conectando hogares con profesionales de confianza.")
            print()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 5.")

        print()


if __name__ == "__main__":
    main()
