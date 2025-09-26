# Base
FROM python:3.12-slim

# Runtime env (unbuffered logs, UTF-8, no .pyc files, faster pip)
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Workdir
WORKDIR /app

# System deps (keep minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# App code
COPY . .

# Start (explicit -u for clarity)
CMD ["python3", "-u", "bot/main_bot.py"]
