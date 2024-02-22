from urllib.parse import urlparse
from page_analyzer.CRUD.crud_utils import get_field


def validate(url: str) -> bool:
    pars_url = urlparse(url)
    errors = ''
    if not pars_url.scheme:
        errors = 'Некорректный URL', 'danger'
    if not pars_url.netloc:
        errors = 'Некорректный URL', 'danger'
    elif '.' not in pars_url.netloc:
            errors = 'Некорректный URL', 'danger'
    return errors
    