export default function Home() {
  return (
    <main>
      <header>
        <p className="eyebrow">Subsecretaría de Hacienda</p>
        <h1>Registro Maestro</h1>
        <p className="intro">Encontrá puntos de servicio, cuentas, proveedores y documentación desde un solo lugar.</p>
      </header>
      <section className="search-panel" aria-labelledby="search-title">
        <h2 id="search-title">Buscar información</h2>
        <label htmlFor="search">NIS, cuenta, dependencia, proveedor o domicilio</label>
        <div className="search-row">
          <input id="search" name="search" placeholder="Ej. CAPS 24 o 123456" />
          <button type="button">Buscar</button>
        </div>
      </section>
      <section className="status-grid" aria-label="Resumen del padrón">
        <div><strong>0</strong><span>Puntos de servicio</span></div>
        <div><strong>0</strong><span>Cuentas activas</span></div>
        <div><strong>0</strong><span>Importaciones pendientes</span></div>
      </section>
    </main>
  );
}
