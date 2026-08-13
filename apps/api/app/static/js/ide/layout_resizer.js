/**
 * EAOS IDE — Layout Resizer
 *
 * Owns:
 * - Explorer width
 * - Right inspector/copilot width
 * - Bottom terminal height
 * - Pointer dragging
 * - Keyboard resizing
 * - Min/max constraints
 * - CSS dimension synchronization
 * - LocalStorage persistence
 * - Resize lifecycle events
 *
 * Does NOT own:
 * - pane visibility
 * - focus mode
 * - Monaco
 * - chat
 * - AI runtime
 * - WebSocket
 * - application state
 *
 * IMPORTANT:
 * This module NEVER auto-initializes itself.
 *
 * main.js must explicitly call:
 *
 *     initIDELayoutResizers();
 */

/* =========================================================
 * CONSTANTS
 * ========================================================= */

const RESIZER_IDS = Object.freeze({
    explorer: "resizer-explorer",
    right: "resizer-copilot",
    terminal: "resizer-terminal",
});

const PANE_IDS = Object.freeze({
    explorer: "pane-left-explorer",
    right: "pane-right-inspector",
    terminal: "pane-bottom-terminal",
});

const WORKSPACE_SELECTOR = ".eaos-workspace-shell";

const STORAGE_KEY = "eaos.ide.pane-sizes.v2";

const KEYBOARD_STEP = 16;

const LIMITS = Object.freeze({
    explorer: Object.freeze({
        min: 180,
        max: 520,
        fallback: 280,
    }),

    right: Object.freeze({
        min: 260,
        max: 620,
        fallback: 360,
    }),

    terminal: Object.freeze({
        min: 140,
        max: 900,
        fallback: 260,
    }),
});

/* =========================================================
 * INTERNAL STATE
 * ========================================================= */

const state = {
    explorer: null,
    right: null,
    terminal: null,

    active: null,
    dragging: false,

    pointerId: null,

    startX: 0,
    startY: 0,
    startSize: 0,
};

let initialized = false;

/* =========================================================
 * DOM HELPERS
 * ========================================================= */

function byId(id) {
    return document.getElementById(id);
}

function getWorkspace() {
    return document.querySelector(
        WORKSPACE_SELECTOR
    );
}

function getPane(type) {
    const id = PANE_IDS[type];

    if (!id) {
        return null;
    }

    return byId(id);
}

function getResizer(type) {
    const id = RESIZER_IDS[type];

    if (!id) {
        return null;
    }

    return byId(id);
}

/* =========================================================
 * VALUE HELPERS
 * ========================================================= */

function toNumber(value) {
    const parsed = Number.parseFloat(value);

    return Number.isFinite(parsed)
        ? parsed
        : null;
}

function clamp(value, min, max) {
    return Math.min(
        Math.max(value, min),
        max
    );
}

function isValidType(type) {
    return Boolean(LIMITS[type]);
}

/* =========================================================
 * LIMITS
 * ========================================================= */

function getLimits(type) {
    const base = LIMITS[type];

    if (!base) {
        return null;
    }

    const limits = {
        min: base.min,
        max: base.max,
        fallback: base.fallback,
    };

    if (type !== "terminal") {
        return limits;
    }

    const shell = getWorkspace();

    if (!shell) {
        return limits;
    }

    const rect = shell.getBoundingClientRect();

    const editorReserve = 120;

    const dynamicMax = Math.floor(
        rect.height - editorReserve
    );

    if (
        Number.isFinite(dynamicMax) &&
        dynamicMax > limits.min
    ) {
        limits.max = Math.min(
            limits.max,
            dynamicMax
        );
    }

    return limits;
}

/* =========================================================
 * SIZE READING
 * ========================================================= */

function getAxis(type) {
    return type === "terminal"
        ? "height"
        : "width";
}

function readComputedSize(pane, axis) {
    if (!pane) {
        return null;
    }

    const computed =
        window.getComputedStyle(pane);

    return axis === "height"
        ? toNumber(computed.height)
        : toNumber(computed.width);
}

function getCurrentSize(type) {
    if (!isValidType(type)) {
        return null;
    }

    const pane = getPane(type);

    if (!pane) {
        return LIMITS[type].fallback;
    }

    const storedDatasetSize =
        toNumber(
            pane.dataset.eaosSize
        );

    if (storedDatasetSize !== null) {
        return storedDatasetSize;
    }

    const computedSize =
        readComputedSize(
            pane,
            getAxis(type)
        );

    if (computedSize !== null) {
        return computedSize;
    }

    return LIMITS[type].fallback;
}

/* =========================================================
 * PERSISTENCE
 * ========================================================= */

function loadState() {
    try {
        const raw =
            window.localStorage.getItem(
                STORAGE_KEY
            );

        if (!raw) {
            return null;
        }

        const parsed =
            JSON.parse(raw);

        if (
            !parsed ||
            typeof parsed !== "object" ||
            Array.isArray(parsed)
        ) {
            return null;
        }

        return parsed;
    } catch (error) {
        console.warn(
            "[EAOS] Failed to load layout state",
            error
        );

        return null;
    }
}

function saveState() {
    try {
        window.localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({
                explorer: state.explorer,
                right: state.right,
                terminal: state.terminal,
            })
        );

        return true;
    } catch (error) {
        console.warn(
            "[EAOS] Failed to save layout state",
            error
        );

        return false;
    }
}

function clearSavedState() {
    try {
        window.localStorage.removeItem(
            STORAGE_KEY
        );

        return true;
    } catch (error) {
        console.warn(
            "[EAOS] Failed to clear layout state",
            error
        );

        return false;
    }
}

/* =========================================================
 * INITIAL STATE
 * ========================================================= */

function resolveInitialSize(type, persisted) {
    const limits = LIMITS[type];

    const persistedSize =
        toNumber(
            persisted?.[type]
        );

    if (persistedSize !== null) {
        return clamp(
            persistedSize,
            limits.min,
            limits.max
        );
    }

    const currentSize =
        getCurrentSize(type);

    return clamp(
        currentSize,
        limits.min,
        limits.max
    );
}

function loadInitialState() {
    const persisted = loadState();

    state.explorer =
        resolveInitialSize(
            "explorer",
            persisted
        );

    state.right =
        resolveInitialSize(
            "right",
            persisted
        );

    state.terminal =
        resolveInitialSize(
            "terminal",
            persisted
        );
}

/* =========================================================
 * EVENTS
 * ========================================================= */

function getPublicState() {
    return {
        explorer: state.explorer,
        right: state.right,
        terminal: state.terminal,

        active: state.active,
        dragging: state.dragging,
    };
}

function emit(type, detail = {}) {
    document.dispatchEvent(
        new CustomEvent(
            type,
            {
                detail,
            }
        )
    );
}

function emitResize(type) {
    emit(
        "eaos:resize",
        {
            type,
            size: state[type],
            state: getPublicState(),
        }
    );
}

function emitResizeStart(type) {
    emit(
        "eaos:resize-start",
        {
            type,
            size: getCurrentSize(type),
        }
    );
}

function emitResizeEnd(type) {
    emit(
        "eaos:resize-end",
        {
            type,
            size: state[type],
        }
    );
}

/* =========================================================
 * CSS APPLICATION
 * ========================================================= */

function applyPaneSize(
    type,
    size,
    options = {}
) {
    if (!isValidType(type)) {
        return false;
    }

    const pane = getPane(type);

    if (!pane) {
        return false;
    }

    const numericSize = toNumber(size);

    if (numericSize === null) {
        return false;
    }

    const limits = getLimits(type);

    const next = clamp(
        numericSize,
        limits.min,
        limits.max
    );

    state[type] = next;

    const rounded =
        Math.round(next);

    pane.dataset.eaosSize =
        String(rounded);

    if (type === "terminal") {
        const value = `${rounded}px`;

        pane.style.height = value;
        pane.style.minHeight = value;
        pane.style.maxHeight = value;
    } else {
        const value = `${rounded}px`;

        pane.style.width = value;
        pane.style.minWidth = value;
        pane.style.maxWidth = value;
    }

    if (!options.silent) {
        saveState();
        emitResize(type);
    }

    return true;
}

function applyAllSizes() {
    if (state.explorer !== null) {
        applyPaneSize(
            "explorer",
            state.explorer,
            { silent: true }
        );
    }

    if (state.right !== null) {
        applyPaneSize(
            "right",
            state.right,
            { silent: true }
        );
    }

    if (state.terminal !== null) {
        applyPaneSize(
            "terminal",
            state.terminal,
            { silent: true }
        );
    }
}

/* =========================================================
 * POINTER RESIZE
 * ========================================================= */

function beginDrag(type, event) {
    const resizer = getResizer(type);
    const pane = getPane(type);

    if (!resizer || !pane) {
        return;
    }

    if (
        event.button !== undefined &&
        event.button !== 0
    ) {
        return;
    }

    state.active = type;
    state.dragging = true;

    state.pointerId =
        event.pointerId ?? null;

    state.startX =
        event.clientX;

    state.startY =
        event.clientY;

    state.startSize =
        getCurrentSize(type);

    resizer.style.touchAction = "none";

    resizer.classList.add(
        "is-resizing"
    );

    document.body.classList.add(
        "eaos-resizing"
    );

    document.body.classList.add(
        `eaos-resizing-${type}`
    );

    if (
        event.pointerId !== undefined &&
        typeof resizer.setPointerCapture ===
            "function"
    ) {
        try {
            resizer.setPointerCapture(
                event.pointerId
            );
        } catch {
            /* Pointer capture is optional. */
        }
    }

    emitResizeStart(type);

    event.preventDefault();
}

function updateDrag(event) {
    if (
        !state.dragging ||
        !state.active
    ) {
        return;
    }

    const type = state.active;

    const deltaX =
        event.clientX -
        state.startX;

    const deltaY =
        event.clientY -
        state.startY;

    let nextSize;

    switch (type) {
        case "explorer":
            nextSize =
                state.startSize +
                deltaX;
            break;

        case "right":
            nextSize =
                state.startSize -
                deltaX;
            break;

        case "terminal":
            nextSize =
                state.startSize -
                deltaY;
            break;

        default:
            return;
    }

    applyPaneSize(
        type,
        nextSize
    );
}

function endDrag() {
    if (!state.dragging) {
        return;
    }

    const type = state.active;

    const resizer =
        type
            ? getResizer(type)
            : null;

    if (resizer) {
        resizer.classList.remove(
            "is-resizing"
        );

        if (
            state.pointerId !== null &&
            typeof resizer.releasePointerCapture ===
                "function"
        ) {
            try {
                resizer.releasePointerCapture(
                    state.pointerId
                );
            } catch {
                /* Pointer capture may already be released. */
            }
        }
    }

    document.body.classList.remove(
        "eaos-resizing"
    );

    if (type) {
        document.body.classList.remove(
            `eaos-resizing-${type}`
        );

        emitResizeEnd(type);
    }

    state.active = null;
    state.dragging = false;
    state.pointerId = null;
}

/* =========================================================
 * KEYBOARD RESIZE
 * ========================================================= */

function resizeByKeyboard(type, direction) {
    const current =
        getCurrentSize(type);

    if (current === null) {
        return;
    }

    const delta =
        direction === "positive"
            ? KEYBOARD_STEP
            : -KEYBOARD_STEP;

    applyPaneSize(
        type,
        current + delta
    );
}

function handleKeydown(type, event) {
    const key = event.key;

    const limits = getLimits(type);

    if (key === "Home") {
        event.preventDefault();

        applyPaneSize(
            type,
            limits.min
        );

        return;
    }

    if (key === "End") {
        event.preventDefault();

        applyPaneSize(
            type,
            limits.max
        );

        return;
    }

    if (type === "explorer") {
        if (key === "ArrowRight") {
            event.preventDefault();

            resizeByKeyboard(
                type,
                "positive"
            );

            return;
        }

        if (key === "ArrowLeft") {
            event.preventDefault();

            resizeByKeyboard(
                type,
                "negative"
            );

            return;
        }
    }

    if (type === "right") {
        if (key === "ArrowLeft") {
            event.preventDefault();

            resizeByKeyboard(
                type,
                "positive"
            );

            return;
        }

        if (key === "ArrowRight") {
            event.preventDefault();

            resizeByKeyboard(
                type,
                "negative"
            );

            return;
        }
    }

    if (type === "terminal") {
        if (key === "ArrowUp") {
            event.preventDefault();

            resizeByKeyboard(
                type,
                "positive"
            );

            return;
        }

        if (key === "ArrowDown") {
            event.preventDefault();

            resizeByKeyboard(
                type,
                "negative"
            );

            return;
        }
    }
}

/* =========================================================
 * RESIZER BINDING
 * ========================================================= */

function setupResizer(type) {
    const resizer = getResizer(type);

    if (!resizer) {
        console.debug(
            `[EAOS] Resizer not present: ${type}`
        );

        return;
    }

    if (
        resizer.dataset.eaosResizeBound ===
        "true"
    ) {
        return;
    }

    resizer.dataset.eaosResizeBound =
        "true";

    resizer.setAttribute(
        "role",
        "separator"
    );

    resizer.setAttribute(
        "tabindex",
        "0"
    );

    resizer.setAttribute(
        "aria-orientation",
        type === "terminal"
            ? "horizontal"
            : "vertical"
    );

    resizer.addEventListener(
        "pointerdown",
        event => {
            beginDrag(
                type,
                event
            );
        }
    );

    resizer.addEventListener(
        "keydown",
        event => {
            handleKeydown(
                type,
                event
            );
        }
    );

    resizer.addEventListener(
        "dblclick",
        event => {
            event.preventDefault();

            applyPaneSize(
                type,
                LIMITS[type].fallback
            );
        }
    );
}

/* =========================================================
 * GLOBAL EVENTS
 * ========================================================= */

function bindGlobalEvents() {
    if (
        document.documentElement.dataset
            .eaosLayoutGlobalBound ===
        "true"
    ) {
        return;
    }

    document.documentElement.dataset
        .eaosLayoutGlobalBound =
        "true";

    document.addEventListener(
        "pointermove",
        updateDrag
    );

    document.addEventListener(
        "pointerup",
        endDrag
    );

    document.addEventListener(
        "pointercancel",
        endDrag
    );

    window.addEventListener(
        "blur",
        endDrag
    );

    window.addEventListener(
        "resize",
        handleViewportResize
    );
}

/* =========================================================
 * VIEWPORT
 * ========================================================= */

function handleViewportResize() {
    if (state.terminal === null) {
        return;
    }

    const limits =
        getLimits("terminal");

    if (
        state.terminal >
        limits.max
    ) {
        applyPaneSize(
            "terminal",
            limits.max
        );

        return;
    }

    if (
        state.terminal <
        limits.min
    ) {
        applyPaneSize(
            "terminal",
            limits.min
        );
    }
}

/* =========================================================
 * PUBLIC API
 * ========================================================= */

function exposeAPI() {
    window.EAOS =
        window.EAOS || {};

    window.EAOS.layout = {
        getState() {
            return getPublicState();
        },

        getSize(type) {
            if (!isValidType(type)) {
                return null;
            }

            return getCurrentSize(type);
        },

        setSize(type, size) {
            if (!isValidType(type)) {
                return false;
            }

            return applyPaneSize(
                type,
                size
            );
        },

        reset(type) {
            if (!isValidType(type)) {
                return false;
            }

            return applyPaneSize(
                type,
                LIMITS[type].fallback
            );
        },

        resetAll() {
            const explorer =
                applyPaneSize(
                    "explorer",
                    LIMITS.explorer.fallback
                );

            const right =
                applyPaneSize(
                    "right",
                    LIMITS.right.fallback
                );

            const terminal =
                applyPaneSize(
                    "terminal",
                    LIMITS.terminal.fallback
                );

            return (
                explorer &&
                right &&
                terminal
            );
        },

        save() {
            return saveState();
        },

        clearSaved() {
            return clearSavedState();
        },

        render() {
            loadInitialState();
            applyAllSizes();

            return getPublicState();
        },
    };
}

/* =========================================================
 * EXPORTED INITIALIZER
 *
 * IMPORTANT:
 * There is intentionally NO:
 *
 *     init();
 *
 * There is intentionally NO:
 *
 *     DOMContentLoaded
 *
 * main.js owns initialization.
 * ========================================================= */

export function initIDELayoutResizers() {
    if (initialized) {
        return getPublicState();
    }

    initialized = true;

    loadInitialState();

    setupResizer("explorer");
    setupResizer("right");
    setupResizer("terminal");

    bindGlobalEvents();

    exposeAPI();

    applyAllSizes();

    const shell = getWorkspace();

    if (shell) {
        shell.dataset.resizeState =
            "ready";
    }

    const publicState =
        getPublicState();

    console.debug(
        "[EAOS] Layout resizer initialized",
        publicState
    );

    emit(
        "eaos:layout-resizer-ready",
        {
            state: publicState,
        }
    );

    return publicState;
}