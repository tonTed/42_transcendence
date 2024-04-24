up:
	docker compose up -d

down:
	docker compose down

exec-frontend:
	docker exec -it django-frontend /bin/sh

exec-gateway:
	docker exec -it api-gateway /bin/sh

exec-database:
	docker exec -it database /bin/sh

logs-frontend:
	@docker logs --tail 50 --follow django-frontend

logs-gateway:
	@docker logs --tail 50 --follow api-gateway

logs-database:
	@docker logs --tail 50 --follow database

rm-images:
	@docker compose down --rmi all
	@echo "All images removed."

setup-venvs:
	./scripts-tools/setup_venvs.sh


# help: List all available commands
help:
	@echo "Available commands:"
	@echo ""
	@echo "  up              : Start the containers"
	@echo "  down            : Stop the containers"
	@echo "  exec-frontend   : Access the frontend container"
	@echo "  exec-gateway	 : Access the api-gateway container"
	@echo "  exec-database   : Access the database container"
	@echo "  logs-frontend   : Show the logs of the frontend container"
	@echo "  logs-gateway    : Show the logs of the api-gateway container"
	@echo "  logs-database   : Show the logs of the database container"
	@echo "  rm-images       : Remove all images"
	@echo "  setup-venvs     : Setup the virtual environments (macOS & linux only with python3.12)"
	@echo "  help            : Show this help message"
	@echo ""