"""
Script para generar el documento academico formal ENTREGA_GUIA_9_YPRI.docx
segun los lineamientos de la Fundacion de Estudios Superiores Comfanorte (FESC).
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def crear_documento():
    doc = docx.Document()

    # Configurar margenes
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Estilos de fuente base
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(15, 23, 42)  # Slate 900

    # =========================================================================
    # PORTADA INSTITUCIONAL
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("FUNDACIÓN DE ESTUDIOS SUPERIORES COMFANORTE — FESC\nFACULTAD DE INGENIERÍA\nINGENIERÍA DE SOFTWARE — OCTAVO SEMESTRE (2026)")
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph("\n\n")

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tit = p_tit.add_run("YPRI — PLATAFORMA DE SERVICIOS A DOMICILIO\nINFORME DE APLICACIÓN PRÁCTICA")
    r_tit.font.size = Pt(18)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGBColor(37, 99, 235)  # Blue 600

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("GUÍA DE APRENDIZAJE N.º 9:\nMATRICES EN PYTHON: CREACIÓN, RECORRIDO Y OPERACIONES\nUnidad 2: Estructuras de Datos | Asignatura: Diseño Funcional")
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph("\n\n\n")

    p_aut = doc.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_aut = p_aut.add_run("Desarrolladores e Integrantes:\nJann Pierre Ortiz Zambrano\nJosué David Rincón Palomino\n\nDocente / Asignatura: Diseño Funcional\nSan José de Cúcuta, Norte de Santander\nNoviembre de 2026")
    r_aut.font.size = Pt(11)
    r_aut.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCCIÓN Y OBJETIVOS
    # =========================================================================
    h1 = doc.add_heading("1. Introducción y Objetivos de la Guía 9", level=1)
    h1.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "El presente informe documenta el desarrollo y cumplimiento integral de la Guía de Aprendizaje N.º 9 "
        "titulada 'Matrices en Python: Creación, Recorrido y Operaciones', enmarcada en la Unidad 2 (Estructuras de Datos) "
        "de la asignatura Diseño Funcional. El proyecto software sobre el cual se implementa esta guía es YPRI, "
        "una plataforma integral para la contratación, cotización y gestión de servicios técnicos y profesionales a domicilio "
        "(electricidad, plomería, limpieza, climatización y cerrajería) en las principales ciudades de Colombia."
    )

    doc.add_paragraph(
        "En esta etapa, el software evoluciona desde las colecciones unidimensionales (vectores de la Guía 8) hacia estructuras "
        "de datos bidimensionales (matrices), permitiendo organizar, consultar, registrar y procesar información analítica de "
        "ventas y cobertura organizada estrictamente en filas y columnas."
    )

    p_obj = doc.add_paragraph()
    p_obj.add_run("Objetivos Específicos Cumplidos:\n").bold = True
    doc.add_paragraph("• Comprender la representación de matrices en Python como listas anidadas (listas de listas).", style='List Bullet')
    doc.add_paragraph("• Acceder y modificar elementos específicos utilizando la notación indexada matriz[fila][columna].", style='List Bullet')
    doc.add_paragraph("• Implementar recorridos bidimensionales completos mediante ciclos for anidados.", style='List Bullet')
    doc.add_paragraph("• Incorporar operaciones matemáticas útiles: suma de filas, suma de columnas, total general y promedios por registro.", style='List Bullet')
    doc.add_paragraph("• Identificar y manipular matrices especiales: matriz cuadrada (nxn), matriz nula y matriz identidad.", style='List Bullet')
    doc.add_paragraph("• Integrar la nueva funcionalidad con la base de datos, módulos de negocio, CLI interactivo, GUI Tkinter y una moderna plataforma Web responsive orientada a móvil y desplegable en Vercel.", style='List Bullet')

    # =========================================================================
    # 2. SECCIÓN 2 DE LA GUÍA: ACTIVIDAD PRÁCTICA GUIADA (3x3)
    # =========================================================================
    h2 = doc.add_heading("2. Desarrollo de la Actividad Práctica Guiada (Sección 2 de la Guía)", level=1)
    h2.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "Siguiendo las directrices de la Sección 2 de la guía de aprendizaje, se implementó y ejecutó el aplicativo "
        "para registrar y procesar las ventas de 3 productos durante 3 días (Lunes, Martes y Miércoles). El programa incluye "
        "un ciclo defensivo 'while True' con bloque 'try - except ValueError' y validación contra valores negativos (valor >= 0)."
    )

    doc.add_paragraph("Estructura de la Matriz de Ventas de Ejemplo:")
    
    # Tabla 3x3 de ejemplo
    tabla_ej = doc.add_table(rows=5, cols=5)
    tabla_ej.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_ej = ["Producto", "Lunes", "Martes", "Miércoles", "Total Producto"]
    for col_idx, text in enumerate(headers_ej):
        cell = tabla_ej.cell(0, col_idx)
        cell.text = text
        set_cell_background(cell, "0F172A")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    filas_datos_ej = [
        ["Producto A", "$150,000.00", "$200,000.00", "$180,000.00", "$530,000.00"],
        ["Producto B", "$120,000.00", "$250,000.00", "$300,000.00", "$670,000.00"],
        ["Producto C", "$175,000.00", "$190,000.00", "$220,000.00", "$585,000.00"],
        ["TOTAL DÍA", "$445,000.00", "$640,000.00", "$700,000.00", "$1,785,000.00"],
    ]

    for row_idx, fila in enumerate(filas_datos_ej):
        for col_idx, valor in enumerate(fila):
            cell = tabla_ej.cell(row_idx + 1, col_idx)
            cell.text = valor
            if row_idx == 3 or col_idx == 4:
                set_cell_background(cell, "F1F5F9")
                cell.paragraphs[0].runs[0].font.bold = True

    p_res_ej = doc.add_paragraph()
    p_res_ej.add_run("\nMétricas Resultantes del Ejercicio Guiado:\n").bold = True
    p_res_ej.add_run("• Total General Acumulado: $1,785,000.00 COP\n")
    p_res_ej.add_run("• Cantidad de Registros: 3 productos × 3 días = 9 celdas\n")
    p_res_ej.add_run("• Promedio por Registro: $1,785,000 / 9 = $198,333.33 COP\n")

    # =========================================================================
    # 3. SECCIÓN 3: APLICACIÓN AL PROYECTO YPRI
    # =========================================================================
    h3 = doc.add_heading("3. Aplicación Práctica al Proyecto de Software YPRI", level=1)
    h3.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "En cumplimiento de la Sección 3 ('Aplicación al Proyecto'), se identificaron las necesidades operativas "
        "y analíticas de YPRI para estructurar información multidimensional mediante filas y columnas."
    )

    # ACTIVIDAD 1
    h_act1 = doc.add_heading("ACTIVIDAD 1: Implementación de Matrices en el Aplicativo", level=2)
    h_act1.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Se implementaron dos matrices bidimensionales representadas como listas de listas en 'data/database.py':\n"
        "1. 'matriz_ventas_semanales': Matriz de 5 filas (Categorías oficiales: Electricidad, Plomería, Limpieza, Climatización, Cerrajería) "
        "por 6 columnas (Días laborables: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado), que almacena la facturación neta en pesos colombianos (COP).\n"
        "2. 'matriz_ventas_ciudades': Matriz de 5 filas (Categorías) por 5 columnas (Ciudades de cobertura: Cúcuta, Cali, Bogotá, Medellín, Bucaramanga), "
        "la cual cumple estrictamente la definición de MATRIZ CUADRADA (5x5)."
    )

    # ACTIVIDAD 2
    h_act2 = doc.add_heading("ACTIVIDAD 2: Registro y Consulta de Información en la Matriz", level=2)
    h_act2.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Se programaron mecanismos interactivos defensivos para consultar y registrar datos:\n"
        "• Consulta por celda: función 'consultar_celda(matriz, i, j)' que retorna directamente matriz[i][j].\n"
        "• Consulta de fila completa: función 'consultar_fila_especifica()' que extrae matriz[i], calcula su total y su promedio diario.\n"
        "• Consulta de columna completa: función 'consultar_columna_especifica()' que itera verticalmente para extraer [fila[j] for fila in matriz].\n"
        "• Registro / Modificación indexada: función 'modificar_celda(matriz, i, j, valor)' que valida los límites de los índices y garantiza "
        "que el importe ingresado no sea negativo."
    )

    # ACTIVIDAD 3
    h_act3 = doc.add_heading("ACTIVIDAD 3: Recorrido de Filas y Columnas con Ciclos Anidados", level=2)
    h_act3.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Se implementaron tres modalidades de recorrido bidimensional utilizando ciclos 'for' anidados en 'modules/matrices.py':\n"
        "• Recorrido horizontal por elementos: un ciclo 'for fila in matriz' externo y un 'for valor in fila' interno para acumulación general y formateo.\n"
        "• Recorrido indexado por rangos: 'for i in range(len(matriz))' y 'for j in range(len(matriz[i]))' para acceder a coordenadas exactas y relacionarlas con las tuplas inmutables de categorías y días.\n"
        "• Recorrido vertical por columnas: ciclo externo 'for j in range(columnas)' y ciclo interno 'for i in range(filas)' para totalizar columnas verticalmente."
    )

    # ACTIVIDAD 4
    h_act4 = doc.add_heading("ACTIVIDAD 4: Operaciones Matemáticas y Procesamiento Útil", level=2)
    h_act4.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Se incorporaron múltiples operaciones analíticas que agregan valor comercial y contable a la plataforma YPRI:\n"
        "• Total por Fila: 'calcular_totales_filas()' suma el total facturado por cada una de las 5 categorías de servicios.\n"
        "• Total por Columna: 'calcular_totales_columnas()' calcula la recaudación diaria de la plataforma o por ciudad.\n"
        "• Total General de la Plataforma: 'calcular_total_general()' suma todas las celdas de la matriz.\n"
        "• Promedio por Registro: 'calcular_promedio_general()' divide el total general entre el producto de filas × columnas (30 celdas en la matriz semanal).\n"
        "• Identificación de Extremos y Categoría Líder: función 'analizar_rendimiento_matriz()' que detecta la categoría con mayores ingresos, el día más productivo y la celda con el récord histórico de venta individual.\n"
        "• Matrices Especiales: funciones 'es_matriz_cuadrada()', 'crear_matriz_nula()', 'crear_matriz_identidad()' y extracción de la diagonal principal."
    )

    # ACTIVIDAD 5
    h_act5 = doc.add_heading("ACTIVIDAD 5: Integración de la Nueva Funcionalidad con las Operaciones Existentes", level=2)
    h_act5.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "En concordancia con la instrucción 'Las actividades deben desarrollarse dentro del mismo proyecto, evitando crear aplicaciones independientes', "
        "el módulo de matrices se integró transversalmente en toda la arquitectura de YPRI:\n"
        "• data/database.py: matrices globales persistentes en memoria del sistema.\n"
        "• modules/admin.py: integración de métricas matriciales en el panel de control administrativo y función de auditoría visual.\n"
        "• main.py: nuevas opciones en los menús interactivos por consola para clientes, prestadores y administradores.\n"
        "• app_gui.py: nueva pestaña y vista interactiva ' Matrices (Guía 9)' con tabla reactiva, tarjetas KPI, edición de celdas, visualizador de matrices especiales y simulador guiado.\n"
        "• Plataforma Web Vercel (Next.js + Tailwind CSS): frontend web responsivo moderno con soporte móvil-first completo desplegable en Vercel."
    )

    # =========================================================================
    # 4. DOCUMENTACIÓN ACUMULATIVA POR SEMANAS
    # =========================================================================
    h4 = doc.add_heading("4. Documentación Acumulativa de Temas por Semanas", level=1)
    h4.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "En cumplimiento de los requerimientos docentes, a continuación se consolida la documentación de todos los "
        "conceptos algorítmicos y estructuras de datos aplicados en el software a lo largo del semestre:"
    )

    tabla_temas = doc.add_table(rows=5, cols=3)
    tabla_temas.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_t = ["Semanas", "Temas y Estructuras", "Implementación en YPRI"]
    for col_idx, text in enumerate(headers_t):
        cell = tabla_temas.cell(0, col_idx)
        cell.text = text
        set_cell_background(cell, "1E293B")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    filas_temas = [
        ["Semanas 5 y 6", "Ciclos y Validaciones Defensivas", "Bucles 'while True', sentencias 'break' y 'continue', bloques 'try - except ValueError', validación de números no negativos y cadenas no vacías en core/validaciones.py."],
        ["Semana 7", "Tuplas, Cadenas y Diccionarios", "Tuplas inmutables (ROLES_SISTEMA, CATEGORIAS_SERVICIO, CIUDADES_COBERTURA, ESTADOS_CONTRATO), diccionarios con atributos clave-valor para cada entidad y normalización con .strip(), .lower(), .title()."],
        ["Semana 8", "Vectores (Almacenamiento, Ordenamiento y Búsqueda)", "Vectores unidimensionales (usuarios[], servicios[], contratos[], calificaciones[]), dimensionamiento len(), ordenamiento ascendente/descendente con sorted(key=lambda), búsquedas secuenciales y reto estadístico con min/max."],
        ["Semana 9", "Matrices (Creación, Recorrido y Operaciones)", "Estructuras bidimensionales (listas de listas), acceso matriz[i][j], ciclos for anidados, suma de filas y columnas, total general, promedio, matrices cuadradas (5x5), nulas e identidad en modules/matrices.py."]
    ]

    for row_idx, fila in enumerate(filas_temas):
        for col_idx, valor in enumerate(fila):
            cell = tabla_temas.cell(row_idx + 1, col_idx)
            cell.text = valor
            if col_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "F8FAFC")

    # =========================================================================
    # 5. PLATAFORMA WEB DESPLEGABLE EN VERCEL
    # =========================================================================
    h5 = doc.add_heading("5. Nueva Plataforma Web y Móvil Desplegable en Vercel", level=1)
    h5.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "Atendiendo a la necesidad de modernizar la experiencia de usuario y facilitar el despliegue en la nube, "
        "se desarrolló una aplicación web completa construida con Next.js, React y Tailwind CSS, diseñada bajo una filosofía "
        "móvil-first y desplegable de manera nativa e instantánea en Vercel.\n\n"
        "Características de la plataforma web:\n"
        "• Selector de perfiles (Cliente, Prestador, Admin) para probar todas las operaciones sin fricción.\n"
        "• Catálogo interactivo de servicios con ordenamiento en tiempo real por tarifa y calificación.\n"
        "• Módulo interactivo de Matrices (Guía 9) con edición de celdas en vivo, recalculo dinámico de totales y promedios, y visualizador de matrices especiales.\n"
        "• Cotizador automático con cálculo de IVA (19%) y gestión del ciclo de vida de contratos.\n"
        "• Modalidad de visualización dual: Vista Web Completa y Simulador Móvil (Smartphone iPhone/Android Frame)."
    )

    import os
    salida_docx = os.path.join(os.path.dirname(__file__), "ENTREGA_GUIA_9_YPRI.docx")
    doc.save(salida_docx)
    print(f"Documento generado exitosamente en: {salida_docx}")

if __name__ == "__main__":
    crear_documento()
