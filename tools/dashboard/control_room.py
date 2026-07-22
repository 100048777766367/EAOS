from pathlib import Path

from tools.metrics.architecture_metrics_calculator import (
    ArchitectureMetricsCalculator,
)
from tools.validate.architecture_validator import ArchitectureValidator


class ControlRoomDashboard:
    """Động cơ tổng hợp dữ liệu thời gian thực và sinh Control Room Dashboard HTML."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def render_html(self) -> str:
        validator = ArchitectureValidator(self.root_dir)
        validator_passed = validator.run_all_checks()
        violations = validator.violations

        metrics_calc = ArchitectureMetricsCalculator(self.root_dir)
        metrics_calc.calculate_all()
        score = metrics_calc.architecture_score
        packages_metrics = metrics_calc.metrics

        mermaid_path = self.root_dir / "generated" / "architecture" / "dependency_graph.md"
        mermaid_code = "graph TD\n    eaos_core['EAOS Operating System']"
        if mermaid_path.exists():
            content = mermaid_path.read_text(encoding="utf-8")
            if "```mermaid" in content:
                mermaid_code = content.split("```mermaid")[1].split("```")[0].strip()

        # Trích xuất dữ liệu chỉ số đóng gói mỏng với bẻ dòng cực sạch
        metrics_rows = ""
        for pkg, m in packages_metrics.items():
            metrics_rows += (
                '<tr class="hover:bg-gray-800/50">\n'
                '    <td class="px-4 py-2.5 font-mono '
                f'text-cyan-400 font-semibold">{pkg}</td>\n'
                f'    <td class="px-4 py-2.5 text-center">'
                f"{m['afferent_coupling_ca']}</td>\n"
                f'    <td class="px-4 py-2.5 text-center">'
                f"{m['efferent_coupling_ce']}</td>\n"
                f'    <td class="px-4 py-2.5 text-center">'
                f"{m['instability_i']}</td>\n"
                f'    <td class="px-4 py-2.5 text-center">'
                f"{m['abstractness_a']}</td>\n"
                f'    <td class="px-4 py-2.5 text-center '
                f'font-bold text-amber-400">'
                f"{m['distance_d']}</td>\n"
                "</tr>\n"
            )

        violations_html = ""
        if violations:
            violations_html = "<ul class='space-y-2 mt-2'>\n"
            for v in violations:
                violations_html += (
                    "    <li class='text-red-400 font-mono text-xs "
                    "bg-red-950/40 p-2.5 rounded border "
                    f"border-red-800/60'>• {v}</li>\n"
                )
            violations_html += "</ul>"
        else:
            violations_html = (
                "<p class='text-emerald-400 font-semibold text-sm mt-3'>\n"
                "✔ Không phát hiện bất kỳ vi phạm hiến pháp nào.</p>\n"
            )

        status_color = "emerald" if validator_passed else "rose"
        status_text = "HEALTHY (PASSED)" if validator_passed else "VIOLATIONS DETECTED"

        status_badge = (
            f'<span class="px-3 py-1 rounded-full text-xs font-bold '
            f"bg-{status_color}-500/20 text-{status_color}-400 border "
            f'border-{status_color}-500/30">● {status_text}</span>'
        )

        # Chia nhỏ chuỗi HTML lớn thành mảng để khống chế dòng code dưới 80 ký tự
        html_parts = [
            "<!DOCTYPE html>",
            '<html lang="vi" class="dark">',
            "<head>",
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            "    <title>EAOS Control Room Dashboard</title>",
            '    <script src="https://cdn.tailwindcss.com"></script>',
            '    <script type="module">',
            "        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';",
            "        mermaid.initialize({ startOnLoad: true, theme: 'dark' });",
            "    </script>",
            "</head>",
            '<body class="bg-gray-950 text-gray-100 font-sans min-h-screen p-6">',
            '    <div class="max-w-7xl mx-auto space-y-6">',
            '        <div class="flex items-center justify-between border-b border-gray-800 pb-4">',
            "            <div>",
            '                <h1 class="text-3xl font-extrabold '
            "text-transparent bg-clip-text bg-gradient-to-r "
            'from-cyan-400 to-blue-500">',
            "                    EAOS CONTROL ROOM",
            "                </h1>",
            '                <p class="text-xs text-gray-400 mt-1">Enterprise Architecture Operating System</p>',
            "            </div>",
            '            <div class="flex items-center space-x-3">',
            f"                {status_badge}",
            '                <span class="text-xs text-gray-500 font-mono">v0.1.0</span>',
            "            </div>",
            "        </div>",
            '        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">',
            '            <div class="bg-gray-900 p-4 rounded-xl border border-gray-800 shadow">',
            '                <p class="text-xs text-gray-400 uppercase font-semibold">Architecture Score</p>',
            '                <p class="text-3xl font-bold text-cyan-400 '
            f'mt-1">{score}<span class="text-lg text-gray-500">'
            "/100</span></p>",
            "            </div>",
            '            <div class="bg-gray-900 p-4 rounded-xl border border-gray-800 shadow">',
            '                <p class="text-xs text-gray-400 uppercase font-semibold">Active Packages</p>',
            f'                <p class="text-3xl font-bold text-blue-400 mt-1">{len(packages_metrics)}</p>',
            "            </div>",
            '            <div class="bg-gray-900 p-4 rounded-xl border border-gray-800 shadow">',
            '                <p class="text-xs text-gray-400 uppercase font-semibold">Violations</p>',
            f'                <p class="text-3xl font-bold text-rose-400 mt-1">{len(violations)}</p>',
            "            </div>",
            '            <div class="bg-gray-900 p-4 rounded-xl border border-gray-800 shadow">',
            '                <p class="text-xs text-gray-400 uppercase font-semibold">Splay Cache Status</p>',
            '                <p class="text-3xl font-bold text-emerald-400 mt-1">ACTIVE</p>',
            "            </div>",
            "        </div>",
            '        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">',
            '            <div class="bg-gray-900 p-5 rounded-xl border border-gray-800 lg:col-span-1">',
            '                <h2 class="text-sm font-bold text-gray-200 '
            "border-b border-gray-800 pb-2 uppercase "
            'tracking-wider">Gác Cổng Ranh Giới</h2>',
            f"                {violations_html}",
            "            </div>",
            '            <div class="bg-gray-900 p-5 rounded-xl border border-gray-800 lg:col-span-2 overflow-x-auto">',
            '                <h2 class="text-sm font-bold text-gray-200 '
            "border-b border-gray-800 pb-2 mb-3 "
            'uppercase tracking-wider">Chỉ Số Đóng Gói</h2>',
            '                <table class="w-full text-xs text-left text-gray-300">',
            '                    <thead class="text-gray-400 uppercase bg-gray-950">',
            "                        <tr>",
            '                            <th class="px-4 py-2">Package</th>',
            '                            <th class="px-4 py-2 text-center">Ca (In)</th>',
            '                            <th class="px-4 py-2 text-center">Ce (Out)</th>',
            '                            <th class="px-4 py-2 text-center">Instability (I)</th>',
            '                            <th class="px-4 py-2 text-center">Abstractness (A)</th>',
            '                            <th class="px-4 py-2 text-center">Distance (D)</th>',
            "                        </tr>",
            "                    </thead>",
            '                    <tbody class="divide-y divide-gray-800">',
            f"                        {metrics_rows}",
            "                    </tbody>",
            "                </table>",
            "            </div>",
            "        </div>",
            '        <div class="bg-gray-900 p-5 rounded-xl border border-gray-800">',
            '            <h2 class="text-sm font-bold text-gray-200 '
            "border-b border-gray-800 pb-3 mb-4 uppercase "
            'tracking-wider">Sơ Đồ Đồ Thị Phụ Thuộc '
            "(Dependency Graph)</h2>",
            '            <div class="flex justify-center bg-gray-950 '
            "p-6 rounded-lg border border-gray-800 "
            'overflow-x-auto">',
            '                <pre class="mermaid">',
            f"{mermaid_code}",
            "                </pre>",
            "            </div>",
            "        </div>",
            "    </div>",
            "</body>",
            "</html>",
        ]

        return "\n".join(html_parts)
