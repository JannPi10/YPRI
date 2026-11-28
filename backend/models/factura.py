"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Clase Factura con Sobrescritura del Operador + (Guia 11)
========================================================================================
[GUIA 11 - ACTIVIDAD 3]: Cada contrato genera una Factura con subtotal, IVA y total.
[GUIA 11 - ACTIVIDAD 4]: El setter de 'subtotal' impide valores negativos y la
                         propiedad 'total' se calcula (solo lectura).
[GUIA 11 - ACTIVIDAD 6]: __add__() suma dos facturas y produce una factura consolidada.
                         Con __radd__() tambien funciona sum(lista_de_facturas).
                         __eq__() compara facturas por total y __str__() define su texto.

Se usa en el reporte de estadisticas del administrador (modules/admin.py) y en la
hoja 'Contratos' del Excel exportado (modules/reportes_excel.py).
========================================================================================
"""

from core.constantes import IVA_PORCENTAJE


class Factura:
    """Factura de uno o varios contratos de servicio."""

    def __init__(self, concepto, subtotal, iva=None, cantidad_contratos=1):
        self.concepto = concepto
        self.subtotal = subtotal
        # Si no se indica el IVA, se calcula con la tasa oficial (19 %)
        self.iva = round(self.subtotal * IVA_PORCENTAJE, 2) if iva is None else round(float(iva), 2)
        self.cantidad_contratos = cantidad_contratos

    @property
    def subtotal(self):
        """Getter del valor antes de impuestos."""
        return self._subtotal

    @subtotal.setter
    def subtotal(self, valor):
        """Setter: el subtotal no puede ser negativo."""
        monto = float(valor)
        if monto < 0:
            raise ValueError("El subtotal de una factura no puede ser negativo.")
        self._subtotal = round(monto, 2)

    @property
    def total(self):
        """Propiedad de solo lectura: subtotal + IVA."""
        return round(self.subtotal + self.iva, 2)

    @classmethod
    def desde_contrato(cls, contrato):
        """
        Crea la factura de un contrato del vector 'contratos'.
        El contrato guarda el total con IVA; aqui se separa el subtotal y el impuesto.
        """
        total = float(contrato["total"])
        subtotal = round(total / (1 + IVA_PORCENTAJE), 2)
        return cls(f"{contrato['id']} - {contrato['servicio_nombre']}", subtotal, round(total - subtotal, 2))

    @classmethod
    def vacia(cls):
        """Factura en cero, punto de partida para acumular sumas."""
        return cls("Sin contratos", 0, 0, cantidad_contratos=0)

    # ------------------------------------------------------------------------------
    # [GUIA 11 - ACTIVIDAD 6] SOBRESCRITURA DE OPERADORES
    # ------------------------------------------------------------------------------
    def __add__(self, otra):
        """Operador +: suma subtotales, IVA y cantidad de contratos de dos facturas."""
        if not isinstance(otra, Factura):
            return NotImplemented
        return Factura(
            "Facturacion consolidada",
            self.subtotal + otra.subtotal,
            self.iva + otra.iva,
            self.cantidad_contratos + otra.cantidad_contratos,
        )

    def __radd__(self, otro):
        """Permite usar sum(facturas), que empieza sumando 0 + primera factura."""
        if otro == 0:
            return self
        return self.__add__(otro)

    def __eq__(self, otra):
        """Operador ==: dos facturas son iguales si tienen el mismo total."""
        if not isinstance(otra, Factura):
            return NotImplemented
        return self.total == otra.total

    def __str__(self):
        return (f"{self.concepto}: subtotal ${self.subtotal:,.2f} + IVA ${self.iva:,.2f} "
                f"= ${self.total:,.2f} COP ({self.cantidad_contratos} contrato(s))")
