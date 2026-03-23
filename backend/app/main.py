from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import kyc_routes

app = FastAPI()

# ✅ CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(kyc_routes.router, prefix="/kyc")

@app.get("/")
def home():
    return {"message": "Backend working"}