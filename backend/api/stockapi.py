from fastapi import APIRouter, Query
from backend.services.stockservice import analyze_stock

router = APIRouter()

@router.get("/analyze")
def analyze(symbol: str = Query(..., description="Stock symbol like INFY, TCS")):
    return analyze_stock(symbol.upper())