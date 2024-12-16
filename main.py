
from app.quote_module.quote import generate_quote
from app.quote_module.models.quote_model import QuoteModel
if __name__ == "__main__":
    generate_quote(QuoteModel(
        quote_text="ggg",
        author_text="w1tnessbtw"
    ))