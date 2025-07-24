run:
	uv run app.py

test:
	uv run -m pytest -vv

lint:
	uv run pre-commit run --all-files