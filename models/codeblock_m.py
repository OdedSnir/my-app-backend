from pydantic import BaseModel
from typing import Optional

class CodeBlock(BaseModel):
    title: str
    initial_code: str
    solution: str