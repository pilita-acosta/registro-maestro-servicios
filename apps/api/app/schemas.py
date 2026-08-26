from pydantic import BaseModel, ConfigDict, Field


class SecretaryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class SecretaryRead(SecretaryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class DependencyCreate(BaseModel):
    code: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=2, max_length=160)
    address: str | None = None
    secretary_id: int | None = None


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
    address: str | None = None
    status: str = "activo"
    notes: str | None = None
    dependency_id: int | None = None


class ServicePointRead(ServicePointCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AccountCreate(BaseModel):
    external_code: str = Field(min_length=1, max_length=80)
    nis: str | None = None
    service_point_id: int
    provider_id: int
    service_type_id: int


class AccountRead(AccountCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool
