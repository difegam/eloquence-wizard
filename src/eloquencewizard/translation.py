from langchain_core.prompts import ChatPromptTemplate
from providers import AnthropicIProvider
from settings import settings

anthropic = AnthropicIProvider(api_key=settings.ANTHROPIC_API_KEY)
# chat = ChatAnthropic(
#     temperature=0,
#     anthropic_api_key=settings.ANTHROPIC_API_KEY,
#     model_name="claude-3-haiku-20240307",
# )
chat = anthropic.chat(model_name="claude-3-haiku-20240307", temperature=0)
system = (
    "You are a helpful assistant that translates {input_language} to {output_language}."
)
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat
print(
    chain.invoke(
        {
            "input_language": "English",
            "output_language": "Spanish",
            "text": "I love Python",
        }
    )
)
