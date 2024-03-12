from validators import url
from urllib.parse import urlparse
# но даже если убрать обязательность заполнения вответ будет Некорректный URL потомучто is_url пустой


def validate_url(addres: str) -> list:
    is_url = url(addres)
    errors = []
    if not is_url:
        errors.append(("Некорректный URL", "danger"))
    return errors

def normalize_url(url: str) -> str:
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"