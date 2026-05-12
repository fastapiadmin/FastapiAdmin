#!/bin/bash

# 设置脚本选项，提高健壮性
set -e  # 遇到错误立即退出
set -u  # 遇到未定义变量立即退出
set -o pipefail  # 管道命令失败时整个命令失败

# 设置全局变量
PROJECT_NAME="FastapiAdmin"
WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKER_DIR="${WORK_DIR}/docker"
ENV_FILE="${DOCKER_DIR}/.env"

GIT_REPO="https://gitee.com/fastapiadmin/${PROJECT_NAME}.git"

# 是否有更新前端
UPDATE_FRONTEND=false
# 是否有更新移动端
UPDATE_FASTAPP=false
# 是否有更新官网
UPDATE_FASTDOCS=false
# 是否跳过前端构建
SKIP_FRONTEND=true

# 部署状态跟踪
DEPLOY_STATUS=""

# 日志级别控制
LOG_LEVEL=${LOG_LEVEL:-INFO}

# 颜色定义
readonly COLOR_RESET='\033[0m'
readonly COLOR_RED='\033[0;31m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_YELLOW='\033[0;33m'
readonly COLOR_BLUE='\033[0;34m'
readonly COLOR_CYAN='\033[0;36m'

# 打印带时间戳的日志（带颜色）
log() {
    local message="$1"
    local level=${2:-INFO}
    local color=""

    case $level in
        DEBUG) color="${COLOR_RESET}" ;;
        INFO) color="${COLOR_BLUE}" ;;
        WARN) color="${COLOR_YELLOW}" ;;
        ERROR) color="${COLOR_RED}" ;;
        SUCCESS) color="${COLOR_GREEN}" ;;
        *) color="${COLOR_RESET}" ;;
    esac

    case $LOG_LEVEL in
        DEBUG) ;;
        INFO) [[ $level == "DEBUG" ]] && return ;;
        WARN) [[ $level == "DEBUG" || $level == "INFO" ]] && return ;;
        ERROR) [[ $level != "ERROR" ]] && return ;;
        SUCCESS) [[ $level == "DEBUG" || $level == "INFO" || $level == "WARN" ]] && return ;;
    esac

    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] ${message}${COLOR_RESET}"
}

# 检查并设置脚本执行权限
check_and_setup_permissions() {
    log "==========🔐 检查脚本执行权限...==========" "INFO"

    local script_path="${WORK_DIR}/deploy.sh"
    local docker_compose_file="${DOCKER_DIR}/docker-compose.yaml"

    if [ ! -x "$script_path" ]; then
        log "⚠️  deploy.sh 缺少执行权限，正在自动设置..." "WARN"
        chmod +x "$script_path"
        log "✅ deploy.sh 执行权限已设置" "INFO"
    else
        log "✅ deploy.sh 执行权限正常" "INFO"
    fi

    if [ ! -f "$docker_compose_file" ]; then
        log "❌ docker-compose.yaml 文件不存在: ${docker_compose_file}" "ERROR"
        exit 1
    fi

    log "✅ 权限检查完成" "INFO"
}

# 加载环境变量
load_env() {
    log "==========🔍 加载环境变量...==========" "INFO"

    if [ -f "${ENV_FILE}" ]; then
        log "📁 加载环境变量文件: ${ENV_FILE}" "INFO"
        set -a
        source "${ENV_FILE}"
        set +a
        log "✅ 环境变量加载成功" "INFO"
    else
        log "⚠️  环境变量文件 ${ENV_FILE} 不存在，使用默认值" "WARN"
        if [ -f "${DOCKER_DIR}/.env.example" ]; then
            log "📁 从示例文件创建环境变量文件" "INFO"
            cp "${DOCKER_DIR}/.env.example" "${ENV_FILE}"
            log "✅ 环境变量文件创建成功" "INFO"
            set -a
            source "${ENV_FILE}"
            set +a
        else
            log "❌ 环境变量示例文件 ${DOCKER_DIR}/.env.example 不存在" "ERROR"
            exit 1
        fi
    fi
}

# 检查系统依赖
check_permissions() {
    log "==========🔍 检查系统依赖...==========" "INFO"

    # 创建必要的持久化目录
    for dir in "${DOCKER_DIR}/mysql/data" "${DOCKER_DIR}/redis/data" "${WORK_DIR}/backups" ; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log "📁 创建目录: ${dir}" "INFO"
        fi
    done

    local missing_deps=()
    local optional_deps_missing=()

    for cmd in git docker; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=($cmd)
            log "❌ $cmd 未安装" "ERROR"
        else
            local version=$($cmd --version 2>/dev/null | head -n1 || $cmd -v 2>/dev/null | head -n1)
            log "🎉 $cmd 已安装 - ${version}" "INFO"
        fi
    done

    # 检查 docker compose（v2 带空格）或 docker-compose（v1 带短横线）
    if docker compose version &> /dev/null; then
        log "🎉 docker compose 已安装 - $(docker compose version | head -n1)" "INFO"
    elif docker-compose --version &> /dev/null; then
        log "🎉 docker-compose 已安装 - $(docker-compose --version | head -n1)" "INFO"
    else
        missing_deps+=("docker compose")
        log "❌ docker compose / docker-compose 未安装" "ERROR"
    fi

    if [ -d "frontend/web" ] || [ -d "frontend/app" ] || [ -d "frontend/docs" ]; then
        for cmd in node pnpm; do
            if ! command -v $cmd &> /dev/null; then
                optional_deps_missing+=($cmd)
                log "⚠️  $cmd 未安装（前端构建需要）" "WARN"
            else
                log "🎉 $cmd 已安装 - $($cmd --version 2>/dev/null || $cmd -v)" "INFO"
            fi
        done
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        log "❌ 缺少必需依赖: ${missing_deps[*]}" "ERROR"
        log "❌ 请安装缺失的依赖后重试" "ERROR"
        exit 1
    fi

    log "✅ 所有必需依赖检查通过" "INFO"
}

# 更新代码
update_code() {
    log "==========🔄 更新最新代码...==========" "INFO"
    log "📂 当前工作目录: $(pwd)" "INFO"
    log "🎯 项目路径: ${WORK_DIR}" "INFO"

    if [ "$(pwd)" != "${WORK_DIR}" ]; then
        cd "${WORK_DIR}" || { log "❌ 无法进入项目根目录" "ERROR"; exit 1; }
        log "📂 进入项目根目录" "INFO"
    fi

    if [ -d ".git" ]; then
        local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
        log "📂 当前Git分支: ${current_branch}" "INFO"

        # 记录更新前的 deploy.sh MD5，判断脚本本身是否有变更
        local script_checksum_before=""
        if command -v md5sum &> /dev/null; then
            script_checksum_before=$(md5sum "$0" 2>/dev/null | awk '{print $1}')
        elif command -v md5 &> /dev/null; then
            script_checksum_before=$(md5 -q "$0" 2>/dev/null)
        fi

        git fetch origin || { log "⚠️  获取远程分支失败" "WARN"; }
        git pull || { log "❌ 拉取更新失败" "ERROR"; exit 1; }
        local commit_info=$(git log -1 --oneline 2>/dev/null || echo "无法获取提交信息")
        log "📝 最新提交: ${commit_info}" "INFO"

        # 如果 deploy.sh 自身有更新，重新执行新版本
        if [ -n "${script_checksum_before}" ]; then
            local script_checksum_after=""
            if command -v md5sum &> /dev/null; then
                script_checksum_after=$(md5sum "$0" 2>/dev/null | awk '{print $1}')
            elif command -v md5 &> /dev/null; then
                script_checksum_after=$(md5 -q "$0" 2>/dev/null)
            fi
            if [ -n "${script_checksum_after}" ] && [ "${script_checksum_before}" != "${script_checksum_after}" ]; then
                log "🔄 deploy.sh 已更新，重新执行新版本..." "WARN"
                exec "$0" "$@"
            fi
        fi
    else
        log "📥 初始化Git仓库..." "INFO"
        git init
        git remote add origin "${GIT_REPO}"
        git pull origin master || git pull origin main || { log "❌ 拉取代码失败" "ERROR"; exit 1; }
    fi

    if [ -d "frontend/web" ]; then
        UPDATE_FRONTEND=true
        log "📦 检测到前端工程" "INFO"
    fi
    if [ -d "frontend/app" ]; then
        UPDATE_FASTAPP=true
        log "📦 检测到移动端工程" "INFO"
    fi
    if [ -d "frontend/docs" ]; then
        UPDATE_FASTDOCS=true
        log "📦 检测到官网工程" "INFO"
    fi

    log "✅ 代码更新成功" "INFO"
}

# 打包前端
build_frontend() {
    log "==========🚀 构建前端...==========" "INFO"

    if [ "$SKIP_FRONTEND" = true ]; then
        log "⚠️  跳过前端构建（使用已上传的静态文件）" "WARN"
        return 0
    fi

    if ! command -v node &> /dev/null || ! command -v pnpm &> /dev/null; then
        log "⚠️  Node.js 或 pnpm 未安装，跳过前端构建" "WARN"
        log "💡 提示: 请在本地构建前端，然后将 dist 目录上传到 docker/nginx/ 对应目录" "WARN"
        return 0
    fi

    if [ -d "frontend/web" ] && [ "$UPDATE_FRONTEND" = true ]; then
        log "📦 开始构建前端工程..." "INFO"
        cd frontend/web || { log "❌ 无法进入前端目录" "ERROR"; exit 1; }

        log "📦 安装前端依赖..." "INFO"
        pnpm install --frozen-lockfile || pnpm install || { log "❌ 前端依赖安装失败" "WARN"; cd ..; return 0; }

        log "🔨 打包前端工程..." "INFO"
        pnpm run build || { log "❌ 前端工程打包失败" "WARN"; cd ..; return 0; }
        log "✅ 前端工程打包成功" "INFO"

        mkdir -p "${WORK_DIR}/docker/nginx/web"

        if [ -d "dist" ]; then
            rm -rf "${WORK_DIR}/docker/nginx/web/dist"
            mv -f "dist" "${WORK_DIR}/docker/nginx/web/" || { log "❌ 移动前端打包到docker/nginx/web目录失败" "ERROR"; cd ..; exit 1; }
            log "✅ 前端打包文件已移动到 docker/nginx/web/dist" "INFO"
        fi

        cd .. || { log "❌ 无法返回项目根目录" "ERROR"; exit 1; }
    fi

    if [ -d "frontend/app" ] && [ "$UPDATE_FASTAPP" = true ]; then
        log "📦 开始构建小程序工程..." "INFO"
        cd frontend/app || { log "❌ 无法进入小程序目录" "ERROR"; exit 1; }

        log "📦 安装小程序依赖..." "INFO"
        pnpm install --frozen-lockfile || pnpm install || { log "❌ 小程序依赖安装失败" "WARN"; cd ..; return 0; }

        log "🔨 打包小程序工程..." "INFO"
        pnpm run build:h5 || { log "❌ 小程序工程打包失败" "WARN"; cd ..; return 0; }
        log "✅ 小程序工程打包成功" "INFO"

        mkdir -p "${WORK_DIR}/docker/nginx/app"

        if [ -d "dist" ]; then
            rm -rf "${WORK_DIR}/docker/nginx/app/dist"
            mv -f "dist" "${WORK_DIR}/docker/nginx/app/" || { log "❌ 移动小程序打包到docker/nginx/app目录失败" "ERROR"; cd ..; exit 1; }
            log "✅ 小程序打包文件已移动到 docker/nginx/app/dist" "INFO"
        fi

        cd .. || { log "❌ 无法返回项目根目录" "ERROR"; exit 1; }
    fi

    if [ -d "frontend/docs" ] && [ "$UPDATE_FASTDOCS" = true ]; then
        log "📦 开始构建项目文档..." "INFO"
        cd frontend/docs || { log "❌ 无法进入项目文档目录" "ERROR"; exit 1; }

        log "📦 安装项目文档依赖..." "INFO"
        pnpm install --frozen-lockfile || pnpm install || { log "❌ 项目文档依赖安装失败" "WARN"; cd ..; return 0; }

        log "🔨 打包项目文档..." "INFO"
        pnpm run docs:build || { log "❌ 项目文档打包生成失败" "WARN"; cd ..; return 0; }
        log "✅ 项目文档打包成功" "INFO"

        mkdir -p "${WORK_DIR}/docker/nginx/docs"

        if [ -d "dist" ]; then
            rm -rf "${WORK_DIR}/docker/nginx/docs/dist"
            mv -f "dist" "${WORK_DIR}/docker/nginx/docs/" || { log "❌ 移动项目文档打包到docker/nginx/docs目录失败" "ERROR"; cd ..; exit 1; }
            log "✅ 项目文档打包文件已移动到 docker/nginx/docs/dist" "INFO"
        fi

        cd .. || { log "❌ 无法返回项目根目录" "ERROR"; exit 1; }
    fi
}

# 构建镜像
build_containers() {
    log "==========🔨 构建Docker镜像...==========" "INFO"
    cd "${DOCKER_DIR}" || { log "❌ 无法进入项目 docker 目录" "ERROR"; exit 1; }
    log "📂 进入项目 docker 目录: $(pwd)" "INFO"

    export DOCKER_BUILDKIT=1
    docker compose build --no-cache || { log "❌ 镜像构建失败" "ERROR"; exit 1; }
    log "✅ Docker镜像构建成功" "SUCCESS"
}

# 启动容器
start_containers() {
    log "==========🚀 启动容器...==========" "INFO"
    cd "${DOCKER_DIR}" || { log "❌ 无法进入项目 docker 目录" "ERROR"; exit 1; }

    if docker compose ps --format '{{.Names}}' 2>/dev/null | grep -q .; then
        log "📦 停止旧容器..." "INFO"
        docker compose down || true
    fi

    log "🚀 启动新容器..." "INFO"
    docker compose up -d --force-recreate || { log "❌ 容器启动失败" "ERROR"; exit 1; }

    log "⏳ 等待容器启动完成..." "INFO"
    local max_wait=60
    local wait_count=0

    while [ $wait_count -lt $max_wait ]; do
        if docker compose ps mysql --format '{{.Status}}' 2>/dev/null | grep -q "healthy"; then
            log "✅ MySQL 已就绪" "SUCCESS"
            break
        fi
        sleep 2
        wait_count=$((wait_count + 2))
        echo -n "."
    done
    echo ""

    log "📊 容器状态检查..." "INFO"
    docker compose ps

    log "✅ 项目容器已启动" "SUCCESS"
}

# 停止项目容器
stop_containers() {
    log "==========⏹️ 停止项目容器...==========" "INFO"

    if [ -d "${DOCKER_DIR}" ]; then
        cd "${DOCKER_DIR}" || { log "❌ 无法进入项目 docker 目录" "ERROR"; exit 1; }
        log "📂 进入项目 docker 目录" "INFO"

        docker compose down || { log "⚠️  停止容器时发生错误" "WARN"; }
        log "✅ 项目容器已停止并删除" "INFO"

        cd .. || { log "❌ 无法返回项目根目录" "ERROR"; exit 1; }
        log "📂 返回项目根目录" "INFO"
    fi
}

# 重启容器
restart_containers() {
    log "==========🔄 重启容器...==========" "INFO"
    cd "${DOCKER_DIR}" || { log "❌ 无法进入项目 docker 目录" "ERROR"; exit 1; }
    docker compose restart || { log "❌ 容器重启失败" "ERROR"; exit 1; }
    log "✅ 容器重启成功" "SUCCESS"
    docker compose ps
}

# 备份数据库
backup_database() {
    log "==========💾 备份数据库...==========" "INFO"
    local backup_dir="${WORK_DIR}/backups"
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    mkdir -p "${backup_dir}"

    if docker compose ps mysql --format '{{.Status}}' 2>/dev/null | grep -q "healthy"; then
        local db_user="${MYSQL_USER:-fastapiadmin}"
        local db_password="${MYSQL_PASSWORD}"
        local db_name="${MYSQL_DATABASE:-fastapiadmin}"
        local backup_file="${backup_dir}/${db_name}_${timestamp}.sql.gz"

        log "📦 备份数据库 ${db_name} 到 ${backup_file}" "INFO"
        docker compose exec -T mysql mysqldump \
            -u"${db_user}" -p"${db_password}" \
            --single-transaction \
            --routines \
            --triggers \
            --events \
            "${db_name}" | gzip > "${backup_file}"
        log "✅ 数据库备份完成: ${backup_file}" "SUCCESS"

        # 保留最近 7 天备份，清理旧的
        find "${backup_dir}" -name "*.sql.gz" -type f -mtime +7 -delete
        log "🗑️ 已清理 7 天前的旧备份" "INFO"
    else
        log "⚠️  MySQL 未运行，跳过数据库备份" "WARN"
    fi

    # 备份 .env 文件
    if [ -f "${ENV_FILE}" ]; then
        cp "${ENV_FILE}" "${backup_dir}/.env.backup.${timestamp}"
        log "✅ 环境变量配置已备份" "INFO"
    fi
}

# 清理旧镜像
clear_old_images() {
    log "==========🗑️ 清理旧镜像...==========" "INFO"

    # 清理悬空镜像（无标签镜像）
    local dangling_count=$(docker images -f "dangling=true" -q | wc -l)
    if [ "${dangling_count}" -gt 0 ]; then
        docker image prune -f >/dev/null 2>&1 || true
        log "✅ 已清理 ${dangling_count} 个悬空镜像" "INFO"
    fi

    # 清理 30 天前的旧镜像（保留最近 3 个版本）
    local before_count=$(docker images | grep -E "backend" | wc -l)
    if [ "${before_count}" -gt 3 ]; then
        docker images --format '{{.Repository}}:{{.Tag}}' | grep -E "backend" | \
            tail -n +4 | xargs -r docker rmi >/dev/null 2>&1 || true
        log "✅ 已清理旧版本镜像，保留最近 3 个版本" "SUCCESS"
    else
        log "ℹ️  项目镜像数量正常（${before_count} 个），无需清理" "INFO"
    fi
}

# 显示日志
show_containers_logs() {
    log "==========📋 查看所有容器日志... ==========" "INFO"
    cd "${DOCKER_DIR}" || { log "❌ 无法进入项目 docker 目录" "ERROR"; exit 1; }

    log "📊 当前容器状态：" "INFO"
    docker compose ps --format "table {{.Service}}\t{{.Name}}\t{{.Status}}\t{{.Ports}}"

    log "📋 服务日志（最近 50 行，实时跟踪请用 docker compose logs -f [服务名]）：" "INFO"
    echo "----------------------------------------"
    docker compose logs --tail=50 --no-log-prefix 2>/dev/null || docker compose logs --tail=50
    echo "----------------------------------------"
}

# 验证部署
verify_deployment() {
    log "==========🔍 验证部署结果...==========" "INFO"

    local all_healthy=true

    log "📊 检查容器运行状态..." "INFO"
    for service in mysql redis backend nginx; do
        local status=$(docker compose ps "$service" --format '{{.Status}}' 2>/dev/null || echo "not found")
        if echo "$status" | grep -q "Up\|healthy"; then
            log "✅ ${service}: ${status}" "SUCCESS"
        else
            log "❌ ${service}: ${status}" "ERROR"
            all_healthy=false
        fi
    done

    log "📊 检查端口监听..." "INFO"
    local backend_port="${BACKEND_PORT:-8001}"
    if command -v nc &> /dev/null; then
        if nc -z localhost ${backend_port} 2>/dev/null; then
            log "✅ 后端服务端口 ${backend_port} 已监听" "SUCCESS"
        else
            log "⚠️  后端服务端口 ${backend_port} 未监听" "WARN"
        fi
    fi

    local http_port="${HTTP_PORT:-80}"
    if nc -z localhost ${http_port} 2>/dev/null; then
        log "✅ Nginx服务端口 ${http_port} 已监听" "SUCCESS"
    else
        log "⚠️  Nginx服务端口 ${http_port} 未监听" "WARN"
    fi

    if [ "$all_healthy" = true ]; then
        log "✅ 所有服务运行正常！" "SUCCESS"
        return 0
    else
        log "⚠️  部分服务可能存在问题，请检查日志" "WARN"
        return 1
    fi
}

# 信号处理
handle_interrupt() {
    log "" "INFO"
    log "==========⚠️ 收到中断信号，正在停止部署...==========" "WARN"
    if [ -d "${DOCKER_DIR}" ]; then
        cd "${DOCKER_DIR}"
        docker compose down >/dev/null 2>&1 || true
    fi
    exit 130
}

# 主函数
main() {
    log "==========🚀 开始部署流程==========" "INFO"
    log "📂 脚本所在目录: $(pwd)" "INFO"
    log "📅 部署时间: $(date '+%Y-%m-%d %H:%M:%S')" "INFO"

    DEPLOY_STATUS="检查脚本权限"
    log "==========🔐 开始${DEPLOY_STATUS}...==========" "INFO"
    check_and_setup_permissions
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="加载环境变量"
    log "==========🔍 开始${DEPLOY_STATUS}...==========" "INFO"
    load_env
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="检查系统依赖"
    log "==========🔍 开始${DEPLOY_STATUS}...==========" "INFO"
    check_permissions
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="备份数据库"
    log "==========💾 开始${DEPLOY_STATUS}...==========" "INFO"
    backup_database
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="停止现有容器"
    log "==========⏹️ 开始${DEPLOY_STATUS}...==========" "INFO"
    stop_containers
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="更新代码"
    log "==========🔄 开始${DEPLOY_STATUS}...==========" "INFO"
    update_code
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    # DEPLOY_STATUS="构建前端"
    # log "==========🚀 开始${DEPLOY_STATUS}...==========" "INFO"
    # build_frontend
    # log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="构建镜像"
    log "==========🔨 开始${DEPLOY_STATUS}...==========" "INFO"
    build_containers
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="启动容器"
    log "==========🚀 开始${DEPLOY_STATUS}...==========" "INFO"
    start_containers
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="验证部署"
    log "==========🔍 开始${DEPLOY_STATUS}...==========" "INFO"
    verify_deployment || log "⚠️  部署验证发现问题，请检查日志" "WARN"
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    DEPLOY_STATUS="显示日志"
    log "==========📋 开始${DEPLOY_STATUS}...==========" "INFO"
    show_containers_logs
    log "✅ ${DEPLOY_STATUS}完成" "INFO"

    log "" "INFO"
    log "🎉🎉🎉 部署完成！🎉🎉🎉" "SUCCESS"
    log "" "INFO"
    log "📌 访问信息：" "INFO"
    log "   🌐 官网: http://域名(或ip:${HTTP_PORT:-80})" "INFO"
    log "   🌐 前端: http://域名(或ip:${HTTP_PORT:-80})/web" "INFO"
    log "   🌐 小程序: http://域名(或ip:${HTTP_PORT:-80})/app" "INFO"
    log "   🔌 后端API: http://域名(或ip):${BACKEND_PORT:-8001}/api/v1/docs" "INFO"
    log "   📝 登录信息: 账号 admin，密码 123456" "INFO"
    log "" "INFO"
    log "💡 常用命令：" "INFO"
    log "   🚀 启动服务: ./deploy.sh start" "INFO"
    log "   ⏹️ 停止服务: ./deploy.sh stop" "INFO"
    log "   🔄 重启服务: ./deploy.sh restart" "INFO"
    log "   📋 查看日志: ./deploy.sh logs" "INFO"
    log "   🔍 验证部署: ./deploy.sh verify" "INFO"
    log "   🧹 清理镜像: ./deploy.sh clean" "INFO"
    log "   ℹ️ 显示帮助: ./deploy.sh help|-h" "INFO"
    log "" "INFO"
    log "🔧 前端构建选项：" "INFO"
    log "   默认: 跳过前端构建，使用已上传的静态文件" "INFO"
    log "   启用: ./deploy.sh --build-frontend" "INFO"
    log "" "INFO"
}

# 设置信号处理
trap handle_interrupt INT TERM

# 解析命令行参数
if [ $# -eq 0 ]; then
    main "$@"
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-frontend)
            SKIP_FRONTEND=true
            log "⚠️  跳过前端构建" "WARN"
            shift
            ;;
        --build-frontend)
            SKIP_FRONTEND=false
            log "🔨 启用前端构建" "INFO"
            shift
            ;;
        start)
            load_env
            start_containers
            exit 0
            ;;
        stop)
            load_env
            stop_containers
            exit 0
            ;;
        restart)
            load_env
            restart_containers
            exit 0
            ;;
        logs)
            load_env
            show_containers_logs
            exit 0
            ;;
        verify)
            load_env
            verify_deployment
            exit 0
            ;;
        clean)
            clear_old_images
            exit 0
            ;;
        help|-h|--help)
            echo "使用说明："
            echo "  $0 [选项]"
            echo ""
            echo "选项："
            echo "  start          启动所有容器"
            echo "  stop           停止所有容器"
            echo "  restart        重启所有容器"
            echo "  logs           查看所有容器日志"
            echo "  verify         验证部署状态"
            echo "  clean          清理旧镜像"
            echo "  --skip-frontend  跳过前端构建（默认）"
            echo "  --build-frontend  启用前端构建（在服务器上构建）"
            echo "  help|-h        显示此帮助信息"
            echo ""
            echo "默认执行完整部署流程："
            echo "  1. 检查脚本权限"
            echo "  2. 加载环境变量"
            echo "  3. 检查系统依赖"
            echo "  4. 备份数据库"
            echo "  5. 停止现有容器"
            echo "  6. 更新代码"
            echo "  7. 构建前端（默认跳过，使用已上传的静态文件）"
            echo "  8. 构建镜像"
            echo "  9. 启动容器"
            echo "  10. 验证部署"
            echo "  11. 显示日志"
            echo ""
            echo "日志查看命令："
            echo "  查看实时日志：docker compose logs -f [服务名]"
            echo "  服务名：backend, nginx, mysql, redis"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            echo "使用 $0 help 查看帮助信息"
            exit 1
            ;;
    esac
done

main "$@"