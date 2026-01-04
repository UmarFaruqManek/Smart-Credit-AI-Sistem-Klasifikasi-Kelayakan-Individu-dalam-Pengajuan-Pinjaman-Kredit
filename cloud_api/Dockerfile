# Gunakan image Python yang ringan
FROM python:3.9-slim

# Setup working directory di dalam container
WORKDIR /app

# Copy requirements terlebih dahulu agar caching layer optimal
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code ke dalam container
COPY . .

# Expose port (Cloud Run default: 8080)
ENV PORT=8080

# Jalankan aplikasi menggunakan gunicorn untuk production performance
# Workers = 1-2 sudah cukup untuk demo, sesuaikan dengan resource
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
