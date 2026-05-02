import httpx
import json
from config.settings import settings

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


async def generate_local_async(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )

            response.raise_for_status()
            data = response.json()

            return data.get("response", "").strip()

    except Exception as e:
        # raise RuntimeError(f"Ollama error: {str(e)}")
        print("OLLAMA ERROR:", e)
        raise


async def stream_local(prompt: str):
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": True
            }
        ) as response:

            async for line in response.aiter_lines():
                if line:
                    try:
                        chunk = json.loads(line)  # Ollama returns JSON-like lines
                        yield chunk.get("response", "")
                    except:
                        continue