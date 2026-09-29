async def test_public_page_has_seeded_content(client):
    r = await client.get("/api/v1/mentoring/")
    assert r.status_code == 200
    data = r.json()
    assert {t["lang"] for t in data["translations"]} == {"ru", "en"}
    assert [m["key"] for m in data["metrics"]] == ["projects", "prizes", "programs"]


async def test_update_page_replaces_translations_and_metrics(client, admin_headers):
    page = (await client.get("/api/v1/mentoring/admin/", headers=admin_headers)).json()
    body = {
        "is_published": True,
        "translations": [
            {"lang": t["lang"], "kicker": t["kicker"], "title_start": "Новый заголовок",
             "title_accent": t["title_accent"], "lead": t["lead"]}
            for t in page["translations"]
        ],
        # те же ключи метрик: замена не должна упираться в уникальность
        "metrics": [
            {"key": m["key"], "value": "99", "order": m["order"],
             "translations": [{"lang": t["lang"], "label": t["label"]} for t in m["translations"]]}
            for m in page["metrics"]
        ],
    }
    r = await client.put("/api/v1/mentoring/", json=body, headers=admin_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert {t["title_start"] for t in data["translations"]} == {"Новый заголовок"}
    assert {m["value"] for m in data["metrics"]} == {"99"}

    public = (await client.get("/api/v1/mentoring/")).json()
    assert {m["value"] for m in public["metrics"]} == {"99"}


async def test_update_requires_auth(client):
    r = await client.put("/api/v1/mentoring/", json={"translations": []})
    assert r.status_code == 403
