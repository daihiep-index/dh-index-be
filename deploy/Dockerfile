# Sử dụng Python 3.10 official image
FROM python:3.10-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc
WORKDIR /app

# Cập nhật hệ thống và cài đặt các dependencies cần thiết
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        build-essential \
        curl \
        git \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Cài đặt Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Cấu hình Poetry
RUN poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Cài đặt dependencies
RUN poetry install --only=main

# Copy source code
COPY . .

# Copy deployment scripts
COPY deploy/create_superuser.py .

# Tạo thư mục logs (database sẽ được tạo khi chạy migrations)
RUN mkdir -p logs

# Collect static files (nếu có)
RUN python manage.py collectstatic --noinput || true

# Note: Volume mounting should be handled at runtime with docker run -v
# VOLUME ["/app/db.sqlite3"]

# Expose port 8000
EXPOSE 8000

# Tạo script khởi động
COPY <<EOF /app/start.sh
#!/bin/bash
set -e

echo "=== Starting DH Index Backend ==="

echo "Checking Python and Django..."
python --version
python -c "import django; print('Django version:', django.get_version())"

echo "Checking database file..."
ls -la db.sqlite3 || echo "Database file not found, will be created during migrations"

echo "Ensuring database file permissions..."
if [ -f db.sqlite3 ]; then
    chmod 666 db.sqlite3
fi

echo "Chạy migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "No static files to collect"

echo "Tạo superuser nếu chưa có..."
python create_superuser.py

echo "Khởi động Django server..."
echo "Server will be available at http://0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000
EOF

# Cấp quyền thực thi cho script
RUN chmod +x /app/start.sh

# Command để chạy server
CMD ["bash", "/app/start.sh"]
