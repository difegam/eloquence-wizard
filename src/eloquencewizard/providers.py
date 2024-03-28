from abc import abstractmethod
from enum import Enum
from typing import Literal, Optional

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr
from typing_extensions import Annotated

__all__ = [
    "OpenAIProvider",
    "AnthropicIProvider",
]


class Provider(BaseModel):
    api_key: SecretStr = Field(..., description="API key")

    def api_key_value(self) -> str:
        return self.api_key.get_secret_value()


class Model(BaseModel):
    name: str = Field(..., description="Model name")
    context_window: int
    max_output: int = Field(..., description="Max output tokens")

    def __repr__(self) -> str:
        return f"Model(name={self.name}, context_window={self.context_window}, max_output={self.max_output})"


TypeModels = Annotated[
    dict[str, Model], Field(..., description="List of available models")
]


class EnumModels(Enum):

    def __str__(self) -> str:
        return self.value

    @classmethod
    def model_names(cls) -> list[str]:
        return [model.value for model in cls]

    @property
    def model(self) -> Model:
        _models = self.models()
        if not self.value in _models:
            raise ValueError(f"Model {self.value} not found")
        return _models[self.value]

    @classmethod
    @abstractmethod
    def models(cls) -> TypeModels: ...


TypeOpenAIModels = Literal["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]


class OpenAIModels(EnumModels):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO_PREVIEW = "gpt-4-turbo-preview"

    @classmethod
    def models(cls) -> TypeModels:
        return {
            # GPT-3.5-Turbo
            cls.GPT_3_5_TURBO.value: Model(
                name=cls.GPT_3_5_TURBO.value,
                context_window=16385,
                max_output=4096,
            ),
            # GPT-4
            cls.GPT_4.value: Model(
                name=cls.GPT_4.value,
                context_window=8192,
                max_output=4096,
            ),
            # GPT-4 Turbo Preview
            cls.GPT_4_TURBO_PREVIEW.value: Model(
                name=cls.GPT_4_TURBO_PREVIEW.value,
                context_window=128000,
                max_output=4096,
            ),
        }


class OpenAIProvider(Provider):
    provider: str = Field("openai", description="OpenAI llm")
    models: dict[str, Model] = Field(
        ..., description="List of available models", default_factory=OpenAIModels.models
    )

    def chat(self, model_name: TypeOpenAIModels) -> ChatOpenAI:
        model = self.models.get(model_name)

        if not model:
            raise ValueError(f"Model {model_name} not found")

        return ChatOpenAI(
            model=model.name,
            api_key=self.api_key_value(),
            max_tokens=700,
            verbose=True,
        )


TypeAnthropicModels = Literal[
    "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
]


class AnthropicModels(EnumModels):
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"

    @classmethod
    def models(cls) -> TypeModels:
        return {
            cls.CLAUDE_3_OPUS.value: Model(
                name=cls.CLAUDE_3_OPUS.value,
                context_window=200000,
                max_output=4096,
            ),
            cls.CLAUDE_3_SONNET.value: Model(
                name=cls.CLAUDE_3_SONNET.value,
                context_window=200000,
                max_output=4096,
            ),
            cls.CLAUDE_3_HAIKU.value: Model(
                name=cls.CLAUDE_3_HAIKU.value,
                context_window=200000,
                max_output=4096,
            ),
        }


class AnthropicIProvider(Provider):
    provider: Optional[str] = Field("anthropic", description="Anthropic llm")
    models: dict[str, Model] = Field(
        ...,
        description="List of available models",
        default_factory=AnthropicModels.models,
    )

    def chat(
        self, model_name: TypeAnthropicModels, temperature: float = 0.5
    ) -> ChatAnthropic:
        model = self.models.get(model_name)

        if not model:
            raise ValueError(f"Model {model_name} not found")

        return ChatAnthropic(
            model_name=model.name,
            anthropic_api_key=self.api_key_value(),
            temperature=temperature,
        )


if __name__ == "__main__":
    print(OpenAIModels.model_names())
    print(OpenAIModels.GPT_3_5_TURBO)
    print(OpenAIModels.GPT_3_5_TURBO.model)

    print(AnthropicModels.model_names())
    print(AnthropicModels.CLAUDE_3_HAIKU)
    print(AnthropicModels.CLAUDE_3_HAIKU.model)
