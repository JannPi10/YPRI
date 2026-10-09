"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Constantes Inmutables del Sistema (Tuplas)
========================================================================================
Valores fijos definidos que no cambian durante la ejecucion del programa.
Garantizan consistencia e integridad referencial en toda la aplicacion.
========================================================================================
"""

# TUPLA: roles permitidos en el sistema
ROLES_SISTEMA = ("cliente", "prestador", "admin")

# TUPLA: categorias oficiales de servicios ofrecidos en YPRI
CATEGORIAS_SERVICIO = (
    "Electricidad",
    "Plomeria",
    "Limpieza",
    "Climatizacion",
    "Cerrajeria"
)

# TUPLA: estados posibles del ciclo de vida de un contrato
ESTADOS_CONTRATO = (
    "Pendiente",
    "En proceso",
    "Completado",
    "Cancelado"
)

# TUPLA: ciudades de cobertura geografica de la plataforma
CIUDADES_COBERTURA = (
    "Cucuta",
    "Cali",
    "Bogota",
    "Medellin",
    "Bucaramanga"
)

# Tasa del Impuesto al Valor Agregado (IVA en Colombia: 19%)
IVA_PORCENTAJE = 0.19
