from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    data: Any = None
    error: str | None = None


def success_response(data: Any) -> dict:
    return {"data": data}


def error_response(message: str) -> dict:
    return {"error": message}
