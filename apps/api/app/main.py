from fastapi import FastAPI, Query

app = FastAPI(
    title="Registro Maestro de Servicios Municipales",
    version="0.1.0",
    description="API para consultar y mantener el padrón maestro de puntos de servicio.",
)


@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/puntos-servicio", tags=["puntos de servicio"])
def search_service_points(
    query: str | None = Query(default=None, min_length=1),
) -> dict[str, object]:
    """Contrato inicial de búsqueda; la persistencia se incorpora en el siguiente corte."""
    return {"items": [], "query": query, "total": 0}
