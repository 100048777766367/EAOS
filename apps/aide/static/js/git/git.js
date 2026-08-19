export function mountGit(node) {
  const state = {
    owner: 'AIDE client',
    branch: 'observed-from-workspace',
    status: 'read-only',
    staged: [],
    unstaged: [],
    diff: 'Diff preview is UI-only until supplied by Gateway/tooling contract.',
    commitMetadata: { author: null, message: null, ready: false },
    destructiveOperations: false,
  };
  node.textContent = `Git ${state.status}: ${state.branch} · staged ${state.staged.length} · unstaged ${state.unstaged.length}`;
  return state;
}
