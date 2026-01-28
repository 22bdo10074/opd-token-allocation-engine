from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="OPD Token Allocation Engine")

@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "OPD Token Allocation Engine is up"
    }

app.include_router(router)
