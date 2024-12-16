from app.quote_module.models.quote_model import Quote
from app.utils.result.result import Result
async def generate_quote(quote: Quote) -> Result[None]:
    ...