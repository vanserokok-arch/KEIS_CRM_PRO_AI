# ---------- 1) Python deps ----------
FROM python:3.11-slim AS py-base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# system deps only for build (purged later)
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# requirements лежит в корне server/
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
 && apt-get purge -y --auto-remove build-essential \
 && rm -rf /var/lib/apt/lists/*

# ---------- 2) Build фронта ----------
FROM node:20 AS web-build
WORKDIR /web
ENV NODE_ENV=production

# фронтовые манифесты из КОРНЯ репо
COPY package.json package-lock.json /web/
RUN npm ci

# только нужные фронтовые файлы из КОРНЯ
COPY index.html vite.config.ts tsconfig.json /web/
COPY src /web/src
COPY public /web/public

# пробрасываем base для фронта на этапе сборки (можно переопределять при build)
ARG VITE_API_BASE=http://localhost:8000
ENV VITE_API_BASE=$VITE_API_BASE
RUN npm run build

# ---------- 3) PROD-образ ----------
# используем готовый слой с установленными python-зависимостями
FROM py-base AS prod
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# серверный код
COPY server /app

# собранный фронт кладём туда, где его ждёт FastAPI (FRONT_DIST=/app/dist)
COPY --from=web-build /web/dist /app/dist

EXPOSE 8000
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]