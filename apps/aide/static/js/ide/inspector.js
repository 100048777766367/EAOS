export function mountInspector(node, contracts) {
  const items = contracts.map((item) => `<li>${item.name}: ${item.owner}</li>`);
  node.insertAdjacentHTML('beforeend', `<h3>Gateway Contracts</h3><ul>${items.join('')}</ul>`);
  return { selectedResource: null, contracts: contracts.length };
}
