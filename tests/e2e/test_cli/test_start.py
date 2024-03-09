from pathlib import Path

import httpx
import pytest


@pytest.mark.asyncio
async def test_blitz_app_urls(blitz_app: None) -> None:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get("http://0.0.0.0:8100/admin")
        assert response.status_code == 200
        response = await client.get("http://0.0.0.0:8100/api/docs")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_blitz_app_redirect(blitz_app_path: Path, blitz_app: None) -> None:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get("http://0.0.0.0:8100")
        assert response.status_code == 200
        assert response.url.path == f"/dashboard/projects/{blitz_app_path.name}/"
