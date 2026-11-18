"""MllyMed API Marshrutizatori (Router)."""
from __future__ import annotations

from typing import Any
from .b2c_routes import handle_b2c_get, handle_b2c_post
from .b2b_routes import handle_b2b_get, handle_b2b_post


class ApiRouter:
    def __init__(self, bridge: Any):
        self.bridge = bridge

    def route_get(self, path: str, query: dict, role: str) -> tuple[dict, int]:
        """Barcha GET so'rovlarini yo'naltirish."""
        if path == "/api/health":
            return {"ok": True, "product": "MllyMed", "version": 2, "role": role}, 200

        if path == "/api/stats":
            return self.bridge.stats(), 200

        # 1. B2C yo'llarini tekshirish
        res, code = handle_b2c_get(self.bridge, path, query)
        if res is not None:
            return res, code

        # 2. B2B yo'llarini tekshirish
        res, code = handle_b2b_get(self.bridge, path, query, role)
        if res is not None:
            return res, code

        return {"error": "yo'l topilmadi"}, 404

    def route_post(self, path: str, body: dict, role: str, user: str) -> tuple[dict, int]:
        """Barcha POST so'rovlarini yo'naltirish."""
        # 1. B2C yo'llarini tekshirish
        res, code = handle_b2c_post(self.bridge, path, body)
        if res is not None:
            return res, code

        # 2. B2B yo'llarini tekshirish
        res, code = handle_b2b_post(self.bridge, path, body, role, user)
        if res is not None:
            return res, code

        return {"error": "yo'l topilmadi"}, 404
