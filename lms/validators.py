import re
from django.core.exceptions import ValidationError
from rest_framework import serializers
from urllib.parse import urlparse


def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведет на youtube.com
    """
    if not value:
        return  # Пустые значения разрешены (blank=True)
    
    parsed = urlparse(value)
    
    # Проверяем, что домен содержит youtube.com
    if 'youtube.com' not in parsed.netloc and 'youtu.be' not in parsed.netloc:
        raise serializers.ValidationError(
            "Ссылка должна вести на youtube.com. Разрешены только ссылки на YouTube."
        )


def validate_no_external_links(value):
    """
    Валидатор для проверки отсутствия ссылок на сторонние ресурсы в тексте
    (кроме youtube.com)
    """
    if not value:
        return
    
    # Ищем все URL в тексте
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, value)
    
    for url in urls:
        parsed = urlparse(url)
        # Если найдена ссылка не на youtube.com
        if 'youtube.com' not in parsed.netloc and 'youtu.be' not in parsed.netloc:
            raise serializers.ValidationError(
                "В материалах запрещены ссылки на сторонние ресурсы, кроме youtube.com"
            )


class YouTubeURLValidator:
    """
    Класс-валидатор для проверки YouTube ссылок в сериализаторах
    """
    def __init__(self, field='video_url'):
        self.field = field
    
    def __call__(self, attrs):
        field_value = attrs.get(self.field)
        if field_value:
            validate_youtube_url(field_value)

