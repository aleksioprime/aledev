import io
import zipfile

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


async def test_export_requires_admin(client):
    response = await client.get("/api/v1/export/portfolio/")
    assert response.status_code in (401, 403)
