dev:
	poetry run python main.py

deploy:
	docker-compose -f docker/docker-compose.yml up --build -d