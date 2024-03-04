from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup


def get_content(url):
    try:
        html = urlopen(url)
    except (Exception) as error:
        print(error)
        if isinstance(error, URLError):
            return None
        return error.code
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
