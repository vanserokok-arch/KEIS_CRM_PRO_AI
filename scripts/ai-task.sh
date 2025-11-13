#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: scripts/ai-task.sh \"short-task-name\""
  exit 1
fi

TASK_NAME="$1"
BRANCH="ai/${TASK_NAME// /-}"

echo "==> Создаю ветку: $BRANCH"
git fetch origin main
git checkout main
git pull origin main
git checkout -b "$BRANCH" || git checkout "$BRANCH"

echo "==> Показываю текущий статус"
git status

echo "==> Устанавливаю зависимости (npm install, если нужно)"
if [ -f package.json ]; then
  npm install
fi

echo "==> Запускаю тесты (если есть)"
if npm run test -- --help >/dev/null 2>&1; then
  npm test || true
else
  echo "npm test не настроен — пропускаю"
fi

echo "==> Сборка фронтенда"
if [ -f package.json ]; then
  npm run build
fi

echo "==> Git status:"
git status

echo "==> Если всё ок, сделай:"
echo "   git add ."
echo "   git commit -m \"feat: ${TASK_NAME}\""
echo "   git push -u origin ${BRANCH}"
echo "и создай Pull Request в main."
