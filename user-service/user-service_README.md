# User Service

This service handles user registration, login with JWT, and user management.

## 📁 Structure
```
user-service/
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

## 🔧 Environment Variables (`.env`)
```
Create a `.env` file using the template below. You can copy it from `.env.example`:

```env
DB_USER=
DB_PASSWORD=
DB_HOST=mysql
DB_PORT=3306
DB_NAME=
DATABASE_URL=

# JWT Authentication
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=
JWT_SECRET_KEY=
```

## 🚀 Endpoints
- `POST /users/` — Register user
- `POST /users/login` — Login user (returns JWT)
- `GET /users/` — List all users
- `GET /users/{id}` — Get user by ID
- `PUT /users/{id}` — Update user
- `DELETE /users/{id}` — Delete user
