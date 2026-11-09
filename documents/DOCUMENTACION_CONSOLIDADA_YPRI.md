# YPRI
## PLATAFORMA DE SERVICIOS A DOMICILIO
### GUIA DE APRENDIZAJE N. 7 Y GUIA N. 9: ESTRUCTURAS DE DATOS (CADENAS, LISTAS, TUPLAS, DICCIONARIOS Y MATRICES)
#### UNIDAD 2 - ESTRUCTURAS DE DATOS
* Jann Pierre Ortiz Zambrano
* Josue David Rincon Palomino
* Fundacion De Estudios Superiores Comfanorte
* Ingenieria de software
* Octavo semestre - 2026

---

# SECCION I: GUIA DE APRENDIZAJE N. 7 (CADENAS, LISTAS, TUPLAS Y DICCIONARIOS)

## Actividad 1. Identificacion de los Datos del Proyecto

| NOMBRE DEL PROYECTO: | YPRI - Plataforma de Servicios a Domicilio |
|---|---|
| OBJETIVO DEL APLICATIVO: | Conectar clientes con prestadores de servicios tecnicos del hogar (electricistas, plomeros, cerrajeros, etc.) en ciudades colombianas, ofreciendo cotizacion con IVA, gestion de contratos, valoracion de los servicios y arquitectura modular. |
| ENTIDAD PRINCIPAL QUE MANEJA EL SISTEMA: | Servicio: unidad central que un prestador ofrece y un cliente puede contratar a traves de la plataforma. |
| DATOS QUE NECESITA ALMACENAR: | Datos de usuarios (nombre, correo, contrasena, rol, ciudad, telefono). Datos de servicios (codigo, categoria, descripcion, tarifa, disponibilidad, calificacion). Datos de contratos (cliente, servicio, horas, total con IVA, estado). Datos de calificaciones (puntuacion, comentario, fecha). |
| DATO QUE IDENTIFICA CADA REGISTRO: | Usuarios: 'id' (USR-001). Servicios: 'codigo' (SERV-01). Contratos: 'id' (CONTR-101). Calificaciones: 'id' (CALIF-001). |
| EJEMPLOS DE REGISTROS QUE MANEJA: | Usuario: {id: USR-001, nombre: Juan Perez, rol: cliente, ciudad: Cucuta}. Servicio: {codigo: SERV-01, categoria: Electricidad, tarifa_hora: 35000}. Contrato: {id: CONTR-101, estado: Completado, total: 179400}. |

### Identificacion de estructuras por tipo de dato:

| Tipo | Descripcion y Uso en YPRI |
|---|---|
| CADENAS (str): | id, nombre, correo, contrasena, rol, ciudad, codigo, categoria, descripcion, estado, comentario, fecha. Las cadenas se procesan con .strip(), .lower(), .upper() y .title() para normalizar la informacion. |
| LISTAS (list): | usuarios[], servicios[], contratos[], calificaciones[]. Cada lista almacena varios registros de la misma entidad. Se usa .append() para agregar y len() para contar. Se recorren con ciclo for para visualizar, buscar o filtrar. |
| TUPLAS, SI APLICA: | ROLES_SISTEMA = ('cliente', 'prestador', 'admin'). CATEGORIAS_SERVICIO = ('Electricidad', 'Plomeria', 'Limpieza', 'Climatizacion', 'Cerrajeria'). ESTADOS_CONTRATO = ('Pendiente', 'En proceso', 'Completado', 'Cancelado'). CIUDADES_COBERTURA = ('Cucuta', 'Cali', 'Bogota', 'Medellin', 'Bucaramanga'). Son valores fijos que no deben cambiar durante la ejecucion del programa. |
| DICCIONARIOS (dict): | Cada usuario, servicio, contrato y calificacion se representa como un diccionario de pares clave-valor. Ejemplo: {'id': 'USR-001', 'nombre': 'Juan Perez', 'rol': 'cliente'}. Se accede a los datos por clave: usuario['nombre'], servicio['tarifa_hora']. |

---

## Actividad 2. Diseno de la Estructura de un Registro

La entidad principal seleccionada para el proyecto YPRI es el Servicio, ya que es el nucleo del aplicativo: los prestadores publican servicios y los clientes los contratan. A continuacion se definen sus atributos:

| Campo | Definicion |
|---|---|
| ENTIDAD: | Servicio |
| IDENTIFICADOR: | codigo (str) — unico, no modificable. Ejemplo: SERV-01 |
| ATRIBUTO 1: categoria | TIPO DE DATO: str (cadena). Ejemplo: 'Electricidad' |
| ATRIBUTO 2: descripcion | TIPO DE DATO: str (cadena). Ejemplo: 'Instalaciones electricas residenciales' |
| ATRIBUTO 3: tarifa_hora | TIPO DE DATO: float (numero decimal). Ejemplo: 35000.0 |
| ATRIBUTO 4: disponible | TIPO DE DATO: bool (booleano). Ejemplo: True |
| ATRIBUTO 5: calificacion | TIPO DE DATO: float (numero decimal de 1.0 a 5.0). Ejemplo: 4.8 |
| ATRIBUTO 6: ciudad | TIPO DE DATO: str (cadena). Ejemplo: 'Cucuta' |
| ATRIBUTO 7: prestador_nombre | TIPO DE DATO: str (cadena). Ejemplo: 'Carlos Gomez' |

### Representacion como Diccionario Python:
```python
servicio = {
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
}
```

### Representacion como Diccionario: entidad Usuario
```python
usuario = {
    "id":         "USR-001",
    "nombre":     "Juan Perez",             # str procesado con .title()
    "correo":     "juan.perez@email.com",   # str procesado con .lower()
    "contrasena": "juan123",
    "rol":        "cliente",                # validado contra TUPLA ROLES_SISTEMA
    "ciudad":     "Cucuta",                 # validado contra TUPLA CIUDADES_COBERTURA
    "telefono":   "3001234567"
}
```

---

## Actividades 3 y 4. Registro y Almacenamiento de Informacion

YPRI implementa el registro de informacion mediante la funcion `registrar_usuario()` y `publicar_servicio()`. En ambas funciones, los datos se solicitan al usuario mediante `input()`, se almacenan en un DICCIONARIO y luego se agregan a la LISTA correspondiente con `.append()`. Al finalizar, se muestra la cantidad total de registros con `len()`.

### 3.1 Registro de Usuario (cadena str, dict, list.append):
```python
# Datos solicitados al usuario con validaciones defensivas
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
print(f"Total de usuarios: {len(usuarios)}")
```

### 3.2 Registro de Servicio (dict, list.append, tupla de validacion):
```python
# Datos solicitados al prestador
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
print(f"Total de servicios: {len(servicios)}")
```

---

## Actividad 5. Utilizacion de Tuplas en el Proyecto

| Campo | Detalle |
|---|---|
| INFORMACION REPRESENTADA: | Cuatro conjuntos de valores fijos que el sistema necesita para validar entradas y controlar el comportamiento del programa. |
| VALORES: | ROLES_SISTEMA = ('cliente', 'prestador', 'admin')<br>CATEGORIAS_SERVICIO = ('Electricidad', 'Plomeria', 'Limpieza', 'Climatizacion', 'Cerrajeria')<br>ESTADOS_CONTRATO = ('Pendiente', 'En proceso', 'Completado', 'Cancelado')<br>CIUDADES_COBERTURA = ('Cucuta', 'Cali', 'Bogota', 'Medellin', 'Bucaramanga') |
| ¿POR QUE ES CONVENIENTE UNA TUPLA? | Porque estos valores son inmutables: los roles, categorias, estados y ciudades de cobertura de la plataforma NO deben cambiar durante la ejecucion del programa. Si cambiaran accidentalmente (por error en el codigo), podrian invalidar registros existentes. La tupla garantiza que estos valores permanezcan constantes. Ademas, las tuplas son mas eficientes en memoria que las listas para conjuntos de valores fijos. |
| FUNCION DENTRO DEL PROGRAMA: | Se usan en funciones de validacion (pedir_categoria(), pedir_ciudad()) para verificar que el usuario ingrese solo valores permitidos. Se usa ESTADOS_CONTRATO[0] = 'Pendiente' como estado inicial de todo contrato nuevo. Se accede por indice en actualizar_estado_contrato() para asignar el nuevo estado. Se muestran en ver_estadisticas() como parte del reporte del sistema. |

### Codigo que demuestra el uso de las tuplas en YPRI:
```python
# TUPLAS definidas al inicio del programa (valores inmutables)
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
nuevo_estado = ESTADOS_CONTRATO[opcion - 1]
```

---

## Actividad 6. Visualizacion de los Registros

La visualizacion de registros se realiza mediante ciclos `for` que recorren las listas de diccionarios. Para cada elemento, se accede a sus datos usando la clave del diccionario. Guia 6: el ciclo for y continue ya existian en el proyecto; en Guia 7 se refactorizan para operar sobre lista de diccionarios en vez de listas paralelas.

### 6.1 Visualizacion del catalogo de servicios (for sobre lista de dict):
```python
def listar_servicios(solo_disponibles=False):
    # CICLO FOR sobre LISTA de DICCIONARIOS
    for i, serv in enumerate(servicios):
        # GUIA 6 CONTINUE: omite servicios sin disponibilidad si aplica filtro
        if solo_disponibles and not serv["disponible"]:
            continue
        # Acceso por CLAVE al DICCIONARIO
        print(f"{serv['codigo']:<10}{serv['prestador_nombre']:<20}"
              f"{serv['categoria']:<16}${serv['tarifa_hora']:>10,.0f}")
    print(f"Total: {len(servicios)} servicios registrados.")
```

### 6.2 Visualizacion de contratos del usuario autenticado:
```python
def ver_mis_contratos():
    mis_contratos = []
    # CICLO FOR: recorre la lista de contratos (diccionarios)
    for c in contratos:
        if c["cliente_id"] == usuario_sesion["id"]:
            mis_contratos.append(c)
            print(f"{c['id']:<14}{c['servicio_nombre']:<30}"
                  f"{c['horas']:>6}${c['total']:>12,.0f}  {c['estado']}")
    print(f"Total de contratos: {len(mis_contratos)}")
```

---

## Actividad 7. Consulta de un Registro

La consulta de un registro especifico se implementa en dos funciones: `login()` (busca usuario por correo) y `ver_detalle_servicio()` (busca servicio por codigo). Ambas contemplan los dos casos requeridos: registro encontrado y registro no encontrado.

### 7.1 Consulta de usuario por correo (login):
```python
def login():
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
    return False
```

### 7.2 Consulta de servicio por codigo:
```python
def ver_detalle_servicio():
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
        print(f"[!] No se encontro el servicio '{codigo}'.")
```

---

## Actividad 8. Modificacion de Informacion

La modificacion de registros se implementa en `modificar_servicio()` y `actualizar_estado_contrato()`. En ambas funciones el programa: 1) Solicita el identificador con validacion, 2) Busca el registro, 3) Verifica que exista, 4) Permite modificar campos, 5) Almacena los nuevos valores directamente en el diccionario, 6) Muestra confirmacion. El identificador principal (codigo/id) no se modifica.

### 8.1 Modificacion de servicio:
```python
def modificar_servicio():
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
    print("[OK] Servicio actualizado exitosamente.")
```

### 8.2 Actualizacion de estado de contrato (usando TUPLA):
```python
def actualizar_estado_contrato():
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
    print(f"[OK] Estado actualizado a: '{nuevo_estado}'")
```

---

## Actividad 9. Tratamiento de Cadenas en el Proyecto

| CAMPO | TRATAMIENTO APLICADO Y RAZON |
|---|---|
| correo (login, registro) | .strip().lower() — Elimina espacios y convierte a minusculas para evitar errores por diferencias en mayusculas. 'JUAN@EMAIL.com' y 'juan@email.com' se tratan igual. |
| nombre (registro usuario) | .strip().title() — Elimina espacios extra y capitaliza cada palabra. 'jUaN peReZ' se almacena como 'Juan Perez'. |
| categoria (publicar servicio) | .strip().capitalize() — Para comparar correctamente con los valores de la TUPLA CATEGORIAS_SERVICIO. |
| ciudad (registro, servicio) | .strip().capitalize() — Para comparar con los valores de la TUPLA CIUDADES_COBERTURA sin errores de mayusculas. |
| codigo de servicio (busqueda) | .strip().upper() — El codigo SERV-01 siempre se compara en mayusculas para evitar que 'serv-01' y 'SERV-01' sean tratados diferente. |
| descripcion (servicio) | .strip() — Elimina espacios al inicio y al final para una presentacion limpia. |

### Codigo que demuestra el tratamiento de cadenas:
```python
# Registro de usuario — cadenas con .strip(), .lower(), .title()
correo = pedir_correo("Correo: ").strip().lower()
nombre = pedir_solo_letras("Nombre: ", "nombre").strip().title()

# Busqueda — cadena con .strip().upper()
codigo = pedir_id_registro("Codigo del servicio: ", prefijo_esperado="SERV")

# Validacion de categoria — cadena con .strip().capitalize()
def pedir_categoria():
    while True:
        valor = input("Categoria: ").strip().capitalize()
        if valor in CATEGORIAS_SERVICIO:
            return valor
        print("[!] Categoria invalida.")
```

---

## Actividad 10. Integracion con Ciclos

YPRI implementa menus con ciclo `while` que mantienen cada modulo activo hasta que el usuario seleccione salir. El sistema tiene tres menus por rol: cliente, prestador y administrador, cada uno controlado por su propio while. Guia 6: el ciclo while del menu ya existia; Guia 7 lo extiende con menus por rol y control modular.

### Menu principal (while + break — Guia 6 existente):
```python
def main():
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
            break  # BREAK: sale del while principal
```

---

## Actividad 11. Integracion de las Estructuras de Datos y Arquitectura Modular

Para garantizar calidad de codigo, escalabilidad y buenas practicas de desarrollo, el aplicativo YPRI fue organizado tanto de forma unificada (ypri_sistema.py) como en una arquitectura modular completa dividida en paquetes logicos (core, data, modules):

| Estructura / Capa | Uso e Implementacion en YPRI | Ubicacion Modular |
|---|---|---|
| Cadenas (str) | Almacenar y procesar datos textuales. Se aplica .strip(), .lower(), .title(), .upper(), .capitalize(). | core/validaciones.py, modules/auth.py |
| Listas (list) | Almacenar colecciones de registros: usuarios[], servicios[], contratos[], calificaciones[]. Se usa .append(), len(). | data/database.py, modules/* |
| Tuplas (tuple) | ROLES_SISTEMA, CATEGORIAS_SERVICIO, ESTADOS_CONTRATO, CIUDADES_COBERTURA. Valores fijos e inmutables para validacion y control. | core/constantes.py |
| Diccionarios (dict) | Cada usuario, servicio, contrato y calificacion es un dict {clave: valor}. Se manipulan atributos in-place de forma eficiente. | data/database.py, modules/* |
| Ciclos (while, for) | while: menus por rol y validaciones repetitivas. for: recorridos de colecciones para listar, buscar o auditar. | main.py, ypri_sistema.py, modules/* |
| Condiciones (if/elif/else) | Control de acceso segun rol, filtros en listados, validaciones defensivas y reglas de negocio. | Todos los modulos del sistema |

---

## Actividad 12. Requerimientos Funcionales del Proyecto

| Campo | Detalle |
|---|---|
| REQUERIMIENTO FUNCIONAL 1: | RF-01: Registro y publicacion de servicios. El sistema permite a los prestadores publicar nuevos servicios con datos como categoria, descripcion, tarifa y ciudad. |
| ESTADO RF-01: | IMPLEMENTADO |
| ESTRUCTURAS UTILIZADAS RF-01: | dict (nuevo_servicio), list (servicios.append()), tuple (CATEGORIAS_SERVICIO para validar, CIUDADES_COBERTURA para validar), str (.strip(), .capitalize() en categoria y ciudad), while (validaciones de entrada). |
| REQUERIMIENTO FUNCIONAL 2: | RF-02: Busqueda, cotizacion y contratacion de servicios. El cliente puede ver el catalogo, seleccionar un servicio, calcular el costo total con IVA (19%) y generar un contrato. |
| ESTADO RF-02: | IMPLEMENTADO |
| ESTRUCTURAS UTILIZADAS RF-02: | list (servicios[], contratos[], for para recorrer), dict (nuevo_contrato con todos los campos), tuple (ESTADOS_CONTRATO[0] = 'Pendiente' como estado inicial), float (calculo de tarifa, IVA y total), str (codigo del servicio con .upper()). |
| REQUERIMIENTO FUNCIONAL 3: | RF-03: Gestion de contratos y calificaciones. El prestador/admin puede actualizar el estado del contrato y el cliente puede calificar el servicio una vez completado con recalculo ponderado de rating. |
| ESTADO RF-03: | IMPLEMENTADO |
| ESTRUCTURAS UTILIZADAS RF-03: | dict (contrato_encontrado['estado'] modificado, nueva_calif como dict), list (calificaciones.append()), tuple (ESTADOS_CONTRATO para mostrar y validar el nuevo estado), for (busqueda del contrato por ID), bool (logica de calificacion ya otorgada). |

---

## Actividad 13. Pruebas del Aplicativo (Guia 7)

| Prueba | Funcionalidad / Datos utilizados | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| 1 | Login + Ver catalogo de servicios + Solicitar servicio (contrato con IVA) | Login exitoso con correo/contrasena. Catalogo muestra 5 servicios con datos de LISTA de DICCIONARIOS. Contrato creado con estado 'Pendiente' (TUPLA ESTADOS[0]) y cotizacion con 19% IVA. | Login exitoso: 'Bienvenido/a, Juan Perez!'. Catalogo muestra 5 servicios. Contrato CONTR-002 creado con TOTAL calculado. Estado = 'Pendiente'. Total contratos: 2. |
| 2 | Registro de nuevo usuario + Login con el nuevo usuario | Nuevo usuario registrado correctamente como dict y agregado a la lista con append(). Validacion de correo, telefono y ciudad con tupla. Login exitoso con nuevas credenciales. | Usuario 'Maria Lopez' registrado con ID USR-004. len(usuarios) = 4. Login exitoso. Menu cliente activado correctamente. |
| 3 | Prestador publica un nuevo servicio y lo modifica | Nuevo servicio creado como diccionario y agregado a servicios[]. El servicio se modifica actualizando los campos 'descripcion' y 'tarifa_hora' directamente en el dict. | Servicio SERV-006 publicado exitosamente. Descripcion y tarifa actualizadas correctamente. Confirmacion mostrada con los nuevos valores. |
| 4 | Admin: ver usuarios, estadisticas del sistema, actualizar estado de contrato | Lista de usuarios recorrida con for. Estadisticas calculadas recorriendo listas. TUPLAS mostradas como valores fijos. Estado del contrato cambia usando ESTADOS_CONTRATO[indice]. | 3 usuarios listados correctamente. Estadisticas calculadas: 5 servicios, 1 contrato, ingresos $179.400. TUPLAS visibles en estadisticas. Estado actualizado a 'Cancelado'. |
| 5 | Cliente califica un servicio completado (contrato en estado Completado) | Admin cambia estado a 'Completado'. Cliente califica con 5.0 y comentario. Nueva calificacion creada como dict y agregada a calificaciones[]. Promedio del servicio recalculado. | Estado actualizado a 'Completado' usando ESTADOS_CONTRATO[2]. Calificacion CALIF-002 creada. len(calificaciones) = 2. Promedio recalculado correctamente en el servicio SERV-01. |

---

# SECCION II: GUIA DE APRENDIZAJE N. 9 (MATRICES EN PYTHON: CREACION, RECORRIDO Y OPERACIONES)

## Actividad 14. Identificacion e Implementacion de Matrices en el Proyecto (Guia 9 - Actividad 1)

Una matriz es una estructura de datos bidimensional que permite organizar informacion en filas y columnas. En Python, se representa mediante una lista que contiene otras listas. Para responder a las necesidades de gestion analitica y financiera de YPRI, se implementaron dos matrices en `backend/data/database.py`:

| CAMPO | DEFINICION Y APLICACION EN YPRI |
|---|---|
| NOMBRE DE LA MATRIZ 1: | matriz_ventas_semanales |
| DIMENSIONES MATRIZ 1: | 5 Filas (Categorias oficiales de servicios) × 6 Columnas (Dias laborales: Lunes, Martes, Miercoles, Jueves, Viernes, Sabado). Total: 30 celdas. |
| TIPO DE DATO CONTENIDO: | float (montos de facturacion en pesos colombianos - COP). |
| UTILIDAD EN EL PROYECTO: | Monitorear el flujo semanal de ingresos por linea de servicio, detectar picos de demanda y calcular la rentabilidad diaria. |
| NOMBRE DE LA MATRIZ 2: | matriz_ventas_ciudades |
| DIMENSIONES MATRIZ 2: | 5 Filas (Categorias) × 5 Columnas (Ciudades de cobertura: Cucuta, Cali, Bogota, Medellin, Bucaramanga). |
| PROPIEDAD MATEMATICA: | MATRIZ CUADRADA (5×5). Mismo numero de filas y columnas, permitiendo extraer la diagonal principal (i == j). |
| UTILIDAD EN EL PROYECTO: | Analizar la distribucion geografica de la demanda y rentabilidad por ciudad en el territorio colombiano. |

### Implementacion de las Matrices en backend/data/database.py:
```python
# MATRIZ 1: Facturacion semanal por Categoria y Dia (5 filas x 6 columnas)
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
]
```

---

## Actividad 15. Registro y Consulta de Informacion en la Matriz (Guia 9 - Actividad 2)

Se desarrollaron mecanismos controlados para consultar y registrar datos en la matriz:

| Operacion | Mecanismo y Logica Aplicada |
|---|---|
| Acceso por Coordenada: | matriz[fila][columna]. Indica primero la fila y despues la columna para leer o modificar. |
| Consulta de Celda Individual: | consultar_celda(matriz, fila_idx, col_idx) retorna el valor exacto en COP de esa posicion. |
| Consulta de Fila Completa: | consultar_fila_especifica() extrae matriz[i], calcula el subtotal de la categoria y su promedio diario. |
| Consulta de Columna Completa: | consultar_columna_especifica() itera verticalmente sumando los valores de todas las categorias para un dia o ciudad dada. |
| Modificacion de Celda: | modificar_celda(matriz, i, j, nuevo_valor) valida que los indices esten dentro de rango y que el valor ingresado sea >= 0. |

### Codigo de Consulta y Modificacion de Celdas:
```python
def consultar_celda(matriz, fila_idx, col_idx):
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
    return True
```

---

## Actividad 16. Recorrido de Filas y Columnas con Ciclos Anidados (Guia 9 - Actividad 3)

Para recorrer una matriz se utilizan ciclos `for` anidados. En YPRI se aplicaron tres modalidades de recorrido bidimensional:
1. **Recorrido horizontal por elementos:** ciclo externo `for fila in matriz:` y ciclo interno `for valor in fila:`.
2. **Recorrido indexado por rangos:** `for i in range(len(matriz)):` para filas y `for j in range(len(matriz[i])):` para columnas.
3. **Recorrido vertical por columnas:** ciclo externo `for j in range(columnas):` y ciclo interno `for i in range(filas):` para totalizar columnas verticalmente.

### Codigo del Recorrido Tabular con Ciclos Anidados:
```python
def mostrar_matriz_tabulada(matriz, nombres_filas, nombres_columnas, titulo):
    print(f"=== {titulo} ===")
    
    # CICLO EXTERNO: recorre las filas de la matriz por indice i
    for i in range(len(matriz)):
        nombre_categoria = nombres_filas[i]
        print(f"{nombre_categoria:<18}", end="")
        
        # CICLO INTERNO: recorre cada columna de la fila actual por indice j
        for j in range(len(matriz[i])):
            valor_celda = matriz[i][j]
            print(f"${valor_celda:>12,.0f}", end=" ")
        
        # Total acumulado por fila (operacion matematica)
        print(f"| Total: ${sum(matriz[i]):>12,.0f}")
    
    # Suma vertical por columnas con ciclos anidados invertidos
    totales_col = calcular_totales_columnas(matriz)
    print("TOTAL COLUMNAS:    ", end="")
    for tot in totales_col:
        print(f"${tot:>12,.0f}", end=" ")
    print()
```

---

## Actividad 17. Operaciones Matematicas y Procesamiento Util (Guia 9 - Actividad 4)

Se incorporaron seis operaciones matematicas analiticas fundamentales para la plataforma YPRI:

| Operacion Matematica | Funcion y Formula | Significado de Negocio en YPRI |
|---|---|---|
| Total por Fila | `calcular_totales_filas()`: `sum(matriz[i])` | Facturacion total acumulada por cada categoria de servicio. |
| Total por Columna | `calcular_totales_columnas()`: suma vertical con for anidado | Recaudacion total diaria de la plataforma o por ciudad. |
| Total General | `calcular_total_general()`: suma de todas las celdas | Ingresos brutos consolidados en la plataforma. |
| Promedio por Registro | `calcular_promedio_general()`: `total_general / (filas * cols)` | Ticket promedio de facturacion por celda (categoria x dia). |
| Analisis de Extremos | `analizar_rendimiento_matriz()`: maximo y minimo | Detecta la categoria lider, el dia record y la celda con mayor facturacion. |
| Matrices Especiales | `es_matriz_cuadrada()`, `crear_matriz_nula()`, `crear_matriz_identidad()` | Validacion de orden 5x5, inicializacion de acumuladores y asignaciones unitarias. |

### Codigo de Calculo de Columnas, Totales y Promedios:
```python
# Suma vertical por columna usando ciclos anidados (Guia 9 - Seccion 1.5)
def calcular_totales_columnas(matriz):
    totales = []
    num_columnas = len(matriz[0])
    num_filas = len(matriz)
    
    for j in range(num_columnas):
        total_col = 0.0
        for i in range(num_filas):
            total_col += matriz[i][j]
        totales.append(total_col)
    return totales

# Total general de la matriz bidimensional
def calcular_total_general(matriz):
    total = 0.0
    for fila in matriz:
        for valor in fila:
            total += valor
    return total

# Promedio global por celda
def calcular_promedio_general(matriz):
    total = calcular_total_general(matriz)
    total_registros = len(matriz) * len(matriz[0])
    return total / total_registros if total_registros > 0 else 0.0
```

### Codigo de Matrices Especiales (Guia 9 - Seccion 1.6):
```python
# Matriz cuadrada (igual numero de filas y columnas)
def es_matriz_cuadrada(matriz):
    return all(len(fila) == len(matriz) for fila in matriz)

# Matriz nula (todos los elementos son cero)
def crear_matriz_nula(filas, columnas):
    return [[0.0 for _ in range(columnas)] for _ in range(filas)]

# Matriz identidad (1.0 en diagonal principal, 0.0 en el resto)
def crear_matriz_identidad(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

# Extraccion de la diagonal principal
def extraer_diagonal_principal(matriz):
    return [matriz[i][i] for i in range(min(len(matriz), len(matriz[0])))]
```

---

## Actividad 18. Integracion de Matrices con las Operaciones Existentes (Guia 9 - Actividad 5)

En concordancia con la directriz institucional de evitar crear aplicativos aislados, el modulo de matrices fue integrado en todas las capas del sistema:

| Capa / Modulo | Ubicacion en la Arquitectura | Integracion Realizada |
|---|---|---|
| Persistencia | `backend/data/database.py` | Matrices globales inicializadas en memoria junto con los vectores de usuarios, servicios y contratos. |
| Negocio | `backend/modules/matrices.py` | Modulo completo con logica de consulta, modificacion, extremos y matrices especiales. |
| Administracion | `backend/modules/admin.py` | El informe de estadisticas del admin consolida el total general y categoria lider desde la matriz. |
| Consola CLI | `backend/main.py` | Opcion directa en el menu principal para acceder a las matrices y al ejercicio guiado. |
| Escritorio GUI | `backend/app_gui.py` | Pestana interactiva en Tkinter con edicion de celdas y visualizador de matrices especiales. |
| Web en la Nube | `web/app/page.tsx` | Frontend moderno en Next.js y Tailwind CSS desplegable en Vercel con tabla reactiva y soporte movil. |

### Sincronizacion de Contratos Reales con la Matriz de Ventas:
```python
def sincronizar_matriz_con_contratos_reales():
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
                    matriz_ventas_semanales[cat_idx][4] += float(c["total"])
                    total_sumado += float(c["total"])
                    contratos_procesados += 1
    return contratos_procesados, total_sumado
```

---

## Actividad 19. Desarrollo de la Seccion 2 de la Guia 9 (Ejercicio Practico Guiado 3x3)

Se desarrollo y probo el programa base de la Sección 2 de la guía (registro de 3 productos en 3 días):

```python
productos = ["Producto A", "Producto B", "Producto C"]
dias = ["Lunes", "Martes", "Miercoles"]
ventas = []

# REGISTRO DEFENSIVO (Guia 9 - Pagina 4)
for producto in productos:
    fila = []
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

# TOTAL POR PRODUCTO
for i in range(len(ventas)):
    total_producto = sum(ventas[i])
    print(f"{productos[i]}: ${total_producto:,.2f}")

# TOTAL POR DIA (Ciclos anidados)
for j in range(len(dias)):
    total_dia = 0.0
    for i in range(len(productos)):
        total_dia += ventas[i][j]
    print(f"{dias[j]}: ${total_dia:,.2f}")

# TOTAL GENERAL Y PROMEDIO
total_general = sum(sum(fila) for fila in ventas)
promedio = total_general / (len(productos) * len(dias))
```

### Tabla de Resultados Obtenidos en la Ejecucion del Ejercicio Guiado:

| Producto | Lunes | Martes | Miercoles | Total Producto |
|---|---|---|---|---|
| Producto A | $150,000.00 | $200,000.00 | $180,000.00 | $530,000.00 |
| Producto B | $120,000.00 | $250,000.00 | $300,000.00 | $670,000.00 |
| Producto C | $175,000.00 | $190,000.00 | $220,000.00 | $585,000.00 |
| TOTAL DIA | $445,000.00 | $640,000.00 | $700,000.00 | $1,785,000.00 |

* **Total General Acumulado:** $1,785,000.00 COP
* **Cantidad de Registros:** 3 productos × 3 días = 9 celdas
* **Promedio por Registro:** $1,785,000 / 9 = $198,333.33 COP

---

## Actividad 20. Pruebas y Evidencias de Ejecucion de Matrices (Guia 9)

| Prueba | Funcionalidad / Datos Utilizados | Resultado Esperado | Resultado Obtenido |
|---|---|---|---|
| 6 | Visualizacion de Matriz Semanal (5x6) y Calculo de Totales | Matriz tabular de 5 categorias por 6 dias con totales por fila, totales por columna y total general. | Matriz desplegada con exito. Facturacion general: $11,270,000 COP. Promedio por celda: $375,667 COP. Categoria lider: Climatizacion ($3,200,000 COP). |
| 7 | Modificacion interactiva de celda matriz[i][j] | Ingreso de coordenadas [0][1] (Electricidad - Martes) y nuevo valor $490,000. | Celda actualizada correctamente de $420,000 a $490,000 COP. Total general recalculado a $11,340,000 COP. |
| 8 | Consulta de Fila Completa y Columna Completa | Consulta de fila 3 (Climatizacion) y columna 4 (Viernes). | Fila Climatizacion muestra total de $3,200,000 COP y promedio de $533,333 COP. Columna Viernes totaliza $2,520,000 COP. |
| 9 | Verificacion de Matrices Especiales (Cuadrada, Nula, Identidad) | Comprobar que matriz_ventas_ciudades es 5x5 cuadrada, extraer diagonal principal y generar nula e identidad 3x3. | es_matriz_cuadrada = True. Diagonal principal extraida: [$450k, $290k, $490k, $890k, $150k]. Matrices nula e identidad generadas con exito. |
| 10 | Sincronizacion de Contratos Completados con la Matriz | Procesar contratos en estado 'Completado' y acreditar monto a la matriz de ventas. | Contrato CONTR-101 por $208,250 COP acreditado a la categoria Electricidad en la columna Viernes. Sincronizacion exitosa. |

---

## Repositorio del Proyecto en GitHub

| Campo | Informacion Oficial |
|---|---|
| ENLACE AL REPOSITORIO: | https://github.com/JannPi10/YPRI.git |
| RAMA PRINCIPAL: | main |
| USUARIO PROPIETARIO: | JannPi10 |
| ORGANIZACION DEL REPOSITORIO: | backend/ (Python CLI y GUI), web/ (Frontend Next.js en Vercel), documents/ (Documentos de entrega institucional). |
| HISTORIAL DE COMMITS ACTUALIZADO: | 1. feat(core): constantes y validaciones defensivas<br>2. feat(data): persistencia en memoria y vectores base<br>3. feat(auth): autenticacion y control de sesion<br>4. feat(servicios): catalogo y busquedas de vector<br>5. feat(contratos): cotizaciones con IVA (19%)<br>6. feat(calificaciones): resenas y reputacion<br>7. feat(matrices): creacion, recorrido y operaciones de matrices bidimensionales (Guia 9)<br>8. feat(matrices-especiales): soporte para matrices cuadradas, nulas e identidad<br>9. feat(gui): visor interactivo de matrices en Tkinter<br>10. feat(web): plataforma moderna responsive en Next.js desplegable en Vercel<br>11. docs: informe academico consolidado de entrega (Guias 7 y 9) |

El codigo fuente completo, la documentacion tecnica, las guias y el historial detallado de commits se encuentran disponibles para su consulta y clonacion en el enlace oficial de GitHub: https://github.com/JannPi10/YPRI.git
