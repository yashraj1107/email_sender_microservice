from fastapi import FastAPI
from dotenv import load_dotenv

from db.session import engine, Base
from routers.v1 import auth, campaigns

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(campaigns.router)

@app.get("/")
def root():
    return {"hello": "world"}
