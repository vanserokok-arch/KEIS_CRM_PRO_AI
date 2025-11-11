#!/usr/bin/env bash
# KEIS_CRM_PRO_AI – единый автозапуск фронта и бэкенда
# Использование:
#   chmod +x ./run_all.sh
#   ./run_all.sh dev     # разработка: uvicorn --reload + vite
#   ./run_all.sh prod    # прод: сборка фронта + uvicorn (без reload)

set -euo pipefail

# --- Настройки портов ---
FRONT_PORT=${FRONT_PORT:-5173}
BACK_PORT=${BACK_PORT:-8000}

# --- Пути ---
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="${ROOT_DIR}/server"

# --- Цветные сообщения ---
msg()  { echo -e "\033[1;36m$*\033[0m"; }
ok()   { echo -e "\033[1;32m$*\033[0m"; }
warn() { echo -e "\033[1;33m$*\033[0m"; }
err()  { echo -e "\033[1;31m$*\033[0m" >&2; }

# --- Проверка зависимостей ---
need() {
  command -v "$1" >/dev/null 2>&1 || { err "Требуется '$1', но не найдено в PATH"; exit 1; }
}

need node
need npm
need python3
need lsof

MODE="${1:-dev}"
if [[ "$MODE" != "dev" && "$MODE" != "prod" ]]; then
  err "Неверный режим: ${MODE}. Используй: dev | prod"
  exit 1
fi

# --- Функция убийства процесса, занимающего порт ---
free_port() {
  local PORT="$1"
  if lsof -ti tcp:"$PORT" >/dev/null 2>&1; then
    warn "Порт $PORT занят. Останавливаю процесс..."
    lsof -ti tcp:"$PORT" | xargs -I {} kill -9 {} || true
    ok "Порт $PORT освобождён."
  fi
}

# --- Подготовка виртуального окружения и зависимостей ---
prepare_backend() {
  cd "$SERVER_DIR"
  if [[ ! -d ".venv" ]]; then
    msg "Создаю server/.venv ..."
    python3 -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate

  # Устанавливаем/обновляем pip и зависимости, если есть requirements.txt
  python -m pip install --upgrade pip >/dev/null
  if [[ -f "requirements.txt" ]]; then
    msg "Проверяю зависимости backend (requirements.txt) ..."
    python -m pip install -r requirements.txt >/dev/null
  fi

  # Подхват переменных окружения, если есть .env
  if [[ -f ".env" ]]; then
    # Экспортим пары KEY=VALUE; игнорируем комментарии и пустые строки
    set -o allexport
    # shellcheck disable=SC2046
    source <(grep -v '^\s*#' .env | grep -E '^[A-Za-z_][A-Za-z0-9_]*=' || true)
    set +o allexport
  fi
  cd "$ROOT_DIR"
}

# --- Запуск backend ---
start_backend_dev() {
  msg "Запускаю backend (dev)..."
  cd "$SERVER_DIR"
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m uvicorn main:app --reload --port "$BACK_PORT" &
  BACK_PID=$!
  cd "$ROOT_DIR"
  ok "Backend (dev) PID: $BACK_PID → http://127.0.0.1:${BACK_PORT}"
}

start_backend_prod() {
  msg "Запускаю backend (prod)..."
  cd "$SERVER_DIR"
  # shellcheck disable=SC1091
  source .venv/bin/activate
  # Можно добавить --host 0.0.0.0 при необходимости
  python -m uvicorn main:app --port "$BACK_PORT" &
  BACK_PID=$!
  cd "$ROOT_DIR"
  ok "Backend (prod) PID: $BACK_PID → http://127.0.0.1:${BACK_PORT}"
}

# --- Запуск frontend ---
start_frontend_dev() {
  msg "Запускаю frontend (Vite dev)..."
  npm run dev --silent &
  FRONT_PID=$!
  ok "Frontend (dev) PID: $FRONT_PID → http://localhost:${FRONT_PORT} (Vite выведет фактический порт)"
}

build_frontend_prod() {
  msg "Собираю frontend (Vite build)..."
  npm run build
  ok "Готово. Фронт собран в /dist и обслуживается FastAPI."
}

# --- Трап на выход: корректно гасим процессы ---
cleanup() {
  echo
  warn "Останавливаю процессы..."
  [[ -n "${FRONT_PID:-}" ]] && kill -9 "$FRONT_PID" 2>/dev/null || true
  [[ -n "${BACK_PID:-}"  ]] && kill -9 "$BACK_PID"  2>/dev/null || true
  ok "Готово."
}
trap cleanup INT TERM EXIT

# --- Основная логика ---
msg "KEIS CRM PRO AI – режим: ${MODE}"

# освобождаем порты
free_port "$FRONT_PORT"
free_port "$BACK_PORT"

# backend
prepare_backend
if [[ "$MODE" == "dev" ]]; then
  start_backend_dev
else
  build_frontend_prod
  start_backend_prod
fi

# frontend
if [[ "$MODE" == "dev" ]]; then
  start_frontend_dev
  msg "Открывай фронт: http://localhost:${FRONT_PORT} (или порт, который напишет Vite)"
else
  msg "Прод-режим: фронт отдаётся FastAPI c / (SPA), Swagger: /docs, Health: /api/v1/health"
fi

# держим скрипт живым в dev (пока работают процессы)
if [[ "$MODE" == "dev" ]]; then
  # ждём фронт
  wait "$FRONT_PID"
else
  # в проде просто ждём backend (если запущен на переднем плане – изменить по желанию)
  wait "$BACK_PID"
fi