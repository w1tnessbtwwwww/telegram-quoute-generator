from pydantic import BaseModel
from typing import Optional

class QuoteModel(BaseModel):
    quote_text: str
    author_text: str