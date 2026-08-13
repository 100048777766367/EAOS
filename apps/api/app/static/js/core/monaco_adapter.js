let monacoEditor = null;

const MONACO_VERSION = "0.44.0";
const MONACO_CDN =
    `https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/${MONACO_VERSION}/min/vs`;

let monacoLoadPromise = null;


/**
 * Resolve the editor container.
 */
function getContainer(containerId) {
    const container = document.getElementById(containerId);

    if (!container) {
        throw new Error(
            `[EAOS Monaco] Container not found: #${containerId}`
        );
    }

    return container;
}


/**
 * Ensure the editor host has an actual layout height.
 *
 * Monaco cannot initialize correctly when its host has height: 0.
 */
function ensureContainerLayout(container) {
    container.style.width = "100%";
    container.style.height = "100%";
    container.style.minHeight = "250px";
    container.style.display = "block";
    container.style.visibility = "visible";

    /*
     * The parent editor pane is flex-based.
     * Make sure the host participates in the flex layout.
     */
    container.classList.add(
        "flex-1",
        "min-h-0"
    );
}


/**
 * Load Monaco exactly once.
 */
function loadMonaco() {
    if (
        window.monaco &&
        window.monaco.editor
    ) {
        return Promise.resolve(window.monaco);
    }

    if (monacoLoadPromise) {
        return monacoLoadPromise;
    }

    monacoLoadPromise = new Promise(
        (resolve, reject) => {
            const existingLoader =
                document.querySelector(
                    'script[data-eaos-monaco-loader="true"]'
                );

            function configureAndLoad() {
                if (!window.require) {
                    reject(
                        new Error(
                            "[EAOS Monaco] AMD loader is unavailable after loader script."
                        )
                    );
                    return;
                }

                try {
                    window.require.config({
                        paths: {
                            vs: MONACO_CDN
                        }
                    });

                    window.require(
                        [
                            "vs/editor/editor.main"
                        ],
                        () => {
                            if (
                                !window.monaco ||
                                !window.monaco.editor
                            ) {
                                reject(
                                    new Error(
                                        "[EAOS Monaco] Monaco module loaded but window.monaco.editor is missing."
                                    )
                                );
                                return;
                            }

                            resolve(
                                window.monaco
                            );
                        },
                        (error) => {
                            reject(
                                new Error(
                                    `[EAOS Monaco] AMD module load failed: ${error?.message || error}`
                                )
                            );
                        }
                    );
                } catch (error) {
                    reject(error);
                }
            }


            if (window.require) {
                configureAndLoad();
                return;
            }


            if (existingLoader) {
                existingLoader.addEventListener(
                    "load",
                    configureAndLoad,
                    { once: true }
                );

                existingLoader.addEventListener(
                    "error",
                    () => {
                        reject(
                            new Error(
                                "[EAOS Monaco] Existing loader script failed."
                            )
                        );
                    },
                    { once: true }
                );

                return;
            }


            const script =
                document.createElement("script");

            script.src =
                `${MONACO_CDN}/loader.min.js`;

            script.async = true;

            script.dataset.eaosMonacoLoader =
                "true";

            script.onload =
                configureAndLoad;

            script.onerror = () => {
                reject(
                    new Error(
                        `[EAOS Monaco] Failed to load ${script.src}`
                    )
                );
            };

            document.head.appendChild(
                script
            );
        }
    );

    return monacoLoadPromise;
}


/**
 * Create the actual Monaco editor.
 */
function setupMonaco(
    containerId,
    initialCode,
    language
) {
    const container =
        getContainer(containerId);

    ensureContainerLayout(container);

    if (monacoEditor) {
        try {
            monacoEditor.dispose();
        } catch {
            // Ignore stale Monaco instances.
        }

        monacoEditor = null;
    }

    container.innerHTML = "";

    monacoEditor =
        window.monaco.editor.create(
            container,
            {
                value: initialCode,
                language,
                theme: "vs-dark",
                automaticLayout: true,
                fontSize: 12,
                fontFamily:
                    "'Fira Code', monospace",
                minimap: {
                    enabled: false
                },
                scrollBeyondLastLine: false,
                readOnly: false
            }
        );

    /*
     * Force Monaco to calculate its dimensions
     * after the flex layout has settled.
     */
    requestAnimationFrame(() => {
        try {
            monacoEditor?.layout();
        } catch {
            // Ignore layout race.
        }
    });

    window.setTimeout(() => {
        try {
            monacoEditor?.layout();
        } catch {
            // Ignore layout race.
        }
    }, 100);

    window.__EAOS_MONACO_READY__ = true;

    window.dispatchEvent(
        new CustomEvent(
            "eaos:monaco-ready",
            {
                detail: {
                    container,
                    editor: monacoEditor
                }
            }
        )
    );

    return monacoEditor;
}


/**
 * Public initialization API.
 */
export async function initMonacoAdapter(
    containerId,
    initialCode = "",
    language = "python"
) {
    const container =
        getContainer(containerId);

    ensureContainerLayout(container);

    try {
        await loadMonaco();

        return setupMonaco(
            containerId,
            initialCode,
            language
        );
    } catch (error) {
        window.__EAOS_MONACO_READY__ = false;
        window.__EAOS_MONACO_ERROR__ =
            String(
                error?.message || error
            );

        console.error(
            "[EAOS Monaco]",
            error
        );

        /*
         * Do not silently swallow the failure.
         * main.js can catch/report it while the rest
         * of the IDE continues running.
         */
        throw error;
    }
}


/**
 * Replace editor contents.
 */
export function updateMonacoCode(
    code,
    language = "python"
) {
    if (!monacoEditor) {
        console.warn(
            "[EAOS Monaco] updateMonacoCode called before editor initialization."
        );
        return;
    }

    const oldModel =
        monacoEditor.getModel();

    const model =
        window.monaco.editor.createModel(
            String(code ?? ""),
            language
        );

    monacoEditor.setModel(model);

    if (oldModel) {
        oldModel.dispose();
    }

    requestAnimationFrame(() => {
        try {
            monacoEditor?.layout();
        } catch {
            // Ignore layout race.
        }
    });
}


/**
 * Read current editor contents.
 */
export function getMonacoCode() {
    return monacoEditor
        ? monacoEditor.getValue()
        : "";
}


/**
 * Optional diagnostic access.
 */
export function getMonacoEditor() {
    return monacoEditor;
}
