from groq import AsyncGroq
from config.settings import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)


async def generate_groq_async(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional financial analyst."},
                {"role": "user", "content": prompt}
            ],
            model=settings.GROQ_MODEL,
            temperature=0.4,
            max_tokens=800  # IMPORTANT
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR RAW:", e)
        raise RuntimeError(f"Groq error: {e}")


async def stream_groq(prompt: str):
    stream = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=settings.GROQ_MODEL,
        stream=True,
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content