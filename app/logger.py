from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict

LOG_PATH = Path("logs/requests.jsonl")


async def log_request(request) -> None:
    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8", errors="ignore")

    entry: Dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "client_ip": getattr(getattr(request, "client", None), "host", None),
        "method": request.method,
        "path": str(request.url.path),
        "query": str(request.url.query),
        "headers": dict(request.headers),
        "body": body_text,
    }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
