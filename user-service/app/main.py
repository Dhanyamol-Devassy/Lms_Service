from fastapi import FastAPI
from app.routes import router as user_router
from app.database import Base, engine
from sqlalchemy.exc import OperationalError
import time
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="User Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:5001"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Delay DB creation until app startup (not import)
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
Instrumentator().instrument(app).expose(app)

