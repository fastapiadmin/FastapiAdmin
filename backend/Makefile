install:
	pip install -r requirements.txt

run:
	python main.py run --env=dev

start:
	@echo "Starting high-school-college-backend ..."
	@python main.py run --env=dev > logs/agent.log 2>&1 & echo $$! > /tmp/high-school-college-backend.pid
	@sleep 1
	@echo "high-school-college-backend PID: $$(cat /tmp/high-school-college-backend.pid)"

stop:
	@if [ -f /tmp/high-school-college-backend.pid ]; then \
		PID=$$(cat /tmp/high-school-college-backend.pid); \
		if ps -p $$PID > /dev/null 2>&1; then \
			kill $$PID 2>/dev/null; \
			sleep 0.5; \
			if ps -p $$PID > /dev/null 2>&1; then \
				kill -9 $$PID 2>/dev/null; \
			fi; \
			echo "high-school-college-backend stopped (PID: $$PID)."; \
		else \
			echo "high-school-college-backend not running (stale PID file)."; \
		fi; \
		rm -f /tmp/high-school-college-backend.pid; \
	else \
		echo "No PID file found."; \
	fi

restart: stop start

lint:
	ruff check app/ tests/
	ruff check --fix app/ tests/

format:
	ruff format app/ tests/