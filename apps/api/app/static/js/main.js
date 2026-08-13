import {
    initIDELayoutResizers
} from './ide/layout_resizer.js';

import {
    initMonacoAdapter,
    updateMonacoCode,
    getMonacoCode
} from './core/monaco_adapter.js';

import {
    WSClient
} from './core/websocket_client.js';

import {
    initResizablePanes
} from './core/resizable.js';

import {
    initExplorer
} from './ide/explorer.js';

import {
    initTabs
} from './ide/tabs.js';

import {
    initTerminal
} from './ide/terminal.js';

import {
    initModelRouter
} from './ai/model_router.js';

import {
    initAgentChat
} from './ai/agent_chat.js';


let currentActivePath = 'apps/api/app/routers/chat.py';
let websocketClient = null;


document.addEventListener('DOMContentLoaded', async () => {
    refreshRuntimeFooter();

    window.setInterval(
        refreshRuntimeFooter,
        5000
    );
    await initMonacoAdapter(
        'monaco-editor-container',
        '# EAOS Real IDE Ready\n',
        'python'
    );

    initResizablePanes();
    initIDELayoutResizers();
    initExplorer();
    initTabs();
    initTerminal();
    initModelRouter();
    initPaneToggles();

    await loadRealWorkspaceTree();
    await loadFileToEditor(currentActivePath);

    initEAOSWebSocket();
});


function initEAOSWebSocket() {
    const protocol = window.location.protocol === 'https:'
        ? 'wss:'
        : 'ws:';

    const wsUrl = `${protocol}//${window.location.host}/ws/chat`;

    websocketClient = new WSClient(wsUrl);

    /*
     * EAOS diagnostic bridge.
     *
     * Keep the real client in the existing closure while also
     * exposing the same object for DevTools/runtime diagnostics.
     */
    window.__EAOS_WS_CLIENT__ = websocketClient;
    window.__EAOS_WS_URL__ = wsUrl;

    console.log(
        '[EAOS] WebSocket client initialized:',
        wsUrl
    );

    websocketClient.on(
        'connection_changed',
        handleConnectionChanged
    );

    websocketClient.on(
        'error',
        handleWebSocketError
    );

    initAgentChat(
        websocketClient,
        () => currentActivePath
    );

    console.log(
        '[EAOS] initAgentChat completed'
    );

    websocketClient.connect();

    console.log(
        '[EAOS] websocketClient.connect() called'
    );
}


function handleConnectionChanged(data) {

    console.log(
        '[EAOS] WebSocket connection_changed:',
        data
    );

    window.__EAOS_WS_STATE__ = data;

    window.eaosRuntime.wsConnected =
        Boolean(data.connected);

    updateRuntimeWebSocketFooter(
        Boolean(data.connected)
    );

    const statusBadge = document.getElementById('exec-status');

    if (!statusBadge) {
        return;
    }

    if (data.connected) {
        setStatus(statusBadge, 'READY', 'ready');
        return;
    }

    setStatus(
        statusBadge,
        'WS DISCONNECTED',
        'error'
    );
}


function handleWebSocketError(data) {
    console.error('[EAOS WS]', data);

    const statusBadge = document.getElementById('exec-status');

    if (statusBadge) {
        setStatus(
            statusBadge,
            'WS ERROR',
            'error'
        );
    }
}


function initPaneToggles() {
    const leftPane = document.getElementById(
        'pane-left-explorer'
    );

    const bottomPane = document.getElementById(
        'pane-bottom-terminal'
    );

    const rightPane = document.getElementById(
        'pane-right-inspector'
    );

    const btnLeft = document.getElementById(
        'btn-toggle-left'
    );

    const btnBottom = document.getElementById(
        'btn-toggle-terminal'
    );

    const btnRight = document.getElementById(
        'btn-toggle-right'
    );

    const btnFocus = document.getElementById(
        'btn-focus-mode'
    );

    if (btnLeft && leftPane) {
        btnLeft.addEventListener('click', () => {
            leftPane.classList.toggle('hidden');
        });
    }

    if (btnBottom && bottomPane) {
        btnBottom.addEventListener('click', () => {
            bottomPane.classList.toggle('hidden');
        });
    }

    if (btnRight && rightPane) {
        btnRight.addEventListener('click', () => {
            rightPane.classList.toggle('hidden');
        });
    }

    if (btnFocus) {
        let isFocus = false;

        btnFocus.addEventListener('click', () => {
            isFocus = !isFocus;

            if (isFocus) {
                leftPane?.classList.add('hidden');
                bottomPane?.classList.add('hidden');
                rightPane?.classList.add('hidden');

                btnFocus.classList.add(
                    'bg-emerald-500',
                    'text-slate-950'
                );
            } else {
                leftPane?.classList.remove('hidden');
                bottomPane?.classList.remove('hidden');
                rightPane?.classList.remove('hidden');

                btnFocus.classList.remove(
                    'bg-emerald-500',
                    'text-slate-950'
                );
            }
        });
    }

    document.addEventListener('keydown', (event) => {
        if (
            (event.ctrlKey || event.metaKey) &&
            event.key.toLowerCase() === 'b'
        ) {
            event.preventDefault();
            leftPane?.classList.toggle('hidden');
        }

        if (
            (event.ctrlKey || event.metaKey) &&
            event.key === '`'
        ) {
            event.preventDefault();
            bottomPane?.classList.toggle('hidden');
        }

        if (
            (event.ctrlKey || event.metaKey) &&
            event.key.toLowerCase() === 's'
        ) {
            event.preventDefault();
            saveCurrentFile();
        }
    });
}


async function loadRealWorkspaceTree() {
    const container = document.querySelector(
        '#pane-left-explorer div.overflow-y-auto'
    );

    if (!container) {
        return;
    }

    try {
        const response = await fetch('/api/files/tree');

        if (!response.ok) {
            throw new Error(
                `Workspace tree failed: ${response.status}`
            );
        }

        const items = await response.json();

        container.innerHTML = '';

        items.forEach((item) => {
            const row = document.createElement('div');
            const isDirectory = item.type === 'directory';

            row.className = [
                'py-1',
                'px-2',
                'hover:bg-slate-800',
                'rounded',
                'cursor-pointer',
                'text-xs',
                'font-mono',
                'flex',
                'items-center',
                'space-x-2'
            ].join(' ');

            if (item.path === currentActivePath) {
                row.classList.add(
                    'text-cyan-400',
                    'font-bold'
                );
            } else {
                row.classList.add('text-slate-300');
            }

            const icon = document.createElement('span');
            icon.textContent = isDirectory ? '📁' : '📄';

            const name = document.createElement('span');
            name.className = 'truncate';
            name.textContent = item.name;

            row.appendChild(icon);
            row.appendChild(name);

            if (!isDirectory) {
                row.addEventListener('click', () => {
                    loadFileToEditor(item.path);
                });
            }

            container.appendChild(row);
        });
    } catch (error) {
        console.error(
            '[EAOS Explorer] Failed to load tree:',
            error
        );
    }
}


async function loadFileToEditor(filePath) {
    currentActivePath = filePath;

    const tabTitle = document.getElementById(
        'active-filename'
    );

    if (tabTitle) {
        tabTitle.textContent = filePath;
    }

    try {
        const response = await fetch(
            `/api/files/content?path=${encodeURIComponent(filePath)}`
        );

        if (!response.ok) {
            throw new Error(
                `File load failed: ${response.status}`
            );
        }

        const data = await response.json();

        updateMonacoCode(
            data.content,
            detectLanguage(filePath)
        );
    } catch (error) {
        console.error(
            '[EAOS Editor] Failed to load file:',
            error
        );
    }
}


function detectLanguage(filePath) {
    const extension = filePath
        .split('.')
        .pop()
        ?.toLowerCase();

    const languages = {
        py: 'python',
        js: 'javascript',
        mjs: 'javascript',
        ts: 'typescript',
        json: 'json',
        html: 'html',
        css: 'css',
        md: 'markdown',
        yaml: 'yaml',
        yml: 'yaml',
        sh: 'shell',
        sql: 'sql'
    };

    return languages[extension] || 'plaintext';
}


async function saveCurrentFile() {
    const content = getMonacoCode();

    if (!content) {
        return;
    }

    try {
        const response = await fetch(
            '/api/files/save',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    path: currentActivePath,
                    content
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                `Save failed: ${response.status}`
            );
        }

        showToast('✔ Đã lưu file thành công!');
    } catch (error) {
        console.error(
            '[EAOS Editor] Failed to save file:',
            error
        );

        showToast('✖ Không thể lưu file.');
    }
}


function setStatus(element, text, state) {
    element.textContent = text;

    element.className = [
        'text-[10px]',
        'px-2',
        'py-0.5',
        'rounded',
        'font-mono',
        'border'
    ].join(' ');

    if (state === 'success' || state === 'ready') {
        element.classList.add(
            'bg-emerald-950',
            'text-emerald-400',
            'border-emerald-800'
        );
    } else if (state === 'running') {
        element.classList.add(
            'bg-cyan-950',
            'text-cyan-400',
            'border-cyan-800'
        );
    } else {
        element.classList.add(
            'bg-rose-950',
            'text-rose-400',
            'border-rose-800'
        );
    }
}


function showToast(text) {
    const toast = document.createElement('div');

    toast.className = [
        'fixed',
        'bottom-8',
        'right-8',
        'px-4',
        'py-2',
        'bg-emerald-500',
        'text-slate-950',
        'font-bold',
        'text-xs',
        'rounded-lg',
        'shadow-2xl',
        'z-50'
    ].join(' ');

    toast.textContent = text;

    document.body.appendChild(toast);

    window.setTimeout(() => {
        toast.remove();
    }, 2500);
}

async function refreshRuntimeFooter() {
    const healthText =
        document.getElementById(
            'runtime-health-text'
        );

    const healthDot =
        document.getElementById(
            'runtime-health-dot'
        );

    const apiText =
        document.getElementById(
            'runtime-api'
        );

    const pythonText =
        document.getElementById(
            'runtime-python'
        );

    const versionText =
        document.getElementById(
            'runtime-version'
        );

    const processText =
        document.getElementById(
            'runtime-process'
        );

    if (!healthText) {
        return;
    }

    try {
        const [
            healthResponse,
            runtimeResponse
        ] = await Promise.all([
            fetch(
                '/health',
                {
                    cache: 'no-store'
                }
            ),
            fetch(
                '/v1/runtime/footer',
                {
                    cache: 'no-store'
                }
            )
        ]);

        if (!healthResponse.ok) {
            throw new Error(
                `Health failed: ${healthResponse.status}`
            );
        }

        if (!runtimeResponse.ok) {
            throw new Error(
                `Runtime failed: ${runtimeResponse.status}`
            );
        }

        const health =
            await healthResponse.json();

        const runtime =
            await runtimeResponse.json();

        const healthy =
            health.status === 'healthy';

        healthText.textContent =
            healthy
                ? 'System Healthy'
                : 'System Degraded';

        healthText.className =
            healthy
                ? 'text-emerald-400'
                : 'text-rose-400';

        if (healthDot) {
            healthDot.className =
                healthy
                    ? 'w-2 h-2 rounded-full bg-emerald-400'
                    : 'w-2 h-2 rounded-full bg-rose-400';
        }

        if (apiText) {
            apiText.textContent =
                `API ${runtime.api_host || '—'}:${runtime.api_port || '—'}`;
        }

        if (pythonText) {
            pythonText.textContent =
                `Python ${runtime.python_version || '—'}`;
        }

        if (versionText) {
            versionText.textContent =
                `EAOS ${health.version || '—'}`;
        }

        if (processText) {
            processText.textContent =
                `PID ${runtime.process_id || '—'}`;
        }

        window.eaosRuntime = {
            ...(window.eaosRuntime || {}),
            health,
            runtime
        };

        updateRuntimeWebSocketFooter(
            Boolean(
                window.eaosRuntime.wsConnected
            )
        );

        return;
    } catch (error) {
        console.error(
            '[EAOS Footer Runtime]',
            error
        );

        healthText.textContent =
            'Runtime Unavailable';

        healthText.className =
            'text-rose-400';

        if (healthDot) {
            healthDot.className =
                'w-2 h-2 rounded-full bg-rose-400';
        }

        if (apiText) {
            apiText.textContent =
                'API Unavailable';
        }

        if (pythonText) {
            pythonText.textContent =
                'Python —';
        }

        if (processText) {
            processText.textContent =
                'PID —';
        }
    }
}

function updateRuntimeWebSocketFooter(
    connected
) {
    const wsText = document.getElementById(
        'runtime-ws'
    );

    if (!wsText) {
        return;
    }

    wsText.textContent = connected
        ? 'WS Connected'
        : 'WS Disconnected';

    wsText.className = connected
        ? 'text-emerald-400'
        : 'text-rose-400';
}

function updateRuntimeTestFooter(
    status,
    runner
) {
    const tests = document.getElementById(
        'runtime-tests'
    );

    if (!tests) {
        return;
    }

    if (runner) {
        tests.textContent =
            `${runner} ${status}`;
        return;
    }

    tests.textContent =
        `Tests ${status}`;
}


