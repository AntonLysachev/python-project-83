from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def get_content(url):
    try:
        html = urlopen(url)
    except (Exception) as error:
        print(error)
        if isinstance(error, HTTPError):
            return error.code
        return None
    return html


def html_content(html: str) -> tuple:
    if html:
        if isinstance(html, int):
            return html, '', '', ''
        status_code = html.getcode()
        soup = BeautifulSoup(html, 'html.parser')
        h1 = soup.h1.string if soup.h1 else ''
        title = soup.title.string if soup.title else ''
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'] if description_tag else ''
        return status_code, h1, title, description
    return '', '', '', ''
