up:
	docker compose up -d

down:
	docker compose down

exec-frontend:
	docker exec -it django-frontend /bin/sh

exec-database:
	docker exec -it database /bin/sh

logs-frontend:
	@docker logs --tail 50 --follow django-frontend

logs-database:
	@docker logs --tail 50 --follow database

# Remove images
rm-images:
	@docker compose down --rmi all
	@echo "All images removed."

# help: List all available commands
help:
	@echo "Available commands:"
	@echo ""
	@echo "  up              : Start the containers"
	@echo "  down            : Stop the containers"
	@echo "  exec-frontend   : Access the frontend container"
	@echo "  exec-database   : Access the database container"
	@echo "  logs-frontend   : Show the logs of the frontend container"
	@echo "  logs-database   : Show the logs of the database container"
	@echo "  rm-images       : Remove all images"
	@echo "  help            : Show this help message"
	@echo ""