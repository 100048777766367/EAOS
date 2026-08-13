/**
 * EAOS Resizable Panes Engine - Drag & Drop Panel Resizer
 */

export function initResizablePanes() {
    console.log("↔️ Resizable Panes Initialized.");

    // 1. Resizer Cột trái (File Explorer)
    const leftSidebar = document.getElementById('pane-explorer') || document.querySelector('.w-56');
    const leftResizer = document.getElementById('resizer-left');

    if (leftResizer && leftSidebar) {
        let isResizing = false;

        leftResizer.addEventListener('mousedown', (e) => {
            isResizing = true;
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const newWidth = e.clientX - leftSidebar.getBoundingClientRect().left;
            if (newWidth > 150 && newWidth < 500) {
                leftSidebar.style.width = `${newWidth}px`;
            }
        });

        document.addEventListener('mouseup', () => {
            isResizing = false;
            document.body.style.cursor = 'default';
            document.body.style.userSelect = 'auto';
        });
    }

    // 2. Resizer Cột phải (AI Chat Pane)
    const rightSidebar = document.getElementById('pane-chat') || document.querySelector('.w-80');
    const rightResizer = document.getElementById('resizer-right');

    if (rightResizer && rightSidebar) {
        let isResizing = false;

        rightResizer.addEventListener('mousedown', (e) => {
            isResizing = true;
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const newWidth = window.innerWidth - e.clientX;
            if (newWidth > 200 && newWidth < 600) {
                rightSidebar.style.width = `${newWidth}px`;
            }
        });

        document.addEventListener('mouseup', () => {
            isResizing = false;
            document.body.style.cursor = 'default';
            document.body.style.userSelect = 'auto';
        });
    }

    // 3. Resizer Khung Terminal phía dưới
    const terminalPane = document.querySelector('div.h-44, div.h-40');
    const terminalResizer = document.getElementById('resizer-terminal');

    if (terminalResizer && terminalPane) {
        let isResizing = false;

        terminalResizer.addEventListener('mousedown', (e) => {
            isResizing = true;
            document.body.style.cursor = 'row-resize';
            document.body.style.userSelect = 'none';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const newHeight = window.innerHeight - e.clientY;
            if (newHeight > 80 && newHeight < 500) {
                terminalPane.style.height = `${newHeight}px`;
            }
        });

        document.addEventListener('mouseup', () => {
            isResizing = false;
            document.body.style.cursor = 'default';
            document.body.style.userSelect = 'auto';
        });
    }
}