import io
import zipfile

import pytest

from src.api.v1.export import export

DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _document_xml(content: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        return archive.read("word/document.xml").decode()


async def test_export_portfolio_docx(client, admin_headers):
    response = await client.get("/api/v1/export/portfolio/", headers=admin_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == DOCX
    assert "Semochkin_portfolio_ru.docx" in response.headers["content-disposition"]
    xml = _document_xml(response.content)
    assert "Алексей Сёмочкин" in xml
    assert "SkolStream" in xml          # проекты из базы
    assert "Опыт работы".upper() in xml  # заголовок раздела


async def test_export_portfolio_english(client, admin_headers):
    response = await client.get("/api/v1/export/portfolio/", params={"lang": "en"}, headers=admin_headers)
    assert response.status_code == 200
    xml = _document_xml(response.content)
    assert "Aleksei Semochkin" in xml
    assert "EXPERIENCE" in xml


@pytest.fixture(autouse=True)
def reset_export_state():
    export._cache.clear()
    export._hits.clear()


async def test_export_is_public(client):
    response = await client.get("/api/v1/export/portfolio/")
    assert response.status_code == 200
    assert response.headers["content-type"] == DOCX


async def test_export_rate_limit(client):
    for _ in range(export.RATE_LIMIT):
        assert (await client.get("/api/v1/export/portfolio/")).status_code == 200
    assert (await client.get("/api/v1/export/portfolio/")).status_code == 429
