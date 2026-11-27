"""
========================================================================================
SUITE DE PRUEBAS AUTOMATIZADAS — GUIA 11 (ARCHIVOS, EXCEL Y POO)
Persistencia en archivos, Excel con openpyxl, clases, getters/setters, herencia y
sobrescritura de metodos y operadores, integradas con el resto de YPRI.
========================================================================================
Asignatura: Diseño Funcional | Unidad 3: Programacion Orientada a Objetos
Institución: Fundación de Estudios Superiores Comfanorte (FESC) - 2026
Integrantes: Jann Pierre Ortiz Zambrano y Josué David Rincón Palomino
========================================================================================
Ejecutar desde la carpeta del proyecto:  python tests_guia11.py
Las pruebas usan una carpeta temporal: no modifican los archivos reales de datos/.
"""

import copy
import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openpyxl import Workbook, load_workbook

import data.database as db
from models.factura import Factura
from models.servicio import Servicio
from models.usuario import Usuario, Cliente, Prestador, Administrador
from modules import persistencia
from modules.reportes_excel import (
    ENCABEZADOS_SERVICIOS,
    crear_plantilla_importacion,
    exportar_reporte_excel,
    importar_servicios_excel,
)
from modules.servicios import quitar_servicio_del_catalogo


def servicio_valido(**cambios):
    """Crea un objeto Servicio de prueba; 'cambios' reemplaza atributos."""
    datos = dict(codigo="SERV-90", prestador_id="USR-002", prestador_nombre="Carlos Gomez",
                 categoria="Electricidad", descripcion="Cambio de tomas e interruptores",
                 tarifa_hora=40000)
    datos.update(cambios)
    return Servicio(**datos)


class TestArchivos(unittest.TestCase):
    """Actividad 1: guardar, leer y recuperar datos; archivos inexistentes o danados."""

    def setUp(self):
        self.carpeta = tempfile.mkdtemp()
        self.ruta = os.path.join(self.carpeta, "ypri_datos.json")
        self.respaldo = {n: copy.deepcopy(getattr(db, n)) for n in persistencia.COLECCIONES}

    def tearDown(self):
        for nombre, valor in self.respaldo.items():
            getattr(db, nombre)[:] = valor
        shutil.rmtree(self.carpeta, ignore_errors=True)

    def test_guardar_y_recuperar_despues_de_reiniciar(self):
        db.servicios.append(servicio_valido().a_diccionario())
        self.assertTrue(persistencia.guardar_datos(self.ruta))
        # Simula cerrar el programa: se pierden los cambios en memoria
        db.servicios[:] = self.respaldo["servicios"]
        self.assertNotIn("SERV-90", [s["codigo"] for s in db.servicios])
        # Simula volver a ejecutar: se cargan desde el archivo
        self.assertEqual(persistencia.cargar_datos(self.ruta), "cargado")
        self.assertIn("SERV-90", [s["codigo"] for s in db.servicios])

    def test_archivo_inexistente_crea_uno_nuevo(self):
        self.assertFalse(os.path.exists(self.ruta))
        self.assertEqual(persistencia.cargar_datos(self.ruta), "nuevo")
        self.assertTrue(os.path.exists(self.ruta))

    def test_archivo_danado_no_detiene_el_programa(self):
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write("{esto no es json")
        with redirect_stdout(io.StringIO()):
            estado = persistencia.cargar_datos(self.ruta)
        self.assertEqual(estado, "danado")
        self.assertTrue(os.path.exists(self.ruta + ".danado"))
        self.assertEqual(len(db.usuarios), len(self.respaldo["usuarios"]))

    def test_historial_agrega_lineas_sin_borrar(self):
        ruta_historial = os.path.join(self.carpeta, "historial.txt")
        self.assertEqual(persistencia.leer_historial(ruta_historial), [])
        persistencia.registrar_evento("Primera operacion", ruta_historial)
        persistencia.registrar_evento("Segunda operacion", ruta_historial)
        lineas = persistencia.leer_historial(ruta_historial)
        self.assertEqual(len(lineas), 2)
        self.assertTrue(lineas[1].endswith("Segunda operacion"))


class TestExcel(unittest.TestCase):
    """Actividad 2: exportar con encabezados, leer e integrar al catalogo."""

    def setUp(self):
        self.carpeta = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.carpeta, ignore_errors=True)

    def test_exportar_con_encabezados_y_totales(self):
        ruta = exportar_reporte_excel(os.path.join(self.carpeta, "reporte.xlsx"))
        libro = load_workbook(ruta)
        self.assertEqual(libro.sheetnames, ["Servicios", "Contratos", "Facturacion semanal"])
        hoja = libro["Servicios"]
        self.assertEqual(tuple(c.value for c in hoja[1]), ENCABEZADOS_SERVICIOS)
        self.assertEqual(hoja.max_row, len(db.servicios) + 1)
        ultima_contratos = [c.value for c in libro["Contratos"][libro["Contratos"].max_row]]
        self.assertEqual(ultima_contratos[0], "TOTAL")
        self.assertAlmostEqual(ultima_contratos[-1], sum(c["total"] for c in db.contratos), places=2)
        libro.close()

    def test_importar_agrega_validos_y_rechaza_invalidos(self):
        ruta = crear_plantilla_importacion(os.path.join(self.carpeta, "plantilla.xlsx"))
        catalogo = copy.deepcopy(db.servicios)
        resultado = importar_servicios_excel(ruta, lista_servicios=catalogo)
        self.assertEqual(resultado["importados"], ["SERV-20", "SERV-21", "SERV-22"])
        self.assertEqual(len(resultado["rechazados"]), 1)  # fila con tarifa de $5.000
        self.assertEqual(len(catalogo), len(db.servicios) + 3)
        # Integracion: los importados se pueden buscar en el catalogo como cualquier servicio
        self.assertIn("Plomeria", [s["categoria"] for s in catalogo if s["codigo"] == "SERV-21"])

    def test_importar_dos_veces_no_duplica(self):
        ruta = crear_plantilla_importacion(os.path.join(self.carpeta, "plantilla.xlsx"))
        catalogo = copy.deepcopy(db.servicios)
        importar_servicios_excel(ruta, lista_servicios=catalogo)
        segundo = importar_servicios_excel(ruta, lista_servicios=catalogo)
        self.assertEqual(segundo["importados"], [])
        self.assertTrue(any("ya existe" in motivo for _, motivo in segundo["rechazados"]))

    def test_importar_archivo_inexistente_o_sin_columnas(self):
        with self.assertRaises(FileNotFoundError):
            importar_servicios_excel(os.path.join(self.carpeta, "no_existe.xlsx"), lista_servicios=[])
        libro = Workbook()
        libro.active.append(["Columna", "Otra"])
        ruta = os.path.join(self.carpeta, "mal.xlsx")
        libro.save(ruta)
        with self.assertRaises(ValueError):
            importar_servicios_excel(ruta, lista_servicios=[])


class TestClasesYEncapsulamiento(unittest.TestCase):
    """Actividades 3 y 4: clases, objetos, metodos, getters y setters."""

    def test_objeto_servicio_y_metodos(self):
        servicio = servicio_valido()
        self.assertEqual(servicio.categoria, "Electricidad")
        self.assertEqual(servicio.calcular_costo(2), round(40000 * 2 * 1.19, 2))
        servicio.cambiar_disponibilidad(False)
        self.assertFalse(servicio.a_diccionario()["disponible"])

    def test_setters_rechazan_datos_incorrectos(self):
        servicio = servicio_valido()
        with self.assertRaises(ValueError):
            servicio.tarifa_hora = 2000
        with self.assertRaises(ValueError):
            servicio.tarifa_hora = "abc"
        with self.assertRaises(ValueError):
            servicio.categoria = "Jardineria"
        with self.assertRaises(ValueError):
            servicio.calificacion = 7
        self.assertEqual(servicio.tarifa_hora, 40000)  # el valor valido se conserva
        servicio.tarifa_hora = "55000"                 # el setter convierte el texto a float
        self.assertEqual(servicio.tarifa_hora, 55000.0)

    def test_setters_de_usuario(self):
        with self.assertRaises(ValueError):
            Cliente("USR-9", "Ana Ruiz", "correo-sin-arroba", "clave12", "Cucuta", "3001112233")
        with self.assertRaises(ValueError):
            Cliente("USR-9", "Ana Ruiz", "ana@mail.com", "clave12", "Cucuta", "123")

    def test_todos_los_datos_iniciales_son_objetos_validos(self):
        for registro in db.servicios:
            self.assertEqual(Servicio.desde_diccionario(registro).a_diccionario()["codigo"], registro["codigo"])
        for registro in db.usuarios:
            self.assertEqual(Usuario.desde_diccionario(registro).correo, registro["correo"])


class TestHerenciaYOperadores(unittest.TestCase):
    """Actividades 5 y 6: herencia, sobrescritura de metodos y de operadores."""

    def test_herencia_crea_la_clase_derivada_correcta(self):
        tipos = [type(Usuario.desde_diccionario(u)) for u in db.usuarios]
        self.assertEqual(tipos, [Cliente, Prestador, Administrador])
        for clase in tipos:
            self.assertTrue(issubclass(clase, Usuario))

    def test_metodo_sobrescrito_y_metodo_heredado(self):
        cliente = Usuario.desde_diccionario(db.usuarios[0])
        prestador = Usuario.desde_diccionario(db.usuarios[1])
        self.assertNotEqual(cliente.describir_rol(), prestador.describir_rol())
        self.assertTrue(prestador.verificar_credenciales("CARLOS.GOMEZ@email.com", "carlos456"))
        salida = io.StringIO()
        with redirect_stdout(salida):
            prestador.presentar()  # heredado de Usuario, usa describir_rol() sobrescrito
        self.assertIn("Prestador: publica servicios", salida.getvalue())
        self.assertGreater(prestador.contar_servicios(db.servicios), 0)

    def test_operador_igual_en_servicios_y_usuarios(self):
        self.assertEqual(servicio_valido(), servicio_valido(tarifa_hora=99000))
        self.assertNotEqual(servicio_valido(), servicio_valido(codigo="SERV-91"))
        self.assertIn(servicio_valido(), [servicio_valido(descripcion="Otra descripcion larga")])
        a = Usuario.desde_diccionario(db.usuarios[0])
        b = Usuario.desde_diccionario(dict(db.usuarios[0], nombre="Juan Pablo Perez"))
        self.assertEqual(a, b)

    def test_operador_suma_en_facturas(self):
        f1 = Factura("A", 100000)
        f2 = Factura("B", 50000)
        total = f1 + f2
        self.assertEqual(total.subtotal, 150000)
        self.assertEqual(total.total, round(150000 * 1.19, 2))
        self.assertEqual(total.cantidad_contratos, 2)
        self.assertEqual(sum([f1, f2]), total)  # __radd__ permite sum()
        self.assertIn("COP", str(total))
        with self.assertRaises(ValueError):
            Factura("Negativa", -1)


class TestIntegracion(unittest.TestCase):
    """Actividad 7: las nuevas funciones conviven con las anteriores."""

    def test_eliminar_servicio_con_remove(self):
        catalogo = copy.deepcopy(db.servicios)
        admin = db.usuarios[2]
        exito, _ = quitar_servicio_del_catalogo("SERV-05", admin, catalogo)
        self.assertTrue(exito)
        self.assertNotIn("SERV-05", [s["codigo"] for s in catalogo])
        exito, mensaje = quitar_servicio_del_catalogo("SERV-99", admin, catalogo)
        self.assertFalse(exito)
        self.assertIn("No se encontro", mensaje)

    def test_cliente_no_puede_eliminar_servicios_ajenos(self):
        catalogo = copy.deepcopy(db.servicios)
        exito, _ = quitar_servicio_del_catalogo("SERV-01", db.usuarios[0], catalogo)
        self.assertFalse(exito)
        self.assertEqual(len(catalogo), len(db.servicios))

    def test_todos_los_modulos_importan(self):
        import main  # noqa: F401  (el menu principal carga sin errores)
        import app_gui  # noqa: F401


if __name__ == "__main__":
    print("=" * 78)
    print("   PRUEBAS AUTOMATIZADAS — GUIA 11 (ARCHIVOS, EXCEL Y POO)")
    print("=" * 78)
    unittest.main(verbosity=2)
