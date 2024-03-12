from bs4 import BeautifulSoup


def get_info_site(response) -> tuple:
    status_code = response.status_code
    soup = BeautifulSoup(response.content, "html.parser")
    h1 = soup.h1.string if soup.h1 else ""
    title = soup.title.string if soup.title else ""
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"] if description_tag else ""
    return status_code, h1, title, description
