import os
from typing import Optional

from fastapi import Header, HTTPException, status

API_KEY = os.getenv("BOOKS_API_KEY", "cw1-secret-key")


def require_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key"
        )
