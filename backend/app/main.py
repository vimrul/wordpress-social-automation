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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "WordPress Social Automation API is running!"}

# Register WordPress routes (New Line)
app.include_router(wordpress.router)
