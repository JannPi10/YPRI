"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Administracion, Auditoria y Metricas del Sistema
========================================================================================
Responsabilidades:
- Visualizacion global de usuarios registrados en la plataforma
- Calculo y reporte de metricas de negocio (usuarios, contratos, ingresos en COP)
- Monitoreo de configuraciones inmutables del sistema (tuplas base)
========================================================================================
"""

from core.constantes import (
    ROLES_SISTEMA,
    CATEGORIAS_SERVICIO,
    ESTADOS_CONTRATO,
    CIUDADES_COBERTURA,
)
from core.validaciones import separador, mostrar_encabezado
from data.database import (
    usuarios,
    servicios,
    contratos,
    calificaciones,
    get_sesion_actual,
)


def listar_usuarios():
    """
    Lista todos los usuarios registrados en el sistema en formato tabular.
    Disponible exclusivamente para administradores.
    """
    mostrar_encabezado("GESTION DE USUARIOS")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual or usuario_actual["rol"] != "admin":
        print("[!] Acceso denegado: se requieren permisos de administrador.")
        return

    print(f"{'ID':<10}{'Nombre':<22}{'Correo':<28}{'Rol':<12}{'Ciudad'}")
    separador()

    for u in usuarios:
        print(f"{u['id']:<10}{u['nombre']:<22}{u['correo']:<28}{u['rol']:<12}{u['ciudad']}")

    separador()
    print(f"Total de usuarios registrados: {len(usuarios)}")


def ver_estadisticas():
    """
    Genera un informe consolidado con las metricas operativas y financieras del sistema.
    Calcula totales mediante ciclos for y comprensiones de lista sobre colecciones.
    """
    mostrar_encabezado("ESTADISTICAS DEL SISTEMA")
    print()

    usuario_actual = get_sesion_actual()
    if not usuario_actual or usuario_actual["rol"] != "admin":
        print("[!] Acceso denegado: se requieren permisos de administrador.")
        return

    # Metricas calculadas dinamicamente
    total_clientes = sum(1 for u in usuarios if u["rol"] == "cliente")
    total_prestadores = sum(1 for u in usuarios if u["rol"] == "prestador")
    servicios_activos = sum(1 for s in servicios if s["disponible"])
    contratos_completados = sum(1 for c in contratos if c["estado"] == "Completado")
    contratos_pendientes = sum(1 for c in contratos if c["estado"] == "Pendiente")
    ingresos_totales = sum(c["total"] for c in contratos if c["estado"] == "Completado")

    print(f"  USUARIOS")
    print(f"    Total registrados: {len(usuarios)}")
    print(f"    Clientes:          {total_clientes}")
    print(f"    Prestadores:       {total_prestadores}")
    print()
    print(f"  SERVICIOS")
    print(f"    Total publicados:  {len(servicios)}")
    print(f"    Con disp. activa:  {servicios_activos}")
    print()
    print(f"  CONTRATOS")
    print(f"    Total generados:   {len(contratos)}")
    print(f"    Completados:       {contratos_completados}")
    print(f"    Pendientes:        {contratos_pendientes}")
    print(f"    Ingresos facturados: ${ingresos_totales:,.0f} COP")
    print()
    print(f"  CALIFICACIONES")
    print(f"    Total registradas: {len(calificaciones)}")
    if calificaciones:
        prom = sum(c["puntuacion"] for c in calificaciones) / len(calificaciones)
        print(f"    Rating promedio:   {prom:.2f} *")

    print()
    print(f"  VALORES FIJOS DEL SISTEMA (TUPLAS INMUTABLES):")
    print(f"    Categorias:        {CATEGORIAS_SERVICIO}")
    print(f"    Estados contrato:  {ESTADOS_CONTRATO}")
    print(f"    Ciudades:          {CIUDADES_COBERTURA}")
    print(f"    Roles admitidos:   {ROLES_SISTEMA}")
