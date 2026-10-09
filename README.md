# 🛠️ YPRI — Plataforma de Servicios a Domicilio

**YPRI** es una plataforma digital desarrollada para conectar clientes con prestadores independientes de servicios técnicos y del hogar (electricistas, plomeros, cerrajeros, técnicos de climatización y personal de limpieza) en ciudades colombianas como Cúcuta, Cali, Bogotá, Medellín y Bucaramanga.

El proyecto aborda la problemática de la informalidad laboral, la desconfianza y la falta de transparencia en precios mediante un sistema estructurado de registro, cotización con cálculo de impuestos (IVA), gestión de contratos y valoración basada en calificaciones por estrellas.

---

## 👥 Integrantes y Datos del Proyecto

* **Desarrolladores:**
  * Jann Pierre Ortiz Zambrano
  * Josué David Rincón Palomino
* **Institución:** Fundación de Estudios Superiores Comfanorte (FESC)
* **Programa:** Ingeniería de Software (Octavo Semestre) — 2026
* **Asignatura:** Diseño Funcional / Estructuras de Datos

---

## 🏗️ Arquitectura Modular del Software

El sistema ha sido diseñado bajo una arquitectura modular limpia en Python, separando responsabilidades en capas lógicas:

```text
YPRI/
├── core/                   # Núcleo del sistema
│   ├── constantes.py       # Tuplas inmutables (roles, categorías, estados, ciudades)
│   └── validaciones.py     # Sistema de validaciones defensivas por teclado
├── data/                   # Capa de datos y persistencia en memoria
│   └── database.py         # Colecciones en listas de diccionarios y gestión de sesión
├── modules/                # Módulos de funcionalidad del negocio
│   ├── auth.py             # Autenticación, registro y control de sesión
│   ├── servicios.py        # Catálogo, publicación, detalle y edición de servicios
│   ├── contratos.py        # Cotización con IVA, solicitud y actualización de estados
│   ├── calificaciones.py   # Reseñas, puntuación y recálculo de promedio del prestador
│   └── admin.py            # Panel administrativo, métricas y auditoría de usuarios
├── main.py                 # Punto de entrada principal con menús interactivos por rol
├── ypri_sistema.py         # Versión unificada ejecutable para entregas académicas
└── README.md               # Documentación general del proyecto
```

---

## 🚀 Requisitos y Ejecución

* **Lenguaje:** Python 3.8 o superior (sin dependencias externas requeridas).

### Ejecución de la aplicación modular:
```bash
python main.py
```

### Ejecución del script unificado:
```bash
python ypri_sistema.py
```

---

## 🔑 Credenciales de Prueba Precargadas

| Rol | Correo Electrónico | Contraseña | Ciudad |
|---|---|---|---|
| **Cliente** | `juan.perez@email.com` | `juan123` | Cúcuta |
| **Prestador** | `carlos.gomez@email.com` | `carlos456` | Cúcuta |
| **Administrador** | `admin@ypri.com` | `admin2026` | Cúcuta |

También es posible registrar nuevos usuarios de tipo cliente o prestador directamente desde el menú principal.

---

## 🧩 Estructuras de Datos Empleadas

* **Tuplas (`tuple`):** Modelan datos inmutables y fijos que no deben alterarse en tiempo de ejecución (`ROLES_SISTEMA`, `CATEGORIAS_SERVICIO`, `ESTADOS_CONTRATO`, `CIUDADES_COBERTURA`).
* **Diccionarios (`dict`):** Representan cada entidad del dominio (`Usuario`, `Servicio`, `Contrato`, `Calificación`) mediante pares `clave: valor`.
* **Listas (`list`):** Almacenan colecciones dinámicas de diccionarios (`usuarios[]`, `servicios[]`, `contratos[]`, `calificaciones[]`) gestionadas mediante `.append()`, `len()` e indexación.
* **Cadenas (`str`):** Normalización de entradas mediante métodos como `.strip()`, `.lower()`, `.upper()` y `.title()`.
* **Ciclos y Control de Flujo:** Ciclos `while` interactivos con `break` para control de menús y validaciones repetitivas, y ciclos `for` con `continue` para filtrado y procesamiento de colecciones.
