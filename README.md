# DH Index Backend

Django REST API backend cho hệ thống quản lý danh mục đầu tư.

## 🚀 Repository Structure

```
dh-index-be/
├── dh_index/           # Django project
├── deploy/             # Docker deployment files
├── Jenkinsfile         # CI/CD pipeline
└── README.md          # This file
```

## 🛠 Tech Stack

- **Python 3.10**
- **Django 5.2.4**
- **Django REST Framework**
- **SQLite Database**
- **Docker & Docker Compose**
- **Jenkins CI/CD**

## 🏃‍♂️ Quick Start

### Local Development:
```bash
cd dh_index
poetry install
poetry shell
python manage.py migrate
python manage.py runserver
```

### Docker Development:
```bash
cd deploy
docker-compose up --build
```

### Production Deployment:
```bash
cd deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 🔐 Default Superuser

- **Username**: `dh`
- **Email**: `dh@gmail.com`
- **Password**: `123`

## 🌐 API Endpoints

- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/docs/
- **API Root**: http://localhost:8000/api/

## 🔄 CI/CD

Sử dụng Jenkins với Jenkinsfile để tự động:
- Build Docker image
- Run tests
- Deploy to production (khi push vào main branch)

### Setup Jenkins:
1. Tạo Pipeline job trong Jenkins
2. Repository URL: `https://github.com/daihiep-index/dh-index-be.git`
3. Script Path: `Jenkinsfile`

## 📁 Key Features

- ✅ **Auto superuser creation**
- ✅ **Database persistence**
- ✅ **Health checks**
- ✅ **Logging system**
- ✅ **CORS configuration**
- ✅ **JWT Authentication**