from urllib.request import urlopen
from urllib import error

def check(url):
    try:
        status_code = urlopen(url).getcode()
    except (Exception) as error:
        print(error)
        return False
    return status_code

