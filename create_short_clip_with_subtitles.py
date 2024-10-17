from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def create_short_clip_with_subtitles(video_path, key_moments):
    for moment in key_moments:
        start = moment['start']
        end = moment['end']
        text = moment['text']

        # Открываем видеофайл и вырезаем фрагмент
        video = VideoFileClip(video_path).subclip(start, end)

        # Создаем текстовый клип для субтитров
        subtitles = TextClip(text, fontsize=24, color='white')
        subtitles = subtitles.set_position('bottom').set_duration(end - start)

        # Комбинируем видео с субтитрами
        result = CompositeVideoClip([video, subtitles])

        # Сохраняем результат
        output_path = f"short_{start}_{end}.mp4"
        result.write_videofile(output_path, codec="libx264")
        print(f"Короткий ролик сохранен в: {output_path}")
