import requests
from bs4 import BeautifulSoup


def get_content(url):
    try:
        response = requests.get(url)
    except (Exception):
        return None
    return response


def html_content(html) -> tuple:
    status_code = html.status_code
    soup = BeautifulSoup(html.content, 'html.parser')
    h1 = soup.h1.string if soup.h1 else ''
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return status_code, h1, title, description
