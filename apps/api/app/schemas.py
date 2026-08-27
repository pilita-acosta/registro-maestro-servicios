from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class SecretaryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class SecretaryRead(SecretaryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class DomicileCreate(BaseModel):
    address: str = Field(min_length=3, max_length=240)
    notes: str | None = None


class DomicileRead(DomicileCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class RentalPropertyCreate(BaseModel):
    owner_name: str = Field(min_length=2, max_length=160)
    lease_file_reference: str | None = None
    starts_at: date
    ends_at: date | None = None
    domicile_id: int


class RentalPropertyRead(RentalPropertyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class DependencyCreate(BaseModel):
    code: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=2, max_length=160)
    domicile_id: int


class DependencyRead(DependencyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class ProviderCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    tax_id: str | None = None


class ProviderRead(ProviderCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class ServiceTypeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)


class ServiceTypeRead(ServiceTypeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class ServicePointCreate(BaseModel):
    code: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=2, max_length=160)
    status: str = "activo"
    notes: str | None = None
    dependency_id: int | None = None
    domicile_id: int


class ServicePointRead(ServicePointCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    address: str | None = None


class AccountCreate(BaseModel):
    external_code: str = Field(min_length=1, max_length=80)
    nis: str | None = None
    service_point_id: int
    provider_id: int
    service_type_id: int
    contract_id: int


class AccountRead(AccountCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class ContractCreate(BaseModel):
    code: str = Field(min_length=1, max_length=60)
    start_date: date
    end_date: date | None = None
    billing_frequency: str = Field(default="mensual", min_length=3, max_length=30)
    provider_id: int
    service_type_id: int


class ContractRead(ContractCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class AssignmentCreate(BaseModel):
    dependency_id: int
    secretary_id: int
    starts_at: date
    ends_at: date | None = None
    reason: str | None = None
    changed_by: str | None = None


class ExpectedInvoiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    period: str
    due_date: date
    delivery_deadline: date
    status: str
    responsible: str | None
    cutoff_risk: str
    account_id: int


class InvoiceCreate(BaseModel):
    number: str = Field(min_length=1, max_length=100)
    period: str = Field(pattern=r"^\d{4}-\d{2}$")
    issued_at: date | None = None
    due_date: date | None = None
    amount: float = Field(ge=0)
    resolution_mode: str = "reintegro_mes_vencido"
    original_file: str | None = None
    account_id: int


class InvoiceRead(InvoiceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str


class InvoiceClaimCreate(BaseModel):
    message: str = Field(min_length=3, max_length=500)
    responsible: str | None = None


class InvoiceClaimRead(InvoiceClaimCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str


class InvoiceReceiveCreate(BaseModel):
    number: str = Field(min_length=1, max_length=100)
    amount: float = Field(ge=0)
    issued_at: date | None = None
    due_date: date | None = None
    resolution_mode: str = "reintegro_mes_vencido"
    original_file: str | None = None


class LiquidationCreate(BaseModel):
    secretary_id: int
    resolution_mode: str = "reintegro_mes_vencido"


class LiquidationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    period: str
    status: str
    resolution_mode: str


class InvoiceAllocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    amount: float
    percentage: float
    invoice_id: int
    secretary_id: int


class AuditEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    entity_type: str
    entity_id: int
    action: str
    details: str | None
    actor: str
    created_at: datetime


class PaymentResolutionCreate(BaseModel):
    mode: str = Field(pattern=r"^(reintegro_mes_vencido|compensacion_proveedor|pago_directo|pago_propietario)$")
    amount: float = Field(gt=0)
    recipient: str = Field(min_length=2, max_length=160)
    reference: str | None = Field(default=None, max_length=160)
    resolved_at: date | None = None


class PaymentResolutionRead(PaymentResolutionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    invoice_id: int


class CompensationSummaryCreate(BaseModel):
    reference: str = Field(min_length=2, max_length=160)
    period: str = Field(pattern=r"^\d{4}-\d{2}$")
    reported_amount: float = Field(ge=0)
    provider_id: int


class CompensationSummaryRead(CompensationSummaryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    validated_amount: float
    status: str


class PhoneLineCreate(BaseModel):
    number: str = Field(min_length=3, max_length=40)
    plan: str | None = None
    user_or_destination: str | None = None
    starts_at: date
    ends_at: date | None = None
    provider_id: int


class PhoneLineRead(PhoneLineCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str


class MobileDeviceCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=80)
    model: str = Field(min_length=1, max_length=80)
    imei: str = Field(min_length=8, max_length=40)
    inventory_reference: str | None = None
    line_id: int | None = None


class MobileDeviceRead(MobileDeviceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str


class PhoneIncidentCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=160)
    description: str = Field(min_length=3)
    provider_reference: str | None = None
    opened_at: date
    line_id: int | None = None
    device_id: int | None = None


class PhoneIncidentRead(PhoneIncidentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    resolution: str | None
    closed_at: date | None


class ImportBatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filename: str
    status: str
    sheet_count: int
    row_count: int
    valid_row_count: int
    error_row_count: int
    warnings: str | None
    created_at: datetime
