"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Autenticacion, Gestion de Usuarios y Control de Sesion
========================================================================================
Responsabilidades:
- Registro de nuevos usuarios con verificacion de correo unico
- Autenticacion y validacion de credenciales
- Control de sesion activa (cliente, prestador o administrador)
========================================================================================
"""

from core.constantes import ROLES_SISTEMA
from core.validaciones import (
    mostrar_encabezado,
    pedir_correo,
    pedir_solo_letras,
    pedir_ciudad,
    generar_id,
)
from data.database import (
    usuarios,
    get_sesion_actual,
    set_sesion_actual,
    limpiar_sesion,
)


def login():
    """
    Solicita credenciales de acceso y autentica al usuario.
    Recorre la lista de diccionarios 'usuarios' comparando correo y clave.
    Retorna True si la autenticacion fue exitosa, False en caso contrario.
    """
    mostrar_encabezado("INICIAR SESION")
    print()

    correo = pedir_correo("  Correo electronico: ")

    contrasena = input("  Contrasena: ").strip()
    while contrasena == "":
        print("[!] La contrasena no puede estar vacia.")
        contrasena = input("  Contrasena: ").strip()

    # Busqueda secuencial en coleccion de usuarios
    for usuario in usuarios:
        if usuario["correo"] == correo and usuario["contrasena"] == contrasena:
            set_sesion_actual(usuario)
            print(f"\n[OK] Bienvenido/a, {usuario['nombre']}!")
            print(f"     Rol: {usuario['rol'].capitalize()} | Ciudad: {usuario['ciudad']}")
            return True

    print("\n[!] Correo o contrasena incorrectos. Intente de nuevo.")
    return False


def cerrar_sesion():
    """Finaliza la sesion del usuario activo."""
    limpiar_sesion()
    print("\n[i] Sesion cerrada exitosamente.")


def registrar_usuario():
    """
    Registra una nueva cuenta de usuario en el sistema.
    Aplica normalizacion de cadenas (.strip(), .lower(), .title())
    y valida que el rol pertenezca a la tupla inmutable ROLES_SISTEMA.
    """
    mostrar_encabezado("REGISTRO DE USUARIO")
    print()

    nuevo_id = generar_id("USR", usuarios)

    # Validacion de no duplicidad de correo
    correo = pedir_correo("  Correo electronico: ")
    for u in usuarios:
        if u["correo"] == correo:
            print(f"[!] Ya existe una cuenta registrada con el correo '{correo}'.")
            return

    nombre = pedir_solo_letras("  Nombre completo: ", "nombre").title()

    # Validacion de robustez de contrasena
    while True:
        contrasena = input("  Contrasena (minimo 6 caracteres, sin espacios al inicio/fin): ").strip()
        if len(contrasena) < 6:
            print("[!] La contrasena debe tener al menos 6 caracteres.")
            continue
        if not any(c.isalnum() for c in contrasena):
            print("[!] La contrasena debe contener al menos un caracter alfanumerico.")
            continue
        break

    # Validacion del rol contra la tupla de roles oficiales
    print(f"  Roles disponibles: {', '.join(ROLES_SISTEMA)}")
    while True:
        rol = input("  Rol (cliente / prestador): ").strip().lower()
        if rol in ROLES_SISTEMA:
            break
        print(f"[!] Rol invalido. Opciones: {', '.join(ROLES_SISTEMA)}")

    # Validacion de telefono de 10 digitos
    telefono = input("  Telefono (10 digitos): ").strip()
    while not telefono.isdigit() or len(telefono) != 10:
        print("[!] Ingrese un telefono de 10 digitos numericos.")
        telefono = input("  Telefono: ").strip()

    ciudad = pedir_ciudad()

    # Creacion del registro como DICCIONARIO
    nuevo_usuario = {
        "id": nuevo_id,
        "nombre": nombre,
        "correo": correo,
        "contrasena": contrasena,
        "rol": rol,
        "ciudad": ciudad,
        "telefono": telefono
    }

    # Insercion en la coleccion en memoria
    usuarios.append(nuevo_usuario)

    print(f"\n[OK] Usuario '{nombre}' registrado exitosamente con ID {nuevo_id}.")
    print(f"     Total de usuarios en YPRI: {len(usuarios)}")
