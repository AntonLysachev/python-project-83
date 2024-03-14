from validators import url
from urllib.parse import urlparse
import requests


def validate_url(addres: str) -> list:
    errors = []
    if addres:
        is_url = url(addres)
    else:
        errors.append(("URL обязателен", "danger"))
    if not is_url:
        errors.append(("Некорректный URL", "danger"))
    return errors


def normalize_url(url: str) -> str:
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"


def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception:
        return False
    return response
