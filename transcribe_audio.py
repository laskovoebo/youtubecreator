from moviepy.editor import AudioFileClip
import whisper
import os

def get_latest_audio(download_folder):
    files = os.listdir(download_folder)
    audio_files = [f for f in files if f.endswith('.mp3')]
    if audio_files:
        latest_audio = audio_files[0]
        return os.path.join(download_folder, latest_audio)
    else:
        print("Аудиофайл не найден.")
        return None

def split_audio(audio_path, duration=300):  # Делим на фрагменты по 300 секунд (5 минут)
    audio = AudioFileClip(audio_path)
    chunks = []
    for i in range(0, int(audio.duration), duration):
        chunk = audio.subclip(i, min(i + duration, audio.duration))
        chunk_filename = f"{audio_path}_chunk_{i // duration}.mp3"
        chunk.write_audiofile(chunk_filename)
        chunks.append(chunk_filename)
    return chunks

def transcribe_audio_chunk(audio_chunk_path, model):
    result = model.transcribe(audio_chunk_path, fp16=False)
    return result['text'], result['segments']

def transcribe_large_audio(audio_path):
    model = whisper.load_model("base")
    chunks = split_audio(audio_path)  # Разбиваем аудио на фрагменты
    all_text = ""
    for chunk in chunks:
        print(f"Распознаем фрагмент {chunk}...")
        text, segments = transcribe_audio_chunk(chunk, model)
        all_text += text + "\n"
    return all_text

# Пример использования
download_folder = 'Downloads'
audio_file_path = get_latest_audio(download_folder)

if audio_file_path:
    full_text = transcribe_large_audio(audio_file_path)
    print("Полный текст расшифровки:", full_text)
else:
    print("Не удалось найти аудиофайл для расшифровки.")
