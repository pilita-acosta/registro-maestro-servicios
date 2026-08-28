"use client";

import { FormEvent, useEffect, useState } from "react";

type ServicePoint = {
  id: number;
  code: string;
  name: string;
  address: string | null;
  status: string;
  dependency_id: number | null;
  dependency: string | null;
  secretary: string | null;
  service: string | null;
  provider: string | null;
  account: string | null;
};

type ServicePointDetail = {
  name: string;
  code: string;
  address: string;
  dependency: string | null;
  secretaries: string[];
  accounts: { external_code: string; nis: string | null; provider: string; service: string; contract: string }[];
};

type InvoiceInboxItem = {
  id: number;
  period: string;
  due_date: string;
  delivery_deadline: string;
  status: string;
  responsible: string | null;
  cutoff_risk: string;
  account: string;
  point: string;
  invoice_id: number | null;
  invoice_status: string | null;
  invoice_amount: number;
  resolved_amount: number;
};

type ReportSummary = {
  expected: number;
  missing: number;
  received: number;
  invoices: number;
  invoiced_amount: number;
  paid_amount: number;
  open_incidents: number;
};

type Section = "inicio" | "padron" | "operacion" | "importaciones" | "historial" | "catalogos" | "usuarios";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState({ secretary: "", domicile: "", service: "", provider: "" });
  const [items, setItems] = useState<ServicePoint[]>([]);
  const [message, setMessage] = useState("Escribí un dato para comenzar la búsqueda.");
  const [isLoading, setIsLoading] = useState(false);
  const [invoiceInbox, setInvoiceInbox] = useState<InvoiceInboxItem[]>([]);
  const [importMessage, setImportMessage] = useState("");
  const [report, setReport] = useState<ReportSummary | null>(null);
  const [selectedPoint, setSelectedPoint] = useState<ServicePointDetail | null>(null);
  const [receiveId, setReceiveId] = useState<number | null>(null);
  const [resolveId, setResolveId] = useState<number | null>(null);
  const [activeSection, setActiveSection] = useState<Section>("inicio");

  async function refreshInbox() {
    const response = await fetch(`${apiUrl}/api/v1/bandeja-facturas`);
    if (!response.ok) throw new Error("No se pudo cargar la bandeja");
    setInvoiceInbox(await response.json() as InvoiceInboxItem[]);
  }

  useEffect(() => {
    refreshInbox().catch(() => setInvoiceInbox([]));
    fetch(`${apiUrl}/api/v1/reportes/resumen`)
      .then((response) => response.ok ? response.json() as Promise<ReportSummary> : Promise.reject())
      .then(setReport)
      .catch(() => setReport(null));
  }, []);

  async function receiveInvoice(id: number) {
    const form = document.querySelector<HTMLFormElement>(`form[data-receive-id="${id}"]`);
    if (!form) return;
    const data = new FormData(form);
    const response = await fetch(`${apiUrl}/api/v1/facturas-esperadas/${id}/recibir`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ number: data.get("number"), amount: Number(data.get("amount")), resolution_mode: "reintegro_mes_vencido" }),
    });
    if (!response.ok) {
      window.alert("No se pudo registrar la factura. Puede existir un duplicado.");
      return;
    }
    await refreshInbox();
  }

  async function claimInvoice(id: number) {
    const message = "No se recibió la factura del período; solicitar entrega urgente";
    await fetch(`${apiUrl}/api/v1/facturas-esperadas/${id}/reclamos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, responsible: "Oficina de Servicios" }),
    });
    await refreshInbox();
  }

  async function liquidateInvoice(invoiceId: number) {
    const response = await fetch(`${apiUrl}/api/v1/facturas/${invoiceId}/liquidar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ secretary_id: 1, resolution_mode: "reintegro_mes_vencido" }),
    });
    if (!response.ok) {
      window.alert("No se pudo iniciar la liquidacion. Puede que ya exista.");
      return;
    }
    await refreshInbox();
  }

  async function resolveInvoice(invoiceId: number, balance: number) {
    const form = document.querySelector<HTMLFormElement>(`form[data-resolve-id="${invoiceId}"]`);
    if (!form) return;
    const data = new FormData(form);
    const amount = Number(data.get("amount"));
    const response = await fetch(`${apiUrl}/api/v1/facturas/${invoiceId}/resolver`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: data.get("mode"), amount, recipient: data.get("recipient") }),
    });
    if (!response.ok) {
      window.alert("No se pudo registrar la resolución. Revisá el importe y la modalidad.");
      return;
    }
    await refreshInbox();
  }

  async function previewImport(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setImportMessage("Analizando archivo...");
    const response = await fetch(`${apiUrl}/api/v1/importaciones/previsualizar`, { method: "POST", body: formData });
    if (!response.ok) {
      setImportMessage("No se pudo previsualizar el archivo.");
      return;
    }
    const result = await response.json() as { sheet_count: number; row_count: number; valid_row_count: number; error_row_count: number };
    setImportMessage(`${result.sheet_count} hojas · ${result.row_count} filas · ${result.valid_row_count} válidas · ${result.error_row_count} observadas`);
  }

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsLoading(true);
    setMessage("Buscando...");
    try {
      const params = new URLSearchParams();
      if (query.trim()) params.set("query", query.trim());
      Object.entries(filters).forEach(([key, value]) => { if (value.trim()) params.set(key, value.trim()); });
      const response = await fetch(`${apiUrl}/api/v1/puntos-servicio?${params.toString()}`);
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

  async function openPoint(id: number) {
    const response = await fetch(`${apiUrl}/api/v1/puntos-servicio/${id}/detalle`);
    if (response.ok) setSelectedPoint(await response.json() as ServicePointDetail);
  }

  return (
    <main>
      <div className="app-shell">
        <aside className="sidebar" aria-label="Navegación del sistema">
          <a className="brand" href="https://www.laplata.gob.ar/" target="_blank" rel="noreferrer">
            <img src="https://turnos.laplata.gob.ar/public/images/laplata_dark.png" alt="La Plata Capital" />
            <span>Subsecretaría de Hacienda</span>
          </a>
          <div className="sidebar-label">Módulos</div>
          <nav className="side-nav">
            {([
              ["inicio", "Inicio", "Resumen y pendientes"],
              ["padron", "Padrón maestro", "Puntos y cuentas"],
              ["operacion", "Operación", "Facturas y liquidaciones"],
              ["importaciones", "Importaciones", "Archivos de proveedores"],
              ["historial", "Historial", "Auditoría y consultas"],
              ["catalogos", "Catálogos", "Datos de referencia"],
              ["usuarios", "Usuarios", "Roles y permisos"],
            ] as [Section, string, string][]).map(([section, label, description]) => (
              <button key={section} type="button" className={activeSection === section ? "active" : ""} onClick={() => setActiveSection(section)}>
                <strong>{label}</strong><span>{description}</span>
              </button>
            ))}
          </nav>
          <span className="environment">MVP · Interno</span>
        </aside>
        <div className="content-column">
      <header>
        <p className="eyebrow">Gestión de servicios municipales</p>
        <h1>{activeSection === "inicio" ? "Registro Maestro" : (["padron", "operacion", "importaciones", "historial", "catalogos", "usuarios"] as Section[]).includes(activeSection) ? ({ padron: "Padrón maestro", operacion: "Operación", importaciones: "Importaciones", historial: "Historial", catalogos: "Catálogos", usuarios: "Usuarios" } as Record<string, string>)[activeSection] : "Registro Maestro"}</h1>
        <p className="intro">{activeSection === "inicio" ? "La información de puntos de servicio, cuentas y proveedores en un solo lugar." : "Una vista enfocada para trabajar con información trazable y ordenada."}</p>
      </header>
      {activeSection === "padron" && <section className="search-panel padron-panel" aria-labelledby="search-title">
        <div className="section-heading">
          <div><p className="eyebrow">Consulta rápida</p><h2 id="search-title">Buscar información</h2></div>
          <span className="shortcut">Padrón maestro</span>
        </div>
        <label htmlFor="search">NIS, cuenta, dependencia, proveedor o domicilio</label>
        <form className="search-row" onSubmit={search}>
          <input id="search" name="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ej. CAPS 24 o 123456" />
          <button type="submit" disabled={isLoading}>{isLoading ? "Buscando" : "Buscar"}</button>
        </form>
        <div className="filter-grid" aria-label="Filtros del padrón">
          {(["secretary", "domicile", "service", "provider"] as const).map((filter) => <input key={filter} aria-label={filter === "secretary" ? "Secretaría" : filter === "domicile" ? "Domicilio" : filter === "service" ? "Servicio" : "Proveedor"} placeholder={filter === "secretary" ? "Secretaría" : filter === "domicile" ? "Domicilio" : filter === "service" ? "Tipo de servicio" : "Proveedor"} value={filters[filter]} onChange={(event) => setFilters({ ...filters, [filter]: event.target.value })} />)}
        </div>
        <p className="message" role="status">{message}</p>
        <div className="table-toolbar"><span>{items.length ? `${items.length} fila(s)` : "Sin resultados todavía"}</span><button type="button" className="link-button" onClick={() => { setQuery(""); setFilters({ secretary: "", domicile: "", service: "", provider: "" }); setItems([]); setMessage("Filtros limpios. Ejecutá una búsqueda para comenzar."); }}>Limpiar filtros</button></div>
        {items.length > 0 && <div className="data-table-wrap"><table className="data-table"><thead><tr><th>Punto</th><th>Cuenta</th><th>Secretaría</th><th>Domicilio</th><th>Servicio</th><th>Proveedor</th><th>Estado</th></tr></thead><tbody>{items.map((item) => <tr key={item.id} onClick={() => openPoint(item.id)}><td><strong>{item.name}</strong><small>{item.code}</small></td><td>{item.account ?? "-"}</td><td>{item.secretary ?? "-"}</td><td>{item.address ?? "-"}</td><td>{item.service ?? "-"}</td><td>{item.provider ?? "-"}</td><td><span className="table-status">{item.status}</span></td></tr>)}</tbody></table></div>}
        {selectedPoint && <aside className="point-detail" aria-label="Detalle del punto de servicio">
          <button type="button" className="close-detail" onClick={() => setSelectedPoint(null)}>Cerrar</button>
          <p className="eyebrow">Ficha del punto</p>
          <h3>{selectedPoint.name}</h3>
          <p>{selectedPoint.code} · {selectedPoint.address}</p>
          <p><strong>Dependencia:</strong> {selectedPoint.dependency ?? "Sin asignar"}</p>
          <p><strong>Secretarías:</strong> {selectedPoint.secretaries.join(", ") || "Sin asignar"}</p>
          <div className="detail-accounts">{selectedPoint.accounts.map((account) => <div key={account.external_code}><strong>{account.service}</strong><span>{account.provider} · {account.external_code} · Contrato {account.contract}</span></div>)}</div>
        </aside>}
        <div className="quick-links" aria-label="Acciones del padrón">
          <button type="button" className="link-button" disabled>Nuevo punto de servicio · Próximamente</button>
        </div>
        {importMessage && <p className="message" role="status">{importMessage}</p>}
      </section>}
      {activeSection === "inicio" && <section className="home-panel"><p className="eyebrow">Panel de control</p><h2>¿Qué necesitás hacer?</h2><p>Usá el Padrón para consultar y configurar puntos de servicio. Entrá en Operación para controlar facturas, imputaciones y pagos.</p><div className="home-actions"><button type="button" onClick={() => setActiveSection("padron")}>Consultar padrón</button><button type="button" onClick={() => setActiveSection("operacion")}>Ver operación</button></div></section>}
      {activeSection === "importaciones" && <section className="search-panel"><div className="section-heading"><div><p className="eyebrow">Carga controlada</p><h2>Previsualizar archivo</h2></div><span className="shortcut">Sin alterar el original</span></div><p className="message">Subí un Excel de proveedor para revisar hojas, filas válidas y observaciones antes de confirmar.</p><label className="file-button">Seleccionar Excel<input type="file" accept=".xlsx,.xlsm" onChange={previewImport} /></label>{importMessage && <p className="message" role="status">{importMessage}</p>}</section>}
      {(activeSection === "inicio" || activeSection === "operacion") && <section className="invoice-panel" aria-labelledby="invoice-title">
        <div className="section-heading">
          <div><p className="eyebrow">Control operativo</p><h2 id="invoice-title">Facturas que requieren atención</h2></div>
          <span className="shortcut">Evitar demoras y cortes</span>
        </div>
        <div className="invoice-list">
          {invoiceInbox.length === 0 && <p className="message">No hay facturas esperadas cargadas.</p>}
          {invoiceInbox.map((invoice) => <article key={invoice.id} className={`invoice-row risk-${invoice.cutoff_risk}`}>
            <div><strong>{invoice.point}</strong><span>{invoice.account} · Período {invoice.period}</span></div>
            <div className="invoice-meta"><small>Entrega: {invoice.delivery_deadline}</small><small>Vence: {invoice.due_date}</small><b>{invoice.status} · riesgo {invoice.cutoff_risk}</b></div>
            <span className="invoice-responsible">Responsable: {invoice.responsible ?? "Sin asignar"}</span>
            <div className="invoice-actions">
              {invoice.status === "faltante" && <button type="button" onClick={() => claimInvoice(invoice.id)}>Registrar reclamo</button>}
              {invoice.status !== "recibida" && <button type="button" onClick={() => setReceiveId(invoice.id)}>Marcar recibida</button>}
              {invoice.invoice_id && invoice.invoice_status === "recibida" && <button type="button" onClick={() => liquidateInvoice(invoice.invoice_id as number)}>Iniciar liquidación</button>}
              {invoice.invoice_id && ["aprobada_para_liquidar", "pago_parcial"].includes(invoice.invoice_status ?? "") && <button type="button" onClick={() => setResolveId(invoice.invoice_id)}>Resolver pago</button>}
            </div>
            {receiveId === invoice.id && <form data-receive-id={invoice.id} className="inline-form" onSubmit={(event) => { event.preventDefault(); receiveInvoice(invoice.id); }}><input name="number" required placeholder="Número de factura" /><input name="amount" required type="number" min="0" step="0.01" placeholder="Importe" /><button type="submit">Confirmar recepción</button><button type="button" onClick={() => setReceiveId(null)}>Cancelar</button></form>}
            {resolveId === invoice.invoice_id && invoice.invoice_id && <form data-resolve-id={invoice.invoice_id} className="inline-form" onSubmit={(event) => { event.preventDefault(); resolveInvoice(invoice.invoice_id as number, invoice.invoice_amount - invoice.resolved_amount); }}><input name="recipient" required placeholder="Destinatario" defaultValue="Propietario o proveedor" /><input name="amount" required type="number" min="0.01" step="0.01" defaultValue={Math.max(0, invoice.invoice_amount - invoice.resolved_amount)} /><select name="mode" defaultValue="reintegro_mes_vencido"><option value="reintegro_mes_vencido">Reintegro a mes vencido</option><option value="pago_directo">Pago directo</option><option value="compensacion_proveedor">Compensación</option></select><button type="submit">Confirmar resolución</button><button type="button" onClick={() => setResolveId(null)}>Cancelar</button></form>}
          </article>)}
        </div>
      </section>}
      {activeSection === "operacion" && <section className="workflow-panel" aria-labelledby="workflow-title">
        <div className="section-heading"><div><p className="eyebrow">Circuito administrativo</p><h2 id="workflow-title">De la recepción al pago</h2></div><span className="shortcut">Trazabilidad por expediente</span></div>
        <div className="workflow-list">
          {["1. Recibida", "2. Validación y verificación", "3. Imputación a secretarías", "4. Liquidación y documentación", "5. Seguimiento en expediente", "6. Pago confirmado"].map((step, index) => <div key={step} className={index === 0 ? "workflow-step current" : "workflow-step"}><b>{step}</b><span>{["Se registra factura y archivo original.", "Controlar puntos facturados, nuevos, duplicados y montos.", "Distribuir el importe y preparar el detalle para Contaduría.", "Guardar fecha, liquidación, alcance y expediente vinculado.", "Consultar avance usando expediente y alcance.", "Registrar pago o compensación y conservar historial."][index]}</span></div>)}
        </div>
        <p className="message">La API actual cubre recepción, liquidación individual y resolución de pago. La validación masiva, liquidación global, expediente/alcance y consulta histórica son las próximas operaciones de backend.</p>
      </section>}
      {activeSection === "inicio" && <section className="status-grid" aria-label="Resumen del padrón">
        <div><strong>{report?.missing ?? invoiceInbox.filter((invoice) => invoice.status === "faltante").length}</strong><span>Facturas faltantes</span></div>
        <div><strong>{report?.invoices ?? 0}</strong><span>Facturas registradas</span></div>
        <div><strong>{report ? `$${report.paid_amount.toLocaleString("es-AR")}` : "-"}</strong><span>Importe resuelto</span></div>
      </section>}
      {["historial", "catalogos", "usuarios"].includes(activeSection) && <section className="empty-section">
        <p className="eyebrow">Próxima etapa</p>
        <h2>{activeSection === "usuarios" ? "Gestión de usuarios" : activeSection === "catalogos" ? "Catálogos maestros" : "Historial y auditoría"}</h2>
        <p>Este módulo está previsto en la arquitectura, pero todavía no tiene operaciones completas en la API. La navegación ya queda separada para incorporarlo sin volver a mezclarlo con la operación diaria.</p>
        <span className="status-chip">Backend pendiente</span>
      </section>}
        </div>
      </div>
    </main>
  );
}
