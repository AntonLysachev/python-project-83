from validators import url

#но даже если убрать обязательность заполнения вответ будет Некорректный URL потомучто is_url пустой

def validate_url(addres: str) -> list:
    is_url = url(addres)
    errors = []
    if not is_url:
        errors.append(("Некорректный URL", "danger"))
    return errors
