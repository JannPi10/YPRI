import { cx } from "@/components/ui";

/**
 * Marca de YPRI: símbolo ámbar con la «Y», el nombre y, si se pide, el lema.
 * Con `claro` el texto va en blanco para usarlo sobre el azul noche.
 */
export function Logo({ claro, className, conLema }: { claro?: boolean; className?: string; prioridad?: boolean; conLema?: boolean }) {
  return (
    <span className={cx("inline-flex items-center gap-2.5", className)}>
      <span aria-hidden className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-accent text-accent-foreground">
        <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round">
          <path d="M5 4l7 9 7-9" />
          <path d="M12 13v7" />
        </svg>
      </span>
      <span className="flex flex-col leading-none">
        <span className={cx("text-xl font-extrabold tracking-wide", claro ? "text-white" : "text-foreground")}>YPRI</span>
        {conLema && <span className={cx("mt-1 text-[11px] font-semibold", claro ? "text-white/70" : "text-muted-foreground")}>Talento al toque</span>}
      </span>
    </span>
  );
}
