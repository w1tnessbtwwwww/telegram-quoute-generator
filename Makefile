dev:
	poetry run python main.py

deploy:
	docker-compose -f docker/docker-compose.yml --project-directory . up --build -d

deploy-debug:
        docker-compose -f docker/docker-compose.yml --project-directory . up --build
