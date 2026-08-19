export function mountGit(node) {
  node.textContent = 'Git aware: status, branch, commits, diff, staged and unstaged review';
  return { destructiveOperations: false, owner: 'AIDE client' };
}
