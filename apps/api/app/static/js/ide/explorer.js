import { updateMonacoCode } from '../core/monaco_adapter.js';

export function initExplorer() {
    // Sử dụng event delegation trên document để tránh lỗi không bắt được sự kiện DOM
    document.addEventListener('click', async (e) => {
        const item = e.target.closest('.file-item');
        if (!item) return;

        // Xử lý đổi active UI style cho explorer
        document.querySelectorAll('.file-item').forEach(i => {
            i.classList.remove('text-cyan-400', 'bg-cyan-500/10');
        });
        item.classList.add('text-cyan-400', 'bg-cyan-500/10');

        const filePath = item.getAttribute('data-path');
        const editorTitle = document.getElementById('editor-title');
        const breadcrumb = document.getElementById('breadcrumb-path');

        if (editorTitle) editorTitle.textContent = `📝 ${filePath}`;
        if (breadcrumb) breadcrumb.textContent = filePath;

        try {
            console.log(`[Explorer] Fetching file content for: ${filePath}`);
            const res = await fetch(`/api/files/content?path=${encodeURIComponent(filePath)}`);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

            const data = await res.json();

            let lang = 'python';
            if (filePath.endsWith('.js')) lang = 'javascript';
            if (filePath.endsWith('.html')) lang = 'html';
            if (filePath.endsWith('.json')) lang = 'json';

            updateMonacoCode(data.content, lang);
            console.log(`[Explorer] Successfully loaded into Monaco Editor.`);
        } catch (err) {
            console.error('[Explorer] Error loading file:', err);
            updateMonacoCode(`# Error loading file: ${filePath}\n# ${err.message}`, 'python');
        }
    });
}
