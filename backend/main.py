from fastapi import FastAPI
from backend.api.analyze import router as analyze_router

app = FastAPI(title="Stock AI System")

@app.get("/")
def root():
    return {"message": "Stock AI running"}

# Register routes
app.include_router(analyze_router, prefix="/api/v1")