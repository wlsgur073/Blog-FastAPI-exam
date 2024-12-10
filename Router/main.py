from fastapi import FastAPI
from routes import item, user

app = FastAPI()

app.include_router(item.itemRouter)
app.include_router(user.router)