
# 📚 LMS Microservices Project

This project is a microservices-based **Library Management System** built using **FastAPI**, **Flask**, **MySQL**, and **Docker Compose**. It includes:

- `user-service`: User registration, login, and management (FastAPI + JWT)
- `book-service`: CRUD operations for books (FastAPI)
- `borrowing-service`: Manage book borrow/return actions (Flask)
- `mysql`: MySQL server with an `init.sql` script for DB setup

---

## 📁 Project Structure

```
LMS_SERVICE/
├── user-service/
│   ├── app/
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── book-service/
│   ├── app/
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── borrowing-service/
│   ├── app/
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── mysql-init/
│   └── init.sql
├── wait-for.sh
├── docker-compose.yaml
└── .env.example (optional global)
```

---

## ⚙️ Technologies

- FastAPI (User & Book Service)
- Flask (Borrowing Service)
- MySQL (Central RDBMS)
- Docker & Docker Compose
- JWT (Authentication)
- SQLAlchemy ORM

---

## 🚀 Getting Started

### ✅ Prerequisites

- Docker
- Docker Compose

### 🛠️ Setup Instructions

1. **Clone the repo**
```bash
git clone https://github.com/Dhanyamol-Devassy/Lms_Service.git
cd LMS_SERVICE
```

2. **Make `wait-for.sh` executable**
```bash
chmod +x wait-for.sh
```

3. **Set up `.env` files**

Each service has a `.env.example` file. Copy it and fill in credentials:

#### Global `.env.example`
```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=mysql
DB_PORT=3306
DB_NAME=your_default_db_name
MYSQL_ROOT_PASSWORD=your_root_password
```

#### `user-service/.env.example`
```
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=mysql
DB_PORT=3306
DB_NAME=lms_users
DATABASE_URL=mysql+mysqlconnector://your_user:your_password@mysql:3306/lms_users
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_SECRET_KEY=your_jwt_key
```

#### `book-service/.env.example`
```
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=mysql
DB_PORT=3306
DB_NAME=lms_books
DATABASE_URL=mysql+mysqlconnector://your_user:your_password@mysql:3306/lms_books
```

#### `borrowing-service/.env.example`
```
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=mysql
DB_PORT=3306
DB_NAME=lms_borrowing
DATABASE_URL=mysql+mysqlconnector://your_user:your_password@mysql:3306/lms_borrowing
```

4. **Build and start containers**
```bash
docker-compose up --build
```

5. **Access services**
- User Service: http://localhost:5001
- Book Service: http://localhost:5002
- Borrowing Service: http://localhost:5003

---

## 🔐 Authentication

- JWT used in user-service
- After login, use `access_token` as Bearer token in `Authorization` header

---

## 🧪 API Testing

Test endpoints with:
- Swagger UI (`/docs` on FastAPI services)
- Postman / Insomnia / cURL

---

## 📄 Environment Security Tips

**Don't commit your `.env` files** with real credentials. Always use `.env.example` with placeholders like:

```
DB_USER=your_user
DB_PASSWORD=your_password
```

---

## 🧰 Common Docker Commands

```bash
docker-compose down           # Stop containers
docker-compose down -v       # Remove containers & volumes
docker-compose up --build    # Rebuild and start all
docker-compose up user-service --build  # Rebuild specific service
```

---

## 👥 Contributors

- Dhanyamol Devassy

---

## 📌 Notes

- `mysql-init/init.sql` initializes all databases/tables
- `wait-for.sh` ensures services wait for MySQL readiness
- Each service logs DB status when ready

---

