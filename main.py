import asyncio
import os
import telebot
from telebot.types import Message
from telebot.types import UserProfilePhotos


from app.quote_module.models.quote_model import QuoteModel
from app.utils.get_user_avatar import get_user_avatar
from app.cfg.settings import settings
from app.quote_module.quote import generate_quote
from typing import Final

from datetime import datetime


bot: telebot.TeleBot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message: telebot.types.Message):

    if message.forward_from or message.forward_from_chat:
        # avatar = get_user_avatar(message.forward_from.username, message.forward_from.id, bot)
        image = generate_quote(QuoteModel(message.any_text, message.forward_from.username))
        if image.success:
            with open(f"temp_quotes/{message.forward_from.username}.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
            
            os.remove(f"temp_quotes/{message.forward_from.username}.png")
               
if __name__ == "__main__":

    print(f"start polling - {datetime.now()}")
    bot.infinity_polling()
