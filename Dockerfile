# ---- 1. Base image ----
FROM python:3.11-slim

# ---- 2. Set working dir ----
WORKDIR /app

# ---- 3. Install dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- 4. Copy app ----
COPY . .

# ---- 5. Set env vars ----
ENV PYTHONUNBUFFERED=1

# ---- 6. Run with Gunicorn + UvicornWorker ----
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
