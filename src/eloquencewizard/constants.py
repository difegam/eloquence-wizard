"""

Credits:
- List of ISO 639 language codes and their native names
    - https://gist.github.com/joshuabaker/d2775b5ada7d1601bcd7b31cb4081981
"""

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


def get_lang_index(languages: tuple, language) -> int:
    if language not in languages:
        return 0
    return languages.index(language)


class LanguageInfo(BaseModel):
    name: str
    code: str
    native: str


class Language(BaseModel):
    """Dict of ISO 639 language codes and their native name"""

    languages: Optional[dict[str, LanguageInfo]] = Field(default_factory=dict)

    @classmethod
    def default_lang(cls) -> dict[str, LanguageInfo]:
        return cls().load_from_json()

    def load_from_json(
        self, file_path: str = "src/eloquencewizard/languages.json"
    ) -> dict[str, LanguageInfo]:
        file_content = Path(file_path).read_text()
        self.languages = {
            lang["name"]: LanguageInfo.model_validate(lang)
            for lang in json.loads(file_content)
        }
        return self.languages


if __name__ == "__main__":
    lang = Language().default_lang()
    print(lang)
