from fastapi import FastAPI
from uvicorn import run
from routes import router as auth_router
from database import Base, engine

app = FastAPI()

app.include_router(auth_router)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    run('main:app', reload=True)