"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Clase Servicio con Encapsulamiento y Sobrescritura de Operadores (Guia 11)
========================================================================================
[GUIA 11 - ACTIVIDAD 3]: La entidad principal del proyecto, el servicio a domicilio,
                         se representa con la clase Servicio (constructor, atributos
                         y metodos como calcular_costo() y cambiar_disponibilidad()).
[GUIA 11 - ACTIVIDAD 4]: Getters y setters con @property. Los setters impiden guardar
                         una categoria inexistente, una descripcion corta, una tarifa
                         fuera de rango o una calificacion fuera de 0 a 5.
[GUIA 11 - ACTIVIDAD 6]: __eq__() compara servicios por codigo (se usa para no importar
                         duplicados desde Excel) y __str__() define su texto.

Se usa en publicar_servicio() y modificar_servicio() (modules/servicios.py) y en la
importacion desde Excel (modules/reportes_excel.py).
========================================================================================
"""

from core.constantes import CATEGORIAS_SERVICIO, CIUDADES_COBERTURA, IVA_PORCENTAJE

# Limites de tarifa por hora en COP (los mismos que usa la validacion de consola)
TARIFA_MINIMA = 10000.0
TARIFA_MAXIMA = 500000.0


class Servicio:
    """Servicio a domicilio publicado por un prestador."""

    def __init__(self, codigo, prestador_id, prestador_nombre, categoria, descripcion,
                 tarifa_hora, ciudad="Cucuta", zona="Centro", lat=7.8939, lng=-72.5078,
                 radio_km=10, disponible=True, calificacion=5.0, num_contratos=0):
        self.codigo = str(codigo).strip().upper()
        self.prestador_id = prestador_id
        self.prestador_nombre = prestador_nombre
        # Los siguientes atributos pasan por sus setters (validacion)
        self.categoria = categoria
        self.descripcion = descripcion
        self.tarifa_hora = tarifa_hora
        self.ciudad = ciudad
        self.calificacion = calificacion
        # Atributos de geolocalizacion y operacion
        self.zona = zona
        self.lat = float(lat)
        self.lng = float(lng)
        self.radio_km = int(radio_km)
        self.disponible = bool(disponible)
        self.num_contratos = int(num_contratos)

    # ------------------------------------------------------------------------------
    # [GUIA 11 - ACTIVIDAD 4] GETTERS Y SETTERS
    # ------------------------------------------------------------------------------
    @property
    def categoria(self):
        """Getter de la categoria (oficio) del servicio."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        """Setter: la categoria debe pertenecer a la tupla CATEGORIAS_SERVICIO."""
        texto = str(valor).strip().capitalize()
        if texto not in CATEGORIAS_SERVICIO:
            raise ValueError(f"Categoria invalida: '{valor}'. Opciones: {', '.join(CATEGORIAS_SERVICIO)}.")
        self._categoria = texto

    @property
    def descripcion(self):
        """Getter de la descripcion."""
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        """Setter: minimo 10 caracteres y al menos una letra."""
        texto = str(valor).strip()
        if len(texto) < 10 or not any(c.isalpha() for c in texto):
            raise ValueError("La descripcion debe tener al menos 10 caracteres con letras.")
        self._descripcion = texto

    @property
    def tarifa_hora(self):
        """Getter de la tarifa por hora en COP."""
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor):
        """Setter: convierte a float y exige una tarifa entre $10.000 y $500.000."""
        try:
            tarifa = float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"La tarifa debe ser un numero (recibido: '{valor}').")
        if tarifa < TARIFA_MINIMA or tarifa > TARIFA_MAXIMA:
            raise ValueError(f"La tarifa debe estar entre ${TARIFA_MINIMA:,.0f} y ${TARIFA_MAXIMA:,.0f} COP.")
        self._tarifa_hora = tarifa

    @property
    def ciudad(self):
        """Getter de la ciudad de cobertura."""
        return self._ciudad

    @ciudad.setter
    def ciudad(self, valor):
        """Setter: la ciudad debe ser una de las ciudades de cobertura."""
        texto = str(valor).strip().capitalize()
        if texto not in CIUDADES_COBERTURA:
            raise ValueError(f"Ciudad sin cobertura: '{valor}'. Opciones: {', '.join(CIUDADES_COBERTURA)}.")
        self._ciudad = texto

    @property
    def calificacion(self):
        """Getter de la calificacion promedio."""
        return self._calificacion

    @calificacion.setter
    def calificacion(self, valor):
        """Setter: la calificacion debe estar entre 0 y 5."""
        puntaje = float(valor)
        if puntaje < 0 or puntaje > 5:
            raise ValueError("La calificacion debe estar entre 0 y 5.")
        self._calificacion = round(puntaje, 2)

    # ------------------------------------------------------------------------------
    # METODOS DE LA ENTIDAD
    # ------------------------------------------------------------------------------
    def calcular_costo(self, horas):
        """Retorna el costo total de contratar el servicio por 'horas', con IVA."""
        if horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")
        return round(self.tarifa_hora * horas * (1 + IVA_PORCENTAJE), 2)

    def cambiar_disponibilidad(self, disponible):
        """Activa o desactiva el servicio en el catalogo."""
        self.disponible = bool(disponible)

    def a_diccionario(self):
        """Convierte el objeto en el diccionario que usa el vector 'servicios'."""
        return {
            "codigo": self.codigo,
            "prestador_id": self.prestador_id,
            "prestador_nombre": self.prestador_nombre,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "tarifa_hora": self.tarifa_hora,
            "ciudad": self.ciudad,
            "zona": self.zona,
            "lat": self.lat,
            "lng": self.lng,
            "radio_km": self.radio_km,
            "disponible": self.disponible,
            "calificacion": self.calificacion,
            "num_contratos": self.num_contratos,
        }

    @classmethod
    def desde_diccionario(cls, registro):
        """Crea un objeto Servicio a partir de un registro del vector 'servicios'."""
        return cls(
            registro["codigo"], registro["prestador_id"], registro["prestador_nombre"],
            registro["categoria"], registro["descripcion"], registro["tarifa_hora"],
            registro.get("ciudad", "Cucuta"), registro.get("zona", "Centro"),
            registro.get("lat", 7.8939), registro.get("lng", -72.5078),
            registro.get("radio_km", 10), registro.get("disponible", True),
            registro.get("calificacion", 5.0), registro.get("num_contratos", 0),
        )

    # ------------------------------------------------------------------------------
    # [GUIA 11 - ACTIVIDAD 6] SOBRESCRITURA DE OPERADORES
    # ------------------------------------------------------------------------------
    def __eq__(self, otro):
        """Operador ==: dos servicios son el mismo si comparten el codigo."""
        if not isinstance(otro, Servicio):
            return NotImplemented
        return self.codigo == otro.codigo

    def __hash__(self):
        return hash(self.codigo)

    def __str__(self):
        """Texto del servicio, por ejemplo al imprimirlo en el catalogo."""
        estado = "Disponible" if self.disponible else "Ocupado"
        return (f"{self.codigo} | {self.categoria:13} | {self.prestador_nombre:18} | "
                f"${self.tarifa_hora:,.0f}/h | {self.calificacion:.1f}* | {estado}")
