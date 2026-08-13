/**
 * EAOS IDE — Pane / Layout Controller
 *
 * Responsibility:
 * - Pane visibility state
 * - Focus mode
 * - Keyboard shortcuts
 * - Toggle button state
 * - Public EAOS.panes API
 * - Layout state persistence
 * - Layout lifecycle events
 *
 * Does NOT own:
 * - pane dimensions / resizing
 * - Monaco
 * - chat
 * - AI runtime
 * - WebSocket
 * - DOM structure
 *
 * Boundary:
 *
 * pane_toggles.js
 *     visibility / state / keyboard / API
 *
 * layout_resizer.js
 *     dimensions / drag / resize
 *
 * chat.css
 *     visual + layout rules
 *
 * Jinja templates
 *     DOM structure
 */

const IDS = {
    explorer: "pane-left-explorer",
    explorerResizer: "resizer-explorer",

    terminal: "pane-bottom-terminal",
    terminalResizer: "resizer-terminal",

    right: "pane-right-inspector",
    rightResizer: "resizer-copilot",

    toggleLeft: "btn-toggle-left",
    toggleTerminal: "btn-toggle-terminal",
    toggleRight: "btn-toggle-right",
    focus: "btn-focus-mode",

    workspace: ".eaos-workspace-shell",
};

const STORAGE_KEY = "eaos.ide.pane-layout.v2";

const DEFAULT_STATE = Object.freeze({
    left: true,
    terminal: true,
    right: true,
    focus: false,
});

const state = {
    ...DEFAULT_STATE,
};

let initialized = false;
let focusSnapshot = null;


/* =========================================================
 * DOM HELPERS
 * ========================================================= */

function $(selector) {
    return document.querySelector(selector);
}

function byId(id) {
    return document.getElementById(id);
}


/* =========================================================
 * STATE NORMALIZATION
 * ========================================================= */

function normalizeBoolean(value, fallback) {
    return typeof value === "boolean"
        ? value
        : fallback;
}

function normalizeState(value) {
    if (!value || typeof value !== "object") {
        return { ...DEFAULT_STATE };
    }

    return {
        left: normalizeBoolean(
            value.left,
            DEFAULT_STATE.left
        ),

        terminal: normalizeBoolean(
            value.terminal,
            DEFAULT_STATE.terminal
        ),

        right: normalizeBoolean(
            value.right,
            DEFAULT_STATE.right
        ),

        focus: normalizeBoolean(
            value.focus,
            DEFAULT_STATE.focus
        ),
    };
}

function getState() {
    return { ...state };
}


/* =========================================================
 * PERSISTENCE
 * ========================================================= */

function loadState() {
    try {
        const raw = window.localStorage.getItem(
            STORAGE_KEY
        );

        if (!raw) {
            return;
        }

        const parsed = JSON.parse(raw);
        const restored = normalizeState(parsed);

        state.left = restored.left;
        state.terminal = restored.terminal;
        state.right = restored.right;

        /*
         * Focus mode is intentionally not restored.
         * A fresh page load should always start in normal mode.
         */
        state.focus = false;
    } catch (error) {
        console.warn(
            "[EAOS] Unable to restore pane layout",
            error
        );
    }
}

function saveState() {
    try {
        window.localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({
                left: state.left,
                terminal: state.terminal,
                right: state.right,
            })
        );
    } catch (error) {
        console.warn(
            "[EAOS] Unable to persist pane layout",
            error
        );
    }
}


/* =========================================================
 * EVENTS
 * ========================================================= */

function emitChange(reason) {
    const detail = {
        state: getState(),
        reason,
    };

    document.dispatchEvent(
        new CustomEvent(
            "eaos:layout-change",
            { detail }
        )
    );
}

function emitFocusChange() {
    document.dispatchEvent(
        new CustomEvent(
            "eaos:focus-change",
            {
                detail: {
                    focus: state.focus,
                    state: getState(),
                },
            }
        )
    );
}


/* =========================================================
 * VISIBILITY
 * ========================================================= */

function setHidden(element, hidden) {
    if (!element) {
        return;
    }

    element.classList.toggle(
        "eaos-pane-hidden",
        hidden
    );

    element.setAttribute(
        "aria-hidden",
        String(hidden)
    );

    /*
     * Keep a semantic state available to CSS,
     * diagnostics and future UI tooling.
     */
    element.dataset.paneState =
        hidden ? "hidden" : "visible";
}

function updateButton(
    button,
    visible,
    visibleTitle,
    hiddenTitle
) {
    if (!button) {
        return;
    }

    button.classList.toggle(
        "is-active",
        visible
    );

    button.setAttribute(
        "aria-pressed",
        String(visible)
    );

    button.dataset.state =
        visible ? "visible" : "hidden";

    button.title =
        visible
            ? visibleTitle
            : hiddenTitle;
}


/* =========================================================
 * LEFT PANE
 * ========================================================= */

function applyLeft() {
    const pane = byId(IDS.explorer);
    const resizer = byId(IDS.explorerResizer);
    const button = byId(IDS.toggleLeft);

    const visible =
        state.left && !state.focus;

    setHidden(pane, !visible);
    setHidden(resizer, !visible);

    updateButton(
        button,
        state.left,
        "Ẩn Cột Trái (Ctrl+B)",
        "Hiện Cột Trái (Ctrl+B)"
    );
}


/* =========================================================
 * TERMINAL
 * ========================================================= */

function applyTerminal() {
    const pane = byId(IDS.terminal);
    const resizer = byId(IDS.terminalResizer);
    const button = byId(IDS.toggleTerminal);

    const visible =
        state.terminal && !state.focus;

    setHidden(pane, !visible);
    setHidden(resizer, !visible);

    updateButton(
        button,
        state.terminal,
        "Ẩn Terminal (Ctrl+`)",
        "Hiện Terminal (Ctrl+`)"
    );
}


/* =========================================================
 * RIGHT PANE
 * ========================================================= */

function applyRight() {
    const pane = byId(IDS.right);
    const resizer = byId(IDS.rightResizer);
    const button = byId(IDS.toggleRight);

    const visible =
        state.right && !state.focus;

    setHidden(pane, !visible);
    setHidden(resizer, !visible);

    updateButton(
        button,
        state.right,
        "Ẩn Cột Phải (Ctrl+Shift+L)",
        "Hiện Cột Phải (Ctrl+Shift+L)"
    );
}


/* =========================================================
 * FOCUS MODE
 * ========================================================= */

function applyFocus() {
    const workspace = $(IDS.workspace);
    const button = byId(IDS.focus);

    if (!workspace) {
        return;
    }

    workspace.classList.toggle(
        "eaos-focus-mode",
        state.focus
    );

    document.body.classList.toggle(
        "eaos-focus-mode",
        state.focus
    );

    workspace.classList.toggle(
        "focus-left-hidden",
        state.focus
    );

    workspace.classList.toggle(
        "focus-right-hidden",
        state.focus
    );

    workspace.classList.toggle(
        "focus-terminal-hidden",
        state.focus
    );

    workspace.dataset.layoutMode =
        state.focus
            ? "focus"
            : "normal";

    if (button) {
        button.classList.toggle(
            "is-active",
            state.focus
        );

        button.setAttribute(
            "aria-pressed",
            String(state.focus)
        );

        button.dataset.state =
            state.focus
                ? "active"
                : "inactive";

        button.title =
            state.focus
                ? "Thoát Focus Mode (Ctrl+Shift+F)"
                : "Focus Mode (Ctrl+Shift+F)";
    }
}


/* =========================================================
 * RENDER
 * ========================================================= */

function render() {
    applyLeft();
    applyTerminal();
    applyRight();
    applyFocus();
}


/* =========================================================
 * MUTATION
 * ========================================================= */

function commit(reason) {
    render();
    saveState();
    emitChange(reason);
}

function toggleLeft() {
    state.left = !state.left;
    commit("toggle-left");
}

function toggleTerminal() {
    state.terminal = !state.terminal;
    commit("toggle-terminal");
}

function toggleRight() {
    state.right = !state.right;
    commit("toggle-right");
}


/* =========================================================
 * FOCUS CONTROL
 * ========================================================= */

function enterFocus() {
    if (state.focus) {
        return;
    }

    /*
     * Capture the current layout so future versions
     * can restore it deterministically.
     */
    focusSnapshot = {
        left: state.left,
        terminal: state.terminal,
        right: state.right,
    };

    state.focus = true;

    render();
    emitFocusChange();
    emitChange("enter-focus");
}

function exitFocus() {
    if (!state.focus) {
        return;
    }

    state.focus = false;

    /*
     * Restore the exact pre-focus visibility state.
     */
    if (focusSnapshot) {
        state.left = focusSnapshot.left;
        state.terminal = focusSnapshot.terminal;
        state.right = focusSnapshot.right;

        focusSnapshot = null;
    }

    commit("exit-focus");
    emitFocusChange();
}

function toggleFocus() {
    if (state.focus) {
        exitFocus();
    } else {
        enterFocus();
    }
}


/* =========================================================
 * RESET
 * ========================================================= */

function reset() {
    state.left = DEFAULT_STATE.left;
    state.terminal = DEFAULT_STATE.terminal;
    state.right = DEFAULT_STATE.right;

    state.focus = false;
    focusSnapshot = null;

    commit("reset");
    emitFocusChange();
}


/* =========================================================
 * KEYBOARD
 * ========================================================= */

function isTypingTarget(target) {
    return (
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement ||
        target?.isContentEditable
    );
}

function handleKeyboard(event) {
    const target = event.target;

    /*
     * Never intercept ordinary typing.
     */
    if (
        isTypingTarget(target) &&
        !event.ctrlKey &&
        !event.metaKey
    ) {
        return;
    }

    const modifier =
        event.ctrlKey ||
        event.metaKey;

    if (!modifier) {
        return;
    }

    const key =
        event.key.toLowerCase();

    /*
     * Ctrl+B
     */
    if (
        !event.shiftKey &&
        key === "b"
    ) {
        event.preventDefault();
        toggleLeft();
        return;
    }

    /*
     * Ctrl+`
     * Ctrl+~
     */
    if (
        !event.shiftKey &&
        (
            event.key === "`" ||
            event.key === "~"
        )
    ) {
        event.preventDefault();
        toggleTerminal();
        return;
    }

    /*
     * Ctrl+Shift+L
     */
    if (
        event.shiftKey &&
        key === "l"
    ) {
        event.preventDefault();
        toggleRight();
        return;
    }

    /*
     * Ctrl+Shift+F
     */
    if (
        event.shiftKey &&
        key === "f"
    ) {
        event.preventDefault();
        toggleFocus();
        return;
    }

    /*
     * Ctrl+Shift+0
     *
     * Reset IDE layout.
     */
    if (
        event.shiftKey &&
        event.key === "0"
    ) {
        event.preventDefault();
        reset();
    }
}


/* =========================================================
 * BINDINGS
 * ========================================================= */

function bind() {
    byId(IDS.toggleLeft)?.addEventListener(
        "click",
        toggleLeft
    );

    byId(IDS.toggleTerminal)?.addEventListener(
        "click",
        toggleTerminal
    );

    byId(IDS.toggleRight)?.addEventListener(
        "click",
        toggleRight
    );

    byId(IDS.focus)?.addEventListener(
        "click",
        toggleFocus
    );

    document.addEventListener(
        "keydown",
        handleKeyboard
    );
}


/* =========================================================
 * PUBLIC API
 * ========================================================= */

function exposeAPI() {
    window.EAOS =
        window.EAOS || {};

    window.EAOS.panes = {
        getState,

        render,

        reset,

        toggleLeft,
        toggleTerminal,
        toggleRight,
        toggleFocus,

        showLeft() {
            state.left = true;
            commit("show-left");
        },

        hideLeft() {
            state.left = false;
            commit("hide-left");
        },

        showTerminal() {
            state.terminal = true;
            commit("show-terminal");
        },

        hideTerminal() {
            state.terminal = false;
            commit("hide-terminal");
        },

        showRight() {
            state.right = true;
            commit("show-right");
        },

        hideRight() {
            state.right = false;
            commit("hide-right");
        },

        enterFocus,
        exitFocus,
    };
}


/* =========================================================
 * INIT
 * ========================================================= */

function init() {
    if (initialized) {
        return;
    }

    initialized = true;

    loadState();
    bind();
    exposeAPI();
    render();

    console.debug(
        "[EAOS] Pane / Layout Controller initialized",
        getState()
    );

    document.dispatchEvent(
        new CustomEvent(
            "eaos:layout-ready",
            {
                detail: {
                    state: getState(),
                },
            }
        )
    );
}


if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        init,
        { once: true }
    );
} else {
    init();
}
