### SERVER
# ¯¯¯¯¯¯¯¯¯¯¯

server.build: ## Build server
	docker-compose build application

server.start: ## Start server
	docker-compose up --build application

server.sh: ## Connect to server to lauch commands
	docker-compose exec application sh

server.daemon: ## Start daemon server in its docker container
	docker-compose up --build -d application

server.stop: ## Stop server
	docker-compose stop

server.remove: ## Stop server and remove volumes
	docker-compose down -v

server.restart: ## Restart server
	docker-compose down -v && docker-compose up --build -d application

server.logs: ## Display server logs
	docker-compose logs -f -t --tail=100