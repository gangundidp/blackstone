from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_PROVIDER: str = "local"
    OLLAMA_MODEL: str = "qwen2.5:3b"

    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama3-8b-8192"

    class Config:
        env_file = ".env"

settings = Settings()