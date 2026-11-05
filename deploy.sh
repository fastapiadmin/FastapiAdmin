#!/usr/bin/env bash
# ============================================================================
# FastapiAdmin 统一部署脚本（本地构建成品 + 容器管理）
#
# 设计目标：
#   1. 服务器上不放业务源码、不跑构建，只接收构建好的成品；
#   2. 后端用「镜像」交付（docker save | ssh docker load），前端用 tar 管道交付；
#   3. 每次上线前先在服务器 backups/ 留一份备份，可一键回滚；
#   4. 只重建变化的那一个容器，MySQL/Redis/Nginx 不重启。
#
# 用法：
#   ./deploy.sh web                 # Web 管理后台（nginx /web）
#   ./deploy.sh app                 # 移动端 H5（nginx /app）
#   ./deploy.sh backend             # 构建并部署 MySQL 版后端镜像（切换线上）
#   ./deploy.sh backend-pg          # 只构建并自检 PostgreSQL 版镜像，不切换线上
#   ./deploy.sh all                 # 三样全发（后端默认 MySQL 版）
#   ./deploy.sh verify              # 公网四端验证
#   ./deploy.sh backups             # 列出服务器上的备份
#   ./deploy.sh rollback web        # 回滚 Web 到最近一次备份
#   ./deploy.sh rollback app        # 回滚 H5 到最近一次备份
#   ./deploy.sh local      # 本机 docker compose up -d --build（开发/单机）
#   ./deploy.sh start|stop|restart|logs|clean  # 服务器容器管理
#
# 前置条件：
#   - 本机 SSH 密钥可免密登录 root@$FA_SERVER
#   - backend 目标需要本机 docker（Colima / Docker Desktop 均可）
#   - frontend/web、frontend/app 依赖已安装（pnpm install）
#
# 环境变量覆盖：FA_SERVER、FA_REMOTE_ROOT、FA_BACKUP_DIR
# ============================================================================
set -euo pipefail

SERVER="${FA_SERVER:-8.137.99.5}"
REMOTE_ROOT="${FA_REMOTE_ROOT:-/home/FastapiAdmin}"
BACKUP_DIR="${FA_BACKUP_DIR:-/home/FastapiAdmin/backups}"
BACKUP_KEEP="${FA_BACKUP_KEEP:-5}"      # 每个标签最多保留的备份份数
IMAGE_KEEP="${FA_IMAGE_KEEP:-2}"        # 每类镜像最多保留的版本数（当前 + 回滚点）
STAMP="$(date +%Y%m%d-%H%M%S)"
KEY="$HOME/.ssh/id_ed25519"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=15)

log()  { printf '\033[0;34m[%s]\033[0m %s\n' "$(date +%H:%M:%S)" "$*"; }
ok()   { printf '\033[0;32m  ✅ %s\033[0m\n' "$*"; }
die()  { printf '\033[0;31m  ❌ %s\033[0m\n' "$*"; exit 1; }

ssh_do() { ssh "${SSH_OPTS[@]}" -i "$KEY" "root@${SERVER}" "$@"; }

# 把本地目录内容流式发到服务器目标目录。
# 服务器侧流程：解包到暂存区 → 校验入口文件 → 备份旧目录到 backups/<label>-<时间> →
#              原子替换 → 修正属主。任何一步失败都中止，绝不留下半成品。
# 用法: push_dir <本地目录> <远端目录> <备份标签>
push_dir() {
  local src="$1" dst="$2" label="$3"
  [ -d "$src" ] || die "本地目录不存在: $src"
  local ts tar_cmd ssh_cmd
  ts="$(date +%Y%m%d-%H%M%S)"

  tar_cmd="COPYFILE_DISABLE=1 tar -czf - -C $(printf '%q' "$src") ."
  ssh_cmd="
set -e
dst=$(printf '%q' "$dst")
bakdir=$(printf '%q' "$BACKUP_DIR")
bak=\"\$bakdir/$(printf '%q' "$label")-\$(date +%Y%m%d-%H%M%S)\"

rm -rf /tmp/fa-stage && mkdir -p /tmp/fa-stage
tar -xzf - --no-same-owner -C /tmp/fa-stage
find /tmp/fa-stage \( -name '._*' -o -name '.DS_Store' \) -delete
[ -f /tmp/fa-stage/index.html ] || { echo 'ERROR: 缺少 index.html，中止'; exit 1; }
new=\$(find /tmp/fa-stage -type f | wc -l)
[ \"\$new\" -gt 0 ] || { echo 'ERROR: 上传内容为空，中止'; exit 1; }

if [ -e \"\$dst\" ]; then
  mkdir -p \"\$bakdir\"
  rm -rf \"\$bak\"
  cp -a \"\$dst\" \"\$bak\"
  old=\$(find \"\$bak\" -type f | wc -l)
  [ \"\$old\" -gt 0 ] || { echo 'ERROR: 备份为空，中止'; exit 1; }
  echo \"  备份 OK: \${bak} （\${old} 文件）\"
fi

rm -rf \"\$dst\" && mkdir -p \"\$dst\"
for e in \$(ls -A /tmp/fa-stage); do mv \"/tmp/fa-stage/\$e\" \"\$dst\"/; done
rm -rf /tmp/fa-stage
chown -R root:root \"\$dst\"
echo \"  上线 OK: \$new 文件, \$(du -sh \"\$dst\" | cut -f1), 属主 \$(stat -c %U:%G \"\$dst\")\"
"
  log "上传 $(basename "$src") → $dst"
  if ! eval "$tar_cmd" 2>/dev/null | ssh_do "$ssh_cmd"; then
    die "部署失败：远端未做替换，备份保留，可安全重试"
  fi
  _rotate_backups "$label"
}

# 每个标签只保留最近 BACKUP_KEEP 份备份（web 一份 23MB，不轮转会持续吃磁盘）
_rotate_backups() {
  local label="$1" keep="$BACKUP_KEEP"
  ssh_do "
    bakdir=${BACKUP_DIR}
    ls -1dt \"\$bakdir/${label}-\"* 2>/dev/null | tail -n +\$(( ${keep} + 1 )) | while read -r d; do
      rm -rf \"\$d\" && echo \"  轮转删除旧备份: \$(basename \$d)\"
    done
    true
  "
}

# ---------- Web 管理后台 ----------
deploy_web() {
  log "构建 Web 管理后台（vue-tsc 类型检查由 type-check 单独负责，这里只出产物）"
  ( cd frontend/web && pnpm run build:prod >/tmp/fa-web-build.log 2>&1 ) \
    || { tail -20 /tmp/fa-web-build.log; die "web 构建失败"; }
  ok "web 构建完成：$(du -sh frontend/web/dist | cut -f1)"
  push_dir frontend/web/dist "${REMOTE_ROOT}/docker/nginx/web/dist" "web"
  ok "Web 已上线"
}

# ---------- 移动端 H5 ----------
deploy_app() {
  log "构建移动端 H5"
  ( cd frontend/app && pnpm run build:h5 >/tmp/fa-app-build.log 2>&1 ) \
    || { tail -20 /tmp/fa-app-build.log; die "app 构建失败"; }
  ok "H5 构建完成：$(du -sh frontend/app/dist/build/h5 | cut -f1)"
  # nginx /app 用 alias 指向 app/dist，真实入口在 build/h5 下；
  # try_files 回退到 /app/index.html，少一层就 500 内部重定向死循环
  push_dir frontend/app/dist/build/h5 \
           "${REMOTE_ROOT}/docker/nginx/app/dist/build/h5" "app-h5"
  ok "H5 已上线"
}

# ---------- 后端镜像 ----------
# deploy_backend <mysql|postgres|sqlite> [switch]
#   switch=1（默认）构建并切换线上；switch=0 只构建+装载+自检，不动生产
deploy_backend() {
  local db="${1:-mysql}" switch="${2:-1}"
  case "$db" in mysql|postgres|sqlite) ;; *) die "数据库类型只能是 mysql / postgres / sqlite" ;; esac
  local tag="backend:${db}-${STAMP}"
  command -v docker >/dev/null || die "本机没有 docker，无法构建镜像"

  log "准备构建上下文"
  rm -rf /tmp/fa-ctx && mkdir -p /tmp/fa-ctx/backend
  ( cd backend && tar -cf - \
      --exclude='.mypy_cache' --exclude='.pytest_cache' --exclude='__pycache__' \
      --exclude='logs' --exclude='tests' --exclude='dist' --exclude='.venv' \
      --exclude='.DS_Store' --exclude='.ruff_cache' --exclude='.codebuddy' \
      --exclude='.vscode' --exclude='.python-version' \
      --exclude='env/.env.dev' --exclude='env/.env.test' \
      . ) | tar -xf - -C /tmp/fa-ctx/backend/
  # 依赖清单目录化：核心 + 数据库驱动分离，镜像里只装所选数据库的驱动
  rm -rf /tmp/fa-ctx/requirements && mkdir -p /tmp/fa-ctx/requirements
  cp -R backend/requirements/. /tmp/fa-ctx/requirements/

  # 镜像内的 .env.prod 只是兜底：数据库/Redis 真实地址与口令由 compose 运行时注入。
  # 这里抹掉本地私网地址与所有密钥/口令，避免把任何凭据烤进镜像层
  # （审计 B3：旧镜像里曾烘进真实 DATABASE_PASSWORD / REDIS_PASSWORD）。
  python3 - "$db" <<'PY'
import re, pathlib, sys
db = sys.argv[1]
p = pathlib.Path("/tmp/fa-ctx/backend/env/.env.prod")
force = {"DATABASE_HOST": "localhost", "REDIS_HOST": "localhost"}
if db == "postgres":
    force.update({"DATABASE_TYPE": "postgres", "DATABASE_PORT": "5432", "DATABASE_USER": "postgres"})
drop_prefixes = ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL")
# 口令类：运行时全部由 compose 注入，镜像内保留会成为泄露面
drop_keys = {
    "DATABASE_PASSWORD", "REDIS_PASSWORD",
    "SECRET_KEY", "DATA_ENCRYPTION_KEY", "DATA_ENCRYPTION_OLD_KEYS",
    "MYSQL_PASSWORD", "MYSQL_ROOT_PASSWORD",
}
out = []
for line in p.read_text().splitlines():
    m = re.match(r"^(\s*)([A-Z_]+)(\s*=\s*)(.*)$", line)
    if m and m.group(2) in force:
        out.append(f"{m.group(1)}{m.group(2)}{m.group(3)}{force[m.group(2)]}")
    elif m and m.group(2).startswith(drop_prefixes):
        continue
    elif m and m.group(2) in drop_keys:
        continue
    else:
        out.append(line)
p.write_text("\n".join(out) + "\n")
PY

  # 只装所选数据库的驱动：mysql 变体不装 asyncpg/psycopg，postgres 变体不装 aiomysql/pymysql
  # 运行用户为非 root（UID 1000）：容器逃逸后的影响面更小
  cat > /tmp/fa-ctx/Dockerfile <<EOF
FROM python:3.12-slim
ARG DB=${db}
ENV TZ=Asia/Shanghai PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 LANG=C.UTF-8 DB=\${DB}
WORKDIR /home
COPY requirements/ /home/requirements/
RUN pip install --no-cache-dir \\
      -r /home/requirements/base.txt \\
      -r /home/requirements/db/\${DB}.txt \\
      -r /home/requirements/storage.txt \\
      -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY backend/ /home/
# 运行时需要写入的目录（日志、上传、迁移版本目录）预先建好并交给运行用户
RUN useradd --uid 1000 --create-home --shell /usr/sbin/nologin app \\
 && mkdir -p /home/logs /home/static/upload /home/alembic/versions \\
 && chown -R app:app /home
USER app
EXPOSE 8001
CMD ["python", "main.py", "run", "--env=prod"]
EOF
  cat > /tmp/fa-ctx/.dockerignore <<'EOF'
**/__pycache__
**/*.pyc
**/.mypy_cache
**/.pytest_cache
**/logs
**/tests
**/.DS_Store
EOF

  log "构建镜像 ${tag} （linux/amd64，依赖层命中缓存时约 5 秒）"
  docker build --platform linux/amd64 -t "$tag" /tmp/fa-ctx >/tmp/fa-build.log 2>&1 \
    || { tail -25 /tmp/fa-build.log; die "镜像构建失败"; }
  ok "镜像构建完成：$(docker images "$tag" --format '{{.Size}}')"

  log "传输镜像（docker save | gzip | ssh docker load）"
  docker save "$tag" | gzip -1 | ssh_do 'gunzip | docker load' >/dev/null
  ok "镜像已加载到服务器"

  if [ "$switch" != "1" ]; then
    # 只构建与装载，不切换线上。用于生产数据库与镜像变体不一致时做验证。
    ok "镜像 ${tag} 已就绪但未切换（避免把 ${db} 变体切到当前生产环境）"
    local drivers
    case "$db" in
      postgres) drivers="asyncpg psycopg" ;;
      mysql)    drivers="aiomysql pymysql" ;;
      sqlite)   drivers="aiosqlite" ;;
    esac
    if ssh_do "
      set -e
      docker run --rm --platform linux/amd64 --entrypoint python ${tag} -c '
import importlib, sys
mods = sys.argv[1:]
for m in mods:
    importlib.import_module(m)
    print(\"    驱动可用:\", m)
print(\"    自检通过:\", len(mods), \"个 ${db} 驱动\")
' ${drivers}
" 2>/dev/null; then
      ok "镜像自检通过：${db} 驱动可正常导入"
    else
      die "镜像自检失败：${db} 驱动无法导入"
    fi
    return 0
  fi

  log "切换并只重建 backend（MySQL/Redis/Nginx 不动）"
  ssh_do "
    set -e
    cd ${REMOTE_ROOT}/docker
    # 容器以非 root（UID 1000）运行；宿主绑定挂载的上传目录必须属于该 UID，否则无法写入
    mkdir -p backend/static/upload
    chown -R 1000:1000 backend/static/upload
    docker tag backend:3.0.0 backend:prev 2>/dev/null || true
    docker tag ${tag} backend:3.0.0
    docker compose up -d --force-recreate backend
    for i in 1 2 3 4 5 6 7; do
      sleep 15
      st=\$(docker inspect backend --format '{{.State.Health.Status}}')
      echo \"  健康检查: \$st\"
      [ \"\$st\" = healthy ] && break
    done
    echo \"  运行用户: \$(docker inspect backend --format '{{.Config.User}}')\"
    docker inspect backend --format '  镜像={{.Config.Image}} 状态={{.State.Status}}'
  "
  ok "后端已上线（回滚：docker tag backend:prev backend:3.0.0 && docker compose up -d backend）"
}

# ---------- 验证 ----------
verify() {
  log "公网四端验证"
  local fail=0
  for p in "/" "/web/" "/app/" "/api/v1/monitor/health/check"; do
    printf '  %-42s ' "$p"
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://service.fastapiadmin.com${p}")
    printf 'HTTP %s\n' "$code"
    [ "$code" = "200" ] || fail=1
  done
  [ "$fail" -eq 0 ] && ok "四端全部 200" || die "存在非 200 端点"
}

# ---------- 轮转清理：备份目录与镜像仓库，避免磁盘无限增长 ----------
prune() {
  log "轮转清理（备份每标签保留 ${BACKUP_KEEP} 份，镜像每类保留 ${IMAGE_KEEP} 个）"
  ssh_do "
    bakdir=${BACKUP_DIR}
    keep=${BACKUP_KEEP}
    if [ -d \"\$bakdir\" ]; then
      for label in \$(ls -1 \"\$bakdir\" | sed 's/-[0-9]\{8\}-[0-9]\{6\}\$//' | sort -u); do
        n=0
        for d in \$(ls -1dt \"\$bakdir\"/\$label-* 2>/dev/null); do
          n=\$((n+1))
          if [ \"\$n\" -gt \"\$keep\" ]; then rm -rf \"\$d\"; echo \"  清理备份: \$(basename \$d)\"; fi
        done
      done
    fi
    true   # 显式成功，避免末端条件表达式在 set -e 下打断后续清理
  "
  # 镜像 tag 形如 <db>-YYYYmmdd-HHMMSS，按 tag 排序即时间序（比 CreatedAt 可靠：秒级相同会乱序）
  local prefix t
  for prefix in "mysql-" "postgres-" "sqlite-" "release-" "deploy-"; do
    while IFS= read -r t; do
      [ -n "$t" ] || continue
      docker rmi "backend:${t}" >/dev/null 2>&1 && ok "清理本机镜像 backend:${t}"
    done < <(docker images "backend:${prefix}*" --format '{{.Tag}}' 2>/dev/null \
             | sort -r | tail -n +$((IMAGE_KEEP + 1)))
  done
  for prefix in "mysql-" "postgres-" "sqlite-" "release-" "deploy-"; do
    for t in $(ssh_do "docker images 'backend:${prefix}*' --format '{{.Tag}}' 2>/dev/null | sort -r | tail -n +$((IMAGE_KEEP + 1))"); do
      [ -n "$t" ] || continue
      ssh_do "docker rmi 'backend:${t}' >/dev/null 2>&1 && echo '  清理服务器镜像 backend:${t}'"
    done
  done
  ssh_do "df -h / | tail -1 | sed 's/^/  文件系统: /'"
  ok "清理完成"
}

# ---------- 备份与回滚 ----------
list_backups() {
  log "服务器备份（${BACKUP_DIR}）"
  ssh_do "ls -1t ${BACKUP_DIR} 2>/dev/null | head -20 || echo '  （还没有备份）'"
}

# rollback <web|app|backend>
rollback() {
  local what="${1:-}"
  case "$what" in
    web)     _rollback_dir web     "${REMOTE_ROOT}/docker/nginx/web/dist" ;;
    app)     _rollback_dir app-h5  "${REMOTE_ROOT}/docker/nginx/app/dist/build/h5" ;;
    backend) _rollback_image ;;
    *) die "用法: $0 rollback <web|app|backend>" ;;
  esac
  verify
}

_rollback_dir() {
  local label="$1" dst="$2"
  log "回滚 $label → $dst"
  ssh_do "
    set -e
    bak=\$(ls -1dt ${BACKUP_DIR}/${label}-* 2>/dev/null | head -1)
    [ -n \"\$bak\" ] || { echo '  ERROR: 没有可用备份'; exit 1; }
    [ -f \"\$bak/index.html\" ] || { echo \"  ERROR: 备份 \$bak 缺少 index.html\"; exit 1; }
    rm -rf '${dst}.broken' && mv '${dst}' '${dst}.broken'
    mkdir -p '${dst}'
    for e in \$(ls -A \"\$bak\"); do cp -a \"\$bak/\$e\" '${dst}'/; done
    rm -rf '${dst}.broken'
    chown -R root:root '${dst}'
    echo \"  已回滚自: \${bak} （\$(find '${dst}' -type f | wc -l) 文件）\"
  "
}

_rollback_image() {
  log "回滚后端到 backend:prev"
  ssh_do "
    set -e
    cd ${REMOTE_ROOT}/docker
    docker image inspect backend:prev >/dev/null 2>&1 || { echo '  ERROR: backend:prev 不存在'; exit 1; }
    docker tag backend:prev backend:3.0.0
    docker compose up -d --force-recreate backend
    sleep 30
    docker inspect backend --format '  已回滚: 镜像={{.Config.Image}} 健康={{.State.Health.Status}}'
  "
}

_compose() {
  cd "${REMOTE_ROOT}/docker" 2>/dev/null || die "找不到服务器部署目录: ${REMOTE_ROOT}/docker"
  docker compose "$@"
}

case "${1:-}" in
  web)                 deploy_web;             verify; prune ;;
  app)                 deploy_app;             verify; prune ;;
  backend)             deploy_backend mysql 1;    verify; prune ;;
  backend-pg)          deploy_backend postgres 0 ;;   # 只构建+自检，绝不自动切换生产
  all)                 deploy_web; deploy_app; deploy_backend mysql 1; verify; prune ;;
  verify)              verify ;;
  prune)               prune ;;
  backups)             list_backups ;;
  rollback)            rollback "${2:-}" ;;
  local)               ( cd "$(dirname "$0")/docker" && docker compose up -d --build ) ;;
  start)               _compose up -d ;;
  stop)                _compose stop ;;
  restart)             _compose restart; _compose ps ;;
  logs)                _compose logs --tail 200 -f ;;
  clean)               docker image prune -f; docker builder prune -f ;;
  help|-h|--help)      sed -n '2,35p' "$0"; exit 0 ;;
  *) sed -n '2,35p' "$0"; exit 1 ;;
esac
