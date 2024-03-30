import re

from app_types import TypeChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from prompts.proofread import PROMPT_PROOFREAD, Text
from prompts.proofread import proofread_output_parser as parser


def proofread(llm: TypeChat, text: str):
    _text = Text(text=text)
    messages = [
        SystemMessagePromptTemplate.from_template(
            template="You are a helpful linguist AI assistant."
        ),
        HumanMessagePromptTemplate.from_template(
            template=PROMPT_PROOFREAD,
        ),
    ]
    # Define the prompt for the OpenAI API
    chat_prompt_template = ChatPromptTemplate.from_messages(messages)

    # Format the prompt with the text and format instructions
    chat_prompt_with_values = chat_prompt_template.format_prompt(
        text=_text,
        format_instructions=parser.get_format_instructions(),
    )

    # Call the OpenAI API with the formatted prompt
    output = llm(chat_prompt_with_values.to_messages())
    return parser.parse(output.content)


def remove_special_characters(text: str) -> str:
    return re.sub("[^A-Za-z0-9]+", " ", text)


def text_differences(original_text: str, corrected_text: str) -> set[str]:
    # Remove special characters from the text
    original = remove_special_characters(original_text).split()
    corrected = remove_special_characters(corrected_text).split()
    return set(original) - set(corrected)


if __name__ == "__main__":

    text = "How kan I fidn to the nearest hospital"

    # out = proofread(llm=settings.llm, text=text)
    # print(out)

    corrected_text = "How can I find the nearest hospital?"
    differences = text_differences(text, corrected_text)
    print(differences)
