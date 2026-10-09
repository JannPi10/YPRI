"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Calificaciones, Resenas y Reputacion de Prestadores
========================================================================================
Responsabilidades:
- Registro de puntuaciones de 1.0 a 5.0 y comentarios por servicio recibido
- Validacion de elegibilidad (solo contratos con estado 'Completado')
- Prevencion de calificaciones duplicadas sobre el mismo contrato
- Recalculo matematico del promedio acumulado de estrellas del servicio
========================================================================================
"""

from core.validaciones import (
    mostrar_encabezado,
    pedir_float,
    pedir_id_registro,
    generar_id,
)
from data.database import (
    contratos,
    servicios,
    calificaciones,
    get_sesion_actual,
)


def calificar_servicio():
    """
    Permite a un cliente calificar un servicio una vez el contrato este 'Completado'.
    Actualiza la calificacion en el contrato, recalcula el rating promedio del servicio
    y anade un registro a la coleccion general de calificaciones.
    """
    mostrar_encabezado("CALIFICAR SERVICIO")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual or usuario_actual["rol"] != "cliente":
        print("[!] Solo los clientes pueden calificar servicios contratados.")
        return

    id_contrato = pedir_id_registro(
        "  ID del contrato a calificar (o '0' para cancelar): ",
        prefijo_esperado="CONTR"
    )
    if id_contrato is None:
        return

    # Busqueda del contrato perteneciente al cliente activo
    contrato_cal = None
    for c in contratos:
        if c["id"] == id_contrato and c["cliente_id"] == usuario_actual["id"]:
            contrato_cal = c
            break

    if not contrato_cal:
        print(f"[!] No se encontro ningun contrato con ID '{id_contrato}' asociado a su cuenta.")
        return

    # Validacion de estado del contrato
    if contrato_cal["estado"] != "Completado":
        print(
            f"[!] Solo es posible calificar contratos en estado 'Completado'. "
            f"Estado actual: '{contrato_cal['estado']}'."
        )
        return

    # Control de no duplicidad de calificacion
    if contrato_cal.get("calificacion", 0.0) > 0.0:
        print(
            f"[!] Este contrato ya fue calificado previamente con "
            f"{contrato_cal['calificacion']:.1f} estrellas."
        )
        return

    puntuacion = pedir_float("  Puntuacion de 1.0 a 5.0 estrellas: ", 1.0, 5.0)
    comentario = input("  Comentario u observacion (opcional): ").strip()

    # Actualizacion en el contrato
    contrato_cal["calificacion"] = puntuacion
    contrato_cal["comentario"] = comentario

    # Recalculo matematico del promedio de calificacion del servicio
    for serv in servicios:
        if serv["codigo"] == contrato_cal["servicio_codigo"]:
            n_contratos = max(1, serv.get("num_contratos", 1))
            rating_previo = serv.get("calificacion", 5.0)
            # Promedio ponderado
            nuevo_promedio = ((rating_previo * (n_contratos - 1)) + puntuacion) / n_contratos
            serv["calificacion"] = round(nuevo_promedio, 1)
            break

    # Creacion del registro en la coleccion de calificaciones
    nueva_calif = {
        "id": generar_id("CALIF", calificaciones),
        "contrato_id": contrato_cal["id"],
        "cliente_nombre": usuario_actual["nombre"],
        "servicio_codigo": contrato_cal["servicio_codigo"],
        "puntuacion": puntuacion,
        "comentario": comentario,
        "fecha": "09/10/2026"
    }

    calificaciones.append(nueva_calif)

    print(f"\n[OK] Calificacion de {puntuacion:.1f}* registrada exitosamente.")
    print(f"     Servicio: {contrato_cal['servicio_codigo']} | ID Resena: {nueva_calif['id']}")
    print(f"     Total de resenas en la plataforma: {len(calificaciones)}")
