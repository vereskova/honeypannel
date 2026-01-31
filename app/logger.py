from datetime import datetime, timezone

async def log_request(request) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    ip = getattr(getattr(request, "client", None), "host", None)
    method = request.method
    path = request.url.path

    print(f"[{ts}] {ip} {method} {path}")
