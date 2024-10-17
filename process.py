import os
import yt_dlp
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import whisper
from transformers import pipeline

def download_video(url):
    download_folder = os.path.join(os.getcwd(), "Downloads")
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'verbose': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Видео успешно скачано в папку: {download_folder}")
    except Exception as e:
        print(f"Ошибка при скачивании видео: {e}")

def get_latest_video(download_folder):
    files = os.listdir(download_folder)
    video_files = [f for f in files if f.endswith(('.mp4', '.mkv', '.webm'))]
    if video_files:
        latest_video = video_files[0]
        return os.path.join(download_folder, latest_video)
    else:
        print("Видео не найдено.")
        return None

def convert_video_to_audio(video_path):
    output_audio_path = os.path.splitext(video_path)[0] + '.mp3'
    print(f'Конвертируем видео в аудио: {video_path}')
    video_clip = VideoFileClip(video_path)
    video_clip.audio.write_audiofile(output_audio_path)
    print(f"Аудио успешно сохранено: {output_audio_path}")
    return output_audio_path

def transcribe_audio(audio_path):
    print(f'Начинаем расшифровку аудио: {audio_path}')
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print(f"Расшифровка завершена. Получен текст и сегменты.")
    return result['text'], result['segments']

def find_key_moments_using_sentiment(segments):
    print("Определяем ключевые моменты с помощью анализа тональности для русскоязычного текста...")

    # Используем модель для русского языка
    sentiment_analyzer = pipeline("sentiment-analysis", model="blanchefort/rubert-base-cased-sentiment", device=0)

    key_moments = []
    for segment in segments:
        sentiment = sentiment_analyzer(segment['text'])[0]
        if sentiment['label'] == 'POSITIVE' and sentiment['score'] > 0.9:
            key_moments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text']
            })
    print(f"Найдено {len(key_moments)} ключевых моментов.")
    return key_moments


def create_short_clip_with_subtitles(video_path, key_moments, min_duration=30, max_duration=40):
    print("Создаем короткие видео с субтитрами...")

    for moment in key_moments:
        start = moment['start']
        end = moment['end']
        text = moment['text']

        # Проверка длины фрагмента
        segment_duration = end - start
        if segment_duration < min_duration:
            # Если сегмент слишком короткий, пропускаем его
            print(f"Сегмент от {start} до {end} слишком короткий ({segment_duration} секунд), пропускаем.")
            continue
        if segment_duration > max_duration:
            # Если сегмент слишком длинный, обрезаем его до max_duration
            end = start + max_duration
            print(f"Сегмент слишком длинный, обрезаем его до {max_duration} секунд.")

        # Открываем видеофайл и вырезаем фрагмент с аудио
        video = VideoFileClip(video_path).subclip(start, end)

        # Создаем текстовый клип для субтитров
        subtitles = TextClip(text, fontsize=24, color='white')
        subtitles = subtitles.set_position('bottom').set_duration(end - start)

        # Комбинируем видео с субтитрами и сохраняем с аудио
        result = CompositeVideoClip([video, subtitles])

        # Сохраняем результат
        output_path = f"short_{start}_{end}.mp4"
        result.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"Короткий ролик сохранен в: {output_path}")
# Главный процесс
video_url = 'https://www.youtube.com/watch?v=b5UNxSESAHI'
download_video(video_url)
download_folder = 'Downloads'
video_file_path = get_latest_video(download_folder)

if video_file_path:
    audio_file_path = convert_video_to_audio(video_file_path)
    text, segments = transcribe_audio(audio_file_path)
    key_moments = find_key_moments_using_sentiment(segments)
    create_short_clip_with_subtitles(video_file_path, key_moments)
else:
    print("Не удалось найти видео для дальнейшей обработки.")