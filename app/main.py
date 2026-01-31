from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.logger import log_request
from app.alerts import send_alert

app = FastAPI(title="HoneyPanel")

SUSPICIOUS_PATHS = ["/admin", "/.env", "/config", "/login"]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    await log_request(request)
    return "<h1>Internal Portal</h1>"


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    await log_request(request)
    return "<h2>Login</h2>"


@app.post("/login")
async def login_submit(request: Request):
    await log_request(request)
    return JSONResponse({"error": "Invalid credentials"}, status_code=401)


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    await log_request(request)
    return "<h2>Admin Panel</h2>"

@app.post("/admin/login")
async def admin_login_submit(request: Request):
    await log_request(request)
    return JSONResponse({"detail": "Forbidden"}, status_code=403)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(path: str, request: Request):
    full_path = "/" + path
    ip = request.client.host

    await log_request(request)

    for bad in SUSPICIOUS_PATHS:
        if bad in full_path:
            send_alert(
                f"URGANCE: Suspicious request\n"
                f"IP: {ip}\n"
                f"Path: {full_path}"
            )
            break

    return JSONResponse({"status": "not_found"}, status_code=404)
