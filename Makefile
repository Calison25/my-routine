.PHONY: up down build logs logs-backend logs-frontend test test-backend test-frontend install setup clean db-migrate db-seed

# ============================================================
# My Routine - Makefile
# ============================================================

SHELL := /bin/bash
NVM_USE := export NVM_DIR="$$HOME/.nvm" && [ -s "$$NVM_DIR/nvm.sh" ] && . "$$NVM_DIR/nvm.sh" && nvm use 20 &&

# --- Setup ---

setup: ## Primeira configuração do projeto (cria .env, instala deps)
	@test -f backend/.env || cp backend/.env.example backend/.env && echo "✓ backend/.env criado"
	@test -f frontend/.env || cp frontend/.env.example frontend/.env && echo "✓ frontend/.env criado"
	@$(MAKE) install

install: ## Instala dependências do frontend
	$(NVM_USE) cd frontend && npm install

# --- Dev (tudo junto) ---

up: ## Sobe backend (Docker) + frontend (Vite) juntos
	@echo "Subindo banco + backend via Docker..."
	docker compose up -d --build
	@echo "Aguardando backend ficar saudável..."
	@until curl -sf http://localhost:8001/health > /dev/null 2>&1; do sleep 1; done
	@echo "✓ Backend rodando em http://localhost:8001"
	@echo "Subindo frontend..."
	$(NVM_USE) cd frontend && npm run dev

down: ## Para tudo (Docker)
	docker compose down

build: ## Build de produção do frontend
	$(NVM_USE) cd frontend && npm run build

# --- Logs ---

logs: ## Logs de todos os containers
	docker compose logs -f

logs-backend: ## Logs só do backend
	docker compose logs -f backend

logs-db: ## Logs só do banco
	docker compose logs -f db

# --- Testes ---

test: test-backend test-frontend ## Roda todos os testes

test-backend: ## Testes do backend
	docker compose run --rm backend pytest -v

test-frontend: ## Testes do frontend
	$(NVM_USE) cd frontend && npx vitest run

# --- Database ---

db-migrate: ## Roda migrations no banco
	docker compose run --rm backend alembic upgrade head

db-seed: ## Roda seeds no banco
	docker compose exec db psql -U postgres -d my_routine -f /seeds/seed_categories.sql
	docker compose exec db psql -U postgres -d my_routine -f /seeds/seed_muscle_groups.sql

# --- Limpeza ---

clean: ## Remove containers, volumes e node_modules
	docker compose down -v
	rm -rf frontend/node_modules
	rm -rf backend/.venv

# --- Help ---

help: ## Mostra este help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
