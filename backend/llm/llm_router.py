from backend.llm.local_llm import generate_local_async, stream_local
from backend.llm.groq_llm import generate_groq_async, stream_groq
from config.settings import settings
from utils.logger import logger


# Normal async response
async def generate_response_async(prompt: str) -> str:

    if settings.LLM_PROVIDER == "local":
        try:
            return await generate_local_async(prompt)

        except Exception as e:
            logger.warning(f"Local failed → Groq fallback: {e}")
            if settings.GROQ_API_KEY:
                return await generate_groq_async(prompt)
            raise

    elif settings.LLM_PROVIDER == "groq":
        return await generate_groq_async(prompt)


# Streaming router
async def stream_response(prompt: str):

    if settings.LLM_PROVIDER == "local":
        try:
            async for chunk in stream_local(prompt):
                yield chunk

        except Exception as e:
            logger.warning(f"Streaming fallback → Groq: {e}")
            async for chunk in stream_groq(prompt):
                yield chunk

    elif settings.LLM_PROVIDER == "groq":
        async for chunk in stream_groq(prompt):
            yield chunk