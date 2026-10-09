"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Catalogo, Publicacion, Busqueda y Modificacion de Servicios
========================================================================================
Responsabilidades:
- Visualizacion del catalogo completo y filtrado por ciudad, categoria o disponibilidad
- Busqueda y detalle de servicios por identificador unico
- Publicacion de nuevos servicios para prestadores
- Modificacion de tarifas, descripcion y estado de disponibilidad
========================================================================================
"""

from core.validaciones import (
    separador,
    mostrar_encabezado,
    pedir_sn,
    pedir_float,
    pedir_categoria,
    pedir_ciudad,
    pedir_texto_minimo,
    pedir_id_registro,
    generar_id,
)
from data.database import servicios, get_sesion_actual


def listar_servicios(filtro_ciudad=None, filtro_categoria=None, solo_disponibles=False):
    """
    Recorre la lista de diccionarios de servicios y muestra la informacion tabular.
    Aplica filtros opcionales utilizando la instruccion 'continue' para omitir elementos.
    """
    mostrar_encabezado("CATALOGO DE SERVICIOS YPRI")
    print()

    if filtro_ciudad:
        print(f"  Filtro por ciudad: {filtro_ciudad}")
    if filtro_categoria:
        print(f"  Filtro por categoria: {filtro_categoria}")
    if solo_disponibles:
        print("  Mostrando unicamente servicios con disponibilidad inmediata")
    print()

    print(f"{'No.':<4}{'Codigo':<10}{'Prestador':<20}{'Categoria':<16}{'Tarifa/h':>12}  {'Disp.':<7}{'Rating'}")
    separador()

    mostrados = 0
    for i, serv in enumerate(servicios):
        # Filtros con instruccion continue
        if solo_disponibles and not serv["disponible"]:
            continue
        if filtro_ciudad and serv["ciudad"].lower() != filtro_ciudad.lower():
            continue
        if filtro_categoria and serv["categoria"].lower() != filtro_categoria.lower():
            continue

        disp = "Si" if serv["disponible"] else "No"
        print(
            f"{i+1:<4}{serv['codigo']:<10}{serv['prestador_nombre']:<20}"
            f"{serv['categoria']:<16}${serv['tarifa_hora']:>10,.0f}  {disp:<7}{serv['calificacion']:.1f}*"
        )
        mostrados += 1

    separador()
    print(f"Servicios mostrados: {mostrados} de {len(servicios)} registrados.")


def ver_detalle_servicio():
    """
    Consulta un servicio especifico mediante su codigo de identificacion.
    Utiliza ciclo for con break al encontrar la coincidencia.
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
    for serv in servicios:
        if serv["codigo"] == codigo:
            encontrado = True
            print(f"\n  --- DETALLE DEL SERVICIO ---")
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
            break

    if not encontrado:
        print(f"\n[!] No se encontro ningun servicio con el codigo '{codigo}'.")


def publicar_servicio():
    """
    Permite a un usuario con rol 'prestador' o 'admin' registrar un nuevo servicio.
    Almacena los datos en un diccionario y lo agrega a la lista general con .append().
    """
    mostrar_encabezado("PUBLICAR NUEVO SERVICIO")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual or usuario_actual["rol"] not in ("prestador", "admin"):
        print("[!] Solo los prestadores o administradores pueden publicar servicios.")
        return

    nuevo_codigo = generar_id("SERV", servicios)

    # Validacion para evitar codigos duplicados
    for s in servicios:
        if s["codigo"] == nuevo_codigo:
            nuevo_codigo = f"SERV-{len(servicios)+10}"

    categoria = pedir_categoria()
    descripcion = pedir_texto_minimo("  Descripcion del servicio: ", "descripcion", minimo=10)
    tarifa = pedir_float("  Tarifa por hora en COP: ", 10000, 500000)
    ciudad = pedir_ciudad()
    disp_resp = pedir_sn("  ¿Disponibilidad inmediata? (s/n): ")

    # Creacion del registro como DICCIONARIO
    nuevo_servicio = {
        "codigo": nuevo_codigo,
        "prestador_id": usuario_actual["id"],
        "prestador_nombre": usuario_actual["nombre"],
        "categoria": categoria,
        "descripcion": descripcion.strip(),
        "tarifa_hora": tarifa,
        "ciudad": ciudad,
        "disponible": (disp_resp == "s"),
        "calificacion": 5.0,
        "num_contratos": 0
    }

    servicios.append(nuevo_servicio)
    print(f"\n[OK] Servicio '{nuevo_codigo}' publicado exitosamente.")
    print(f"     Total de servicios en YPRI: {len(servicios)}")


def modificar_servicio():
    """
    Permite modificar atributos de un servicio existente (descripcion, tarifa, disponibilidad).
    Verifica permisos: solo el prestador dueno o un admin pueden modificar.
    El identificador principal (codigo) permanece inmutable.
    """
    mostrar_encabezado("MODIFICAR SERVICIO")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual or usuario_actual["rol"] not in ("prestador", "admin"):
        print("[!] Solo los prestadores o administradores pueden modificar servicios.")
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
            # Control de autorizacion por usuario
            if usuario_actual["rol"] != "admin" and serv["prestador_id"] != usuario_actual["id"]:
                print("[!] Solo puede modificar los servicios publicados por usted.")
                return
            servicio_encontrado = serv
            break

    if not servicio_encontrado:
        print(f"[!] No se encontro el servicio '{codigo}'.")
        return

    print(f"\n  Servicio encontrado: {servicio_encontrado['codigo']} - {servicio_encontrado['categoria']}")
    print("  Deje vacio y presione Enter si desea conservar el valor actual.\n")

    # Modificacion opcional de descripcion
    nueva_desc = input(f"  Descripcion [{servicio_encontrado['descripcion']}]: ").strip()
    if nueva_desc:
        if len(nueva_desc) < 10 or not any(c.isalpha() for c in nueva_desc):
            print("[!] Descripcion invalida (minimo 10 caracteres con letras). Se conserva la anterior.")
        else:
            servicio_encontrado["descripcion"] = nueva_desc

    # Modificacion opcional de tarifa
    while True:
        nueva_tarifa = input(f"  Tarifa/hora [${servicio_encontrado['tarifa_hora']:,.0f}] (Enter para conservar): ").strip()
        if nueva_tarifa == "":
            break
        try:
            t = float(nueva_tarifa)
            if 10000 <= t <= 500000:
                servicio_encontrado["tarifa_hora"] = t
                break
            else:
                print("[!] La tarifa debe estar entre $10.000 y $500.000 COP. Intente de nuevo.")
        except ValueError:
            print("[!] Valor invalido. Ingrese solo numeros (ej. 35000) o Enter para conservar.")

    # Modificacion opcional de disponibilidad
    while True:
        resp_disp = input(f"  ¿Disponible? (s/n) [{'s' if servicio_encontrado['disponible'] else 'n'}]: ").strip().lower()
        if resp_disp == "":
            break
        if resp_disp in ("s", "n"):
            servicio_encontrado["disponible"] = (resp_disp == "s")
            break
        print("[!] Ingrese 's' para Si, 'n' para No, o Enter para conservar.")

    print(f"\n[OK] Servicio '{codigo}' actualizado exitosamente.")
    print(f"     Descripcion: {servicio_encontrado['descripcion']}")
    print(f"     Tarifa:      ${servicio_encontrado['tarifa_hora']:,.0f} COP/h")
    print(f"     Disponible:  {'Si' if servicio_encontrado['disponible'] else 'No'}")
