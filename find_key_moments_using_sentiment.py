from transformers import pipeline

# Загружаем модель для анализа тональности
sentiment_analyzer = pipeline("sentiment-analysis")

def find_key_moments_using_sentiment(segments):
    key_moments = []
    for segment in segments:
        sentiment = sentiment_analyzer(segment['text'])[0]
        # Если тональность текста положительная или имеет высокую оценку, считаем его важным
        if sentiment['label'] == 'POSITIVE' and sentiment['score'] > 0.9:
            key_moments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text']
            })
    return key_moments

# Пример использования
segments = [{'start': 0, 'end': 40, 'text': 'Это важный момент'}, {'start': 41, 'end': 80, 'text': 'Менее важный текст'}]
key_moments = find_key_moments_using_sentiment(segments)
print("Ключевые моменты:", key_moments)
