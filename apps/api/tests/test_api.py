from fastapi.testclient import TestClient
import pytest

from app.database import Base, engine
from app.main import app, seed_demo_data


@pytest.fixture(autouse=True)
def reset_database():
    """Starts every test with the same small, isolated master-data set."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_and_summary_are_available(client: TestClient):
    assert client.get("/health").json() == {"status": "ok"}

    summary = client.get("/api/v1/reportes/resumen")

    assert summary.status_code == 200
    assert summary.json()["expected"] == 2
    assert summary.json()["missing"] == 1


def test_service_point_grid_returns_columns_filters_and_detail(client: TestClient):
    response = client.get("/api/v1/puntos-servicio", params={"provider": "EDELAP"})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    row = body["items"][0]
    assert row["account"] == "EDE-458921"
    assert row["secretary"] == "Secretaría de Hacienda"
    assert row["service"] == "Electricidad"
    assert row["provider"] == "EDELAP"
    assert row["dependency"] == "Torre 1 - Oficinas"

    detail = client.get(f"/api/v1/puntos-servicio/{row['id']}/detalle")

    assert detail.status_code == 200
    assert detail.json()["accounts"] == [
        {
            "id": 1,
            "external_code": "EDE-458921",
            "nis": "NIS-458921",
            "provider": "EDELAP",
            "service": "Electricidad",
            "contract": "CT-DEMO-2026",
        }
    ]


def test_invoice_can_be_received_liquidated_paid_and_audited(client: TestClient):
    inbox = client.get("/api/v1/bandeja-facturas").json()
    expected_invoice = next(item for item in inbox if item["period"] == "2026-06")

    received = client.post(
        f"/api/v1/facturas-esperadas/{expected_invoice['id']}/recibir",
        json={"number": "TEST-0001", "amount": 1500, "resolution_mode": "pago_directo"},
    )

    assert received.status_code == 201
    invoice = received.json()

    liquidated = client.post(
        f"/api/v1/facturas/{invoice['id']}/liquidar",
        json={"secretary_id": 1, "resolution_mode": "pago_directo"},
    )
    assert liquidated.status_code == 201

    paid = client.post(
        f"/api/v1/facturas/{invoice['id']}/resolver",
        json={"mode": "pago_directo", "amount": 1500, "recipient": "Proveedor de prueba"},
    )
    assert paid.status_code == 201

    audit = client.get(f"/api/v1/facturas/{invoice['id']}/auditoria")
    assert audit.status_code == 200
    assert [event["action"] for event in audit.json()] == ["recibida", "liquidada", "resolucion_registrada"]


def test_payment_cannot_exceed_invoice_amount(client: TestClient):
    invoice_id = client.post(
        "/api/v1/facturas-esperadas/1/recibir",
        json={"number": "TEST-0002", "amount": 100, "resolution_mode": "pago_directo"},
    ).json()["id"]

    assert client.post(
        f"/api/v1/facturas/{invoice_id}/liquidar",
        json={"secretary_id": 1, "resolution_mode": "pago_directo"},
    ).status_code == 201

    response = client.post(
        f"/api/v1/facturas/{invoice_id}/resolver",
        json={"mode": "pago_directo", "amount": 101, "recipient": "Proveedor de prueba"},
    )
    assert response.status_code == 422
