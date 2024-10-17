import yt_dlp
import os


def download_video(url):
    # Путь для сохранения видео
    download_folder = os.path.join(os.getcwd(), "Downloads")

    # Создаем папку, если она не существует
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Опции для скачивания
    ydl_opts = {
        'format': 'best',  # Выбираем лучший доступный формат
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Имя файла на основе названия видео
        'noplaylist': True,  # Скачивать только одно видео, если это плейлист
        'verbose': True,  # Подробные логи
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Видео успешно скачано в папку: {download_folder}")
    except Exception as e:
        print(f"Ошибка при скачивании видео: {e}")


# Пример использования
video_url = 'https://www.youtube.com/watch?v=b5UNxSESAHI'
download_video(video_url)
