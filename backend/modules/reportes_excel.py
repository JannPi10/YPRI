"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Reportes e Importacion con Excel usando openpyxl (Guia 11 - Actividad 2)
========================================================================================
[GUIA 11 - ACTIVIDAD 2 - INTEGRACION CON EXCEL]:
  1. exportar_reporte_excel(): genera 'reportes/reporte_ypri.xlsx' con tres hojas
     (Servicios, Contratos y Facturacion semanal).
  2. Cada hoja tiene encabezados que identifican los datos (fila 1 en negrilla).
  3. importar_servicios_excel(): lee servicios desde un archivo .xlsx.
  4. Los servicios importados se agregan al vector 'servicios', es decir, quedan en el
     catalogo, en las busquedas y en el ordenamiento (funcionalidades de la Guia 8).
     Cada fila se valida con los setters de la clase Servicio y los duplicados se
     detectan con el operador == sobrescrito (__eq__).
  * crear_plantilla_importacion(): genera 'datos/plantilla_servicios.xlsx' de ejemplo.
========================================================================================
"""

import os

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils.exceptions import InvalidFileException

from core.constantes import CATEGORIAS_MATRIZ, DIAS_SEMANA_MATRIZ
from core.validaciones import mostrar_encabezado, separador
from data.database import servicios, contratos, matriz_ventas_semanales, get_sesion_actual
from models.factura import Factura
from models.servicio import Servicio
from modules.matrices import calcular_totales_filas, calcular_totales_columnas, calcular_total_general
from modules.persistencia import CARPETA_PROYECTO, CARPETA_DATOS, registrar_evento, guardar_datos

CARPETA_REPORTES = os.path.join(CARPETA_PROYECTO, "reportes")
RUTA_REPORTE = os.path.join(CARPETA_REPORTES, "reporte_ypri.xlsx")
RUTA_PLANTILLA = os.path.join(CARPETA_DATOS, "plantilla_servicios.xlsx")

# Encabezados de la hoja de servicios. Tambien son las columnas que se esperan al importar.
ENCABEZADOS_SERVICIOS = ("Codigo", "Categoria", "Prestador", "Descripcion",
                         "Tarifa por hora (COP)", "Ciudad", "Zona", "Disponible", "Calificacion")
ENCABEZADOS_CONTRATOS = ("Contrato", "Cliente", "Servicio", "Horas", "Estado",
                         "Subtotal (COP)", "IVA (COP)", "Total (COP)")

ESTILO_ENCABEZADO = Font(bold=True, color="FFFFFF")
RELLENO_ENCABEZADO = PatternFill("solid", fgColor="1E2A4A")


def _escribir_encabezados(hoja, encabezados):
    """Procedimiento auxiliar: escribe la fila de encabezados con formato."""
    hoja.append(list(encabezados))
    for celda in hoja[1]:
        celda.font = ESTILO_ENCABEZADO
        celda.fill = RELLENO_ENCABEZADO
    hoja.freeze_panes = "A2"


def _ajustar_ancho_columnas(hoja):
    """Procedimiento auxiliar: ensancha cada columna segun su texto mas largo."""
    for columna in hoja.columns:
        largo = max(len(str(celda.value)) if celda.value is not None else 0 for celda in columna)
        hoja.column_dimensions[columna[0].column_letter].width = min(largo + 2, 60)


def exportar_reporte_excel(ruta=RUTA_REPORTE, lista_servicios=None, lista_contratos=None, matriz=None):
    """
    Exporta la informacion del proyecto a un libro de Excel.
    Retorna la ruta del archivo generado.
    """
    lista_servicios = servicios if lista_servicios is None else lista_servicios
    lista_contratos = contratos if lista_contratos is None else lista_contratos
    matriz = matriz_ventas_semanales if matriz is None else matriz

    libro = Workbook()

    # Hoja 1: catalogo de servicios
    hoja_servicios = libro.active
    hoja_servicios.title = "Servicios"
    _escribir_encabezados(hoja_servicios, ENCABEZADOS_SERVICIOS)
    for s in lista_servicios:
        hoja_servicios.append([
            s["codigo"], s["categoria"], s["prestador_nombre"], s["descripcion"],
            s["tarifa_hora"], s.get("ciudad", ""), s.get("zona", ""),
            "Si" if s["disponible"] else "No", s.get("calificacion", 0),
        ])

    # Hoja 2: contratos con su factura (clase Factura y operador + sobrescrito)
    hoja_contratos = libro.create_sheet("Contratos")
    _escribir_encabezados(hoja_contratos, ENCABEZADOS_CONTRATOS)
    consolidado = Factura.vacia()
    for c in lista_contratos:
        factura = Factura.desde_contrato(c)
        consolidado = consolidado + factura
        hoja_contratos.append([
            c["id"], c["cliente_nombre"], c["servicio_nombre"], c["horas"], c["estado"],
            factura.subtotal, factura.iva, factura.total,
        ])
    hoja_contratos.append(["TOTAL", "", "", "", f"{consolidado.cantidad_contratos} contrato(s)",
                           consolidado.subtotal, consolidado.iva, consolidado.total])
    for celda in hoja_contratos[hoja_contratos.max_row]:
        celda.font = Font(bold=True)

    # Hoja 3: matriz de facturacion semanal (Guia 9) con totales por fila y columna
    hoja_matriz = libro.create_sheet("Facturacion semanal")
    _escribir_encabezados(hoja_matriz, ("Categoria",) + DIAS_SEMANA_MATRIZ + ("Total",))
    totales_filas = calcular_totales_filas(matriz)
    for i in range(len(matriz)):
        hoja_matriz.append([CATEGORIAS_MATRIZ[i]] + matriz[i] + [totales_filas[i]])
    hoja_matriz.append(["Total por dia"] + calcular_totales_columnas(matriz) + [calcular_total_general(matriz)])
    for celda in hoja_matriz[hoja_matriz.max_row]:
        celda.font = Font(bold=True)

    for hoja in libro.worksheets:
        _ajustar_ancho_columnas(hoja)

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    libro.save(ruta)
    return ruta


def crear_plantilla_importacion(ruta=RUTA_PLANTILLA):
    """
    Crea un Excel de ejemplo con servicios para importar. La ultima fila tiene una
    tarifa invalida a proposito, para mostrar que la validacion la rechaza.
    """
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Servicios"
    _escribir_encabezados(hoja, ENCABEZADOS_SERVICIOS)
    hoja.append(["SERV-20", "Electricidad", "Luis Ortega", "Revision de tableros y cambio de breakers",
                 40000, "Cucuta", "San Luis", "Si", 4.6])
    hoja.append(["SERV-21", "Plomeria", "Diana Paez", "Destape de canerias y arreglo de fugas de agua",
                 32000, "Cucuta", "El Llano", "Si", 4.4])
    hoja.append(["SERV-22", "Limpieza", "Rosa Medina", "Limpieza de oficinas y locales comerciales",
                 27000, "Cucuta", "Centro", "No", 4.8])
    hoja.append(["SERV-23", "Cerrajeria", "Pedro Vera", "Copia de llaves y cambio de guardas",
                 5000, "Cucuta", "Atalaya", "Si", 4.0])
    _ajustar_ancho_columnas(hoja)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    libro.save(ruta)
    return ruta


def importar_servicios_excel(ruta, lista_servicios=None, prestador_id="USR-IMPORT"):
    """
    Lee servicios desde un archivo Excel y agrega al catalogo los que sean validos.
    Retorna un diccionario con las listas 'importados' (codigos) y 'rechazados'
    (fila y motivo). Lanza FileNotFoundError o ValueError si el archivo no sirve.
    """
    lista_servicios = servicios if lista_servicios is None else lista_servicios
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo '{ruta}'.")
    try:
        libro = load_workbook(ruta, read_only=True, data_only=True)
    except (InvalidFileException, OSError, KeyError) as error:
        raise ValueError(f"El archivo no es un Excel valido (.xlsx): {error}")

    hoja = libro.active
    filas = list(hoja.iter_rows(values_only=True))
    libro.close()
    if len(filas) == 0:
        raise ValueError("El archivo de Excel esta vacio.")

    encabezados = [str(valor).strip() if valor is not None else "" for valor in filas[0]]
    faltantes = [col for col in ENCABEZADOS_SERVICIOS if col not in encabezados]
    if faltantes:
        raise ValueError(f"Faltan columnas en el Excel: {', '.join(faltantes)}.")
    posicion = {nombre: encabezados.index(nombre) for nombre in ENCABEZADOS_SERVICIOS}

    # Objetos de los servicios existentes, para detectar duplicados con ==
    existentes = [Servicio.desde_diccionario(s) for s in lista_servicios]
    resultado = {"importados": [], "rechazados": []}

    for numero_fila, fila in enumerate(filas[1:], start=2):
        if all(valor is None for valor in fila):
            continue  # fila vacia: se ignora
        valor = lambda columna: fila[posicion[columna]]  # acceso a una celda por encabezado
        try:
            nuevo = Servicio(
                codigo=valor("Codigo"),
                prestador_id=prestador_id,
                prestador_nombre=str(valor("Prestador") or "Sin nombre").strip(),
                categoria=valor("Categoria"),
                descripcion=valor("Descripcion"),
                tarifa_hora=valor("Tarifa por hora (COP)"),
                ciudad=valor("Ciudad") or "Cucuta",
                zona=str(valor("Zona") or "Centro").strip(),
                disponible=str(valor("Disponible") or "Si").strip().lower() in ("si", "sí", "true", "1"),
                calificacion=valor("Calificacion") or 5.0,
            )
        except (ValueError, TypeError) as error:
            resultado["rechazados"].append((numero_fila, str(error)))
            continue

        # Operador == sobrescrito: el servicio ya existe si tiene el mismo codigo
        if nuevo in existentes:
            resultado["rechazados"].append((numero_fila, f"El codigo {nuevo.codigo} ya existe en el catalogo."))
            continue

        lista_servicios.append(nuevo.a_diccionario())
        existentes.append(nuevo)
        resultado["importados"].append(nuevo.codigo)

    return resultado


# ========================================================================================
# MENU DE ARCHIVOS Y EXCEL (integrado en los menus de prestador y administrador)
# ========================================================================================

def accion_exportar_excel():
    """Procedimiento del menu: exporta el reporte y muestra donde quedo."""
    try:
        ruta = exportar_reporte_excel()
    except PermissionError:
        print("[!] No se pudo guardar el Excel. Cierre el archivo si lo tiene abierto en Excel e intente de nuevo.")
        return
    registrar_evento(f"Reporte Excel exportado: {os.path.basename(ruta)}")
    print(f"[OK] Reporte exportado: {ruta}")
    print(f"     Hojas: Servicios ({len(servicios)}), Contratos ({len(contratos)}), Facturacion semanal")


def accion_importar_excel():
    """Procedimiento del menu: importa servicios desde un Excel elegido por el usuario."""
    if not os.path.exists(RUTA_PLANTILLA):
        crear_plantilla_importacion()
    print(f"  Archivo de ejemplo: {RUTA_PLANTILLA}")
    ruta = input("  Ruta del Excel a importar (Enter para usar el de ejemplo): ").strip().strip('"')
    if ruta == "":
        ruta = RUTA_PLANTILLA

    usuario = get_sesion_actual()
    prestador_id = usuario["id"] if usuario and usuario["rol"] == "prestador" else "USR-IMPORT"
    try:
        resultado = importar_servicios_excel(ruta, prestador_id=prestador_id)
    except (FileNotFoundError, ValueError) as error:
        print(f"[!] {error}")
        return

    print(f"\n[OK] Servicios importados al catalogo: {len(resultado['importados'])}")
    for codigo in resultado["importados"]:
        print(f"     + {codigo}")
    if resultado["rechazados"]:
        print(f"[!] Filas rechazadas: {len(resultado['rechazados'])}")
        for numero_fila, motivo in resultado["rechazados"]:
            print(f"     Fila {numero_fila}: {motivo}")
    if resultado["importados"]:
        guardar_datos()
        registrar_evento(f"Importados desde Excel: {', '.join(resultado['importados'])}")
        print("     Ya aparecen en el catalogo, la busqueda y el ordenamiento de servicios.")


def menu_archivos_excel():
    """Submenu de la Guia 11: archivos de datos, historial y Excel."""
    from modules.persistencia import RUTA_DATOS, mostrar_historial
    while True:
        mostrar_encabezado("ARCHIVOS Y REPORTES EXCEL (Guia 11)")
        print()
        print("  1. Exportar reporte a Excel (servicios, contratos y facturacion)")
        print("  2. Importar servicios desde un archivo Excel")
        print("  3. Guardar ahora los datos en archivo")
        print("  4. Ver historial de operaciones guardado")
        print("  0. Volver")
        separador()
        opcion = input("  Seleccione una opcion (0-4): ").strip()

        if opcion == "1":
            accion_exportar_excel()
        elif opcion == "2":
            accion_importar_excel()
        elif opcion == "3":
            if guardar_datos():
                registrar_evento("Respaldo manual de datos")
                print(f"[OK] Datos guardados en {RUTA_DATOS}")
        elif opcion == "4":
            mostrar_historial()
        elif opcion == "0":
            break
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 4.")
            continue
        input("\n  Presione Enter para continuar...")
