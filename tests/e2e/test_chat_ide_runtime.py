import os

import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.getenv("EAOS_BASE_URL", "http://127.0.0.1:8000")
CHAT_URL = f"{BASE_URL}/chat"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1600, "height": 1000},
    }


@pytest.fixture
def chat(page: Page):
    page.goto(CHAT_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)

    expect(page.locator(".eaos-workspace-shell")).to_be_visible()

    return page


# ============================================================
# DOM CONTRACT
# ============================================================


def test_ide_dom_contract(chat: Page):
    required = [
        "#pane-left-explorer",
        "#pane-right-inspector",
        "#pane-bottom-terminal",
        "#resizer-explorer",
        "#resizer-copilot",
        "#resizer-terminal",
        "#btn-toggle-left",
        "#btn-toggle-terminal",
        "#btn-toggle-right",
        "#btn-focus-mode",
        "#act-explorer",
        "#act-search",
        "#act-source-control",
        "#act-ai-studio",
        "#act-doctor",
        "#monaco-editor-container",
        "#chat-form",
        "#chat-input",
        "#btn-send-chat",
        "#execution-trace",
    ]

    for selector in required:
        expect(chat.locator(selector)).to_have_count(1)


# ============================================================
# PANE TOGGLES
# ============================================================


@pytest.mark.parametrize(
    "button, pane",
    [
        ("#btn-toggle-left", "#pane-left-explorer"),
        ("#btn-toggle-terminal", "#pane-bottom-terminal"),
        ("#btn-toggle-right", "#pane-right-inspector"),
    ],
)
def test_pane_toggle(chat: Page, button, pane):
    target = chat.locator(pane)

    initial_hidden = target.is_hidden()

    chat.locator(button).click()
    chat.wait_for_timeout(150)

    assert target.is_hidden() != initial_hidden

    chat.locator(button).click()
    chat.wait_for_timeout(150)

    assert target.is_hidden() == initial_hidden


# ============================================================
# FOCUS MODE
# ============================================================


def test_focus_mode(chat: Page):
    shell = chat.locator(".eaos-workspace-shell")

    before = shell.evaluate("(el) => el.classList.contains('eaos-focus-mode')")

    chat.locator("#btn-focus-mode").click()
    chat.wait_for_timeout(150)

    after = shell.evaluate("(el) => el.classList.contains('eaos-focus-mode')")

    assert after != before

    chat.locator("#btn-focus-mode").click()
    chat.wait_for_timeout(150)

    restored = shell.evaluate("(el) => el.classList.contains('eaos-focus-mode')")

    assert restored == before


# ============================================================
# ACTIVITY BAR
# ============================================================


@pytest.mark.parametrize(
    "activity",
    [
        "explorer",
        "search",
        "source-control",
        "ai-studio",
        "doctor",
    ],
)
def test_activity_bar(activity, chat: Page):
    button = chat.locator(f'[data-activity="{activity}"]')

    expect(button).to_have_count(1)

    button.click()
    chat.wait_for_timeout(100)

    expect(button).to_have_attribute(
        "aria-pressed",
        "true",
    )

    state = chat.evaluate("() => window.EAOS && window.EAOS.activity")

    assert state is not None


# ============================================================
# ACTIVITY BAR KEYBOARD
# ============================================================


def test_activity_keyboard_navigation(chat: Page):
    buttons = chat.locator(".eaos-activity-nav [data-activity]")

    expect(buttons).to_have_count(5)

    buttons.first.focus()

    chat.keyboard.press("ArrowDown")
    chat.wait_for_timeout(100)

    focused = chat.locator(":focus")

    expect(focused).to_have_attribute(
        "data-activity",
        "search",
    )

    chat.keyboard.press("ArrowDown")
    chat.wait_for_timeout(100)

    expect(chat.locator(":focus")).to_have_attribute(
        "data-activity",
        "source-control",
    )


# ============================================================
# RESIZER HELPERS
# ============================================================


def rect(page: Page, selector: str):
    return page.locator(selector).bounding_box()


def drag_horizontal(page: Page, selector: str, delta: int):
    box = rect(page, selector)

    assert box is not None

    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2

    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x + delta, y, steps=15)
    page.mouse.up()

    page.wait_for_timeout(150)


def drag_vertical(page: Page, selector: str, delta: int):
    box = rect(page, selector)

    assert box is not None

    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2

    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x, y + delta, steps=15)
    page.mouse.up()

    page.wait_for_timeout(150)


# ============================================================
# EXPLORER RESIZER
# ============================================================


def test_explorer_resizer_drag(chat: Page):
    pane = chat.locator("#pane-left-explorer")

    before = pane.bounding_box()
    assert before is not None

    drag_horizontal(
        chat,
        "#resizer-explorer",
        100,
    )

    after = pane.bounding_box()
    assert after is not None

    assert abs(after["width"] - before["width"]) >= 30


# ============================================================
# RIGHT / COPILOT RESIZER
# ============================================================


def test_copilot_resizer_drag(chat: Page):
    pane = chat.locator("#pane-right-inspector")

    before = pane.bounding_box()
    assert before is not None

    drag_horizontal(
        chat,
        "#resizer-copilot",
        -100,
    )

    after = pane.bounding_box()
    assert after is not None

    assert abs(after["width"] - before["width"]) >= 30


# ============================================================
# TERMINAL RESIZER
# ============================================================


def test_terminal_resizer_drag(chat: Page):
    pane = chat.locator("#pane-bottom-terminal")

    before = pane.bounding_box()
    assert before is not None

    drag_vertical(
        chat,
        "#resizer-terminal",
        -100,
    )

    after = pane.bounding_box()
    assert after is not None

    assert abs(after["height"] - before["height"]) >= 30


# ============================================================
# KEYBOARD RESIZE
# ============================================================


def test_keyboard_resize(chat: Page):
    resizer = chat.locator("#resizer-explorer")

    resizer.focus()

    before = chat.locator("#pane-left-explorer").bounding_box()

    assert before is not None

    chat.keyboard.press("ArrowRight")
    chat.wait_for_timeout(100)

    after = chat.locator("#pane-left-explorer").bounding_box()

    assert after is not None

    assert after["width"] != before["width"]


# ============================================================
# LAYOUT PERSISTENCE
# ============================================================


def test_layout_persistence(chat: Page):
    pane = chat.locator("#pane-left-explorer")

    before = pane.bounding_box()
    assert before is not None

    drag_horizontal(
        chat,
        "#resizer-explorer",
        120,
    )

    changed = pane.bounding_box()
    assert changed is not None

    assert abs(changed["width"] - before["width"]) >= 30

    persisted_width = changed["width"]

    chat.reload(wait_until="domcontentloaded")
    chat.wait_for_timeout(500)

    restored = pane.bounding_box()
    assert restored is not None

    assert abs(restored["width"] - persisted_width) <= 8


# ============================================================
# VISIBILITY PERSISTENCE
# ============================================================


def test_visibility_persistence(chat: Page):
    pane = chat.locator("#pane-bottom-terminal")
    button = chat.locator("#btn-toggle-terminal")

    initial = pane.is_hidden()

    button.click()
    chat.wait_for_timeout(150)

    changed = pane.is_hidden()

    assert changed != initial

    chat.reload(wait_until="domcontentloaded")
    chat.wait_for_timeout(500)

    restored = pane.is_hidden()

    assert restored == changed

    # Restore normal state for this browser context.
    button = chat.locator("#btn-toggle-terminal")

    if restored != initial:
        button.click()


# ============================================================
# MONACO
# ============================================================


def test_monaco_editor(chat: Page):
    host = chat.locator("#monaco-editor-container")

    expect(host).to_be_visible()

    result = chat.evaluate(
        """
        () => ({
            monaco: typeof window.monaco !== "undefined",
            editors:
                typeof window.monaco !== "undefined" &&
                typeof window.monaco.editor !== "undefined"
                    ? window.monaco.editor.getEditors().length
                    : 0
        })
        """
    )

    assert result["monaco"] is True
    assert result["editors"] >= 1


# ============================================================
# CHAT INPUT
# ============================================================


def test_chat_input(chat: Page):
    input_box = chat.locator("#chat-input")
    form = chat.locator("#chat-form")
    send = chat.locator("#btn-send-chat")

    expect(input_box).to_be_visible()
    expect(form).to_have_count(1)
    expect(send).to_have_count(1)

    input_box.fill("EAOS runtime test")

    expect(input_box).to_have_value("EAOS runtime test")


# ============================================================
# CHAT SEND EVENT
# ============================================================


def test_chat_send_event(chat: Page):
    chat.evaluate(
        """
        () => {
            window.__eaosChatSubmit = false;

            window.addEventListener(
                "eaos:chat-submit",
                () => {
                    window.__eaosChatSubmit = true;
                },
                { once: true }
            );
        }
        """
    )

    chat.locator("#chat-input").fill("EAOS integration test")

    chat.locator("#btn-send-chat").click()

    chat.wait_for_timeout(200)

    result = chat.evaluate("() => window.__eaosChatSubmit === true")

    assert result is True


# ============================================================
# EXECUTION TRACE
# ============================================================


def test_execution_trace(chat: Page):
    trace = chat.locator("#execution-trace")
    toggle = chat.locator("#btn-toggle-execution")

    expect(trace).to_have_count(1)
    expect(toggle).to_have_count(1)

    before = trace.is_visible()

    toggle.click()
    chat.wait_for_timeout(100)

    after = trace.is_visible()

    assert after != before

    toggle.click()


# ============================================================
# UI RUNTIME
# ============================================================


def test_ui_runtime_contract(chat: Page):
    result = chat.evaluate(
        """
        () => ({
            eaos: typeof window.EAOS !== "undefined",
            ui: !!window.EAOS?.ui,
            activity: !!window.EAOS?.activity,
            panes: !!window.EAOS?.panes,
            layout: !!window.EAOS?.layout
        })
        """
    )

    assert result["eaos"] is True
    assert result["ui"] is True
    assert result["activity"] is True
    assert result["panes"] is True
    assert result["layout"] is True
