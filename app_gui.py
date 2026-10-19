"""
========================================================================================
SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
Modulo: Interfaz Grafica de Usuario (GUI Moderna con Tkinter y TTK)
========================================================================================
Asignatura: Diseño Funcional | Unidad 2: Estructuras de Datos
Integrantes: Jann Pierre Ortiz Zambrano y Josue David Rincon Palomino
Institucion: Fundacion de Estudios Superiores Comfanorte (FESC) - 2026
========================================================================================
GUIA 8 - VECTORES EN PYTHON:
- Visualizacion reactiva del vector de servicios
- Ordenamiento interactivo ascendente y descendente (sorted + key lambda)
- Busqueda reactiva por identificador y por multiples atributos
- Cotizador de contratos con calculo de IVA (19%) en tiempo real
- Sistema de calificaciones y metricas analiticas del vector
========================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Importacion de la arquitectura modular de YPRI
from core.constantes import (
    ROLES_SISTEMA,
    CATEGORIAS_SERVICIO,
    ESTADOS_CONTRATO,
    CIUDADES_COBERTURA,
    IVA_PORCENTAJE,
)
from data.database import (
    usuarios,
    servicios,
    contratos,
    calificaciones,
    get_sesion_actual,
    set_sesion_actual,
    limpiar_sesion,
)
from modules.servicios import (
    ordenar_servicios_ascendente,
    ordenar_servicios_descendente,
)


class YpriApp(tk.Tk):
    """Aplicacion principal con interfaz grafica moderna para YPRI."""

    def __init__(self):
        super().__init__()
        self.title("YPRI — Plataforma de Servicios a Domicilio")
        self.geometry("1100x720")
        self.minsize(980, 640)
        self.configure(bg="#F1F5F9")

        # Iniciar con usuario cliente precargado para comodidad
        if not get_sesion_actual():
            set_sesion_actual(usuarios[0])  # Juan Perez (Cliente)

        self._configurar_estilos()
        self._construir_layout_principal()
        self.mostrar_vista("catalogo")

    # ====================================================================================
    # ESTILOS VISUALES MODERNOS
    # ====================================================================================

    def _configurar_estilos(self):
        """Configura la paleta de colores, fuentes y estilos TTK modernos."""
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Colores del sistema
        self.c_bg = "#F1F5F9"           # Slate 100
        self.c_sidebar = "#0F172A"      # Slate 900
        self.c_sidebar_hover = "#1E293B"# Slate 800
        self.c_sidebar_text = "#F8FAFC"
        self.c_primary = "#2563EB"      # Blue 600
        self.c_primary_hover = "#1D4ED8"
        self.c_card = "#FFFFFF"
        self.c_border = "#E2E8F0"
        self.c_text = "#0F172A"
        self.c_muted = "#64748B"
        self.c_success = "#059669"
        self.c_warning = "#D97706"

        fuente_base = ("Segoe UI", 10)
        fuente_negrita = ("Segoe UI", 10, "bold")
        fuente_titulo = ("Segoe UI", 16, "bold")

        # Treeview (Tablas)
        self.style.configure(
            "Ypri.Treeview",
            background="#FFFFFF",
            foreground="#0F172A",
            rowheight=30,
            fieldbackground="#FFFFFF",
            font=fuente_base,
            borderwidth=0,
        )
        self.style.configure(
            "Ypri.Treeview.Heading",
            background="#E2E8F0",
            foreground="#0F172A",
            font=fuente_negrita,
            padding=6,
        )
        self.style.map("Ypri.Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", "#1E3A8A")])

        # Boton Primario
        self.style.configure(
            "Primary.TButton",
            background=self.c_primary,
            foreground="#FFFFFF",
            font=fuente_negrita,
            padding=(12, 8),
            borderwidth=0,
        )
        self.style.map("Primary.TButton", background=[("active", self.c_primary_hover)])

        # Boton Secundario
        self.style.configure(
            "Secondary.TButton",
            background="#E2E8F0",
            foreground="#1E293B",
            font=fuente_base,
            padding=(10, 6),
            borderwidth=0,
        )

    # ====================================================================================
    # LAYOUT PRINCIPAL (SIDEBAR + CONTENIDO)
    # ====================================================================================

    def _construir_layout_principal(self):
        """Construye el sidebar lateral y el contenedor de vistas dinamicas."""
        # Contenedor raiz
        self.main_container = tk.Frame(self, bg=self.c_bg)
        self.main_container.pack(fill="both", expand=True)

        # ----------------- SIDEBAR LATERAL -----------------
        self.sidebar = tk.Frame(self.main_container, bg=self.c_sidebar, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Header de la marca en Sidebar
        brand_frame = tk.Frame(self.sidebar, bg=self.c_sidebar, padx=16, pady=20)
        brand_frame.pack(fill="x")

        lbl_logo = tk.Label(
            brand_frame,
            text="🛠️ YPRI",
            font=("Segoe UI", 20, "bold"),
            bg=self.c_sidebar,
            fg="#60A5FA"
        )
        lbl_logo.pack(anchor="w")

        lbl_sub = tk.Label(
            brand_frame,
            text="Servicios a Domicilio",
            font=("Segoe UI", 9),
            bg=self.c_sidebar,
            fg="#94A3B8"
        )
        lbl_sub.pack(anchor="w")

        # Tarjeta de usuario en sesion
        self.user_card = tk.Frame(self.sidebar, bg=self.c_sidebar_hover, padx=12, pady=12)
        self.user_card.pack(fill="x", padx=12, pady=(0, 16))

        self.lbl_user_name = tk.Label(
            self.user_card,
            text="Usuario",
            font=("Segoe UI", 11, "bold"),
            bg=self.c_sidebar_hover,
            fg="#FFFFFF"
        )
        self.lbl_user_name.pack(anchor="w")

        self.lbl_user_role = tk.Label(
            self.user_card,
            text="Rol: Cliente",
            font=("Segoe UI", 9),
            bg=self.c_sidebar_hover,
            fg="#38BDF8"
        )
        self.lbl_user_role.pack(anchor="w")

        # Botones de Navegacion
        self.nav_buttons = {}
        items_nav = [
            ("catalogo", "🔍 Catálogo & Búsqueda", self._abrir_catalogo),
            ("solicitar", "📝 Solicitar Servicio", self._abrir_solicitar),
            ("contratos", "📋 Mis Contratos", self._abrir_contratos),
            ("publicar", "➕ Publicar Servicio", self._abrir_publicar),
            ("reto", "📊 Análisis de Vectores", self._abrir_reto),
            ("admin", "🛡️ Panel Administrador", self._abrir_admin),
        ]

        self.nav_frame = tk.Frame(self.sidebar, bg=self.c_sidebar)
        self.nav_frame.pack(fill="x", padx=8)

        for key, texto, comando in items_nav:
            btn = tk.Button(
                self.nav_frame,
                text=texto,
                font=("Segoe UI", 10),
                bg=self.c_sidebar,
                fg="#E2E8F0",
                activebackground=self.c_primary,
                activeforeground="#FFFFFF",
                bd=0,
                padx=14,
                pady=10,
                anchor="w",
                cursor="hand2",
                command=comando,
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        # Espaciador inferior
        tk.Label(self.sidebar, bg=self.c_sidebar).pack(expand=True, fill="both")

        # Acciones de pie de sidebar (Cambiar Usuario / Salir)
        footer_frame = tk.Frame(self.sidebar, bg=self.c_sidebar, padx=12, pady=16)
        footer_frame.pack(fill="x")

        btn_switch = tk.Button(
            footer_frame,
            text="🔄 Cambiar Usuario",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            bd=0,
            pady=6,
            cursor="hand2",
            command=self._dialogo_cambiar_usuario,
        )
        btn_switch.pack(fill="x", pady=2)

        # ----------------- CONTENEDOR DE VISTAS DINAMICAS -----------------
        self.content_area = tk.Frame(self.main_container, bg=self.c_bg, padx=24, pady=20)
        self.content_area.pack(side="right", fill="both", expand=True)

        self._actualizar_info_usuario()

    def _actualizar_info_usuario(self):
        """Refresca la tarjeta de usuario en el sidebar y ajusta permisos visibles."""
        u = get_sesion_actual()
        if u:
            self.lbl_user_name.config(text=u["nombre"])
            rol_txt = f"Rol: {u['rol'].capitalize()} • {u['ciudad']}"
            self.lbl_user_role.config(text=rol_txt)
        else:
            self.lbl_user_name.config(text="Sin Sesión")
            self.lbl_user_role.config(text="Invitado")

    def mostrar_vista(self, clave):
        """Limpia el area de contenido y monta la vista seleccionada."""
        for k, btn in self.nav_buttons.items():
            if k == clave:
                btn.config(bg=self.c_primary, fg="#FFFFFF")
            else:
                btn.config(bg=self.c_sidebar, fg="#E2E8F0")

        # Limpiar contenedor
        for widget in self.content_area.winfo_children():
            widget.destroy()

        self._actualizar_info_usuario()

        if clave == "catalogo":
            self._vista_catalogo()
        elif clave == "solicitar":
            self._vista_solicitar()
        elif clave == "contratos":
            self._vista_contratos()
        elif clave == "publicar":
            self._vista_publicar()
        elif clave == "reto":
            self._vista_reto_vectores()
        elif clave == "admin":
            self._vista_admin()

    # Callbacks de navegacion
    def _abrir_catalogo(self): self.mostrar_vista("catalogo")
    def _abrir_solicitar(self): self.mostrar_vista("solicitar")
    def _abrir_contratos(self): self.mostrar_vista("contratos")
    def _abrir_publicar(self): self.mostrar_vista("publicar")
    def _abrir_reto(self): self.mostrar_vista("reto")
    def _abrir_admin(self): self.mostrar_vista("admin")

    # ====================================================================================
    # VISTA 1: CATALOGO, BUSQUEDA Y ORDENAMIENTO (GUIA 8)
    # ====================================================================================

    def _vista_catalogo(self):
        """
        GUIA 8 - ACTIVIDADES 3, 4, 5, 6, 7, 8:
        Vista con busqueda reactiva y ordenamientos ascendente y descendente sobre el vector.
        """
        # Encabezado
        header = tk.Frame(self.content_area, bg=self.c_bg)
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="Catálogo de Servicios Profesionales",
            font=("Segoe UI", 18, "bold"),
            bg=self.c_bg,
            fg=self.c_text
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Guía 8: Búsqueda secuencial y ordenamiento de vectores en tiempo real",
            font=("Segoe UI", 9),
            bg=self.c_bg,
            fg=self.c_muted
        ).pack(anchor="w")

        # Tarjeta de Controles y Filtros (Card)
        card_filtros = tk.Frame(self.content_area, bg=self.c_card, padx=16, pady=12, bd=1, relief="solid")
        card_filtros.pack(fill="x", pady=(0, 12))

        # Fila 1: Buscador de texto y Combos
        fila1 = tk.Frame(card_filtros, bg=self.c_card)
        fila1.pack(fill="x", pady=4)

        tk.Label(fila1, text="Buscar:", font=("Segoe UI", 9, "bold"), bg=self.c_card).pack(side="left", padx=(0, 6))
        self.ent_buscar = ttk.Entry(fila1, width=28)
        self.ent_buscar.pack(side="left", padx=(0, 16))
        self.ent_buscar.bind("<KeyRelease>", lambda e: self._filtrar_y_ordenar_catalogo())

        tk.Label(fila1, text="Categoría:", font=("Segoe UI", 9), bg=self.c_card).pack(side="left", padx=(0, 6))
        self.combo_cat = ttk.Combobox(fila1, values=["Todas"] + list(CATEGORIAS_SERVICIO), state="readonly", width=14)
        self.combo_cat.set("Todas")
        self.combo_cat.pack(side="left", padx=(0, 16))
        self.combo_cat.bind("<<ComboboxSelected>>", lambda e: self._filtrar_y_ordenar_catalogo())

        tk.Label(fila1, text="Ciudad:", font=("Segoe UI", 9), bg=self.c_card).pack(side="left", padx=(0, 6))
        self.combo_ciudad = ttk.Combobox(fila1, values=["Todas"] + list(CIUDADES_COBERTURA), state="readonly", width=14)
        self.combo_ciudad.set("Todas")
        self.combo_ciudad.pack(side="left", padx=(0, 16))
        self.combo_ciudad.bind("<<ComboboxSelected>>", lambda e: self._filtrar_y_ordenar_catalogo())

        # Fila 2: Ordenamiento de Vectores (Guia 8)
        fila2 = tk.Frame(card_filtros, bg=self.c_card)
        fila2.pack(fill="x", pady=6)

        tk.Label(
            fila2,
            text="⚡ Ordenar Vector:",
            font=("Segoe UI", 9, "bold"),
            bg=self.c_card,
            fg=self.c_primary
        ).pack(side="left", padx=(0, 6))

        self.combo_orden = ttk.Combobox(
            fila2,
            values=[
                "Original",
                "Tarifa: Menor a Mayor (Ascendente - Act. 4)",
                "Tarifa: Mayor a Menor (Descendente - Act. 5)",
                "Calificación: Mejor Valorados",
                "Código (A-Z)"
            ],
            state="readonly",
            width=36
        )
        self.combo_orden.set("Original")
        self.combo_orden.pack(side="left", padx=(0, 16))
        self.combo_orden.bind("<<ComboboxSelected>>", lambda e: self._filtrar_y_ordenar_catalogo())

        self.var_solo_disp = tk.BooleanVar(value=False)
        chk_disp = tk.Checkbutton(
            fila2,
            text="Solo disponibilidad inmediata",
            variable=self.var_solo_disp,
            bg=self.c_card,
            activebackground=self.c_card,
            font=("Segoe UI", 9),
            command=self._filtrar_y_ordenar_catalogo
        )
        chk_disp.pack(side="left")

        # Contador de resultados
        self.lbl_contador_catalogo = tk.Label(
            fila2,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg=self.c_card,
            fg=self.c_muted
        )
        self.lbl_contador_catalogo.pack(side="right")

        # Tabla Treeview de Servicios
        tabla_frame = tk.Frame(self.content_area, bg=self.c_card, bd=1, relief="solid")
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "categoria", "prestador", "tarifa", "ciudad", "disp", "rating", "contratos")
        self.tree_servicios = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            style="Ypri.Treeview",
            selectmode="browse"
        )

        headers = [
            ("codigo", "Código", 90, "center"),
            ("categoria", "Categoría", 130, "w"),
            ("prestador", "Prestador de Servicio", 170, "w"),
            ("tarifa", "Tarifa / Hora (COP)", 140, "e"),
            ("ciudad", "Ciudad", 110, "center"),
            ("disp", "Disponibilidad", 120, "center"),
            ("rating", "Rating", 90, "center"),
            ("contratos", "Contratos", 90, "center"),
        ]

        for col, txt, w, anch in headers:
            self.tree_servicios.heading(col, text=txt)
            self.tree_servicios.column(col, width=w, anchor=anch)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree_servicios.yview)
        self.tree_servicios.configure(yscrollcommand=scroll.set)
        self.tree_servicios.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Barra de Accion Inferior
        bar_accion = tk.Frame(self.content_area, bg=self.c_bg, pady=10)
        bar_accion.pack(fill="x")

        btn_contratar = tk.Button(
            bar_accion,
            text="🤝 Solicitar Contratación de este Servicio",
            font=("Segoe UI", 10, "bold"),
            bg=self.c_primary,
            fg="#FFFFFF",
            activebackground=self.c_primary_hover,
            activeforeground="#FFFFFF",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self._contratar_servicio_seleccionado
        )
        btn_contratar.pack(side="left")

        btn_detalle = tk.Button(
            bar_accion,
            text="🔎 Ver Detalle Completo",
            font=("Segoe UI", 9),
            bg="#E2E8F0",
            fg="#1E293B",
            activebackground="#CBD5E1",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self._ver_detalle_popup
        )
        btn_detalle.pack(side="left", padx=10)

        # Cargar datos iniciales
        self._filtrar_y_ordenar_catalogo()

    def _filtrar_y_ordenar_catalogo(self):
        """
        GUIA 8 - ACTIVIDADES 3, 4, 5, 7:
        Procesa el vector de servicios aplicando busqueda secuencial y ordenamiento.
        """
        texto = self.ent_buscar.get().strip().lower()
        cat = self.combo_cat.get()
        ciu = self.combo_ciudad.get()
        orden = self.combo_orden.get()
        solo_disp = self.var_solo_disp.get()

        # 1. Copiar vector base (Actividad 2)
        resultado = list(servicios)

        # 2. Filtrado / Busqueda secuencial (Actividad 7)
        if texto:
            resultado = [
                s for s in resultado
                if texto in s["codigo"].lower()
                or texto in s["categoria"].lower()
                or texto in s["prestador_nombre"].lower()
                or texto in s["descripcion"].lower()
            ]

        if cat != "Todas":
            resultado = [s for s in resultado if s["categoria"] == cat]

        if ciu != "Todas":
            resultado = [s for s in resultado if s["ciudad"] == ciu]

        if solo_disp:
            resultado = [s for s in resultado if s["disponible"]]

        # 3. Ordenamiento de Vectores (Actividades 4 y 5)
        if "Ascendente" in orden:
            resultado = sorted(resultado, key=lambda s: s["tarifa_hora"])
        elif "Descendente" in orden:
            resultado = sorted(resultado, key=lambda s: s["tarifa_hora"], reverse=True)
        elif "Calificación" in orden:
            resultado = sorted(resultado, key=lambda s: s["calificacion"], reverse=True)
        elif "Código" in orden:
            resultado = sorted(resultado, key=lambda s: s["codigo"])

        # 4. Renderizar en Treeview (Actividad 3 y 9)
        for item in self.tree_servicios.get_children():
            self.tree_servicios.delete(item)

        for s in resultado:
            disp_str = "🟢 Inmediata" if s["disponible"] else "🔴 No disponible"
            self.tree_servicios.insert(
                "",
                "end",
                iid=s["codigo"],
                values=(
                    s["codigo"],
                    s["categoria"],
                    s["prestador_nombre"],
                    f"${s['tarifa_hora']:,.0f}",
                    s["ciudad"],
                    disp_str,
                    f"⭐ {s['calificacion']:.1f}",
                    s["num_contratos"]
                )
            )

        self.lbl_contador_catalogo.config(
            text=f"Mostrando {len(resultado)} de {len(servicios)} servicios registrados en el vector"
        )

    def _ver_detalle_popup(self):
        """Muestra popup con el detalle completo del servicio seleccionado."""
        sel = self.tree_servicios.selection()
        if not sel:
            messagebox.showinfo("YPRI", "Seleccione un servicio de la tabla para ver su detalle.")
            return

        codigo = sel[0]
        # Busqueda secuencial por identificador (Guia 8 - Actividad 6)
        serv = next((s for s in servicios if s["codigo"] == codigo), None)
        if not serv:
            return

        msg = (
            f"Código: {serv['codigo']}\n"
            f"Categoría: {serv['categoria']}\n"
            f"Prestador: {serv['prestador_nombre']}\n"
            f"Ciudad de Cobertura: {serv['ciudad']}\n"
            f"Tarifa por Hora: ${serv['tarifa_hora']:,.0f} COP\n"
            f"Disponibilidad Inmediata: {'Sí' if serv['disponible'] else 'No'}\n"
            f"Calificación Promedio: ⭐ {serv['calificacion']:.1f}\n"
            f"Contratos Realizados: {serv['num_contratos']}\n\n"
            f"Descripción del Trabajo:\n{serv['descripcion']}"
        )
        messagebox.showinfo(f"Detalle de Servicio — {codigo}", msg)

    def _contratar_servicio_seleccionado(self):
        """Redirige al modulo de solicitud con el servicio seleccionado pre-cargado."""
        sel = self.tree_servicios.selection()
        if not sel:
            messagebox.showinfo("YPRI", "Seleccione un servicio del catálogo para contratar.")
            return

        codigo = sel[0]
        self.servicio_preseleccionado_codigo = codigo
        self.mostrar_vista("solicitar")

    # ====================================================================================
    # VISTA 2: SOLICITAR SERVICIO Y COTIZADOR CON IVA (19%)
    # ====================================================================================

    def _vista_solicitar(self):
        """Vista para cotizar servicios con calculo de IVA automatico y generacion de contrato."""
        header = tk.Frame(self.content_area, bg=self.c_bg)
        header.pack(fill="x", pady=(0, 16))

        tk.Label(
            header,
            text="Solicitar Servicio y Cotización en Tiempo Real",
            font=("Segoe UI", 18, "bold"),
            bg=self.c_bg,
            fg=self.c_text
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Calcula el valor exacto del servicio incluyendo el impuesto del 19% (IVA)",
            font=("Segoe UI", 9),
            bg=self.c_bg,
            fg=self.c_muted
        ).pack(anchor="w")

        # Contenedor dividido en 2 columnas: Formulario (Izq) y Resumen de Cotizacion (Der)
        split_frame = tk.Frame(self.content_area, bg=self.c_bg)
        split_frame.pack(fill="both", expand=True)

        col_izq = tk.Frame(split_frame, bg=self.c_card, padx=20, pady=20, bd=1, relief="solid")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # Selector de servicio
        tk.Label(col_izq, text="1. Seleccione el Servicio a Contratar:", font=("Segoe UI", 10, "bold"), bg=self.c_card).pack(anchor="w", pady=(0, 6))

        # Solo servicios disponibles
        disponibles = [s for s in servicios if s["disponible"]]
        opciones_serv = [f"{s['codigo']} | {s['categoria']} — {s['prestador_nombre']} (${s['tarifa_hora']:,.0f}/h)" for s in disponibles]

        self.combo_solicitar_serv = ttk.Combobox(col_izq, values=opciones_serv, state="readonly", width=46)
        if opciones_serv:
            # Si habia preseleccion
            pre_codigo = getattr(self, "servicio_preseleccionado_codigo", None)
            idx_sel = 0
            if pre_codigo:
                for i, op in enumerate(opciones_serv):
                    if pre_codigo in op:
                        idx_sel = i
                        break
            self.combo_solicitar_serv.current(idx_sel)
        self.combo_solicitar_serv.pack(fill="x", pady=(0, 16))
        self.combo_solicitar_serv.bind("<<ComboboxSelected>>", lambda e: self._recalcular_cotizacion())

        # Horas requeridas
        tk.Label(col_izq, text="2. Horas estimadas requeridas:", font=("Segoe UI", 10, "bold"), bg=self.c_card).pack(anchor="w", pady=(0, 6))

        horas_frame = tk.Frame(col_izq, bg=self.c_card)
        horas_frame.pack(anchor="w", pady=(0, 20))

        self.var_horas = tk.IntVar(value=4)

        btn_menos = tk.Button(horas_frame, text="  -  ", font=("Segoe UI", 11, "bold"), bg="#E2E8F0", bd=0, command=self._disminuir_horas)
        btn_menos.pack(side="left")

        self.lbl_horas_disp = tk.Label(horas_frame, text="4 horas", font=("Segoe UI", 12, "bold"), width=12, bg=self.c_card)
        self.lbl_horas_disp.pack(side="left", padx=8)

        btn_mas = tk.Button(horas_frame, text="  +  ", font=("Segoe UI", 11, "bold"), bg="#E2E8F0", bd=0, command=self._aumentar_horas)
        btn_mas.pack(side="left")

        # Boton Confirmar
        btn_confirmar = tk.Button(
            col_izq,
            text="✅ Confirmar Solicitud y Formalizar Contrato",
            font=("Segoe UI", 11, "bold"),
            bg=self.c_primary,
            fg="#FFFFFF",
            activebackground=self.c_primary_hover,
            activeforeground="#FFFFFF",
            bd=0,
            pady=12,
            cursor="hand2",
            command=self._confirmar_contratacion_gui
        )
        btn_confirmar.pack(fill="x", pady=(20, 0))

        # Columna Derecha: Tarjeta de Cotizacion en Vivo
        col_der = tk.Frame(split_frame, bg="#1E293B", padx=24, pady=24, bd=1, relief="solid")
        col_der.pack(side="right", fill="both", expand=True)

        tk.Label(col_der, text="RESUMEN DE COTIZACIÓN", font=("Segoe UI", 13, "bold"), bg="#1E293B", fg="#60A5FA").pack(anchor="w", pady=(0, 16))

        self.lbl_cot_servicio = tk.Label(col_der, text="Servicio: -", font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0")
        self.lbl_cot_servicio.pack(anchor="w", pady=3)

        self.lbl_cot_prestador = tk.Label(col_der, text="Prestador: -", font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0")
        self.lbl_cot_prestador.pack(anchor="w", pady=3)

        self.lbl_cot_tarifa = tk.Label(col_der, text="Tarifa por hora: $0 COP", font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0")
        self.lbl_cot_tarifa.pack(anchor="w", pady=3)

        tk.Frame(col_der, bg="#334155", height=1).pack(fill="x", pady=12)

        self.lbl_cot_subtotal = tk.Label(col_der, text="Subtotal: $0 COP", font=("Segoe UI", 11), bg="#1E293B", fg="#E2E8F0")
        self.lbl_cot_subtotal.pack(anchor="w", pady=3)

        self.lbl_cot_iva = tk.Label(col_der, text="IVA (19%): $0 COP", font=("Segoe UI", 11), bg="#1E293B", fg="#FCD34D")
        self.lbl_cot_iva.pack(anchor="w", pady=3)

        tk.Frame(col_der, bg="#334155", height=2).pack(fill="x", pady=12)

        tk.Label(col_der, text="VALOR TOTAL FACTURADO:", font=("Segoe UI", 9, "bold"), bg="#1E293B", fg="#94A3B8").pack(anchor="w")
        self.lbl_cot_total = tk.Label(col_der, text="$ 0 COP", font=("Segoe UI", 22, "bold"), bg="#1E293B", fg="#34D399")
        self.lbl_cot_total.pack(anchor="w", pady=4)

        tk.Label(col_der, text="* Estado inicial del contrato: Pendiente", font=("Segoe UI", 8, "italic"), bg="#1E293B", fg="#94A3B8").pack(anchor="w", pady=(10, 0))

        self._recalcular_cotizacion()

    def _disminuir_horas(self):
        h = max(1, self.var_horas.get() - 1)
        self.var_horas.set(h)
        self.lbl_horas_disp.config(text=f"{h} hora{'s' if h > 1 else ''}")
        self._recalcular_cotizacion()

    def _aumentar_horas(self):
        h = min(100, self.var_horas.get() + 1)
        self.var_horas.set(h)
        self.lbl_horas_disp.config(text=f"{h} hora{'s' if h > 1 else ''}")
        self._recalcular_cotizacion()

    def _recalcular_cotizacion(self):
        """Calcula subtotal, IVA del 19% y total estimado en tiempo real."""
        val = self.combo_solicitar_serv.get()
        if not val:
            return

        codigo = val.split(" | ")[0]
        serv = next((s for s in servicios if s["codigo"] == codigo), None)
        if not serv:
            return

        horas = self.var_horas.get()
        subtotal = horas * serv["tarifa_hora"]
        iva = subtotal * IVA_PORCENTAJE
        total = subtotal + iva

        self.lbl_cot_servicio.config(text=f"Servicio: {serv['codigo']} — {serv['categoria']}")
        self.lbl_cot_prestador.config(text=f"Prestador: {serv['prestador_nombre']} ({serv['ciudad']})")
        self.lbl_cot_tarifa.config(text=f"Tarifa base: ${serv['tarifa_hora']:,.0f} COP / hora")
        self.lbl_cot_subtotal.config(text=f"Subtotal ({horas}h): ${subtotal:,.0f} COP")
        self.lbl_cot_iva.config(text=f"IVA (19%): ${iva:,.0f} COP")
        self.lbl_cot_total.config(text=f"${total:,.0f} COP")

    def _confirmar_contratacion_gui(self):
        """Crea el nuevo contrato en el vector de contratos."""
        val = self.combo_solicitar_serv.get()
        if not val:
            messagebox.showwarning("YPRI", "Seleccione un servicio válido.")
            return

        codigo = val.split(" | ")[0]
        serv = next((s for s in servicios if s["codigo"] == codigo), None)
        if not serv:
            return

        u = get_sesion_actual()
        if not u:
            messagebox.showerror("YPRI", "Debe tener una sesión activa para contratar.")
            return

        horas = self.var_horas.get()
        subtotal = horas * serv["tarifa_hora"]
        total = subtotal * (1 + IVA_PORCENTAJE)

        # Generar ID
        nuevo_id = f"CONTR-{str(len(contratos) + 1).zfill(3)}"

        # GUIA 8: Insercion de diccionario en vector contratos
        nuevo_contrato = {
            "id": nuevo_id,
            "cliente_id": u["id"],
            "cliente_nombre": u["nombre"],
            "servicio_codigo": serv["codigo"],
            "servicio_nombre": f"{serv['categoria']} - {serv['prestador_nombre']}",
            "horas": horas,
            "tarifa_hora": serv["tarifa_hora"],
            "total": total,
            "estado": ESTADOS_CONTRATO[0],  # "Pendiente"
            "calificacion": 0.0,
            "comentario": ""
        }

        contratos.append(nuevo_contrato)
        serv["num_contratos"] += 1

        messagebox.showinfo(
            "¡Contrato Formalizado!",
            f"Contrato {nuevo_id} generado exitosamente.\n\n"
            f"Servicio: {serv['categoria']} con {serv['prestador_nombre']}\n"
            f"Horas: {horas}h\n"
            f"Total Facturado: ${total:,.0f} COP (IVA 19% incluido)\n"
            f"Estado Inicial: Pendiente"
        )
        self.mostrar_vista("contratos")

    # ====================================================================================
    # VISTA 3: MIS CONTRATOS, ESTADOS Y CALIFICACIONES
    # ====================================================================================

    def _vista_contratos(self):
        """Visualiza el vector de contratos del usuario con controles para actualizar y calificar."""
        header = tk.Frame(self.content_area, bg=self.c_bg)
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="Gestión de Contratos y Calificaciones",
            font=("Segoe UI", 18, "bold"),
            bg=self.c_bg,
            fg=self.c_text
        ).pack(anchor="w")

        u = get_sesion_actual()
        tk.Label(
            header,
            text=f"Listado de acuerdos de servicio para {u['nombre']} ({u['rol'].capitalize()})",
            font=("Segoe UI", 9),
            bg=self.c_bg,
            fg=self.c_muted
        ).pack(anchor="w")

        # Tabla de Contratos
        tabla_frame = tk.Frame(self.content_area, bg=self.c_card, bd=1, relief="solid")
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("id", "servicio", "cliente", "horas", "total", "estado", "calif")
        self.tree_contratos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            style="Ypri.Treeview",
            selectmode="browse"
        )

        headers = [
            ("id", "ID Contrato", 110, "center"),
            ("servicio", "Servicio Contratado", 220, "w"),
            ("cliente", "Cliente", 150, "w"),
            ("horas", "Horas", 70, "center"),
            ("total", "Total Facturado", 130, "e"),
            ("estado", "Estado Actual", 130, "center"),
            ("calif", "Calificación", 100, "center"),
        ]

        for col, txt, w, anch in headers:
            self.tree_contratos.heading(col, text=txt)
            self.tree_contratos.column(col, width=w, anchor=anch)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree_contratos.yview)
        self.tree_contratos.configure(yscrollcommand=scroll.set)
        self.tree_contratos.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Cargar contratos correspondientes al usuario
        for c in contratos:
            if u["rol"] == "admin" or c["cliente_id"] == u["id"] or u["nombre"] in c["servicio_nombre"]:
                calif_str = f"⭐ {c['calificacion']:.1f}" if c.get("calificacion", 0) > 0 else "Sin calificar"
                self.tree_contratos.insert(
                    "",
                    "end",
                    iid=c["id"],
                    values=(
                        c["id"],
                        c["servicio_nombre"],
                        c["cliente_nombre"],
                        f"{c['horas']}h",
                        f"${c['total']:,.0f}",
                        c["estado"],
                        calif_str
                    )
                )

        # Acciones de Contratos
        bar_accion = tk.Frame(self.content_area, bg=self.c_bg, pady=10)
        bar_accion.pack(fill="x")

        btn_actualizar_estado = tk.Button(
            bar_accion,
            text="🔄 Actualizar Estado de Contrato",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#FFFFFF",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self._actualizar_estado_popup
        )
        btn_actualizar_estado.pack(side="left")

        btn_calificar = tk.Button(
            bar_accion,
            text="⭐ Calificar Servicio Completado",
            font=("Segoe UI", 9, "bold"),
            bg="#D97706",
            fg="#FFFFFF",
            activebackground="#B45309",
            activeforeground="#FFFFFF",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self._calificar_servicio_popup
        )
        btn_calificar.pack(side="left", padx=10)

    def _actualizar_estado_popup(self):
        """Permite a prestadores o administradores avanzar el estado del contrato."""
        sel = self.tree_contratos.selection()
        if not sel:
            messagebox.showinfo("YPRI", "Seleccione un contrato de la lista.")
            return

        cid = sel[0]
        c = next((item for item in contratos if item["id"] == cid), None)
        if not c:
            return

        u = get_sesion_actual()
        if u["rol"] == "cliente":
            messagebox.showwarning("YPRI", "Solo los prestadores y administradores pueden modificar el estado del contrato.")
            return

        win = tk.Toplevel(self)
        win.title("Actualizar Estado de Contrato")
        win.geometry("380x240")
        win.configure(bg="#FFFFFF", padx=20, pady=20)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text=f"Contrato: {c['id']}", font=("Segoe UI", 12, "bold"), bg="#FFFFFF").pack(anchor="w")
        tk.Label(win, text=f"Estado actual: {c['estado']}", font=("Segoe UI", 10), bg="#FFFFFF", fg="#64748B").pack(anchor="w", pady=(0, 12))

        tk.Label(win, text="Seleccione el nuevo estado:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w")
        combo = ttk.Combobox(win, values=list(ESTADOS_CONTRATO), state="readonly")
        combo.set(c["estado"])
        combo.pack(fill="x", pady=8)

        def guardar():
            nuevo = combo.get()
            c["estado"] = nuevo
            messagebox.showinfo("YPRI", f"Estado del contrato {c['id']} actualizado a '{nuevo}'.")
            win.destroy()
            self.mostrar_vista("contratos")

        btn_guardar = tk.Button(win, text="Guardar Estado", font=("Segoe UI", 10, "bold"), bg=self.c_primary, fg="#FFFFFF", bd=0, pady=8, command=guardar)
        btn_guardar.pack(fill="x", pady=10)

    def _calificar_servicio_popup(self):
        """Permite calificar un contrato en estado Completado."""
        sel = self.tree_contratos.selection()
        if not sel:
            messagebox.showinfo("YPRI", "Seleccione un contrato para calificar.")
            return

        cid = sel[0]
        c = next((item for item in contratos if item["id"] == cid), None)
        if not c:
            return

        if c["estado"] != "Completado":
            messagebox.showwarning("YPRI", f"Solo se pueden calificar contratos en estado 'Completado'. Estado actual: {c['estado']}.")
            return

        if c.get("calificacion", 0) > 0:
            messagebox.showinfo("YPRI", f"Este contrato ya fue calificado previamente con {c['calificacion']:.1f} estrellas.")
            return

        win = tk.Toplevel(self)
        win.title("Calificar Servicio")
        win.geometry("400x320")
        win.configure(bg="#FFFFFF", padx=20, pady=20)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Calificar Servicio Recibido", font=("Segoe UI", 13, "bold"), bg="#FFFFFF", fg=self.c_primary).pack(anchor="w")
        tk.Label(win, text=f"Servicio: {c['servicio_nombre']}", font=("Segoe UI", 10), bg="#FFFFFF", fg="#64748B").pack(anchor="w", pady=(0, 12))

        tk.Label(win, text="Puntuación (estrellas de 1.0 a 5.0):", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w")
        combo_estrellas = ttk.Combobox(win, values=["5.0", "4.8", "4.5", "4.0", "3.5", "3.0", "2.0", "1.0"], state="readonly")
        combo_estrellas.set("5.0")
        combo_estrellas.pack(fill="x", pady=6)

        tk.Label(win, text="Comentario u observación (opcional):", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w", pady=(8, 2))
        ent_comentario = ttk.Entry(win)
        ent_comentario.insert(0, "Excelente servicio y puntualidad")
        ent_comentario.pack(fill="x", pady=6)

        def registrar_calif():
            try:
                punt = float(combo_estrellas.get())
            except ValueError:
                punt = 5.0
            coment = ent_comentario.get().strip()

            c["calificacion"] = punt
            c["comentario"] = coment

            # Recalculo matematico ponderado en el servicio
            serv = next((s for s in servicios if s["codigo"] == c["servicio_codigo"]), None)
            if serv:
                n = max(1, serv["num_contratos"])
                serv["calificacion"] = round(((serv["calificacion"] * (n - 1)) + punt) / n, 1)

            calificaciones.append({
                "id": f"CALIF-{str(len(calificaciones) + 1).zfill(3)}",
                "contrato_id": c["id"],
                "cliente_nombre": c["cliente_nombre"],
                "servicio_codigo": c["servicio_codigo"],
                "puntuacion": punt,
                "comentario": coment,
                "fecha": "19/10/2026"
            })

            messagebox.showinfo("YPRI", f"¡Calificación de {punt}⭐ registrada exitosamente!")
            win.destroy()
            self.mostrar_vista("contratos")

        btn_guardar = tk.Button(win, text="⭐ Enviar Calificación", font=("Segoe UI", 10, "bold"), bg="#D97706", fg="#FFFFFF", bd=0, pady=8, command=registrar_calif)
        btn_guardar.pack(fill="x", pady=16)

    # ====================================================================================
    # VISTA 4: PUBLICAR / MODIFICAR SERVICIOS (PRESTADORES)
    # ====================================================================================

    def _vista_publicar(self):
        """Vista para dar de alta nuevos servicios en el vector y modificar existentes."""
        header = tk.Frame(self.content_area, bg=self.c_bg)
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="Publicar Nuevo Servicio Profesional",
            font=("Segoe UI", 18, "bold"),
            bg=self.c_bg,
            fg=self.c_text
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Agrega un nuevo elemento al vector unidimensional de servicios en memoria",
            font=("Segoe UI", 9),
            bg=self.c_bg,
            fg=self.c_muted
        ).pack(anchor="w")

        # Formulario
        form_frame = tk.Frame(self.content_area, bg=self.c_card, padx=24, pady=20, bd=1, relief="solid")
        form_frame.pack(fill="x", pady=(0, 16))

        # Grid de campos
        tk.Label(form_frame, text="Categoría del Servicio:", font=("Segoe UI", 9, "bold"), bg=self.c_card).grid(row=0, column=0, sticky="w", pady=6)
        combo_cat = ttk.Combobox(form_frame, values=list(CATEGORIAS_SERVICIO), state="readonly", width=30)
        combo_cat.set(CATEGORIAS_SERVICIO[0])
        combo_cat.grid(row=0, column=1, sticky="w", padx=10, pady=6)

        tk.Label(form_frame, text="Ciudad de Cobertura:", font=("Segoe UI", 9, "bold"), bg=self.c_card).grid(row=1, column=0, sticky="w", pady=6)
        combo_ciudad = ttk.Combobox(form_frame, values=list(CIUDADES_COBERTURA), state="readonly", width=30)
        combo_ciudad.set(CIUDADES_COBERTURA[0])
        combo_ciudad.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        tk.Label(form_frame, text="Tarifa por Hora (COP):", font=("Segoe UI", 9, "bold"), bg=self.c_card).grid(row=2, column=0, sticky="w", pady=6)
        ent_tarifa = ttk.Entry(form_frame, width=32)
        ent_tarifa.insert(0, "32000")
        ent_tarifa.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        tk.Label(form_frame, text="Descripción del Servicio:", font=("Segoe UI", 9, "bold"), bg=self.c_card).grid(row=3, column=0, sticky="w", pady=6)
        ent_desc = ttk.Entry(form_frame, width=54)
        ent_desc.insert(0, "Instalaciones profesionales garantizadas con herramientas de alta calidad")
        ent_desc.grid(row=3, column=1, sticky="w", padx=10, pady=6)

        var_disp = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(form_frame, text="Disponibilidad inmediata para atender hoy", variable=var_disp, bg=self.c_card, font=("Segoe UI", 9))
        chk.grid(row=4, column=1, sticky="w", padx=10, pady=6)

        def publicar():
            try:
                tarifa_val = float(ent_tarifa.get().strip())
                if tarifa_val < 10000 or tarifa_val > 500000:
                    messagebox.showerror("YPRI", "La tarifa debe estar entre $10.000 y $500.000 COP.")
                    return
            except ValueError:
                messagebox.showerror("YPRI", "Ingrese un valor numérico válido para la tarifa.")
                return

            desc_val = ent_desc.get().strip()
            if len(desc_val) < 10:
                messagebox.showerror("YPRI", "La descripción debe tener al menos 10 caracteres.")
                return

            u = get_sesion_actual()
            nuevo_cod = f"SERV-{str(len(servicios) + 1).zfill(2)}"

            nuevo_serv = {
                "codigo": nuevo_cod,
                "prestador_id": u["id"],
                "prestador_nombre": u["nombre"],
                "categoria": combo_cat.get(),
                "descripcion": desc_val,
                "tarifa_hora": tarifa_val,
                "ciudad": combo_ciudad.get(),
                "disponible": var_disp.get(),
                "calificacion": 5.0,
                "num_contratos": 0
            }

            servicios.append(nuevo_serv)
            messagebox.showinfo("YPRI", f"¡Servicio '{nuevo_cod}' registrado exitosamente en el vector!")
            self.mostrar_vista("catalogo")

        btn_guardar = tk.Button(
            form_frame,
            text="🚀 Guardar y Publicar Servicio",
            font=("Segoe UI", 10, "bold"),
            bg=self.c_primary,
            fg="#FFFFFF",
            bd=0,
            pady=10,
            cursor="hand2",
            command=publicar
        )
        btn_guardar.grid(row=5, column=1, sticky="w", padx=10, pady=16)

    # ====================================================================================
    # VISTA 5: RETO DE INTEGRACION Y ANALISIS DEL VECTOR (GUIA 8 - ACTIVIDAD 13)
    # ====================================================================================

    def _vista_reto_vectores(self):
        """
        GUIA 8 - ACTIVIDAD 13: Reto de Integracion.
        Procesa el vector de servicios para mostrar:
        - Elemento minimo (servicio mas economico)
        - Elemento maximo (servicio mas costoso)
        - Promedio aritmetico del vector
        - Ranking de los 3 mas contratados
        """
        header = tk.Frame(self.content_area, bg=self.c_bg)
        header.pack(fill="x", pady=(0, 16))

        tk.Label(
            header,
            text="Análisis y Procesamiento Estadístico de Vectores",
            font=("Segoe UI", 18, "bold"),
            bg=self.c_bg,
            fg=self.c_text
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Guía 8 - Actividad 13: Extracción de métricas sobre la estructura unidimensional (min, max, avg, sort)",
            font=("Segoe UI", 9),
            bg=self.c_bg,
            fg=self.c_muted
        ).pack(anchor="w")

        if not servicios:
            tk.Label(self.content_area, text="No hay elementos en el vector.", bg=self.c_bg).pack()
            return

        # Calculos en el vector
        s_min = min(servicios, key=lambda s: s["tarifa_hora"])
        s_max = max(servicios, key=lambda s: s["tarifa_hora"])
        s_best = max(servicios, key=lambda s: s["calificacion"])
        tarifa_prom = sum(s["tarifa_hora"] for s in servicios) / len(servicios)

        # Fila de 4 Tarjetas de Metricas (KPIs)
        kpi_frame = tk.Frame(self.content_area, bg=self.c_bg)
        kpi_frame.pack(fill="x", pady=(0, 16))

        metricas = [
            ("🟢 SERVICIO MÁS ECONÓMICO", f"${s_min['tarifa_hora']:,.0f}/h", f"{s_min['codigo']} • {s_min['categoria']}", s_min['prestador_nombre']),
            ("💎 SERVICIO MAYOR TARIFA", f"${s_max['tarifa_hora']:,.0f}/h", f"{s_max['codigo']} • {s_max['categoria']}", s_max['prestador_nombre']),
            ("⭐ MEJOR VALORADO", f"{s_best['calificacion']:.1f} Estrellas", f"{s_best['codigo']} • {s_best['categoria']}", s_best['prestador_nombre']),
            ("📈 TARIFA PROMEDIO", f"${tarifa_prom:,.0f}/h", f"Sobre {len(servicios)} servicios", "Vector YPRI"),
        ]

        for titulo, val, sub, autor in metricas:
            card = tk.Frame(kpi_frame, bg=self.c_card, padx=14, pady=12, bd=1, relief="solid")
            card.pack(side="left", fill="both", expand=True, padx=4)

            tk.Label(card, text=titulo, font=("Segoe UI", 8, "bold"), bg=self.c_card, fg=self.c_muted).pack(anchor="w")
            tk.Label(card, text=val, font=("Segoe UI", 14, "bold"), bg=self.c_card, fg=self.c_primary).pack(anchor="w", pady=2)
            tk.Label(card, text=sub, font=("Segoe UI", 9, "bold"), bg=self.c_card, fg=self.c_text).pack(anchor="w")
            tk.Label(card, text=autor, font=("Segoe UI", 8), bg=self.c_card, fg=self.c_muted).pack(anchor="w")

        # Tarjeta de Top 3 Ranking
        top_frame = tk.Frame(self.content_area, bg=self.c_card, padx=20, pady=16, bd=1, relief="solid")
        top_frame.pack(fill="both", expand=True)

        tk.Label(
            top_frame,
            text="🏆 Ranking Top 3: Servicios con Mayor Número de Contratos Realizados",
            font=("Segoe UI", 12, "bold"),
            bg=self.c_card,
            fg=self.c_text
        ).pack(anchor="w", pady=(0, 12))

        top3 = sorted(servicios, key=lambda s: s["num_contratos"], reverse=True)[:3]
        for idx, s in enumerate(top3, 1):
            row = tk.Frame(top_frame, bg="#F8FAFC", padx=12, pady=10, bd=1, relief="solid")
            row.pack(fill="x", pady=4)

            tk.Label(row, text=f"#{idx}", font=("Segoe UI", 12, "bold"), bg="#F8FAFC", fg=self.c_primary, width=3).pack(side="left")
            tk.Label(row, text=f"{s['codigo']} — {s['categoria']}", font=("Segoe UI", 10, "bold"), bg="#F8FAFC", width=22, anchor="w").pack(side="left")
            tk.Label(row, text=f"Prestador: {s['prestador_nombre']} ({s['ciudad']})", font=("Segoe UI", 9), bg="#F8FAFC", width=30, anchor="w").pack(side="left")
            tk.Label(row, text=f"Tarifa: ${s['tarifa_hora']:,.0f}/h", font=("Segoe UI", 9), bg="#F8FAFC", width=18, anchor="w").pack(side="left")
            tk.Label(row, text=f"⭐ {s['calificacion']:.1f}", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#D97706", width=8).pack(side="left")
            tk.Label(row, text=f"{s['num_contratos']} contratos", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg=self.c_success).pack(side="right")

    # ====================================================================================
    # VISTA 6: PANEL ADMINISTRADOR
    # ====================================================================================

    def _vista_admin(self):
        """Vista exclusiva para el administrador con metricas de facturacion y usuarios."""
        header = tk.Frame(self.content_area, bg=self.c_bg)
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="Panel de Control y Auditoría de la Plataforma",
            font=("Segoe UI", 18, "bold"),
            bg=self.c_bg,
            fg=self.c_text
        ).pack(anchor="w")

        # Tarjetas de Facturacion y Totales
        ingresos_totales = sum(c["total"] for c in contratos if c["estado"] == "Completado")
        disp_count = sum(1 for s in servicios if s["disponible"])

        kpi_frame = tk.Frame(self.content_area, bg=self.c_bg)
        kpi_frame.pack(fill="x", pady=(0, 14))

        for tit, val, col in [
            ("TOTAL USUARIOS", str(len(usuarios)), "#2563EB"),
            ("SERVICIOS ACTIVOS", f"{disp_count} de {len(servicios)}", "#059669"),
            ("CONTRATOS GENERADOS", str(len(contratos)), "#D97706"),
            ("INGRESOS FACTURADOS", f"${ingresos_totales:,.0f} COP", "#7C3AED"),
        ]:
            c = tk.Frame(kpi_frame, bg=self.c_card, padx=14, pady=12, bd=1, relief="solid")
            c.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(c, text=tit, font=("Segoe UI", 8, "bold"), bg=self.c_card, fg=self.c_muted).pack(anchor="w")
            tk.Label(c, text=val, font=("Segoe UI", 14, "bold"), bg=self.c_card, fg=col).pack(anchor="w", pady=2)

        # Tabla de Usuarios
        tk.Label(self.content_area, text="Usuarios Registrados en el Sistema:", font=("Segoe UI", 11, "bold"), bg=self.c_bg).pack(anchor="w", pady=(6, 4))

        tabla_frame = tk.Frame(self.content_area, bg=self.c_card, bd=1, relief="solid")
        tabla_frame.pack(fill="both", expand=True)

        cols = ("id", "nombre", "correo", "rol", "ciudad", "telefono")
        tree_u = ttk.Treeview(tabla_frame, columns=cols, show="headings", style="Ypri.Treeview", selectmode="browse")

        for col, txt, w, anch in [
            ("id", "ID", 90, "center"),
            ("nombre", "Nombre Completo", 180, "w"),
            ("correo", "Correo Electrónico", 220, "w"),
            ("rol", "Rol de Acceso", 110, "center"),
            ("ciudad", "Ciudad", 120, "center"),
            ("telefono", "Teléfono", 120, "center"),
        ]:
            tree_u.heading(col, text=txt)
            tree_u.column(col, width=w, anchor=anch)

        tree_u.pack(fill="both", expand=True)

        for u in usuarios:
            tree_u.insert("", "end", values=(u["id"], u["nombre"], u["correo"], u["rol"].capitalize(), u["ciudad"], u["telefono"]))

    # ====================================================================================
    # DIALOGO CAMBIAR USUARIO
    # ====================================================================================

    def _dialogo_cambiar_usuario(self):
        """Permite alternar entre los perfiles precargados o registrar uno nuevo."""
        win = tk.Toplevel(self)
        win.title("Seleccionar Cuenta de Usuario")
        win.geometry("440x360")
        win.configure(bg="#FFFFFF", padx=20, pady=20)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Seleccione una Cuenta de Demostración:", font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg=self.c_primary).pack(anchor="w", pady=(0, 10))

        for u in usuarios:
            btn = tk.Button(
                win,
                text=f"👤 {u['nombre']}  ({u['rol'].capitalize()} • {u['ciudad']})\n   {u['correo']}",
                font=("Segoe UI", 9),
                bg="#F8FAFC",
                fg="#0F172A",
                activebackground="#E2E8F0",
                bd=1,
                relief="solid",
                justify="left",
                anchor="w",
                padx=10,
                pady=6,
                cursor="hand2",
                command=lambda usr=u: self._asignar_usuario_y_cerrar(usr, win)
            )
            btn.pack(fill="x", pady=4)

        tk.Frame(win, bg="#E2E8F0", height=1).pack(fill="x", pady=12)

        btn_nuevo = tk.Button(
            win,
            text="➕ Registrar Nuevo Usuario",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg="#FFFFFF",
            bd=0,
            pady=8,
            cursor="hand2",
            command=lambda: [win.destroy(), self._dialogo_registro_nuevo()]
        )
        btn_nuevo.pack(fill="x")

    def _asignar_usuario_y_cerrar(self, usr, win):
        set_sesion_actual(usr)
        win.destroy()
        self._actualizar_info_usuario()
        messagebox.showinfo("YPRI", f"Sesión iniciada como: {usr['nombre']} ({usr['rol'].capitalize()})")
        self.mostrar_vista("catalogo")

    def _dialogo_registro_nuevo(self):
        """Dialogo para registrar un nuevo usuario con validaciones en la GUI."""
        win = tk.Toplevel(self)
        win.title("Registro de Nuevo Usuario")
        win.geometry("420x460")
        win.configure(bg="#FFFFFF", padx=20, pady=20)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Crear Nueva Cuenta en YPRI", font=("Segoe UI", 13, "bold"), bg="#FFFFFF", fg=self.c_primary).pack(anchor="w", pady=(0, 12))

        def make_field(label_text, default=""):
            tk.Label(win, text=label_text, font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w", pady=(4, 2))
            ent = ttk.Entry(win)
            ent.insert(0, default)
            ent.pack(fill="x")
            return ent

        e_nombre = make_field("Nombre Completo:")
        e_correo = make_field("Correo Electrónico:")
        e_clave  = make_field("Contraseña (mínimo 6 caracteres):")

        tk.Label(win, text="Rol en el Sistema:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w", pady=(6, 2))
        combo_rol = ttk.Combobox(win, values=["cliente", "prestador"], state="readonly")
        combo_rol.set("cliente")
        combo_rol.pack(fill="x")

        tk.Label(win, text="Ciudad de Residencia:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w", pady=(6, 2))
        combo_ciudad = ttk.Combobox(win, values=list(CIUDADES_COBERTURA), state="readonly")
        combo_ciudad.set(CIUDADES_COBERTURA[0])
        combo_ciudad.pack(fill="x")

        e_tel = make_field("Teléfono (10 dígitos):")

        def guardar():
            nombre = e_nombre.get().strip().title()
            correo = e_correo.get().strip().lower()
            clave  = e_clave.get().strip()
            tel    = e_tel.get().strip()

            if not nombre or not any(c.isalpha() for c in nombre):
                messagebox.showerror("Error", "Ingrese un nombre válido con letras.")
                return
            if "@" not in correo or "." not in correo:
                messagebox.showerror("Error", "Ingrese un correo electrónico válido.")
                return
            if any(u["correo"] == correo for u in usuarios):
                messagebox.showerror("Error", "Este correo ya se encuentra registrado.")
                return
            if len(clave) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
                return
            if not tel.isdigit() or len(tel) != 10:
                messagebox.showerror("Error", "El teléfono debe contener exactamente 10 dígitos numéricos.")
                return

            nuevo_u = {
                "id": f"USR-{str(len(usuarios) + 1).zfill(3)}",
                "nombre": nombre,
                "correo": correo,
                "contrasena": clave,
                "rol": combo_rol.get(),
                "ciudad": combo_ciudad.get(),
                "telefono": tel
            }

            usuarios.append(nuevo_u)
            set_sesion_actual(nuevo_u)
            messagebox.showinfo("YPRI", f"¡Usuario {nombre} registrado exitosamente con ID {nuevo_u['id']}!")
            win.destroy()
            self._actualizar_info_usuario()
            self.mostrar_vista("catalogo")

        btn_reg = tk.Button(win, text="Registrar Usuario", font=("Segoe UI", 10, "bold"), bg=self.c_primary, fg="#FFFFFF", bd=0, pady=10, command=guardar)
        btn_reg.pack(fill="x", pady=16)


def main_gui():
    """Lanzador de la aplicacion grafica."""
    app = YpriApp()
    app.mainloop()


if __name__ == "__main__":
    main_gui()
