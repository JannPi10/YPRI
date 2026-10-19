"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Base de Datos y Persistencia en Memoria (Vectores de Diccionarios)
========================================================================================
GUIA 8 - VECTORES EN PYTHON: ALMACENAMIENTO, ORDENAMIENTO Y BUSQUEDA DE DATOS
- Actividad 1 y 2: Implementacion de vectores (listas unidimensionales) en Python
  donde cada posicion indexada (0, 1, 2...) almacena un registro de la entidad
  representado como un diccionario con atributos estructurados.
- Actividad 1.2: Almacenamiento dinamico mediante append() y consulta con len().
[YA SE CUMPLIA DESDE GUIAS PREVIAS]: Se mantiene la coleccion existente sin duplicar.
========================================================================================
"""

# GUIA 8 - VECTOR DE USUARIOS: lista unidimensional indexada de diccionarios
usuarios = [
    {
        "id": "USR-001",
        "nombre": "Juan Perez",
        "correo": "juan.perez@email.com",
        "contrasena": "juan123",
        "rol": "cliente",
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

# GUIA 8 - VECTOR DE SERVICIOS (ENTIDAD PRINCIPAL DE GUIA 8):
# Vector unidimensional que almacena los registros de servicios publicados.
servicios = [
    {
        "codigo": "SERV-01",
        "prestador_id": "USR-002",
        "prestador_nombre": "Carlos Gomez",
        "categoria": "Electricidad",
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

# GUIA 8 - VECTOR DE CONTRATOS: lista unidimensional de acuerdos y cotizaciones
contratos = [
    {
        "id": "CONTR-101",
        "cliente_id": "USR-001",
        "cliente_nombre": "Juan Perez",
        "servicio_codigo": "SERV-01",
        "servicio_nombre": "Electricidad - Carlos Gomez",
        "horas": 5,
        "tarifa_hora": 35000.0,
        "total": 179400.0,      # Tarifa base + 19% IVA
        "estado": "Completado",
        "calificacion": 4.8,
        "comentario": "Excelente trabajo, muy puntual"
    }
]

# GUIA 8 - VECTOR DE CALIFICACIONES: lista unidimensional de resenas
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

# Estado de sesion autenticada en memoria
_usuario_sesion = None


def get_sesion_actual():
    """Retorna el usuario con sesion iniciada actualmente o None."""
    global _usuario_sesion
    return _usuario_sesion


def set_sesion_actual(usuario):
    """Establece el usuario con sesion iniciada."""
    global _usuario_sesion
    _usuario_sesion = usuario


def limpiar_sesion():
    """Cierra la sesion activa restaurando el valor a None."""
    global _usuario_sesion
    _usuario_sesion = None
