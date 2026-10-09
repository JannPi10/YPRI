"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Punto de Entrada Principal (CLI y Menus Interactivos por Rol)
========================================================================================
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos
Integrantes: Jann Pierre Ortiz Zambrano y Josue David Rincon Palomino
Institucion: Fundacion de Estudios Superiores Comfanorte (FESC) - 2026
========================================================================================
"""

import sys
from core.validaciones import (
    separador,
    mostrar_encabezado,
    pedir_sn,
)
from data.database import get_sesion_actual
from modules.auth import login, cerrar_sesion, registrar_usuario
from modules.servicios import (
    listar_servicios,
    ver_detalle_servicio,
    publicar_servicio,
    modificar_servicio,
)
from modules.contratos import (
    solicitar_servicio,
    ver_mis_contratos,
    actualizar_estado_contrato,
)
from modules.calificaciones import calificar_servicio
from modules.admin import listar_usuarios, ver_estadisticas


def menu_cliente():
    """Menu interactivo del ciclo while para usuarios con rol 'cliente'."""
    while True:
        usuario = get_sesion_actual()
        if not usuario:
            break

        mostrar_encabezado(f"MENU CLIENTE — {usuario['nombre']}")
        print()
        print("  1. Ver catalogo de servicios")
        print("  2. Ver detalle de un servicio")
        print("  3. Solicitar servicio (cotizacion y contrato)")
        print("  4. Ver mis contratos")
        print("  5. Calificar un servicio completado")
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-5): ").strip()

        if opcion == "1":
            resp_filtro = pedir_sn("  ¿Filtrar solo con disponibilidad inmediata? (s/n): ")
            listar_servicios(solo_disponibles=(resp_filtro == "s"))
        elif opcion == "2":
            ver_detalle_servicio()
        elif opcion == "3":
            solicitar_servicio()
        elif opcion == "4":
            ver_mis_contratos()
        elif opcion == "5":
            calificar_servicio()
        elif opcion == "0":
            cerrar_sesion()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 5.")

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
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-5): ").strip()

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
        elif opcion == "0":
            cerrar_sesion()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 5.")

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
        print("  5. Ver reporte de metricas y estadisticas")
        print("  6. Modificar informacion de un servicio")
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-6): ").strip()

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
            modificar_servicio()
        elif opcion == "0":
            cerrar_sesion()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 6.")

        input("\n  Presione Enter para continuar...")
        print()


def main():
    """
    Punto de entrada principal.
    Mantiene el ciclo while global hasta que el usuario elija salir del programa.
    """
    while True:
        mostrar_encabezado("BIENVENIDO A YPRI")
        print()
        print("  1. Iniciar sesion")
        print("  2. Registrarse como nuevo usuario")
        print("  0. Salir")
        separador()

        opcion = input("  Seleccione una opcion (0-2): ").strip()

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
        elif opcion == "0":
            print("\n  Gracias por utilizar YPRI.")
            print("  Conectando hogares con profesionales de confianza.")
            print()
            break
        else:
            print("\n[!] Opcion invalida. Ingrese 1, 2 o 0.")

        print()


if __name__ == "__main__":
    main()
