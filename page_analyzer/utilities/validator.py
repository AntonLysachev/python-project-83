from validators import url

# Мне кажется validators и так делает нужные проверки, а пустой url быть не может потомучто строка обязательна к заполнению 
def validate(addres: str) -> list:
    is_url = url(addres)
    errors = []
    if not is_url:
        errors.append(('Некорректный URL', 'danger'))
    return errors
