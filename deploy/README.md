# DH Index Backend - Docker Deployment

Thư mục này chứa các file cần thiết để deploy DH Index backend bằng Docker.

## Files trong thư mục deploy:

- `Dockerfile` - Docker image configuration
- `docker-compose.yml` - Docker Compose configuration  
- `.dockerignore` - Files to ignore during Docker build
- `create_superuser.py` - Script tự động tạo superuser
- `README.md` - Hướng dẫn này

## Cách sử dụng:

### 1. Sử dụng Docker Compose (Khuyến nghị)

```bash
cd dh_index/deploy
docker-compose up --build
```

### 2. Sử dụng Docker trực tiếp

```bash
cd dh_index/deploy
docker build -f Dockerfile -t dh-index-backend ..
docker run -p 8000:8000 \
  -v $(pwd)/../db.sqlite3:/app/db.sqlite3 \
  -v $(pwd)/../logs:/app/logs \
  dh-index-backend
```

## Tính năng:

- ✅ **Python 3.10** environment
- ✅ **Auto superuser creation**: 
  - Username: `dh`
  - Email: `dh@gmail.com`
  - Password: `123`
- ✅ **Database persistence**: Database được bảo toàn giữa các lần rebuild
- ✅ **Port 8000**: Application chạy trên port 8000
- ✅ **Auto migrations**: Tự động chạy migrations khi khởi động
- ✅ **Logs persistence**: Logs được lưu trên host machine

## Truy cập:

- **Application**: http://localhost:8000
- **Admin panel**: http://localhost:8000/admin
  - Username: `dh`
  - Password: `123`

## Lưu ý:

- Database `db.sqlite3` sẽ được tạo trong thư mục gốc `dh_index/`
- Logs sẽ được lưu trong thư mục `dh_index/logs/`
- Superuser chỉ được tạo lần đầu tiên, các lần sau sẽ bỏ qua nếu đã tồn tại
