from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from services.validator.engine import EAOSValidatorEngine

app = FastAPI(title="EAOS Web Dashboard")

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard() -> HTMLResponse:
    engine = EAOSValidatorEngine(ROOT_PATH)
    report = engine.run_validation()

    status_bg = (
        "bg-green-100 text-green-800 border-green-200"
        if report.overall_passed
        else "bg-red-100 text-red-800 border-red-200"
    )
    status_label = "HIẾN PHÁP HỢP CHUẨN" if report.overall_passed else "CÓ VI PHẠM"

    rules_html = ""
    for res in report.results:
        color = "green" if res.passed else "red"
        symbol = "✔" if res.passed else "✘"
        details_list = ""
        if res.details:
            details_list = (
                "<ul class='mt-2 list-disc list-inside text-xs text-amber-900 "
                "space-y-1 bg-amber-50 p-2 rounded border border-amber-200'>"
            )
            for detail in res.details:
                details_list += f"<li>{detail}</li>"
            details_list += "</ul>"

        rules_html += f"""
        <div class="p-4 bg-white rounded-lg border border-{color}-200 shadow-sm">
            <div class="flex items-center space-x-2">
                <span class="text-lg font-bold text-{color}-600">{symbol}</span>
                <h3 class="text-sm font-semibold text-gray-900">{res.rule_name}</h3>
            </div>
            <p class="mt-1 text-xs text-gray-600">{res.message}</p>
            {details_list}
        </div>
        """

    html_head = (
        "<!DOCTYPE html>\n"
        '<html lang="vi" class="dark">\n'
        "<head>\n"
        '    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        "    <title>EAOS Control Room</title>\n"
        '    <script src="https://cdn.tailwindcss.com"></script>\n'
        "</head>\n"
    )

    html_body = f"""<body class="bg-gray-50 text-gray-900 font-sans p-6">
    <div class="max-w-4xl mx-auto space-y-6">
        <div class="border-b border-gray-200 pb-4">
            <h1 class="text-2xl font-bold text-gray-900">EAOS Control Room</h1>
            <p class="text-xs text-gray-500 mt-1">Hệ điều hành kiểm toán kiến trúc tự thích ứng</p>
        </div>

        <div class="rounded-lg p-4 border {status_bg} flex items-center justify-between">
            <div>
                <h3 class="text-sm font-bold">Trạng thái: {status_label}</h3>
                <p class="text-xs mt-1">Đã hoàn tất kiểm toán ranh giới mã nguồn.</p>
            </div>
        </div>

        <div class="space-y-4">
            {rules_html}
        </div>
    </div>
</body>
</html>"""

    return HTMLResponse(content=html_head + html_body)
