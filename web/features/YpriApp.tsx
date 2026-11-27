"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { Logo } from "@/components/layout/Logo";
import { useToast } from "@/components/ui";
import { puedeVerVista, usaAppMovil, vistaInicial, vistasPermitidas, type VistaId } from "@/lib/domain/navigation";
import { useAppStore } from "@/store/AppStore";
import { useSesion } from "@/store/hooks";
import { Bienvenida } from "./auth/Bienvenida";
import { LoginView } from "./auth/LoginView";
import { RegisterView } from "./auth/RegisterView";
import { ClienteApp } from "./cliente/ClienteApp";
import { REGISTRO_VISTAS } from "./viewRegistry";

/** Marca en el navegador que la persona ya vio el recorrido de bienvenida. */
const CLAVE_BIENVENIDA = "ypri:bienvenida-vista";

export function YpriApp() {
  const { hidratado } = useAppStore();
  // null mientras se consulta el navegador; así no parpadea la pantalla equivocada.
  const [bienvenidaPendiente, setBienvenidaPendiente] = useState<boolean | null>(null);
  useEffect(() => {
    try {
      setBienvenidaPendiente(window.localStorage.getItem(CLAVE_BIENVENIDA) !== "1");
    } catch {
      setBienvenidaPendiente(false);
    }
  }, []);
  const cerrarBienvenida = (destino: "login" | "registro") => {
    try {
      window.localStorage.setItem(CLAVE_BIENVENIDA, "1");
    } catch {
      // Sin almacenamiento disponible, el recorrido simplemente vuelve a mostrarse la próxima vez.
    }
    setBienvenidaPendiente(false);
    setPantallaAcceso(destino);
  };
  const { usuarioActual, cerrarSesion } = useSesion();
  const toast = useToast();
  const [pantallaAcceso, setPantallaAcceso] = useState<"login" | "registro">("login");
  const [vista, setVista] = useState<VistaId | null>(null);

  // Al cambiar de sesión se reinicia la vista a la primera permitida para el rol.
  const claveSesion = usuarioActual ? `${usuarioActual.id}:${usuarioActual.rol}` : null;
  const [claveVista, setClaveVista] = useState(claveSesion);
  if (claveVista !== claveSesion) {
    setClaveVista(claveSesion);
    setVista(vistaInicial(usuarioActual));
  }

  if (!hidratado || bienvenidaPendiente === null) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#0A1320]" aria-busy="true" aria-label="Cargando YPRI">
        <Logo claro conLema className="animate-pulso-suave scale-125" />
      </div>
    );
  }

  if (!usuarioActual) {
    if (bienvenidaPendiente) {
      return <Bienvenida onIngresar={() => cerrarBienvenida("login")} onRegistrarse={() => cerrarBienvenida("registro")} />;
    }
    return pantallaAcceso === "login" ? (
      <LoginView onIrARegistro={() => setPantallaAcceso("registro")} />
    ) : (
      <RegisterView onIrALogin={() => setPantallaAcceso("login")} />
    );
  }

  const salir = () => {
    cerrarSesion();
    setPantallaAcceso("login");
    toast.exito("Cerraste sesión correctamente.");
  };

  // Los clientes usan la app móvil; el resto de roles, el panel por vistas.
  if (usaAppMovil(usuarioActual)) return <ClienteApp key={usuarioActual.id} usuario={usuarioActual} onCerrarSesion={salir} />;

  // Protección de vistas: nunca se renderiza una vista que el rol no tiene permitida.
  const vistaSegura = vista && puedeVerVista(usuarioActual, vista) ? vista : vistaInicial(usuarioActual);
  if (!vistaSegura) return null;

  const navegar = (destino: VistaId) => {
    if (puedeVerVista(usuarioActual, destino)) setVista(destino);
    window.scrollTo({ top: 0 });
  };

  return (
    <AppShell
      usuario={usuarioActual}
      vistas={vistasPermitidas(usuarioActual)}
      vistaActiva={vistaSegura}
      onNavegar={navegar}
      onCerrarSesion={salir}
    >
      {REGISTRO_VISTAS[vistaSegura]({ usuario: usuarioActual, navegar })}
    </AppShell>
  );
}
