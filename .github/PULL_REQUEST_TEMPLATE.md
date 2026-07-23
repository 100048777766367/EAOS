## EAOS Pull Request Checklist
- [ ] Hexagonal domain isolation verified (Zero framework imports)
- [ ] Line length under 88 characters (uv run task lint)
- [ ] All integration tests passing (uv run task test)
- [ ] AST Constitution audit passing (uv run task validate)