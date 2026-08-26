import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = {
  title: "Registro Maestro de Servicios",
  description: "Consulta centralizada de puntos de servicio municipales",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es"><body>{children}</body></html>;
}
