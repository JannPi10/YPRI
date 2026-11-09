# YPRI - Plataforma de Servicios a Domicilio
### Sistema de Gestion, Facturacion y Analisis Matricial

YPRI es una plataforma orientada a conectar clientes con profesionales independientes de servicios tecnicos y para el hogar (electricidad, plomeria, cerrajeria, climatizacion y limpieza) en Colombia.

El proyecto cuenta con una arquitectura organizada en modulos independientes para el backend en Python, el frontend web/movil en Next.js y los documentos academicos de entrega.

---

## Estructura del Proyecto Organizada por Carpetas

```text
semana-09/
├── backend/                        # Codigo fuente en Python (CLI y GUI de Escritorio)
│   ├── core/                       # Reglas, tuplas y validaciones defensivas
│   │   ├── constantes.py           # Tuplas inmutables (roles, categorias, ciudades, dias)
│   │   └── validaciones.py         # Control defensivo de entradas, excepciones y rangos
│   ├── data/                       # Base de datos y persistencia en memoria
│   │   └── database.py             # Vectores unidimensionales y matrices bidimensionales
│   ├── modules/                    # Modulos de negocio
│   │   ├── matrices.py             # Creacion, recorrido, calculos matematicos y matrices especiales
│   │   ├── admin.py                # Auditoria, metricas operativas y consolidado matricial
│   │   ├── auth.py                 # Autenticacion, control de roles y registro de usuarios
│   │   ├── servicios.py            # Catalogo, ordenamiento y busquedas
│   │   ├── contratos.py            # Cotizacion con IVA (19%) y gestion de acuerdos
│   │   └── calificaciones.py       # Puntuaciones y recalculo dinamico de promedios
│   ├── app_gui.py                  # Interfaz grafica de escritorio con Tkinter / TTK
│   └── main.py                     # Menu interactivo por consola (CLI)
├── web/                            # Frontend Web y Movil (Next.js 14 + Tailwind CSS)
│   ├── app/                        # App Router (layout, page reactiva, globals.css)
│   ├── lib/                        # Modelos de datos, inicializacion y funciones matematicas
│   ├── package.json                # Dependencias y scripts web
│   └── next.config.js              # Configuracion de compilacion y despliegue
├── documents/                      # Documentacion academica formal y guias
│   ├── ENTREGA_GUIA_9_YPRI.docx    # Informe institucional formal de la FESC
│   ├── generar_documento_entrega.py# Script generador del informe en Word (.docx)
│   └── GUÍA DE APRENDIZAJE N.º 9...# Guia oficial de aprendizaje en PDF
├── package.json                    # Scripts raiz para ejecucion directa del frontend
├── vercel.json                     # Configuracion de despliegue automatico en Vercel
├── .gitignore                      # Reglas de exclusion de dependencias y temporales
└── README.md                       # Documentacion tecnica general del repositorio
```

---

## Modulos y Temas Desarrollados

### 1. Backend (Python): Matrices y Analisis Multidimensional
* **Matriz de Ventas Semanales (5x6):** 5 categorias de servicio x 6 dias laborales (Lunes a Sabado).
* **Matriz de Cobertura por Ciudad (5x5):** Matriz cuadrada con 5 categorias x 5 ciudades.
* **Recorridos Anidados:** Ciclos `for` para tabulacion de filas y acumulacion vertical de columnas.
* **Operaciones Matematicas:** Suma de filas (total por categoria), suma de columnas (total por dia/ciudad), total general y promedio por registro.
* **Matrices Especiales:** Validacion de matriz cuadrada, matriz nula inicializada en ceros y matriz identidad unitaria.
* **Sincronizacion:** Los contratos completados acreditan ingresos en tiempo real a la matriz de facturacion.

### 2. Frontend Web y Movil (Next.js): Experiencia de Usuario Profesional
* **Catalogo de Servicios:** Busqueda reactiva, filtros por categoria y ciudad, ordenamiento ascendente y descendente por tarifa o calificacion.
* **Cotizador en Tiempo Real:** Calculo de subtotal segun horas estimadas y liquidacion del 19% de IVA.
* **Facturacion y Metricas:** Tabla matricial interactiva donde cualquier celda se puede editar haciendo clic para recalcular totales y promedios en vivo.
* **Simulador Movil:** Opcion para alternar entre la vista web completa y un marco de telefono inteligente (smartphone frame) ideal para demostraciones en dispositivos moviles.
* **Gestion de Usuarios:** Selector de perfiles (Cliente, Prestador, Administrador) y modal de registro de nuevos usuarios totalmente funcional.

---

## Instrucciones de Ejecucion

### 1. Ejecucion de la Plataforma Web (Vercel / Local)
Desde la raiz del proyecto:
```bash
npm run dev
```
O directamente desde la carpeta `web`:
```bash
cd web
npm run dev
```
Abre en tu navegador: [http://localhost:3000](http://localhost:3000)

Para compilar para produccion:
```bash
npm run build
```

#### Despliegue en Vercel
El repositorio cuenta con `vercel.json` configurado en la raiz. Al importar el proyecto en Vercel, la plataforma detecta la carpeta `web` y compila automaticamente.

---

### 2. Ejecucion del Backend en Python (Desktop GUI / CLI)

#### Interfaz Grafica de Escritorio (Tkinter):
```bash
cd backend
python app_gui.py
```
O desde la raiz:
```bash
python backend/app_gui.py
```

#### Modo Consola Tradicional (CLI):
```bash
cd backend
python main.py
```
O desde la raiz:
```bash
python backend/main.py
```

---

### 3. Documentos Academicos
El informe formal listo para entrega institucional se encuentra en:
`documents/ENTREGA_GUIA_9_YPRI.docx`

Para regenerarlo en cualquier momento:
```bash
python documents/generar_documento_entrega.py
```

---

## Usuarios de Prueba Precargados

| Rol | Correo Electronico | Contrasena | Ciudad |
|---|---|---|---|
| **Cliente** | juan.perez@email.com | juan123 | Cucuta |
| **Prestador** | carlos.gomez@email.com | carlos456 | Cucuta |
| **Administrador** | admin@ypri.com | admin2026 | Cucuta |
