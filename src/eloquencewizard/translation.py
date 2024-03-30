from app_types import TypeChat
from constants import Language
from langchain_core.prompts import ChatPromptTemplate


def translate(
    chat: TypeChat,
    text: str,
    *,
    input_language: str,
    output_language: str,
) -> dict:

    system = "You are a helpful assistant that translates {input_language} to {output_language}."
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    return chain.invoke(
        {
            "input_language": input_language,
            "output_language": output_language,
            "text": text,
        }
    )


if __name__ == "__main__":
    from providers import anthropic, openai

    chat = anthropic.chat(model_name="claude-3-haiku-20240307", temperature=0)
    chat = openai.chat(model_name="gpt-3.5-turbo", temperature=0)
    text = "I love Python"
    output = translate(
        chat,
        text,
        input_language=Language.ENGLISH.value,
        output_language=Language.SPANISH.value,
    )
    print(output)
