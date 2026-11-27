"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Clases de Usuario con Herencia y Sobrescritura de Metodos (Guia 11)
========================================================================================
[GUIA 11 - ACTIVIDAD 3]: Clase Usuario con constructor __init__(), atributos y metodos.
[GUIA 11 - ACTIVIDAD 4]: Getters y setters con @property que validan correo, nombre
                         y telefono antes de almacenarlos.
[GUIA 11 - ACTIVIDAD 5]: Herencia. Usuario es la clase base; Cliente, Prestador y
                         Administrador son clases derivadas que heredan presentar(),
                         verificar_credenciales() y a_diccionario(), y sobrescriben
                         describir_rol() y permisos().
[GUIA 11 - ACTIVIDAD 6]: Sobrescritura de operadores: __eq__() compara usuarios por
                         correo y __str__() define su representacion textual.

El resto del sistema sigue guardando los usuarios como diccionarios en el vector
'usuarios' (Guias 7 y 8). Estas clases se usan en el login y en el registro, y se
convierten a diccionario con a_diccionario() para almacenarlas y guardarlas en archivo.
========================================================================================
"""

from core.constantes import ROLES_SISTEMA


class Usuario:
    """Clase base que representa a cualquier persona registrada en YPRI."""

    def __init__(self, id_usuario, nombre, correo, contrasena, rol, ciudad, telefono):
        # Atributos del objeto. Los que tienen setter pasan por su validacion.
        self.id = id_usuario
        self.nombre = nombre
        self.correo = correo
        self._contrasena = contrasena
        self.rol = rol
        self.ciudad = ciudad
        self.telefono = telefono

    # ------------------------------------------------------------------------------
    # [GUIA 11 - ACTIVIDAD 4] GETTERS Y SETTERS CON VALIDACION
    # ------------------------------------------------------------------------------
    @property
    def nombre(self):
        """Getter: retorna el nombre del usuario."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Setter: exige un nombre con letras y lo guarda con formato Titulo."""
        texto = str(valor).strip()
        if len(texto) < 3 or not all(c.isalpha() or c.isspace() for c in texto):
            raise ValueError("El nombre debe tener al menos 3 letras y solo letras o espacios.")
        self._nombre = texto

    @property
    def correo(self):
        """Getter: retorna el correo normalizado en minusculas."""
        return self._correo

    @correo.setter
    def correo(self, valor):
        """Setter: valida que el correo tenga usuario, '@' y dominio con punto."""
        texto = str(valor).strip().lower()
        if "@" not in texto or " " in texto:
            raise ValueError("El correo debe contener '@' y no tener espacios.")
        usuario, dominio = texto.split("@", 1)
        if not usuario or "." not in dominio:
            raise ValueError("El correo debe tener el formato usuario@dominio.com.")
        self._correo = texto

    @property
    def telefono(self):
        """Getter: retorna el telefono de 10 digitos."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        """Setter: el telefono debe tener exactamente 10 digitos numericos."""
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) != 10:
            raise ValueError("El telefono debe tener exactamente 10 digitos.")
        self._telefono = texto

    # ------------------------------------------------------------------------------
    # METODOS HEREDADOS POR TODAS LAS CLASES DERIVADAS
    # ------------------------------------------------------------------------------
    def verificar_credenciales(self, correo, contrasena):
        """Retorna True si el correo y la contrasena coinciden con los del usuario."""
        return self.correo == str(correo).strip().lower() and self._contrasena == contrasena

    def describir_rol(self):
        """Descripcion general del rol. Las clases derivadas la sobrescriben."""
        return "Usuario del sistema YPRI"

    def permisos(self):
        """Tupla de acciones permitidas. Las clases derivadas la sobrescriben."""
        return ("ver catalogo",)

    def presentar(self):
        """
        Procedimiento heredado: imprime la bienvenida usando describir_rol() y permisos().
        Como esos dos metodos estan sobrescritos, el mismo codigo muestra un mensaje
        distinto para cada tipo de usuario (polimorfismo).
        """
        print(f"\n[OK] Bienvenido/a, {self.nombre}!")
        print(f"     {self.describir_rol()} | Ciudad: {self.ciudad}")
        print(f"     Puede: {', '.join(self.permisos())}")

    def a_diccionario(self):
        """Convierte el objeto en el diccionario que usa el vector 'usuarios'."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self._contrasena,
            "rol": self.rol,
            "ciudad": self.ciudad,
            "telefono": self.telefono,
        }

    @staticmethod
    def desde_diccionario(registro):
        """
        Crea el objeto de la clase derivada que corresponde al rol del registro.
        Ejemplo: un diccionario con rol 'prestador' produce un objeto Prestador.
        """
        clases = {"cliente": Cliente, "prestador": Prestador, "admin": Administrador}
        rol = registro.get("rol", "cliente")
        if rol not in ROLES_SISTEMA:
            raise ValueError(f"Rol desconocido: {rol}")
        clase = clases[rol]
        return clase(
            registro["id"],
            registro["nombre"],
            registro["correo"],
            registro["contrasena"],
            registro.get("ciudad", "Cucuta"),
            registro.get("telefono", "0000000000"),
        )

    # ------------------------------------------------------------------------------
    # [GUIA 11 - ACTIVIDAD 6] SOBRESCRITURA DE OPERADORES
    # ------------------------------------------------------------------------------
    def __eq__(self, otro):
        """Operador ==: dos usuarios son iguales si tienen el mismo correo."""
        if not isinstance(otro, Usuario):
            return NotImplemented
        return self.correo == otro.correo

    def __hash__(self):
        return hash(self.correo)

    def __str__(self):
        """Representacion textual usada al imprimir el objeto."""
        return f"{self.id} | {self.nombre} | {self.rol} | {self.correo}"


class Cliente(Usuario):
    """Clase derivada: persona que contrata servicios a domicilio."""

    def __init__(self, id_usuario, nombre, correo, contrasena, ciudad, telefono):
        # super() reutiliza el constructor de la clase base (herencia)
        super().__init__(id_usuario, nombre, correo, contrasena, "cliente", ciudad, telefono)

    def describir_rol(self):
        """Sobrescritura: descripcion propia del cliente."""
        return "Cliente: contrata y califica servicios a domicilio"

    def permisos(self):
        """Sobrescritura: acciones del cliente."""
        return ("buscar servicios", "contratar", "calificar")


class Prestador(Usuario):
    """Clase derivada: profesional que publica sus servicios en YPRI."""

    def __init__(self, id_usuario, nombre, correo, contrasena, ciudad, telefono):
        super().__init__(id_usuario, nombre, correo, contrasena, "prestador", ciudad, telefono)

    def describir_rol(self):
        """Sobrescritura: descripcion propia del prestador."""
        return "Prestador: publica servicios y atiende contratos"

    def permisos(self):
        """Sobrescritura: acciones del prestador."""
        return ("publicar servicios", "modificar servicios", "exportar a Excel")

    def contar_servicios(self, lista_servicios):
        """Metodo propio de la clase derivada: cuenta los servicios que publico."""
        return len([s for s in lista_servicios if s["prestador_id"] == self.id])


class Administrador(Usuario):
    """Clase derivada: responsable de la operacion de la plataforma."""

    def __init__(self, id_usuario, nombre, correo, contrasena, ciudad, telefono):
        super().__init__(id_usuario, nombre, correo, contrasena, "admin", ciudad, telefono)

    def describir_rol(self):
        """Sobrescritura: descripcion propia del administrador."""
        return "Administrador: supervisa usuarios, servicios y reportes"

    def permisos(self):
        """Sobrescritura: acciones del administrador."""
        return ("gestionar usuarios", "auditar matrices", "importar y exportar Excel", "respaldar datos")
