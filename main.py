from fastapi import FastAPI
from db.session import engine
import models
from dotenv import load_dotenv
from routers.v1 import auth,campaigns

models.Base.metadata.create_all(bind=engine)

load_dotenv()
app=FastAPI()

app.include_router(auth.router)
app.include_router(campaigns.router)

@app.get("/")
def root():
    return{"hello world"}