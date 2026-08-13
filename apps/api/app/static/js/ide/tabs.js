export function initTabs() {
    // 1. Chuyển đổi Tab nguồn / Diff trong Editor Pane
    const btnSource = document.getElementById('btn-view-source');
    const btnDiff = document.getElementById('btn-view-diff');

    if (btnSource && btnDiff) {
        btnSource.addEventListener('click', () => {
            btnSource.className = 'px-2 py-0.5 text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 rounded font-mono';
            btnDiff.className = 'px-2 py-0.5 text-[10px] bg-slate-800 text-slate-400 hover:text-slate-200 rounded font-mono';
        });
        btnDiff.addEventListener('click', () => {
            btnDiff.className = 'px-2 py-0.5 text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 rounded font-mono';
            btnSource.className = 'px-2 py-0.5 text-[10px] bg-slate-800 text-slate-400 hover:text-slate-200 rounded font-mono';
        });
    }

    // 2. Tương tác Activity Bar bên trái để ẩn/hiện Sidebar views
    const actButtons = document.querySelectorAll('.act-btn');
    const sidebarViews = document.querySelectorAll('.sidebar-view');
    const explorerSidebar = document.getElementById('explorer-sidebar');

    actButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Highlight icon được chọn trên Activity Bar
            actButtons.forEach(b => b.classList.remove('bg-cyan-500/10', 'text-cyan-400', 'border', 'border-cyan-500/30'));
            actButtons.forEach(b => b.classList.add('hover:bg-slate-800/80', 'hover:text-slate-200'));
            
            btn.classList.add('bg-cyan-500/10', 'text-cyan-400', 'border', 'border-cyan-500/30');
            btn.classList.remove('hover:bg-slate-800/80', 'hover:text-slate-200');

            // Xác định view cần hiển thị tương ứng với nút bấm
            let targetViewId = 'sidebar-view-explorer';
            if (btn.id === 'act-search') targetViewId = 'sidebar-view-search';
            else if (btn.id === 'act-source-control') targetViewId = 'sidebar-view-git';
            else if (btn.id === 'act-doctor' || btn.id === 'act-ai-studio') targetViewId = 'sidebar-view-doctor';

            // Ẩn tất cả các view, chỉ hiện view được chọn
            sidebarViews.forEach(view => {
                if (view.id === targetViewId) {
                    view.classList.remove('hidden');
                } else {
                    view.classList.add('hidden');
                }
            });

            // Đảm bảo khung sidebar hiển thị
            if (explorerSidebar) {
                explorerSidebar.classList.remove('hidden');
            }

            console.log(`[ActivityBar] Switched sidebar view to: ${targetViewId}`);
        });
    });
}