from fastapi import FastAPI
from app.routes import router as user_router
from app.database import Base, engine
from sqlalchemy.exc import OperationalError
import time

app = FastAPI(title="User Service")

# Wait for DB to be ready before creating tables
for i in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        print("User DB connected.")
        break
    except OperationalError:
        print(f"Attempt {i+1}: Waiting for User DB...")
        time.sleep(2)

# Register routes
app.include_router(user_router)
