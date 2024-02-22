from urllib.parse import urlparse
from page_analyzer.CRUD.crud_utils import get_field


def validate(url: str) -> bool:
    pars_url = urlparse(url)
    errors = ''
    if get_field('urls', 'name', url):
        errors = 'Страница уже существует'
    else:
        if not pars_url.scheme:
            errors = 'Некорректный URL'
        if not pars_url.netloc:
            errors = 'Некорректный URL'
        elif '.' not in pars_url.netloc:
            errors = 'Некорректный URL'
    return errors
    