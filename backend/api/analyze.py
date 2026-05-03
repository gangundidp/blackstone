from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse 
from utils.logger import logger
from backend.services.dataservice import fetch_complete_stock_data
from backend.analysis.fundamentalanalysis import analyze_fundamentals
# from backend.agents.explanationagent import generate_explanation
from backend.services.newsservice import get_news_with_sentiment
from backend.services.sentimentservice import analyze_sentiment
from backend.services.llmservice import generate_explanation, stream_explanation

router = APIRouter()

@router.get("/llm-health")
async def llm_health():
    from backend.llm.local_llm import generate_local_async

    try:
        res = await generate_local_async("Hello")
        return {"status": "ok", "response": res[:50]}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@router.get("/analyze/{symbol}")
async def analyze_stock(symbol: str):
    try:
        data = fetch_complete_stock_data(symbol)
        
        if data["price"] is None:
            raise HTTPException(
            status_code=400,
            detail=f"Invalid or unavailable stock data for symbol: {symbol}"
        )

        logger.info(f"Analyzing stock: {symbol}")
        logger.info(f"Fetched data: {data}")
        
        analysis = analyze_fundamentals(data)
        logger.info(f"Analysis: {analysis}")
        # explanation = generate_explanation(data, analysis)
        
        news_data = get_news_with_sentiment(symbol)

        sentiment = analyze_sentiment(news_data["articles"])

        try:
            explanation = await generate_explanation({
                "ticker": symbol,
                "analysis": analysis,
                "financials": data,
                "ratios": {
                    "pe": data.get("pe"),
                    "roe": data.get("roe"),
                    "de_ratio": data.get("de_ratio")
                },
                "sentiment": sentiment
            })
        except Exception as e:
            explanation = f"""
LLM unavailable.

Quick Summary:
- Rating: {analysis.get('rating')}
- Score: {analysis.get('score')}
- Sentiment: {sentiment.get('label')}

This stock shows {'strong' if analysis.get('score',0) > 70 else 'moderate'} fundamentals.
"""        

        return {
            "data": data,
            "ticker": symbol,
            "analysis": analysis,
            "sentiment": sentiment,
            "explanation": explanation,
            "news": news_data
        }
            
        
    except Exception as e:
        return {
            "error": str(e)
        }
        
        
@router.get("/analyze-stream/{symbol}")
async def analyze_stock_stream(symbol: str):

    data = fetch_complete_stock_data(symbol)
    analysis = analyze_fundamentals(data)
    news_data = get_news_with_sentiment(symbol)
    sentiment = analyze_sentiment(news_data["articles"])

    async def generator():
        async for chunk in stream_explanation({
            "ticker": symbol,
            "analysis": analysis,
            "financials": data,
            "ratios": {
                "pe": data.get("pe"),
                "roe": data.get("roe"),
                "de_ratio": data.get("de_ratio")
            },
            "sentiment": sentiment
        }):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")