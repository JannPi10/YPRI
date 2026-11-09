"""
========================================================================================
GENERADOR DEL INFORME FORMAL DE ENTREGA ACADÉMICA — GUÍA 10
Plataforma YPRI: Subalgoritmos en Python (Funciones, Procedimientos y Modularización)
========================================================================================
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos
Institución: Fundación de Estudios Superiores Comfanorte (FESC) - 2026
Integrantes: Jann Pierre Ortiz Zambrano y Josué David Rincón Palomino
========================================================================================
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, hex_color):
    """Aplica color de fondo hexadecimal a una celda de tabla."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece márgenes internos en dxa para legibilidad."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def crear_documento():
    doc = docx.Document()

    # Configuración de márgenes estándar (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Estilo base
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(15, 23, 42)  # Slate 900

    # =========================================================================
    # PORTADA INSTITUCIONAL FORMAL (FESC)
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run(
        "FUNDACIÓN DE ESTUDIOS SUPERIORES COMFANORTE — FESC\n"
        "FACULTAD DE INGENIERÍA\n"
        "PROGRAMA DE INGENIERÍA DE SOFTWARE — 2026"
    )
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph("\n\n")

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tit = p_tit.add_run(
        "YPRI — PLATAFORMA DE SERVICIOS A DOMICILIO\n"
        "INFORME TÉCNICO DE APLICACIÓN PRÁCTICA"
    )
    r_tit.font.size = Pt(18)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGBColor(37, 99, 235)  # Blue 600

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(
        "GUÍA DE APRENDIZAJE N.º 10:\n"
        "SUBALGORITMOS EN PYTHON: FUNCIONES, PROCEDIMIENTOS Y MODULARIZACIÓN\n"
        "Unidad 2: Estructuras de Datos | Asignatura: Diseño Funcional"
    )
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph("\n\n\n")

    p_aut = doc.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_aut = p_aut.add_run(
        "Desarrolladores e Integrantes:\n"
        "Jann Pierre Ortiz Zambrano\n"
        "Josué David Rincón Palomino\n\n"
        "Docente / Asignatura: Diseño Funcional\n"
        "San José de Cúcuta, Norte de Santander\n"
        "Noviembre de 2026"
    )
    r_aut.font.size = Pt(11)
    r_aut.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCCIÓN Y OBJETIVOS DE LA GUÍA 10
    # =========================================================================
    h1 = doc.add_heading("1. Introducción y Objetivos de la Guía 10", level=1)
    h1.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "El presente informe consolida el cumplimiento integral y riguroso de la Guía de Aprendizaje N.º 10, "
        "titulada 'Subalgoritmos en Python: Funciones, Procedimientos y Modularización', correspondiente a la Unidad 2 "
        "(Estructuras de Datos) de la asignatura Diseño Funcional en la Fundación de Estudios Superiores Comfanorte (FESC). "
        "El proyecto sobre el cual se desarrolla esta aplicación es YPRI, una plataforma integral orientada a la contratación, "
        "cotización y gestión de servicios técnicos e instalaciones para el hogar y comercio (electricidad, plomería, limpieza, "
        "climatización y cerrajería) en las principales ciudades de Colombia."
    )

    doc.add_paragraph(
        "En esta etapa, el proyecto evoluciona desde la organización estructurada de datos (tuplas de la semana 7, vectores "
        "unidimensionales de la semana 8 y matrices bidimensionales de la semana 9) hacia el paradigma de modularización "
        "funcional y subalgoritmos. Esto permite segmentar el aplicativo en unidades de ejecución cohesivas, desacopladas, "
        "reutilizables y fácilmente testeables, erradicando instrucciones repetidas y elevando la calidad del código bajo el principio DRY (Don't Repeat Yourself)."
    )

    p_obj = doc.add_paragraph()
    p_obj.add_run("Objetivos de Aprendizaje Cumplidos:\n").bold = True
    doc.add_paragraph("• Comprender el concepto de subalgoritmo y sus ventajas en la arquitectura de software.", style='List Bullet')
    doc.add_paragraph("• Implementar funciones con parámetros que retornan resultados explícitos mediante la sentencia return.", style='List Bullet')
    doc.add_paragraph("• Desarrollar procedimientos de interacción con el usuario que ejecutan tareas específicas sin retornar valor (None).", style='List Bullet')
    doc.add_paragraph("• Aplicar funciones lambda para operaciones breves, cálculos ágiles y criterios dinámicos de ordenamiento.", style='List Bullet')
    doc.add_paragraph("• Analizar y diferenciar el ámbito de variables locales y globales, así como el comportamiento de argumentos por valor (inmutables) y por referencia (mutables).", style='List Bullet')
    doc.add_paragraph("• Reorganizar y modularizar el código del sistema YPRI, conservando el 100% de las funcionalidades desarrolladas en semanas anteriores.", style='List Bullet')
    doc.add_paragraph("• Diseñar y ejecutar una suite automatizada de pruebas unitarias que compruebe empíricamente el correcto funcionamiento de cada subalgoritmo.", style='List Bullet')

    # =========================================================================
    # 2. SECCIÓN 2: ACTIVIDAD PRÁCTICA GUIADA (SISTEMA DE INVENTARIO)
    # =========================================================================
    h2 = doc.add_heading("2. Actividad Práctica Guiada (Sección 2 de la Guía)", level=1)
    h2.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "En cumplimiento de la Sección 2 de la guía de aprendizaje, se implementó, ejecutó y verificó el programa "
        "'Sistema de Inventario con Funciones', el cual administra un catálogo de productos permitiendo registrar, consultar, "
        "buscar, ordenar por precio mediante funciones lambda y calcular el total financiero mediante funciones con retorno."
    )

    doc.add_paragraph("Estructura de Subalgoritmos Implementados en el Ejercicio Guiado:")

    tabla_ej = doc.add_table(rows=8, cols=4)
    tabla_ej.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_ej = ["Subalgoritmo", "Tipo", "Parámetros", "Responsabilidad Principal"]
    for col_idx, text in enumerate(headers_ej):
        cell = tabla_ej.cell(0, col_idx)
        cell.text = text
        set_cell_background(cell, "0F172A")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    filas_ej = [
        ["registrar_producto()", "Procedimiento", "Ninguno (captura por input)", "Solicita código, nombre, precio y cantidad; valida no duplicidad, campos obligatorios y números no negativos."],
        ["calcular_subtotal(precio, cantidad)", "Función (return)", "precio (float), cantidad (int)", "Multiplica precio por cantidad y devuelve el valor monetario exacto del ítem."],
        ["mostrar_productos()", "Procedimiento", "Ninguno", "Recorre la lista de productos e invoca calcular_subtotal() para presentar cada registro tabulado."],
        ["buscar_producto()", "Procedimiento", "Ninguno", "Solicita un código por consola, recorre la lista secuencialmente y muestra el diccionario si coincide."],
        ["calcular_total_inventario()", "Función (return)", "Ninguno", "Suma acumulativa de subtotales invocando calcular_subtotal() para cada ítem y retorna el total general."],
        ["ordenar_productos()", "Procedimiento + Lambda", "Ninguno", "Ordena los productos por precio utilizando sorted(productos, key=lambda p: p['precio'])."],
        ["mostrar_menu()", "Procedimiento", "Ninguno", "Imprime en consola las opciones del menú interactivo (1 al 5 y 0 para salir)."]
    ]

    for row_idx, fila in enumerate(filas_ej):
        for col_idx, valor in enumerate(fila):
            cell = tabla_ej.cell(row_idx + 1, col_idx)
            cell.text = valor
            if col_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph(
        "\nEl código fuente del ejercicio guiado se encuentra compilado en 'backend/ejercicio_practico_guia10.py' y puede ejecutarse "
        "de manera independiente o desde la opción 6 del menú principal de consola de YPRI y desde la pestaña dedicada en la interfaz gráfica."
    )

    # =========================================================================
    # 3. SECCIÓN 3: APLICACIÓN PRÁCTICA AL PROYECTO YPRI
    # =========================================================================
    h3 = doc.add_heading("3. Aplicación Práctica al Proyecto Software YPRI", level=1)
    h3.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    # ACTIVIDAD 1
    h_act1 = doc.add_heading("ACTIVIDAD 1. Identificación y Clasificación de Subalgoritmos en YPRI", level=2)
    h_act1.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Se realizó una revisión integral del código del aplicativo YPRI para mapear todas las operaciones del sistema, "
        "clasificándolas según su naturaleza funcional y su interacción:"
    )

    tabla_clasif = doc.add_table(rows=6, cols=3)
    tabla_clasif.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_c = ["Operación del Sistema", "Clasificación", "Subalgoritmo / Módulo"]
    for col_idx, text in enumerate(headers_c):
        cell = tabla_clasif.cell(0, col_idx)
        cell.text = text
        set_cell_background(cell, "1E293B")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    filas_c = [
        ["Liquidación y Cotización con IVA", "Función con return (Cálculo puro)", "calcular_liquidacion_contrato() en modules/subalgoritmos.py"],
        ["Comisión YPRI y Transferencia Neta", "Función con return (Distribución)", "calcular_comision_plataforma() en modules/subalgoritmos.py"],
        ["Recálculo Ponderado de Reputación", "Función con return (Estadística)", "calcular_promedio_calificacion() en modules/subalgoritmos.py"],
        ["Generación de Recibo Formal", "Procedimiento (Interacción y formato)", "mostrar_recibo_liquidacion() en modules/subalgoritmos.py"],
        ["Presentación de Ficha Técnica", "Procedimiento (Visualización)", "mostrar_ficha_tecnica_servicio() en modules/subalgoritmos.py"]
    ]

    for row_idx, fila in enumerate(filas_c):
        for col_idx, valor in enumerate(fila):
            cell = tabla_clasif.cell(row_idx + 1, col_idx)
            cell.text = valor
            if col_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "F8FAFC")

    # ACTIVIDAD 2
    h_act2 = doc.add_heading("ACTIVIDAD 2. Implementación de Funciones con Parámetros y Retorno (return)", level=2)
    h_act2.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "En concordancia con el requerimiento de implementar al menos tres funciones que reciban parámetros y devuelvan resultados mediante return, "
        "se implementaron cinco funciones de cálculo en 'modules/subalgoritmos.py':"
    )
    doc.add_paragraph(
        "1. 'calcular_liquidacion_contrato(tarifa_hora, horas, descuento_pct, tasa_iva)': Recibe la tarifa horaria, horas requeridas, porcentaje de descuento y tasa impositiva. "
        "Calcula el subtotal bruto, deducción promocional, subtotal neto, liquidación del 19% de IVA y total a pagar. Devuelve un diccionario con cada uno de estos valores exactos.\n\n"
        "2. 'calcular_comision_plataforma(total_pagar, porcentaje_comision, retencion_pct)': Recibe el importe total facturado y calcula la comisión operacional de YPRI (10%), "
        "la retención en la fuente tributaria (4%) y el importe neto que debe ser transferido a la cuenta del prestador del servicio.\n\n"
        "3. 'calcular_promedio_calificacion(rating_previo, num_evaluaciones, nueva_puntuacion)': Recibe el promedio previo, la cantidad acumulada de servicios evaluados y la nueva calificación (1.0 a 5.0). "
        "Aplica la fórmula matemática de actualización ponderada continua y devuelve el nuevo rating redondeado a 1 decimal.\n\n"
        "4. 'calcular_metricas_prestador(prestador_id, lista_contratos, lista_calificaciones)': Analiza los contratos y calificaciones históricas del prestador, retornando total de contratos, tasa de cumplimiento, ingresos brutos, comisión y promedio de estrellas.\n\n"
        "5. 'calcular_resumen_estadistico(valores)': Recibe un vector numérico arbitrario y retorna un diccionario con cantidad de elementos, suma total, media aritmética, valor mínimo y valor máximo."
    )

    # ACTIVIDAD 3
    h_act3 = doc.add_heading("ACTIVIDAD 3. Implementación de Procedimientos (Interacción sin Retorno)", level=2)
    h_act3.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Los procedimientos son subalgoritmos cuya única responsabilidad es ejecutar tareas operativas, formatear salidas "
        "o interactuar con el usuario, sin devolver valores reutilizables (retornan 'None' implícitamente en Python):\n\n"
        "• 'mostrar_recibo_liquidacion(datos_liquidacion, servicio)': Procedimiento que recibe el diccionario de liquidación y los datos del servicio, "
        "generando en consola un recibo tabular con formato de moneda colombiana (COP), encabezados y líneas divisorias.\n"
        "• 'mostrar_ficha_tecnica_servicio(servicio)': Procedimiento que despliega de forma profesional la información completa del servicio: código, prestador, categoría, ciudad, tarifa, estrellas, experiencia y disponibilidad.\n"
        "• 'mostrar_tarjeta_rendimiento_prestador(prestador_nombre, metricas)': Procedimiento de auditoría operativa que imprime el balance de rendimiento del prestador.\n"
        "• 'mostrar_menu_subalgoritmos()': Procedimiento de menú en consola que permite al docente o evaluador probar individualmente cada componente de la Guía 10."
    )

    # ACTIVIDAD 4
    h_act4 = doc.add_heading("ACTIVIDAD 4. Aplicación de Funciones Lambda en YPRI", level=2)
    h_act4.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Las funciones lambda se aplicaron tanto en expresiones breves de cálculo como en criterios funcionales de ordenamiento:\n\n"
        "1. Lambdas de cálculo:\n"
        "   • 'calcular_descuento_lambda = lambda subtotal, pct: round(subtotal * (pct / 100.0), 2)'\n"
        "   • 'calcular_iva_lambda = lambda base, tasa=0.19: round(base * tasa, 2)'\n"
        "   • 'formatear_cop_lambda = lambda valor: f\"${valor:,.0f} COP\"'\n\n"
        "2. Lambdas para ordenamiento en vectores de diccionarios:\n"
        "   • Ordenamiento por tarifa: 'sorted(servicios, key=lambda s: s[\"tarifa_hora\"], reverse=descendente)'\n"
        "   • Ordenamiento por reputación: 'sorted(servicios, key=lambda s: s.get(\"calificacion\", 0.0), reverse=True)'\n"
        "   • Ordenamiento de contratos por importe: 'sorted(contratos, key=lambda c: c.get(\"total\", 0.0), reverse=True)'"
    )

    # ACTIVIDAD 5
    h_act5 = doc.add_heading("ACTIVIDAD 5. Variables Locales, Globales y Comportamiento de Argumentos", level=2)
    h_act5.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Se analizó exhaustivamente el ciclo de vida y ámbito de variables en el sistema YPRI:\n"
        "• Variables Globales: Residen en 'data/database.py' (listas 'usuarios', 'servicios', 'contratos', 'calificaciones', 'matriz_ventas_semanales', '_sesion_actual'). "
        "Son compartidas transversalmente por la aplicación, pero su mutación está encapsulada mediante funciones especializadas para evitar efectos secundarios incontrolados.\n"
        "• Variables Locales: Creadas dentro de cada función ('tarifa_hora', 'horas', 'subtotal_bruto', 'monto_descuento', 'monto_iva', 'total_pagar'). "
        "Existen únicamente durante la ejecución del bloque de la función y se liberan automáticamente de la memoria al finalizar (recolección de basura)."
    )
    doc.add_paragraph(
        "Diferenciación del Paso de Argumentos:\n"
        "1. Objetos Inmutables (int, float, str, tuple): En Python se pasan mediante referencias a objetos inmutables. "
        "Cualquier modificación o reasignación interna ('numero = numero + 10000') crea un nuevo objeto en el ámbito local, "
        "dejando la variable del llamador exactamente igual (comportamiento equivalente al paso por valor).\n"
        "2. Objetos Mutables (list, dict): Las colecciones se pasan mediante referencias a objetos mutables. "
        "Las operaciones 'in-place' como 'lista.append(item)' o 'diccionario[clave] = valor' modifican directamente la estructura compartida en memoria, "
        "reflejándose inmediatamente en el llamador (comportamiento equivalente al paso por referencia).\n\n"
        "Para comprobar empíricamente este comportamiento, se desarrollaron las funciones 'modificar_numero_prueba', 'modificar_cadena_prueba', "
        "'agregar_elemento_lista_prueba' y 'actualizar_campo_diccionario_prueba', las cuales fueron verificadas mediante pruebas unitarias automatizadas."
    )

    # ACTIVIDAD 6
    h_act6 = doc.add_heading("ACTIVIDAD 6. Modularización del Aplicativo y Principio DRY", level=2)
    h_act6.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Siguiendo la instrucción de reorganizar el código existente para evitar instrucciones repetidas conservando "
        "el 100% de las funcionalidades desarrolladas en semanas anteriores:\n\n"
        "1. Se creó el módulo especializado 'backend/modules/subalgoritmos.py', desacoplando los cálculos matemáticos de las interfaces de entrada/salida.\n"
        "2. Se refactorizó 'modules/contratos.py': la operación de cotización que antes realizaba sumas y multiplicaciones en línea dentro del procedimiento de solicitud ahora delega el cálculo a 'calcular_liquidacion_contrato()' y la impresión a 'mostrar_recibo_liquidacion()'.\n"
        "3. Se refactorizó 'modules/calificaciones.py': el recálculo ponderado del promedio que se realizaba manualmente ahora invoca la función 'calcular_promedio_calificacion()'.\n"
        "4. Se actualizó 'main.py' para incorporar el acceso directo al explorador de subalgoritmos y al ejercicio de práctica guiada.\n"
        "5. Se integró una nueva vista en 'app_gui.py' (interfaz Tkinter) y en la plataforma web desplegable en Vercel."
    )

    # ACTIVIDAD 7
    h_act7 = doc.add_heading("ACTIVIDAD 7. Pruebas Automatizadas de Funcionamiento", level=2)
    h_act7.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Se desarrolló la suite automatizada 'backend/tests_guia10.py' basada en el módulo estándar 'unittest'. "
        "La suite ejecutó 9 pruebas exhaustivas con un resultado de 100% exitoso (0 fallos y 0 errores) en 0.008 segundos:"
    )

    doc.add_paragraph("• test_01_ejercicio_practico_seccion2: Valida subtotal, total de inventario y ordenamiento lambda del ejercicio guiado.")
    doc.add_paragraph("• test_02_funciones_con_return_liquidacion: Valida matemática de cotización, descuento, IVA 19% y control de excepciones ValueError.")
    doc.add_paragraph("• test_03_funciones_con_return_comision: Valida liquidación del 10% de comisión y 4% de retención en la fuente.")
    doc.add_paragraph("• test_04_funciones_con_return_promedio_rating: Valida cálculo ponderado del rating acumulado de prestadores.")
    doc.add_paragraph("• test_05_funciones_con_return_estadisticas_vector: Valida cantidad, suma, promedio, mínimo y máximo en vectores.")
    doc.add_paragraph("• test_06_procedimientos_interaccion: Valida que los procedimientos retornen None e impriman en consola correctamente.")
    doc.add_paragraph("• test_07_funciones_lambda: Valida lambdas de cálculo y ordenamiento ascendente y descendente.")
    doc.add_paragraph("• test_08_paso_argumentos_inmutables_vs_mutables: Valida empíricamente la inmutabilidad de floats/strings y la mutabilidad in-place de listas/diccionarios.")
    doc.add_paragraph("• test_09_modularizacion_y_conservacion_de_funcionalidad: Comprueba la ausencia de dependencias circulares y la preservación integral de módulos previos.")

    # =========================================================================
    # 4. DOCUMENTACIÓN ACUMULATIVA POR SEMANAS
    # =========================================================================
    h4 = doc.add_heading("4. Documentación Acumulativa de Temas por Semanas", level=1)
    h4.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "A continuación se presenta la matriz evolutiva de temas de programación y estructuras de datos aplicados en el software YPRI:"
    )

    tabla_sem = doc.add_table(rows=6, cols=3)
    tabla_sem.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_s = ["Semanas", "Temas y Estructuras", "Implementación Concreta en YPRI"]
    for col_idx, text in enumerate(headers_s):
        cell = tabla_sem.cell(0, col_idx)
        cell.text = text
        set_cell_background(cell, "1E293B")
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    filas_sem = [
        ["Semanas 5 y 6", "Ciclos y Validaciones Defensivas", "Bucles 'while True', sentencias 'break' y 'continue', bloques 'try - except ValueError', validación de rangos y entradas no vacías en core/validaciones.py."],
        ["Semana 7", "Tuplas, Cadenas y Diccionarios", "Tuplas inmutables (ROLES, CATEGORIAS, CIUDADES, ESTADOS_CONTRATO), diccionarios con atributos clave-valor para cada entidad y normalización con .strip(), .lower()."],
        ["Semana 8", "Vectores (Almacenamiento, Ordenamiento y Búsqueda)", "Vectores unidimensionales (usuarios[], servicios[], contratos[], calificaciones[]), dimensionamiento len(), ordenamiento con sorted(key=lambda), búsquedas secuenciales y reto estadístico."],
        ["Semana 9", "Matrices (Creación, Recorrido y Operaciones)", "Estructuras bidimensionales (listas de listas), acceso matriz[i][j], ciclos for anidados, suma de filas y columnas, matriz cuadrada 5x5, nula e identidad en modules/matrices.py."],
        ["Semana 10", "Subalgoritmos (Funciones, Procedimientos y Modularización)", "Funciones puras con return (liquidación, comisiones, rating), procedimientos desacoplados de presentación, expresiones lambda, modularización DRY en modules/subalgoritmos.py y paso de argumentos por valor y referencia."]
    ]

    for row_idx, fila in enumerate(filas_sem):
        for col_idx, valor in enumerate(fila):
            cell = tabla_sem.cell(row_idx + 1, col_idx)
            cell.text = valor
            if col_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "F8FAFC")

    # =========================================================================
    # 5. PLATAFORMA WEB Y MOVIL ACTUALIZADA (NEXT.JS + VERCEL)
    # =========================================================================
    h5 = doc.add_heading("5. Plataforma Web y Móvil Actualizada Desplegable en Vercel", level=1)
    h5.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "La plataforma web construida en Next.js 14 y Tailwind CSS fue actualizada con una pestaña interactiva dedicada a la Guía 10:\n\n"
        "• Calculadora interactiva de liquidación financiera y comisión de plataforma en tiempo real con return tipado en TypeScript.\n"
        "• Visualizador de fichas técnicas y recibos de liquidación desacoplados mediante procedimientos.\n"
        "• Tabulación reactiva ordenada con funciones lambda (tarifa ascendente, tarifa descendente y calificación).\n"
        "• Simulador visual del paso de parámetros que ilustra la mutabilidad de listas versus la inmutabilidad de números.\n"
        "• Simulador web completo del Sistema de Inventario de la Sección 2 con alta de productos, cálculo de subtotales y total general.\n"
        "• Compatibilidad nativa con despliegue en la nube mediante Vercel (vercel.json configurado)."
    )

    salida_docx = os.path.join(os.path.dirname(__file__), "ENTREGA_GUIA_10_YPRI.docx")
    doc.save(salida_docx)
    print(f"Documento institucional generado exitosamente en: {salida_docx}")


if __name__ == "__main__":
    crear_documento()
