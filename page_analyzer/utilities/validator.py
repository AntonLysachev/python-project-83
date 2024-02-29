from validators import url
from page_analyzer.CRUD.crud_utils import get_url


def validate(addres: str) -> bool:
    is_url = url(addres)
    errors = ''
    if not is_url:
        errors = 'Некорректный URL', 'danger'
    return errors
