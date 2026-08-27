"use client";

import { FormEvent, useEffect, useState } from "react";

type ServicePoint = {
  id: number;
  code: string;
  name: string;
  address: string | null;
  status: string;
  dependency_id: number | null;
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

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [query, setQuery] = useState("");
  const [items, setItems] = useState<ServicePoint[]>([]);
  const [message, setMessage] = useState("Escribí un dato para comenzar la búsqueda.");
  const [isLoading, setIsLoading] = useState(false);
  const [invoiceInbox, setInvoiceInbox] = useState<InvoiceInboxItem[]>([]);
  const [importMessage, setImportMessage] = useState("");
  const [report, setReport] = useState<ReportSummary | null>(null);
  const [selectedPoint, setSelectedPoint] = useState<ServicePointDetail | null>(null);
  const [receiveId, setReceiveId] = useState<number | null>(null);
  const [resolveId, setResolveId] = useState<number | null>(null);

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

  async function openPoint(id: number) {
    const response = await fetch(`${apiUrl}/api/v1/puntos-servicio/${id}/detalle`);
    if (response.ok) setSelectedPoint(await response.json() as ServicePointDetail);
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
          {items.map((item) => <article key={item.id} className="result" onClick={() => openPoint(item.id)}>
            <strong>{item.name}</strong>
            <span>{item.code} · {item.address ?? "Domicilio pendiente"}</span>
            <small>{item.status}</small>
          </article>)}
        </div>}
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
          <label className="file-button">Previsualizar Excel<input type="file" accept=".xlsx,.xlsm" onChange={previewImport} /></label>
          <button type="button" className="link-button" disabled>Ver gastos · Próximamente</button>
        </div>
        {importMessage && <p className="message" role="status">{importMessage}</p>}
      </section>
      <section className="invoice-panel" aria-labelledby="invoice-title">
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
      </section>
      <section className="status-grid" aria-label="Resumen del padrón">
        <div><strong>{report?.missing ?? invoiceInbox.filter((invoice) => invoice.status === "faltante").length}</strong><span>Facturas faltantes</span></div>
        <div><strong>{report?.invoices ?? 0}</strong><span>Facturas registradas</span></div>
        <div><strong>{report ? `$${report.paid_amount.toLocaleString("es-AR")}` : "-"}</strong><span>Importe resuelto</span></div>
      </section>
    </main>
  );
}
