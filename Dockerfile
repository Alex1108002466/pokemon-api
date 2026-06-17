FROM python:3.12-slim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /code

# Копируем только файлы зависимостей сначала — для эффективного кеширования слоёв
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости из uv.lock
RUN uv sync --frozen --no-install-project

# Копируем остальной код приложения
COPY . .

# Добавляем виртуальное окружение uv в PATH
ENV PATH="/code/.venv/bin:$PATH"

EXPOSE 8000

# Перед запуском сервера применяем миграции Alembic, затем стартуем uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
