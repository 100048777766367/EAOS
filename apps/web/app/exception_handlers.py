from fastapi import Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import Response

"""Web Application Exception Handlers."""


async def custom_http_exception_handler(
    request: Request,
    exc: Exception,
) -> Response:
    """Handles HTTP and system exceptions with HTML page or JSON depending on Accept header."""
    accept = request.headers.get("accept", "")
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", str(exc))

    if "text/html" in accept:
        btn_class = (
            "inline-block bg-cyan-600 hover:bg-cyan-500 "
            "text-white font-medium py-2 px-4 rounded-lg "
            "text-sm transition-colors"
        )
        html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Lỗi {status_code} - EAOS Web UI</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 flex items-center justify-center min-h-screen p-6">
    <div class="max-w-md w-full bg-slate-800 border border-slate-700 rounded-xl p-6 text-center space-y-4">
        <div class="text-5xl font-extrabold text-cyan-400">{status_code}</div>
        <h1 class="text-xl font-bold">Xảy ra lỗi truy cập</h1>
        <p class="text-sm text-slate-400">{detail}</p>
        <a href="/control-room" class="{btn_class}">
            Quay lại Control Room
        </a>
    </div>
</body>
</html>"""
        return HTMLResponse(
            content=html_content,
            status_code=status_code,
        )

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ERROR",
            "code": status_code,
            "detail": detail,
        },
    )
