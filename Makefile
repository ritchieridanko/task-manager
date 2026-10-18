start-app:
	docker compose --env-file backend/.env --env-file frontend/.env up -d --build

stop-app:
	docker compose --env-file backend/.env --env-file frontend/.env down -v
