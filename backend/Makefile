SERVER_PORT = 18001

# 安装依赖
install:
	pip install -r requirements.txt

# 启动开发服务器
run:
	python main.py run --env=dev

start:
	@echo "Starting high-school-college-backend ..."
	@python main.py run --env=dev > logs/agent.log 2>&1 & echo $$! > /tmp/high-school-college-backend.pid
	@sleep 1
	@echo "high-school-college-backend PID: $$(cat /tmp/high-school-college-backend.pid)"

stop:
	@echo "Stopping high-school-college-backend on port $(SERVER_PORT)..."
	@PID=$$(cat /tmp/high-school-college-backend.pid 2>/dev/null); \
	if [ -n "$$PID" ]; then \
		if ps -p $$PID > /dev/null 2>&1; then \
			echo "Killing process from PID file: $$PID"; \
			kill $$PID 2>/dev/null; \
			sleep 0.5; \
			ps -p $$PID > /dev/null 2>&1 && kill -9 $$PID 2>/dev/null; \
			echo "Process $$PID stopped."; \
		else \
			echo "PID $$PID not running (stale PID file)."; \
		fi; \
		rm -f /tmp/high-school-college-backend.pid; \
	else \
		echo "No PID file found."; \
	fi
	@PORT_PID=$$(lsof -ti :$(SERVER_PORT) 2>/dev/null); \
	if [ -n "$$PORT_PID" ]; then \
		echo "Killing process on port $(SERVER_PORT): $$PORT_PID"; \
		kill -9 $$PORT_PID 2>/dev/null; \
		echo "Port $(SERVER_PORT) freed."; \
	else \
		echo "No process on port $(SERVER_PORT)."; \
	fi

restart: stop start

lint:
	ruff check app/ tests/
	ruff check --fix app/ tests/

# 代码格式化
format:
	ruff format app/ tests/

# 生成数据库迁移文件（模型变更后执行）
revision:
	python main.py revision --env=dev

# 应用数据库迁移
migrate:
	python main.py upgrade --env=dev
