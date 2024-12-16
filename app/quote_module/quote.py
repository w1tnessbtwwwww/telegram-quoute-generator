from app.quote_module.models.quote_model import QuoteModel
from app.utils.result.result import Result, err, success
from app.utils.logger.logger import logger
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_black_rectangle(width, height):
    return Image.new('RGB', (width, height), 'black')

def add_text(image, text, font, position, fill="white", align="left"):
    draw = ImageDraw.Draw(image)
    draw.multiline_text(position, text, font=font, fill=fill, align=align)

def wrap_text(text, font, max_width):
    lines = []
    line = ""
    for word in text.split():
        if font.getbbox(line + " " + word)[2] - font.getbbox(line + " " + word)[0] > max_width:
            lines.append(line)
            line = word
        else:
            if line:
                line += " "
            line += word
    if line:
        lines.append(line)
    wrapped_text = "\n".join(lines)
    return wrapped_text

def create_avatar_circle(size, border_color='black', border_width=2):
    avatar = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    avatar_draw = ImageDraw.Draw(avatar)
    avatar_draw.ellipse((0, 0, size, size), outline=border_color, width=border_width)
    return avatar

def paste_avatar(image, avatar, position):
    image.paste(avatar, position, avatar)

def generate_image(quote_text: str, author_name: str) -> Result[None]:
    title_font = ImageFont.truetype("app/quote_module/media/Roboto-Medium.ttf", 24)
    quote_font = ImageFont.truetype("app/quote_module/media/Roboto-Medium.ttf", 20)
    author_font = ImageFont.truetype("app/quote_module/media/Roboto-Medium.ttf", 16)

    title_text = "Цитаты великих людей"
    title_bbox = title_font.getbbox(title_text)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    max_text_width = 400 - 40

    wrapped_quote = wrap_text(quote_text, quote_font, max_text_width)
    quote_lines = wrapped_quote.split('\n')
    quote_height = sum(quote_font.getbbox(line)[3] - quote_font.getbbox(line)[1] for line in quote_lines) + (len(quote_lines) - 1) * 10 

    author_text = f"© {author_name}"
    author_bbox = author_font.getbbox(author_text)
    author_width = author_bbox[2] - author_bbox[0]
    author_height = author_bbox[3] - author_bbox[1]

    padding = 20
    avatar_size = 50
    additional_padding = 20  # Дополнительный отступ между цитатой и именем автора
    width = max(title_width, max(quote_font.getbbox(line)[2] for line in quote_lines), author_width + avatar_size + padding) + 2 * padding
    height = title_height + quote_height + author_height + 4 * padding + additional_padding

    image = create_black_rectangle(width, height)

    title_position = ((width - title_width) // 2, padding)
    add_text(image, title_text, title_font, title_position)

    quote_position = ((width - max(quote_font.getbbox(line)[2] for line in quote_lines)) // 2, padding + title_height + padding)
    add_text(image, wrapped_quote, quote_font, quote_position)

    author_position = (padding + avatar_size + padding, height - author_height - padding)
    add_text(image, author_text, author_font, author_position)

    avatar = create_avatar_circle(avatar_size)
    avatar_position = (50, height - avatar_size - 50)
    # paste_avatar(image, f"{author_name}_avatar.png", avatar_position)


    image.save(f'temp_quotes/{author_name.replace("@", "")}.png')
    image.close()
def generate_quote(quote: QuoteModel) -> Result[None]:
    try:
        generate_image(quote.wrapped_quote, quote.author)
        logger.info(f"Создана цитата: Автор {quote.author}, Текст: {quote.wrapped_quote}")
        return success(None)
    except Exception as e:
        print(e)
        return err("Не удалось создать цитату. Информация уже направлена разработчикам.")
