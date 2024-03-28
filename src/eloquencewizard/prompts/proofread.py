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

# # Define the prompt for the OpenAI API
# PROMPT_PROOFREAD = """
#     Please proofread the following text for spelling and grammar.
#     Return the corrected text, and Python dictionary of grammar errors and rules violated.
#     If there are no errors, return simply "No errors".
#     ---
#     {text}
#     ---
#     {format_instructions}
#     """
PROMPT_PROOFREAD = """
Please proofread the following text for spelling and grammar errors.
Return the corrected text, removed words, any errors, and violations of rules.
If there are no errors, simply return "No errors."
---
{text}

{format_instructions}
"""
