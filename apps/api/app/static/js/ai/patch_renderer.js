export function renderPatchDiff(diffText) {
    const box = document.getElementById('exec-result-box');
    if (box) box.textContent = diffText;
}
