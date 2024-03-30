from langchain.output_parsers import PydanticOutputParser
from pydantic.v1 import BaseModel, Field


# Models for the output parser
class TextError(BaseModel):
    incorrect: str = Field(description="Incorrect word or phrase")
    correct: str = Field(description="Corrected word or phrase")
    error_type: str = Field(description="Type of error")


class TextProofread(BaseModel):
    corrected_text: str = Field(description="Corrected text")
    errors: list[TextError] = Field(description="List of  errors and rules violated")


class Text(BaseModel):
    text: str = Field(description="Text to be proofread", max_length=1000)


# Define the output parser
proofread_output_parser: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=TextProofread
)

# Prompt for proofreading
PROMPT_PROOFREAD = """
Please proofread the following text for spelling and grammar errors.
Return the corrected text."
---
{text}

{format_instructions}
"""
