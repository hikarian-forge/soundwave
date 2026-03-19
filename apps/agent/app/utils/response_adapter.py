from typing import Any

from schemas.base import Fail, Success, SuccessExtra


def adapt_response(response: Success | Fail | SuccessExtra) -> dict[str, Any]:
    """
    Converts a JSONResponse object to dictionary format.

    Note:
        This function serves as a compatibility layer during
        the transition period, allowing existing service layer
        code to work with new Pydantic response models.

    Args:
        response: Success, Fail, or SuccessExtra instance

    Returns:
        A dictionary containing the response data
    """
    if hasattr(response, "body"):
        import json

        return json.loads(response.body)
    else:
        return {
            "code": getattr(response, "code", 200),
            "msg": getattr(response, "msg", "OK"),
            "data": getattr(response, "data", None),
            "total": getattr(response, "total", None),
            "page": getattr(response, "page", None),
            "page_size": getattr(response, "page_size", None),
        }
