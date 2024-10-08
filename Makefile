up: prod

prod:
	docker compose -f docker-compose_prod.yml up -d --build

dev:
	docker compose -f docker-compose_dev.yml up -d --build

down:
	docker compose down

exec-frontend:
	docker exec -it django-frontend /bin/sh

exec-game:
	docker exec -it api-game /bin/sh

exec-gateway:
	docker exec -it api-gateway /bin/sh

exec-user-service:
	docker exec -it api-users /bin/sh

exec-database:
	docker exec -it database /bin/sh

exec-webserver:
	docker exec -it webserver /bin/sh

logs-frontend:
	@docker logs --tail 50 --follow django-frontend

logs-game:
	@docker logs --tail 50 --follow api-game

logs-gateway:
	@docker logs --tail 50 --follow api-gateway

logs-user-service:
	@docker logs --tail 50 --follow api-users

logs-database:
	@docker logs --tail 50 --follow database

logs-webserver:
	@docker logs --tail 50 --follow webserver

rm-images: down
	@docker rmi "django-frontend" "drf-api-gateway" "drf-api-users"
	@echo "All images removed."

setup-venvs:
	./scripts-tools/setup_venvs.sh

fclean: down
	rm -rf ./postgres/postgres_data/*
	docker system prune -a -f
	docker volume prune -a -f

# help: List all available commands
help:
	@echo "Available commands:"
	@echo ""
	@echo "  up              : Start the containers"
	@echo "  down            : Stop the containers"
	@echo "  exec-frontend   : Access the frontend container"
	@echo "  exec-game	     : Access the api-game container"
	@echo "  exec-gateway	 : Access the api-gateway container"
	@echo "  exec-database   : Access the database container"
	@echo "  logs-frontend   : Show the logs of the frontend container"
	@echo "  logs-game       : Show the logs of the api-game container"
	@echo "  logs-gateway    : Show the logs of the api-gateway container"
	@echo "  logs-database   : Show the logs of the database container"
	@echo "  rm-images       : Remove all images"
	@echo "  setup-venvs     : Setup the virtual environments (macOS & linux only with python3.12)"
	@echo "  help            : Show this help message"
	@echo ""