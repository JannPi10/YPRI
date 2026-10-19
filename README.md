# 🛠️ YPRI — Plataforma de Servicios a Domicilio

**YPRI** es una plataforma digital desarrollada para conectar clientes con prestadores independientes de servicios técnicos y del hogar (electricistas, plomeros, cerrajeros, técnicos de climatización y personal de limpieza) en ciudades colombianas como Cúcuta, Cali, Bogotá, Medellín y Bucaramanga.

El proyecto aborda la problemática de la informalidad laboral, la desconfianza y la falta de transparencia en precios mediante un sistema estructurado de registro, cotización con cálculo de impuestos (IVA), gestión de contratos, valoración basada en calificaciones por estrellas, ordenamiento y búsqueda de vectores, y una interfaz gráfica interactiva moderna.

---

## 👥 Integrantes y Datos del Proyecto

* **Desarrolladores:**
  * Jann Pierre Ortiz Zambrano
  * Josué David Rincón Palomino
* **Institución:** Fundación de Estudios Superiores Comfanorte (FESC)
* **Programa:** Ingeniería de Software (Octavo Semestre) — 2026
* **Asignatura:** Diseño Funcional / Estructuras de Datos
* **Repositorio Oficial:** [https://github.com/JannPi10/YPRI.git](https://github.com/JannPi10/YPRI.git)

---

## 🏗️ Arquitectura Modular del Software

El sistema está construido bajo una arquitectura modular limpia y desacoplada en Python:

```text
YPRI/
├── core/                   # Núcleo del sistema
│   ├── constantes.py       # Tuplas inmutables (roles, categorías, estados, ciudades)
│   └── validaciones.py     # Sistema de validaciones defensivas por teclado
├── data/                   # Capa de datos y persistencia en memoria (Vectores)
│   └── database.py         # Vectores unidimensionales de diccionarios y sesión activa
├── modules/                # Módulos de lógica de negocio
│   ├── auth.py             # Autenticación, registro y control de sesión
│   ├── servicios.py        # Catálogo, ordenamiento asc/desc, búsqueda y reto (Guía 8)
│   ├── contratos.py        # Cotización con IVA (19%), solicitud y ciclo de vida de contratos
│   ├── calificaciones.py   # Reseñas, puntuación y recálculo dinámico de promedios
│   └── admin.py            # Panel administrativo, métricas y auditoría de usuarios
├── app_gui.py              # 🎨 Interfaz Gráfica Moderna (GUI) con Tkinter/TTK
├── main.py                 # Punto de entrada modular (Soporta Consola y GUI)
└── README.md               # Documentación general del proyecto
```

---

## 🚀 Requisitos y Ejecución

* **Lenguaje:** Python 3.8 o superior (sin dependencias externas requeridas).

### 1. Ejecución de la Interfaz Gráfica Moderna (GUI):
```bash
python app_gui.py
```
*O mediante el argumento de línea de comandos:*
```bash
python main.py --gui
```

### 2. Ejecución del Modo Consola Tradicional (CLI):
```bash
python main.py
```

---

## 🧩 Estructuras de Datos y Guías Académicas Aplicadas

* **Guía 8 — Vectores en Python (Almacenamiento, Ordenamiento y Búsqueda):**
  * **Estructura unidimensional:** Vectores de registros `servicios[]`, `usuarios[]`, `contratos[]`, `calificaciones[]` implementados como listas de diccionarios indexadas.
  * **Almacenamiento:** Crecimiento dinámico con `.append()` y dimensionamiento con `len()`.
  * **Recorrido:** Ciclos `for` secuenciales con control de colecciones vacías.
  * **Ordenamiento Ascendente (Act. 4):** Ordenamiento por precio de menor a mayor mediante `sorted(servicios, key=lambda s: s["tarifa_hora"])`.
  * **Ordenamiento Descendente (Act. 5):** Ordenamiento por precio de mayor a menor y por calificación mediante `sorted(..., reverse=True)`.
  * **Búsqueda Secuencial por Identificador (Act. 6):** Localización exacta de registros mediante su código único (`SERV-XX`, `CONTR-XX`, correo).
  * **Búsqueda por Atributos (Act. 7):** Búsqueda con múltiples coincidencias por categoría, ciudad o texto descriptivo.
  * **Reto de Integración (Act. 13):** Procesamiento estadístico del vector extrayendo el valor mínimo (`min`), máximo (`max`), tarifa promedio y ranking del Top 3 de servicios más contratados.
* **Guía 7 — Tuplas, Cadenas y Diccionarios:**
  * **Tuplas inmutables:** `ROLES_SISTEMA`, `CATEGORIAS_SERVICIO`, `ESTADOS_CONTRATO`, `CIUDADES_COBERTURA`.
  * **Diccionarios mutables:** Cada registro almacena pares `clave: valor`.
  * **Normalización de cadenas:** Métodos `.strip()`, `.lower()`, `.upper()`, `.title()` y `.capitalize()`.
* **Guías 5 y 6 — Ciclos y Validaciones:**
  * Ciclos `while` con `break` para menús interactivos y bucles de validación defensiva.
  * Instrucción `continue` para saltos condicionales en filtrado.

---

## 🔑 Credenciales de Prueba Precargadas

| Rol | Correo Electrónico | Contraseña | Ciudad |
|---|---|---|---|
| **Cliente** | `juan.perez@email.com` | `juan123` | Cúcuta |
| **Prestador** | `carlos.gomez@email.com` | `carlos456` | Cúcuta |
| **Administrador** | `admin@ypri.com` | `admin2026` | Cúcuta |

*(En la interfaz gráfica `app_gui.py`, puedes alternar entre estos perfiles al instante con un solo clic usando el botón "🔄 Cambiar Usuario").*
