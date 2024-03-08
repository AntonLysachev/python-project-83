from validators import url


def validate(addres: str) -> list:
    is_url = url(addres)
    errors = []
    if not is_url:
        errors.append(('Некорректный URL', 'danger'))
    return errors
