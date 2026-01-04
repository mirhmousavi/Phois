install:
	pip install --upgrade uv
	uv sync --group dev

lint:
	uv run mypy src
	uv run ruff check .
	
format:
	uv run ruff format .

test:
	uv run pytest --capture=no .
