"""
========================================================================================
GUÍA DE APRENDIZAJE N.º 10 - ACTIVIDAD PRÁCTICA (SECCIÓN 2)
SISTEMA DE INVENTARIO CON FUNCIONES
========================================================================================
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos
Institución: Fundación de Estudios Superiores Comfanorte (FESC) - 2026
Integrantes: Jann Pierre Ortiz Zambrano y Josué David Rincón Palomino
========================================================================================
Este programa corresponde al ejercicio guiado de la Sección 2 de la Guía 10.
Implementa registro de productos, cálculo de subtotal con función y return,
procedimientos para mostrar y buscar, cálculo de total de inventario,
ordenamiento con función lambda y un menú interactivo.
========================================================================================
"""

# SISTEMA DE INVENTARIO CON FUNCIONES
productos = []


# REGISTRAR PRODUCTO
def registrar_producto():
    print("\nREGISTRAR PRODUCTO")
    codigo = input("Código: ").strip()
    nombre = input("Nombre: ").strip()

    for producto in productos:
        if producto["codigo"] == codigo:
            print("El código ya existe.")
            return

    try:
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad: "))

        if not codigo or not nombre:
            print("Código y nombre son requeridos.")
            return

        if precio < 0 or cantidad < 0:
            print("Los valores no pueden ser negativos.")
            return

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad
        }

        productos.append(producto)
        print("Producto registrado correctamente.")

    except ValueError:
        print("Ingrese valores numéricos válidos.")


# CALCULAR VALOR DE UN PRODUCTO
def calcular_subtotal(precio, cantidad):
    return precio * cantidad


# MOSTRAR PRODUCTOS
def mostrar_productos():
    print("\nLISTADO DE PRODUCTOS")

    if not productos:
        print("No existen productos registrados.")
        return

    for producto in productos:
        subtotal = calcular_subtotal(
            producto["precio"],
            producto["cantidad"]
        )

        print("--------------------")
        print("Código:", producto["codigo"])
        print("Nombre:", producto["nombre"])
        print("Precio:", producto["precio"])
        print("Cantidad:", producto["cantidad"])
        print("Subtotal:", subtotal)


# BUSCAR PRODUCTO
def buscar_producto():
    codigo = input("\nCódigo a buscar: ").strip()

    for producto in productos:
        if producto["codigo"] == codigo:
            print("Producto encontrado:")
            print(producto)
            return

    print("Producto no encontrado.")


# CALCULAR TOTAL DEL INVENTARIO
def calcular_total_inventario():
    total = 0

    for producto in productos:
        total += calcular_subtotal(
            producto["precio"],
            producto["cantidad"]
        )

    return total


# ORDENAR PRODUCTOS
def ordenar_productos():
    ordenados = sorted(
        productos,
        key=lambda producto: producto["precio"]
    )

    print("\nPRODUCTOS ORDENADOS POR PRECIO")

    for producto in ordenados:
        print(producto["nombre"], "-", producto["precio"])


# MENÚ PRINCIPAL
def mostrar_menu():
    print("\n===== SISTEMA DE INVENTARIO =====")
    print("1. Registrar producto")
    print("2. Mostrar productos")
    print("3. Buscar producto")
    print("4. Calcular total del inventario")
    print("5. Ordenar productos por precio")
    print("0. Salir")


def iniciar_programa():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            buscar_producto()
        elif opcion == "4":
            total = calcular_total_inventario()
            print("Valor total:", total)
        elif opcion == "5":
            ordenar_productos()
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida.")


# EJECUTAR PROGRAMA
if __name__ == "__main__":
    iniciar_programa()
