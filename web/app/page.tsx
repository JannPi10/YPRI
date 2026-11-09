"use client";

import React, { useState, useMemo } from "react";
import {
  Search,
  Filter,
  ArrowUpDown,
  Plus,
  Shield,
  CheckCircle2,
  Clock,
  XCircle,
  Star,
  Phone,
  MapPin,
  Building2,
  User,
  RefreshCw,
  Smartphone,
  Laptop,
  Sparkles,
  TrendingUp,
  DollarSign,
  Calendar,
  Layers,
  Edit3,
  Award,
  ChevronDown,
  Info,
  Code2,
  Check,
  AlertCircle,
  Wrench
} from "lucide-react";
import {
  USUARIOS_INICIALES,
  SERVICIOS_INICIALES,
  CONTRATOS_INICIALES,
  MATRIZ_SEMANAL_INICIAL,
  MATRIZ_CIUDADES_INICIAL,
  CATEGORIAS_SERVICIO,
  CIUDADES_COBERTURA,
  DIAS_SEMANA_MATRIZ,
  IVA_PORCENTAJE,
  calcularTotalFilas,
  calcularTotalColumnas,
  calcularTotalGeneral,
  calcularPromedioGeneral,
  crearMatrizNula,
  crearMatrizIdentidad,
  formatearMoneda,
  calcularLiquidacionContrato,
  calcularComisionPlataforma,
  calcularPromedioRating,
  ProductoInventario,
  calcularSubtotalInventario,
  calcularTotalInventario,
  Usuario,
  Servicio,
  Contrato,
  CategoriaServicio,
  CiudadCobertura,
  EstadoContrato
} from "../lib/data";

export default function YpriWebApp() {
  // Estado de aplicacion
  const [usuarios, setUsuarios] = useState<Usuario[]>(USUARIOS_INICIALES);
  const [usuarioActual, setUsuarioActual] = useState<Usuario>(USUARIOS_INICIALES[0]); // Juan Perez
  const [servicios, setServicios] = useState<Servicio[]>(SERVICIOS_INICIALES);
  const [contratos, setContratos] = useState<Contrato[]>(CONTRATOS_INICIALES);
  
  // Control de menu de usuario
  const [menuUsuarioAbierto, setMenuUsuarioAbierto] = useState<boolean>(false);

  // Matrices de datos
  const [matrizSemanal, setMatrizSemanal] = useState<number[][]>(MATRIZ_SEMANAL_INICIAL);
  const [matrizCiudades, setMatrizCiudades] = useState<number[][]>(MATRIZ_CIUDADES_INICIAL);
  const [subTipoMatriz, setSubTipoMatriz] = useState<"semanal" | "ciudades" | "ejercicio" | "especiales">("semanal");

  // Vistas
  const [vistaActiva, setVistaActiva] = useState<"catalogo" | "matrices" | "subalgoritmos" | "contratos" | "publicar" | "admin">("catalogo");
  const [modoMovil, setModoMovil] = useState<boolean>(false);

  // Estados de Guía 10 (Subalgoritmos)
  const [subG10Tab, setSubG10Tab] = useState<"funciones" | "procedimientos" | "lambdas" | "argumentos" | "inventario">("funciones");
  const [subG10Tarifa, setSubG10Tarifa] = useState<number>(45000);
  const [subG10Horas, setSubG10Horas] = useState<number>(4);
  const [subG10Descuento, setSubG10Descuento] = useState<number>(10);
  const [subG10ServicioSel, setSubG10ServicioSel] = useState<string>("SERV-001");
  const [subG10RatingPrev, setSubG10RatingPrev] = useState<number>(4.2);
  const [subG10RatingN, setSubG10RatingN] = useState<number>(5);
  const [subG10RatingNueva, setSubG10RatingNueva] = useState<number>(5.0);
  const [subG10Inventario, setSubG10Inventario] = useState<ProductoInventario[]>([
    { codigo: "P01", nombre: "Kit Herramientas Pro", precio: 180000, cantidad: 4 },
    { codigo: "P02", nombre: "Multímetro Digital", precio: 95000, cantidad: 8 },
    { codigo: "P03", nombre: "Taladro Percutor 750W", precio: 250000, cantidad: 3 },
  ]);
  const [invCod, setInvCod] = useState("");
  const [invNom, setInvNom] = useState("");
  const [invPre, setInvPre] = useState("");
  const [invCan, setInvCan] = useState("");
  const [demoLista, setDemoLista] = useState<string[]>(["Electricidad", "Plomería"]);
  const [demoDict, setDemoDict] = useState<{ rol: string; nivel: string }>({ rol: "cliente", nivel: "estándar" });

  // Modales
  const [modalCotizar, setModalCotizar] = useState<Servicio | null>(null);
  const [horasCotizar, setHorasCotizar] = useState<number>(3);
  const [modalEditarCelda, setModalEditarCelda] = useState<{ fila: number; col: number; valor: number; tipo: "semanal" | "ciudades" } | null>(null);
  const [nuevoValorCelda, setNuevoValorCelda] = useState<string>("");
  const [modalCalificar, setModalCalificar] = useState<Contrato | null>(null);
  const [estrellasCalif, setEstrellasCalif] = useState<number>(5);
  const [comentarioCalif, setComentarioCalif] = useState<string>("");
  const [modalNuevoUsuario, setModalNuevoUsuario] = useState<boolean>(false);
  const [notificacion, setNotificacion] = useState<string | null>(null);

  // Formulario nuevo usuario
  const [nuevoU_nombre, setNuevoU_nombre] = useState("");
  const [nuevoU_correo, setNuevoU_correo] = useState("");
  const [nuevoU_rol, setNuevoU_rol] = useState<"cliente" | "prestador">("cliente");
  const [nuevoU_ciudad, setNuevoU_ciudad] = useState<CiudadCobertura>("Cucuta");
  const [nuevoU_tel, setNuevoU_tel] = useState("");

  // Formulario publicar servicio
  const [pub_categoria, setPub_categoria] = useState<CategoriaServicio>("Electricidad");
  const [pub_desc, setPub_desc] = useState("");
  const [pub_tarifa, setPub_tarifa] = useState("35000");
  const [pub_ciudad, setPub_ciudad] = useState<CiudadCobertura>("Cucuta");

  // Filtros de catalogo
  const [filtroTexto, setFiltroTexto] = useState("");
  const [filtroCategoria, setFiltroCategoria] = useState<string>("todas");
  const [filtroCiudad, setFiltroCiudad] = useState<string>("todas");
  const [ordenamiento, setOrdenamiento] = useState<"precio_asc" | "precio_desc" | "rating_desc">("precio_asc");

  const mostrarAlerta = (msg: string) => {
    setNotificacion(msg);
    setTimeout(() => setNotificacion(null), 4000);
  };

  // Filtrado y ordenamiento de servicios
  const serviciosFiltrados = useMemo(() => {
    return servicios
      .filter((s) => {
        const matchTexto =
          s.descripcion.toLowerCase().includes(filtroTexto.toLowerCase()) ||
          s.prestador_nombre.toLowerCase().includes(filtroTexto.toLowerCase()) ||
          s.codigo.toLowerCase().includes(filtroTexto.toLowerCase());
        const matchCat = filtroCategoria === "todas" || s.categoria === filtroCategoria;
        const matchCiu = filtroCiudad === "todas" || s.ciudad === filtroCiudad;
        return matchTexto && matchCat && matchCiu;
      })
      .sort((a, b) => {
        if (ordenamiento === "precio_asc") return a.tarifa_hora - b.tarifa_hora;
        if (ordenamiento === "precio_desc") return b.tarifa_hora - a.tarifa_hora;
        if (ordenamiento === "rating_desc") return b.calificacion - a.calificacion;
        return 0;
      });
  }, [servicios, filtroTexto, filtroCategoria, filtroCiudad, ordenamiento]);

  // Cálculos dinámicos de Facturación y Métricas
  const statsMatrizSemanal = useMemo(() => {
    const totalGen = calcularTotalGeneral(matrizSemanal);
    const promedio = calcularPromedioGeneral(matrizSemanal);
    const totalesFila = calcularTotalFilas(matrizSemanal);
    const totalesCol = calcularTotalColumnas(matrizSemanal);

    let maxVal = -Infinity;
    let maxFila = 0;
    let maxCol = 0;
    for (let i = 0; i < matrizSemanal.length; i++) {
      for (let j = 0; j < matrizSemanal[i].length; j++) {
        if (matrizSemanal[i][j] > maxVal) {
          maxVal = matrizSemanal[i][j];
          maxFila = i;
          maxCol = j;
        }
      }
    }

    const idxMaxFila = totalesFila.indexOf(Math.max(...totalesFila));
    const idxMaxCol = totalesCol.indexOf(Math.max(...totalesCol));

    return {
      totalGen,
      promedio,
      totalesFila,
      totalesCol,
      maxVal,
      maxCat: CATEGORIAS_SERVICIO[maxFila],
      maxDia: DIAS_SEMANA_MATRIZ[maxCol],
      catLider: CATEGORIAS_SERVICIO[idxMaxFila],
      catLiderTotal: totalesFila[idxMaxFila],
      diaLider: DIAS_SEMANA_MATRIZ[idxMaxCol],
      diaLiderTotal: totalesCol[idxMaxCol]
    };
  }, [matrizSemanal]);

  const statsMatrizCiudades = useMemo(() => {
    const totalGen = calcularTotalGeneral(matrizCiudades);
    const promedio = calcularPromedioGeneral(matrizCiudades);
    const totalesFila = calcularTotalFilas(matrizCiudades);
    const totalesCol = calcularTotalColumnas(matrizCiudades);

    const idxMaxFila = totalesFila.indexOf(Math.max(...totalesFila));
    const idxMaxCol = totalesCol.indexOf(Math.max(...totalesCol));

    const diagonal = matrizCiudades.map((row, idx) => row[idx]);

    return {
      totalGen,
      promedio,
      totalesFila,
      totalesCol,
      catLider: CATEGORIAS_SERVICIO[idxMaxFila],
      ciuLider: CIUDADES_COBERTURA[idxMaxCol],
      diagonal
    };
  }, [matrizCiudades]);

  // Actualizar celda
  const guardarEdicionCelda = () => {
    if (!modalEditarCelda) return;
    const num = parseFloat(nuevoValorCelda);
    if (isNaN(num) || num < 0) {
      alert("Por favor ingrese un número no negativo válido.");
      return;
    }
    const { fila, col, tipo } = modalEditarCelda;
    if (tipo === "semanal") {
      const copia = matrizSemanal.map((r, i) => (i === fila ? r.map((c, j) => (j === col ? num : c)) : [...r]));
      setMatrizSemanal(copia);
    } else {
      const copia = matrizCiudades.map((r, i) => (i === fila ? r.map((c, j) => (j === col ? num : c)) : [...r]));
      setMatrizCiudades(copia);
    }
    setModalEditarCelda(null);
    mostrarAlerta(`Celda [${fila}][${col}] actualizada a ${formatearMoneda(num)}`);
  };

  // Sincronizar contratos con matriz
  const sincronizarContratosConMatriz = () => {
    const copia = matrizSemanal.map(r => [...r]);
    let suma = 0;
    let cant = 0;
    contratos.forEach(c => {
      if (c.estado === "Completado") {
        const serv = servicios.find(s => s.codigo === c.servicio_codigo);
        if (serv) {
          const idxCat = CATEGORIAS_SERVICIO.indexOf(serv.categoria);
          if (idxCat !== -1) {
            copia[idxCat][4] += c.total; // Sumar al Viernes
            suma += c.total;
            cant++;
          }
        }
      }
    });
    setMatrizSemanal(copia);
    mostrarAlerta(`Sincronización completada: ${cant} contratos sumaron ${formatearMoneda(suma)} a la facturación.`);
  };

  // Solicitar servicio / Crear contrato
  const confirmarContrato = () => {
    if (!modalCotizar) return;
    const subtotal = modalCotizar.tarifa_hora * horasCotizar;
    const iva = subtotal * IVA_PORCENTAJE;
    const total = subtotal + iva;

    const nuevoContrato: Contrato = {
      id: `CONTR-${100 + contratos.length + 1}`,
      cliente_id: usuarioActual.id,
      cliente_nombre: usuarioActual.nombre,
      servicio_codigo: modalCotizar.codigo,
      servicio_nombre: `${modalCotizar.categoria} - ${modalCotizar.prestador_nombre}`,
      horas: horasCotizar,
      tarifa_hora: modalCotizar.tarifa_hora,
      total,
      estado: "Pendiente",
      fecha: new Date().toLocaleDateString("es-CO")
    };

    setContratos([nuevoContrato, ...contratos]);
    setModalCotizar(null);
    setVistaActiva("contratos");
    mostrarAlerta(`Contrato ${nuevoContrato.id} formalizado por ${formatearMoneda(total)}.`);
  };

  // Cambiar estado de contrato
  const cambiarEstadoContrato = (id: string, nuevoEstado: EstadoContrato) => {
    setContratos(contratos.map(c => c.id === id ? { ...c, estado: nuevoEstado } : c));
    mostrarAlerta(`Contrato ${id} actualizado a estado '${nuevoEstado}'.`);
  };

  // Calificar contrato
  const guardarCalificacion = () => {
    if (!modalCalificar) return;
    setContratos(contratos.map(c => c.id === modalCalificar.id ? { ...c, calificacion: estrellasCalif, comentario: comentarioCalif } : c));
    setServicios(servicios.map(s => {
      if (s.codigo === modalCalificar.servicio_codigo) {
        const nuevaCal = Number(((s.calificacion * s.num_contratos + estrellasCalif) / (s.num_contratos + 1)).toFixed(1));
        return { ...s, calificacion: nuevaCal, num_contratos: s.num_contratos + 1 };
      }
      return s;
    }));
    setModalCalificar(null);
    mostrarAlerta(`Calificación de ${estrellasCalif}.0 puntos registrada exitosamente.`);
  };

  // Publicar nuevo servicio
  const guardarNuevoServicio = (e: React.FormEvent) => {
    e.preventDefault();
    const tarifa = parseFloat(pub_tarifa);
    if (isNaN(tarifa) || tarifa <= 0) {
      alert("Ingrese una tarifa por hora válida.");
      return;
    }
    const nuevoS: Servicio = {
      codigo: `SERV-0${servicios.length + 1}`,
      prestador_id: usuarioActual.id,
      prestador_nombre: usuarioActual.nombre,
      categoria: pub_categoria,
      descripcion: pub_desc || `Servicio profesional de ${pub_categoria}`,
      tarifa_hora: tarifa,
      ciudad: pub_ciudad,
      disponible: true,
      calificacion: 5.0,
      num_contratos: 0
    };
    setServicios([nuevoS, ...servicios]);
    setPub_desc("");
    setVistaActiva("catalogo");
    mostrarAlerta(`Servicio ${nuevoS.codigo} publicado en el catálogo.`);
  };

  // Registrar nuevo usuario
  const guardarNuevoUsuario = (e: React.FormEvent) => {
    e.preventDefault();
    if (!nuevoU_nombre.trim() || !nuevoU_correo.trim()) {
      alert("Por favor complete los campos obligatorios.");
      return;
    }
    const nuevoU: Usuario = {
      id: `USR-00${usuarios.length + 1}`,
      nombre: nuevoU_nombre.trim(),
      correo: nuevoU_correo.trim(),
      contrasena: "123456",
      rol: nuevoU_rol,
      ciudad: nuevoU_ciudad,
      telefono: nuevoU_tel.trim() || "3000000000"
    };
    setUsuarios(prev => [...prev, nuevoU]);
    setUsuarioActual(nuevoU);
    setModalNuevoUsuario(false);
    setNuevoU_nombre("");
    setNuevoU_correo("");
    setNuevoU_tel("");
    mostrarAlerta(`Usuario ${nuevoU.nombre} registrado e iniciado en sesión.`);
  };

  return (
    <div className={`min-h-screen ${modoMovil ? "bg-slate-900 py-6 px-4 flex justify-center items-center" : "bg-slate-100"}`}>
      {/* CONTENEDOR PRINCIPAL: VISTA WEB O SIMULADOR MOVIL */}
      <div
        className={`${
          modoMovil
            ? "w-[400px] h-[840px] bg-slate-100 rounded-[44px] shadow-2xl border-[10px] border-slate-800 flex flex-col overflow-hidden relative"
            : "w-full min-h-screen flex flex-col"
        }`}
      >
        {/* ENCABEZADO SUPERIOR */}
        <header className="bg-slate-900 text-white px-4 py-3 border-b border-slate-800 sticky top-0 z-30 shadow-md">
          <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
            {/* Logo y Titulo */}
            <div className="flex items-center gap-2.5">
              <div className="bg-blue-600 text-white p-2 rounded-xl shadow-sm">
                <Wrench className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-base font-bold tracking-tight text-white">YPRI</h1>
                  <span className="bg-blue-500/20 text-blue-300 text-[10px] font-semibold px-2 py-0.5 rounded-full border border-blue-400/30">
                    Plataforma Oficial
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">Servicios Profesionales a Domicilio</p>
              </div>
            </div>

            {/* Selector de Usuario y Toggle Movil */}
            <div className="flex items-center gap-2">
              {/* Boton Toggle Movil / Web */}
              <button
                type="button"
                onClick={() => setModoMovil(!modoMovil)}
                title={modoMovil ? "Cambiar a Vista Web Completa" : "Simular Dispositivo Móvil"}
                className="hidden sm:flex items-center gap-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1.5 rounded-lg border border-slate-700 transition"
              >
                {modoMovil ? <Laptop className="w-3.5 h-3.5 text-blue-400" /> : <Smartphone className="w-3.5 h-3.5 text-blue-400" />}
                <span className="text-[11px]">{modoMovil ? "Web" : "Móvil"}</span>
              </button>

              {/* Selector de Perfil con Control de Estado (Click directo) */}
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setMenuUsuarioAbierto(!menuUsuarioAbierto)}
                  className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white text-xs px-2.5 py-1.5 rounded-xl cursor-pointer transition"
                >
                  <User className="w-3.5 h-3.5 text-blue-400" />
                  <div className="text-left hidden xs:block">
                    <p className="text-[11px] font-semibold leading-tight">{usuarioActual.nombre}</p>
                    <p className="text-[9px] text-blue-300 capitalize">{usuarioActual.rol}</p>
                  </div>
                  <ChevronDown className="w-3 h-3 text-slate-400" />
                </button>

                {/* Dropdown Activo */}
                {menuUsuarioAbierto && (
                  <>
                    <div
                      className="fixed inset-0 z-40"
                      onClick={() => setMenuUsuarioAbierto(false)}
                    />
                    <div className="absolute right-0 mt-2 w-60 bg-slate-800 border border-slate-700 rounded-xl shadow-2xl p-2 z-50">
                      <p className="text-[10px] text-slate-400 uppercase font-bold px-2 py-1">Cambiar usuario:</p>
                      <div className="space-y-1">
                        {usuarios.map(u => (
                          <button
                            key={u.id}
                            type="button"
                            onClick={() => {
                              setUsuarioActual(u);
                              setMenuUsuarioAbierto(false);
                              mostrarAlerta(`Sesión activa: ${u.nombre} (${u.rol})`);
                            }}
                            className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs flex items-center justify-between transition ${
                              usuarioActual.id === u.id ? "bg-blue-600 text-white font-medium" : "text-slate-200 hover:bg-slate-700"
                            }`}
                          >
                            <div>
                              <p className="font-semibold">{u.nombre}</p>
                              <span className="text-[10px] opacity-75 capitalize">{u.rol} • {u.ciudad}</span>
                            </div>
                            {usuarioActual.id === u.id && <Check className="w-3.5 h-3.5" />}
                          </button>
                        ))}
                      </div>
                      <div className="border-t border-slate-700 my-1.5"></div>
                      <button
                        type="button"
                        onClick={() => {
                          setMenuUsuarioAbierto(false);
                          setModalNuevoUsuario(true);
                        }}
                        className="w-full text-left px-2.5 py-2 rounded-lg text-xs text-blue-400 hover:bg-slate-700 flex items-center gap-1.5 font-bold transition"
                      >
                        <Plus className="w-4 h-4 text-blue-400" /> Registrar nuevo usuario
                      </button>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Barra de Navegacion por Pestanas */}
          <div className="max-w-7xl mx-auto mt-2.5 flex items-center gap-1 overflow-x-auto pb-1 scrollbar-none">
            <button
              type="button"
              onClick={() => setVistaActiva("catalogo")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                vistaActiva === "catalogo" ? "bg-blue-600 text-white shadow-sm" : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              <Search className="w-3.5 h-3.5" /> Catálogo
            </button>
            <button
              type="button"
              onClick={() => setVistaActiva("matrices")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                vistaActiva === "matrices" ? "bg-blue-600 text-white shadow-sm" : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              <TrendingUp className="w-3.5 h-3.5 text-blue-400" /> Facturación y Métricas
            </button>
            <button
              type="button"
              onClick={() => setVistaActiva("subalgoritmos")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                vistaActiva === "subalgoritmos" ? "bg-blue-600 text-white shadow-sm" : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              <Code2 className="w-3.5 h-3.5 text-amber-400" /> Subalgoritmos (Guía 10)
            </button>
            <button
              type="button"
              onClick={() => setVistaActiva("contratos")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                vistaActiva === "contratos" ? "bg-blue-600 text-white shadow-sm" : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              <CheckCircle2 className="w-3.5 h-3.5" /> Contratos ({contratos.length})
            </button>
            {usuarioActual.rol === "prestador" && (
              <button
                type="button"
                onClick={() => setVistaActiva("publicar")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  vistaActiva === "publicar" ? "bg-blue-600 text-white shadow-sm" : "text-slate-300 hover:bg-slate-800"
                }`}
              >
                <Plus className="w-3.5 h-3.5" /> Publicar Servicio
              </button>
            )}
            {usuarioActual.rol === "admin" && (
              <button
                type="button"
                onClick={() => setVistaActiva("admin")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                  vistaActiva === "admin" ? "bg-blue-600 text-white shadow-sm" : "text-slate-300 hover:bg-slate-800"
                }`}
              >
                <Shield className="w-3.5 h-3.5 text-emerald-400" /> Administración
              </button>
            )}
          </div>
        </header>

        {/* ALERTA / NOTIFICACION FLOTANTE */}
        {notificacion && (
          <div className="bg-emerald-600 text-white text-xs px-4 py-2 text-center font-medium shadow-md flex items-center justify-center gap-2 sticky top-16 z-40">
            <CheckCircle2 className="w-4 h-4" />
            <span>{notificacion}</span>
          </div>
        )}

        {/* CONTENIDO PRINCIPAL SCROLLEABLE */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 max-w-7xl mx-auto w-full">
          {/* ========================================================================= */}
          {/* VISTA 1: CATALOGO DE SERVICIOS                                            */}
          {/* ========================================================================= */}
          {vistaActiva === "catalogo" && (
            <div className="space-y-4">
              {/* Encabezado y Filtros */}
              <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
                  <div>
                    <h2 className="text-lg font-bold text-slate-900">Catálogo de Servicios Profesionales</h2>
                    <p className="text-xs text-slate-500">
                      Encuentra profesionales calificados para tu hogar o empresa • {serviciosFiltrados.length} servicios disponibles
                    </p>
                  </div>
                  {/* Selector de Ordenamiento */}
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500 font-medium flex items-center gap-1">
                      <ArrowUpDown className="w-3.5 h-3.5 text-blue-600" /> Ordenar por:
                    </span>
                    <select
                      value={ordenamiento}
                      onChange={(e: any) => setOrdenamiento(e.target.value)}
                      className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 font-medium text-slate-700 outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="precio_asc">Precio: Menor a Mayor</option>
                      <option value="precio_desc">Precio: Mayor a Menor</option>
                      <option value="rating_desc">Mejor Calificación</option>
                    </select>
                  </div>
                </div>

                {/* Filtros de Busqueda */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                  <div className="relative">
                    <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                    <input
                      type="text"
                      placeholder="Buscar por código, descripción o técnico..."
                      value={filtroTexto}
                      onChange={(e) => setFiltroTexto(e.target.value)}
                      className="w-full pl-9 pr-3 py-2 text-xs bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <select
                      value={filtroCategoria}
                      onChange={(e) => setFiltroCategoria(e.target.value)}
                      className="w-full py-2 px-3 text-xs bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-slate-700"
                    >
                      <option value="todas">Todas las Categorías</option>
                      {CATEGORIAS_SERVICIO.map((cat) => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <select
                      value={filtroCiudad}
                      onChange={(e) => setFiltroCiudad(e.target.value)}
                      className="w-full py-2 px-3 text-xs bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-slate-700"
                    >
                      <option value="todas">Todas las Ciudades</option>
                      {CIUDADES_COBERTURA.map((ciu) => (
                        <option key={ciu} value={ciu}>{ciu}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {/* Tarjetas de Servicios */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {serviciosFiltrados.map((s) => (
                  <div
                    key={s.codigo}
                    className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <span className="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-100 font-mono">
                          {s.codigo}
                        </span>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full flex items-center ${
                          s.disponible ? "bg-emerald-50 text-emerald-700 border border-emerald-200" : "bg-amber-50 text-amber-700 border border-amber-200"
                        }`}>
                          <span className={`w-1.5 h-1.5 rounded-full mr-1.5 ${s.disponible ? "bg-emerald-500" : "bg-amber-500"}`}></span>
                          {s.disponible ? "Disponible" : "Ocupado"}
                        </span>
                      </div>

                      <h3 className="text-sm font-bold text-slate-900 leading-snug">{s.categoria}</h3>
                      <p className="text-xs text-slate-600 font-medium mb-1.5">{s.prestador_nombre}</p>
                      <p className="text-xs text-slate-500 line-clamp-2 mb-3">{s.descripcion}</p>
                    </div>

                    <div className="border-t border-slate-100 pt-3 mt-1">
                      <div className="flex items-center justify-between mb-3 text-xs">
                        <div>
                          <span className="text-[10px] text-slate-400 block">Tarifa por hora:</span>
                          <span className="text-sm font-black text-slate-900">{formatearMoneda(s.tarifa_hora)}</span>
                          <span className="text-[10px] text-slate-400"> + IVA</span>
                        </div>
                        <div className="text-right">
                          <span className="text-[10px] text-slate-400 block">Calificación:</span>
                          <span className="inline-flex items-center gap-1 font-bold text-amber-600 text-xs">
                            <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" /> {s.calificacion.toFixed(1)}
                            <span className="text-[10px] text-slate-400 font-normal">({s.num_contratos})</span>
                          </span>
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={() => {
                          setModalCotizar(s);
                          setHorasCotizar(3);
                        }}
                        disabled={!s.disponible}
                        className={`w-full py-2 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-sm ${
                          s.disponible
                            ? "bg-blue-600 hover:bg-blue-700 text-white cursor-pointer"
                            : "bg-slate-100 text-slate-400 cursor-not-allowed"
                        }`}
                      >
                        <Sparkles className="w-3.5 h-3.5" /> Cotizar y Contratar
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {serviciosFiltrados.length === 0 && (
                <div className="bg-white rounded-2xl p-8 text-center border border-slate-200">
                  <AlertCircle className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                  <p className="text-sm font-semibold text-slate-700">No se encontraron servicios</p>
                  <p className="text-xs text-slate-400">Intente modificando los filtros de búsqueda o categoría.</p>
                </div>
              )}
            </div>
          )}

          {/* ========================================================================= */}
          {/* VISTA 2: FACTURACION Y METRICAS                                           */}
          {/* ========================================================================= */}
          {vistaActiva === "matrices" && (
            <div className="space-y-4">
              {/* Encabezado */}
              <div className="bg-gradient-to-r from-slate-900 to-blue-900 text-white p-5 rounded-2xl shadow-md border border-slate-800">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                  <div>
                    <span className="bg-blue-500/30 text-blue-200 text-[10px] font-bold px-2.5 py-0.5 rounded-full border border-blue-400/30">
                      Métricas Consolidadas
                    </span>
                    <h2 className="text-xl font-black tracking-tight mt-1">Control Financiero y Facturación de Servicios</h2>
                    <p className="text-xs text-slate-300 mt-0.5">
                      Distribución de ingresos por categoría, análisis semanal y cobertura geográfica en tiempo real.
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={sincronizarContratosConMatriz}
                      className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-3 py-2 rounded-xl transition flex items-center gap-1.5 shadow-sm"
                    >
                      <RefreshCw className="w-3.5 h-3.5" /> Sincronizar Contratos
                    </button>
                  </div>
                </div>

                {/* Sub-pestanas */}
                <div className="flex items-center gap-1.5 mt-4 pt-3 border-t border-slate-700/60 overflow-x-auto">
                  <button
                    type="button"
                    onClick={() => setSubTipoMatriz("semanal")}
                    className={`text-xs px-3 py-1.5 rounded-lg font-medium transition whitespace-nowrap ${
                      subTipoMatriz === "semanal" ? "bg-blue-600 text-white shadow-sm" : "bg-slate-800/80 text-slate-300 hover:bg-slate-800"
                    }`}
                  >
                    Facturación Semanal
                  </button>
                  <button
                    type="button"
                    onClick={() => setSubTipoMatriz("ciudades")}
                    className={`text-xs px-3 py-1.5 rounded-lg font-medium transition whitespace-nowrap ${
                      subTipoMatriz === "ciudades" ? "bg-blue-600 text-white shadow-sm" : "bg-slate-800/80 text-slate-300 hover:bg-slate-800"
                    }`}
                  >
                    Demanda por Ciudad
                  </button>
                  <button
                    type="button"
                    onClick={() => setSubTipoMatriz("ejercicio")}
                    className={`text-xs px-3 py-1.5 rounded-lg font-medium transition whitespace-nowrap ${
                      subTipoMatriz === "ejercicio" ? "bg-blue-600 text-white shadow-sm" : "bg-slate-800/80 text-slate-300 hover:bg-slate-800"
                    }`}
                  >
                    Simulación de Rendimiento
                  </button>
                  <button
                    type="button"
                    onClick={() => setSubTipoMatriz("especiales")}
                    className={`text-xs px-3 py-1.5 rounded-lg font-medium transition whitespace-nowrap ${
                      subTipoMatriz === "especiales" ? "bg-blue-600 text-white shadow-sm" : "bg-slate-800/80 text-slate-300 hover:bg-slate-800"
                    }`}
                  >
                    Estructuras de Análisis
                  </button>
                </div>
              </div>

              {/* 1. FACTURACION SEMANAL */}
              {subTipoMatriz === "semanal" && (
                <div className="space-y-4">
                  {/* Tarjetas KPI */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wide block">Total Facturado</span>
                      <p className="text-base font-black text-blue-600 mt-1">{formatearMoneda(statsMatrizSemanal.totalGen)}</p>
                      <span className="text-[10px] text-slate-400">Facturación acumulada</span>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wide block">Promedio por Registro</span>
                      <p className="text-base font-black text-emerald-600 mt-1">{formatearMoneda(statsMatrizSemanal.promedio)}</p>
                      <span className="text-[10px] text-slate-400">Media por categoría y día</span>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wide block">Categoría Líder</span>
                      <p className="text-base font-black text-amber-600 mt-1">{statsMatrizSemanal.catLider}</p>
                      <span className="text-[10px] text-slate-400">{formatearMoneda(statsMatrizSemanal.catLiderTotal)}</span>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wide block">Día de Mayor Actividad</span>
                      <p className="text-base font-black text-purple-600 mt-1">{statsMatrizSemanal.diaLider}</p>
                      <span className="text-[10px] text-slate-400">{formatearMoneda(statsMatrizSemanal.diaLiderTotal)}</span>
                    </div>
                  </div>

                  {/* Tabla Tabular */}
                  <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-900">Ingresos Semanales por Categoría de Servicio</h3>
                        <p className="text-xs text-slate-500">Haz clic en cualquier celda para actualizar el valor inmediatamente.</p>
                      </div>
                      <span className="text-[10px] bg-slate-100 text-slate-600 font-semibold px-2 py-1 rounded border border-slate-200">
                        5 Categorías × 6 Días
                      </span>
                    </div>

                    <div className="overflow-x-auto">
                      <table className="w-full text-xs text-left border-collapse">
                        <thead>
                          <tr className="bg-slate-900 text-white font-semibold">
                            <th className="py-2.5 px-3 rounded-tl-xl">Categoría</th>
                            {DIAS_SEMANA_MATRIZ.map(dia => (
                              <th key={dia} className="py-2.5 px-3 text-right">{dia}</th>
                            ))}
                            <th className="py-2.5 px-3 text-right bg-blue-800 rounded-tr-xl">Total Categoría</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          {matrizSemanal.map((fila, i) => {
                            const totFila = statsMatrizSemanal.totalesFila[i];
                            return (
                              <tr key={CATEGORIAS_SERVICIO[i]} className="hover:bg-slate-50 transition">
                                <td className="py-2.5 px-3 font-bold text-slate-800 bg-slate-50/50">
                                  {CATEGORIAS_SERVICIO[i]}
                                </td>
                                {fila.map((valor, j) => (
                                  <td
                                    key={j}
                                    onClick={() => {
                                      setModalEditarCelda({ fila: i, col: j, valor, tipo: "semanal" });
                                      setNuevoValorCelda(valor.toString());
                                    }}
                                    className="py-2.5 px-3 text-right font-medium cursor-pointer hover:bg-blue-50 text-slate-700 hover:text-blue-700 transition group"
                                  >
                                    <div className="flex items-center justify-end gap-1">
                                      <span>{formatearMoneda(valor)}</span>
                                      <Edit3 className="w-2.5 h-2.5 text-blue-400 opacity-0 group-hover:opacity-100" />
                                    </div>
                                  </td>
                                ))}
                                <td className="py-2.5 px-3 text-right font-black text-blue-900 bg-blue-50/60">
                                  {formatearMoneda(totFila)}
                                </td>
                              </tr>
                            );
                          })}
                          <tr className="bg-slate-100 font-black text-slate-900 border-t-2 border-slate-300">
                            <td className="py-2.5 px-3 font-black rounded-bl-xl">TOTAL DÍA</td>
                            {statsMatrizSemanal.totalesCol.map((totCol, idx) => (
                              <td key={idx} className="py-2.5 px-3 text-right text-emerald-800">
                                {formatearMoneda(totCol)}
                              </td>
                            ))}
                            <td className="py-2.5 px-3 text-right bg-blue-900 text-white rounded-br-xl">
                              {formatearMoneda(statsMatrizSemanal.totalGen)}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <div className="mt-3 p-3 bg-slate-50 rounded-xl border border-slate-200 text-[11px] text-slate-600 flex items-start gap-2">
                      <Info className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" />
                      <div>
                        <strong className="text-slate-800">Panel de control interactivo:</strong>
                        <p>Los totales horizontales y verticales se recalculan dinámicamente en tiempo real al editar cualquier celda.</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 2. DEMANDA POR CIUDAD */}
              {subTipoMatriz === "ciudades" && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wide block">Estructura</span>
                      <p className="text-base font-black text-blue-600 mt-1">Matriz Balanceada (5 × 5)</p>
                      <span className="text-[10px] text-slate-400">Igual número de filas y columnas</span>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wide block">Ciudad Líder</span>
                      <p className="text-base font-black text-purple-600 mt-1">{statsMatrizCiudades.ciuLider}</p>
                      <span className="text-[10px] text-slate-400">Mayor volumen de demanda</span>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wide block">Total Nacional</span>
                      <p className="text-base font-black text-emerald-600 mt-1">{formatearMoneda(statsMatrizCiudades.totalGen)}</p>
                      <span className="text-[10px] text-slate-400">Consolidado 5 ciudades</span>
                    </div>
                  </div>

                  {/* Tabla 5x5 */}
                  <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-900">Demanda Consolidada por Ciudad</h3>
                        <p className="text-xs text-slate-500">Las celdas resaltadas en azul forman la diagonal principal de asignación directa.</p>
                      </div>
                      <span className="text-[10px] bg-purple-50 text-purple-700 font-bold px-2 py-1 rounded border border-purple-200">
                        5 Ciudades Principales
                      </span>
                    </div>

                    <div className="overflow-x-auto">
                      <table className="w-full text-xs text-left border-collapse">
                        <thead>
                          <tr className="bg-slate-900 text-white font-semibold">
                            <th className="py-2.5 px-3 rounded-tl-xl">Categoría</th>
                            {CIUDADES_COBERTURA.map(c => (
                              <th key={c} className="py-2.5 px-3 text-right">{c}</th>
                            ))}
                            <th className="py-2.5 px-3 text-right bg-blue-800 rounded-tr-xl">Total Categoría</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          {matrizCiudades.map((fila, i) => (
                            <tr key={CATEGORIAS_SERVICIO[i]} className="hover:bg-slate-50 transition">
                              <td className="py-2.5 px-3 font-bold text-slate-800 bg-slate-50/50">
                                {CATEGORIAS_SERVICIO[i]}
                              </td>
                              {fila.map((valor, j) => {
                                const esDiagonal = i === j;
                                return (
                                  <td
                                    key={j}
                                    onClick={() => {
                                      setModalEditarCelda({ fila: i, col: j, valor, tipo: "ciudades" });
                                      setNuevoValorCelda(valor.toString());
                                    }}
                                    className={`py-2.5 px-3 text-right font-medium cursor-pointer transition ${
                                      esDiagonal ? "bg-blue-100 font-bold text-blue-900 border border-blue-200" : "text-slate-700 hover:bg-slate-100"
                                    }`}
                                  >
                                    {formatearMoneda(valor)}
                                  </td>
                                );
                              })}
                              <td className="py-2.5 px-3 text-right font-black text-blue-900 bg-blue-50/60">
                                {formatearMoneda(statsMatrizCiudades.totalesFila[i])}
                              </td>
                            </tr>
                          ))}
                          <tr className="bg-slate-100 font-black text-slate-900 border-t-2 border-slate-300">
                            <td className="py-2.5 px-3 rounded-bl-xl">TOTAL CIUDAD</td>
                            {statsMatrizCiudades.totalesCol.map((tot, idx) => (
                              <td key={idx} className="py-2.5 px-3 text-right text-purple-800">{formatearMoneda(tot)}</td>
                            ))}
                            <td className="py-2.5 px-3 text-right bg-blue-900 text-white rounded-br-xl">
                              {formatearMoneda(statsMatrizCiudades.totalGen)}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {/* 3. SIMULACION DE RENDIMIENTO */}
              {subTipoMatriz === "ejercicio" && (
                <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-4">
                  <div className="border-b border-slate-100 pb-3">
                    <span className="text-[10px] bg-blue-100 text-blue-800 font-bold px-2.5 py-0.5 rounded-full">
                      Simulación de Rendimiento
                    </span>
                    <h3 className="text-base font-bold text-slate-900 mt-1">
                      Simulación de Ventas por Producto y Día
                    </h3>
                    <p className="text-xs text-slate-500">
                      Proyección estimada de ingresos por línea de servicio durante tres jornadas consecutivas.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Tabla de Resultados */}
                    <div className="border border-slate-200 rounded-xl overflow-hidden">
                      <table className="w-full text-xs text-left">
                        <thead>
                          <tr className="bg-slate-900 text-white">
                            <th className="py-2.5 px-3">Producto</th>
                            <th className="py-2.5 px-3 text-right">Lunes</th>
                            <th className="py-2.5 px-3 text-right">Martes</th>
                            <th className="py-2.5 px-3 text-right">Miércoles</th>
                            <th className="py-2.5 px-3 text-right bg-blue-700">Total</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          <tr>
                            <td className="py-2 px-3 font-semibold text-slate-800">Producto A</td>
                            <td className="py-2 px-3 text-right">$150,000</td>
                            <td className="py-2 px-3 text-right">$200,000</td>
                            <td className="py-2 px-3 text-right">$180,000</td>
                            <td className="py-2 px-3 text-right font-bold text-blue-800 bg-blue-50">$530,000</td>
                          </tr>
                          <tr>
                            <td className="py-2 px-3 font-semibold text-slate-800">Producto B</td>
                            <td className="py-2 px-3 text-right">$120,000</td>
                            <td className="py-2 px-3 text-right">$250,000</td>
                            <td className="py-2 px-3 text-right">$300,000</td>
                            <td className="py-2 px-3 text-right font-bold text-blue-800 bg-blue-50">$670,000</td>
                          </tr>
                          <tr>
                            <td className="py-2 px-3 font-semibold text-slate-800">Producto C</td>
                            <td className="py-2 px-3 text-right">$175,000</td>
                            <td className="py-2 px-3 text-right">$190,000</td>
                            <td className="py-2 px-3 text-right">$220,000</td>
                            <td className="py-2 px-3 text-right font-bold text-blue-800 bg-blue-50">$585,000</td>
                          </tr>
                          <tr className="bg-slate-100 font-bold">
                            <td className="py-2 px-3">TOTAL DÍA</td>
                            <td className="py-2 px-3 text-right text-emerald-700">$445,000</td>
                            <td className="py-2 px-3 text-right text-emerald-700">$640,000</td>
                            <td className="py-2 px-3 text-right text-emerald-700">$700,000</td>
                            <td className="py-2 px-3 text-right bg-blue-900 text-white">$1,785,000</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    {/* Resumen de Metricas */}
                    <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2.5 text-xs">
                      <h4 className="font-bold text-slate-800 border-b border-slate-200 pb-1.5 flex items-center gap-1.5">
                        <Code2 className="w-4 h-4 text-blue-600" /> Resultados Consolidados
                      </h4>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Facturación General:</span>
                        <strong className="text-slate-900">$1,785,000.00 COP</strong>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Total de Registros:</span>
                        <strong className="text-slate-900">9 celdas procesadas</strong>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-100">
                        <span className="text-slate-500">Promedio por Registro:</span>
                        <strong className="text-emerald-700">$198,333.33 COP</strong>
                      </div>
                      <div className="flex justify-between py-1">
                        <span className="text-slate-500">Producto con Mayor Facturación:</span>
                        <strong className="text-blue-700">Producto B ($670,000 COP)</strong>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 4. ESTRUCTURAS DE ANALISIS */}
              {subTipoMatriz === "especiales" && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Cuadrada */}
                  <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                    <span className="text-[10px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded-full border border-blue-200">
                      Estructura Balanceada
                    </span>
                    <h3 className="text-sm font-bold text-slate-900">Matriz Cuadrada (5x5)</h3>
                    <p className="text-xs text-slate-500">
                      Mismo número de filas y columnas para análisis simétrico entre categorías y ciudades.
                    </p>
                    <div className="bg-slate-900 text-blue-300 font-mono text-[11px] p-3 rounded-xl">
                      <p># Dimensiones 5x5</p>
                      <p>filas = 5  # Categorías</p>
                      <p>columnas = 5  # Ciudades</p>
                    </div>
                  </div>

                  {/* Nula */}
                  <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                    <span className="text-[10px] bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded-full border border-emerald-200">
                      Estado Inicial
                    </span>
                    <h3 className="text-sm font-bold text-slate-900">Inicialización Base (Ceros)</h3>
                    <p className="text-xs text-slate-500">
                      Estructura inicial donde todas las celdas comienzan en cero antes de procesar ventas.
                    </p>
                    <div className="bg-slate-900 text-emerald-300 font-mono text-[11px] p-3 rounded-xl">
                      <p># Matriz nula</p>
                      <p>base = [[0.0 for _ in cols]</p>
                      <p>        for _ in filas]</p>
                    </div>
                  </div>

                  {/* Identidad */}
                  <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                    <span className="text-[10px] bg-purple-50 text-purple-700 font-bold px-2 py-0.5 rounded-full border border-purple-200">
                      Asignación Unitaria
                    </span>
                    <h3 className="text-sm font-bold text-slate-900">Asignación Unitaria (Diagonal)</h3>
                    <p className="text-xs text-slate-500">
                      Contiene valor unitario (1) en la diagonal principal y cero (0) en las demás posiciones.
                    </p>
                    <div className="bg-slate-900 text-purple-300 font-mono text-[11px] p-3 rounded-xl">
                      <p># Diagonal principal</p>
                      <p>identidad = 1 if i == j else 0</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ========================================================================= */}
          {/* VISTA GUÍA 10: SUBALGORITMOS EN PYTHON (FUNCIONES, PROCEDIMIENTOS, LAMBDAS)*/}
          {/* ========================================================================= */}
          {vistaActiva === "subalgoritmos" && (
            <div className="space-y-4">
              {/* Encabezado */}
              <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs bg-amber-100 text-amber-800 font-bold px-2 py-0.5 rounded-full border border-amber-200">
                      Guía de Aprendizaje N.º 10
                    </span>
                    <h2 className="text-lg font-bold text-slate-900">
                      Subalgoritmos en Python: Funciones, Procedimientos y Modularización
                    </h2>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    Funciones puras con retorno (return), procedimientos de presentación, expresiones lambda, modularización y análisis de paso de argumentos.
                  </p>
                </div>

                {/* Sub-tabs */}
                <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl overflow-x-auto scrollbar-none">
                  <button
                    type="button"
                    onClick={() => setSubG10Tab("funciones")}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                      subG10Tab === "funciones" ? "bg-white text-blue-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    1. Funciones (return)
                  </button>
                  <button
                    type="button"
                    onClick={() => setSubG10Tab("procedimientos")}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                      subG10Tab === "procedimientos" ? "bg-white text-blue-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    2. Procedimientos
                  </button>
                  <button
                    type="button"
                    onClick={() => setSubG10Tab("lambdas")}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                      subG10Tab === "lambdas" ? "bg-white text-blue-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    3. Lambdas
                  </button>
                  <button
                    type="button"
                    onClick={() => setSubG10Tab("argumentos")}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                      subG10Tab === "argumentos" ? "bg-white text-blue-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    4. Argumentos
                  </button>
                  <button
                    type="button"
                    onClick={() => setSubG10Tab("inventario")}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                      subG10Tab === "inventario" ? "bg-white text-blue-600 shadow-sm" : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    5. Inventario (Secc. 2)
                  </button>
                </div>
              </div>

              {/* ---------------- PESTAÑA 1: FUNCIONES CON RETURN ---------------- */}
              {subG10Tab === "funciones" && (() => {
                const liq = calcularLiquidacionContrato(subG10Tarifa, subG10Horas, subG10Descuento);
                const com = calcularComisionPlataforma(liq.totalPagar);
                const nuevoRating = calcularPromedioRating(subG10RatingPrev, subG10RatingN, subG10RatingNueva);

                return (
                  <div className="space-y-4">
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                      <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
                        <div>
                          <h3 className="text-sm font-bold text-slate-900">
                            Función 1: calcular_liquidacion_contrato(tarifa, horas, descuento, tasa_iva)
                          </h3>
                          <p className="text-xs text-slate-500">
                            Recibe parámetros numéricos, valida límites y retorna un diccionario estructurado mediante return.
                          </p>
                        </div>
                        <span className="text-[11px] font-mono bg-blue-50 text-blue-700 px-2.5 py-1 rounded-lg border border-blue-200">
                          return dict
                        </span>
                      </div>

                      {/* Formulario Reactivo */}
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                          <label className="text-xs font-semibold text-slate-600 block mb-1">
                            Tarifa por Hora ($ COP)
                          </label>
                          <input
                            type="number"
                            min="1000"
                            step="5000"
                            value={subG10Tarifa}
                            onChange={(e) => setSubG10Tarifa(Math.max(0, Number(e.target.value)))}
                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-slate-600 block mb-1">
                            Horas Contratadas
                          </label>
                          <input
                            type="number"
                            min="1"
                            max="100"
                            value={subG10Horas}
                            onChange={(e) => setSubG10Horas(Math.max(1, Number(e.target.value)))}
                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-slate-600 block mb-1">
                            Descuento Promocional (%)
                          </label>
                          <input
                            type="number"
                            min="0"
                            max="100"
                            value={subG10Descuento}
                            onChange={(e) => setSubG10Descuento(Math.max(0, Math.min(100, Number(e.target.value))))}
                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                          />
                        </div>
                      </div>

                      {/* Tarjetas de Desglose Financiero */}
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
                        <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                          <span className="text-[10px] text-slate-500 block">Subtotal Bruto</span>
                          <span className="text-sm font-bold text-slate-900">{formatearMoneda(liq.subtotalBruto)}</span>
                        </div>
                        <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                          <span className="text-[10px] text-slate-500 block">Descuento ({subG10Descuento}%)</span>
                          <span className="text-sm font-bold text-rose-600">- {formatearMoneda(liq.montoDescuento)}</span>
                        </div>
                        <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                          <span className="text-[10px] text-slate-500 block">IVA Liquidado (19%)</span>
                          <span className="text-sm font-bold text-slate-900">+ {formatearMoneda(liq.montoIva)}</span>
                        </div>
                        <div className="bg-blue-50 p-3 rounded-xl border border-blue-200">
                          <span className="text-[10px] text-blue-700 font-bold block">Total a Pagar</span>
                          <span className="text-sm font-extrabold text-blue-700">{formatearMoneda(liq.totalPagar)}</span>
                        </div>
                      </div>

                      {/* Función 2: Comisión de Plataforma */}
                      <div className="bg-emerald-50/60 p-4 rounded-xl border border-emerald-200 space-y-2">
                        <div className="flex items-center justify-between">
                          <h4 className="text-xs font-bold text-emerald-900">
                            Función 2: calcular_comision_plataforma(total_pagar)
                          </h4>
                          <span className="text-[10px] font-mono bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-bold">
                            Distribución YPRI
                          </span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
                          <div>
                            <span className="text-[10px] text-emerald-700 block">Comisión Plataforma (10%)</span>
                            <span className="text-xs font-bold text-emerald-900">{formatearMoneda(com.comisionYpri)}</span>
                          </div>
                          <div>
                            <span className="text-[10px] text-emerald-700 block">Retención Fuente (4%)</span>
                            <span className="text-xs font-bold text-emerald-900">{formatearMoneda(com.retencionFuente)}</span>
                          </div>
                          <div>
                            <span className="text-[10px] text-emerald-700 font-bold block">Pago Neto Prestador</span>
                            <span className="text-xs font-extrabold text-emerald-800">{formatearMoneda(com.pagoNetoPrestador)}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Función 3: Recálculo Ponderado de Calificación */}
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                      <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                        <div>
                          <h3 className="text-sm font-bold text-slate-900">
                            Función 3: calcular_promedio_calificacion(rating_previo, num_evaluaciones, nueva_nota)
                          </h3>
                          <p className="text-xs text-slate-500">
                            Fórmula de actualización incremental de la media aritmética ponderada.
                          </p>
                        </div>
                        <span className="text-[11px] font-mono bg-purple-50 text-purple-700 px-2.5 py-1 rounded-lg border border-purple-200">
                          return float
                        </span>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 items-center">
                        <div>
                          <label className="text-xs font-semibold text-slate-600 block mb-1">Rating Actual</label>
                          <input
                            type="number"
                            step="0.1"
                            min="1.0"
                            max="5.0"
                            value={subG10RatingPrev}
                            onChange={(e) => setSubG10RatingPrev(Number(e.target.value))}
                            className="w-full text-xs p-2 border border-slate-200 rounded-xl outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-slate-600 block mb-1">Total Reseñas (N)</label>
                          <input
                            type="number"
                            min="1"
                            value={subG10RatingN}
                            onChange={(e) => setSubG10RatingN(Math.max(1, Number(e.target.value)))}
                            className="w-full text-xs p-2 border border-slate-200 rounded-xl outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-slate-600 block mb-1">Nueva Nota (1-5)</label>
                          <input
                            type="number"
                            step="0.1"
                            min="1.0"
                            max="5.0"
                            value={subG10RatingNueva}
                            onChange={(e) => setSubG10RatingNueva(Number(e.target.value))}
                            className="w-full text-xs p-2 border border-slate-200 rounded-xl outline-none"
                          />
                        </div>
                        <div className="bg-purple-50 p-2.5 rounded-xl border border-purple-200 text-center">
                          <span className="text-[10px] text-purple-700 font-bold block">Nuevo Rating Ponderado</span>
                          <span className="text-base font-extrabold text-purple-900">★ {nuevoRating} / 5.0</span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })()}

              {/* ---------------- PESTAÑA 2: PROCEDIMIENTOS ---------------- */}
              {subG10Tab === "procedimientos" && (() => {
                const servActual = servicios.find((s) => s.codigo === subG10ServicioSel) || servicios[0];
                const liq = calcularLiquidacionContrato(servActual.tarifa_hora, 4, 10);

                return (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {/* Procedimiento 1: Ficha Técnica */}
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                      <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                        <div className="flex items-center gap-2">
                          <Award className="w-4 h-4 text-blue-600" />
                          <h3 className="text-sm font-bold text-slate-900">
                            Procedimiento 1: mostrar_ficha_tecnica_servicio()
                          </h3>
                        </div>
                        <span className="text-[10px] font-mono bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md">
                          void (sin return)
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <label className="text-xs font-semibold text-slate-600">Servicio:</label>
                        <select
                          value={subG10ServicioSel}
                          onChange={(e) => setSubG10ServicioSel(e.target.value)}
                          className="text-xs p-2 border border-slate-200 rounded-xl flex-1 outline-none font-medium"
                        >
                          {servicios.map((s) => (
                            <option key={s.codigo} value={s.codigo}>
                              {s.codigo} — {s.categoria} ({s.prestador_nombre} • {s.ciudad})
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* Tarjeta Visual de Ficha Técnica */}
                      <div className="bg-slate-900 text-slate-100 p-4 rounded-xl font-mono text-xs space-y-1.5 border border-slate-800">
                        <div className="text-amber-400 font-bold border-b border-slate-700 pb-1">
                          ------------------ FICHA TÉCNICA FORMAL ------------------
                        </div>
                        <div><span className="text-slate-400">Código:</span> {servActual.codigo}</div>
                        <div><span className="text-slate-400">Categoría:</span> {servActual.categoria}</div>
                        <div><span className="text-slate-400">Prestador:</span> {servActual.prestador_nombre}</div>
                        <div><span className="text-slate-400">Ciudad:</span> {servActual.ciudad}</div>
                        <div><span className="text-slate-400">Tarifa Horaria:</span> {formatearMoneda(servActual.tarifa_hora)}/h</div>
                        <div><span className="text-slate-400">Calificación:</span> ★ {servActual.calificacion} / 5.0 ({servActual.num_contratos} servicios)</div>
                        <div><span className="text-slate-400">Experiencia:</span> {servActual.anios_experiencia} año(s)</div>
                        <div><span className="text-slate-400">Disponibilidad:</span> {servActual.disponible ? "Inmediata (Activo)" : "Ocupado"}</div>
                        <div><span className="text-slate-400">Descripción:</span> {servActual.descripcion}</div>
                        <div className="text-slate-500 pt-1">----------------------------------------------------------</div>
                      </div>
                    </div>

                    {/* Procedimiento 2: Recibo de Liquidación */}
                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                      <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                        <div className="flex items-center gap-2">
                          <DollarSign className="w-4 h-4 text-emerald-600" />
                          <h3 className="text-sm font-bold text-slate-900">
                            Procedimiento 2: mostrar_recibo_liquidacion()
                          </h3>
                        </div>
                        <span className="text-[10px] font-mono bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md">
                          void (sin return)
                        </span>
                      </div>

                      <p className="text-xs text-slate-500">
                        Formatea y presenta en pantalla la factura final para el cliente y los registros de auditoría.
                      </p>

                      <div className="bg-slate-900 text-slate-100 p-4 rounded-xl font-mono text-xs space-y-1.5 border border-slate-800">
                        <div className="text-emerald-400 font-bold border-b border-slate-700 pb-1 text-center">
                          === RECIBO DE COTIZACIÓN Y LIQUIDACIÓN — YPRI ===
                        </div>
                        <div><span className="text-slate-400">Servicio:</span> {servActual.codigo} - {servActual.categoria}</div>
                        <div><span className="text-slate-400">Prestador:</span> {servActual.prestador_nombre}</div>
                        <div><span className="text-slate-400">Horas:</span> {liq.horas} hora(s) @ {formatearMoneda(liq.tarifaHora)}</div>
                        <div className="border-t border-slate-800 pt-1">
                          <span className="text-slate-400">Subtotal Bruto:</span> {formatearMoneda(liq.subtotalBruto)}
                        </div>
                        <div className="text-rose-400">
                          <span className="text-slate-400">Descuento ({liq.descuentoPct}%):</span> - {formatearMoneda(liq.montoDescuento)}
                        </div>
                        <div>
                          <span className="text-slate-400">Subtotal Neto:</span> {formatearMoneda(liq.subtotalNeto)}
                        </div>
                        <div className="text-cyan-400">
                          <span className="text-slate-400">IVA (19%):</span> + {formatearMoneda(liq.montoIva)}
                        </div>
                        <div className="border-t border-slate-700 pt-1 text-emerald-300 font-bold text-sm">
                          TOTAL A PAGAR: {formatearMoneda(liq.totalPagar)}
                        </div>
                        <div className="text-center text-slate-500 text-[10px] pt-1">
                          ================================================
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })()}

              {/* ---------------- PESTAÑA 3: FUNCIONES LAMBDA ---------------- */}
              {subG10Tab === "lambdas" && (
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                    <div>
                      <h3 className="text-sm font-bold text-slate-900">
                        Funciones Lambda: Operaciones Breves y Criterios de Ordenamiento
                      </h3>
                      <p className="text-xs text-slate-500">
                        sorted(servicios, key=lambda s: s[&apos;tarifa_hora&apos;]) y sorted(servicios, key=lambda s: s[&apos;calificacion&apos;], reverse=True)
                      </p>
                    </div>
                    <span className="text-xs bg-amber-50 text-amber-800 font-bold px-2.5 py-1 rounded-lg border border-amber-200">
                      lambda arg: expr
                    </span>
                  </div>

                  {/* Tabla con Filtros Lambda */}
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px]">
                        <tr>
                          <th className="p-2.5 rounded-l-lg">Código</th>
                          <th className="p-2.5">Prestador</th>
                          <th className="p-2.5">Categoría</th>
                          <th className="p-2.5">Ciudad</th>
                          <th className="p-2.5 text-right">Tarifa Horaria</th>
                          <th className="p-2.5 text-center rounded-r-lg">Rating</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {[...servicios]
                          .sort((a, b) => b.tarifa_hora - a.tarifa_hora)
                          .map((s) => (
                            <tr key={s.codigo} className="hover:bg-slate-50/80 transition">
                              <td className="p-2.5 font-mono font-bold text-blue-600">{s.codigo}</td>
                              <td className="p-2.5 font-medium text-slate-900">{s.prestador_nombre}</td>
                              <td className="p-2.5 text-slate-600">{s.categoria}</td>
                              <td className="p-2.5 text-slate-600">{s.ciudad}</td>
                              <td className="p-2.5 text-right font-semibold text-slate-900">{formatearMoneda(s.tarifa_hora)}</td>
                              <td className="p-2.5 text-center">
                                <span className="bg-amber-50 text-amber-700 font-bold px-2 py-0.5 rounded-full text-[11px] border border-amber-200">
                                  ★ {s.calificacion}
                                </span>
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* ---------------- PESTAÑA 4: VARIABLES & ARGUMENTOS ---------------- */}
              {subG10Tab === "argumentos" && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Inmutables */}
                  <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                    <span className="text-[10px] bg-sky-100 text-sky-800 font-bold px-2 py-0.5 rounded-full">
                      Objetos Inmutables (int, float, str, tuple)
                    </span>
                    <h3 className="text-sm font-bold text-slate-900">
                      Paso de Parámetros: Simulación de Paso por Valor
                    </h3>
                    <p className="text-xs text-slate-500">
                      Al reasignar un número o cadena dentro de una función, la variable externa en el llamador jamás sufre modificaciones.
                    </p>

                    <div className="bg-slate-900 text-slate-100 p-3.5 rounded-xl font-mono text-xs space-y-1">
                      <p className="text-sky-400 font-bold">def modificar_numero(numero):</p>
                      <p className="pl-4">numero = numero + 10000</p>
                      <p className="pl-4">return numero</p>
                      <p className="text-slate-400 pt-1">tarifa = 50000</p>
                      <p className="text-slate-400">modificar_numero(tarifa) # Retorna 60000</p>
                      <p className="text-emerald-400 font-bold">print(tarifa) # Imprime 50000 (INALTERADO)</p>
                    </div>
                  </div>

                  {/* Mutables */}
                  <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                    <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full">
                      Objetos Mutables (list, dict, set)
                    </span>
                    <h3 className="text-sm font-bold text-slate-900">
                      Paso de Parámetros: Comportamiento por Referencia
                    </h3>
                    <p className="text-xs text-slate-500">
                      Las colecciones mutables se modifican directamente in-place mediante métodos como append() o asignación de llaves [clave].
                    </p>

                    <div className="bg-slate-900 text-slate-100 p-3.5 rounded-xl font-mono text-xs space-y-1">
                      <p className="text-emerald-400 font-bold">def agregar_servicio(servicios):</p>
                      <p className="pl-4">servicios.append(&quot;Climatización&quot;)</p>
                      <p className="text-slate-400 pt-1">inventario = [&quot;Electricidad&quot;, &quot;Plomería&quot;]</p>
                      <p className="text-slate-400">agregar_servicio(inventario)</p>
                      <p className="text-emerald-400 font-bold">print(inventario) # [&apos;Electricidad&apos;, &apos;Plomería&apos;, &apos;Climatización&apos;]</p>
                    </div>

                    <div className="flex items-center gap-2 pt-2">
                      <button
                        type="button"
                        onClick={() => setDemoLista([...demoLista, `Servicio ${demoLista.length + 1}`])}
                        className="text-xs bg-emerald-600 text-white font-semibold px-3 py-1.5 rounded-lg hover:bg-emerald-700 transition"
                      >
                        Mutar Lista in-place (.append)
                      </button>
                      <span className="text-xs text-slate-600 font-mono">
                        Elementos: {demoLista.length} [{demoLista.join(", ")}]
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* ---------------- PESTAÑA 5: INVENTARIO GUIADO (SECCIÓN 2) ---------------- */}
              {subG10Tab === "inventario" && (() => {
                const totalInv = calcularTotalInventario(subG10Inventario);

                const agregarProducto = (e: React.FormEvent) => {
                  e.preventDefault();
                  if (!invCod.trim() || !invNom.trim()) {
                    alert("Código y nombre son requeridos.");
                    return;
                  }
                  if (subG10Inventario.some((p) => p.codigo.toLowerCase() === invCod.trim().toLowerCase())) {
                    alert("El código ya existe.");
                    return;
                  }
                  const pre = parseFloat(invPre);
                  const can = parseInt(invCan);
                  if (isNaN(pre) || isNaN(can) || pre < 0 || can < 0) {
                    alert("Valores numéricos no válidos o negativos.");
                    return;
                  }
                  setSubG10Inventario([...subG10Inventario, { codigo: invCod.trim(), nombre: invNom.trim(), precio: pre, cantidad: can }]);
                  setInvCod("");
                  setInvNom("");
                  setInvPre("");
                  setInvCan("");
                };

                const ordenarPorPrecio = () => {
                  const ord = [...subG10Inventario].sort((a, b) => a.precio - b.precio);
                  setSubG10Inventario(ord);
                };

                return (
                  <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                      <div>
                        <h3 className="text-sm font-bold text-slate-900">
                          Sección 2 de la Guía: Sistema de Inventario con Subalgoritmos
                        </h3>
                        <p className="text-xs text-slate-500">
                          Implementación del ejercicio guiado con registro, cálculo de subtotal, ordenamiento lambda y total general.
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={ordenarPorPrecio}
                        className="text-xs bg-slate-900 text-white font-semibold px-3 py-1.5 rounded-xl hover:bg-slate-800 transition"
                      >
                        Ordenar por Precio (key=lambda)
                      </button>
                    </div>

                    {/* Formulario */}
                    <form onSubmit={agregarProducto} className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
                      <input
                        type="text"
                        placeholder="Código (ej. P04)"
                        value={invCod}
                        onChange={(e) => setInvCod(e.target.value)}
                        className="text-xs p-2 border border-slate-200 rounded-xl outline-none"
                      />
                      <input
                        type="text"
                        placeholder="Nombre Producto"
                        value={invNom}
                        onChange={(e) => setInvNom(e.target.value)}
                        className="text-xs p-2 border border-slate-200 rounded-xl outline-none"
                      />
                      <input
                        type="number"
                        placeholder="Precio Unitario"
                        value={invPre}
                        onChange={(e) => setInvPre(e.target.value)}
                        className="text-xs p-2 border border-slate-200 rounded-xl outline-none"
                      />
                      <input
                        type="number"
                        placeholder="Cantidad"
                        value={invCan}
                        onChange={(e) => setInvCan(e.target.value)}
                        className="text-xs p-2 border border-slate-200 rounded-xl outline-none"
                      />
                      <button
                        type="submit"
                        className="col-span-2 sm:col-span-1 text-xs bg-blue-600 text-white font-bold p-2 rounded-xl hover:bg-blue-700 transition"
                      >
                        Registrar
                      </button>
                    </form>

                    {/* Tabla de Inventario */}
                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-xs">
                        <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px]">
                          <tr>
                            <th className="p-2.5 rounded-l-lg">Código</th>
                            <th className="p-2.5">Nombre</th>
                            <th className="p-2.5 text-right">Precio Unitario</th>
                            <th className="p-2.5 text-center">Cantidad</th>
                            <th className="p-2.5 text-right rounded-r-lg">Subtotal</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          {subG10Inventario.map((p) => {
                            const sub = calcularSubtotalInventario(p.precio, p.cantidad);
                            return (
                              <tr key={p.codigo} className="hover:bg-slate-50/80 transition">
                                <td className="p-2.5 font-mono font-bold text-blue-600">{p.codigo}</td>
                                <td className="p-2.5 font-medium text-slate-900">{p.nombre}</td>
                                <td className="p-2.5 text-right text-slate-700">{formatearMoneda(p.precio)}</td>
                                <td className="p-2.5 text-center font-bold text-slate-900">{p.cantidad}</td>
                                <td className="p-2.5 text-right font-bold text-emerald-700">{formatearMoneda(sub)}</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>

                    {/* Total Inventario */}
                    <div className="bg-blue-50 p-3.5 rounded-xl border border-blue-200 flex items-center justify-between">
                      <span className="text-xs font-bold text-blue-900">
                        Función calcular_total_inventario(): Suma acumulada de subtotales
                      </span>
                      <span className="text-base font-extrabold text-blue-700">{formatearMoneda(totalInv)}</span>
                    </div>
                  </div>
                );
              })()}
            </div>
          )}
          {/* ========================================================================= */}
          {vistaActiva === "contratos" && (
            <div className="space-y-4">
              <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-bold text-slate-900">Historial y Gestión de Contratos</h2>
                  <p className="text-xs text-slate-500">
                    Cotizaciones calculadas con impuesto al valor agregado (IVA 19%) y ciclo de vida de acuerdos.
                  </p>
                </div>
                <span className="text-xs font-bold bg-blue-50 text-blue-700 px-3 py-1 rounded-full border border-blue-200">
                  {contratos.length} Contratos
                </span>
              </div>

              <div className="space-y-3">
                {contratos.map((c) => (
                  <div key={c.id} className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-3">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-black text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-100 font-mono">
                          {c.id}
                        </span>
                        <h3 className="text-sm font-bold text-slate-900">{c.servicio_nombre}</h3>
                      </div>
                      <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full inline-block text-center ${
                        c.estado === "Completado"
                          ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                          : c.estado === "En proceso"
                          ? "bg-blue-50 text-blue-700 border border-blue-200"
                          : c.estado === "Pendiente"
                          ? "bg-amber-50 text-amber-700 border border-amber-200"
                          : "bg-red-50 text-red-700 border border-red-200"
                      }`}>
                        {c.estado}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs mb-3">
                      <div>
                        <span className="text-[10px] text-slate-400 block">Cliente:</span>
                        <span className="font-semibold text-slate-700">{c.cliente_nombre}</span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-400 block">Horas Contratadas:</span>
                        <span className="font-semibold text-slate-700">{c.horas} horas</span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-400 block">Tarifa Base:</span>
                        <span className="font-semibold text-slate-700">{formatearMoneda(c.tarifa_hora)}/h</span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-400 block">Total con IVA:</span>
                        <span className="font-bold text-slate-900 text-sm text-blue-700">{formatearMoneda(c.total)}</span>
                      </div>
                    </div>

                    {/* Calificacion */}
                    {c.calificacion && (
                      <div className="bg-amber-50 border border-amber-200 rounded-xl p-2.5 text-xs mb-3">
                        <div className="flex items-center gap-1 text-amber-700 font-bold mb-0.5">
                          <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                          <span>Calificación: {c.calificacion.toFixed(1)} / 5.0</span>
                        </div>
                        {c.comentario && <p className="text-slate-600 italic">"{c.comentario}"</p>}
                      </div>
                    )}

                    {/* Acciones */}
                    <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
                      {c.estado === "Pendiente" && (
                        <>
                          <button
                            type="button"
                            onClick={() => cambiarEstadoContrato(c.id, "En proceso")}
                            className="text-xs bg-blue-600 hover:bg-blue-700 text-white font-semibold px-3 py-1.5 rounded-lg transition"
                          >
                            Iniciar Servicio
                          </button>
                          <button
                            type="button"
                            onClick={() => cambiarEstadoContrato(c.id, "Cancelado")}
                            className="text-xs bg-slate-100 hover:bg-red-50 text-red-600 font-semibold px-3 py-1.5 rounded-lg transition"
                          >
                            Cancelar
                          </button>
                        </>
                      )}
                      {c.estado === "En proceso" && (
                        <button
                          type="button"
                          onClick={() => cambiarEstadoContrato(c.id, "Completado")}
                          className="text-xs bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-3 py-1.5 rounded-lg transition flex items-center gap-1"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5" /> Marcar como Completado
                        </button>
                      )}
                      {c.estado === "Completado" && !c.calificacion && (
                        <button
                          type="button"
                          onClick={() => {
                            setModalCalificar(c);
                            setEstrellasCalif(5);
                            setComentarioCalif("");
                          }}
                          className="text-xs bg-amber-500 hover:bg-amber-600 text-white font-semibold px-3 py-1.5 rounded-lg transition flex items-center gap-1"
                        >
                          <Star className="w-3.5 h-3.5" /> Calificar Servicio
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ========================================================================= */}
          {/* VISTA 4: PUBLICAR SERVICIO                                                */}
          {/* ========================================================================= */}
          {vistaActiva === "publicar" && (
            <div className="max-w-2xl mx-auto bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Publicar Nuevo Servicio Profesional</h2>
                <p className="text-xs text-slate-500">
                  Registra un nuevo servicio en la plataforma con disponibilidad inmediata.
                </p>
              </div>

              <form onSubmit={guardarNuevoServicio} className="space-y-3.5 text-xs">
                <div>
                  <label className="block text-slate-700 font-bold mb-1">Categoría del Servicio:</label>
                  <select
                    value={pub_categoria}
                    onChange={(e: any) => setPub_categoria(e.target.value)}
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {CATEGORIAS_SERVICIO.map((cat) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-slate-700 font-bold mb-1">Ciudad de Cobertura:</label>
                  <select
                    value={pub_ciudad}
                    onChange={(e: any) => setPub_ciudad(e.target.value)}
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {CIUDADES_COBERTURA.map((ciu) => (
                      <option key={ciu} value={ciu}>{ciu}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-slate-700 font-bold mb-1">Tarifa por Hora (COP):</label>
                  <input
                    type="number"
                    min="10000"
                    step="5000"
                    value={pub_tarifa}
                    onChange={(e) => setPub_tarifa(e.target.value)}
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-700 font-bold mb-1">Descripción del Servicio:</label>
                  <textarea
                    rows={3}
                    value={pub_desc}
                    onChange={(e) => setPub_desc(e.target.value)}
                    placeholder="Describe detalladamente los trabajos técnicos incluidos..."
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-sm transition"
                >
                  Publicar Servicio en el Catálogo
                </button>
              </form>
            </div>
          )}

          {/* ========================================================================= */}
          {/* VISTA 5: PANEL ADMINISTRADOR                                              */}
          {/* ========================================================================= */}
          {vistaActiva === "admin" && (
            <div className="space-y-4">
              <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-bold text-slate-900">Panel de Control y Auditoría</h2>
                  <p className="text-xs text-slate-500">Métricas globales y control de usuarios registrados.</p>
                </div>
                <span className="bg-slate-900 text-white text-xs font-bold px-3 py-1 rounded-full">
                  Administrador
                </span>
              </div>

              {/* Metricas */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                  <span className="text-[10px] text-slate-400 font-bold uppercase block">Usuarios</span>
                  <p className="text-lg font-black text-slate-900 mt-1">{usuarios.length}</p>
                  <span className="text-[10px] text-blue-600 font-medium">Usuarios registrados</span>
                </div>
                <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                  <span className="text-[10px] text-slate-400 font-bold uppercase block">Servicios</span>
                  <p className="text-lg font-black text-slate-900 mt-1">{servicios.length}</p>
                  <span className="text-[10px] text-emerald-600 font-medium">Servicios activos</span>
                </div>
                <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                  <span className="text-[10px] text-slate-400 font-bold uppercase block">Contratos</span>
                  <p className="text-lg font-black text-slate-900 mt-1">{contratos.length}</p>
                  <span className="text-[10px] text-purple-600 font-medium">Contratos totales</span>
                </div>
                <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                  <span className="text-[10px] text-slate-400 font-bold uppercase block">Facturación</span>
                  <p className="text-lg font-black text-blue-700 mt-1">{formatearMoneda(statsMatrizSemanal.totalGen)}</p>
                  <span className="text-[10px] text-slate-400 font-medium">Facturación semanal</span>
                </div>
              </div>

              {/* Lista de Usuarios */}
              <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm">
                <h3 className="text-sm font-bold text-slate-900 mb-3">Usuarios Registrados en el Sistema</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left">
                    <thead>
                      <tr className="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
                        <th className="py-2 px-3">ID</th>
                        <th className="py-2 px-3">Nombre</th>
                        <th className="py-2 px-3">Correo</th>
                        <th className="py-2 px-3">Rol</th>
                        <th className="py-2 px-3">Ciudad</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {usuarios.map(u => (
                        <tr key={u.id} className="hover:bg-slate-50">
                          <td className="py-2 px-3 font-mono font-bold text-blue-600">{u.id}</td>
                          <td className="py-2 px-3 font-medium text-slate-900">{u.nombre}</td>
                          <td className="py-2 px-3 text-slate-500">{u.correo}</td>
                          <td className="py-2 px-3">
                            <span className="capitalize text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                              {u.rol}
                            </span>
                          </td>
                          <td className="py-2 px-3 text-slate-600">{u.ciudad}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </main>

        {/* ========================================================================= */}
        {/* MODAL 1: COTIZAR SERVICIO (CON IVA 19%)                                   */}
        {/* ========================================================================= */}
        {modalCotizar && (
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setModalCotizar(null)}
          >
            <div
              className="bg-white rounded-3xl max-w-md w-full p-5 shadow-2xl border border-slate-200"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Cotizador de Servicios</h3>
                    <p className="text-[11px] text-slate-500">{modalCotizar.categoria} • {modalCotizar.prestador_nombre}</p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setModalCotizar(null)}
                  className="text-slate-400 hover:text-slate-600 cursor-pointer"
                >
                  <XCircle className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-600 font-bold mb-1">Horas estimadas requeridas:</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="range"
                      min="1"
                      max="20"
                      value={horasCotizar}
                      onChange={(e) => setHorasCotizar(parseInt(e.target.value))}
                      className="flex-1 accent-blue-600"
                    />
                    <span className="font-bold text-slate-900 bg-slate-100 px-3 py-1 rounded-lg border border-slate-200">
                      {horasCotizar} {horasCotizar === 1 ? "hora" : "horas"}
                    </span>
                  </div>
                </div>

                {/* Desglose */}
                <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-200 space-y-2">
                  <div className="flex justify-between text-slate-600">
                    <span>Tarifa horaria:</span>
                    <span>{formatearMoneda(modalCotizar.tarifa_hora)}</span>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>Subtotal ({horasCotizar}h):</span>
                    <span>{formatearMoneda(modalCotizar.tarifa_hora * horasCotizar)}</span>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>Impuesto IVA (19%):</span>
                    <span>{formatearMoneda(modalCotizar.tarifa_hora * horasCotizar * IVA_PORCENTAJE)}</span>
                  </div>
                  <div className="border-t border-slate-200 pt-2 flex justify-between font-bold text-sm text-slate-900">
                    <span>Total a Liquidar:</span>
                    <span className="text-blue-700">
                      {formatearMoneda(modalCotizar.tarifa_hora * horasCotizar * (1 + IVA_PORCENTAJE))}
                    </span>
                  </div>
                </div>

                <div className="pt-2 flex gap-2">
                  <button
                    type="button"
                    onClick={() => setModalCotizar(null)}
                    className="flex-1 py-2.5 rounded-xl border border-slate-200 text-slate-600 font-bold hover:bg-slate-50 transition"
                  >
                    Cancelar
                  </button>
                  <button
                    type="button"
                    onClick={confirmarContrato}
                    className="flex-1 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold transition shadow-sm"
                  >
                    Confirmar Contrato
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* MODAL 2: EDITAR CELDA                                                     */}
        {/* ========================================================================= */}
        {modalEditarCelda && (
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setModalEditarCelda(null)}
          >
            <div
              className="bg-white rounded-3xl max-w-sm w-full p-5 shadow-2xl border border-slate-200"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
                    <Edit3 className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Modificar Valor de Facturación</h3>
                    <p className="text-[11px] text-slate-500">
                      Categoría: {CATEGORIAS_SERVICIO[modalEditarCelda.fila]}
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setModalEditarCelda(null)}
                  className="text-slate-400 hover:text-slate-600"
                >
                  <XCircle className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-600 font-bold mb-1">Nuevo Monto en Pesos ($ COP):</label>
                  <input
                    type="number"
                    min="0"
                    step="10000"
                    value={nuevoValorCelda}
                    onChange={(e) => setNuevoValorCelda(e.target.value)}
                    className="w-full p-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 font-mono font-bold"
                    autoFocus
                  />
                  <span className="text-[10px] text-slate-400 mt-1 block">
                    Ingrese el valor numérico correspondiente sin puntos ni decimales.
                  </span>
                </div>

                <div className="pt-2 flex gap-2">
                  <button
                    type="button"
                    onClick={() => setModalEditarCelda(null)}
                    className="flex-1 py-2 rounded-xl border border-slate-200 text-slate-600 font-bold hover:bg-slate-50"
                  >
                    Cancelar
                  </button>
                  <button
                    type="button"
                    onClick={guardarEdicionCelda}
                    className="flex-1 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold"
                  >
                    Guardar Valor
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* MODAL 3: CALIFICAR SERVICIO                                               */}
        {/* ========================================================================= */}
        {modalCalificar && (
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setModalCalificar(null)}
          >
            <div
              className="bg-white rounded-3xl max-w-sm w-full p-5 shadow-2xl border border-slate-200"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                <h3 className="text-sm font-bold text-slate-900">Calificar Servicio Completado</h3>
                <button
                  type="button"
                  onClick={() => setModalCalificar(null)}
                  className="text-slate-400 hover:text-slate-600"
                >
                  <XCircle className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-3 text-xs text-center">
                <p className="text-slate-600 font-medium">{modalCalificar.servicio_nombre}</p>

                <div className="flex justify-center gap-1.5 py-2">
                  {[1, 2, 3, 4, 5].map((num) => (
                    <button
                      key={num}
                      type="button"
                      onClick={() => setEstrellasCalif(num)}
                      className="p-1 transition transform hover:scale-110"
                    >
                      <Star
                        className={`w-7 h-7 ${
                          num <= estrellasCalif ? "fill-amber-400 text-amber-400" : "text-slate-200"
                        }`}
                      />
                    </button>
                  ))}
                </div>
                <p className="font-bold text-amber-600 text-sm">{estrellasCalif}.0 Puntos</p>

                <textarea
                  rows={3}
                  value={comentarioCalif}
                  onChange={(e) => setComentarioCalif(e.target.value)}
                  placeholder="Escribe tu reseña o comentario..."
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-left"
                />

                <div className="pt-2 flex gap-2">
                  <button
                    type="button"
                    onClick={() => setModalCalificar(null)}
                    className="flex-1 py-2 rounded-xl border border-slate-200 text-slate-600 font-bold"
                  >
                    Cancelar
                  </button>
                  <button
                    type="button"
                    onClick={guardarCalificacion}
                    className="flex-1 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold"
                  >
                    Enviar Calificación
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* MODAL 4: REGISTRAR NUEVO USUARIO (CORREGIDO - FIRME Y FUNCIONAL)           */}
        {/* ========================================================================= */}
        {modalNuevoUsuario && (
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setModalNuevoUsuario(false)}
          >
            <div
              className="bg-white rounded-3xl max-w-sm w-full p-5 shadow-2xl border border-slate-200 relative"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
                    <User className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Registrar Nuevo Usuario</h3>
                    <p className="text-[11px] text-slate-500">Crea una cuenta e inicia sesión al instante</p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setModalNuevoUsuario(false)}
                  className="text-slate-400 hover:text-slate-600 cursor-pointer p-1"
                >
                  <XCircle className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={guardarNuevoUsuario} className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-600 font-bold mb-1">Nombre Completo:</label>
                  <input
                    type="text"
                    value={nuevoU_nombre}
                    onChange={(e) => setNuevoU_nombre(e.target.value)}
                    placeholder="Ej. Laura Gómez"
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
                    required
                    autoFocus
                  />
                </div>
                <div>
                  <label className="block text-slate-600 font-bold mb-1">Correo Electrónico:</label>
                  <input
                    type="email"
                    value={nuevoU_correo}
                    onChange={(e) => setNuevoU_correo(e.target.value)}
                    placeholder="laura@email.com"
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
                    required
                  />
                </div>
                <div>
                  <label className="block text-slate-600 font-bold mb-1">Teléfono:</label>
                  <input
                    type="tel"
                    value={nuevoU_tel}
                    onChange={(e) => setNuevoU_tel(e.target.value)}
                    placeholder="3001234567"
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
                  />
                </div>
                <div>
                  <label className="block text-slate-600 font-bold mb-1">Rol en el Sistema:</label>
                  <select
                    value={nuevoU_rol}
                    onChange={(e: any) => setNuevoU_rol(e.target.value)}
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 font-medium"
                  >
                    <option value="cliente">Cliente (Solicitar y contratar)</option>
                    <option value="prestador">Prestador de Servicios (Técnico)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-600 font-bold mb-1">Ciudad de Residencia:</label>
                  <select
                    value={nuevoU_ciudad}
                    onChange={(e: any) => setNuevoU_ciudad(e.target.value)}
                    className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 font-medium"
                  >
                    {CIUDADES_COBERTURA.map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>

                <div className="pt-2 flex gap-2">
                  <button
                    type="button"
                    onClick={() => setModalNuevoUsuario(false)}
                    className="flex-1 py-2.5 rounded-xl border border-slate-200 text-slate-600 font-bold hover:bg-slate-50 cursor-pointer transition"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold cursor-pointer transition shadow-sm"
                  >
                    Guardar Usuario
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
