"use client";

import { useState } from "react";
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { Logo } from "@/components/layout/Logo";
import { Button, cx } from "@/components/ui";

interface Paso {
  imagen: string;
  /** El primer paso va sobre azul noche; los demás, sobre fondo claro. */
  oscuro?: boolean;
  titulo: string;
  texto: string;
}

const PASOS: readonly Paso[] = [
  {
    imagen: "/images/ilustraciones/hero.png",
    oscuro: true,
    titulo: "Talento al toque",
    texto: "Profesionales revisados llegan a tu puerta: electricidad, plomería, limpieza, cerrajería y más.",
  },
  {
    imagen: "/images/ilustraciones/reserva.png",
    titulo: "Reserva con fecha o pide al instante",
    texto: "Agenda el día y la hora que te sirvan, o usa el pedido inmediato cuando algo no puede esperar.",
  },
  {
    imagen: "/images/ilustraciones/seguimiento.png",
    titulo: "Sigue cada paso y paga con claridad",
    texto: "Mira en el mapa cuándo llega tu profesional y recibe el valor con el IVA detallado.",
  },
];

/** Recorrido de bienvenida que se muestra la primera vez, antes de las pantallas de acceso. */
export function Bienvenida({ onIngresar, onRegistrarse }: { onIngresar: () => void; onRegistrarse: () => void }) {
  const [indice, setIndice] = useState(0);
  const paso = PASOS[indice];
  const ultimo = indice === PASOS.length - 1;

  return (
    <div className={cx("min-h-screen transition-colors duration-300", paso.oscuro ? "bg-[#0A1320] text-white" : "bg-background text-foreground")}>
      <div className="mx-auto flex min-h-screen w-full max-w-md flex-col">
        <div className={cx("relative h-[52vh] min-h-[300px] shrink-0 overflow-hidden", paso.oscuro ? "bg-[#0A1320]" : "bg-[#F4F5F7] sm:mt-6 sm:rounded-[2rem]")}>
          <Image
            key={paso.imagen}
            src={paso.imagen}
            alt=""
            fill
            priority={indice === 0}
            sizes="(max-width: 768px) 100vw, 448px"
            className={cx("animate-fade-in object-cover", paso.oscuro ? "object-[center_75%]" : "object-center")}
          />
          {paso.oscuro && (
            <>
              <div aria-hidden className="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-b from-transparent to-[#0A1320]" />
              <Logo claro conLema className="absolute left-6 top-8" />
            </>
          )}
        </div>

        <div className="flex flex-1 flex-col gap-3 px-6 pb-8 pt-7">
          <h1 key={paso.titulo} className="animate-fade-up text-[2rem] font-extrabold leading-[1.1] tracking-tight">
            {paso.oscuro ? (
              <>
                Talento
                <br />
                <span className="text-accent">al toque</span>
              </>
            ) : (
              paso.titulo
            )}
          </h1>
          <p className={cx("text-[15px] leading-relaxed", paso.oscuro ? "text-white/70" : "text-muted-foreground")}>{paso.texto}</p>

          <div className="mt-1 flex gap-1.5" role="group" aria-label={`Paso ${indice + 1} de ${PASOS.length}`}>
            {PASOS.map((p, i) => (
              <button
                key={p.imagen}
                type="button"
                onClick={() => setIndice(i)}
                aria-label={`Ir al paso ${i + 1}`}
                aria-current={i === indice ? "step" : undefined}
                className={cx(
                  "h-2 rounded-full transition-all duration-300",
                  i === indice ? "w-8 bg-accent" : cx("w-2", paso.oscuro ? "bg-white/25" : "bg-border"),
                )}
              />
            ))}
          </div>

          <div className="mt-auto flex flex-col gap-2 pt-6">
            {ultimo ? (
              <Button variante="accent" tamano="lg" bloque onClick={onRegistrarse}>
                Crear mi cuenta
              </Button>
            ) : (
              <Button variante="accent" tamano="lg" bloque onClick={() => setIndice(indice + 1)}>
                {indice === 0 ? "Comenzar" : "Siguiente"}
                <ArrowRight className="h-5 w-5" aria-hidden />
              </Button>
            )}
            <button
              type="button"
              onClick={onIngresar}
              className={cx("touch-feedback h-11 rounded-full text-[15px] font-bold", paso.oscuro ? "text-white hover:bg-white/10" : "text-foreground hover:bg-muted")}
            >
              Ya tengo cuenta
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
