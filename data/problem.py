from typing import List, Literal, Optional

from pydantic import BaseModel, validator


class Problem(BaseModel):
    name: str
    type: str
    description: str
    difficulty: Literal[1, 2, 3]
    point: List[str]
    prompt: List[str]
    flag: str = ""
    comment: Optional[str] = ""

    @validator("type")
    def type_upper(cls, v: str):
        return v.upper()

    @property
    def difficulty_text(self):
        return ["简单", "中等", "困难"][self.difficulty-1]

    @property
    def point_joined(self):
        return "\n".join(
            f"{i+1}. {s}" for i, s in enumerate(self.point))
