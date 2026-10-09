# 📐 Arquitectura y Especificación Técnica — YPRI

Este documento detalla la arquitectura del sistema **YPRI** y la correspondencia entre los módulos implementados y los Requerimientos Funcionales (RF).

---

## 🎯 Requerimientos Funcionales Implementados

### 1. RF-01: Gestión y Publicación de Servicios
* **Módulo:** `modules/servicios.py`
* **Descripción:** Permite a los prestadores de servicios crear, consultar y modificar sus ofertas técnicas.
* **Estructuras aplicadas:**
  * Diccionarios (`dict`) para representar cada servicio.
  * Tuplas (`tuple`) para validar categorías (`CATEGORIAS_SERVICIO`) y ciudades (`CIUDADES_COBERTURA`).
  * Validación de rango de tarifa por hora.

### 2. RF-02: Búsqueda, Cotización y Contratación
* **Módulo:** `modules/contratos.py`
* **Descripción:** Los clientes exploran el catálogo, aplican filtros de disponibilidad o categoría, calculan el costo total estimado (incluyendo el 19% de IVA) y formalizan un acuerdo de servicio.
* **Estructuras aplicadas:**
  * Listas de diccionarios con recorrido `for` y saltos condicionales `continue`.
  * Tupla `ESTADOS_CONTRATO` para inicializar el estado en `"Pendiente"`.
  * Cálculo aritmético del subtotal, IVA y valor total facturado.

### 3. RF-03: Seguimiento de Contratos y Reputación
* **Módulo:** `modules/calificaciones.py`
* **Descripción:** Control del ciclo de vida del contrato (Pendiente → En proceso → Completado / Cancelado) y calificación por estrellas (1.0 a 5.0) con recálculo dinámico de la reputación promedio del prestador.
* **Estructuras aplicadas:**
  * Control de unicidad de calificación por contrato.
  * Recálculo matemático del promedio ponderado en el catálogo.

---

## 🔐 Seguridad y Validaciones Defensivas

* **Módulo:** `core/validaciones.py`
* Todas las entradas por teclado cuentan con validación en bucle `while` para evitar excepciones por valores vacíos, tipos incompatibles o entradas no esperadas.
