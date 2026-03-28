# ---------- 1. Base image ----------
FROM python:3.13-slim

# ---------- 2. Environment variables ----------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.1

# ---------- 3. Install Poetry ----------
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# ---------- 4. Set workdir ----------
WORKDIR /app

# ---------- 5. Copy dependency files ----------
COPY pyproject.toml poetry.lock ./

# ---------- 6. Install system dependencies ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# ---------- 7. Install dependencies ----------
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# ---------- 8. Copy and install scraper as a package ----------
COPY scraper ./scraper
RUN pip install --no-cache-dir --force-reinstall ./scraper

# ---------- 9. Copy backend ----------
COPY backend ./backend

# ---------- 10. Expose and start ----------
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

