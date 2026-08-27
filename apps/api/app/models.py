from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Secretary(Base):
    __tablename__ = "secretarias"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    assignments: Mapped[list["DependencySecretaryAssignment"]] = relationship(back_populates="secretary")


class Domicile(Base):
    __tablename__ = "domicilios"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(240), index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    dependencies: Mapped[list["Dependency"]] = relationship(back_populates="domicile")
    service_points: Mapped[list["ServicePoint"]] = relationship(back_populates="domicile")
    rentals: Mapped[list["RentalProperty"]] = relationship(back_populates="domicile")


class RentalProperty(Base):
    __tablename__ = "inmuebles_alquilados"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_name: Mapped[str] = mapped_column(String(160), index=True)
    lease_file_reference: Mapped[str | None] = mapped_column(String(120))
    starts_at: Mapped[date] = mapped_column(Date)
    ends_at: Mapped[date | None] = mapped_column(Date)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    domicile_id: Mapped[int] = mapped_column(ForeignKey("domicilios.id"))
    domicile: Mapped[Domicile] = relationship(back_populates="rentals")


class Dependency(Base):
    __tablename__ = "dependencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    domicile_id: Mapped[int] = mapped_column(ForeignKey("domicilios.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    domicile: Mapped[Domicile] = relationship(back_populates="dependencies")
    service_points: Mapped[list["ServicePoint"]] = relationship(back_populates="dependency")
    assignments: Mapped[list["DependencySecretaryAssignment"]] = relationship(back_populates="dependency")


class Provider(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    tax_id: Mapped[str | None] = mapped_column(String(30), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    accounts: Mapped[list["Account"]] = relationship(back_populates="provider")
    compensation_summaries: Mapped[list["CompensationSummary"]] = relationship(back_populates="provider")


class ServiceType(Base):
    __tablename__ = "tipos_servicio"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    accounts: Mapped[list["Account"]] = relationship(back_populates="service_type")


class Contract(Base):
    __tablename__ = "contratos"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    billing_frequency: Mapped[str] = mapped_column(String(30), default="mensual")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"))
    service_type_id: Mapped[int] = mapped_column(ForeignKey("tipos_servicio.id"))
    provider: Mapped[Provider] = relationship()
    service_type: Mapped[ServiceType] = relationship()
    accounts: Mapped[list["Account"]] = relationship(back_populates="contract")


class DependencySecretaryAssignment(Base):
    __tablename__ = "asignaciones_dependencia_secretaria"

    id: Mapped[int] = mapped_column(primary_key=True)
    starts_at: Mapped[date] = mapped_column(Date, nullable=False)
    ends_at: Mapped[date | None] = mapped_column(Date)
    reason: Mapped[str | None] = mapped_column(String(240))
    changed_by: Mapped[str | None] = mapped_column(String(120))
    dependency_id: Mapped[int] = mapped_column(ForeignKey("dependencias.id"))
    secretary_id: Mapped[int] = mapped_column(ForeignKey("secretarias.id"))
    dependency: Mapped[Dependency] = relationship(back_populates="assignments")
    secretary: Mapped[Secretary] = relationship(back_populates="assignments")


class ServicePoint(Base):
    __tablename__ = "puntos_servicio"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    status: Mapped[str] = mapped_column(String(30), default="activo", index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    dependency_id: Mapped[int | None] = mapped_column(ForeignKey("dependencias.id"))
    domicile_id: Mapped[int] = mapped_column(ForeignKey("domicilios.id"))
    dependency: Mapped[Dependency | None] = relationship(back_populates="service_points")
    domicile: Mapped[Domicile] = relationship(back_populates="service_points")
    accounts: Mapped[list["Account"]] = relationship(back_populates="service_point")


class Account(Base):
    __tablename__ = "cuentas"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_code: Mapped[str] = mapped_column(String(80), index=True)
    nis: Mapped[str | None] = mapped_column(String(80), index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    service_point_id: Mapped[int] = mapped_column(ForeignKey("puntos_servicio.id"))
    provider_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"))
    service_type_id: Mapped[int] = mapped_column(ForeignKey("tipos_servicio.id"))
    contract_id: Mapped[int] = mapped_column(ForeignKey("contratos.id"))
    service_point: Mapped[ServicePoint] = relationship(back_populates="accounts")
    provider: Mapped[Provider] = relationship(back_populates="accounts")
    service_type: Mapped[ServiceType] = relationship(back_populates="accounts")
    contract: Mapped[Contract] = relationship(back_populates="accounts")
    expected_invoices: Mapped[list["ExpectedInvoice"]] = relationship(back_populates="account")
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="account")


class Liquidation(Base):
    __tablename__ = "liquidaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    period: Mapped[str] = mapped_column(String(7), index=True)
    status: Mapped[str] = mapped_column(String(40), default="en_preparacion", index=True)
    resolution_mode: Mapped[str] = mapped_column(String(40), default="reintegro_mes_vencido")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="liquidation")


class ExpectedInvoice(Base):
    __tablename__ = "facturas_esperadas"

    id: Mapped[int] = mapped_column(primary_key=True)
    period: Mapped[str] = mapped_column(String(7), index=True)
    due_date: Mapped[date] = mapped_column(Date)
    delivery_deadline: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="faltante", index=True)
    responsible: Mapped[str | None] = mapped_column(String(120))
    cutoff_risk: Mapped[str] = mapped_column(String(20), default="bajo", index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("cuentas.id"))
    account: Mapped[Account] = relationship(back_populates="expected_invoices")
    claims: Mapped[list["InvoiceClaim"]] = relationship(back_populates="expected_invoice")


class InvoiceClaim(Base):
    __tablename__ = "reclamos_factura"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    message: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="abierto")
    responsible: Mapped[str | None] = mapped_column(String(120))
    expected_invoice_id: Mapped[int] = mapped_column(ForeignKey("facturas_esperadas.id"))
    expected_invoice: Mapped[ExpectedInvoice] = relationship(back_populates="claims")


class AuditEvent(Base):
    __tablename__ = "eventos_auditoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(80), index=True)
    entity_id: Mapped[int] = mapped_column(index=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    details: Mapped[str | None] = mapped_column(Text)
    actor: Mapped[str] = mapped_column(String(120), default="sistema")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class Invoice(Base):
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(100), index=True)
    period: Mapped[str] = mapped_column(String(7), index=True)
    issued_at: Mapped[date | None] = mapped_column(Date)
    due_date: Mapped[date | None] = mapped_column(Date)
    amount: Mapped[float] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(40), default="recibida", index=True)
    resolution_mode: Mapped[str] = mapped_column(String(40), default="reintegro_mes_vencido")
    original_file: Mapped[str | None] = mapped_column(String(240))
    account_id: Mapped[int] = mapped_column(ForeignKey("cuentas.id"))
    liquidation_id: Mapped[int | None] = mapped_column(ForeignKey("liquidaciones.id"))
    account: Mapped[Account] = relationship(back_populates="invoices")
    liquidation: Mapped[Liquidation | None] = relationship(back_populates="invoices")
    allocations: Mapped[list["InvoiceAllocation"]] = relationship(back_populates="invoice")
    payment_resolutions: Mapped[list["PaymentResolution"]] = relationship(back_populates="invoice")
    compensation_summary_id: Mapped[int | None] = mapped_column(ForeignKey("resumenes_compensacion.id"))
    compensation_summary: Mapped["CompensationSummary | None"] = relationship(back_populates="invoices")


class InvoiceAllocation(Base):
    __tablename__ = "imputaciones_factura"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(default=0)
    percentage: Mapped[float] = mapped_column(default=100)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("facturas.id"))
    secretary_id: Mapped[int] = mapped_column(ForeignKey("secretarias.id"))
    invoice: Mapped[Invoice] = relationship(back_populates="allocations")
    secretary: Mapped[Secretary] = relationship()


class PaymentResolution(Base):
    __tablename__ = "resoluciones_pago"

    id: Mapped[int] = mapped_column(primary_key=True)
    mode: Mapped[str] = mapped_column(String(40), index=True)
    amount: Mapped[float] = mapped_column(default=0)
    recipient: Mapped[str] = mapped_column(String(160))
    reference: Mapped[str | None] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(30), default="registrada", index=True)
    resolved_at: Mapped[date | None] = mapped_column(Date)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("facturas.id"))
    invoice: Mapped[Invoice] = relationship(back_populates="payment_resolutions")


class CompensationSummary(Base):
    __tablename__ = "resumenes_compensacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(160), index=True)
    period: Mapped[str] = mapped_column(String(7), index=True)
    reported_amount: Mapped[float] = mapped_column(default=0)
    validated_amount: Mapped[float] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(30), default="recibido", index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"))
    provider: Mapped[Provider] = relationship(back_populates="compensation_summaries")
    invoices: Mapped[list[Invoice]] = relationship(back_populates="compensation_summary")


class PhoneLine(Base):
    __tablename__ = "lineas_telefonicas"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    plan: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(30), default="activa", index=True)
    user_or_destination: Mapped[str | None] = mapped_column(String(160))
    starts_at: Mapped[date] = mapped_column(Date)
    ends_at: Mapped[date | None] = mapped_column(Date)
    provider_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"))
    provider: Mapped[Provider] = relationship()
    devices: Mapped[list["MobileDevice"]] = relationship(back_populates="line")
    incidents: Mapped[list["PhoneIncident"]] = relationship(back_populates="line")


class MobileDevice(Base):
    __tablename__ = "dispositivos_moviles"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(80))
    model: Mapped[str] = mapped_column(String(80))
    imei: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    inventory_reference: Mapped[str | None] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(30), default="en_stock", index=True)
    line_id: Mapped[int | None] = mapped_column(ForeignKey("lineas_telefonicas.id"))
    line: Mapped[PhoneLine | None] = relationship(back_populates="devices")
    incidents: Mapped[list["PhoneIncident"]] = relationship(back_populates="device")


class PhoneIncident(Base):
    __tablename__ = "incidencias_telefonia"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="abierta", index=True)
    provider_reference: Mapped[str | None] = mapped_column(String(100))
    resolution: Mapped[str | None] = mapped_column(Text)
    opened_at: Mapped[date] = mapped_column(Date)
    closed_at: Mapped[date | None] = mapped_column(Date)
    line_id: Mapped[int | None] = mapped_column(ForeignKey("lineas_telefonicas.id"))
    device_id: Mapped[int | None] = mapped_column(ForeignKey("dispositivos_moviles.id"))
    line: Mapped[PhoneLine | None] = relationship(back_populates="incidents")
    device: Mapped[MobileDevice | None] = relationship(back_populates="incidents")


class ImportBatch(Base):
    __tablename__ = "importaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(240))
    original_path: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(30), default="previsualizada", index=True)
    sheet_count: Mapped[int] = mapped_column(default=0)
    row_count: Mapped[int] = mapped_column(default=0)
    valid_row_count: Mapped[int] = mapped_column(default=0)
    error_row_count: Mapped[int] = mapped_column(default=0)
    warnings: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
