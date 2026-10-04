up:
	docker compose up --build -d
down:
	docker compose down
test:
	python -m pytest -q
lint:
	ruff check .
