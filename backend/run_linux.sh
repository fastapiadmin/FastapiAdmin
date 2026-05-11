#!/bin/bash

set -e

# 固定脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ========== 彩色输出定义 ==========
if [[ -t 1 ]]; then
  tty_red="\033[0;31m"
  tty_green="\033[0;32m"
  tty_yellow="\033[0;33m"
  tty_blue="\033[0;34m"
  tty_cyan="\033[0;36m"
  tty_purple="\033[0;35m"
  tty_bold="\033[1m"
  tty_reset="\033[0m"
else
  tty_red="" tty_green="" tty_yellow="" tty_blue="" tty_cyan="" tty_purple="" tty_bold="" tty_reset=""
fi

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[38;5;226m[!]'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
LIGHT_GRAY='\033[0;37m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
RESET='\033[0m'

# ========== 彩色输出函数 ==========
function info() {
  echo -e "${tty_green}✅ $1${tty_reset}"
}

function warn() {
  echo -e "${tty_yellow}⚠️  $1${tty_reset}"
}

function error() {
  echo -e "${tty_red}❌ $1${tty_reset}"
}

function pause() {
  read -n1 -r -p "按任意键继续..." key
}

# 判断执行是否成功
JudgeSuccess() {
  if [ $? -ne 0 ]; then
    error "步骤失败: $1"
    exit 1
  else
    info "步骤成功: $1"
  fi
}

# 分割线输出函数
print_separator() {
  printf "${LIGHT_GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}\n"
}

show_banner() {
  echo ""
  echo -e "╭──────────────────────────────────────────────╮"
  echo -e "│         \033[1;34m👋 欢迎使用 FastAPI 初始化脚本\033[0m       │"
  echo -e "╰──────────────────────────────────────────────╯"
  echo "版本: 3.0.0"
  echo "作者：coderxslee"
  echo ""
}

# ========== 从 .env.dev 文件中读取数据库配置 ==========
function load_db_config() {
  local env_file="$SCRIPT_DIR/env/.env.dev"
  
  if [ ! -f "$env_file" ]; then
    error "未找到 $env_file 文件"
    return 1
  fi
  
  # 读取数据库配置（忽略注释和空行）
  # 使用 sed 去掉注释部分，然后提取值
  DATABASE_HOST=$(grep "^DATABASE_HOST" "$env_file" | cut -d'=' -f2 | sed 's/#.*//' | xargs)
  DATABASE_PORT=$(grep "^DATABASE_PORT" "$env_file" | cut -d'=' -f2 | sed 's/#.*//' | xargs)
  DATABASE_USER=$(grep "^DATABASE_USER" "$env_file" | cut -d'=' -f2 | sed 's/#.*//' | xargs)
  DATABASE_PASSWORD=$(grep "^DATABASE_PASSWORD" "$env_file" | cut -d'=' -f2 | sed 's/#.*//' | xargs)
  DATABASE_NAME=$(grep "^DATABASE_NAME" "$env_file" | cut -d'=' -f2 | sed 's/#.*//' | xargs)
  DATABASE_TYPE=$(grep "^DATABASE_TYPE" "$env_file" | cut -d'=' -f2 | sed 's/#.*//' | xargs)
  
  # 验证必要的配置
  if [[ -z "$DATABASE_HOST" ]] || [[ -z "$DATABASE_PORT" ]] || [[ -z "$DATABASE_USER" ]] || [[ -z "$DATABASE_NAME" ]]; then
    error "数据库配置不完整，请检查 $env_file 文件"
    return 1
  fi
  
  return 0
}

# ========== FastAPI 功能函数 ==========

# 1. 启动开发服务器
function start_dev_server() {
  print_separator
  echo -e "${tty_cyan}🚀 启动（uv run dev）...${tty_reset}"
  
  load_db_config || return 1
  
  echo -e "${tty_blue}🗄️ 检查并创建数据库...${tty_reset}"
  
  # 检查数据库是否存在
  DB_EXISTS=$(PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "postgres" -tAc "SELECT 1 FROM pg_database WHERE datname='$DATABASE_NAME';" 2>/dev/null || echo "")
  
  if [ "$DB_EXISTS" != "1" ]; then
    warn "数据库 '$DATABASE_NAME' 不存在，正在创建..."
    CREATE_DB_OUTPUT=$(PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "postgres" -c "CREATE DATABASE \"$DATABASE_NAME\" WITH ENCODING 'UTF8' LC_COLLATE 'C.UTF-8' LC_CTYPE 'C.UTF-8' TEMPLATE template0 OWNER $DATABASE_USER;" 2>&1)
    if [ $? -ne 0 ]; then
      error "数据库创建失败"
      echo -e "${tty_red}错误详情:${tty_reset}"
      echo -e "${tty_red}$CREATE_DB_OUTPUT${tty_reset}"
      return 1
    fi
    info "数据库 '$DATABASE_NAME' 创建成功 (UTF8 编码, C.UTF-8 排序规则)"
  else
    info "数据库 '$DATABASE_NAME' 已存在"
  fi
  
  print_separator
  cd "$SCRIPT_DIR"
  uv run main.py run --env=dev
  JudgeSuccess "开发服务器启动"
  
  echo -e "${tty_green}🎉 开发服务器启动完成！${tty_reset}"
  print_separator
}

# 2. 生成迁移文件
function create_migration() {
  print_separator
  echo -e "${tty_cyan}📝 生成迁移文件（模型变更后）...${tty_reset}"
  
  cd "$SCRIPT_DIR"
  uv run main.py revision --env=dev
  JudgeSuccess "迁移文件生成"
  
  echo -e "${tty_green}🎉 迁移文件生成完成！${tty_reset}"
  print_separator
}

# 3. 应用迁移
function apply_migration() {
  print_separator
  echo -e "${tty_cyan}⚡ 应用迁移...${tty_reset}"
  
  cd "$SCRIPT_DIR"
  uv run main.py upgrade --env=dev
  JudgeSuccess "迁移应用"
  
  echo -e "${tty_green}🎉 迁移应用完成！${tty_reset}"
  print_separator
}

# 4. 重置数据库中的迁移记录
function reset_migration_records() {
  print_separator
  echo -e "${tty_cyan}🔄 重置数据库中的迁移记录...${tty_reset}"
  
  echo -e "${tty_yellow}⚠️ 警告：此操作将重置数据库中的迁移记录！${tty_reset}"
  read -p "确认继续吗？(y/N): " confirm
  if [[ $confirm != [yY] ]]; then
    echo -e "${tty_yellow}操作已取消${tty_reset}"
    return
  fi
  
  load_db_config || return 1
  
  cd "$SCRIPT_DIR"
  echo -e "${tty_blue}🔄 正在重置迁移记录...${tty_reset}"
  
  # 使用 psql 连接到数据库并重置迁移记录
  PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c "DELETE FROM alembic_version;" 2>/dev/null
  JudgeSuccess "迁移记录重置"
  
  echo -e "${tty_green}🎉 迁移记录重置完成！${tty_reset}"
  print_separator
}

# 5. 清理数据库（删除所有表）
function clean_database() {
  print_separator
  echo -e "${tty_cyan}🗄️ 清理数据库（删除所有表）...${tty_reset}"
  
  echo -e "${tty_yellow}⚠️ 警告：此操作将删除数据库中的所有数据！${tty_reset}"
  read -p "确认继续吗？(y/N): " confirm
  if [[ $confirm != [yY] ]]; then
    echo -e "${tty_yellow}操作已取消${tty_reset}"
    return
  fi
  
  load_db_config || return 1
  
  cd "$SCRIPT_DIR"
  echo -e "${tty_blue}🗄️ 清理数据库，删除所有现有的表...${tty_reset}"
  
  # 使用 psql 连接到数据库并删除所有表
  PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" 2>/dev/null
  JudgeSuccess "数据库清理"
  
  echo -e "${tty_green}🎉 数据库清理完成！${tty_reset}"
  print_separator
}

# 6. 删除数据库
function drop_database() {
  print_separator
  echo -e "${tty_cyan}🗑️ 删除数据库...${tty_reset}"
  
  # 获取数据库名称
  echo -e "${tty_blue}📝 请输入要删除的数据库名称:${tty_reset}"
  read -p "数据库名称: " db_name
  
  # 验证数据库名称不为空
  if [[ -z "$db_name" ]]; then
    error "数据库名称不能为空！"
    return
  fi
  
  # 显示警告信息
  echo -e "${tty_red}⚠️ 警告：此操作将永久删除数据库 '$db_name' 及其所有数据！${tty_reset}"
  echo -e "${tty_yellow}此操作不可撤销！${tty_reset}"
  
  # 第一次确认
  read -p "确认要删除数据库 '$db_name' 吗？(y/N): " confirm1
  if [[ $confirm1 != [yY] ]]; then
    echo -e "${tty_yellow}操作已取消${tty_reset}"
    return
  fi
  
  # 第二次确认
  echo -e "${tty_red}⚠️ 最后确认：您真的要删除数据库 '$db_name' 吗？${tty_reset}"
  read -p "请输入 'DELETE' 来确认删除: " confirm2
  if [[ $confirm2 != "DELETE" && $confirm2 != "delete" ]]; then
    echo -e "${tty_yellow}操作已取消${tty_reset}"
    return
  fi
  
  load_db_config || return 1
  
  cd "$SCRIPT_DIR"
  echo -e "${tty_blue}🗑️ 正在删除数据库 '$db_name'...${tty_reset}"
  
  # 先断开所有连接到该数据库的连接
  PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "postgres" -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$db_name' AND pid <> pg_backend_pid();" 2>/dev/null
  
  # 删除数据库
  PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "postgres" -c "DROP DATABASE IF EXISTS \"$db_name\";" 2>/dev/null
  JudgeSuccess "数据库删除"
  
  echo -e "${tty_green}🎉 数据库 '$db_name' 删除完成！${tty_reset}"
  print_separator
}

# 7. 初始化数据（执行 sql 目录下脚本）
function init_sql_data() {
  print_separator
  echo -e "${tty_cyan}🧰 初始化数据...${tty_reset}"

  local sql_dir
  sql_dir="$REPO_ROOT/backend/sql/postgres/init_data"
  
  if [ ! -d "$sql_dir" ]; then
    error "未找到 SQL 目录: $sql_dir"
    return 1
  fi

  local sql_files=()
  while IFS= read -r file; do
    sql_files+=("$file")
  done < <(find "$sql_dir" -maxdepth 1 -type f -name "*.sql" 2>/dev/null | sort)

  if [ ${#sql_files[@]} -eq 0 ]; then
    warn "SQL 目录下没有可执行的 .sql 文件: $sql_dir"
    return 0
  fi

  echo -e "${tty_purple}可用 SQL 文件：${tty_reset}"
  echo -e "${tty_yellow}0. 执行全部 SQL 文件${tty_reset}"

  local i
  for i in "${!sql_files[@]}"; do
    echo "$((i + 1)). $(basename "${sql_files[$i]}")"
  done

  local choice
  read -p "请选择要初始化的 SQL（输入序号）: " choice

  if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
    error "输入无效，请输入数字序号"
    return 1
  fi

  load_db_config || return 1

  if [ "$choice" -eq 0 ]; then
    echo -e "${tty_blue}🚀 开始执行全部 SQL 文件...${tty_reset}"
    local file
    for file in "${sql_files[@]}"; do
      echo -e "${tty_blue}执行: $(basename "$file")${tty_reset}"
      if PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "$DATABASE_NAME" -f "$file"; then
        info "执行成功: $(basename "$file")"
      else
        error "执行失败: $(basename "$file")"
        return 1
      fi
    done
    info "全部 SQL 文件执行完成"
  else
    local index=$((choice - 1))
    if [ "$index" -lt 0 ] || [ "$index" -ge ${#sql_files[@]} ]; then
      error "序号超出范围"
      return 1
    fi

    local selected_file="${sql_files[$index]}"
    echo -e "${tty_blue}执行: $(basename "$selected_file")${tty_reset}"
    if PGPASSWORD="$DATABASE_PASSWORD" psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "$DATABASE_NAME" -f "$selected_file"; then
      info "执行成功: $(basename "$selected_file")"
      info "SQL 初始化完成"
    else
      error "执行失败: $(basename "$selected_file")"
      return 1
    fi
  fi

  print_separator
}

# 主菜单
function main_menu() {
  clear
  show_banner
  echo -e "\033[1;34m📦 请选择要执行的操作：\033[0m"
  echo ""
  echo -e "\033[1;33m1. 🚀 启动（uv run dev）\033[0m"
  echo -e "\033[1;32m2. 📝 生成迁移文件（模型变更后）\033[0m"
  echo -e "\033[1;36m3. ⚡ 应用迁移\033[0m"
  echo -e "\033[1;36m4. 🔄 重置数据库中的迁移记录\033[0m"
  echo -e "\033[1;31m5. 🗄️ 清理数据库（删除所有表）\033[0m"
  echo -e "\033[1;31m6. 🗑️ 删除数据库\033[0m"
  echo -e "\033[1;36m7. 🧰 初始化数据（执行 sql 脚本）\033[0m"
  echo -e "\033[1;31m0. ❌ 退出\033[0m"
  echo ""

  read -p "请选择你要执行的操作: " option
  case $option in
    1) start_dev_server && pause ;;
    2) create_migration && pause ;;
    3) apply_migration && pause ;;
    4) reset_migration_records && pause ;;
    5) clean_database && pause ;;
    6) drop_database && pause ;;
    7) init_sql_data && pause ;;
    0) exit 0 ;;
    *) error "未知选项: $option" && pause ;;
  esac
}

# 非交互模式入口
if [[ "$1" == "--start-dev" ]]; then
  start_dev_server
  exit $?
fi

# 默认进入交互菜单
main_menu
