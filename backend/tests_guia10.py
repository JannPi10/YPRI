"""
========================================================================================
SUITE DE PRUEBAS AUTOMATIZADAS — GUÍA DE APRENDIZAJE N.º 10
Subalgoritmos en Python: Funciones, Procedimientos, Lambdas y Modularización
========================================================================================
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos
Institución: Fundación de Estudios Superiores Comfanorte (FESC) - 2026
Integrantes: Jann Pierre Ortiz Zambrano y Josué David Rincón Palomino
========================================================================================
"""

import sys
import os
import unittest
import io
from contextlib import redirect_stdout

# Configurar ruta del backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.subalgoritmos import (
    calcular_liquidacion_contrato,
    calcular_comision_plataforma,
    calcular_promedio_calificacion,
    calcular_metricas_prestador,
    calcular_resumen_estadistico,
    mostrar_recibo_liquidacion,
    mostrar_ficha_tecnica_servicio,
    mostrar_tarjeta_rendimiento_prestador,
    calcular_descuento_lambda,
    calcular_iva_lambda,
    formatear_cop_lambda,
    ordenar_servicios_por_tarifa,
    ordenar_servicios_por_rating,
    modificar_numero_prueba,
    modificar_cadena_prueba,
    agregar_elemento_lista_prueba,
    actualizar_campo_diccionario_prueba,
)
import ejercicio_practico_guia10 as ep
from data.database import servicios, contratos, calificaciones


class TestGuia10Subalgoritmos(unittest.TestCase):
    """Pruebas unitarias de cumplimiento de la Guía 10."""

    # ====================================================================================
    # PRUEBA SECCIÓN 2: EJERCICIO PRÁCTICO GUIADO
    # ====================================================================================
    def test_01_ejercicio_practico_seccion2(self):
        """Verifica las funciones del Sistema de Inventario de la Sección 2."""
        # 1. Función con return calcular_subtotal
        subtotal = ep.calcular_subtotal(45000, 3)
        self.assertEqual(subtotal, 135000)

        # 2. Total del inventario
        ep.productos.clear()
        ep.productos.append({"codigo": "P1", "nombre": "Item 1", "precio": 100.0, "cantidad": 2})
        ep.productos.append({"codigo": "P2", "nombre": "Item 2", "precio": 200.0, "cantidad": 3})
        total_inv = ep.calcular_total_inventario()
        self.assertEqual(total_inv, 800.0)

        # 3. Ordenamiento lambda por precio
        ordenados = sorted(ep.productos, key=lambda p: p["precio"])
        self.assertEqual(ordenados[0]["codigo"], "P1")
        self.assertEqual(ordenados[1]["codigo"], "P2")

    # ====================================================================================
    # PRUEBA ACTIVIDAD 2: FUNCIONES CON RETURN Y PARÁMETROS
    # ====================================================================================
    def test_02_funciones_con_return_liquidacion(self):
        """Verifica la función calcular_liquidacion_contrato."""
        tarifa = 50000.0
        horas = 4
        descuento = 10.0
        tasa_iva = 0.19

        res = calcular_liquidacion_contrato(tarifa, horas, descuento_pct=descuento, tasa_iva=tasa_iva)
        self.assertEqual(res["subtotal_bruto"], 200000.0)
        self.assertEqual(res["monto_descuento"], 20000.0)
        self.assertEqual(res["subtotal_neto"], 180000.0)
        self.assertEqual(res["monto_iva"], 34200.0)
        self.assertEqual(res["total_pagar"], 214200.0)

        # Validación defensiva de parámetros inválidos
        with self.assertRaises(ValueError):
            calcular_liquidacion_contrato(-100, 2)
        with self.assertRaises(ValueError):
            calcular_liquidacion_contrato(50000, 0)
        with self.assertRaises(ValueError):
            calcular_liquidacion_contrato(50000, 2, descuento_pct=-5)

    def test_03_funciones_con_return_comision(self):
        """Verifica la función calcular_comision_plataforma."""
        total = 200000.0
        com = calcular_comision_plataforma(total, porcentaje_comision=0.10, retencion_pct=0.04)

        self.assertEqual(com["comision_ypri"], 20000.0)
        self.assertEqual(com["retencion_fuente"], 8000.0)
        self.assertEqual(com["pago_neto_prestador"], 172000.0)

    def test_04_funciones_con_return_promedio_rating(self):
        """Verifica el recálculo ponderado del rating promedio."""
        # 4 evaluaciones previas con promedio 4.0; nueva calificación de 5.0 -> (16 + 5) / 5 = 4.2
        nuevo_prom = calcular_promedio_calificacion(4.0, 5, 5.0)
        self.assertEqual(nuevo_prom, 4.2)

        # Caso primera evaluación
        primera = calcular_promedio_calificacion(0.0, 1, 4.8)
        self.assertEqual(primera, 4.8)

        # Fuera de rango
        with self.assertRaises(ValueError):
            calcular_promedio_calificacion(4.0, 2, 6.0)

    def test_05_funciones_con_return_estadisticas_vector(self):
        """Verifica la función calcular_resumen_estadistico."""
        datos = [10.0, 20.0, 30.0, 40.0]
        st = calcular_resumen_estadistico(datos)
        self.assertEqual(st["cantidad"], 4)
        self.assertEqual(st["suma"], 100.0)
        self.assertEqual(st["promedio"], 25.0)
        self.assertEqual(st["minimo"], 10.0)
        self.assertEqual(st["maximo"], 40.0)

    # ====================================================================================
    # PRUEBA ACTIVIDAD 3: PROCEDIMIENTOS (INTERACCIÓN SIN RETURN)
    # ====================================================================================
    def test_06_procedimientos_interaccion(self):
        """Verifica que los procedimientos se ejecuten correctamente sin retornar valores."""
        f = io.StringIO()
        with redirect_stdout(f):
            s = servicios[0]
            mostrar_ficha_tecnica_servicio(s)
            liq = calcular_liquidacion_contrato(s["tarifa_hora"], 2)
            ret_recibo = mostrar_recibo_liquidacion(liq, s)
            mostrar_tarjeta_rendimiento_prestador("Prestador Demo", {
                "total_contratos": 5, "contratos_completados": 4, "tasa_cumplimiento_pct": 80.0,
                "rating_promedio": 4.8, "ingresos_brutos": 400000.0, "comision_retenida": 40000.0,
                "ingresos_netos": 360000.0, "total_calificaciones": 4
            })

        output = f.getvalue()
        # Verificar que sean procedimientos (retornan None)
        self.assertIsNone(ret_recibo)
        # Verificar que hayan generado la salida esperada en consola
        self.assertIn("RECIBO DE COTIZACIÓN Y LIQUIDACIÓN", output)
        self.assertIn("FICHA TÉCNICA", output)
        self.assertIn("PANEL DE RENDIMIENTO OPERATIVO", output)

    # ====================================================================================
    # PRUEBA ACTIVIDAD 4: FUNCIONES LAMBDA
    # ====================================================================================
    def test_07_funciones_lambda(self):
        """Verifica el uso de expresiones lambda para cálculos y ordenamientos."""
        # Cálculo aritmético
        self.assertEqual(calcular_descuento_lambda(200000, 15), 30000.0)
        self.assertEqual(calcular_iva_lambda(100000, 0.19), 19000.0)
        self.assertEqual(formatear_cop_lambda(150000), "$150,000 COP")

        # Ordenamiento ascendente por tarifa
        ord_asc = ordenar_servicios_por_tarifa(servicios, descendente=False)
        self.assertTrue(ord_asc[0]["tarifa_hora"] <= ord_asc[-1]["tarifa_hora"])

        # Ordenamiento descendente por rating
        ord_rat = ordenar_servicios_por_rating(servicios)
        self.assertTrue(ord_rat[0]["calificacion"] >= ord_rat[-1]["calificacion"])

    # ====================================================================================
    # PRUEBA ACTIVIDAD 5: PASO DE ARGUMENTOS (VALOR VS REFERENCIA)
    # ====================================================================================
    def test_08_paso_argumentos_inmutables_vs_mutables(self):
        """Demuestra rigurosamente la diferencia entre mutables e inmutables."""
        # 1. Inmutable (float): Simula paso por valor
        num_original = 50000.0
        ret_num = modificar_numero_prueba(num_original)
        self.assertEqual(num_original, 50000.0, "El número original NO debe cambiar.")
        self.assertEqual(ret_num, 60000.0)

        # 2. Inmutable (str): Simula paso por valor
        cadena_orig = "Cúcuta"
        ret_cad = modificar_cadena_prueba(cadena_orig)
        self.assertEqual(cadena_orig, "Cúcuta", "La cadena original NO debe cambiar.")

        # 3. Mutable (list): Paso por referencia (in-place)
        lista_orig = ["A", "B"]
        agregar_elemento_lista_prueba(lista_orig, "C")
        self.assertEqual(lista_orig, ["A", "B", "C"], "La lista original SÍ debe modificarse in-place.")

        # 4. Mutable (dict): Paso por referencia (in-place)
        dict_orig = {"rol": "cliente", "puntos": 10}
        actualizar_campo_diccionario_prueba(dict_orig, "rol", "admin")
        self.assertEqual(dict_orig["rol"], "admin", "El diccionario original SÍ debe modificarse in-place.")

    # ====================================================================================
    # PRUEBA ACTIVIDAD 6: MODULARIZACIÓN E INTEGRACIÓN EN YPRI
    # ====================================================================================
    def test_09_modularizacion_y_conservacion_de_funcionalidad(self):
        """Comprueba que todos los módulos cooperen sin dependencias circulares."""
        import core.validaciones as val
        import core.constantes as const
        import modules.auth as auth
        import modules.servicios as srv
        import modules.contratos as cnt
        import modules.calificaciones as cal
        import modules.matrices as mat
        import modules.admin as adm

        self.assertIsNotNone(val)
        self.assertIsNotNone(const)
        self.assertIsNotNone(auth)
        self.assertIsNotNone(srv)
        self.assertIsNotNone(cnt)
        self.assertIsNotNone(cal)
        self.assertIsNotNone(mat)
        self.assertIsNotNone(adm)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("   EJECUCIÓN DE PRUEBAS AUTOMATIZADAS — GUÍA 10 (SUBALGORITMOS)")
    print("=" * 70 + "\n")
    unittest.main(verbosity=2)
