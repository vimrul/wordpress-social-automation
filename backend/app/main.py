from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import wordpress  # New Import

app = FastAPI(
    title="WordPress Social Automation",
    description="Automate posting WordPress content to Twitter & Facebook",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # explicitly allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "WordPress Social Automation API is running!"}

# Register WordPress routes (New Line)
app.include_router(wordpress.router)

# Import Auth Router
from app.api import wordpress, auth

# Add Auth router
app.include_router(auth.router)

from app.api import wordpress, auth, social  # clearly import social

app.include_router(social.router)  # clearly register router
