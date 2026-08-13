export function initTerminal() {
    const tabs = document.querySelectorAll('.term-tab');
    const box = document.getElementById('exec-result-box');

    const logs = {
        'term-tab-terminal': '{\n  "ruff": "Passed (0 errors)",\n  "mypy": "Success: no issues found",\n  "pytest": "237 passed in 1.42s"\n}',
        'term-tab-problems': '✅ Zero architecture or typing violations detected.',
        'term-tab-output': '[INFO] WebSocket connected to ws://127.0.0.1:8000/ws/chat\n[INFO] AI Studio ready.'
    };

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.className = 'term-tab hover:text-slate-200');
            tab.className = 'term-tab font-bold text-emerald-400 border-b-2 border-emerald-400 pb-0.5';
            if (box) box.textContent = logs[tab.id] || 'No logs available.';
        });
    });
}