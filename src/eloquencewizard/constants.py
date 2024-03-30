from enum import Enum


class Language(Enum):
    AUTO: str = "auto"
    ENGLISH: str = "en"
    SPANISH: str = "es"

    def __str__(self) -> str:
        return self.value
