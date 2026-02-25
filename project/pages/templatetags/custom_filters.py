from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# Список нецензурных слов (можно дополнить)
CENSORED_WORDS = ['редиска', 'дурак', 'негодяй', 'подлец']


@register.filter(name='censor')
@stringfilter  # проверяет, что значение - строка
def censor(value):
    """
    Заменяет нецензурные слова на звёздочки
    """
    words = value.split()
    result = []

    for word in words:
        word_lower = word.lower()
        is_censored = False

        # Проверяем, есть ли слово в списке запрещённых
        for censor_word in CENSORED_WORDS:
            if censor_word in word_lower:
                # Заменяем буквы на звёздочки, сохраняя первую букву
                first_letter = word[0]
                censored_part = '*' * (len(word) - 1)
                result.append(first_letter + censored_part)
                is_censored = True
                break

        if not is_censored:
            result.append(word)

    return ' '.join(result)