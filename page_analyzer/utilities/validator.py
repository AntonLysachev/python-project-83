from urllib.parse import urlparse
from validators import url


def validate(_url: str) -> bool:
    is_url = url(_url)
    errors = ''
    if not is_url:
        errors = 'Некорректный URL', 'danger'
    return errors
