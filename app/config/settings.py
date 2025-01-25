import logging
import os
from datetime import timedelta
from functools import lru_cache
from typing import Optional
from langfuse import Langfuse

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


def setup_logging():
    """Configure basic logging for the application."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

class LangfuseSettings(BaseModel):
    """
    Langfuse-specific settings.
    """

    public_key: str = Field(default_factory=lambda: os.getenv("LANGFUSE_PUBLIC_KEY"))
    secret_key: str = Field(default_factory=lambda: os.getenv("LANGFUSE_SECRET_KEY"))
    host: str = Field(default_factory=lambda: os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"))

    def get_client(self):
        """
        Returns an instance of the Langfuse client.
        """
        from langfuse import Langfuse

        if not self.public_key or not self.secret_key:
            logger.error("Langfuse public key or secret key is missing in environment variables.")
            raise ValueError("Langfuse public key or secret key is missing in environment variables.")

        try:
            return Langfuse(
                public_key=self.public_key,
                secret_key=self.secret_key,
                host=self.host,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Langfuse client: {e}")
            raise

class LLMSettings(BaseModel):
    """Base settings for Language Model configurations."""

    temperature: float = 0.0
    max_tokens: Optional[int] = 8000
    max_retries: int = 3

class HuggingFaceSettings(LLMSettings):
    """Hugging Face-specific settings extending LLMSettings."""

    api_key: str = Field(default_factory=lambda: os.getenv("HUGGINGFACE_API_KEY"))
    default_model: str = Field(default="aiplanet/buddhi-128k-chat-7b")

class GroqSettings(LLMSettings):
    """Groq-specific settings extending LLMSettings."""

    api_key: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY"))
    default_model: str = Field(default="gemma2-9b-it")  # Replace with the actual model name

    
class OpenAISettings(LLMSettings):
    """OpenAI-specific settings extending LLMSettings."""
 
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    default_model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-3-small")


class DatabaseSettings(BaseModel):
    """Database connection settings."""

    service_url: str = Field(default_factory=lambda: os.getenv("TIMESCALE_SERVICE_URL"))


class VectorStoreSettings(BaseModel):
    """Settings for the VectorStore."""

    table_name: str = "embeddings"
    embedding_dimensions: int = 1536
    time_partition_interval: timedelta = timedelta(days=7)


class Settings(BaseModel):
    """Main settings class combining all sub-settings."""

    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)
    huggingface: HuggingFaceSettings = Field(default_factory=HuggingFaceSettings)
    groq: GroqSettings = Field(default_factory=GroqSettings)
    langfuse: LangfuseSettings = Field(default_factory=LangfuseSettings)

@lru_cache()
def get_settings() -> Settings:
    """Create and return a cached instance of the Settings."""
    settings = Settings()
    setup_logging()
    return settings


