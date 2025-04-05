from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as user_router
from routes.chat import router as chat_router
from database import create_tables, get_db

app = FastAPI(
    title="Tax Code Chat API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/api/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.get("/api/test")
async def test():
    return {"message": "Server is responding"}