"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos
Integrantes: Jann Pierre Ortiz Zambrano y Josue David Rincon Palomino
Institucion: Fundacion de Estudios Superiores Comfanorte (FESC) - 2026
========================================================================================
GUIA DE APRENDIZAJE N. 7: CADENAS, LISTAS, TUPLAS Y DICCIONARIOS EN PYTHON

Estructuras de datos aplicadas:
- Cadenas (str): codigos, nombres, correos, contrasenas, categorias, estados
- Listas  (list): usuarios[], servicios[], contratos[], calificaciones[]
  * Guia 5: listas paralelas para datos de servicios y contratos [YA EXISTIA]
  * Guia 6: listas con ciclos for, while, break, continue       [YA EXISTIA]
  * Guia 7: lista de diccionarios (registros completos)         [REFACTORIZADO]
- Tuplas (tuple): ROLES_SISTEMA, CATEGORIAS_SERVICIO, ESTADOS_CONTRATO,
                  CIUDADES_COBERTURA - valores fijos que no cambian en ejecucion
- Diccionarios (dict): cada usuario, servicio y contrato como dict {clave: valor}
- Ciclos: while (menus, validaciones), for (recorridos, busquedas)  [YA EXISTIA]
- Condiciones: if/elif/else con operadores logicos                  [YA EXISTIA]
========================================================================================
"""

# ============================================================
# TUPLAS: valores fijos definidos para el sistema
# GUIA 7 - ACTIVIDAD 5: tuplas con informacion que NO cambia
# durante la ejecucion del programa
# ============================================================

# TUPLA: roles posibles en el sistema (no deben cambiar)
ROLES_SISTEMA = ("cliente", "prestador", "admin")

# TUPLA: categorias de servicio validas en YPRI (fijas)
# Guia 6: CATEGORIAS_VALIDAS era una lista; ahora es tupla porque son valores inmutables
CATEGORIAS_SERVICIO = ("Electricidad", "Plomeria", "Limpieza", "Climatizacion", "Cerrajeria")

# TUPLA: estados posibles de un contrato (no modificables en el tiempo)
ESTADOS_CONTRATO = ("Pendiente", "En proceso", "Completado", "Cancelado")

# TUPLA: ciudades de cobertura de la plataforma (predefinidas)
CIUDADES_COBERTURA = ("Cucuta", "Cali", "Bogota", "Medellin", "Bucaramanga")


# ============================================================
# LISTAS DE DICCIONARIOS: datos del sistema
# GUIA 7 - ACTIVIDADES 3 y 4:
#   - Cada registro es un DICCIONARIO {clave: valor}
#   - Todos los registros se almacenan en LISTAS
# ============================================================

# LISTA de usuarios registrados (cada usuario es un DICCIONARIO)
# GUIA 5: existian listas paralelas; GUIA 7 refactoriza a lista de dicts
usuarios = [
    {
        "id": "USR-001",
        "nombre": "Juan Perez",
        "correo": "juan.perez@email.com",
        "contrasena": "juan123",
        "rol": "cliente",       # CADENA: dato textual del rol
        "ciudad": "Cucuta",
        "telefono": "3001234567"
    },
    {
        "id": "USR-002",
        "nombre": "Carlos Gomez",
        "correo": "carlos.gomez@email.com",
        "contrasena": "carlos456",
        "rol": "prestador",
        "ciudad": "Cucuta",
        "telefono": "3109876543"
    },
    {
        "id": "USR-003",
        "nombre": "Admin YPRI",
        "correo": "admin@ypri.com",
        "contrasena": "admin2026",
        "rol": "admin",
        "ciudad": "Cucuta",
        "telefono": "3200000000"
    }
]

# LISTA de servicios publicados (cada servicio es un DICCIONARIO)
# GUIA 5/6: existian listas paralelas; GUIA 7 refactoriza a lista de dicts
servicios = [
    {
        "codigo": "SERV-01",
        "prestador_id": "USR-002",
        "prestador_nombre": "Carlos Gomez",
        "categoria": "Electricidad",        # CADENA: valor de texto
        "descripcion": "Instalaciones electricas residenciales y comerciales",
        "tarifa_hora": 35000.0,
        "ciudad": "Cucuta",
        "disponible": True,
        "calificacion": 4.8,
        "num_contratos": 12
    },
    {
        "codigo": "SERV-02",
        "prestador_id": "USR-002",
        "prestador_nombre": "Marta Rodriguez",
        "categoria": "Plomeria",
        "descripcion": "Reparacion de tuberias, grifos y sistemas hidraulicos",
        "tarifa_hora": 30000.0,
        "ciudad": "Cucuta",
        "disponible": True,
        "calificacion": 4.5,
        "num_contratos": 8
    },
    {
        "codigo": "SERV-03",
        "prestador_id": "USR-002",
        "prestador_nombre": "Andres Silva",
        "categoria": "Climatizacion",
        "descripcion": "Mantenimiento y reparacion de aires acondicionados",
        "tarifa_hora": 45000.0,
        "ciudad": "Cucuta",
        "disponible": False,
        "calificacion": 5.0,
        "num_contratos": 5
    },
    {
        "codigo": "SERV-04",
        "prestador_id": "USR-002",
        "prestador_nombre": "Jorge Mendoza",
        "categoria": "Cerrajeria",
        "descripcion": "Apertura de puertas, cambio de chapas y cerraduras",
        "tarifa_hora": 38000.0,
        "ciudad": "Cucuta",
        "disponible": True,
        "calificacion": 4.7,
        "num_contratos": 15
    },
    {
        "codigo": "SERV-05",
        "prestador_id": "USR-002",
        "prestador_nombre": "Sandra Rios",
        "categoria": "Limpieza",
        "descripcion": "Limpieza profunda de hogares y oficinas",
        "tarifa_hora": 25000.0,
        "ciudad": "Cucuta",
        "disponible": True,
        "calificacion": 4.3,
        "num_contratos": 20
    }
]

# LISTA de contratos realizados (cada contrato es un DICCIONARIO)
contratos = [
    {
        "id": "CONTR-101",
        "cliente_id": "USR-001",
        "cliente_nombre": "Juan Perez",
        "servicio_codigo": "SERV-01",
        "servicio_nombre": "Electricidad - Carlos Gomez",
        "horas": 5,
        "tarifa_hora": 35000.0,
        "total": 179400.0,      # incluye IVA
        "estado": "Completado", # CADENA: estado del contrato
        "calificacion": 4.8,
        "comentario": "Excelente trabajo, muy puntual"
    }
]

# LISTA de calificaciones/resenas (cada una es un DICCIONARIO)
calificaciones = [
    {
        "id": "CALIF-001",
        "contrato_id": "CONTR-101",
        "cliente_nombre": "Juan Perez",
        "servicio_codigo": "SERV-01",
        "puntuacion": 4.8,
        "comentario": "Excelente trabajo, muy puntual",
        "fecha": "18/09/2026"
    }
]

# Variable global: usuario autenticado en la sesion actual
usuario_sesion = None


# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def separador(caracter="-", largo=72):
    print(caracter * largo)


def mostrar_encabezado(subtitulo="SISTEMA DE SERVICIOS A DOMICILIO"):
    separador("=")
    print("           YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO")
    print(f"              {subtitulo}")
    separador("=")


# ---- VALIDACIONES (Guia 6: ciclos while de validacion) ----

def pedir_sn(prompt):
    """Solo acepta 's' o 'n'. Rechaza cualquier otro valor."""
    while True:
        resp = input(prompt).strip().lower()
        if resp in ("s", "n"):
            return resp
        print("[!] Solo se acepta 's' para Si o 'n' para No.")


def pedir_solo_letras(prompt, campo):
    """Exige que el valor contenga al menos una letra."""
    while True:
        valor = input(prompt).strip()
        if valor == "":
            print(f"[!] El campo '{campo}' no puede estar vacio.")
            continue
        tiene_letra = any(c.isalpha() for c in valor)
        if not tiene_letra:
            print(f"[!] '{campo}' debe contener letras, no solo numeros o simbolos.")
            continue
        return valor


def pedir_entero(prompt, minimo, maximo):
    """Valida que la entrada sea un entero dentro del rango indicado."""
    while True:
        try:
            val = int(input(prompt).strip())
            if val < minimo or val > maximo:
                print(f"[!] Ingrese un numero entre {minimo} y {maximo}.")
                continue
            return val
        except ValueError:
            print("[!] Ingrese un numero entero valido.")


def pedir_float(prompt, minimo, maximo):
    """Valida que la entrada sea un numero decimal en el rango indicado."""
    while True:
        try:
            val = float(input(prompt).strip())
            if val < minimo or val > maximo:
                print(f"[!] El valor debe estar entre {minimo} y {maximo}.")
                continue
            return val
        except ValueError:
            print("[!] Ingrese un valor numerico valido.")


def pedir_categoria():
    """Muestra las categorias validas (TUPLA) y valida la seleccion."""
    # TUPLA CATEGORIAS_SERVICIO: usada aqui para validar y mostrar opciones
    print(f"  Categorias disponibles: {', '.join(CATEGORIAS_SERVICIO)}")
    while True:
        valor = input("  Categoria: ").strip().capitalize()
        if valor in CATEGORIAS_SERVICIO:
            return valor
        print(f"[!] Categoria invalida. Opciones: {', '.join(CATEGORIAS_SERVICIO)}")


def pedir_ciudad():
    """Muestra las ciudades validas (TUPLA) y valida la seleccion."""
    # TUPLA CIUDADES_COBERTURA: usada para validar la ciudad ingresada
    print(f"  Ciudades disponibles: {', '.join(CIUDADES_COBERTURA)}")
    while True:
        valor = input("  Ciudad: ").strip().capitalize()
        if valor in CIUDADES_COBERTURA:
            return valor
        print(f"[!] Ciudad invalida. Opciones: {', '.join(CIUDADES_COBERTURA)}")


def pedir_correo(prompt):
    """Valida que el correo tenga formato minimo: contiene @ y un punto despues del @."""
    while True:
        correo = input(prompt).strip().lower()
        if correo == "":
            print("[!] El correo no puede estar vacio.")
            continue
        partes = correo.split("@")
        if len(partes) == 2 and partes[0] and "." in partes[1] and partes[1].index(".") > 0:
            return correo
        print("[!] Ingrese un correo valido (ej. nombre@dominio.com).")


def pedir_texto_minimo(prompt, campo, minimo=10):
    """
    Solicita un texto con longitud minima, que no sea solo espacios
    y que contenga al menos una letra.
    """
    while True:
        valor = input(prompt).strip()
        if len(valor) < minimo:
            print(f"[!] '{campo}' debe tener al menos {minimo} caracteres.")
            continue
        if not any(c.isalpha() for c in valor):
            print(f"[!] '{campo}' debe contener al menos una letra.")
            continue
        return valor


def pedir_id_registro(prompt, prefijo_esperado=None):
    """
    Solicita un ID de registro (CONTR-XXX, SERV-XXX, etc.).
    Rechaza entradas vacias. Si se indica prefijo_esperado, valida el formato.
    Devuelve None si el usuario ingresa '0'.
    """
    while True:
        valor = input(prompt).strip().upper()
        if valor == "0":
            return None
        if valor == "":
            print("[!] El ID no puede estar vacio. Ingrese un ID valido o '0' para cancelar.")
            continue
        if prefijo_esperado and not valor.startswith(prefijo_esperado):
            print(f"[!] El ID debe comenzar con '{prefijo_esperado}' (ej. {prefijo_esperado}-001).")
            continue
        return valor


def generar_id(prefijo, lista):
    """Genera un ID unico basado en el largo actual de la lista."""
    return f"{prefijo}-{str(len(lista) + 1).zfill(3)}"


# ============================================================
# AUTENTICACION
# ============================================================

def login():
    """
    GUIA 7 - ACTIVIDAD 7 (consulta por identificador):
    Busca el usuario en la LISTA 'usuarios' por correo (identificador).
    Usa ciclo for para recorrer la lista de DICCIONARIOS.
    Las cadenas se procesan con .strip().lower() (ACTIVIDAD 9).
    """
    global usuario_sesion
    mostrar_encabezado("INICIAR SESION")
    print()

    # CADENA: operacion .strip().lower() sobre el correo (GUIA 7 - ACTIVIDAD 9)
    correo = pedir_correo("  Correo electronico: ")

    contrasena = input("  Contrasena: ").strip()
    while contrasena == "":
        print("[!] La contrasena no puede estar vacia.")
        contrasena = input("  Contrasena: ").strip()

    # CICLO FOR sobre LISTA de DICCIONARIOS: busca el usuario por correo
    for usuario in usuarios:
        if usuario["correo"] == correo and usuario["contrasena"] == contrasena:
            usuario_sesion = usuario
            print(f"\n[OK] Bienvenido/a, {usuario['nombre']}!")
            print(f"     Rol: {usuario['rol'].capitalize()} | Ciudad: {usuario['ciudad']}")
            return True

    print("\n[!] Correo o contrasena incorrectos. Intente de nuevo.")
    return False


def cerrar_sesion():
    global usuario_sesion
    usuario_sesion = None
    print("\n[i] Sesion cerrada exitosamente.")


def registrar_usuario():
    """
    GUIA 7 - ACTIVIDAD 3: registra informacion mediante input() y la
    almacena en un DICCIONARIO. El diccionario se agrega a la LISTA
    'usuarios' con append() (ACTIVIDAD 4).
    Usa TUPLA ROLES_SISTEMA para validar el rol.
    """
    mostrar_encabezado("REGISTRO DE USUARIO")
    print()

    # Generar ID automatico
    nuevo_id = generar_id("USR", usuarios)

    # Verificar que el correo no este duplicado
    correo = pedir_correo("  Correo electronico: ")
    for u in usuarios:
        if u["correo"] == correo:
            print(f"[!] Ya existe una cuenta con el correo '{correo}'.")
            return

    nombre = pedir_solo_letras("  Nombre completo: ", "nombre").title()
    # CADENA .title(): formatea correctamente el nombre (ACTIVIDAD 9)

    while True:
        contrasena = input("  Contrasena (minimo 6 caracteres, sin espacios al inicio/fin): ").strip()
        if len(contrasena) < 6:
            print("[!] La contrasena debe tener al menos 6 caracteres.")
            continue
        if not any(c.isalnum() for c in contrasena):
            print("[!] La contrasena debe contener al menos un caracter alfanumerico.")
            continue
        break

    # TUPLA ROLES_SISTEMA: valida que el rol sea uno de los permitidos
    print(f"  Roles disponibles: {', '.join(ROLES_SISTEMA)}")
    while True:
        rol = input("  Rol (cliente / prestador): ").strip().lower()
        if rol in ROLES_SISTEMA:
            break
        print(f"[!] Rol invalido. Opciones: {', '.join(ROLES_SISTEMA)}")

    telefono = input("  Telefono (10 digitos): ").strip()
    while not telefono.isdigit() or len(telefono) != 10:
        print("[!] Ingrese un telefono de 10 digitos numericos.")
        telefono = input("  Telefono: ").strip()

    ciudad = pedir_ciudad()

    # DICCIONARIO: representa el nuevo registro del usuario (ACTIVIDAD 3)
    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": nombre,           # CADENA procesada con .title()
        "correo": correo,           # CADENA procesada con .lower()
        "contrasena": contrasena,
        "rol": rol,
        "ciudad": ciudad,
        "telefono": telefono
    }

    # LISTA.append(): agrega el DICCIONARIO a la lista de usuarios (ACTIVIDAD 4)
    usuarios.append(nuevo_usuario)

    print(f"\n[OK] Usuario '{nombre}' registrado exitosamente con ID {nuevo_id}.")
    print(f"     Total de usuarios en YPRI: {len(usuarios)}")


# ============================================================
# GESTION DE SERVICIOS
# ============================================================

def listar_servicios(filtro_ciudad=None, filtro_categoria=None, solo_disponibles=False):
    """
    GUIA 7 - ACTIVIDAD 6: visualizacion de registros almacenados.
    Ciclo FOR sobre LISTA de DICCIONARIOS, accediendo con claves.
    Guia 6: uso de continue para omitir elementos (YA EXISTIA).
    """
    mostrar_encabezado("CATALOGO DE SERVICIOS YPRI")
    print()

    if filtro_ciudad:
        print(f"  Filtro ciudad: {filtro_ciudad}")
    if filtro_categoria:
        print(f"  Filtro categoria: {filtro_categoria}")
    if solo_disponibles:
        print("  Mostrando: solo con disponibilidad inmediata")
    print()

    print(f"{'No.':<4}{'Codigo':<10}{'Prestador':<20}{'Categoria':<16}{'Tarifa/h':>12}  {'Disp.':<7}{'Rating'}")
    separador()

    mostrados = 0
    # CICLO FOR sobre LISTA de DICCIONARIOS (ACTIVIDAD 6)
    for i, serv in enumerate(servicios):
        # GUIA 6 CONTINUE: omite segun filtros activos
        if solo_disponibles and not serv["disponible"]:
            continue
        if filtro_ciudad and serv["ciudad"].lower() != filtro_ciudad.lower():
            continue
        if filtro_categoria and serv["categoria"].lower() != filtro_categoria.lower():
            continue

        disp = "Si" if serv["disponible"] else "No"
        # Acceso a DICCIONARIO por clave (ACTIVIDAD 6)
        print(f"{i+1:<4}{serv['codigo']:<10}{serv['prestador_nombre']:<20}"
              f"{serv['categoria']:<16}${serv['tarifa_hora']:>10,.0f}  {disp:<7}{serv['calificacion']:.1f}*")
        mostrados += 1

    separador()
    print(f"Servicios mostrados: {mostrados} de {len(servicios)} registrados.")


def ver_detalle_servicio():
    """
    GUIA 7 - ACTIVIDAD 7: consulta de un registro por identificador.
    Busca en la LISTA por el campo 'codigo' del DICCIONARIO.
    Contempla los dos casos: encontrado / no encontrado.
    """
    mostrar_encabezado("DETALLE DE SERVICIO")
    print()
    codigo = pedir_id_registro(
        "  Ingrese el codigo del servicio (ej. SERV-01) o '0' para cancelar: ",
        prefijo_esperado="SERV"
    )
    if codigo is None:
        return

    encontrado = False
    # CICLO FOR + busqueda en LISTA de DICCIONARIOS (ACTIVIDAD 7)
    for serv in servicios:
        if serv["codigo"] == codigo:
            encontrado = True
            print(f"\n  --- DETALLE DEL SERVICIO ---")
            # Acceso por clave al DICCIONARIO
            print(f"  Codigo:       {serv['codigo']}")
            print(f"  Prestador:    {serv['prestador_nombre']}")
            print(f"  Categoria:    {serv['categoria']}")
            print(f"  Descripcion:  {serv['descripcion']}")
            print(f"  Tarifa/hora:  ${serv['tarifa_hora']:,.0f} COP")
            print(f"  Ciudad:       {serv['ciudad']}")
            print(f"  Disponible:   {'Si' if serv['disponible'] else 'No'}")
            print(f"  Calificacion: {serv['calificacion']:.1f} *")
            print(f"  Contratos:    {serv['num_contratos']} realizados")
            separador()
            break  # GUIA 6 BREAK: encontrado, sale del for

    if not encontrado:
        print(f"\n[!] No se encontro ningun servicio con el codigo '{codigo}'.")


def publicar_servicio():
    """
    GUIA 7 - ACTIVIDADES 3 y 4: registra un nuevo servicio como DICCIONARIO
    y lo agrega a la LISTA 'servicios' con append().
    Solo disponible para usuarios con rol 'prestador'.
    Usa TUPLAS CATEGORIAS_SERVICIO y CIUDADES_COBERTURA para validar.
    """
    mostrar_encabezado("PUBLICAR NUEVO SERVICIO")
    print()

    if usuario_sesion["rol"] not in ("prestador", "admin"):
        print("[!] Solo los prestadores pueden publicar servicios.")
        return

    nuevo_codigo = generar_id("SERV", servicios)

    # Verificar que el codigo no exista
    for s in servicios:
        if s["codigo"] == nuevo_codigo:
            nuevo_codigo = f"SERV-{len(servicios)+10}"

    categoria = pedir_categoria()
    descripcion = pedir_texto_minimo("  Descripcion del servicio: ", "descripcion", minimo=10)

    tarifa = pedir_float("  Tarifa por hora en COP: ", 10000, 500000)
    ciudad = pedir_ciudad()
    disp_resp = pedir_sn("  ¿Disponibilidad inmediata? (s/n): ")

    # DICCIONARIO: nuevo servicio (ACTIVIDAD 3)
    nuevo_servicio = {
        "codigo": nuevo_codigo,
        "prestador_id": usuario_sesion["id"],
        "prestador_nombre": usuario_sesion["nombre"],
        "categoria": categoria,
        "descripcion": descripcion.strip(),
        "tarifa_hora": tarifa,
        "ciudad": ciudad,
        "disponible": (disp_resp == "s"),
        "calificacion": 5.0,
        "num_contratos": 0
    }

    # LISTA.append(): agrega el DICCIONARIO a la lista (ACTIVIDAD 4)
    servicios.append(nuevo_servicio)
    print(f"\n[OK] Servicio '{nuevo_codigo}' publicado exitosamente.")
    print(f"     Total de servicios en YPRI: {len(servicios)}")


def modificar_servicio():
    """
    GUIA 7 - ACTIVIDAD 8: modificacion de un registro existente.
    Busca por identificador ('codigo'), verifica existencia,
    permite modificar campos y muestra el registro actualizado.
    No se modifica el codigo (identificador principal).
    """
    mostrar_encabezado("MODIFICAR SERVICIO")
    print()

    if usuario_sesion["rol"] not in ("prestador", "admin"):
        print("[!] Solo los prestadores pueden modificar sus servicios.")
        return

    codigo = pedir_id_registro(
        "  Codigo del servicio a modificar (o '0' para cancelar): ",
        prefijo_esperado="SERV"
    )
    if codigo is None:
        return

    servicio_encontrado = None
    for serv in servicios:
        if serv["codigo"] == codigo:
            # Solo el propio prestador o admin puede modificar
            if usuario_sesion["rol"] != "admin" and serv["prestador_id"] != usuario_sesion["id"]:
                print("[!] Solo puede modificar sus propios servicios.")
                return
            servicio_encontrado = serv
            break

    if not servicio_encontrado:
        print(f"[!] No se encontro el servicio '{codigo}'.")
        return

    print(f"\n  Servicio encontrado: {servicio_encontrado['codigo']} - {servicio_encontrado['categoria']}")
    print("  Deje vacio y presione Enter para conservar el valor actual.")
    print()

    # ACTIVIDAD 8: modificar datos del DICCIONARIO
    nueva_desc = input(f"  Descripcion [{servicio_encontrado['descripcion']}]: ").strip()
    if nueva_desc:
        if len(nueva_desc) < 10 or not any(c.isalpha() for c in nueva_desc):
            print("[!] Descripcion invalida (minimo 10 caracteres con letras). Se conserva la anterior.")
        else:
            servicio_encontrado["descripcion"] = nueva_desc

    while True:
        nueva_tarifa = input(f"  Tarifa/hora [${servicio_encontrado['tarifa_hora']:,.0f}] (Enter para conservar): ").strip()
        if nueva_tarifa == "":
            break   # conservar valor actual
        try:
            t = float(nueva_tarifa)
            if 10000 <= t <= 500000:
                servicio_encontrado["tarifa_hora"] = t
                break
            else:
                print("[!] La tarifa debe estar entre $10.000 y $500.000 COP. Intente de nuevo.")
        except ValueError:
            print("[!] Valor invalido. Ingrese solo numeros (ej. 35000) o Enter para conservar.")

    while True:
        resp_disp = input(f"  ¿Disponible? (s/n) [{'s' if servicio_encontrado['disponible'] else 'n'}]: ").strip().lower()
        if resp_disp == "":
            break   # conservar valor actual
        if resp_disp in ("s", "n"):
            servicio_encontrado["disponible"] = (resp_disp == "s")
            break
        print("[!] Ingrese 's' para Si, 'n' para No, o Enter para conservar.")

    print(f"\n[OK] Servicio '{codigo}' actualizado exitosamente.")
    print(f"     Descripcion: {servicio_encontrado['descripcion']}")
    print(f"     Tarifa:      ${servicio_encontrado['tarifa_hora']:,.0f} COP/h")
    print(f"     Disponible:  {'Si' if servicio_encontrado['disponible'] else 'No'}")


# ============================================================
# GESTION DE CONTRATOS
# ============================================================

def solicitar_servicio():
    """
    GUIA 7 - ACTIVIDAD 3: crea un contrato como DICCIONARIO y lo
    agrega a la LISTA 'contratos' con append().
    Solo disponible para clientes.
    Usa TUPLA ESTADOS_CONTRATO para el estado inicial.
    """
    mostrar_encabezado("SOLICITAR SERVICIO")
    print()

    if usuario_sesion["rol"] != "cliente":
        print("[!] Solo los clientes pueden solicitar servicios.")
        return

    # Mostrar catalogo disponible
    print("  Servicios disponibles:")
    disponibles = []
    for serv in servicios:
        if serv["disponible"]:
            disponibles.append(serv)
            print(f"   {serv['codigo']} | {serv['categoria']:15} | "
                  f"{serv['prestador_nombre']:18} | ${serv['tarifa_hora']:,.0f}/h")

    if not disponibles:
        print("[!] No hay servicios disponibles en este momento.")
        return

    print()
    codigo_serv = pedir_id_registro(
        "  Ingrese el codigo del servicio (o '0' para cancelar): ",
        prefijo_esperado="SERV"
    )
    if codigo_serv is None:
        return

    servicio_sel = None
    for s in disponibles:
        if s["codigo"] == codigo_serv:
            servicio_sel = s
            break

    if not servicio_sel:
        print(f"[!] El codigo '{codigo_serv}' no corresponde a un servicio disponible.")
        return

    horas = pedir_entero("  Numero de horas requeridas: ", 1, 100)

    # Calcular total con IVA 19%
    iva = 0.19
    subtotal = horas * servicio_sel["tarifa_hora"]
    total = subtotal * (1 + iva)

    print(f"\n  --- RESUMEN DE COTIZACION ---")
    print(f"  Servicio:   {servicio_sel['codigo']} - {servicio_sel['categoria']}")
    print(f"  Prestador:  {servicio_sel['prestador_nombre']}")
    print(f"  Horas:      {horas}")
    print(f"  Subtotal:   ${subtotal:,.0f} COP")
    print(f"  IVA (19%):  ${subtotal*iva:,.0f} COP")
    print(f"  TOTAL:      ${total:,.0f} COP")
    separador()

    confirmar = pedir_sn("  ¿Confirmar la solicitud? (s/n): ")
    if confirmar == "n":
        print("[i] Solicitud cancelada.")
        return

    nuevo_id = generar_id("CONTR", contratos)

    # DICCIONARIO: nuevo contrato (ACTIVIDAD 3)
    # TUPLA ESTADOS_CONTRATO[0]: primer estado = "Pendiente"
    nuevo_contrato = {
        "id": nuevo_id,
        "cliente_id": usuario_sesion["id"],
        "cliente_nombre": usuario_sesion["nombre"],
        "servicio_codigo": servicio_sel["codigo"],
        "servicio_nombre": f"{servicio_sel['categoria']} - {servicio_sel['prestador_nombre']}",
        "horas": horas,
        "tarifa_hora": servicio_sel["tarifa_hora"],
        "total": total,
        "estado": ESTADOS_CONTRATO[0],   # TUPLA: "Pendiente"
        "calificacion": 0,
        "comentario": ""
    }

    # LISTA.append(): agrega el contrato a la lista (ACTIVIDAD 4)
    contratos.append(nuevo_contrato)
    servicio_sel["num_contratos"] += 1

    print(f"\n[OK] Contrato '{nuevo_id}' creado exitosamente.")
    print(f"     Estado inicial: {ESTADOS_CONTRATO[0]}")
    print(f"     Total de contratos en YPRI: {len(contratos)}")


def ver_mis_contratos():
    """
    GUIA 7 - ACTIVIDAD 6: visualizacion de contratos del usuario actual.
    Recorre la LISTA de DICCIONARIOS con ciclo for y filtra por cliente_id.
    """
    mostrar_encabezado("MIS CONTRATOS")
    print()

    print(f"{'ID Contrato':<14}{'Servicio':<30}{'Horas':>6}{'Total':>14}  {'Estado'}")
    separador()

    mis_contratos = []
    # CICLO FOR sobre LISTA de DICCIONARIOS
    for c in contratos:
        if c["cliente_id"] == usuario_sesion["id"] or usuario_sesion["rol"] == "admin":
            mis_contratos.append(c)
            # Acceso por clave al DICCIONARIO
            print(f"{c['id']:<14}{c['servicio_nombre']:<30}{c['horas']:>6}"
                  f"${c['total']:>12,.0f}  {c['estado']}")

    separador()
    print(f"Total de contratos: {len(mis_contratos)}")
    if len(mis_contratos) == 0:
        print("  No tiene contratos registrados.")


def actualizar_estado_contrato():
    """
    GUIA 7 - ACTIVIDAD 8: modificacion de un contrato existente.
    Usa TUPLA ESTADOS_CONTRATO para mostrar y validar los estados permitidos.
    """
    mostrar_encabezado("ACTUALIZAR ESTADO DE CONTRATO")
    print()

    if usuario_sesion["rol"] not in ("prestador", "admin"):
        print("[!] Solo prestadores y administradores pueden actualizar contratos.")
        return

    id_contrato = pedir_id_registro(
        "  ID del contrato a actualizar (o '0' para cancelar): ",
        prefijo_esperado="CONTR"
    )
    if id_contrato is None:
        return

    contrato_encontrado = None
    for c in contratos:
        if c["id"] == id_contrato:
            contrato_encontrado = c
            break

    if not contrato_encontrado:
        print(f"[!] No se encontro el contrato '{id_contrato}'.")
        return

    print(f"  Contrato: {contrato_encontrado['id']} | Estado actual: {contrato_encontrado['estado']}")

    # TUPLA ESTADOS_CONTRATO: muestra y valida los estados disponibles
    print(f"\n  Estados disponibles (tupla inmutable):")
    for i, estado in enumerate(ESTADOS_CONTRATO):
        print(f"    {i+1}. {estado}")

    opcion = pedir_entero("  Seleccione el nuevo estado (1-4): ", 1, 4)
    nuevo_estado = ESTADOS_CONTRATO[opcion - 1]   # acceso a TUPLA por indice

    # ACTIVIDAD 8: modificacion del campo en el DICCIONARIO
    contrato_encontrado["estado"] = nuevo_estado
    print(f"\n[OK] Estado actualizado a: '{nuevo_estado}'")


def calificar_servicio():
    """
    Permite al cliente calificar un contrato completado.
    Crea una calificacion como DICCIONARIO y la agrega a la LISTA.
    """
    mostrar_encabezado("CALIFICAR SERVICIO")
    print()

    if usuario_sesion["rol"] != "cliente":
        print("[!] Solo los clientes pueden calificar servicios.")
        return

    id_contrato = pedir_id_registro(
        "  ID del contrato a calificar (o '0' para cancelar): ",
        prefijo_esperado="CONTR"
    )
    if id_contrato is None:
        return

    contrato_cal = None
    for c in contratos:
        if c["id"] == id_contrato and c["cliente_id"] == usuario_sesion["id"]:
            contrato_cal = c
            break

    if not contrato_cal:
        print(f"[!] No se encontro el contrato '{id_contrato}' para su usuario.")
        return

    if contrato_cal["estado"] != "Completado":
        print(f"[!] Solo puede calificar contratos en estado 'Completado'. Estado actual: {contrato_cal['estado']}")
        return

    if contrato_cal["calificacion"] > 0:
        print(f"[!] Este contrato ya fue calificado con {contrato_cal['calificacion']:.1f} estrellas.")
        return

    puntuacion = pedir_float("  Puntuacion (1.0 - 5.0): ", 1.0, 5.0)
    comentario = input("  Comentario (opcional): ").strip()

    # Actualizar calificacion en el contrato (DICCIONARIO)
    contrato_cal["calificacion"] = puntuacion
    contrato_cal["comentario"] = comentario

    # Actualizar calificacion promedio del servicio
    for serv in servicios:
        if serv["codigo"] == contrato_cal["servicio_codigo"]:
            # Calcular nuevo promedio
            total_calif = serv["calificacion"] * (serv["num_contratos"] - 1) + puntuacion
            if serv["num_contratos"] > 0:
                serv["calificacion"] = round(total_calif / serv["num_contratos"], 1)
            break

    # DICCIONARIO: nueva calificacion (ACTIVIDAD 3)
    nueva_calif = {
        "id": generar_id("CALIF", calificaciones),
        "contrato_id": contrato_cal["id"],
        "cliente_nombre": usuario_sesion["nombre"],
        "servicio_codigo": contrato_cal["servicio_codigo"],
        "puntuacion": puntuacion,
        "comentario": comentario,
        "fecha": "09/10/2026"
    }

    # LISTA.append() (ACTIVIDAD 4)
    calificaciones.append(nueva_calif)

    print(f"\n[OK] Calificacion registrada: {puntuacion:.1f}* para {contrato_cal['servicio_codigo']}.")
    print(f"     Total de calificaciones: {len(calificaciones)}")


# ============================================================
# PANEL DE ADMINISTRACION
# ============================================================

def listar_usuarios():
    """Admin: lista todos los usuarios registrados."""
    mostrar_encabezado("GESTION DE USUARIOS")
    print()
    print(f"{'ID':<10}{'Nombre':<22}{'Correo':<28}{'Rol':<12}{'Ciudad'}")
    separador()

    # CICLO FOR sobre LISTA de DICCIONARIOS
    for u in usuarios:
        print(f"{u['id']:<10}{u['nombre']:<22}{u['correo']:<28}{u['rol']:<12}{u['ciudad']}")

    separador()
    print(f"Total de usuarios registrados: {len(usuarios)}")


def ver_estadisticas():
    """
    Muestra estadisticas del sistema recorriendo las listas.
    Demuestra: for sobre lista de dicts, len(), contadores.
    """
    mostrar_encabezado("ESTADISTICAS DEL SISTEMA")
    print()

    # Contadores usando ciclo FOR
    clientes = sum(1 for u in usuarios if u["rol"] == "cliente")
    prestadores = sum(1 for u in usuarios if u["rol"] == "prestador")
    disponibles = sum(1 for s in servicios if s["disponible"])
    contratos_completados = sum(1 for c in contratos if c["estado"] == "Completado")
    contratos_pendientes = sum(1 for c in contratos if c["estado"] == "Pendiente")
    ingresos_total = sum(c["total"] for c in contratos if c["estado"] == "Completado")

    print(f"  USUARIOS")
    print(f"    Total:      {len(usuarios)}")
    print(f"    Clientes:   {clientes}")
    print(f"    Prestadores:{prestadores}")
    print()
    print(f"  SERVICIOS")
    print(f"    Total:      {len(servicios)}")
    print(f"    Disponibles:{disponibles}")
    print()
    print(f"  CONTRATOS")
    print(f"    Total:      {len(contratos)}")
    print(f"    Completados:{contratos_completados}")
    print(f"    Pendientes: {contratos_pendientes}")
    print(f"    Ingresos:   ${ingresos_total:,.0f} COP")
    print()
    print(f"  CALIFICACIONES")
    print(f"    Total:      {len(calificaciones)}")
    if calificaciones:
        prom = sum(c["puntuacion"] for c in calificaciones) / len(calificaciones)
        print(f"    Promedio:   {prom:.2f} *")

    # TUPLAS: muestra los valores fijos del sistema
    print()
    print(f"  VALORES FIJOS DEL SISTEMA (TUPLAS):")
    print(f"    Categorias:    {CATEGORIAS_SERVICIO}")
    print(f"    Estados:       {ESTADOS_CONTRATO}")
    print(f"    Ciudades:      {CIUDADES_COBERTURA}")
    print(f"    Roles:         {ROLES_SISTEMA}")


# ============================================================
# MENUS POR ROL
# ============================================================

def menu_cliente():
    """Menu del ciclo while para clientes."""
    while True:
        mostrar_encabezado(f"MENU CLIENTE — {usuario_sesion['nombre']}")
        print()
        print("  1. Ver catalogo de servicios")
        print("  2. Ver detalle de un servicio")
        print("  3. Solicitar servicio (crear contrato)")
        print("  4. Ver mis contratos")
        print("  5. Calificar un servicio")
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-5): ").strip()

        if opcion == "1":
            resp_filtro = pedir_sn("  ¿Filtrar por disponibilidad inmediata? (s/n): ")
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
            break  # GUIA 6 BREAK: sale del while del menu cliente
        else:
            print("\n[!] Opcion invalida. Ingrese un numero entre 0 y 5.")

        input("\n  Presione Enter para continuar...")
        print()


def menu_prestador():
    """Menu del ciclo while para prestadores."""
    while True:
        mostrar_encabezado(f"MENU PRESTADOR — {usuario_sesion['nombre']}")
        print()
        print("  1. Ver mis servicios publicados")
        print("  2. Publicar nuevo servicio")
        print("  3. Modificar un servicio")
        print("  4. Ver contratos del sistema")
        print("  5. Actualizar estado de contrato")
        print("  0. Cerrar sesion")
        separador()

        opcion = input("  Seleccione una opcion (0-5): ").strip()

        if opcion == "1":
            listar_servicios(filtro_ciudad=usuario_sesion["ciudad"])
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
    """Menu del ciclo while para administradores."""
    while True:
        mostrar_encabezado(f"PANEL ADMIN — {usuario_sesion['nombre']}")
        print()
        print("  1. Ver todos los usuarios")
        print("  2. Ver catalogo de servicios completo")
        print("  3. Ver todos los contratos")
        print("  4. Actualizar estado de contrato")
        print("  5. Ver estadisticas del sistema")
        print("  6. Modificar un servicio")
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


# ============================================================
# MENU PRINCIPAL (antes del login)
# ============================================================

def main():
    """
    Menu principal del sistema YPRI.
    GUIA 6 - ACTIVIDAD 6/8: ciclo while como menu principal con break para salir.
    Desde aqui se accede al login y al registro de nuevos usuarios.
    Luego redirige al menu correspondiente segun el rol (GUIA 7).
    """
    # CICLO WHILE: mantiene el sistema activo (GUIA 6)
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
                # Redirigir al menu segun el ROL del usuario (CADENA en DICCIONARIO)
                if usuario_sesion["rol"] == "cliente":
                    menu_cliente()
                elif usuario_sesion["rol"] == "prestador":
                    menu_prestador()
                elif usuario_sesion["rol"] == "admin":
                    menu_admin()
        elif opcion == "2":
            registrar_usuario()
            input("\n  Presione Enter para continuar...")
        elif opcion == "0":
            print("\n  Gracias por utilizar YPRI.")
            print("  Conectando hogares con profesionales de confianza.")
            print()
            break  # GUIA 6 BREAK: finaliza el ciclo while principal
        else:
            print("\n[!] Opcion invalida.")

        print()


if __name__ == "__main__":
    main()
