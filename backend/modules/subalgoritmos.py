"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Módulo: Subalgoritmos (Funciones, Procedimientos, Lambdas y Modularización)
========================================================================================
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos | Tema: 5. Subalgoritmos
Institución: Fundación de Estudios Superiores Comfanorte (FESC) - 2026
Integrantes: Jann Pierre Ortiz Zambrano y Josué David Rincón Palomino
========================================================================================
DOCUMENTACIÓN DE CUMPLIMIENTO GUÍA DE APRENDIZAJE N.º 10:
- ACTIVIDAD 1: Identificación y clasificación de subalgoritmos (funciones vs procedimientos).
- ACTIVIDAD 2: Funciones con parámetros y retorno explícito (return) para cálculos clave:
    1. calcular_liquidacion_contrato(...) -> dict
    2. calcular_comision_plataforma(...) -> dict
    3. calcular_promedio_calificacion(...) -> float
    4. calcular_metricas_prestador(...) -> dict
    5. calcular_resumen_estadistico(...) -> dict
- ACTIVIDAD 3: Procedimientos de interacción que ejecutan tareas sin valor de retorno:
    1. mostrar_recibo_liquidacion(...)
    2. mostrar_ficha_tecnica_servicio(...)
    3. mostrar_tarjeta_rendimiento_prestador(...)
    4. mostrar_resumen_inventario(...)
- ACTIVIDAD 4: Funciones lambda aplicadas a cálculos rápidos y criterios de ordenamiento:
    * lambda_descuento, lambda_iva, lambda_formato_cop
    * Ordenamientos por precio/tarifa, calificación y monto de contrato.
- ACTIVIDAD 5: Gestión de variables locales vs globales y análisis empírico del paso de
  argumentos por valor (inmutables: int, float, str) y por referencia (mutables: list, dict).
- ACTIVIDAD 6: Modularización del aplicativo: centralización de responsabilidades,
  eliminación de instrucciones repetidas (principio DRY) y conservación del 100% de
  las funcionalidades previas (semanas 5, 6, 7, 8 y 9).
========================================================================================
"""

from core.constantes import IVA_PORCENTAJE
from core.validaciones import separador, mostrar_encabezado


# ========================================================================================
# ACTIVIDAD 4. APLICACIÓN DE FUNCIONES LAMBDA
# Expresiones breves para cálculos inmediatos y formateo
# ========================================================================================

# Lambdas de cálculo aritmético
calcular_descuento_lambda = lambda subtotal, pct: round(subtotal * (pct / 100.0), 2)
calcular_iva_lambda = lambda base, tasa=IVA_PORCENTAJE: round(base * tasa, 2)
formatear_cop_lambda = lambda valor: f"${valor:,.0f} COP"


# ========================================================================================
# ACTIVIDAD 2. IMPLEMENTACIÓN DE FUNCIONES CON PARÁMETROS Y RETURN
# Bloques reutilizables con lógica pura de negocio, sin acoplamiento a entradas por consola.
# ========================================================================================

def calcular_liquidacion_contrato(tarifa_hora: float, horas: int, descuento_pct: float = 0.0, tasa_iva: float = IVA_PORCENTAJE) -> dict:
    """
    [GUÍA 10 - ACTIVIDAD 2 - FUNCIÓN 1]
    Calcula la liquidación financiera completa de un servicio cotizado.
    
    Parámetros:
        tarifa_hora (float): Tarifa por hora del servicio en COP. Debe ser >= 0.
        horas (int): Cantidad de horas estimadas o laboradas. Debe ser >= 1.
        descuento_pct (float): Porcentaje de descuento promocional (0 a 100).
        tasa_iva (float): Tasa impositiva del IVA (por defecto 0.19 = 19%).
        
    Retorna:
        dict: Diccionario estructurado con el desglose exacto:
            {
                "subtotal_bruto": float,
                "descuento_pct": float,
                "monto_descuento": float,
                "subtotal_neto": float,
                "tasa_iva": float,
                "monto_iva": float,
                "total_pagar": float
            }
    """
    if tarifa_hora < 0 or horas < 1 or descuento_pct < 0 or descuento_pct > 100:
        raise ValueError("Parámetros de liquidación fuera de los límites permitidos.")

    subtotal_bruto = round(tarifa_hora * horas, 2)
    monto_descuento = calcular_descuento_lambda(subtotal_bruto, descuento_pct)
    subtotal_neto = round(subtotal_bruto - monto_descuento, 2)
    monto_iva = calcular_iva_lambda(subtotal_neto, tasa_iva)
    total_pagar = round(subtotal_neto + monto_iva, 2)

    return {
        "tarifa_hora": tarifa_hora,
        "horas": horas,
        "subtotal_bruto": subtotal_bruto,
        "descuento_pct": descuento_pct,
        "monto_descuento": monto_descuento,
        "subtotal_neto": subtotal_neto,
        "tasa_iva": tasa_iva,
        "monto_iva": monto_iva,
        "total_pagar": total_pagar,
    }


def calcular_comision_plataforma(total_pagar: float, porcentaje_comision: float = 0.10, retencion_pct: float = 0.04) -> dict:
    """
    [GUÍA 10 - ACTIVIDAD 2 - FUNCIÓN 2]
    Calcula la distribución financiera entre la plataforma YPRI y el prestador del servicio.
    
    Parámetros:
        total_pagar (float): Valor total facturado del servicio.
        porcentaje_comision (float): Comisión operacional de YPRI (ej. 10% = 0.10).
        retencion_pct (float): Retención tributaria en la fuente (ej. 4% = 0.04).
        
    Retorna:
        dict: Desglose financiero con comisión, retención y pago neto transferido al prestador.
    """
    if total_pagar < 0:
        raise ValueError("El total a pagar no puede ser negativo.")

    comision_ypri = round(total_pagar * porcentaje_comision, 2)
    retencion_fuente = round(total_pagar * retencion_pct, 2)
    pago_neto_prestador = round(total_pagar - comision_ypri - retencion_fuente, 2)

    return {
        "total_facturado": total_pagar,
        "porcentaje_comision": porcentaje_comision,
        "comision_ypri": comision_ypri,
        "porcentaje_retencion": retencion_pct,
        "retencion_fuente": retencion_fuente,
        "pago_neto_prestador": pago_neto_prestador,
    }


def calcular_promedio_calificacion(rating_previo: float, num_evaluaciones: int, nueva_puntuacion: float) -> float:
    """
    [GUÍA 10 - ACTIVIDAD 2 - FUNCIÓN 3]
    Recalcula dinámicamente el promedio ponderado de calificación de un servicio o prestador.
    
    Parámetros:
        rating_previo (float): Promedio acumulado previo (1.0 a 5.0).
        num_evaluaciones (int): Total de evaluaciones incluyendo la nueva.
        nueva_puntuacion (float): Puntuación ingresada por el cliente (1.0 a 5.0).
        
    Retorna:
        float: Nuevo promedio ponderado redondeado a 1 decimal.
    """
    if not (1.0 <= nueva_puntuacion <= 5.0):
        raise ValueError("La puntuación debe estar comprendida entre 1.0 y 5.0.")

    if num_evaluaciones <= 1:
        return round(nueva_puntuacion, 1)

    # Fórmula de actualización continua de la media aritmética
    total_previo = rating_previo * (num_evaluaciones - 1)
    nuevo_promedio = (total_previo + nueva_puntuacion) / num_evaluaciones
    return round(nuevo_promedio, 1)


def calcular_metricas_prestador(prestador_id: str, lista_contratos: list, lista_calificaciones: list) -> dict:
    """
    [GUÍA 10 - ACTIVIDAD 2 - FUNCIÓN 4]
    Procesa las colecciones de contratos y calificaciones para consolidar el rendimiento de un prestador.
    
    Parámetros:
        prestador_id (str): Identificador único del prestador.
        lista_contratos (list): Lista global de contratos de la plataforma.
        lista_calificaciones (list): Lista global de reseñas y puntuaciones.
        
    Retorna:
        dict: Métricas cuantitativas (total, completados, tasa de éxito, ingresos brutos y netos).
    """
    contratos_prestador = [c for c in lista_contratos if c.get("prestador_id") == prestador_id]
    total_contratos = len(contratos_prestador)

    completados = [c for c in contratos_prestador if c.get("estado") == "Completado"]
    total_completados = len(completados)

    tasa_cumplimiento = (total_completados / total_contratos * 100.0) if total_contratos > 0 else 0.0
    ingresos_brutos = sum(c.get("total", 0.0) for c in completados)

    # Comisión y neto estimado mediante la función 2
    liquidacion_comision = calcular_comision_plataforma(ingresos_brutos) if ingresos_brutos > 0 else {
        "comision_ypri": 0.0,
        "retencion_fuente": 0.0,
        "pago_neto_prestador": 0.0
    }

    # Calificaciones recibidas
    califs = [c.get("puntuacion", 0.0) for c in lista_calificaciones if c.get("prestador_id") == prestador_id]
    rating_promedio = round(sum(califs) / len(califs), 1) if califs else 5.0

    return {
        "prestador_id": prestador_id,
        "total_contratos": total_contratos,
        "contratos_completados": total_completados,
        "tasa_cumplimiento_pct": round(tasa_cumplimiento, 1),
        "ingresos_brutos": ingresos_brutos,
        "comision_retenida": liquidacion_comision["comision_ypri"],
        "ingresos_netos": liquidacion_comision["pago_neto_prestador"],
        "total_calificaciones": len(califs),
        "rating_promedio": rating_promedio,
    }


def calcular_resumen_estadistico(valores: list) -> dict:
    """
    [GUÍA 10 - ACTIVIDAD 2 - FUNCIÓN 5]
    Calcula parámetros estadísticos descriptivos sobre un vector numérico recibido.
    
    Parámetros:
        valores (list): Lista de valores numéricos (int o float).
        
    Retorna:
        dict: Diccionario con total de elementos, suma, promedio, mínimo y máximo.
    """
    if not valores:
        return {"cantidad": 0, "suma": 0.0, "promedio": 0.0, "minimo": 0.0, "maximo": 0.0}

    suma = sum(valores)
    cantidad = len(valores)
    return {
        "cantidad": cantidad,
        "suma": round(suma, 2),
        "promedio": round(suma / cantidad, 2),
        "minimo": min(valores),
        "maximo": max(valores),
    }


# ========================================================================================
# ACTIVIDAD 3. IMPLEMENTACIÓN DE PROCEDIMIENTOS (INTERACCIÓN SIN RETURN)
# Subalgoritmos dedicados a la visualización, impresión y formateo de resultados al usuario.
# ========================================================================================

def mostrar_recibo_liquidacion(datos_liquidacion: dict, servicio: dict = None):
    """
    [GUÍA 10 - ACTIVIDAD 3 - PROCEDIMIENTO 1]
    Muestra en consola el recibo formal de cotización y liquidación financiera.
    No devuelve ningún resultado con 'return'; su única responsabilidad es interactuar con el usuario.
    """
    separador("=")
    print("                 RECIBO DE COTIZACIÓN Y LIQUIDACIÓN — YPRI")
    separador("=")
    if servicio:
        print(f"  Código Servicio:   {servicio.get('codigo', 'N/A')}")
        print(f"  Categoría:         {servicio.get('categoria', 'N/A')}")
        print(f"  Prestador:         {servicio.get('prestador_nombre', 'N/A')}")
        print(f"  Ciudad:            {servicio.get('ciudad', 'N/A')}")
        separador("-")

    print(f"  Tarifa por hora:   {formatear_cop_lambda(datos_liquidacion['tarifa_hora'])}")
    print(f"  Horas contratadas: {datos_liquidacion['horas']} hora(s)")
    print(f"  Subtotal Bruto:    {formatear_cop_lambda(datos_liquidacion['subtotal_bruto'])}")

    if datos_liquidacion["descuento_pct"] > 0:
        print(f"  Descuento ({datos_liquidacion['descuento_pct']}%):  - {formatear_cop_lambda(datos_liquidacion['monto_descuento'])}")
        print(f"  Subtotal Neto:     {formatear_cop_lambda(datos_liquidacion['subtotal_neto'])}")

    print(f"  IVA ({int(datos_liquidacion['tasa_iva'] * 100)}%):        + {formatear_cop_lambda(datos_liquidacion['monto_iva'])}")
    separador("-")
    print(f"  TOTAL A PAGAR:     {formatear_cop_lambda(datos_liquidacion['total_pagar'])}")
    separador("=")


def mostrar_ficha_tecnica_servicio(servicio: dict):
    """
    [GUÍA 10 - ACTIVIDAD 3 - PROCEDIMIENTO 2]
    Presenta de manera organizada y tabular la ficha técnica de un servicio seleccionado.
    Procedimiento puro de presentación (sin return).
    """
    separador("-")
    print(f"  [FICHA TÉCNICA] {servicio.get('codigo', 'N/A')} — {servicio.get('categoria', 'N/A')}")
    separador("-")
    print(f"  • Prestador:       {servicio.get('prestador_nombre', 'N/A')}")
    print(f"  • Ciudad:          {servicio.get('ciudad', 'N/A')}")
    print(f"  • Tarifa por hora: {formatear_cop_lambda(servicio.get('tarifa_hora', 0))}")
    print(f"  • Calificación:    ★ {servicio.get('calificacion', 5.0):.1f} / 5.0 ({servicio.get('num_contratos', 0)} servicios)")
    print(f"  • Disponibilidad:  {'Inmediata (Activo)' if servicio.get('disponible', True) else 'Ocupado / Inactivo'}")
    print(f"  • Experiencia:     {servicio.get('anios_experiencia', 1)} año(s)")
    print(f"  • Descripción:     {servicio.get('descripcion', 'Sin descripción.')}")
    separador("-")


def mostrar_tarjeta_rendimiento_prestador(prestador_nombre: str, metricas: dict):
    """
    [GUÍA 10 - ACTIVIDAD 3 - PROCEDIMIENTO 3]
    Imprime la tarjeta de rendimiento operativo de un profesional prestador.
    """
    separador("=")
    print(f"       PANEL DE RENDIMIENTO OPERATIVO — {prestador_nombre.upper()}")
    separador("=")
    print(f"  Contratos Totales:       {metricas.get('total_contratos', 0)}")
    print(f"  Contratos Completados:   {metricas.get('contratos_completados', 0)}")
    print(f"  Tasa de Cumplimiento:    {metricas.get('tasa_cumplimiento_pct', 0.0)}%")
    print(f"  Calificación Promedio:   ★ {metricas.get('rating_promedio', 5.0):.1f} / 5.0 ({metricas.get('total_calificaciones', 0)} reseñas)")
    separador("-")
    print(f"  Ingresos Brutos:         {formatear_cop_lambda(metricas.get('ingresos_brutos', 0.0))}")
    print(f"  Comisión Plataforma YPRI: - {formatear_cop_lambda(metricas.get('comision_retenida', 0.0))}")
    print(f"  Transferencia Neta:      {formatear_cop_lambda(metricas.get('ingresos_netos', 0.0))}")
    separador("=")


# ========================================================================================
# ACTIVIDAD 4. FUNCIONES LAMBDA DE ORDENAMIENTO
# ========================================================================================

def ordenar_servicios_por_tarifa(coleccion_servicios: list, descendente: bool = False) -> list:
    """
    [GUÍA 10 - ACTIVIDAD 4 - LAMBDA]
    Ordena una lista de servicios utilizando una función lambda como criterio de clave.
    """
    return sorted(coleccion_servicios, key=lambda s: s.get("tarifa_hora", 0.0), reverse=descendente)


def ordenar_servicios_por_rating(coleccion_servicios: list) -> list:
    """
    [GUÍA 10 - ACTIVIDAD 4 - LAMBDA]
    Ordena los servicios de mayor a menor calificación utilizando una función lambda.
    """
    return sorted(coleccion_servicios, key=lambda s: s.get("calificacion", 0.0), reverse=True)


def ordenar_contratos_por_total(coleccion_contratos: list) -> list:
    """
    [GUÍA 10 - ACTIVIDAD 4 - LAMBDA]
    Ordena los contratos por el valor total facturado de forma descendente.
    """
    return sorted(coleccion_contratos, key=lambda c: c.get("total", 0.0), reverse=True)


# ========================================================================================
# ACTIVIDAD 5. ANÁLISIS DE VARIABLES LOCALES, GLOBALES Y PASO DE ARGUMENTOS
# Comportamiento diferenciado entre tipos inmutables (valor) y tipos mutables (referencia).
# ========================================================================================

def modificar_numero_prueba(numero: float) -> float:
    """
    Demuestra que los números (int/float) son inmutables en Python.
    La reasignación dentro de la función solo cambia la variable local.
    """
    numero = numero + 10000.0  # Modificación en ámbito local
    return numero


def modificar_cadena_prueba(texto: str) -> str:
    """
    Demuestra que las cadenas (str) son inmutables.
    """
    texto = texto.upper() + " [MODIFICADO]"
    return texto


def agregar_elemento_lista_prueba(lista_mut: list, elemento) -> None:
    """
    Demuestra que las listas (list) son mutables.
    La modificación mediante métodos in-place (append, extend) afecta la lista original.
    """
    lista_mut.append(elemento)


def actualizar_campo_diccionario_prueba(diccionario_mut: dict, clave: str, valor) -> None:
    """
    Demuestra que los diccionarios (dict) son mutables.
    Modifica directamente la estructura de datos original referenciada.
    """
    diccionario_mut[clave] = valor


def demostrar_paso_argumentos():
    """
    [GUÍA 10 - ACTIVIDAD 5 - PROCEDIMIENTO DE DEMOSTRACIÓN]
    Ejecuta en consola una prueba didáctica con valores inmutables y mutables,
    imprimiendo los estados antes y después de la llamada.
    """
    mostrar_encabezado("DEMOSTRACIÓN: PASO DE ARGUMENTOS (VALOR VS REFERENCIA)")
    print()

    # 1. Objeto inmutable (número)
    tarifa_original = 45000.0
    print("1. OBJETO INMUTABLE (float):")
    print(f"   Valor antes de llamar la función:    {tarifa_original}")
    resultado_fn = modificar_numero_prueba(tarifa_original)
    print(f"   Resultado retornado por la función:  {resultado_fn}")
    print(f"   Valor original de la variable:       {tarifa_original}")
    print("   -> Conclusión: La variable original NO cambió (comportamiento por valor).\n")

    # 2. Objeto inmutable (cadena)
    ciudad_original = "Cúcuta"
    print("2. OBJETO INMUTABLE (str):")
    print(f"   Cadena antes de llamar la función:   '{ciudad_original}'")
    cadena_retornada = modificar_cadena_prueba(ciudad_original)
    print(f"   Resultado retornado:                 '{cadena_retornada}'")
    print(f"   Cadena original en el llamador:      '{ciudad_original}'")
    print("   -> Conclusión: La cadena original permanece inmutable.\n")

    # 3. Objeto mutable (lista)
    servicios_simulados = ["Electricidad", "Plomería"]
    print("3. OBJETO MUTABLE (list):")
    print(f"   Lista antes del procedimiento:       {servicios_simulados}")
    agregar_elemento_lista_prueba(servicios_simulados, "Climatización")
    print(f"   Lista después del procedimiento:     {servicios_simulados}")
    print("   -> Conclusión: La lista original SÍ cambió (comportamiento por referencia).\n")

    # 4. Objeto mutable (diccionario)
    usuario_demo = {"nombre": "Carlos", "rol": "cliente"}
    print("4. OBJETO MUTABLE (dict):")
    print(f"   Diccionario antes del procedimiento: {usuario_demo}")
    actualizar_campo_diccionario_prueba(usuario_demo, "rol", "prestador")
    print(f"   Diccionario después del procedim.:   {usuario_demo}")
    print("   -> Conclusión: El diccionario original se modificó en el mismo bloque de memoria.\n")
    separador()


# ========================================================================================
# MENÚ INTERACTIVO DE EXPLORACIÓN DE SUBALGORITMOS (GUÍA 10)
# ========================================================================================

def menu_subalgoritmos_interactivo():
    """
    Procedimiento interactivo que permite al docente o usuario explorar todas
    las actividades requeridas por la Guía de Aprendizaje N.º 10.
    """
    from data.database import servicios, contratos, calificaciones

    while True:
        mostrar_encabezado("EXPLORADOR DE SUBALGORITMOS — GUÍA 10")
        print()
        print("  1. Probar Funciones con return (Cotización, IVA y Comisión)")
        print("  2. Probar Procedimientos de visualización (Ficha y Recibo)")
        print("  3. Probar Funciones Lambda (Cálculos rápidos y ordenamiento)")
        print("  4. Ejecutar Demostración de Variables y Paso de Argumentos")
        print("  5. Ejecutar Ejercicio de Práctica Guiada (Inventario Guía 10)")
        print("  0. Volver al menú anterior")
        separador()

        opcion = input("  Seleccione una opción (0-5): ").strip()

        if opcion == "1":
            print("\n--- PRUEBA DE FUNCIONES CON RETURN ---")
            tarifa = 50000.0
            horas = 4
            descuento = 10.0
            print(f"  Entradas: Tarifa=${tarifa:,.0f}/h, Horas={horas}, Descuento={descuento}%")
            resultado = calcular_liquidacion_contrato(tarifa, horas, descuento_pct=descuento)
            print(f"  Resultado retornado (dict): {resultado}")
            comision = calcular_comision_plataforma(resultado["total_pagar"])
            print(f"  Comisión YPRI retornada:    {comision}")

        elif opcion == "2":
            print("\n--- PRUEBA DE PROCEDIMIENTOS (SIN RETURN) ---")
            if servicios:
                mostrar_ficha_tecnica_servicio(servicios[0])
                liq = calcular_liquidacion_contrato(servicios[0]["tarifa_hora"], 3)
                mostrar_recibo_liquidacion(liq, servicios[0])
            else:
                print("  [!] No hay servicios cargados.")

        elif opcion == "3":
            print("\n--- PRUEBA DE FUNCIONES LAMBDA ---")
            subtotal_ejemplo = 150000.0
            desc = calcular_descuento_lambda(subtotal_ejemplo, 15)
            iva = calcular_iva_lambda(subtotal_ejemplo - desc)
            print(f"  Base: {formatear_cop_lambda(subtotal_ejemplo)}")
            print(f"  Descuento 15% (lambda): {formatear_cop_lambda(desc)}")
            print(f"  IVA 19% (lambda):       {formatear_cop_lambda(iva)}")
            print("\n  Top 3 Servicios por Tarifa (ordenados con sorted + lambda):")
            ordenados = ordenar_servicios_por_tarifa(servicios, descendente=True)[:3]
            for s in ordenados:
                print(f"    • {s['codigo']} | {s['categoria']:15} | {formatear_cop_lambda(s['tarifa_hora'])}/h")

        elif opcion == "4":
            demostrar_paso_argumentos()

        elif opcion == "5":
            from ejercicio_practico_guia10 import iniciar_programa as iniciar_inventario
            print("\nIniciando Sistema de Inventario Guiado de la Guía 10...\n")
            iniciar_inventario()

        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida. Ingrese un valor entre 0 y 5.")

        input("\nPresione Enter para continuar...")
        print()
