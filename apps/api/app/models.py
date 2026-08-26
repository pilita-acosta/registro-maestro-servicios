from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Secretary(Base):
    __tablename__ = "secretarias"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    dependencies: Mapped[list["Dependency"]] = relationship(back_populates="secretary")


class Dependency(Base):
    __tablename__ = "dependencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    address: Mapped[str | None] = mapped_column(String(240))
    secretary_id: Mapped[int | None] = mapped_column(ForeignKey("secretarias.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    secretary: Mapped[Secretary | None] = relationship(back_populates="dependencies")
    service_points: Mapped[list["ServicePoint"]] = relationship(back_populates="dependency")


class Provider(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    tax_id: Mapped[str | None] = mapped_column(String(30), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    accounts: Mapped[list["Account"]] = relationship(back_populates="provider")


class ServiceType(Base):
    __tablename__ = "tipos_servicio"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    accounts: Mapped[list["Account"]] = relationship(back_populates="service_type")


class ServicePoint(Base):
    __tablename__ = "puntos_servicio"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    address: Mapped[str | None] = mapped_column(String(240), index=True)
    status: Mapped[str] = mapped_column(String(30), default="activo", index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    dependency_id: Mapped[int | None] = mapped_column(ForeignKey("dependencias.id"))
    dependency: Mapped[Dependency | None] = relationship(back_populates="service_points")
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
    service_point: Mapped[ServicePoint] = relationship(back_populates="accounts")
    provider: Mapped[Provider] = relationship(back_populates="accounts")
    service_type: Mapped[ServiceType] = relationship(back_populates="accounts")
