dev:
	poetry run python main.py

deploy:
	docker-compose -f docker/docker-compose.yml --project-directory . up --build -d

deploydebug:
	docker-compose -f docker/docker-compose.yml --project-directory . up --build
