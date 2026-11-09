// ========================================================================================
// SISTEMA YPRI - PLATAFORMA DE SERVICIOS A DOMICILIO
// Definiciones, Modelos y Persistencia en Memoria / LocalStorage
// ========================================================================================

export const ROLES_SISTEMA = ["cliente", "prestador", "admin"] as const;
export type RolUsuario = typeof ROLES_SISTEMA[number];

export const CATEGORIAS_SERVICIO = [
  "Electricidad",
  "Plomeria",
  "Limpieza",
  "Climatizacion",
  "Cerrajeria"
] as const;
export type CategoriaServicio = typeof CATEGORIAS_SERVICIO[number];

export const CIUDADES_COBERTURA = [
  "Cucuta",
  "Cali",
  "Bogota",
  "Medellin",
  "Bucaramanga"
] as const;
export type CiudadCobertura = typeof CIUDADES_COBERTURA[number];

export const DIAS_SEMANA_MATRIZ = [
  "Lunes",
  "Martes",
  "Miercoles",
  "Jueves",
  "Viernes",
  "Sabado"
] as const;

export const ESTADOS_CONTRATO = [
  "Pendiente",
  "En proceso",
  "Completado",
  "Cancelado"
] as const;
export type EstadoContrato = typeof ESTADOS_CONTRATO[number];

export const IVA_PORCENTAJE = 0.19;

export interface Usuario {
  id: string;
  nombre: string;
  correo: string;
  contrasena: string;
  rol: RolUsuario;
  ciudad: CiudadCobertura;
  telefono: string;
}

export interface Servicio {
  codigo: string;
  prestador_id: string;
  prestador_nombre: string;
  categoria: CategoriaServicio;
  descripcion: string;
  tarifa_hora: number;
  ciudad: CiudadCobertura;
  disponible: boolean;
  calificacion: number;
  num_contratos: number;
}

export interface Contrato {
  id: string;
  cliente_id: string;
  cliente_nombre: string;
  servicio_codigo: string;
  servicio_nombre: string;
  horas: number;
  tarifa_hora: number;
  total: number;
  estado: EstadoContrato;
  calificacion?: number;
  comentario?: string;
  fecha?: string;
}

export interface Calificacion {
  id: string;
  contrato_id: string;
  cliente_nombre: string;
  servicio_codigo: string;
  puntuacion: number;
  comentario: string;
  fecha: string;
}

// Datos iniciales precargados
export const USUARIOS_INICIALES: Usuario[] = [
  {
    id: "USR-001",
    nombre: "Juan Perez",
    correo: "juan.perez@email.com",
    contrasena: "juan123",
    rol: "cliente",
    ciudad: "Cucuta",
    telefono: "3001234567"
  },
  {
    id: "USR-002",
    nombre: "Carlos Gomez",
    correo: "carlos.gomez@email.com",
    contrasena: "carlos456",
    rol: "prestador",
    ciudad: "Cucuta",
    telefono: "3109876543"
  },
  {
    id: "USR-003",
    nombre: "Admin YPRI",
    correo: "admin@ypri.com",
    contrasena: "admin2026",
    rol: "admin",
    ciudad: "Cucuta",
    telefono: "3200000000"
  }
];

export const SERVICIOS_INICIALES: Servicio[] = [
  {
    codigo: "SERV-01",
    prestador_id: "USR-002",
    prestador_nombre: "Carlos Gomez",
    categoria: "Electricidad",
    descripcion: "Instalaciones electricas residenciales y comerciales",
    tarifa_hora: 35000,
    ciudad: "Cucuta",
    disponible: true,
    calificacion: 4.8,
    num_contratos: 12
  },
  {
    codigo: "SERV-02",
    prestador_id: "USR-002",
    prestador_nombre: "Marta Rodriguez",
    categoria: "Plomeria",
    descripcion: "Reparacion de tuberias, grifos y sistemas hidraulicos",
    tarifa_hora: 30000,
    ciudad: "Cucuta",
    disponible: true,
    calificacion: 4.5,
    num_contratos: 8
  },
  {
    codigo: "SERV-03",
    prestador_id: "USR-002",
    prestador_nombre: "Andres Silva",
    categoria: "Climatizacion",
    descripcion: "Mantenimiento y reparacion de aires acondicionados",
    tarifa_hora: 45000,
    ciudad: "Cucuta",
    disponible: false,
    calificacion: 5.0,
    num_contratos: 5
  },
  {
    codigo: "SERV-04",
    prestador_id: "USR-002",
    prestador_nombre: "Jorge Mendoza",
    categoria: "Cerrajeria",
    descripcion: "Apertura de puertas, cambio de chapas y cerraduras",
    tarifa_hora: 38000,
    ciudad: "Cucuta",
    disponible: true,
    calificacion: 4.7,
    num_contratos: 15
  },
  {
    codigo: "SERV-05",
    prestador_id: "USR-002",
    prestador_nombre: "Sandra Rios",
    categoria: "Limpieza",
    descripcion: "Limpieza profunda de hogares y oficinas",
    tarifa_hora: 25000,
    ciudad: "Cucuta",
    disponible: true,
    calificacion: 4.3,
    num_contratos: 20
  }
];

export const CONTRATOS_INICIALES: Contrato[] = [
  {
    id: "CONTR-101",
    cliente_id: "USR-001",
    cliente_nombre: "Juan Perez",
    servicio_codigo: "SERV-01",
    servicio_nombre: "Electricidad - Carlos Gomez",
    horas: 5,
    tarifa_hora: 35000,
    total: 208250, // 35000 * 5 = 175000 + 19% IVA = 208250
    estado: "Completado",
    calificacion: 4.8,
    comentario: "Excelente trabajo, muy puntual",
    fecha: "18/09/2026"
  }
];

// MATRICES INICIALES DE GUIA 9
export const MATRIZ_SEMANAL_INICIAL: number[][] = [
  [350000, 420000, 280000, 510000, 600000, 450000], // Electricidad
  [280000, 310000, 390000, 250000, 480000, 320000], // Plomeria
  [180000, 220000, 250000, 290000, 380000, 420000], // Limpieza
  [450000, 520000, 380000, 490000, 650000, 710000], // Climatizacion
  [220000, 190000, 260000, 310000, 410000, 300000]  // Cerrajeria
];

export const MATRIZ_CIUDADES_INICIAL: number[][] = [
  // Cucuta, Cali, Bogota, Medellin, Bucaramanga (5x5 CUADRADA)
  [450000, 380000, 850000, 720000, 210000], // Electricidad
  [320000, 290000, 640000, 510000, 180000], // Plomeria
  [250000, 210000, 490000, 430000, 160000], // Limpieza
  [580000, 620000, 950000, 890000, 310000], // Climatizacion
  [290000, 240000, 530000, 470000, 150000]  // Cerrajeria
];

// OPERACIONES MATEMATICAS DE GUIA 9
export function calcularTotalFilas(matriz: number[][]): number[] {
  return matriz.map(fila => fila.reduce((acc, val) => acc + val, 0));
}

export function calcularTotalColumnas(matriz: number[][]): number[] {
  if (!matriz.length || !matriz[0].length) return [];
  const cols = matriz[0].length;
  const filas = matriz.length;
  const totales: number[] = [];
  for (let j = 0; j < cols; j++) {
    let sum = 0;
    for (let i = 0; i < filas; i++) {
      sum += matriz[i][j];
    }
    totales.push(sum);
  }
  return totales;
}

export function calcularTotalGeneral(matriz: number[][]): number {
  return matriz.reduce((acc, fila) => acc + fila.reduce((a, b) => a + b, 0), 0);
}

export function calcularPromedioGeneral(matriz: number[][]): number {
  if (!matriz.length || !matriz[0].length) return 0;
  const total = calcularTotalGeneral(matriz);
  const totalCeldas = matriz.length * matriz[0].length;
  return total / totalCeldas;
}

export function crearMatrizNula(filas: number, cols: number): number[][] {
  return Array.from({ length: filas }, () => Array(cols).fill(0));
}

export function crearMatrizIdentidad(n: number): number[][] {
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => (i === j ? 1 : 0))
  );
}

export function formatearMoneda(val: number): string {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0
  }).format(val);
}

// ========================================================================================
// SUBALGORITMOS EN TYPESCRIPT / REACT (GUÍA 10)
// ========================================================================================

export interface LiquidacionFinanciera {
  tarifaHora: number;
  horas: number;
  subtotalBruto: number;
  descuentoPct: number;
  montoDescuento: number;
  subtotalNeto: number;
  tasaIva: number;
  montoIva: number;
  totalPagar: number;
}

export function calcularLiquidacionContrato(
  tarifaHora: number,
  horas: number,
  descuentoPct: number = 0,
  tasaIva: number = IVA_PORCENTAJE
): LiquidacionFinanciera {
  const subtotalBruto = tarifaHora * horas;
  const montoDescuento = subtotalBruto * (descuentoPct / 100);
  const subtotalNeto = subtotalBruto - montoDescuento;
  const montoIva = subtotalNeto * tasaIva;
  const totalPagar = subtotalNeto + montoIva;

  return {
    tarifaHora,
    horas,
    subtotalBruto,
    descuentoPct,
    montoDescuento,
    subtotalNeto,
    tasaIva,
    montoIva,
    totalPagar
  };
}

export function calcularComisionPlataforma(
  totalPagar: number,
  comisionPct: number = 0.10,
  retencionPct: number = 0.04
) {
  const comisionYpri = Math.round(totalPagar * comisionPct);
  const retencionFuente = Math.round(totalPagar * retencionPct);
  const pagoNetoPrestador = Math.round(totalPagar - comisionYpri - retencionFuente);

  return {
    comisionYpri,
    retencionFuente,
    pagoNetoPrestador
  };
}

export function calcularPromedioRating(
  ratingPrevio: number,
  numEvaluaciones: number,
  nuevaNota: number
): number {
  if (numEvaluaciones <= 1) return Number(nuevaNota.toFixed(1));
  const totalPrevio = ratingPrevio * (numEvaluaciones - 1);
  return Number(((totalPrevio + nuevaNota) / numEvaluaciones).toFixed(1));
}

export interface ProductoInventario {
  codigo: string;
  nombre: string;
  precio: number;
  cantidad: number;
}

export function calcularSubtotalInventario(precio: number, cantidad: number): number {
  return precio * cantidad;
}

export function calcularTotalInventario(prods: ProductoInventario[]): number {
  return prods.reduce((acc, p) => acc + calcularSubtotalInventario(p.precio, p.cantidad), 0);
}
