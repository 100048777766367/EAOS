/**
 * EAOS IDE Runtime Coordinator
 *
 * Owns:
 * - runtime-level IDE state observation
 * - controller event observation
 * - DOM readiness diagnostics
 *
 * Does NOT own:
 * - pane visibility
 * - pane dimensions
 * - activity selection
 * - Monaco
 * - WebSocket
 * - AI runtime
 */

const state = {
    initialized: false,
    activity: null,

    panes: {
        left: null,
        right: null,
        terminal: null,
    },

    sizes: {
        explorer: null,
        right: null,
        terminal: null,
    },

    events: {
        activity: 0,
        pane: 0,
        resize: 0,
    },

    dom: {
        workspace: false,
        editor: false,
        monaco: false,
        chat: false,
    },
};

function ensureEAOS() {
    window.EAOS = window.EAOS || {};
    return window.EAOS;
}

function byId(id) {
    return document.getElementById(id);
}

function detectDOM() {
    state.dom.workspace =
        !!document.querySelector(".eaos-workspace-shell");

    state.dom.editor =
        !!document.querySelector(
            '[data-eaos-pane="editor"]'
        );

    state.dom.monaco =
        !!document.querySelector(
            '[data-editor-host="monaco"]'
        );

    state.dom.chat =
        !!document.querySelector(
            '[data-eaos-pane="chat"]'
        );
}

function readPaneState() {
    const panes = {
        left: byId("pane-left-explorer"),
        right: byId("pane-right-inspector"),
        terminal: byId("pane-bottom-terminal"),
    };

    for (const [name, element] of Object.entries(panes)) {
        state.panes[name] = element
            ? !element.classList.contains(
                "eaos-pane-hidden"
            )
            : null;
    }
}

function readLayoutState() {
    const layout = window.EAOS?.layout;

    if (!layout || typeof layout.getState !== "function") {
        return;
    }

    const layoutState = layout.getState();

    state.sizes.explorer =
        layoutState.explorer ?? null;

    state.sizes.right =
        layoutState.right ?? null;

    state.sizes.terminal =
        layoutState.terminal ?? null;
}

function refreshState() {
    detectDOM();
    readPaneState();
    readLayoutState();
}

function handleActivity(event) {
    state.events.activity += 1;

    const detail = event.detail || {};

    state.activity =
        detail.activity ??
        detail.id ??
        detail.name ??
        null;
}

function handlePane(event) {
    state.events.pane += 1;

    const detail = event.detail || {};

    if (typeof detail.left === "boolean") {
        state.panes.left = detail.left;
    }

    if (typeof detail.right === "boolean") {
        state.panes.right = detail.right;
    }

    if (typeof detail.terminal === "boolean") {
        state.panes.terminal = detail.terminal;
    }

    readPaneState();
}

function handleResize() {
    state.events.resize += 1;
    readLayoutState();
}

function bindEvents() {
    document.addEventListener(
        "eaos:activity",
        handleActivity
    );

    document.addEventListener(
        "eaos:pane",
        handlePane
    );

    document.addEventListener(
        "eaos:resize",
        handleResize
    );
}

function getState() {
    refreshState();

    return {
        initialized: state.initialized,
        activity: state.activity,
        panes: { ...state.panes },
        sizes: { ...state.sizes },
        dom: { ...state.dom },
        events: { ...state.events },
    };
}

function exposeAPI() {
    const EAOS = ensureEAOS();

    EAOS.ide = {
        getState,

        refresh() {
            return getState();
        },

        validate() {
            return getState();
        },

        isReady() {
            refreshState();

            return (
                state.initialized &&
                state.dom.workspace &&
                state.dom.editor &&
                state.dom.monaco &&
                state.dom.chat
            );
        },
    };
}

function init() {
    ensureEAOS();

    bindEvents();
    exposeAPI();
    refreshState();

    state.initialized = true;

    console.debug(
        "[EAOS] IDE runtime coordinator initialized",
        getState()
    );

    window.dispatchEvent(
        new CustomEvent("eaos:ide-ready", {
            detail: getState(),
        })
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
