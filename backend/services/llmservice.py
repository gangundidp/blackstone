from backend.llm.llm_router import generate_response_async, stream_response
import json

def clean_data(data: dict) -> str:
    return json.dumps(data, default=str, indent=2)

# Async full response
async def generate_explanation(data: dict) -> str:

    score = data.get("analysis", {}).get("score", 0)
    score_100 = round(score * 20, 2)

    prompt = f"""
You are a senior equity research analyst.

Ticker: {data['ticker']}
Score: {score_100}/100

Key Metrics:
{clean_data(data['ratios'])}

Financial Summary:
{clean_data(data['financials'])}

News Sentiment:
Score: {clean_data(data['sentiment']['score'])}
Label: {clean_data(data['sentiment']['label'])}

Return structured analysis.
"""

    return await generate_response_async(prompt)


# Streaming version
async def stream_explanation(data: dict):

    score = data.get("analysis", {}).get("score", 0)
    score_100 = round(score * 20, 2)

    prompt = f"""
You are a senior equity research analyst.

Ticker: {data['ticker']}
Score: {score_100}/100

Key Metrics:
{clean_data(data['ratios'])}

Financial Summary:
{clean_data(data['financials'])}

News Sentiment:
Score: {clean_data(data['sentiment']['score'])}
Label: {clean_data(data['sentiment']['label'])}

Return structured analysis.
"""

    async for chunk in stream_response(prompt):
        yield chunk