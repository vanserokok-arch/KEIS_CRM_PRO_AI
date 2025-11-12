# ---------- 1) Python deps ----------
FROM python:3.11-slim AS py-base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# requirements лежит в server/
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ---------- 2) Build фронта ----------
FROM node:20 AS web-build
WORKDIR /web
# фронтовые манифесты из КОРНЯ репо
COPY package.json ./
COPY package-lock.json ./
RUN npm ci || npm install
# весь фронт-код (у тебя он в корне)
COPY . .
ARG VITE_API_BASE=http://localhost:8000
ENV VITE_API_BASE=$VITE_API_BASE
RUN VITE_API_BASE=$VITE_API_BASE npm run build

# ---------- 3) PROD-образ ----------
FROM python:3.11-slim AS prod
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# установленные python-зависимости переносим из py-base
COPY --from=py-base /usr/local /usr/local

# серверный код
COPY server /app

# собранный фронт кладём туда, где его ждёт FastAPI (FRONT_DIST=/app/dist)
COPY --from=web-build /web/dist /app/dist

EXPOSE 8000
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]