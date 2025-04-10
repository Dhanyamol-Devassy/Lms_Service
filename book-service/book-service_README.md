# Book Service

Handles CRUD operations for books in the LMS.

## 📁 Structure
```
book-service/
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

## 🔐 .env Configuration
```
Copy `.env.example` and create your own `.env` file:

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=mysql
DB_PORT=3306
DB_NAME=your_database_name
DATABASE_URL=mysql+mysqlconnector://your_db_user:your_db_password@mysql:3306/your_database_name
```

## 🚀 Endpoints
- `POST /books/` — Add a book
- `GET /books/` — List books
- `GET /books/{id}` — Get book details
- `PUT /books/{id}` — Update book
- `DELETE /books/{id}` — Remove book
