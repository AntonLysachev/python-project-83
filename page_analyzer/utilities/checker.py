from urllib.request import urlopen
from bs4 import BeautifulSoup


def check(url: str) -> tuple:
    try:
        html = urlopen(url)
        status_code = html.getcode()
        soup = BeautifulSoup(html, 'html.parser')
        h1 = soup.h1.string if soup.h1 else ''
        title = soup.title.string if soup.title else ''
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'] if description_tag else ''
    except (Exception) as error:
        print(error)
        return '', '', '', ''
    return status_code, h1, title, description
