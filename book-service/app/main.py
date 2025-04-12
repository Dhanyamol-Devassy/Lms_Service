from fastapi import FastAPI
from app.routes import router as book_router
from app.database import Base, engine
from sqlalchemy.exc import OperationalError
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

import time

app = FastAPI(title="Book Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wait for DB to be ready
for i in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        print("Book DB connected.")
        break
    except OperationalError:
        print(f"Attempt {i+1}: Waiting for Book DB...")
        time.sleep(2)

# Include the router
app.include_router(book_router)
Instrumentator().instrument(app).expose(app)
