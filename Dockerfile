FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables (optional, for production)
# ENV BOT_TOKEN=your_token
# ENV SUPERADMIN=your_admin_id
# ENV API_ID=your_api_id
# ENV API_HASH=your_api_hash

CMD ["python3", "bot/main_bot.py"]