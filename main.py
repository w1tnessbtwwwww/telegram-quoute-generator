import asyncio
import os
import telebot
import requests
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
        user_id = message.forward_from.id
        try:
            photos = bot.get_user_profile_photos(user_id)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                file_info = bot.get_file(file_id)
                file_path = file_info.file_path
                file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_TOKEN}/{file_path}"
                response =  requests.get(file_url)
                if response.status_code == 200:
                    with open(f"{message.forward_from.full_name}_avatar.png", "wb") as file:
                        file.write(response.content)
                else:
                    bot.send_message(message.chat.id, "Не удалось скачать аватар")
        except Exception as e:
            bot.reply_to(message, f"Ошибка!")
        # avatar = get_user_avatar(message.forward_from.username, message.forward_from.id, bot)
        image = generate_quote(QuoteModel(message.any_text, message.forward_from.username, f"{message.forward_from.full_name}"))
        if image.success:
            with open(f"temp_quotes/{message.forward_from.username}.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
            
            os.remove(f"temp_quotes/{message.forward_from.username}.png")
               
if __name__ == "__main__":

    print(f"start polling - {datetime.now()}")
    bot.infinity_polling()
