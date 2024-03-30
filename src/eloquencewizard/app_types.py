from typing import Union

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

TypeChat = Union[ChatOpenAI, ChatAnthropic]
