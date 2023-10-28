dev:
	docker compose -f docker-compose.dev.yml up --build
	docker compose -f docker-compose.dev.yml down
lint:
	docker build -t chack-check-events-lint -f docker/Dockerfile.lint .
	docker run --rm chack-check-events-lint

