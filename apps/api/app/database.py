import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


database_url = os.getenv("DATABASE_URL", "sqlite:///./registro_maestro.db")
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def migrate_legacy_schema() -> None:
    if engine.dialect.name != "postgresql":
        return

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if "puntos_servicio" not in tables or "domicilios" not in tables:
        return

    dependency_columns = {column["name"] for column in inspector.get_columns("dependencias")}
    point_columns = {column["name"] for column in inspector.get_columns("puntos_servicio")}
    account_columns = {column["name"] for column in inspector.get_columns("cuentas")}
    invoice_columns = {column["name"] for column in inspector.get_columns("facturas")} if "facturas" in tables else set()

    with engine.begin() as connection:
        if "domicile_id" not in dependency_columns:
            connection.execute(text("ALTER TABLE dependencias ADD COLUMN domicile_id INTEGER"))
            connection.execute(text("""
                INSERT INTO domicilios (address)
                SELECT DISTINCT COALESCE(NULLIF(address, ''), 'Domicilio pendiente')
                FROM dependencias
                ON CONFLICT DO NOTHING
            """))
            connection.execute(text("""
                UPDATE dependencias AS dependency
                SET domicile_id = domicile.id
                FROM domicilios AS domicile
                WHERE domicile.address = COALESCE(NULLIF(dependency.address, ''), 'Domicilio pendiente')
            """))

        if "domicile_id" not in point_columns:
            connection.execute(text("ALTER TABLE puntos_servicio ADD COLUMN domicile_id INTEGER"))
            connection.execute(text("""
                INSERT INTO domicilios (address)
                SELECT DISTINCT COALESCE(NULLIF(service_point.address, ''), dependency.address, 'Domicilio pendiente')
                FROM puntos_servicio AS service_point
                LEFT JOIN dependencias AS dependency ON dependency.id = service_point.dependency_id
                ON CONFLICT DO NOTHING
            """))
            connection.execute(text("""
                UPDATE puntos_servicio AS service_point
                SET domicile_id = domicile.id
                                FROM domicilios AS domicile, dependencias AS dependency
                WHERE domicile.address = COALESCE(NULLIF(service_point.address, ''), dependency.address, 'Domicilio pendiente')
                                    AND dependency.id = service_point.dependency_id
            """))

        if "contract_id" not in account_columns:
            connection.execute(text("ALTER TABLE cuentas ADD COLUMN contract_id INTEGER"))

        if "liquidation_id" not in invoice_columns and "facturas" in tables:
            connection.execute(text("ALTER TABLE facturas ADD COLUMN liquidation_id INTEGER"))

        if "compensation_summary_id" not in invoice_columns and "facturas" in tables:
            connection.execute(text("ALTER TABLE facturas ADD COLUMN compensation_summary_id INTEGER"))
