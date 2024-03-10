from validators import url

#пустым адрес не будет потому что поле обязательно к заполнению, форма без него не отправится

def address(addres: str) -> list:
    is_url = url(addres)
    errors = []
    if not is_url:
        errors.append(('Некорректный URL', 'danger'))
    return errors
