/**
 * EAOS IDE UI Runtime
 *
 * Owns:
 * - Activity UI state
 * - Execution trace UI
 * - Chat UI event contract
 * - Editor integration events
 *
 * Does NOT own:
 * - Monaco lifecycle
 * - pane dimensions
 * - pane visibility
 * - WebSocket transport
 * - AI execution
 */

(function () {
    "use strict";

    const STORAGE_KEY = "eaos.ide.ui";

    const state = {
        activity: "explorer",
        executionTrace: true
    };


    function readState() {
        try {
            const raw =
                localStorage.getItem(STORAGE_KEY);

            if (!raw) {
                return;
            }

            const saved =
                JSON.parse(raw);

            if (
                saved &&
                typeof saved.activity === "string"
            ) {
                state.activity =
                    saved.activity;
            }

            if (
                saved &&
                typeof saved.executionTrace === "boolean"
            ) {
                state.executionTrace =
                    saved.executionTrace;
            }
        } catch {
            // Persistence is optional.
        }
    }


    function saveState() {
        try {
            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify(state)
            );
        } catch {
            // Persistence is optional.
        }
    }


    function emitChatSubmit(detail) {
        /*
         * The E2E/application contract is WINDOW level.
         *
         * Do not emit multiple competing versions of the same event.
         */
        window.__eaosChatSubmit = true;
        window.__EAOS_LAST_CHAT_SUBMIT__ =
            detail;

        window.dispatchEvent(
            new CustomEvent(
                "eaos:chat-submit",
                {
                    detail
                }
            )
        );

        document.dispatchEvent(
            new CustomEvent(
                "eaos:chat-submit",
                {
                    bubbles: true,
                    detail
                }
            )
        );
    }


    function setActivity(activity) {
        if (!activity) {
            return;
        }

        state.activity = activity;

        applyActivity(activity);

        saveState();

        document.dispatchEvent(
            new CustomEvent(
                "eaos:activity-ui",
                {
                    detail: {
                        activity
                    }
                }
            )
        );
    }


    function applyActivity(activity) {
        document
            .querySelectorAll(
                "[data-activity]"
            )
            .forEach((button) => {
                const active =
                    button.dataset.activity ===
                    activity;

                button.classList.toggle(
                    "active",
                    active
                );

                button.setAttribute(
                    "aria-pressed",
                    String(active)
                );
            });

        document
            .querySelectorAll(
                "[data-eaos-activity-region]"
            )
            .forEach((region) => {
                region.hidden =
                    region.dataset
                        .eaosActivityRegion !==
                    activity;
            });

        /*
         * Keep the public application contract.
         */
        window.EAOS =
            window.EAOS || {};

        window.EAOS.activity =
            window.EAOS.activity || {};

        window.EAOS.activity.current =
            activity;
    }


    function setupActivity() {
        document.addEventListener(
            "eaos:activity-change",
            (event) => {
                setActivity(
                    event.detail &&
                    event.detail.activity
                );
            }
        );
    }


    function setupExecutionTrace() {
        const button =
            document.getElementById(
                "btn-toggle-execution"
            );

        const trace =
            document.getElementById(
                "execution-trace"
            );

        if (!button || !trace) {
            return;
        }

        const render = () => {
            trace.hidden =
                !state.executionTrace;

            button.setAttribute(
                "aria-expanded",
                String(
                    state.executionTrace
                )
            );

            button.classList.toggle(
                "is-expanded",
                state.executionTrace
            );
        };

        button.addEventListener(
            "click",
            () => {
                state.executionTrace =
                    !state.executionTrace;

                render();
                saveState();
            }
        );

        render();
    }


    function setupChat() {
        const form =
            document.getElementById(
                "chat-form"
            );

        const input =
            document.getElementById(
                "chat-input"
            );

        if (!form || !input) {
            return;
        }

        if (
            form.dataset
                .eaosChatRuntimeBound ===
            "true"
        ) {
            return;
        }

        form.dataset
            .eaosChatRuntimeBound =
            "true";

        form.addEventListener(
            "submit",
            (event) => {
                const value =
                    String(
                        input.value || ""
                    ).trim();

                if (!value) {
                    event.preventDefault();
                    return;
                }

                emitChatSubmit({
                    message: value,
                    value,
                    source: "chat-form",
                    timestamp: Date.now(),
                    input,
                    form
                });

                /*
                 * Do NOT preventDefault here.
                 *
                 * Existing chat/AI/WebSocket handlers
                 * are allowed to continue.
                 */
            },
            false
        );

        /*
         * Enter => normal form submit.
         */
        input.addEventListener(
            "keydown",
            (event) => {
                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {
                    event.preventDefault();

                    if (
                        typeof form.requestSubmit ===
                        "function"
                    ) {
                        form.requestSubmit();
                    } else {
                        form.dispatchEvent(
                            new Event(
                                "submit",
                                {
                                    bubbles: true,
                                    cancelable: true
                                }
                            )
                        );
                    }
                }
            }
        );

        /*
         * Explicit application API.
         */
        window.EAOS =
            window.EAOS || {};

        window.EAOS.ui =
            window.EAOS.ui || {};

        window.EAOS.ui.chat =
            window.EAOS.ui.chat || {};

        window.EAOS.ui.chat.submit =
            function () {
                if (!form) {
                    return false;
                }

                form.requestSubmit();

                return true;
            };
    }


    function setupEditorBridge() {
        document.addEventListener(
            "eaos:monaco-ready",
            (event) => {
                document.dispatchEvent(
                    new CustomEvent(
                        "eaos:editor-ready",
                        {
                            detail:
                                event.detail || {}
                        }
                    )
                );
            }
        );
    }


    function exposeAPI() {
        window.EAOS =
            window.EAOS || {};

        window.EAOS.ui =
            window.EAOS.ui || {};

        window.EAOS.ui.getState =
            function () {
                return {
                    ...state
                };
            };

        window.EAOS.ui.setActivity =
            setActivity;

        window.EAOS.ui.toggleExecutionTrace =
            function () {
                state.executionTrace =
                    !state.executionTrace;

                const button =
                    document.getElementById(
                        "btn-toggle-execution"
                    );

                const trace =
                    document.getElementById(
                        "execution-trace"
                    );

                if (trace) {
                    trace.hidden =
                        !state.executionTrace;
                }

                if (button) {
                    button.setAttribute(
                        "aria-expanded",
                        String(
                            state.executionTrace
                        )
                    );
                }

                saveState();

                return state.executionTrace;
            };

        /*
         * Public contracts expected by E2E.
         */
        window.EAOS.activity =
            window.EAOS.activity || {};

        window.EAOS.panes =
            window.EAOS.panes || {};

        window.EAOS.layout =
            window.EAOS.layout || {};
    }


    function init() {
        readState();

        exposeAPI();

        setupActivity();
        setupExecutionTrace();
        setupChat();
        setupEditorBridge();

        applyActivity(
            state.activity
        );

        console.debug(
            "[EAOS] UI runtime initialized",
            state
        );
    }


    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            init,
            {
                once: true
            }
        );
    } else {
        init();
    }
})();
