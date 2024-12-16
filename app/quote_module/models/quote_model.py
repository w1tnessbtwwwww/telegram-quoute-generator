from pydantic import BaseModel
from typing import Optional



class QuoteModel:
    def __init__(self, quote: str, author: str):
        self.quote = quote
        self.author = author

    @property
    def wrapped_quote(self, chunk_size=50):
        parts = [self.quote[i:i+chunk_size] for i in range(0, len(self.quote), chunk_size)]
        result = '\n'.join(parts)
        return result