from validators import url


def validate(addres: str) -> bool:
    is_url = url(addres)
    errors = ''
    if not is_url:
        errors = 'Некорректный URL', 'danger'
    return errors
