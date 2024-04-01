from typing import Literal

from langchain_openai import ChatOpenAI
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]





class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    OPENAI_API_KEY: str = Field(
        ..., description="OpenAI API Key", pattern=r"^sk-[a-zA-Z0-9]{48}$"
    )
    ANTHROPIC_API_KEY: str = Field(..., description="Anthropic API Key")

    def get_api_key(self, api_type: Literal["anthropic", "openai"]) -> str:
        api_keys = {"openai": self.OPENAI_API_KEY, "anthropic": self.ANTHROPIC_API_KEY}

        if not api_type in api_keys:
            raise ValueError(f"Invalid API type: {api_type}")

        return api_keys[api_type]

    @property
    def llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=self.OPENAI_API_KEY,
            max_tokens=700,
            verbose=True,
        )

    @classmethod
    def gets(cls) -> "Settings":
        return cls()


settings = Settings.gets()


if __name__ == "__main__":
    print(settings)
