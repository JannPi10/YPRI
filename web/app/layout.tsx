import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import { Urbanist } from "next/font/google";
import { SCRIPT_TEMA } from "@/components/layout/temaScript";
import { ToastProvider } from "@/components/ui";
import { AppStoreProvider } from "@/store/AppStore";
import "./globals.css";

// Tipografía de la identidad «Talento al toque», servida por Next.js desde el propio sitio.
const urbanist = Urbanist({ subsets: ["latin"], variable: "--font-urbanist", display: "swap" });

export const metadata: Metadata = {
  title: "YPRI | Talento al toque",
  description: "Encuentra y contrata profesionales de electricidad, plomería, limpieza, climatización y cerrajería a domicilio.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#0F1B2D" },
    { media: "(prefers-color-scheme: dark)", color: "#0A1320" },
  ],
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    // La clase "dark" la pone el script antes de hidratar; por eso se ignora la diferencia.
    <html lang="es" className={urbanist.variable} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: SCRIPT_TEMA }} />
      </head>
      <body className="min-h-screen">
        <AppStoreProvider>
          <ToastProvider>{children}</ToastProvider>
        </AppStoreProvider>
      </body>
    </html>
  );
}
