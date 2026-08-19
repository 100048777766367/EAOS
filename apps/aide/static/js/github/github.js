export function githubContract(state) {
  return { owner: 'gateway integration', repositoryUrl: state.github_url || 'https://github.com' };
}
