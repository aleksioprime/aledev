import time

import pytest

from src.services import feedback as feedback_module
from src.services.mailer import MailResult


@pytest.fixture(autouse=True)
def no_external_calls(monkeypatch):
    async def human(self, **kwargs):
        return True

    sent = []

    async def send(self, msg, text, html):
        sent.append(msg)
        return MailResult("yandex", [])

    monkeypatch.setattr(feedback_module.FeedbackService, "verify_feedback_request", human)
    monkeypatch.setattr(feedback_module.Mailer, "send", send)
    return sent


def form(**overrides):
    body = {
        "kind": "order", "name": "Иван", "email": "ivan@example.com",
        "service": "web", "budget": "discuss", "deadline": "к весне",
        "message": "Нужна образовательная платформа", "lang": "ru",
        "captcha_token": "x" * 20, "website": "", "form_started_at": int(time.time() * 1000) - 5000,
    }
    body.update(overrides)
    return body


async def test_order_is_saved_and_emailed(client, admin_headers, no_external_calls):
    r = await client.post("/api/v1/feedback/", json=form())
    assert r.status_code == 202, r.text
    feedback_id = r.json()["id"]

    # фоновая задача выполняется до завершения ответа в ASGITransport
    assert len(no_external_calls) == 1
    assert no_external_calls[0]["Reply-To"] == "ivan@example.com"

    items = (await client.get("/api/v1/feedback/", params={"limit": 50}, headers=admin_headers)).json()["items"]
    item = next(i for i in items if i["id"] == feedback_id)
    assert item["email_status"] == "sent"
    assert item["service"] == "web"


async def test_question_drops_order_fields(client, admin_headers):
    r = await client.post("/api/v1/feedback/", json=form(kind="question"))
    assert r.status_code == 202
    feedback_id = r.json()["id"]
    items = (await client.get("/api/v1/feedback/", params={"limit": 50}, headers=admin_headers)).json()["items"]
    item = next(i for i in items if i["id"] == feedback_id)
    assert item["service"] is None and item["budget"] is None and item["deadline"] is None


async def test_validation(client):
    r = await client.post("/api/v1/feedback/", json=form(email="bad", message="short"))
    assert r.status_code == 422
    fields = {e["loc"][-1] for e in r.json()["detail"]}
    assert {"email", "message"} <= fields


@pytest.mark.parametrize("kind, service", [
    ("order", "hack"),
    ("order", "individual"),   # формат обучения не подходит заказу
    ("training", "web"),       # тип работ не подходит обучению
])
async def test_service_must_match_kind(client, kind, service):
    r = await client.post("/api/v1/feedback/", json=form(kind=kind, service=service))
    assert r.status_code == 422


async def test_training_request(client, admin_headers, no_external_calls):
    r = await client.post("/api/v1/feedback/", json=form(kind="training", service="team", budget=None))
    assert r.status_code == 202, r.text
    assert "Обучение" in no_external_calls[-1]["Subject"]

    stats = (await client.get("/api/v1/feedback/stats/", headers=admin_headers)).json()
    assert stats["trainings"] >= 1
    items = (await client.get("/api/v1/feedback/", params={"kind": "training"}, headers=admin_headers)).json()["items"]
    assert items and all(i["kind"] == "training" for i in items)


async def test_admin_endpoints_require_auth(client):
    assert (await client.get("/api/v1/feedback/")).status_code == 403
