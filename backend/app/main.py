from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api import wordpress, auth, social
from app.core.config import settings  # ✅ Add this

app = FastAPI(
    title="WordPress Social Automation",
    description="Automate posting WordPress content to Twitter & Facebook",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)  # ✅ No more NameError

# Root
@app.get("/")
async def root():
    return {"message": "WordPress Social Automation API is running!"}

# Routers
app.include_router(wordpress.router)
app.include_router(auth.router)
app.include_router(social.router)
