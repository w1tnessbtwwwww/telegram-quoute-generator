from telebot import telebot
import requests

from app.cfg.settings import settings

def get_user_avatar(name: str, user_id: int, client: telebot) -> bool:
    media: telebot.types.UserProfilePhotos = client.get_user_profile_photos(user_id)
    if media.total_count > 0:
        # Получаем последнюю фотографию профиля
        photo = media.photos[0][-1]
        file_id = photo.file_id

        # Получаем информацию о файле
        file_info = client.get_file(file_id)
        file_path = file_info.file_path

        # Скачиваем файл
        file_url = f'https://api.telegram.org/file/bot{settings.TELEGRAM_TOKEN}/{file_path}'
        response = requests.get(file_url)

        if response.status_code == 200:
            # Сохраняем файл на диск
            with open(f'{name}_avatar.jpg', 'wb') as f:
                f.write(response.content)
                return True
            
        return False