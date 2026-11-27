"""
[GUIA 11 - PROGRAMACION ORIENTADA A OBJETOS]
Paquete de clases del dominio de YPRI: usuarios (con herencia), servicios y facturas.
"""

from models.usuario import Usuario, Cliente, Prestador, Administrador
from models.servicio import Servicio
from models.factura import Factura

__all__ = ["Usuario", "Cliente", "Prestador", "Administrador", "Servicio", "Factura"]
