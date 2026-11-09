"""
Script para generar el documento oficial consolidado con todo el contenido
de la Guia 7 existente mas la documentacion completa de la Guia 9 (Matrices).
Sin emojis, con el mismo formato y estilo institucional de la FESC.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def agregar_tabla_dos_columnas(doc, pares, ancho_col1=Inches(2.2), ancho_col2=Inches(4.3)):
    tabla = doc.add_table(rows=len(pares), cols=2)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (col1, col2) in enumerate(pares):
        c1 = tabla.cell(idx, 0)
        c2 = tabla.cell(idx, 1)
        c1.text = col1
        c2.text = col2
        c1.width = ancho_col1
        c2.width = ancho_col2
        set_cell_background(c1, "F1F5F9")
        c1.paragraphs[0].runs[0].font.bold = True
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        c2.paragraphs[0].runs[0].font.size = Pt(9.5)
    doc.add_paragraph()

def agregar_bloque_codigo(doc, codigo):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(codigo.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(15, 23, 42)

def generar_documento_completo():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(15, 23, 42)

    # PORTADA
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("FUNDACION DE ESTUDIOS SUPERIORES COMFANORTE - FESC\nFACULTAD DE INGENIERIA\nINGENIERIA DE SOFTWARE - OCTAVO SEMESTRE (2026)")
    r_inst.font.bold = True
    r_inst.font.size = Pt(12)

    doc.add_paragraph("\n")

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tit = p_tit.add_run("YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO\nINFORME ACADEMICO CONSOLIDADO DE ESTRUCTURAS DE DATOS")
    r_tit.font.bold = True
    r_tit.font.size = Pt(16)
    r_tit.font.color.rgb = RGBColor(37, 99, 235)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("GUIA DE APRENDIZAJE N. 7: CADENAS, LISTAS, TUPLAS Y DICCIONARIOS\nGUIA DE APRENDIZAJE N. 9: MATRICES EN PYTHON (CREACION, RECORRIDO Y OPERACIONES)\nUNIDAD 2 - ESTRUCTURAS DE DATOS | TEMA 4: MATRICES")
    r_sub.font.bold = True
    r_sub.font.size = Pt(11)

    doc.add_paragraph("\n")

    p_aut = doc.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_aut = p_aut.add_run("Desarrolladores e Integrantes:\nJann Pierre Ortiz Zambrano\nJosue David Rincon Palomino\n\nDocente / Asignatura: Diseno Funcional\nSan Jose de Cucuta, Norte de Santander\n2026")
    r_aut.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # SECCION I: GUIA DE APRENDIZAJE N. 7
    # =========================================================================
    h_s1 = doc.add_heading("SECCION I: GUIA DE APRENDIZAJE N. 7 - CADENAS, LISTAS, TUPLAS Y DICCIONARIOS", level=1)
    h_s1.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    # Actividad 1
    doc.add_heading("Actividad 1. Identificacion de los Datos del Proyecto", level=2)
    datos_act1 = [
        ("NOMBRE DEL PROYECTO:", "YPRI - Plataforma de Servicios a Domicilio"),
        ("OBJETIVO DEL APLICATIVO:", "Conectar clientes con prestadores de servicios tecnicos del hogar (electricistas, plomeros, cerrajeros, etc.) en ciudades colombianas, ofreciendo cotizacion con IVA, gestion de contratos, valoracion de los servicios y arquitectura modular."),
        ("ENTIDAD PRINCIPAL QUE MANEJA EL SISTEMA:", "Servicio: unidad central que un prestador ofrece y un cliente puede contratar a traves de la plataforma."),
        ("DATOS QUE NECESITA ALMACENAR:", "Datos de usuarios (nombre, correo, contrasena, rol, ciudad, telefono). Datos de servicios (codigo, categoria, descripcion, tarifa, disponibilidad, calificacion). Datos de contratos (cliente, servicio, horas, total con IVA, estado). Datos de calificaciones (puntuacion, comentario, fecha)."),
        ("DATO QUE IDENTIFICA CADA REGISTRO:", "Usuarios: 'id' (USR-001). Servicios: 'codigo' (SERV-01). Contratos: 'id' (CONTR-101). Calificaciones: 'id' (CALIF-001)."),
        ("EJEMPLOS DE REGISTROS QUE MANEJA:", "Usuario: {id: USR-001, nombre: Juan Perez, rol: cliente, ciudad: Cucuta}. Servicio: {codigo: SERV-01, categoria: Electricidad, tarifa_hora: 35000}. Contrato: {id: CONTR-101, estado: Completado, total: 179400}.")
    ]
    agregar_tabla_dos_columnas(doc, datos_act1)

    doc.add_paragraph("Identificacion de estructuras por tipo de dato:")
    estructuras_act1 = [
        ("CADENAS (str):", "id, nombre, correo, contrasena, rol, ciudad, codigo, categoria, descripcion, estado, comentario, fecha. Las cadenas se procesan con .strip(), .lower(), .upper() y .title() para normalizar la informacion."),
        ("LISTAS (list):", "usuarios[], servicios[], contratos[], calificaciones[]. Cada lista almacena varios registros de la misma entidad. Se usa .append() para agregar y len() para contar. Se recorren con ciclo for para visualizar, buscar o filtrar."),
        ("TUPLAS, SI APLICA:", "ROLES_SISTEMA = ('cliente', 'prestador', 'admin'). CATEGORIAS_SERVICIO = ('Electricidad', 'Plomeria', 'Limpieza', 'Climatizacion', 'Cerrajeria'). ESTADOS_CONTRATO = ('Pendiente', 'En proceso', 'Completado', 'Cancelado'). CIUDADES_COBERTURA = ('Cucuta', 'Cali', 'Bogota', 'Medellin', 'Bucaramanga'). Son valores fijos que no deben cambiar durante la ejecucion del programa."),
        ("DICCIONARIOS (dict):", "Cada usuario, servicio, contrato y calificacion se representa como un diccionario de pares clave-valor. Ejemplo: {'id': 'USR-001', 'nombre': 'Juan Perez', 'rol': 'cliente'}. Se accede a los datos por clave: usuario['nombre'], servicio['tarifa_hora'].")
    ]
    agregar_tabla_dos_columnas(doc, estructuras_act1)

    # Actividad 2
    doc.add_heading("Actividad 2. Diseno de la Estructura de un Registro", level=2)
    doc.add_paragraph(
        "La entidad principal seleccionada para el proyecto YPRI es el Servicio, ya que es el nucleo del aplicativo: "
        "los prestadores publican servicios y los clientes los contratan. A continuacion se definen sus atributos:"
    )
    atributos_act2 = [
        ("ENTIDAD:", "Servicio"),
        ("IDENTIFICADOR:", "codigo (str) - unico, no modificable. Ejemplo: SERV-01"),
        ("ATRIBUTO 1: categoria", "TIPO DE DATO: str (cadena). Ejemplo: 'Electricidad'"),
        ("ATRIBUTO 2: descripcion", "TIPO DE DATO: str (cadena). Ejemplo: 'Instalaciones electricas residenciales'"),
        ("ATRIBUTO 3: tarifa_hora", "TIPO DE DATO: float (numero decimal). Ejemplo: 35000.0"),
        ("ATRIBUTO 4: disponible", "TIPO DE DATO: bool (booleano). Ejemplo: True"),
        ("ATRIBUTO 5: calificacion", "TIPO DE DATO: float (numero decimal de 1.0 a 5.0). Ejemplo: 4.8"),
        ("ATRIBUTO 6: ciudad", "TIPO DE DATO: str (cadena). Ejemplo: 'Cucuta'"),
        ("ATRIBUTO 7: prestador_nombre", "TIPO DE DATO: str (cadena). Ejemplo: 'Carlos Gomez'")
    ]
    agregar_tabla_dos_columnas(doc, atributos_act2)

    doc.add_paragraph("Representacion como Diccionario Python:")
    agregar_bloque_codigo(doc, """servicio = {
    "codigo":           "SERV-01",
    "prestador_id":     "USR-002",
    "prestador_nombre": "Carlos Gomez",
    "categoria":        "Electricidad",
    "descripcion":      "Instalaciones electricas residenciales y comerciales",
    "tarifa_hora":      35000.0,
    "ciudad":           "Cucuta",
    "disponible":       True,
    "calificacion":     4.8,
    "num_contratos":    12
}""")

    doc.add_paragraph("Representacion como Diccionario: entidad Usuario")
    agregar_bloque_codigo(doc, """usuario = {
    "id":         "USR-001",
    "nombre":     "Juan Perez",             # str procesado con .title()
    "correo":     "juan.perez@email.com",   # str procesado con .lower()
    "contrasena": "juan123",
    "rol":        "cliente",                # validado contra TUPLA ROLES_SISTEMA
    "ciudad":     "Cucuta",                 # validado contra TUPLA CIUDADES_COBERTURA
    "telefono":   "3001234567"
}""")

    # Actividades 3 y 4
    doc.add_heading("Actividades 3 y 4. Registro y Almacenamiento de Informacion", level=2)
    doc.add_paragraph(
        "YPRI implementa el registro de informacion mediante la funcion registrar_usuario() y publicar_servicio(). "
        "En ambas funciones, los datos se solicitan al usuario mediante input(), se almacenan en un DICCIONARIO y luego "
        "se agregan a la LISTA correspondiente con .append(). Al finalizar, se muestra la cantidad total de registros con len()."
    )

    doc.add_paragraph("3.1 Registro de Usuario (cadena str, dict, list.append):")
    agregar_bloque_codigo(doc, """# Datos solicitados al usuario con validaciones defensivas
correo     = pedir_correo("Correo: ").strip().lower()         # CADENA con .lower()
nombre     = pedir_solo_letras("Nombre: ", "nombre").title() # CADENA con .title()
contrasena = input("Contrasena: ").strip()
rol        = input("Rol: ").strip().lower()                 # validado vs TUPLA ROLES_SISTEMA
ciudad     = pedir_ciudad()                                 # validado vs TUPLA CIUDADES_COBERTURA

# DICCIONARIO: representa el registro del usuario (Actividad 3)
nuevo_usuario = {
    "id":         generar_id("USR", usuarios),
    "nombre":     nombre,
    "correo":     correo,
    "contrasena": contrasena,
    "rol":        rol,
    "ciudad":     ciudad,
    "telefono":   telefono
}

# LISTA.append(): agrega el DICCIONARIO a la lista (Actividad 4)
usuarios.append(nuevo_usuario)
print(f"Total de usuarios: {len(usuarios)}")""")

    doc.add_paragraph("3.2 Registro de Servicio (dict, list.append, tupla de validacion):")
    agregar_bloque_codigo(doc, """# Datos solicitados al prestador
categoria   = pedir_categoria()    # valida contra TUPLA CATEGORIAS_SERVICIO
descripcion = pedir_texto_minimo("Descripcion: ", "descripcion", minimo=10)
tarifa      = pedir_float("Tarifa/hora: ", 10000, 500000)
ciudad      = pedir_ciudad()       # valida contra TUPLA CIUDADES_COBERTURA

# DICCIONARIO: nuevo servicio (Actividad 3)
nuevo_servicio = {
    "codigo":           nuevo_codigo,
    "prestador_nombre": usuario_sesion["nombre"],
    "categoria":        categoria,
    "descripcion":      descripcion,
    "tarifa_hora":      tarifa,
    "ciudad":           ciudad,
    "disponible":       True,
    "calificacion":     5.0
}

# LISTA.append(): agrega a la lista de servicios (Actividad 4)
servicios.append(nuevo_servicio)
print(f"Total de servicios: {len(servicios)}")""")

    # Actividad 5
    doc.add_heading("Actividad 5. Utilizacion de Tuplas en el Proyecto", level=2)
    datos_act5 = [
        ("INFORMACION REPRESENTADA:", "Cuatro conjuntos de valores fijos que el sistema necesita para validar entradas y controlar el comportamiento del programa."),
        ("VALORES:", "ROLES_SISTEMA = ('cliente', 'prestador', 'admin')\nCATEGORIAS_SERVICIO = ('Electricidad', 'Plomeria', 'Limpieza', 'Climatizacion', 'Cerrajeria')\nESTADOS_CONTRATO = ('Pendiente', 'En proceso', 'Completado', 'Cancelado')\nCIUDADES_COBERTURA = ('Cucuta', 'Cali', 'Bogota', 'Medellin', 'Bucaramanga')"),
        ("¿POR QUE ES CONVENIENTE UNA TUPLA?", "Porque estos valores son inmutables: los roles, categorias, estados y ciudades de cobertura de la plataforma NO deben cambiar durante la ejecucion del programa. Si cambiaran accidentalmente (por error en el codigo), podrian invalidar registros existentes. La tupla garantiza que estos valores permanezcan constantes. Ademas, las tuplas son mas eficientes en memoria que las listas para conjuntos de valores fijos."),
        ("FUNCION DENTRO DEL PROGRAMA:", "Se usan en funciones de validacion (pedir_categoria(), pedir_ciudad()) para verificar que el usuario ingrese solo valores permitidos. Se usa ESTADOS_CONTRATO[0] = 'Pendiente' como estado inicial de todo contrato nuevo. Se accede por indice en actualizar_estado_contrato() para asignar el nuevo estado. Se muestran en ver_estadisticas() como parte del reporte del sistema.")
    ]
    agregar_tabla_dos_columnas(doc, datos_act5)

    doc.add_paragraph("Codigo que demuestra el uso de las tuplas en YPRI:")
    agregar_bloque_codigo(doc, """# TUPLAS definidas al inicio del programa (valores inmutables)
ROLES_SISTEMA        = ("cliente", "prestador", "admin")
CATEGORIAS_SERVICIO  = ("Electricidad", "Plomeria", "Limpieza", "Climatizacion", "Cerrajeria")
ESTADOS_CONTRATO     = ("Pendiente", "En proceso", "Completado", "Cancelado")
CIUDADES_COBERTURA   = ("Cucuta", "Cali", "Bogota", "Medellin", "Bucaramanga")

# Uso 1: validar rol al registrar usuario
if rol in ROLES_SISTEMA:
    break

# Uso 2: estado inicial del contrato (acceso por indice)
nuevo_contrato["estado"] = ESTADOS_CONTRATO[0]  # -> "Pendiente"

# Uso 3: validar categoria al publicar servicio
if valor in CATEGORIAS_SERVICIO:
    return valor

# Uso 4: mostrar estados en actualizar_estado_contrato
for i, estado in enumerate(ESTADOS_CONTRATO):
    print(f"{i+1}. {estado}")
nuevo_estado = ESTADOS_CONTRATO[opcion - 1]""")

    # Actividad 6
    doc.add_heading("Actividad 6. Visualizacion de los Registros", level=2)
    doc.add_paragraph(
        "La visualizacion de registros se realiza mediante ciclos for que recorren las listas de diccionarios. "
        "Para cada elemento, se accede a sus datos usando la clave del diccionario. Guia 6: el ciclo for y continue "
        "ya existian en el proyecto; en Guia 7 se refactorizan para operar sobre lista de diccionarios en vez de listas paralelas."
    )

    doc.add_paragraph("6.1 Visualizacion del catalogo de servicios (for sobre lista de dict):")
    agregar_bloque_codigo(doc, """def listar_servicios(solo_disponibles=False):
    # CICLO FOR sobre LISTA de DICCIONARIOS
    for i, serv in enumerate(servicios):
        # GUIA 6 CONTINUE: omite servicios sin disponibilidad si aplica filtro
        if solo_disponibles and not serv["disponible"]:
            continue
        # Acceso por CLAVE al DICCIONARIO
        print(f"{serv['codigo']:<10}{serv['prestador_nombre']:<20}"
              f"{serv['categoria']:<16}${serv['tarifa_hora']:>10,.0f}")
    print(f"Total: {len(servicios)} servicios registrados.")""")

    doc.add_paragraph("6.2 Visualizacion de contratos del usuario autenticado:")
    agregar_bloque_codigo(doc, """def ver_mis_contratos():
    mis_contratos = []
    # CICLO FOR: recorre la lista de contratos (diccionarios)
    for c in contratos:
        if c["cliente_id"] == usuario_sesion["id"]:
            mis_contratos.append(c)
            print(f"{c['id']:<14}{c['servicio_nombre']:<30}"
                  f"{c['horas']:>6}${c['total']:>12,.0f}  {c['estado']}")
    print(f"Total de contratos: {len(mis_contratos)}")""")

    # Actividad 7
    doc.add_heading("Actividad 7. Consulta de un Registro", level=2)
    doc.add_paragraph(
        "La consulta de un registro especifico se implementa en dos funciones: login() (busca usuario por correo) "
        "y ver_detalle_servicio() (busca servicio por codigo). Ambas contemplan los dos casos requeridos: registro encontrado y no encontrado."
    )

    doc.add_paragraph("7.1 Consulta de usuario por correo (login):")
    agregar_bloque_codigo(doc, """def login():
    correo = pedir_correo("Correo: ")  # CADENA validada con .lower()
    contrasena = input("Contrasena: ").strip()
    # CICLO FOR sobre LISTA de DICCIONARIOS: busca por correo
    for usuario in usuarios:
        if usuario["correo"] == correo and usuario["contrasena"] == contrasena:
            usuario_sesion = usuario   # CASO 1: encontrado
            print(f"Bienvenido/a, {usuario['nombre']}!")
            return True
    # CASO 2: no encontrado
    print("[!] Correo o contrasena incorrectos.")
    return False""")

    doc.add_paragraph("7.2 Consulta de servicio por codigo:")
    agregar_bloque_codigo(doc, """def ver_detalle_servicio():
    codigo = pedir_id_registro("Codigo del servicio: ", prefijo_esperado="SERV")
    encontrado = False
    # CICLO FOR + busqueda en LISTA de DICCIONARIOS
    for serv in servicios:
        if serv["codigo"] == codigo:
            encontrado = True
            # CASO 1: encontrado - muestra los datos del diccionario
            print(f"Prestador:   {serv['prestador_nombre']}")
            print(f"Categoria:   {serv['categoria']}")
            print(f"Tarifa/hora: ${serv['tarifa_hora']:,.0f} COP")
            break  # GUIA 6 BREAK
    if not encontrado:
        # CASO 2: no encontrado
        print(f"[!] No se encontro el servicio '{codigo}'.")""")

    # Actividad 8
    doc.add_heading("Actividad 8. Modificacion de Informacion", level=2)
    doc.add_paragraph(
        "La modificacion de registros se implementa en modificar_servicio() y actualizar_estado_contrato(). En ambas funciones el programa: "
        "1) Solicita el identificador con validacion, 2) Busca el registro, 3) Verifica que exista, 4) Permite modificar campos, "
        "5) Almacena los nuevos valores directamente en el diccionario, 6) Muestra confirmacion. El identificador principal no se modifica."
    )

    doc.add_paragraph("8.1 Modificacion de servicio:")
    agregar_bloque_codigo(doc, """def modificar_servicio():
    codigo = pedir_id_registro("Codigo del servicio: ", prefijo_esperado="SERV")
    servicio_encontrado = None
    for serv in servicios:
        if serv["codigo"] == codigo:
            servicio_encontrado = serv  # referencia al diccionario
            break
    if not servicio_encontrado:
        print(f"[!] No se encontro el servicio '{codigo}'.")
        return
    # MODIFICACION de campos del DICCIONARIO con control de conservacion
    nueva_desc = input(f"Descripcion [{serv['descripcion']}]: ").strip()
    if nueva_desc:
        servicio_encontrado["descripcion"] = nueva_desc  # modifica el dict
    nueva_tarifa = input(f"Tarifa [${serv['tarifa_hora']:,.0f}]: ").strip()
    if nueva_tarifa:
        servicio_encontrado["tarifa_hora"] = float(nueva_tarifa)
    print("[OK] Servicio actualizado exitosamente.")""")

    doc.add_paragraph("8.2 Actualizacion de estado de contrato (usando TUPLA):")
    agregar_bloque_codigo(doc, """def actualizar_estado_contrato():
    id_contrato = pedir_id_registro("ID del contrato: ", prefijo_esperado="CONTR")
    contrato_encontrado = None
    for c in contratos:
        if c["id"] == id_contrato:
            contrato_encontrado = c
            break
    if not contrato_encontrado:
        print("[!] Contrato no encontrado.")
        return
    # TUPLA ESTADOS_CONTRATO: muestra opciones validas (inmutables)
    for i, estado in enumerate(ESTADOS_CONTRATO):
        print(f"{i+1}. {estado}")
    opcion = pedir_entero("Nuevo estado (1-4): ", 1, 4)
    nuevo_estado = ESTADOS_CONTRATO[opcion - 1]
    # MODIFICACION del campo en el DICCIONARIO
    contrato_encontrado["estado"] = nuevo_estado
    print(f"[OK] Estado actualizado a: '{nuevo_estado}'")""")

    # Actividad 9
    doc.add_heading("Actividad 9. Tratamiento de Cadenas en el Proyecto", level=2)
    cadenas_act9 = [
        ("CAMPO", "TRATAMIENTO APLICADO Y RAZON"),
        ("correo (login, registro)", ".strip().lower() - Elimina espacios y convierte a minusculas para evitar errores por diferencias en mayusculas. 'JUAN@EMAIL.com' y 'juan@email.com' se tratan igual."),
        ("nombre (registro usuario)", ".strip().title() - Elimina espacios extra y capitaliza cada palabra. 'jUaN peReZ' se almacena como 'Juan Perez'."),
        ("categoria (publicar servicio)", ".strip().capitalize() - Para comparar correctamente con los valores de la TUPLA CATEGORIAS_SERVICIO."),
        ("ciudad (registro, servicio)", ".strip().capitalize() - Para comparar con los valores de la TUPLA CIUDADES_COBERTURA sin errores de mayusculas."),
        ("codigo de servicio (busqueda)", ".strip().upper() - El codigo SERV-01 siempre se compara en mayusculas para evitar que 'serv-01' y 'SERV-01' sean tratados diferente."),
        ("descripcion (servicio)", ".strip() - Elimina espacios al inicio y al final para una presentacion limpia.")
    ]
    agregar_tabla_dos_columnas(doc, cadenas_act9)

    doc.add_paragraph("Codigo que demuestra el tratamiento de cadenas:")
    agregar_bloque_codigo(doc, """# Registro de usuario - cadenas con .strip(), .lower(), .title()
correo = pedir_correo("Correo: ").strip().lower()
nombre = pedir_solo_letras("Nombre: ", "nombre").strip().title()

# Busqueda - cadena con .strip().upper()
codigo = pedir_id_registro("Codigo del servicio: ", prefijo_esperado="SERV")

# Validacion de categoria - cadena con .strip().capitalize()
def pedir_categoria():
    while True:
        valor = input("Categoria: ").strip().capitalize()
        if valor in CATEGORIAS_SERVICIO:
            return valor
        print("[!] Categoria invalida.")""")

    # Actividad 10
    doc.add_heading("Actividad 10. Integracion con Ciclos", level=2)
    doc.add_paragraph(
        "YPRI implementa menus con ciclo while que mantienen cada modulo activo hasta que el usuario seleccione salir. "
        "El sistema tiene tres menus por rol: cliente, prestador y administrador, cada uno controlado por su propio while. "
        "Guia 6: el ciclo while del menu ya existia; Guia 7 lo extiende con menus por rol y control modular."
    )
    doc.add_paragraph("Menu principal (while + break - Guia 6 existente):")
    agregar_bloque_codigo(doc, """def main():
    # CICLO WHILE: sistema activo hasta que el usuario elija salir
    while True:
        print("1. Iniciar sesion")
        print("2. Registrarse")
        print("0. Salir")
        opcion = input("Seleccione: ").strip()
        if opcion == "1":
            if login():
                # Redirige al menu segun ROL (cadena en diccionario)
                if usuario_sesion["rol"] == "cliente":
                    menu_cliente()
                elif usuario_sesion["rol"] == "prestador":
                    menu_prestador()
                elif usuario_sesion["rol"] == "admin":
                    menu_admin()
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "0":
            break  # BREAK: sale del while principal""")

    # Actividad 11
    doc.add_heading("Actividad 11. Integracion de las Estructuras de Datos y Arquitectura Modular", level=2)
    doc.add_paragraph(
        "Para garantizar calidad de codigo, escalabilidad y buenas practicas de desarrollo, el aplicativo YPRI "
        "fue organizado tanto de forma unificada como en una arquitectura modular completa dividida en paquetes logicos (core, data, modules):"
    )
    modulos_act11 = [
        ("Estructura / Capa", "Uso e Implementacion en YPRI"),
        ("Cadenas (str)", "Almacenar y procesar datos textuales. Se aplica .strip(), .lower(), .title(), .upper(), .capitalize(). Ubicacion: core/validaciones.py, modules/auth.py."),
        ("Listas (list)", "Almacenar colecciones de registros: usuarios[], servicios[], contratos[], calificaciones[]. Se usa .append(), len(). Ubicacion: data/database.py, modules/*."),
        ("Tuplas (tuple)", "ROLES_SISTEMA, CATEGORIAS_SERVICIO, ESTADOS_CONTRATO, CIUDADES_COBERTURA. Valores fijos e inmutables para validacion y control. Ubicacion: core/constantes.py."),
        ("Diccionarios (dict)", "Cada usuario, servicio, contrato y calificacion es un dict {clave: valor}. Se manipulan atributos in-place de forma eficiente. Ubicacion: data/database.py, modules/*."),
        ("Ciclos (while, for)", "while: menus por rol y validaciones repetitivas. for: recorridos de colecciones para listar, buscar o auditar. Ubicacion: main.py, modules/*."),
        ("Condiciones (if/elif/else)", "Control de acceso segun rol, filtros en listados, validaciones defensivas y reglas de negocio en todos los modulos.")
    ]
    agregar_tabla_dos_columnas(doc, modulos_act11)

    # Actividad 12
    doc.add_heading("Actividad 12. Requerimientos Funcionales del Proyecto", level=2)
    rf_act12 = [
        ("REQUERIMIENTO FUNCIONAL 1:", "RF-01: Registro y publicacion de servicios. El sistema permite a los prestadores publicar nuevos servicios con datos como categoria, descripcion, tarifa y ciudad. ESTADO: IMPLEMENTADO. Estructuras: dict, list.append, tuple, str, while."),
        ("REQUERIMIENTO FUNCIONAL 2:", "RF-02: Busqueda, cotizacion y contratacion de servicios. El cliente puede ver el catalogo, seleccionar un servicio, calcular el costo total con IVA (19%) y generar un contrato. ESTADO: IMPLEMENTADO. Estructuras: list, dict, tuple, float, str."),
        ("REQUERIMIENTO FUNCIONAL 3:", "RF-03: Gestion de contratos y calificaciones. El prestador/admin puede actualizar el estado del contrato y el cliente puede calificar el servicio una vez completado con recalculo ponderado de rating. ESTADO: IMPLEMENTADO. Estructuras: dict, list.append, tuple, for, bool.")
    ]
    agregar_tabla_dos_columnas(doc, rf_act12)

    # Actividad 13
    doc.add_heading("Actividad 13. Pruebas del Aplicativo (Guia 7)", level=2)
    pruebas_act13 = [
        ("Prueba 1: Login + Ver catalogo + Solicitar servicio (contrato con IVA)", "Resultado obtenido: Login exitoso: 'Bienvenido/a, Juan Perez!'. Catalogo muestra 5 servicios. Contrato CONTR-002 creado con TOTAL calculado. Estado = 'Pendiente'. Total contratos: 2."),
        ("Prueba 2: Registro de nuevo usuario + Login", "Resultado obtenido: Usuario 'Maria Lopez' registrado con ID USR-004. len(usuarios) = 4. Login exitoso. Menu cliente activado correctamente."),
        ("Prueba 3: Prestador publica un nuevo servicio y lo modifica", "Resultado obtenido: Servicio SERV-006 publicado exitosamente. Descripcion y tarifa actualizadas correctamente. Confirmacion mostrada con los nuevos valores."),
        ("Prueba 4: Admin: ver usuarios, estadisticas, actualizar contrato", "Resultado obtenido: 3 usuarios listados correctamente. Estadisticas calculadas: 5 servicios, 1 contrato, ingresos $179.400. TUPLAS visibles en estadisticas. Estado actualizado a 'Cancelado'."),
        ("Prueba 5: Cliente califica un servicio completado", "Resultado obtenido: Estado actualizado a 'Completado' usando ESTADOS_CONTRATO[2]. Calificacion CALIF-002 creada. len(calificaciones) = 2. Promedio recalculado correctamente en el servicio SERV-01.")
    ]
    agregar_tabla_dos_columnas(doc, pruebas_act13)

    # =========================================================================
    # SECCION II: GUIA DE APRENDIZAJE N. 9 - MATRICES EN PYTHON
    # =========================================================================
    doc.add_page_break()
    h_s2 = doc.add_heading("SECCION II: GUIA DE APRENDIZAJE N. 9 - MATRICES EN PYTHON: CREACION, RECORRIDO Y OPERACIONES", level=1)
    h_s2.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph(
        "En esta segunda parte del documento se incorpora la totalidad de las actividades, conceptos y operaciones "
        "exigidas en la Guia de Aprendizaje N. 9 ('Matrices en Python: Creacion, Recorrido y Operaciones'), articuladas "
        "dentro del mismo software YPRI sin crear aplicativos independientes, siguiendo el mismo rigor tecnico y academico."
    )

    # Actividad 14 (Guia 9 - Actividad 1)
    doc.add_heading("Actividad 14. Identificacion e Implementacion de Matrices en el Proyecto (Guia 9 - Actividad 1)", level=2)
    doc.add_paragraph(
        "Una matriz es una estructura de datos bidimensional que permite organizar informacion en filas y columnas. "
        "En Python, se representa como una lista que contiene otras listas. Para responder a las necesidades de la plataforma YPRI, "
        "se definieron e implementaron dos matrices en el modulo data/database.py:"
    )

    matriz_def = [
        ("NOMBRE DE LA MATRIZ 1:", "matriz_ventas_semanales"),
        ("DIMENSIONES MATRIZ 1:", "5 Filas (Categorias) x 6 Columnas (Dias laborales: Lunes a Sabado). Total: 30 celdas."),
        ("TIPO DE DATO CONTENIDO:", "float (valores monetarios de facturacion en pesos colombianos - COP)."),
        ("UTILIDAD EN EL SISTEMA:", "Monitorear la distribucion semanal de ingresos por linea de servicio y detectar dias de mayor y menor facturacion."),
        ("NOMBRE DE LA MATRIZ 2:", "matriz_ventas_ciudades"),
        ("DIMENSIONES MATRIZ 2:", "5 Filas (Categorias) x 5 Columnas (Ciudades de cobertura: Cucuta, Cali, Bogota, Medellin, Bucaramanga)."),
        ("PROPIEDAD MATEMATICA:", "MATRIZ CUADRADA (5x5). Igual numero de filas y columnas, permitiendo extraer la diagonal principal (i == j)."),
        ("UTILIDAD EN EL SISTEMA:", "Analizar la cobertura y demanda territorial del servicio en cada ciudad de Colombia.")
    ]
    agregar_tabla_dos_columnas(doc, matriz_def)

    doc.add_paragraph("Implementacion de las Matrices en data/database.py:")
    agregar_bloque_codigo(doc, """# MATRIZ 1: Facturacion semanal por Categoria y Dia (5 filas x 6 columnas)
matriz_ventas_semanales = [
    #  Lunes     Martes    Miercoles   Jueves    Viernes    Sabado
    [350000.0, 420000.0, 280000.0, 510000.0, 600000.0, 450000.0],  # Fila 0: Electricidad
    [280000.0, 310000.0, 390000.0, 250000.0, 480000.0, 320000.0],  # Fila 1: Plomeria
    [180000.0, 220000.0, 250000.0, 290000.0, 380000.0, 420000.0],  # Fila 2: Limpieza
    [450000.0, 520000.0, 380000.0, 490000.0, 650000.0, 710000.0],  # Fila 3: Climatizacion
    [220000.0, 190000.0, 260000.0, 310000.0, 410000.0, 300000.0]   # Fila 4: Cerrajeria
]

# MATRIZ 2: Demanda por Categoria y Ciudad (5 filas x 5 columnas -> MATRIZ CUADRADA)
matriz_ventas_ciudades = [
    #  Cucuta     Cali      Bogota    Medellin  Bucaramanga
    [450000.0, 380000.0, 850000.0, 720000.0, 210000.0],  # Fila 0: Electricidad
    [320000.0, 290000.0, 640000.0, 510000.0, 180000.0],  # Fila 1: Plomeria
    [250000.0, 210000.0, 490000.0, 430000.0, 160000.0],  # Fila 2: Limpieza
    [580000.0, 620000.0, 950000.0, 890000.0, 310000.0],  # Fila 3: Climatizacion
    [290000.0, 240000.0, 530000.0, 470000.0, 150000.0]   # Fila 4: Cerrajeria
]""")

    # Actividad 15 (Guia 9 - Actividad 2)
    doc.add_heading("Actividad 15. Registro y Consulta de Informacion en la Matriz (Guia 9 - Actividad 2)", level=2)
    doc.add_paragraph(
        "Se implementaron funciones especializadas en modules/matrices.py y data/database.py para consultar y registrar "
        "datos en las matrices, cubriendo el acceso por celda matriz[i][j], consulta de fila completa matriz[i], consulta de columna "
        "y modificacion con validacion defensiva contra valores negativos:"
    )

    consultas_mat = [
        ("MECANISMO DE ACCESO INDEXADO:", "Para consultar o modificar un elemento se indica primero el indice de fila [i] y despues el de columna [j]: matriz[i][j]."),
        ("CONSULTA DE CELDA INDIVIDUAL:", "consultar_celda(matriz, fila_idx, col_idx) retorna el valor exacto en COP de esa posicion."),
        ("CONSULTA DE FILA COMPLETA:", "consultar_fila_especifica() extrae matriz[i], calcula el subtotal de la fila y el promedio de la categoria."),
        ("CONSULTA DE COLUMNA COMPLETA:", "consultar_columna_especifica() itera verticalmente sumando los valores de todas las categorias para un dia o ciudad dada."),
        ("MODIFICACION DE INFORMACION:", "modificar_celda(matriz, i, j, nuevo_valor) valida que los indices esten dentro de rango y que el valor sea >= 0.")
    ]
    agregar_tabla_dos_columnas(doc, consultas_mat)

    doc.add_paragraph("Codigo de Acceso, Consulta y Modificacion de Celdas:")
    agregar_bloque_codigo(doc, """def consultar_celda(matriz, fila_idx, col_idx):
    # Acceso indexado directo: fila [i], columna [j]
    return matriz[fila_idx][col_idx]

def modificar_celda(matriz, fila_idx, col_idx, nuevo_valor):
    # Validacion defensiva de limites de indice
    if fila_idx < 0 or fila_idx >= len(matriz):
        return False
    if col_idx < 0 or col_idx >= len(matriz[fila_idx]):
        return False
    # Modificacion directa de la celda
    matriz[fila_idx][col_idx] = float(nuevo_valor)
    return True""")

    # Actividad 16 (Guia 9 - Actividad 3)
    doc.add_heading("Actividad 16. Recorrido de Filas y Columnas con Ciclos Anidados (Guia 9 - Actividad 3)", level=2)
    doc.add_paragraph(
        "Para recorrer una matriz se utilizan ciclos for anidados. El ciclo externo recorre las filas y el ciclo interno "
        "los elementos de cada columna en esa fila. En YPRI se implementaron tanto el recorrido secuencial directo como "
        "el recorrido indexado por rangos y el recorrido vertical por columnas:"
    )

    doc.add_paragraph("Codigo del Recorrido Tabular con Ciclos Anidados (mostrar_matriz_tabulada):")
    agregar_bloque_codigo(doc, """def mostrar_matriz_tabulada(matriz, nombres_filas, nombres_columnas, titulo):
    print(f"=== {titulo} ===")
    
    # CICLO EXTERNO: recorre las filas de la matriz por indice i
    for i in range(len(matriz)):
        nombre_categoria = nombres_filas[i]
        print(f"{nombre_categoria:<18}", end="")
        
        # CICLO INTERNO: recorre cada columna de la fila actual por indice j
        for j in range(len(matriz[i])):
            valor_celda = matriz[i][j]
            print(f"${valor_celda:>12,.0f}", end=" ")
        
        # Total acumulado por fila
        print(f"| Total: ${sum(matriz[i]):>12,.0f}")
    
    # Suma vertical por columnas con ciclos anidados invertidos
    totales_col = calcular_totales_columnas(matriz)
    print("TOTAL COLUMNAS:    ", end="")
    for tot in totales_col:
        print(f"${tot:>12,.0f}", end=" ")
    print()""")

    # Actividad 17 (Guia 9 - Actividad 4)
    doc.add_heading("Actividad 17. Operaciones Matematicas y Procesamiento Util (Guia 9 - Actividad 4)", level=2)
    doc.add_paragraph(
        "Las matrices permiten realizar operaciones matematicas de alto valor analitico sobre sus elementos. "
        "En YPRI se incorporaron cinco calculos matematicos fundamentales:"
    )

    operaciones_mat = [
        ("1. TOTAL POR FILA (CATEGORIA):", "calcular_totales_filas(matriz) -> sum(matriz[i]). Calcula la facturacion total por cada categoria de servicio."),
        ("2. TOTAL POR COLUMNA (DIA/CIUDAD):", "calcular_totales_columnas(matriz) -> suma vertical con ciclos for anidados para cada columna j."),
        ("3. TOTAL GENERAL DE LA PLATAFORMA:", "calcular_total_general(matriz) -> acumulador con ciclos for anidados sobre toda la matriz bidimensional."),
        ("4. PROMEDIO POR REGISTRO:", "calcular_promedio_general(matriz) -> total_general / (filas * columnas). Media de venta por cada celda."),
        ("5. ANALISIS DE EXTREMOS Y LIDERES:", "analizar_rendimiento_matriz() -> detecta categoria con mayor venta, dia record y la celda individual maxima."),
        ("6. MATRICES ESPECIALES:", "es_matriz_cuadrada(), crear_matriz_nula(), crear_matriz_identidad() y extraccion de diagonal principal.")
    ]
    agregar_tabla_dos_columnas(doc, operaciones_mat)

    doc.add_paragraph("Implementacion de Operaciones Matematicas en modules/matrices.py:")
    agregar_bloque_codigo(doc, """# Calculo vertical por columna usando ciclos anidados (Guia 9 - Seccion 1.5)
def calcular_totales_columnas(matriz):
    totales = []
    num_columnas = len(matriz[0])
    num_filas = len(matriz)
    
    # Ciclo externo recorre columnas
    for j in range(num_columnas):
        total_col = 0.0
        # Ciclo interno recorre filas acumulando verticalmente
        for i in range(num_filas):
            total_col += matriz[i][j]
        totales.append(total_col)
    return totales

# Total general y promedio por registro
def calcular_total_general(matriz):
    total = 0.0
    for fila in matriz:
        for valor in fila:
            total += valor
    return total

def calcular_promedio_general(matriz):
    total = calcular_total_general(matriz)
    total_registros = len(matriz) * len(matriz[0])
    return total / total_registros if total_registros > 0 else 0.0""")

    doc.add_paragraph("Implementacion de Matrices Especiales (Guia 9 - Seccion 1.6):")
    agregar_bloque_codigo(doc, """# Matriz cuadrada (igual numero de filas y columnas)
def es_matriz_cuadrada(matriz):
    return all(len(fila) == len(matriz) for fila in matriz)

# Matriz nula (todos los elementos son cero)
def crear_matriz_nula(filas, columnas):
    return [[0.0 for _ in range(columnas)] for _ in range(filas)]

# Matriz identidad (1.0 en diagonal i == j, 0.0 en el resto)
def crear_matriz_identidad(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

# Extraccion de la diagonal principal
def extraer_diagonal_principal(matriz):
    return [matriz[i][i] for i in range(min(len(matriz), len(matriz[0])))]""")

    # Actividad 18 (Guia 9 - Actividad 5)
    doc.add_heading("Actividad 18. Integracion de Matrices con las Operaciones Existentes (Guia 9 - Actividad 5)", level=2)
    doc.add_paragraph(
        "En cumplimiento de la pauta 'Las actividades deben desarrollarse dentro del mismo proyecto, evitando crear aplicaciones independientes', "
        "el modulo de matrices fue integrado transversalmente en todas las capas del sistema YPRI:"
    )

    integracion_datos = [
        ("CAPA DE DATOS (backend/data/database.py):", "Persistencia en memoria de matriz_ventas_semanales y matriz_ventas_ciudades vinculadas al ciclo de vida del software."),
        ("MODULO DE NEGOCIO (backend/modules/matrices.py):", "Contiene la logica de analisis matricial, menus de consulta y sincronizacion automatica con contratos."),
        ("PANEL ADMINISTRATIVO (backend/modules/admin.py):", "Las metricas del administrador integran el total general de la matriz y la categoria lider junto con los vectores."),
        ("MENU CONSOLA CLI (backend/main.py):", "Opcion directa para consultar matrices, editar celdas y ejecutar la simulacion guiada."),
        ("INTERFAZ GRAFICA (backend/app_gui.py):", "Pestana 'Matrices' en Tkinter con edicion de celdas en vivo y visor de matrices especiales."),
        ("FRONTEND WEB VERCEL (web/app/page.tsx):", "Aplicacion moderna en Next.js y Tailwind CSS con tabla matricial interactiva, recalculo en tiempo real y soporte movil.")
    ]
    agregar_tabla_dos_columnas(doc, integracion_datos)

    doc.add_paragraph("Sincronizacion de Contratos Reales con la Matriz de Ventas:")
    agregar_bloque_codigo(doc, """def sincronizar_matriz_con_contratos_reales():
    cat_to_idx = {cat.lower(): idx for idx, cat in enumerate(CATEGORIAS_SERVICIO)}
    total_sumado = 0.0
    contratos_procesados = 0

    for c in contratos:
        if c.get("estado") == "Completado":
            cod_serv = c.get("servicio_codigo")
            serv = next((s for s in servicios if s["codigo"] == cod_serv), None)
            if serv:
                cat = serv["categoria"].lower()
                if cat in cat_to_idx:
                    cat_idx = cat_to_idx[cat]
                    # Se acredita la facturacion del contrato a la columna correspondiente
                    matriz_ventas_semanales[cat_idx][4] += float(c["total"])
                    total_sumado += float(c["total"])
                    contratos_procesados += 1
    return contratos_procesados, total_sumado""")

    # Actividad 19 (Ejercicio Practico Guiado Seccion 2)
    doc.add_heading("Actividad 19. Desarrollo de la Seccion 2 de la Guia 9 (Ejercicio Practico Guiado 3x3)", level=2)
    doc.add_paragraph(
        "Se implemento el ejercicio academico de la Seccion 2 de la guia que registra las ventas de 3 productos "
        "durante 3 dias (Lunes, Martes y Miercoles), utilizando validacion defensiva while True + try-except y control de valores no negativos:"
    )

    doc.add_paragraph("Codigo del Ejercicio Guiado (ejecutar_ejercicio_practico_guia9):")
    agregar_bloque_codigo(doc, """productos = ["Producto A", "Producto B", "Producto C"]
dias = ["Lunes", "Martes", "Miercoles"]
ventas = []

# REGISTRO CON VALIDACION DEFENSIVA (Guia 9 - Pagina 4)
for producto in productos:
    fila = []
    print(f"Registro de {producto}")
    for dia in dias:
        while True:
            try:
                valor = float(input(f"Venta del {dia}: $"))
                if valor < 0:
                    print("El valor no puede ser negativo.")
                    continue
                fila.append(valor)
                break
            except ValueError:
                print("Ingrese un valor numerico valido.")
    ventas.append(fila)

# TOTAL POR PRODUCTO (Suma de filas)
for i in range(len(ventas)):
    total_producto = sum(ventas[i])
    print(f"{productos[i]}: ${total_producto:,.2f}")

# TOTAL POR DIA (Suma de columnas con ciclos anidados)
for j in range(len(dias)):
    total_dia = 0.0
    for i in range(len(productos)):
        total_dia += ventas[i][j]
    print(f"{dias[j]}: ${total_dia:,.2f}")

# TOTAL GENERAL Y PROMEDIO
total_general = sum(sum(fila) for fila in ventas)
promedio = total_general / (len(productos) * len(dias))
print(f"Total general: ${total_general:,.2f} | Promedio: ${round(promedio, 2):,.2f}")""")

    doc.add_paragraph("Resultados Obtenidos de la Ejecucion del Ejercicio Guiado:")
    tabla_ej_data = [
        ("Producto", "Lunes", "Martes", "Miercoles", "Total Producto"),
        ("Producto A", "$150,000.00", "$200,000.00", "$180,000.00", "$530,000.00"),
        ("Producto B", "$120,000.00", "$250,000.00", "$300,000.00", "$670,000.00"),
        ("Producto C", "$175,000.00", "$190,000.00", "$220,000.00", "$585,000.00"),
        ("TOTAL DIA", "$445,000.00", "$640,000.00", "$700,000.00", "$1,785,000.00")
    ]
    t_ej = doc.add_table(rows=5, cols=5)
    t_ej.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(tabla_ej_data):
        for c_idx, val in enumerate(row):
            cell = t_ej.cell(r_idx, c_idx)
            cell.text = val
            if r_idx == 0:
                set_cell_background(cell, "0F172A")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == 4 or c_idx == 4:
                set_cell_background(cell, "F1F5F9")
                cell.paragraphs[0].runs[0].font.bold = True
    doc.add_paragraph()

    # Actividad 20 (Pruebas Guia 9)
    doc.add_heading("Actividad 20. Pruebas y Evidencias de Ejecucion de Matrices (Guia 9)", level=2)
    pruebas_act20 = [
        ("Prueba 6: Visualizacion de Matriz Semanal (5x6) y Calculo de Totales", "Resultado obtenido: Matriz mostrada con 5 categorias y 6 dias. Total general: $11,270,000 COP. Promedio por celda: $375,667 COP. Totales por fila y columna calculados correctamente."),
        ("Prueba 7: Modificacion interactiva de celda matriz[i][j]", "Resultado obtenido: Celda matriz[0][1] (Electricidad - Martes) modificada de $420,000 a $490,000 COP. Recalculo inmediato del total general a $11,340,000 COP."),
        ("Prueba 8: Consulta de Fila Completa y Columna Completa", "Resultado obtenido: Fila de Climatizacion consultada con total de $3,200,000 COP y promedio de $533,333 COP. Columna de Viernes consultada con recaudacion de $2,520,000 COP."),
        ("Prueba 9: Verificacion de Matrices Especiales (Cuadrada, Nula, Identidad)", "Resultado obtenido: Matriz de ciudades validada como cuadrada 5x5 (es_matriz_cuadrada = True). Diagonal principal extraida. Matrices nula e identidad 3x3 generadas correctamente."),
        ("Prueba 10: Sincronizacion de Contratos Completados con la Matriz", "Resultado obtenido: Contrato CONTR-101 completado por $208,250 COP acreditado a la matriz semanal en la categoria Electricidad. Sincronizacion confirmada.")
    ]
    agregar_tabla_dos_columnas(doc, pruebas_act20)

    # Repositorio
    doc.add_heading("Repositorio del Proyecto en GitHub", level=2)
    repo_datos = [
        ("ENLACE AL REPOSITORIO:", "https://github.com/JannPi10/YPRI.git"),
        ("RAMA PRINCIPAL:", "main"),
        ("USUARIO PROPIETARIO:", "JannPi10"),
        ("ORGANIZACION DEL PROYECTO:", "backend/ (Python CLI y GUI), web/ (Frontend Next.js en Vercel), documents/ (Documentos formales y guias)."),
        ("HISTORIAL DE COMMITS ACTUALIZADO:", "1. feat(core): constantes y validaciones defensivas\n2. feat(data): persistencia en memoria y vectores base\n3. feat(auth): autenticacion y control de sesion\n4. feat(servicios): catalogo y busquedas de vector\n5. feat(contratos): cotizaciones con IVA (19%)\n6. feat(calificaciones): resenas y reputacion\n7. feat(matrices): creacion, recorrido y operaciones de matrices bidimensionales (Guia 9)\n8. feat(matrices-especiales): soporte para matrices cuadradas, nulas e identidad\n9. feat(gui): visor interactivo de matrices en Tkinter\n10. feat(web): plataforma moderna responsive en Next.js desplegable en Vercel\n11. docs: informe academico consolidado de entrega (Guias 7 y 9)")
    ]
    agregar_tabla_dos_columnas(doc, repo_datos)

    # Guardar Word
    salida_docx = os.path.join(os.path.dirname(__file__), "ENTREGA_GUIA_9_YPRI.docx")
    doc.save(salida_docx)
    print(f"Documento Word guardado exitosamente en: {salida_docx}")

    # Guardar Markdown consolidado
    salida_md = os.path.join(os.path.dirname(__file__), "DOCUMENTACION_CONSOLIDADA_YPRI.md")
    # We will write the markdown file as well
    return salida_docx, salida_md

if __name__ == "__main__":
    generar_documento_completo()
