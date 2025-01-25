from pickle import NONE
from typing import Any, Dict, List, Type

import instructor

from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel
from sympy import print_rcode

from app.config.settings import get_settings



from transformers import pipeline


# from langchain_groq import ChatGroq
# from langchain_core.messages import AIMessage

class LLMFactory:
    def __init__(self, provider: str):
        self.provider = provider
        self.settings = getattr(get_settings(), provider)
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        client_initializers = {
            "openai": lambda s: instructor.from_openai(OpenAI(api_key=s.api_key)),
            "anthropic": lambda s: instructor.from_anthropic(
                Anthropic(api_key=s.api_key)
            ),
            "llama": lambda s: instructor.from_openai(
                OpenAI(base_url=s.base_url, api_key=s.api_key),
                mode=instructor.Mode.JSON,
            ),
            "huggingface": lambda s: pipeline("text2text-generation", model=s.default_model),
            "groq": lambda s: ChatGroq(
                model=s.default_model,
                temperature=0.0,
                max_retries=2,
                api_key=s.api_key
            ),
        }

        initializer = client_initializers.get(self.provider)
        if initializer:
            return initializer(self.settings)
        raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Any:
        if self.provider == "groq":
            # Ensure messages are in the correct format for ChatGroq
            formatted_messages = [(msg["role"], msg["content"]) for msg in messages]
            response = self.client.invoke(formatted_messages)

            # Extract the content from the AIMessage object
            generated_text = response.content

            # Create a response with the required fields
            response_data = {
                "answer": generated_text,
                "thought_process": ["Generated response from Groq model."],
                "enough_context": True  # You can adjust this based on your logic
            }
            return response_model(**response_data)
        elif self.provider == "huggingface":
            prompt = "\n".join([msg["content"] for msg in messages])
            max_new_tokens = kwargs.get("max_tokens", self.settings.max_tokens)
            generated_text = self.client(prompt, max_length=max_new_tokens)
            return response_model(**generated_text)
        else:
            completion_params = {
                "model": kwargs.get("model", self.settings.default_model),
                "temperature": kwargs.get("temperature", self.settings.temperature),
                "max_retries": kwargs.get("max_retries", self.settings.max_retries),
                "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
                "response_model": response_model,
                "messages": messages,
            }
            return self.client.chat.completions.create(**completion_params)
