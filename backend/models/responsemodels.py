from pydantic import BaseModel

class Sentiment(BaseModel):
    score: float
    label: str

class StockResponse(BaseModel):
    ticker: str
    score: float
    sentiment: Sentiment
    explanation: str