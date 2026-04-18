.PHONY: install run start stop restart 

install:
	npm install

run:
	npm run dev

start:
	@echo "Starting high-school-college-frontend ..."
	@nohup npm run dev > logs/agent.log 2>&1 & echo $$! > /tmp/high-school-college-frontend.pid
	@sleep 2
	@echo "high-school-college-frontend started (PID: $$(cat /tmp/high-school-college-frontend.pid))"

stop:
	@if [ -f /tmp/high-school-college-frontend.pid ]; then \
		PID=$$(cat /tmp/high-school-college-frontend.pid); \
		if ps -p $$PID > /dev/null 2>&1; then \
			kill $$PID 2>/dev/null; \
			sleep 0.5; \
			if ps -p $$PID > /dev/null 2>&1; then \
				kill -9 $$PID 2>/dev/null; \
			fi; \
			echo "high-school-college-frontend stopped (PID: $$PID)."; \
		else \
			echo "high-school-college-frontend not running (stale PID file)."; \
		fi; \
		rm -f /tmp/high-school-college-frontend.pid; \
	else \
		echo "No PID file found."; \
	fi

restart: stop start
