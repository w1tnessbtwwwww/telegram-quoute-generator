from app.quote_module.models.quote_model import QuoteModel
from app.utils.result.result import Result, err, success
from app.utils.logger.logger import logger
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_black_rectangle(width, height):
    return Image.new('RGB', (width, height), 'black')

def add_text(image, text, font, position, fill="white"):
    draw = ImageDraw.Draw(image)
    draw.text(position, text, font=font, fill=fill)

def wrap_text(text, font, max_width):
    lines = textwrap.wrap(text, width=max_width)
    wrapped_text = "\n".join(lines)
    return wrapped_text

def create_avatar_circle(size, border_color='black', border_width=2):
    avatar = Image.new('RGB', (size, size), 'white')
    avatar_draw = ImageDraw.Draw(avatar)
    avatar_draw.ellipse((0, 0, size, size), outline=border_color, width=border_width)
    return avatar

def paste_avatar(image, avatar, position):
    image.paste(avatar, position)

def generate_image(quote_text: str, 
                   author_name: str, 
                   avatar_size: int = 400, 
                   width: int = 400, 
                   height: int = 600) -> Result[None]:
    """Генерирует конечное изображение."""
    # Создаем черный прямоугольник
    image = create_black_rectangle(width, height)

    # Загружаем шрифты
    title_font = ImageFont.truetype("app/quote_module/media/Roboto-Medium.ttf", 24)
    quote_font = ImageFont.truetype("app/quote_module/media/Roboto-Medium.ttf", 20)
    author_font = ImageFont.truetype("app/quote_module/media/Roboto-Medium.ttf", 16)

    title_text = "Цитаты великих людей"
    title_width, _ = title_font.getmask(title_text)
    title_position = ((width - title_width) // 2, 10)
    add_text(image, title_text, title_font, title_position)

    max_width = width - 20
    wrapped_quote = wrap_text(quote_text, quote_font, max_width)
    quote_width, quote_height = quote_font.getsize_multiline(wrapped_quote)
    quote_position = ((width - quote_width) // 2, (height - quote_height) // 2)
    add_text(image, wrapped_quote, quote_font, quote_position)

    author_text = f"© {author_name}"
    author_width, author_height = author_font.getsize(author_text)
    author_position = ((width - author_width) // 2, height - author_height - 10)
    add_text(image, author_text, author_font, author_position)

    avatar = create_avatar_circle(avatar_size)
    avatar_position = (50, height - avatar_size - 50)
    # paste_avatar(image, f"{author_name}.png", avatar_position)
    image.save(f'{author_name}.png')
    image.show()


def generate_quote(quote: QuoteModel) -> Result[None]:
    try:
        generate_image(quote.quote_text, quote.author_text)
        return success()
    except Exception as e:
        logger.error(e)
        return err("Не удалось создать цитату. Информация уже направлена разработчикам.")