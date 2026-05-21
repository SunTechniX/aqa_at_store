import re
from bs4 import BeautifulSoup

def load_data(mutable_data: dict,
              tokens: str | list[str] | tuple[str],
              instance: str | list[str] | tuple[str]) -> None:
    if isinstance(tokens, str):
        mutable_data["csrftoken"] = tokens
        mutable_data["csrfinstance"] = instance
    else:
        mutable_data["csrftoken"] = tokens[0]
        mutable_data["csrfinstance"] = instance[0]


def extract_visible_errors(html: str) -> list[str]:
    """ Извлекает видимые сообщения об ошибках из HTML """
    errors = []
    # Удаляем скрипты, стили, комментарии
    clean = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    clean = re.sub(r'<script[^>]*>.*?</script>', '', clean,
                   flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean,
                   flags=re.DOTALL | re.IGNORECASE)

    patterns = [
        r'<div[^>]*class="[^"]*alert[^"]*error[^"]*"[^>]*>(?:<button[^>]*></button>)?\s*([^<]+)</div>',
        r'<div[^>]*class="[^"]*error[^"]*"[^>]*>([^<]+)</div>',
        r'<span[^>]*class="[^"]*error[^"]*"[^>]*>([^<]+)</span>',
        r'(?:^|[\s>])(Error|Warning|Notice):\s*([^<\.\n]+)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, clean, flags=re.IGNORECASE)
        for match in matches:
            text = match[-1].strip() if isinstance(match,
                                                   tuple) else match.strip()
            if text and len(
                    text) < 150 and '<' not in text and not text.startswith(
                    ('function', 'var', 'if', '$')):
                errors.append(text)
    return list(dict.fromkeys(errors))


def extract_error_text(html: str) -> str | None:
    """
    Извлекает текст ошибки из HTML с помощью BeautifulSoup.
    Ищет элементы с классами: alert-error, error, warning
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем различные типы сообщений об ошибках
    error_selectors = [
        '.alert-error',
        '.alert.alert-danger',
        '.error',
        '.warning',
        'div[class*="error"]',
        'span[class*="error"]',
        ]

    for selector in error_selectors:
        error_element = soup.select_one(selector)
        if error_element:
            # Получаем текст, убираем лишние пробелы и переносы строк
            error_text = error_element.get_text(strip=True)
            # Убираем текст кнопки "×" (close button)
            error_text = error_text.replace('×', "")
            if error_text and len(error_text) > 10:  # Фильтруем пустые/слишком короткие
                return error_text

    return None
