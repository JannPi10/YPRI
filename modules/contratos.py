"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Cotizaciones con IVA y Gestion de Contratos
========================================================================================
Responsabilidades:
- Cotizacion automatica de servicios con calculo aritmetico de IVA (19%)
- Creacion de contratos vinculando clientes, prestadores y servicios
- Consulta del historial de contratos segun el rol del usuario
- Actualizacion controlada de estados segun la tupla ESTADOS_CONTRATO
========================================================================================
"""

from core.constantes import ESTADOS_CONTRATO, IVA_PORCENTAJE
from core.validaciones import (
    separador,
    mostrar_encabezado,
    pedir_sn,
    pedir_entero,
    pedir_id_registro,
    generar_id,
)
from data.database import contratos, servicios, get_sesion_actual


def solicitar_servicio():
    """
    Permite a un cliente seleccionar un servicio, ingresar horas requeridas,
    calcular la cotizacion con IVA (19%) y formalizar un nuevo contrato.
    El contrato inicia en estado 'Pendiente' (ESTADOS_CONTRATO[0]).
    """
    mostrar_encabezado("SOLICITAR SERVICIO")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual or usuario_actual["rol"] != "cliente":
        print("[!] Solo los clientes pueden solicitar servicios.")
        return

    # Filtro de servicios con disponibilidad activa
    disponibles = [s for s in servicios if s["disponible"]]
    if not disponibles:
        print("[!] No hay servicios con disponibilidad inmediata en este momento.")
        return

    print("  Servicios disponibles para contratacion:")
    for serv in disponibles:
        print(
            f"   {serv['codigo']} | {serv['categoria']:15} | "
            f"{serv['prestador_nombre']:18} | ${serv['tarifa_hora']:,.0f}/h"
        )

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

    horas = pedir_entero("  Numero de horas requeridas (1 - 100): ", 1, 100)

    # Calculo aritmetico de cotizacion
    subtotal = horas * servicio_sel["tarifa_hora"]
    monto_iva = subtotal * IVA_PORCENTAJE
    total = subtotal + monto_iva

    print(f"\n  --- RESUMEN DE COTIZACION ---")
    print(f"  Servicio:   {servicio_sel['codigo']} - {servicio_sel['categoria']}")
    print(f"  Prestador:  {servicio_sel['prestador_nombre']}")
    print(f"  Horas:      {horas}")
    print(f"  Subtotal:   ${subtotal:,.0f} COP")
    print(f"  IVA (19%):  ${monto_iva:,.0f} COP")
    print(f"  TOTAL:      ${total:,.0f} COP")
    separador()

    confirmar = pedir_sn("  ¿Confirmar la contratacion? (s/n): ")
    if confirmar == "n":
        print("[i] Solicitud cancelada por el usuario.")
        return

    nuevo_id = generar_id("CONTR", contratos)

    # Creacion del contrato como DICCIONARIO
    nuevo_contrato = {
        "id": nuevo_id,
        "cliente_id": usuario_actual["id"],
        "cliente_nombre": usuario_actual["nombre"],
        "servicio_codigo": servicio_sel["codigo"],
        "servicio_nombre": f"{servicio_sel['categoria']} - {servicio_sel['prestador_nombre']}",
        "horas": horas,
        "tarifa_hora": servicio_sel["tarifa_hora"],
        "total": total,
        "estado": ESTADOS_CONTRATO[0],  # Estado inicial inmutable: 'Pendiente'
        "calificacion": 0.0,
        "comentario": ""
    }

    contratos.append(nuevo_contrato)
    servicio_sel["num_contratos"] += 1

    print(f"\n[OK] Contrato '{nuevo_id}' creado exitosamente.")
    print(f"     Estado inicial: {ESTADOS_CONTRATO[0]}")
    print(f"     Total de contratos registrados en YPRI: {len(contratos)}")


def ver_mis_contratos():
    """
    Visualiza los contratos vinculados al usuario autenticado.
    - Clientes: ven unicamente los contratos que solicitaron.
    - Prestadores y Administradores: acceden a los contratos correspondientes.
    """
    mostrar_encabezado("MIS CONTRATOS")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual:
        print("[!] Debe iniciar sesion para ver contratos.")
        return

    print(f"{'ID Contrato':<14}{'Servicio':<30}{'Horas':>6}{'Total':>14}  {'Estado'}")
    separador()

    mis_contratos = []
    for c in contratos:
        # Filtro segun el rol del usuario actual
        if (
            usuario_actual["rol"] == "admin"
            or c["cliente_id"] == usuario_actual["id"]
            or usuario_actual["nombre"] in c["servicio_nombre"]
        ):
            mis_contratos.append(c)
            print(
                f"{c['id']:<14}{c['servicio_nombre']:<30}{c['horas']:>6}"
                f"${c['total']:>12,.0f}  {c['estado']}"
            )

    separador()
    print(f"Total de contratos listados: {len(mis_contratos)}")
    if len(mis_contratos) == 0:
        print("  No se encontraron contratos registrados para esta cuenta.")


def actualizar_estado_contrato():
    """
    Permite actualizar el estado de un contrato segun la tupla ESTADOS_CONTRATO.
    Restringido a usuarios con rol 'prestador' o 'admin'.
    """
    mostrar_encabezado("ACTUALIZAR ESTADO DE CONTRATO")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual or usuario_actual["rol"] not in ("prestador", "admin"):
        print("[!] Solo los prestadores o administradores pueden actualizar contratos.")
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
    print(f"\n  Estados disponibles (tupla inmutable):")
    for i, estado in enumerate(ESTADOS_CONTRATO):
        print(f"    {i+1}. {estado}")

    opcion = pedir_entero("  Seleccione el nuevo estado (1-4): ", 1, len(ESTADOS_CONTRATO))
    nuevo_estado = ESTADOS_CONTRATO[opcion - 1]

    # Modificacion en diccionario
    contrato_encontrado["estado"] = nuevo_estado
    print(f"\n[OK] Estado del contrato actualizado exitosamente a: '{nuevo_estado}'")
