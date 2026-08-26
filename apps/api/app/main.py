from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Account, Dependency, Provider, Secretary, ServicePoint, ServiceType
from .schemas import (
    AccountCreate,
    AccountRead,
    DependencyCreate,
    DependencyRead,
    ProviderCreate,
    ProviderRead,
    SecretaryCreate,
    SecretaryRead,
    ServicePointCreate,
    ServicePointRead,
    ServiceTypeCreate,
    ServiceTypeRead,
)

app = FastAPI(
    title="Registro Maestro de Servicios Municipales",
    version="0.1.0",
    description="API para consultar y mantener el padrón maestro de puntos de servicio.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/puntos-servicio", tags=["puntos de servicio"])
def search_service_points(
    query: str | None = Query(default=None, min_length=1),
    database: Session = Depends(get_db),
) -> dict[str, object]:
    statement = select(ServicePoint).order_by(ServicePoint.name)
    if query:
        pattern = f"%{query.strip()}%"
        statement = statement.where(
            or_(ServicePoint.code.ilike(pattern), ServicePoint.name.ilike(pattern), ServicePoint.address.ilike(pattern))
        )
    items = list(database.scalars(statement))
    return {"items": [ServicePointRead.model_validate(item) for item in items], "query": query, "total": len(items)}


def create_crud_routes(create_schema, read_schema, model, route: str):
    @app.post(route, response_model=read_schema, status_code=status.HTTP_201_CREATED, tags=[route.strip("/")])
    def create_item(payload: create_schema, database: Session = Depends(get_db)):
        item = model(**payload.model_dump())
        database.add(item)
        database.commit()
        database.refresh(item)
        return item

    @app.get(route, response_model=list[read_schema], tags=[route.strip("/")])
    def list_items(database: Session = Depends(get_db)):
        return list(database.scalars(select(model).order_by(model.id)))


create_crud_routes(SecretaryCreate, SecretaryRead, Secretary, "/api/v1/secretarias")
create_crud_routes(DependencyCreate, DependencyRead, Dependency, "/api/v1/dependencias")
create_crud_routes(ProviderCreate, ProviderRead, Provider, "/api/v1/proveedores")
create_crud_routes(ServiceTypeCreate, ServiceTypeRead, ServiceType, "/api/v1/servicios")


@app.post("/api/v1/puntos-servicio", response_model=ServicePointRead, status_code=status.HTTP_201_CREATED, tags=["puntos de servicio"])
def create_service_point(payload: ServicePointCreate, database: Session = Depends(get_db)):
    item = ServicePoint(**payload.model_dump())
    database.add(item)
    database.commit()
    database.refresh(item)
    return item


@app.get("/api/v1/puntos-servicio/{item_id}", response_model=ServicePointRead, tags=["puntos de servicio"])
def get_service_point(item_id: int, database: Session = Depends(get_db)):
    item = database.get(ServicePoint, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Punto de servicio no encontrado")
    return item


@app.post("/api/v1/cuentas", response_model=AccountRead, status_code=status.HTTP_201_CREATED, tags=["cuentas"])
def create_account(payload: AccountCreate, database: Session = Depends(get_db)):
    item = Account(**payload.model_dump())
    database.add(item)
    database.commit()
    database.refresh(item)
    return item
