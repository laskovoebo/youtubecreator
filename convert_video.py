def get_latest_video(download_folder):
    # Получаем список файлов в папке Downloads
    files = os.listdir(download_folder)

    # Фильтруем только видеофайлы (расширения можно расширить по необходимости)
    video_files = [f for f in files if f.endswith(('.mp4', '.mkv', '.webm'))]

    if video_files:
        latest_video = video_files[0]  # Берём первый файл
        return os.path.join(download_folder, latest_video)
    else:
        print("Видео не найдено.")
        return None


def convert_video_to_audio(video_path, output_audio_path=None):
    try:
        if output_audio_path is None:
            output_audio_path = os.path.splitext(video_path)[0] + '.mp3'

        print(f'Преобразование видео: {video_path} в аудио: {output_audio_path}')

        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(output_audio_path)

        print(f"Аудио успешно сохранено в: {output_audio_path}")
        return output_audio_path
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")


# Пример использования
download_folder = 'Downloads'
video_file_path = get_latest_video(download_folder)

if video_file_path:
    convert_video_to_audio(video_file_path)
else:
    print("Не удалось найти видео для конвертации.")
