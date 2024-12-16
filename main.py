
from app.quote_module.quote import generate_quote
from app.quote_module.models.quote_model import QuoteModel


quote = "уебан" * 20

if __name__ == "__main__":
    generate_quote(QuoteModel("хуй" * 120, "@always_failure"))
