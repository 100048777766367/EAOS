
function updateCopilotModelStrip(runtime) {
    const provider = document.getElementById(
        'runtime-provider'
    );

    const model = document.getElementById(
        'runtime-model'
    );

    if (provider) {
        provider.textContent =
            runtime?.llm_provider || '—';
    }

    if (model) {
        const isGemini =
            String(
                runtime?.llm_provider || ''
            ).toLowerCase() === 'gemini';

        model.textContent = isGemini
            ? (
                runtime?.gemini_model
                || '—'
            )
            : (
                runtime?.ollama_model
                || '—'
            );
    }
}

function updateTaskStateChip(
    state
) {
    const chip = document.getElementById(
        'task-state-chip'
    );

    if (!chip) {
        return;
    }

    const normalized =
        String(state || 'IDLE')
            .toUpperCase();

    chip.textContent = normalized;

    chip.className =
        'eaos-status-chip';

    if (
        normalized === 'COMPLETED' ||
        normalized === 'PASSED'
    ) {
        chip.classList.add(
            'status-ready'
        );
        return;
    }

    if (
        normalized === 'QUEUED' ||
        normalized === 'RUNNING' ||
        normalized === 'VERIFYING' ||
        normalized === 'STREAMING'
    ) {
        chip.classList.add(
            'status-running'
        );
        return;
    }

    if (
        normalized === 'FAILED' ||
        normalized === 'ERROR'
    ) {
        chip.classList.add(
            'status-error'
        );
        return;
    }

    chip.classList.add(
        'status-idle'
    );
}

function updateTraceSummary(
    text
) {
    const summary =
        document.getElementById(
            'trace-summary'
        );

    if (summary) {
        summary.textContent =
            text || 'Waiting for task';
    }
}

function updateRuntimeLatency(
    startedAt
) {
    const latency =
        document.getElementById(
            'runtime-latency'
        );

    if (!latency || !startedAt) {
        return;
    }

    const elapsed =
        Date.now() - startedAt;

    latency.textContent =
        `${(elapsed / 1000).toFixed(1)}s`;
}


function updateRuntimeTestFooter(
    runner,
    status
) {
    const tests =
        document.getElementById(
            'runtime-tests'
        );

    if (!tests) {
        return;
    }

    const normalizedRunner =
        String(runner || '')
            .toUpperCase();

    const normalizedStatus =
        String(status || '')
            .toUpperCase();

    const quickId =
        normalizedRunner === 'RUFF'
            ? 'runtime-ruff'
            : normalizedRunner === 'PYTEST'
                ? 'runtime-pytest'
                : null;

    const quick =
        quickId
            ? document.getElementById(
                quickId
            )
            : null;

    if (normalizedStatus === 'PASSED') {
        tests.textContent =
            `${normalizedRunner} PASS`;

        tests.className =
            'text-emerald-400';

        if (quick) {
            quick.textContent = 'PASS';
            quick.className =
                'eaos-quick-value pass';
        }

        return;
    }

    if (normalizedStatus === 'RUNNING') {
        tests.textContent =
            `${normalizedRunner} RUN`;

        tests.className =
            'text-cyan-400';

        if (quick) {
            quick.textContent = 'RUN';
            quick.className =
                'eaos-quick-value running';
        }

        return;
    }

    if (normalizedStatus === 'FAILED') {
        tests.textContent =
            `${normalizedRunner} FAIL`;

        tests.className =
            'text-rose-400';

        if (quick) {
            quick.textContent = 'FAIL';
            quick.className =
                'eaos-quick-value fail';
        }

        return;
    }

    tests.textContent =
        `${normalizedRunner} ${normalizedStatus}`;

    tests.className =
        'text-slate-400';
}

function updateRuntimeOverall(status) {
    const tests =
        document.getElementById(
            'runtime-tests'
        );

    if (!tests) {
        return;
    }

    const normalized =
        String(status || '')
            .toUpperCase();

    tests.textContent =
        `Tests ${normalized}`;

    const overall =
        document.getElementById(
            'runtime-overall'
        );

    if (overall) {
        overall.textContent =
            normalized;

        overall.className =
            normalized === 'PASSED'
                ? 'eaos-quick-value pass'
                : normalized === 'FAILED'
                    ? 'eaos-quick-value fail'
                    : 'eaos-quick-value running';
    }

    updateTaskStateChip(
        normalized === 'PASSED'
            ? 'COMPLETED'
            : normalized
    );

    if (normalized === 'PASSED') {
        tests.className =
            'text-emerald-400';
    } else if (normalized === 'FAILED') {
        tests.className =
            'text-rose-400';
    } else {
        tests.className =
            'text-cyan-400';
    }
}

import { updateMonacoCode } from '../core/monaco_adapter.js';

export function initAgentChat(wsClient, getActiveFile) {

    async function refreshRuntimeFooter() {
        try {
            const response =
                await fetch('/v1/runtime/footer');

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            const runtime =
                await response.json();

            updateCopilotModelStrip(
                runtime
            );
        } catch (error) {
            console.warn(
                '[EAOS] runtime footer unavailable:',
                error
            );
        }
    }

    refreshRuntimeFooter();

    const form = document.getElementById('chat-form');
    const input = document.getElementById('chat-input');
    const stream = document.getElementById('chat-stream');
    const statusBadge = document.getElementById('exec-status');
    const sendButton = document.getElementById('btn-send-chat');

    const runtimeTask = document.getElementById(
        'runtime-task'
    );

    const runtimeAgent = document.getElementById(
        'runtime-agent'
    );

    const runtimeEvidence = document.getElementById(
        'runtime-evidence'
    );

    const executionTrace = document.getElementById(
        'execution-trace'
    );

    const toggleExecution = document.getElementById(
        'btn-toggle-execution'
    );

    if (!form || !input || !wsClient) {
        return;
    }

    let currentResponse = null;
    let currentResponseBody = null;
    let accumulatedText = '';
    let taskStartedAt = null;

    const steps = [
        'QUEUED',
        'RUNNING',
        'LLM_STREAM',
        'RESPONSE',
        'VERIFYING',
        'RUFF',
        'PYTEST',
        'COMPLETED'
    ];

    const stepIndex = new Map(
        steps.map((step, index) => [step, index])
    );

    function setStatus(text, state) {
        if (!statusBadge) {
            return;
        }

        statusBadge.textContent = text;

        statusBadge.className = [
            'text-[10px]',
            'px-2',
            'py-0.5',
            'rounded',
            'font-mono',
            'border'
        ].join(' ');

        if (state === 'success') {
            statusBadge.classList.add(
                'bg-emerald-950',
                'text-emerald-400',
                'border-emerald-800'
            );
            return;
        }

        if (state === 'running') {
            statusBadge.classList.add(
                'bg-cyan-950',
                'text-cyan-400',
                'border-cyan-800'
            );
            return;
        }

        if (state === 'error') {
            statusBadge.classList.add(
                'bg-rose-950',
                'text-rose-400',
                'border-rose-800'
            );
            return;
        }

        statusBadge.classList.add(
            'bg-emerald-950',
            'text-emerald-400',
            'border-emerald-800'
        );
    }

    function getTimelineItems() {
        return Array.from(
            document.querySelectorAll(
                '.eaos-timeline-item'
            )
        );
    }

    function resetTimeline() {
        getTimelineItems().forEach(
            (item) => {
                item.classList.remove(
                    'active',
                    'completed',
                    'failed'
                );
            }
        );
    }

    function markTimeline(
        step,
        state = 'active'
    ) {
        if (!stepIndex.has(step)) {
            return;
        }

        const targetIndex = stepIndex.get(step);

        getTimelineItems().forEach(
            (item) => {
                const itemStep = item.dataset.step;

                if (!stepIndex.has(itemStep)) {
                    return;
                }

                const itemIndex =
                    stepIndex.get(itemStep);

                item.classList.remove(
                    'active',
                    'completed',
                    'failed'
                );

                if (
                    state === 'failed' &&
                    itemStep === step
                ) {
                    item.classList.add(
                        'failed'
                    );
                    return;
                }

                if (itemIndex < targetIndex) {
                    item.classList.add(
                        'completed'
                    );
                }

                if (
                    itemIndex === targetIndex &&
                    state !== 'completed'
                ) {
                    item.classList.add(
                        'active'
                    );
                }

                if (
                    itemIndex === targetIndex &&
                    state === 'completed'
                ) {
                    item.classList.add(
                        'completed'
                    );
                }
            }
        );

        const target = document.querySelector(
            `[data-step="${step}"]`
        );

        target?.scrollIntoView({
            block: 'nearest',
            behavior: 'smooth'
        });
    }

    function addMessage(
        role,
        text,
        type = 'assistant'
    ) {
        if (!stream) {
            return null;
        }

        const wrapper =
            document.createElement('div');

        wrapper.className = [
            'eaos-chat-message',
            type === 'user'
                ? 'eaos-chat-user'
                : 'eaos-chat-assistant'
        ].join(' ');

        const label =
            document.createElement('div');

        label.className = [
            'eaos-chat-label',
            type === 'user'
                ? 'text-cyan-400'
                : 'text-emerald-400'
        ].join(' ');

        label.textContent = role;

        const body =
            document.createElement('div');

        body.className =
            'eaos-chat-body';

        body.textContent =
            text || '';

        wrapper.appendChild(label);
        wrapper.appendChild(body);

        stream.appendChild(wrapper);
        stream.scrollTop =
            stream.scrollHeight;

        return {
            wrapper,
            body
        };
    }

    function startAssistantResponse() {
        const result = addMessage(
            'EAOS AGENT',
            '',
            'assistant'
        );

        if (!result) {
            return;
        }

        currentResponse =
            result.wrapper;

        currentResponseBody =
            result.body;

        accumulatedText = '';
    }

    function appendToken(token) {
        if (!currentResponseBody) {
            startAssistantResponse();
        }

        if (!currentResponseBody) {
            return;
        }

        accumulatedText += token;

        currentResponseBody.textContent =
            accumulatedText;

        stream.scrollTop =
            stream.scrollHeight;
    }

    function attachApplyCodeButton() {
        if (
            !currentResponse ||
            !accumulatedText
        ) {
            return;
        }

        const codeMatch =
            accumulatedText.match(
                /```(?:\w+)?\n([\s\S]*?)```/
            );

        if (
            !codeMatch ||
            !codeMatch[1]
        ) {
            return;
        }

        if (
            currentResponse.querySelector(
                '[data-apply-code]'
            )
        ) {
            return;
        }

        const button =
            document.createElement('button');

        button.type = 'button';
        button.dataset.applyCode = 'true';

        button.className = [
            'mt-3',
            'w-full',
            'py-1.5',
            'px-3',
            'bg-cyan-500',
            'hover:bg-cyan-400',
            'text-slate-950',
            'font-bold',
            'text-xs',
            'rounded',
            'transition',
            'cursor-pointer'
        ].join(' ');

        button.textContent =
            'Apply code to Monaco';

        const code =
            codeMatch[1].trim();

        button.addEventListener(
            'click',
            () => {
                const activeFile =
                    getActiveFile
                        ? getActiveFile()
                        : 'plaintext';

                const language =
                    detectLanguage(
                        activeFile
                    );

                updateMonacoCode(
                    code,
                    language
                );

                button.textContent =
                    'Applied — Ctrl+S to save';

                button.className = [
                    'mt-3',
                    'w-full',
                    'py-1.5',
                    'px-3',
                    'bg-emerald-500',
                    'text-slate-950',
                    'font-bold',
                    'text-xs',
                    'rounded'
                ].join(' ');
            }
        );

        currentResponse.appendChild(
            button
        );
    }

    function detectLanguage(filePath) {
        const extension = String(filePath)
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

        return (
            languages[extension]
            || 'plaintext'
        );
    }

    function setRunner(
        runner,
        status
    ) {
        const normalized =
            String(runner)
                .toUpperCase();

        if (
            normalized !== 'RUFF' &&
            normalized !== 'PYTEST'
        ) {
            return;
        }

        const step =
            normalized;

        const state =
            String(status)
                .toUpperCase();

        if (state === 'PASSED') {
            markTimeline(
                step,
                'completed'
            );
            return;
        }

        if (state === 'FAILED') {
            markTimeline(
                step,
                'failed'
            );
            return;
        }

        markTimeline(
            step,
            'active'
        );
    }

    wsClient.on(
        'connection_changed',
        (data) => {
            if (data.connected) {
                setStatus(
                    'READY',
                    'ready'
                );
                return;
            }

            setStatus(
                'RECONNECTING',
                'running'
            );
        }
    );

    wsClient.on(
        'task_lifecycle',
        (data) => {
            const state =
                String(
                    data.state
                    || 'UNKNOWN'
                ).toUpperCase();

            if (
                data.correlation
            ) {
                if (runtimeTask) {
                    runtimeTask.textContent =
                        data.correlation.task_id
                        || '—';
                }

                if (runtimeAgent) {
                    runtimeAgent.textContent =
                        data.correlation.agent_id
                        || '—';
                }

                if (
                    data.correlation
                        .evidence_id &&
                    runtimeEvidence
                ) {
                    runtimeEvidence.textContent =
                        data.correlation
                            .evidence_id;
                }
            }

            updateTaskStateChip(
                state
            );

            updateTraceSummary(
                `Runtime state: ${state}`
            );

            if (
                !taskStartedAt &&
                (
                    state === 'QUEUED' ||
                    state === 'RUNNING'
                )
            ) {
                taskStartedAt =
                    Date.now();
            }

            if (
                taskStartedAt
            ) {
                updateRuntimeLatency(
                    taskStartedAt
                );
            }

            if (
                state === 'QUEUED'
            ) {
                markTimeline(
                    'QUEUED',
                    'active'
                );

                setStatus(
                    'QUEUED',
                    'running'
                );

                return;
            }

            if (
                state === 'RUNNING'
            ) {
                markTimeline(
                    'RUNNING',
                    'active'
                );

                setStatus(
                    'RUNNING',
                    'running'
                );

                return;
            }

            if (
                state === 'VERIFYING'
            ) {
                markTimeline(
                    'VERIFYING',
                    'active'
                );

                setStatus(
                    'VERIFYING',
                    'running'
                );

                return;
            }

            if (
                state === 'COMPLETED'
            ) {
                markTimeline(
                    'COMPLETED',
                    'completed'
                );

                setStatus(
                    'COMPLETED',
                    'success'
                );
            }
        }
    );

    wsClient.on(
        'stream_start',
        () => {
            startAssistantResponse();

            markTimeline(
                'LLM_STREAM',
                'active'
            );

            updateTaskStateChip(
                'STREAMING'
            );

            updateTraceSummary(
                'Provider generating response'
            );

            setStatus(
                'STREAMING',
                'running'
            );
        }
    );

    wsClient.on(
        'stream_chunk',
        (data) => {
            if (data.content) {
                appendToken(
                    data.content
                );
            }
        }
    );

    wsClient.on(
        'stream_end',
        (data) => {
            if (
                data.reply &&
                currentResponseBody
            ) {
                accumulatedText =
                    data.reply;

                currentResponseBody
                    .textContent =
                    accumulatedText;
            }

            markTimeline(
                'RESPONSE',
                'active'
            );

            setStatus(
                'RESPONSE',
                'running'
            );

            attachApplyCodeButton();
        }
    );

    wsClient.on(
        'response_complete',
        (data) => {
            if (
                data.reply &&
                currentResponseBody
            ) {
                accumulatedText =
                    data.reply;

                currentResponseBody
                    .textContent =
                    accumulatedText;
            }

            markTimeline(
                'RESPONSE',
                'completed'
            );

            attachApplyCodeButton();
        }
    );

    wsClient.on(
        'verification_started',
        () => {
            markTimeline(
                'VERIFYING',
                'active'
            );

            updateTaskStateChip(
                'VERIFYING'
            );

            updateTraceSummary(
                'Verification pipeline running'
            );

            setStatus(
                'VERIFYING',
                'running'
            );
        }
    );

    wsClient.on(
        'verification_runner_started',
        (data) => {
            const runner =
                String(
                    data.runner
                    || ''
                ).toUpperCase();

            setRunner(
                runner,
                'RUNNING'
            );
        }
    );

    wsClient.on(
        'verification_runner_result',
        (data) => {
            setRunner(
                data.runner,
                data.status
            );
        }
    );

    wsClient.on(
        'verification_result',
        (data) => {
            const result =
                data.result || {};

            const runs =
                Array.isArray(
                    result.runs
                )
                    ? result.runs
                    : [];

            for (
                const run of runs
            ) {
                if (
                    !run ||
                    typeof run !== 'object'
                ) {
                    continue;
                }

                setRunner(
                    run.name,
                    run.status
                );
            }

            const status =
                String(
                    data.status
                    || result.status
                    || 'UNKNOWN'
                ).toUpperCase();

            if (
                status === 'PASSED'
            ) {
                markTimeline(
                    'COMPLETED',
                    'completed'
                );
            }

            updateRuntimeOverall(
                status
            );

            if (
                data.evidence_id &&
                runtimeEvidence
            ) {
                runtimeEvidence.textContent =
                    data.evidence_id;
            }

            setStatus(
                status,
                status === 'PASSED'
                    ? 'success'
                    : 'error'
            );
        }
    );

    wsClient.on(
        'error',
        (data) => {
            console.error(
                '[EAOS WS]',
                data
            );

            const active =
                document.querySelector(
                    '.eaos-timeline-item.active'
                );

            if (active) {
                active.classList.remove(
                    'active'
                );

                active.classList.add(
                    'failed'
                );
            }

            setStatus(
                'ERROR',
                'error'
            );
        }
    );

    if (
        toggleExecution &&
        executionTrace
    ) {
        toggleExecution.addEventListener(
            'click',
            () => {
                const collapsed =
                    executionTrace
                        .classList.toggle(
                            'hidden'
                        );

                toggleExecution.textContent =
                    collapsed
                        ? 'Expand'
                        : 'Collapse';
            }
        );
    }

    input.addEventListener(
        'keydown',
        (event) => {
            if (
                event.key === 'Enter' &&
                !event.shiftKey
            ) {
                event.preventDefault();
                form.requestSubmit();
            }
        }
    );

    form.addEventListener(
        'submit',
        (event) => {
            event.preventDefault();

            const message =
                input.value.trim();

            if (!message) {
                return;
            }

            if (
                !wsClient.isConnected()
            ) {
                setStatus(
                    'OFFLINE',
                    'error'
                );
                return;
            }

            addMessage(
                'OPERATOR',
                message,
                'user'
            );

            resetTimeline();

            if (runtimeTask) {
                runtimeTask.textContent =
                    'QUEUED';
            }

            const agentSelect =
                document.getElementById(
                    'agent-role-select'
                );

            const agentRole =
                agentSelect
                    ? agentSelect.value
                    : 'agent-coder';

            if (runtimeAgent) {
                runtimeAgent.textContent =
                    agentRole;
            }

            if (runtimeEvidence) {
                runtimeEvidence.textContent =
                    '—';
            }

            if (sendButton) {
                sendButton.disabled =
                    true;
            }

            const activeFile =
                getActiveFile
                    ? getActiveFile()
                    : 'apps/api/app/routers/chat.py';

            const sent =
                wsClient.send({
                    conversation_id:
                        `conv-${Date.now()}`,
                    agent_role:
                        agentRole,
                    message,
                    active_file:
                        activeFile,
                    system_instruction:
                        '',
                    temperature:
                        0.7,
                    max_output_tokens:
                        4096,
                    json_mode:
                        false
                });

            if (!sent) {
                setStatus(
                    'SEND ERROR',
                    'error'
                );

                if (sendButton) {
                    sendButton.disabled =
                        false;
                }

                return;
            }

            input.value = '';

            markTimeline(
                'QUEUED',
                'active'
            );

            setStatus(
                'QUEUED',
                'running'
            );

            window.setTimeout(
                () => {
                    if (sendButton) {
                        sendButton.disabled =
                            false;
                    }
                },
                500
            );
        }
    );
}

const clearChatButton =
    document.getElementById(
        'btn-clear-chat'
    );

if (clearChatButton) {
    clearChatButton.addEventListener(
        'click',
        () => {
            const stream =
                document.getElementById(
                    'chat-stream'
                );

            if (!stream) {
                return;
            }

            stream.innerHTML = `
                <div class="eaos-chat-message
                            eaos-chat-assistant">
                    <div class="eaos-chat-label">
                        EAOS AGENT
                    </div>

                    <div class="eaos-chat-body">
                        Conversation cleared.
                        Runtime is ready.
                    </div>
                </div>
            `;

            resetTimeline();
            updateTaskStateChip('IDLE');

            updateTraceSummary(
                'Waiting for task'
            );

            const task =
                document.getElementById(
                    'runtime-task'
                );

            const evidence =
                document.getElementById(
                    'runtime-evidence'
                );

            const latency =
                document.getElementById(
                    'runtime-latency'
                );

            if (task) {
                task.textContent = '—';
            }

            if (evidence) {
                evidence.textContent = '—';
            }

            if (latency) {
                latency.textContent = '—';
            }

            taskStartedAt = null;
            currentResponse = null;
            currentResponseBody = null;
            accumulatedText = '';
        }
    );
}
