SHELL := /bin/sh

.DEFAULT_GOAL := help

RUNTIME_DIR := $(CURDIR)/.runtime
LOG_DIR := $(RUNTIME_DIR)/logs

BACKEND_DIR := $(CURDIR)/backend
FRONTEND_DIR := $(CURDIR)/frontend
MINIAPP_DIR := $(CURDIR)/miniapp

BACKEND_PID := $(RUNTIME_DIR)/backend.pid
FRONTEND_PID := $(RUNTIME_DIR)/frontend.pid
MINIAPP_PID := $(RUNTIME_DIR)/miniapp.pid

BACKEND_LOG := $(LOG_DIR)/backend.log
FRONTEND_LOG := $(LOG_DIR)/frontend.log
MINIAPP_LOG := $(LOG_DIR)/miniapp.log

BACKEND_PYTHON ?= $(BACKEND_DIR)/.venv/bin/python
BACKEND_CMD ?= $(BACKEND_PYTHON) main.py run --env=dev
FRONTEND_CMD ?= pnpm run dev
MINIAPP_CMD ?= npm run dev:h5

.PHONY: help start stop restart status logs \
	backend-start backend-stop backend-restart backend-status backend-logs \
	frontend-start frontend-stop frontend-restart frontend-status frontend-logs \
	miniapp-start miniapp-stop miniapp-restart miniapp-status miniapp-logs

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "All services:"
	@echo "  start              Start backend, frontend and miniapp"
	@echo "  stop               Stop backend, frontend and miniapp"
	@echo "  restart            Restart all three services"
	@echo "  status             Show status of all three services"
	@echo "  logs               Follow logs of all three services"
	@echo ""
	@echo "Single service:"
	@echo "  backend-{start|stop|restart|status|logs}"
	@echo "  frontend-{start|stop|restart|status|logs}"
	@echo "  miniapp-{start|stop|restart|status|logs}"

start: backend-start frontend-start miniapp-start
	@echo "All services started."

stop: miniapp-stop frontend-stop backend-stop
	@echo "All services stopped."

restart: stop start

status: backend-status frontend-status miniapp-status

logs:
	@mkdir -p "$(LOG_DIR)"
	@touch "$(BACKEND_LOG)" "$(FRONTEND_LOG)" "$(MINIAPP_LOG)"
	@tail -f "$(BACKEND_LOG)" "$(FRONTEND_LOG)" "$(MINIAPP_LOG)"

backend-start:
	@mkdir -p "$(LOG_DIR)"
	@if [ ! -x "$(BACKEND_PYTHON)" ]; then \
		echo "backend: Python not found: $(BACKEND_PYTHON)"; exit 1; \
	fi
	@if [ -f "$(BACKEND_PID)" ] && kill -0 "$$(cat "$(BACKEND_PID)")" 2>/dev/null; then \
		echo "backend: already running (PID $$(cat "$(BACKEND_PID)"))"; \
	else \
		rm -f "$(BACKEND_PID)"; \
		cd "$(BACKEND_DIR)" && nohup $(BACKEND_CMD) > "$(BACKEND_LOG)" 2>&1 & echo $$! > "$(BACKEND_PID)"; \
		sleep 1; \
		if kill -0 "$$(cat "$(BACKEND_PID)")" 2>/dev/null; then \
			echo "backend: started (PID $$(cat "$(BACKEND_PID)"), http://localhost:18001)"; \
		else \
			echo "backend: failed to start; see $(BACKEND_LOG)"; rm -f "$(BACKEND_PID)"; exit 1; \
		fi; \
	fi

frontend-start:
	@mkdir -p "$(LOG_DIR)"
	@if [ ! -f "$(FRONTEND_DIR)/package.json" ]; then \
		echo "frontend: package.json not found"; exit 1; \
	fi
	@if [ -f "$(FRONTEND_PID)" ] && kill -0 "$$(cat "$(FRONTEND_PID)")" 2>/dev/null; then \
		echo "frontend: already running (PID $$(cat "$(FRONTEND_PID)"))"; \
	else \
		rm -f "$(FRONTEND_PID)"; \
		cd "$(FRONTEND_DIR)" && nohup $(FRONTEND_CMD) > "$(FRONTEND_LOG)" 2>&1 & echo $$! > "$(FRONTEND_PID)"; \
		sleep 1; \
		if kill -0 "$$(cat "$(FRONTEND_PID)")" 2>/dev/null; then \
			echo "frontend: started (PID $$(cat "$(FRONTEND_PID)"), http://localhost:15180/web)"; \
		else \
			echo "frontend: failed to start; see $(FRONTEND_LOG)"; rm -f "$(FRONTEND_PID)"; exit 1; \
		fi; \
	fi

miniapp-start:
	@mkdir -p "$(LOG_DIR)"
	@if [ ! -f "$(MINIAPP_DIR)/package.json" ]; then \
		echo "miniapp: package.json not found (the miniapp project may still be generating)"; exit 1; \
	fi
	@if [ -f "$(MINIAPP_PID)" ] && kill -0 "$$(cat "$(MINIAPP_PID)")" 2>/dev/null; then \
		echo "miniapp: already running (PID $$(cat "$(MINIAPP_PID)"))"; \
	else \
		rm -f "$(MINIAPP_PID)"; \
		cd "$(MINIAPP_DIR)" && nohup $(MINIAPP_CMD) > "$(MINIAPP_LOG)" 2>&1 & echo $$! > "$(MINIAPP_PID)"; \
		sleep 1; \
		if kill -0 "$$(cat "$(MINIAPP_PID)")" 2>/dev/null; then \
			echo "miniapp: started (PID $$(cat "$(MINIAPP_PID)"))"; \
		else \
			echo "miniapp: failed to start; see $(MINIAPP_LOG)"; rm -f "$(MINIAPP_PID)"; exit 1; \
		fi; \
	fi

backend-stop:
	@$(MAKE) --no-print-directory _stop-service NAME=backend PID_FILE="$(BACKEND_PID)"

frontend-stop:
	@$(MAKE) --no-print-directory _stop-service NAME=frontend PID_FILE="$(FRONTEND_PID)"

miniapp-stop:
	@$(MAKE) --no-print-directory _stop-service NAME=miniapp PID_FILE="$(MINIAPP_PID)"

.PHONY: _stop-service
_stop-service:
	@if [ ! -f "$(PID_FILE)" ]; then \
		echo "$(NAME): not running (no PID file)"; \
	else \
		pid=$$(cat "$(PID_FILE)"); \
		if kill -0 "$$pid" 2>/dev/null; then \
			pkill -TERM -P "$$pid" 2>/dev/null || true; \
			kill "$$pid" 2>/dev/null || true; \
			sleep 1; \
			pkill -KILL -P "$$pid" 2>/dev/null || true; \
			kill -KILL "$$pid" 2>/dev/null || true; \
			echo "$(NAME): stopped (PID $$pid)"; \
		else \
			echo "$(NAME): removed stale PID file ($$pid)"; \
		fi; \
		rm -f "$(PID_FILE)"; \
	fi

backend-restart: backend-stop backend-start
frontend-restart: frontend-stop frontend-start
miniapp-restart: miniapp-stop miniapp-start

backend-status:
	@$(MAKE) --no-print-directory _status-service NAME=backend PID_FILE="$(BACKEND_PID)"

frontend-status:
	@$(MAKE) --no-print-directory _status-service NAME=frontend PID_FILE="$(FRONTEND_PID)"

miniapp-status:
	@$(MAKE) --no-print-directory _status-service NAME=miniapp PID_FILE="$(MINIAPP_PID)"

.PHONY: _status-service
_status-service:
	@if [ -f "$(PID_FILE)" ] && kill -0 "$$(cat "$(PID_FILE)")" 2>/dev/null; then \
		echo "$(NAME): running (PID $$(cat "$(PID_FILE)"))"; \
	else \
		echo "$(NAME): stopped"; \
	fi

backend-logs:
	@mkdir -p "$(LOG_DIR)" && touch "$(BACKEND_LOG)" && tail -f "$(BACKEND_LOG)"

frontend-logs:
	@mkdir -p "$(LOG_DIR)" && touch "$(FRONTEND_LOG)" && tail -f "$(FRONTEND_LOG)"

miniapp-logs:
	@mkdir -p "$(LOG_DIR)" && touch "$(MINIAPP_LOG)" && tail -f "$(MINIAPP_LOG)"
