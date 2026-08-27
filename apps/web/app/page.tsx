"use client";

import { FormEvent, useState } from "react";

type ServicePoint = {
  id: number;
  code: string;
  name: string;
  address: string | null;
  status: string;
  dependency_id: number | null;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [query, setQuery] = useState("");
  const [items, setItems] = useState<ServicePoint[]>([]);
  const [message, setMessage] = useState("Escribí un dato para comenzar la búsqueda.");
  const [isLoading, setIsLoading] = useState(false);

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoading(true);
    setMessage("Buscando...");
    try {
      const response = await fetch(`${apiUrl}/api/v1/puntos-servicio?query=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error("No se pudo consultar el padrón");
      const result = await response.json() as { items: ServicePoint[]; total: number };
      setItems(result.items);
      setMessage(result.total ? `${result.total} resultado(s) encontrado(s).` : "No encontramos puntos con ese criterio.");
    } catch {
      setMessage("No se pudo conectar con la API. Verificá que el backend esté ejecutándose.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <nav className="topbar" aria-label="Navegación principal">
        <a className="brand" href="https://www.laplata.gob.ar/" target="_blank" rel="noreferrer">
          <img src="https://turnos.laplata.gob.ar/public/images/laplata_dark.png" alt="La Plata Capital" />
          <span>Subsecretaría de Hacienda</span>
        </a>
        <span className="environment">MVP · Interno</span>
      </nav>
      <header>
        <p className="eyebrow">Gestión de servicios municipales</p>
        <h1>Registro Maestro</h1>
        <p className="intro">La información de puntos de servicio, cuentas y proveedores en un solo lugar.</p>
      </header>
      <section className="search-panel" aria-labelledby="search-title">
        <div className="section-heading">
          <div><p className="eyebrow">Consulta rápida</p><h2 id="search-title">Buscar información</h2></div>
          <span className="shortcut">Padrón maestro</span>
        </div>
        <label htmlFor="search">NIS, cuenta, dependencia, proveedor o domicilio</label>
        <form className="search-row" onSubmit={search}>
          <input id="search" name="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ej. CAPS 24 o 123456" />
          <button type="submit" disabled={isLoading}>{isLoading ? "Buscando" : "Buscar"}</button>
        </form>
        <p className="message" role="status">{message}</p>
        {items.length > 0 && <div className="results">
          {items.map((item) => <article key={item.id} className="result">
            <strong>{item.name}</strong>
            <span>{item.code} · {item.address ?? "Domicilio pendiente"}</span>
            <small>{item.status}</small>
          </article>)}
        </div>}
        <div className="quick-links" aria-label="Accesos del padrón">
          <button type="button" className="link-button">+ Nuevo punto de servicio</button>
          <button type="button" className="link-button">Importar facturas</button>
          <button type="button" className="link-button">Ver gastos</button>
        </div>
      </section>
      <section className="status-grid" aria-label="Resumen del padrón">
        <div><strong>{items.length}</strong><span>Resultados actuales</span></div>
        <div><strong>API</strong><span>Fuente de consulta</span></div>
        <div><strong>MVP</strong><span>Padrón en construcción</span></div>
      </section>
    </main>
  );
}
