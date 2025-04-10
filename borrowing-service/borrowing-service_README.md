# Borrowing Service

Manages book borrowing and return operations.

## 📁 Structure
```
borrowing-service/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── .env
├── Dockerfile
├── requirements.txt
└── wait-for.sh
```

## 🔐 Environment Configuration

Copy `.env.example` to `.env` and fill in your own values:

```env
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=mysql
DB_PORT=3306
DB_NAME=your_database_name
DATABASE_URL=mysql+mysqlconnector://your_database_username:your_database_password@mysql:3306/your_database_name

```

## 🚀 Endpoints
- `POST /borrow` — Borrow a book
- `PUT /return/{borrow_id}` — Return a book
