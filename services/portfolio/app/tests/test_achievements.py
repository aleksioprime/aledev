async def test_public_list_returns_seeded_published_achievements(client):
    r = await client.get("/api/v1/achievements/", params={"limit": 50, "offset": 1})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 12
    # избранные идут первыми
    assert all(item["is_featured"] for item in data["items"][:3])
    assert {t["lang"] for t in data["items"][0]["translations"]} == {"ru", "en"}


async def test_filter_by_scope(client):
    r = await client.get("/api/v1/achievements/", params={"scope": "students", "limit": 50})
    assert r.status_code == 200
    assert {item["scope"] for item in r.json()["items"]} == {"students"}


async def test_write_requires_auth(client):
    r = await client.post("/api/v1/achievements/", json={"category": "grant", "scope": "personal"})
    assert r.status_code == 403


async def test_crud_and_unpublished_visibility(client, admin_headers):
    body = {
        "category": "competition",
        "scope": "personal",
        "year": 2025,
        "is_published": False,
        "translations": [{"lang": "ru", "title": "Черновик"}],
    }
    r = await client.post("/api/v1/achievements/", json=body, headers=admin_headers)
    assert r.status_code == 201, r.text
    item_id = r.json()["id"]

    public = await client.get("/api/v1/achievements/", params={"limit": 100})
    assert item_id not in {i["id"] for i in public.json()["items"]}
    admin = await client.get("/api/v1/achievements/admin/", params={"limit": 100}, headers=admin_headers)
    assert item_id in {i["id"] for i in admin.json()["items"]}

    # замена переводов: в ответе должны быть только новые
    r = await client.patch(
        f"/api/v1/achievements/{item_id}/",
        json={"is_published": True, "translations": [
            {"lang": "ru", "title": "Новое название"},
            {"lang": "en", "title": "New title"},
        ]},
        headers=admin_headers,
    )
    assert r.status_code == 200, r.text
    titles = sorted(t["title"] for t in r.json()["translations"])
    assert titles == ["New title", "Новое название"]
    assert r.json()["is_published"] is True

    r = await client.delete(f"/api/v1/achievements/{item_id}/", headers=admin_headers)
    assert r.status_code == 204
    r = await client.delete(f"/api/v1/achievements/{item_id}/", headers=admin_headers)
    assert r.status_code == 404
