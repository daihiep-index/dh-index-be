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

# Tạo thư mục logs nếu chưa có
RUN mkdir -p logs

# Collect static files (nếu có)
RUN python manage.py collectstatic --noinput || true

# Tạo volume cho database để bảo toàn data
VOLUME ["/app/db.sqlite3"]

# Expose port 8000
EXPOSE 8000

# Tạo script khởi động
COPY <<EOF /app/start.sh
#!/bin/bash
set -e

echo "Chạy migrations..."
python manage.py migrate

echo "Tạo superuser nếu chưa có..."
python create_superuser.py

echo "Khởi động Django server..."
exec python manage.py runserver 0.0.0.0:8000
EOF

# Cấp quyền thực thi cho script
RUN chmod +x /app/start.sh

# Command để chạy server
CMD ["/app/start.sh"]
