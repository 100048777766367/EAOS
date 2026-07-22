.PHONY: test lint validate graph metrics run-web clean
test:
pytest tests/ -v

lint:
ruff check . && mypy services/ libs/ tests/

validate:
python -m services.dashboard.app validate

graph:
python -m services.dashboard.app graph

metrics:
python -m services.dashboard.app metrics

run-web:
python -m uvicorn services.dashboard.web:app --reload --host 0.0.0.0 --port 8000
