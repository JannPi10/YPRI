"""
========================================================================================
SISTEMA YPRI - EJECUCION DE TODAS LAS PRUEBAS AUTOMATIZADAS
========================================================================================
Corre las cuatro suites de pruebas del proyecto y guarda el resultado completo en
'evidencias/resultado_pruebas.txt' como evidencia de funcionamiento.

  * tests_guia10.py          -> Subalgoritmos, modularizacion e integracion (Guias 5 a 10)
  * tests_geolocalizacion.py -> Distancias, cercania y seguimiento del prestador
  * tests_pedido_rapido.py   -> Palabras clave y pedido inmediato
  * tests_guia11.py          -> Archivos, Excel, clases, herencia y operadores (Guia 11)

Uso:  python ejecutar_pruebas.py
========================================================================================
"""

import io
import os
import sys
import unittest
from datetime import datetime

CARPETA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CARPETA)

SUITES = ("tests_guia10", "tests_geolocalizacion", "tests_pedido_rapido", "tests_guia11")
RUTA_EVIDENCIA = os.path.join(CARPETA, "evidencias", "resultado_pruebas.txt")


def ejecutar_suites():
    """Ejecuta cada suite y retorna (texto_del_reporte, total_pruebas, total_fallas)."""
    salida = io.StringIO()
    salida.write("=" * 78 + "\n")
    salida.write("  YPRI - RESULTADO DE LAS PRUEBAS AUTOMATIZADAS\n")
    salida.write(f"  Fecha de ejecucion: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    salida.write(f"  Python {sys.version.split()[0]}\n")
    salida.write("=" * 78 + "\n")

    total_pruebas = 0
    total_fallas = 0
    for nombre in SUITES:
        salida.write(f"\n### {nombre}.py\n")
        suite = unittest.defaultTestLoader.loadTestsFromName(nombre)
        resultado = unittest.TextTestRunner(stream=salida, verbosity=2).run(suite)
        total_pruebas += resultado.testsRun
        total_fallas += len(resultado.failures) + len(resultado.errors)

    salida.write("\n" + "=" * 78 + "\n")
    salida.write(f"  TOTAL: {total_pruebas} pruebas | {total_pruebas - total_fallas} correctas | "
                 f"{total_fallas} con fallas\n")
    salida.write("=" * 78 + "\n")
    return salida.getvalue(), total_pruebas, total_fallas


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    texto, pruebas, fallas = ejecutar_suites()
    print(texto)
    os.makedirs(os.path.dirname(RUTA_EVIDENCIA), exist_ok=True)
    with open(RUTA_EVIDENCIA, "w", encoding="utf-8") as archivo:
        archivo.write(texto)
    print(f"Evidencia guardada en: {RUTA_EVIDENCIA}")
    sys.exit(1 if fallas else 0)
