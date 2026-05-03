from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse 
from utils.logger import logger
import asyncio
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
        
        analysis_task = asyncio.to_thread(analyze_fundamentals, data)
        news_task = asyncio.to_thread(get_news_with_sentiment, symbol)

        analysis, news_data = await asyncio.gather(
        analysis_task,
        news_task
        )

        logger.info(f"Analysis: {analysis}")
        sentiment = analyze_sentiment(news_data["articles"])
        
        logger.info(f"Sentiment: {sentiment}")

        return {
            "data": data,
            "ticker": symbol,
            "analysis": analysis,
            "sentiment": sentiment
        }
            
        
    except Exception as e:
        return {
            "error": str(e)
        }
        
        

@router.get("/analyze-stream/{symbol}")
async def analyze_stock_stream(symbol: str, request: Request):

    # -----------------------------
    # 1. SAFE DATA FETCH
    # -----------------------------
    try:
        data = fetch_complete_stock_data(symbol)

        if not data or data.get("price") is None:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid or unavailable stock data for symbol: {symbol}"
            )

        analysis = analyze_fundamentals(data)

        news_data = get_news_with_sentiment(symbol)
        sentiment = analyze_sentiment(news_data["articles"])

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Data processing failed: {str(e)}"
        )

    # -----------------------------
    # 2. STREAM GENERATOR (SAFE)
    # -----------------------------
    async def generator():
        try:
            async for chunk in stream_explanation({
                "ticker": symbol,
                "analysis": analysis,
                "financials": data,
                "ratios": {
                    "pe": data.get("pe_ratio"),
                    "roe": data.get("roe"),
                    "de_ratio": data.get("de_ratio")
                },
                "sentiment": sentiment
            }):

                if await request.is_disconnected():
                    print("Client disconnected")
                    break

                yield chunk

                # small async yield to event loop
                await asyncio.sleep(0)

        except Exception as e:
            error_msg = f"\n\n[ERROR] LLM streaming failed: {str(e)}\n"
            yield error_msg

    # -----------------------------
    # 3. RETURN STREAM
    # -----------------------------
    return StreamingResponse(
        generator(),
        media_type="text/plain"
    )
@router.get("/news/{symbol}")
def get_news(symbol: str):
    news_data = get_news_with_sentiment(symbol)
    return news_data