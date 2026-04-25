import os
from openai import OpenAI
from dotenv import load_dotenv
import os

# loads .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_explanation(data):
    """
    data = {
        "ticker": "AAPL",
        "score": 78,
        "financials": {...},
        "ratios": {...},
        "sentiment": {...}
    }
    """

    prompt = f"""
You are a senior equity research analyst.

Analyze the following stock:

Ticker: {data['ticker']}
Score: {data['analysis']['score']}/100

Key Metrics:
{data['ratios']}

Financial Summary:
{data['financials']}

News Sentiment:
Score: {data['sentiment']['score']}
Label: {data['sentiment']['label']}

Tasks:
1. Explain WHY this stock received this score
2. Highlight strengths and weaknesses
3. Interpret sentiment impact
4. Give a professional summary (Buy/Hold/Avoid style — NOT financial advice)

Be concise but insightful.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # cost-efficient
        messages=[
            {"role": "system", "content": "You are a professional stock analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content