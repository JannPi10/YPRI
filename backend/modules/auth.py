"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Autenticacion, Gestion de Usuarios y Control de Sesion
========================================================================================
DOCUMENTACION DE TEMAS POR SEMANAS:
- [SEMANAS 5 Y 6 - CICLOS Y CONDICIONALES]:
  * Verificacion de existencia de correo con ciclos for y comparaciones de igualdad.
  * Bucle de captura con intentos y cancelacion controlada.
- [SEMANA 7 - TUPLAS, CADENAS Y DICCIONARIOS]:
  * Creacion de nuevos usuarios como diccionarios con claves estructuradas.
  * Validacion de rol contra la tupla ROLES_SISTEMA ("cliente", "prestador", "admin").
  * Normalizacion de correos con .strip().lower().
- [SEMANA 8 - VECTORES EN PYTHON]:
  * Almacenamiento dinamico del nuevo usuario en el vector usuarios[] usando .append().
  * Generacion automatica de ID correlativo usando len(usuarios).
- [SEMANA 9 - MATRICES EN PYTHON]:
  * Segregacion de permisos: los administradores tienen acceso a la auditoria de matrices
    y los clientes/prestadores a los reportes analiticos asociados.
- [GUIA 11 - PROGRAMACION ORIENTADA A OBJETOS]:
  * login() convierte cada registro en un objeto (Cliente, Prestador o Administrador)
    y usa su metodo heredado verificar_credenciales() y el procedimiento presentar(),
    que muestra un texto distinto segun el metodo describir_rol() sobrescrito.
  * registrar_usuario() crea el objeto con su clase; los setters validan nombre,
    correo y telefono, y luego se guarda con a_diccionario().
  * Cada inicio de sesion y registro queda en el historial (archivo, modo "a").
========================================================================================
"""

from core.constantes import ROLES_SISTEMA
from models.usuario import Usuario
from modules.persistencia import registrar_evento, guardar_datos
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

    # GUIA 8 - ACTIVIDAD 6: Busqueda secuencial en el vector de usuarios
    # GUIA 11: cada registro se convierte en un objeto de su clase (herencia)
    for usuario in usuarios:
        try:
            objeto_usuario = Usuario.desde_diccionario(usuario)
        except (ValueError, KeyError):
            continue  # registro incompleto: se omite sin detener el login
        if objeto_usuario.verificar_credenciales(correo, contrasena):
            set_sesion_actual(usuario)
            # Metodo heredado que usa describir_rol() sobrescrito en cada clase derivada
            objeto_usuario.presentar()
            registrar_evento(f"Inicio de sesion: {objeto_usuario}")
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

    # GUIA 11: el registro se crea como OBJETO de la clase que corresponde al rol.
    # Los setters de la clase validan de nuevo nombre, correo y telefono.
    try:
        objeto_usuario = Usuario.desde_diccionario({
            "id": nuevo_id,
            "nombre": nombre,
            "correo": correo,
            "contrasena": contrasena,
            "rol": rol,
            "ciudad": ciudad,
            "telefono": telefono
        })
    except ValueError as error:
        print(f"[!] No se pudo registrar el usuario: {error}")
        return

    # Insercion en la coleccion en memoria como DICCIONARIO (Guias 7 y 8)
    usuarios.append(objeto_usuario.a_diccionario())
    guardar_datos()
    registrar_evento(f"Usuario registrado: {objeto_usuario}")

    print(f"\n[OK] Usuario '{objeto_usuario.nombre}' registrado exitosamente con ID {nuevo_id}.")
    print(f"     {objeto_usuario.describir_rol()}")
    print(f"     Total de usuarios en YPRI: {len(usuarios)}")
