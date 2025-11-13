# AI_WORKFLOW — как работать с этим репозиторием

Ты — ИИ-разработчик, который помогает дорабатывать KEIS CRM PRO AI.

## Структура проекта

- `docker-compose.yml` — запуск прод-контейнера на сервере.
- `docker-compose.prod.yml` — сборка прод-образа фронта.
- `.github/workflows/docker-build.yml` — CI: сборка и пуш Docker-образов в GHCR/Docker Hub.
- `.github/workflows/deploy.yml` — CD: деплой на сервер 94.241.141.3 через SSH.
- `server/` или `api/` — backend (FastAPI, uvicorn main:app).
- `web/` или корень проекта — frontend (React + Vite).

## Команды, которые нужно использовать

### Frontend

- Сборка: `npm run build`
- (если появятся) Тесты: `npm test`
- Форматирование/линт (когда добавим): `npm run lint` / `npm run format`

### Docker / CI

Локально (при необходимости руками):

- `docker compose -f docker-compose.prod.yml build --no-cache`
- `docker compose -f docker-compose.prod.yml push`

На сервере (делает GitHub Actions, руками не трогаем):

- `cd /srv/keis`
- `docker compose pull`
- `docker compose up -d`

## Правила для ИИ

1. **Никогда** не меняй `.github/workflows/*` без явного запроса.
2. Все правки делай через минимальные диффы: меняй только нужные строки.
3. Перед коммитом:
   - `npm test` (если есть),
   - `npm run build`.
4. Коммиты в feature-ветки, а не напрямую в `main`.
   Пример имени ветки: `feature/add-deal-stage`, `fix/login-bug`.
5. Сообщения коммитов по форме:
   - `feat: ...`
   - `fix: ...`
   - `chore: ...`
6. Ничего не пушь в `main` напрямую — только через merge/PR.

## Локальный цикл задачи

1. Прочитай условие задачи.
2. Найди связанные файлы по названию/ключевым словам.
3. Сначала измени код фронта/бэка.
4. Запусти:
   - `npm test` (если есть),
   - `npm run build`.
5. Если всё ок — подготовь коммит и push в свою ветку.

