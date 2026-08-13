export function initModelRouter() {
    const selector = document.getElementById('model-provider-select');
    const badge = document.getElementById('active-model-badge');

    if (selector && badge) {
        selector.addEventListener('change', () => {
            const selectedText = selector.options[selector.selectedIndex].text;
            badge.textContent = `Model: ${selectedText}`;
        });
    }
}