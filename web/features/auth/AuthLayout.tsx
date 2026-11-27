import type { ReactNode } from "react";
import Image from "next/image";
import { BadgeCheck, Receipt, Star } from "lucide-react";
import { Logo } from "@/components/layout/Logo";
import { SelectorTema } from "@/components/layout/Tema";
import { escalonado } from "@/components/ui";

const VENTAJAS = [
  { icono: BadgeCheck, titulo: "Profesionales verificados", texto: "Perfiles revisados por YPRI antes de recibir solicitudes." },
  { icono: Receipt, titulo: "Precios claros", texto: "Tarifa por hora con IVA calculado desde el primer momento." },
  { icono: Star, titulo: "Calificaciones reales", texto: "Cada reseña viene de un servicio completado en la plataforma." },
];

const EQUIPO = "/images/ilustraciones/equipo.png";
const ALT_EQUIPO = "Equipo de profesionales de YPRI: electricista, plomera, limpieza y cerrajera";

/** Marco de las pantallas de acceso: encabezado azul noche en móvil y pantalla dividida en escritorio. */
export function AuthLayout({ titulo, descripcion, children }: { titulo: string; descripcion: string; children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background lg:grid lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
      {/* Panel de marca (solo escritorio) */}
      <aside className="relative hidden overflow-hidden bg-[#0A1320] p-12 text-white lg:flex lg:flex-col">
        <Logo claro conLema prioridad />
        <div className="relative my-auto max-w-md py-10">
          <h2 className="animate-fade-up text-5xl font-extrabold leading-[1.05] tracking-tight">
            Talento
            <br />
            <span className="text-accent">al toque</span>
          </h2>
          <p className="mt-4 animate-fade-up text-white/70" style={escalonado(1, 80)}>
            Electricidad, plomería, limpieza, climatización, cerrajería y belleza en las principales ciudades de Colombia.
          </p>
          <div className="relative mt-8 aspect-[16/9] animate-fade-up overflow-hidden rounded-[2rem]" style={escalonado(2, 80)}>
            <Image src={EQUIPO} alt={ALT_EQUIPO} fill priority sizes="(min-width: 1024px) 448px, 0px" className="object-cover object-[center_20%]" />
          </div>
          <ul className="mt-8 space-y-5">
            {VENTAJAS.map(({ icono: Icono, titulo: t, texto }, i) => (
              <li key={t} className="flex animate-fade-up gap-4" style={escalonado(i + 3, 80)}>
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-accent text-accent-foreground">
                  <Icono className="h-5 w-5" aria-hidden />
                </span>
                <span>
                  <span className="block font-bold">{t}</span>
                  <span className="block text-sm text-white/65">{texto}</span>
                </span>
              </li>
            ))}
          </ul>
        </div>
        <p className="relative text-xs text-white/45">YPRI · Talento al toque</p>
      </aside>

      {/* Formulario */}
      <div className="flex min-h-screen flex-col">
        <header className="relative overflow-hidden rounded-b-[2rem] bg-[#0A1320] px-6 pb-16 pt-8 text-white lg:hidden">
          <div className="relative flex items-center justify-between gap-3">
            <Logo claro conLema prioridad />
            <SelectorTema sobreOscuro />
          </div>
          <div className="relative mt-6 h-36 overflow-hidden rounded-3xl">
            <Image src={EQUIPO} alt={ALT_EQUIPO} fill priority sizes="(max-width: 1023px) 100vw, 0px" className="object-cover object-[center_24%]" />
          </div>
          <h1 className="relative mt-6 animate-fade-up text-3xl font-extrabold tracking-tight">{titulo}</h1>
          <p className="relative mt-1 animate-fade-up text-sm text-white/70" style={escalonado(1, 80)}>
            {descripcion}
          </p>
        </header>
        <main className="flex flex-1 items-start justify-center px-4 pb-10 lg:items-center lg:px-12 lg:py-12">
          <div className="-mt-10 w-full max-w-md animate-fade-up lg:mt-0" style={escalonado(2, 80)}>
            <div className="mb-6 hidden justify-end lg:flex">
              <SelectorTema />
            </div>
            <div className="mb-8 hidden lg:block">
              <h1 className="text-4xl font-extrabold tracking-tight">{titulo}</h1>
              <p className="mt-2 text-muted-foreground">{descripcion}</p>
            </div>
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
